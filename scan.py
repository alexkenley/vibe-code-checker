import argparse
import os
import subprocess
import sys
import shutil
import json
import re
import logging
import time
import threading
from datetime import datetime

# Supported languages (lowercase)
SUPPORTED_LANGUAGES = ["python", "javascript", "typescript", "go", "ruby"]
REPORT_FILENAME = "vibe_scan_report.md"
JSON_REPORT_FILENAME = "vibe_scan_report.json"
LOG_FILENAME = "vibe_scan_log.txt"

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILENAME, mode='w'),
        logging.StreamHandler(sys.stderr)
    ]
)
logger = logging.getLogger("vibe_scanner")

# --- Progress Indicator ---

class Spinner:
    """Simple spinner to show progress during long-running operations."""
    def __init__(self, message="Processing"):
        self.message = message
        self.spinning = False
        self.spinner_chars = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
        self.spinner_thread = None

    def spin(self):
        i = 0
        while self.spinning:
            sys.stdout.write(f"\r{self.message} {self.spinner_chars[i]} ")
            sys.stdout.flush()
            time.sleep(0.1)
            i = (i + 1) % len(self.spinner_chars)

    def start(self, message=None):
        if message:
            self.message = message
        self.spinning = True
        self.spinner_thread = threading.Thread(target=self.spin)
        self.spinner_thread.daemon = True
        self.spinner_thread.start()

    def stop(self, message=None):
        self.spinning = False
        if self.spinner_thread:
            self.spinner_thread.join()
        if message:
            sys.stdout.write(f"\r{message}{' ' * 20}\n")
        else:
            sys.stdout.write(f"\r{' ' * (len(self.message) + 10)}\r")
        sys.stdout.flush()

# Global spinner instance
spinner = Spinner()

def print_section(title):
    """Print a section header with formatting to make it stand out."""
    width = 80
    print("\n" + "=" * width)
    print(f" {title} ".center(width, "="))
    print("=" * width + "\n")

# --- Tool Execution Helpers ---

def is_tool_installed(name):
    """Check whether `name` is on PATH and marked as executable."""
    return shutil.which(name) is not None

def check_prerequisite(command, install_guide, language=None):
    """
    Check if a prerequisite tool is installed and provide helpful feedback if not.
    Returns True if installed, False otherwise.
    """
    if not shutil.which(command):
        logger.error(f"\nERROR: Required tool '{command}' not found.")
        logger.error(f"  {install_guide}")
        if language:
            logger.error(f"  This tool is required for {language} code scanning.")
        logger.error("  Please see README.md for more information on setting up prerequisites.")
        return False
    return True

def _run_command_and_capture(command, cwd):
    """Runs a command and returns its stdout, stderr, and return code."""
    print(f"Running command: {' '.join(command)}")
    
    # Create a copy of the current environment
    env = os.environ.copy()
    
    # Add common Node.js installation paths to PATH if running Node.js tools
    if command[0] in ["npx", "npm", "node", "retire"]:
        nodejs_paths = [
            r"C:\Program Files\nodejs",
            r"C:\Program Files (x86)\nodejs",
            os.path.expanduser(r"~\AppData\Roaming\npm")
        ]
        
        # Add these paths to the PATH environment variable
        path_sep = os.pathsep  # ; on Windows, : on Unix
        for nodejs_path in nodejs_paths:
            if os.path.exists(nodejs_path) and nodejs_path not in env["PATH"]:
                env["PATH"] = nodejs_path + path_sep + env["PATH"]
    
    try:
        # Run the command and capture output
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd=cwd,
            env=env  # Use our modified environment
        )
        stdout, stderr = process.communicate()
        return {"stdout": stdout, "stderr": stderr, "returncode": process.returncode}
    except FileNotFoundError:
        logger.error(f"ERROR: Command not found - '{command[0]}'. Please ensure it is installed and in your PATH.")
        return {"stdout": None, "stderr": None, "returncode": -1}
    except Exception as e:
        logger.error(f"ERROR: Failed to run command: {e}")
        return {"stdout": None, "stderr": str(e), "returncode": -1}

# --- Core Logic Functions ---

def detect_language(project_path, specified_language):
    """
    Detects the primary language of the project.
    Priority: User-specified > File-based detection.
    Returns the detected language (lowercase string) or None if undetectable.
    """
    # 1. Check user-specified language
    if specified_language:
        lang = specified_language.lower()
        if lang in SUPPORTED_LANGUAGES:
            print(f"Using specified language: {lang}")
            return lang
        else:
            print(f"Warning: Specified language '{specified_language}' is not supported. Trying auto-detection.", file=sys.stderr)
            # Fall through to auto-detection

    # 2. File-based detection (simple checks in root directory)
    print("Attempting language auto-detection...")

    # Check for TypeScript config first (strong indicator)
    if os.path.exists(os.path.join(project_path, "tsconfig.json")):
        print("Detected TypeScript (found tsconfig.json).")
        return "typescript"

    # Check for JavaScript package manager file
    if os.path.exists(os.path.join(project_path, "package.json")):
        # Could be JS or TS. If tsconfig wasn't found, assume JS for now.
        # A more robust check could look for .js/.ts files.
        print("Detected JavaScript (found package.json, no tsconfig.json).")
        return "javascript"

    # Check for Python dependency file
    if os.path.exists(os.path.join(project_path, "requirements.txt")):
        print("Detected Python (found requirements.txt).")
        return "python"

    # Check for Go module file
    if os.path.exists(os.path.join(project_path, "go.mod")):
        print("Detected Go (found go.mod).")
        return "go"

    # Check for Ruby dependency file
    if os.path.exists(os.path.join(project_path, "Gemfile")):
        print("Detected Ruby (found Gemfile).")
        return "ruby"

    # Basic check for common source files if primary indicators fail
    try:
        for item in os.listdir(project_path):
            if item.endswith(".py"):
                print("Detected Python (found .py files).")
                return "python"
            # Check for .ts/.tsx before .js
            if item.endswith((".ts", ".tsx")):
                 print("Detected TypeScript (found .ts/.tsx files, no tsconfig.json).")
                 return "typescript"
            if item.endswith(".js"):
                print("Detected JavaScript (found .js files, no package.json/tsconfig.json).")
                return "javascript"
            if item.endswith(".go"):
                print("Detected Go (found .go files, no go.mod).")
                return "go"
            if item.endswith(".rb"):
                print("Detected Ruby (found .rb files, no Gemfile).")
                return "ruby"
    except OSError as e:
        print(f"Warning: Could not scan directory items for file extensions: {e}", file=sys.stderr)

    print("Could not automatically detect a supported language.")
    return None

def run_tools(project_path, language):
    """Runs the appropriate static analysis tools based on the detected language."""
    print(f"Proceeding with scan for: {language}\n")
    results = {}
    tools_found = False
    original_cwd = os.getcwd()
    os.chdir(project_path) # Change to project directory for tool execution

    # Helper function to find files by extension
    def find_files_by_extension(directory, extensions):
        found_files = []
        for root, _, files in os.walk(directory):
            # Skip node_modules directories
            if "node_modules" in root.split(os.path.sep):
                continue
                
            for file in files:
                if any(file.endswith(ext) for ext in extensions):
                    found_files.append(os.path.join(root, file))
        return found_files

    # --- JavaScript / TypeScript Tools ---
    if language in ["javascript", "typescript"]:
        # Add detailed diagnostic information to log file
        logger.info("--- Node.js PATH Diagnostics ---")
        logger.info(f"Current PATH: {os.environ.get('PATH', 'Not found')}")
        
        # Check common Node.js installation paths
        nodejs_paths = [
            r"C:\Program Files\nodejs",
            r"C:\Program Files (x86)\nodejs",
            os.path.expanduser(r"~\AppData\Roaming\npm")
        ]
        
        for path in nodejs_paths:
            if os.path.exists(path):
                logger.info(f"Node.js path exists: {path}")
                npx_path = os.path.join(path, "npx.cmd" if os.name == 'nt' else "npx")
                if os.path.exists(npx_path):
                    logger.info(f"npx found at: {npx_path}")
            else:
                logger.info(f"Node.js path does not exist: {path}")
        
        # Check if npx is in PATH
        npx_path = shutil.which("npx")
        logger.info(f"npx found in PATH: {npx_path if npx_path else 'Not found'}")
        
        print_section("ESLint")
        spinner.start("Running ESLint...")
        print(f"\n--- Running ESLint ---")
        # Find JavaScript and TypeScript files
        js_ts_files = find_files_by_extension(project_path, ['.js', '.jsx', '.ts', '.tsx'])
        # Filter out node_modules, dist, and build directories
        js_ts_files = [f for f in js_ts_files if not any(excluded in f for excluded in ['node_modules', 'dist', 'build'])]
        
        if js_ts_files:
            logger.info(f"Found {len(js_ts_files)} JavaScript/TypeScript files to scan")
            # Use our new run_eslint function
            results["eslint"] = run_eslint(project_path, js_ts_files)
        else:
            logger.warning("No JavaScript/TypeScript files found to scan")
            results["eslint"] = {"error": "No JavaScript/TypeScript files found to scan"}
        spinner.stop("ESLint finished.")

        print_section("RetireJS")
        spinner.start("Running RetireJS...")
        # Add RetireJS for JavaScript/TypeScript security scanning
        print(f"\n--- Running RetireJS ---")
        if not shutil.which("retire"):
            logger.error("\n" + "#"*80)
            logger.error("ERROR: Required tool 'retire' not found.")
            logger.error("This is an open-source security scanner for JavaScript.")
            logger.error("To install: npm install -g retire")
            logger.error("This tool is required for JavaScript/TypeScript security scanning.")
            logger.error("\nPlease see README.md for more information on setting up prerequisites.")
            logger.error("#"*80 + "\n")
            results["retirejs"] = {"error": "Tool 'retire' not found.", "stdout": None, "stderr": None, "returncode": -1}
        else:
            tools_found = True
            try:
                # RetireJS: 0 = no vulnerabilities, 13 = vulnerabilities found
                cmd = ["retire", "--outputformat", "json", "--path", "."]
                results["retirejs"] = _run_command_and_capture(cmd, cwd=project_path)
                if results["retirejs"]["returncode"] not in [0, 13]:
                    logger.error(f"RetireJS execution failed (Exit Code: {results['retirejs']['returncode']}).")
                    if results["retirejs"]["stderr"]: logger.error(f"Stderr:\n{results['retirejs']['stderr']}")
            except Exception as e:
                logger.error("\n" + "#"*80)
                logger.error(f"ERROR: Failed to run retire: {str(e)}")
                logger.error("This could be due to a PATH environment issue when running from Python.")
                logger.error("Try running the scanner from a command prompt where 'retire --version' works.")
                logger.error("#"*80 + "\n")
                results["retirejs"] = {"error": f"Failed to run retire: {str(e)}", "stdout": None, "stderr": None, "returncode": -1}
        spinner.stop("RetireJS finished.")

        print_section("TypeScript Compiler")
        spinner.start("Running TypeScript Compiler...")
        # Run TypeScript compiler in noEmit mode to check for errors
        print(f"\n--- Running TypeScript Compiler ---")
        results["typescript"] = run_typescript_check(project_path)
        spinner.stop("TypeScript Compiler finished.")

    # --- Python Tools ---
    elif language == "python":
        print_section("Flake8")
        spinner.start("Running Flake8...")
        print("--- Running Flake8 ---")
        if not shutil.which("flake8"):
            logger.error("\n" + "="*80)
            logger.error("ERROR: Required tool 'flake8' not found.")
            logger.error("To install: pip install flake8")
            logger.error("This tool is required for Python code scanning.")
            logger.error("\nPlease see README.md for more information on setting up prerequisites.")
            logger.error("="*80 + "\n")
            results["flake8"] = {"error": "Tool not found", "stdout": None, "stderr": None, "returncode": -1}
        else:
            tools_found = True
            # Flake8 usually exits 1 if issues found, 0 if none. Both are "success" in terms of execution.
            # Run without specific format first to check basic execution
            cmd = ["flake8", "."]
            results["flake8"] = _run_command_and_capture(cmd, cwd=project_path)
            if results["flake8"]["returncode"] not in [0, 1]:
                 logger.error(f"Flake8 execution error (Exit Code: {results['flake8']['returncode']}).")
                 if results["flake8"]["stderr"]: logger.error(f"Stderr:\n{results['flake8']['stderr']}")
        spinner.stop("Flake8 finished.")

        print_section("Bandit")
        spinner.start("Running Bandit...")
        print("\n--- Running Bandit ---")
        if not shutil.which("bandit"):
            logger.error("\n" + "="*80)
            logger.error("ERROR: Required tool 'bandit' not found.")
            logger.error("To install: pip install bandit")
            logger.error("This tool is required for Python code scanning.")
            logger.error("\nPlease see README.md for more information on setting up prerequisites.")
            logger.error("="*80 + "\n")
            results["bandit"] = {"error": "Tool not found", "stdout": None, "stderr": None, "returncode": -1}
        else:
            tools_found = True
            # Bandit exits 0 for success (even with issues), non-zero for errors.
            cmd = ["bandit", "-r", ".", "-f", "json"]
            results["bandit"] = _run_command_and_capture(cmd, cwd=project_path)
            if results["bandit"]["returncode"] != 0:
                 logger.error(f"Bandit execution error (Exit Code: {results['bandit']['returncode']}).")
                 if results["bandit"]["stderr"]: logger.error(f"Stderr:\n{results['bandit']['stderr']}")
        spinner.stop("Bandit finished.")

    # --- Go Tools ---
    elif language == "go":
        print_section("golangci-lint")
        spinner.start("Running golangci-lint...")
        print(f"\n--- Running golangci-lint ---")
        if not shutil.which("golangci-lint"):
            logger.error("\n" + "="*80)
            logger.error("ERROR: Required tool 'golangci-lint' not found.")
            logger.error("Installation guide: https://golangci-lint.run/usage/install/")
            logger.error("This tool is required for Go code scanning.")
            logger.error("\nPlease see README.md for more information on setting up prerequisites.")
            logger.error("="*80 + "\n")
            results["golangci-lint"] = {"error": "Tool not found", "stdout": None, "stderr": None, "returncode": -1}
        else:
            tools_found = True
            # golangci-lint: 0 = success no issues, 1 = success issues found, >1 = error
            cmd = ["golangci-lint", "run", "./...", "--out-format", "json", "--issues-exit-code", "1"]
            # We set --issues-exit-code to 1 so both 0 and 1 mean successful execution
            results["golangci-lint"] = _run_command_and_capture(cmd, cwd=project_path)
            if results["golangci-lint"]["returncode"] not in [0, 1]:
                 logger.error(f"golangci-lint execution error (Exit Code: {results['golangci-lint']['returncode']}).")
                 if results["golangci-lint"]["stderr"]: logger.error(f"Stderr:\n{results['golangci-lint']['stderr']}")
        spinner.stop("golangci-lint finished.")

        print_section("gosec")
        spinner.start("Running gosec...")
        print(f"\n--- Running gosec ---")
        if not shutil.which("gosec"):
            logger.error("\n" + "="*80)
            logger.error("ERROR: Required tool 'gosec' not found.")
            logger.error("To install: go install github.com/securego/gosec/v2/cmd/gosec@latest")
            logger.error("This tool is required for Go code scanning.")
            logger.error("\nPlease see README.md for more information on setting up prerequisites.")
            logger.error("="*80 + "\n")
            results["gosec"] = {"error": "Tool not found", "stdout": None, "stderr": None, "returncode": -1}
        else:
            tools_found = True
            # gosec: 0 = No warnings, 3 = Warnings found, 4 = Error, other non-zero = Error
            # We treat 0 and 3 as successful execution
            cmd = ["gosec", "-fmt=json", "./..."]
            results["gosec"] = _run_command_and_capture(cmd, cwd=project_path)
            # Gosec might print to stderr even on success (e.g., progress), check return code first
            if results["gosec"]["returncode"] not in [0, 3]:
                logger.error(f"gosec execution issues (Exit Code: {results['gosec']['returncode']}).")
                if results["gosec"]["stderr"]: logger.error(f"Stderr:\n{results['gosec']['stderr']}")
        spinner.stop("gosec finished.")

    # --- Ruby Tools ---
    elif language == "ruby":
        print_section("RuboCop")
        spinner.start("Running RuboCop...")
        print(f"\n--- Running RuboCop ---")
        if not shutil.which("rubocop"):
            logger.error("\n" + "="*80)
            logger.error("ERROR: Required tool 'rubocop' not found.")
            logger.error("To install: gem install rubocop")
            logger.error("This tool is required for Ruby code scanning.")
            logger.error("\nPlease see README.md for more information on setting up prerequisites.")
            logger.error("="*80 + "\n")
            results["rubocop"] = {"error": "Tool not found", "stdout": None, "stderr": None, "returncode": -1}
        else:
            tools_found = True
            # rubocop: 0 = no offenses, 1 = offenses found, >1 = error
            cmd = ["rubocop", ".", "--format", "json"]
            results["rubocop"] = _run_command_and_capture(cmd, cwd=project_path)
            if results["rubocop"]["returncode"] not in [0, 1]:
                 logger.error(f"RuboCop execution error (Exit Code: {results['rubocop']['returncode']}).")
                 if results["rubocop"]["stderr"]: logger.error(f"Stderr:\n{results['rubocop']['stderr']}")
        spinner.stop("RuboCop finished.")

        print_section("Brakeman")
        spinner.start("Running Brakeman...")
        print(f"\n--- Running Brakeman ---")
        if not shutil.which("brakeman"):
            logger.error("\n" + "="*80)
            logger.error("ERROR: Required tool 'brakeman' not found.")
            logger.error("To install: gem install brakeman")
            logger.error("This tool is required for Ruby code scanning.")
            logger.error("\nPlease see README.md for more information on setting up prerequisites.")
            logger.error("="*80 + "\n")
            results["brakeman"] = {"error": "Tool not found", "stdout": None, "stderr": None, "returncode": -1}
        else:
            tools_found = True
            # brakeman: 0 = No warnings, 3 = Warnings found, 4 = Error, other non-zero = Error
            # We treat 0 and 3 as successful execution
            cmd = ["brakeman", "-f", "json", "-q"] # -q for quiet
            results["brakeman"] = _run_command_and_capture(cmd, cwd=project_path)
            if results["brakeman"]["returncode"] not in [0, 3]:
                 logger.error(f"Brakeman execution error (Exit Code: {results['brakeman']['returncode']}).")
                 if results["brakeman"]["stderr"]: logger.error(f"Stderr:\n{results['brakeman']['stderr']}")
        spinner.stop("Brakeman finished.")

    # --- Cleanup --- #
    os.chdir(original_cwd) # Change back to original directory

    # If no tools were found for the language, exit early
    if not tools_found:
        logger.error("\n" + "#"*80)
        logger.error(f"ERROR: No required tools were found for {language}.")
        logger.error("Please install the required tools as described in the README.md file.")
        logger.error("The scan cannot proceed without the necessary tools.")
        logger.error("#"*80 + "\n")
        print(f"\nScan aborted. No tools were found for {language}.")
        print(f"Please see README.md for installation instructions for {language} tools.")
        print(f"Log file with detailed messages: {os.path.abspath(LOG_FILENAME)}")
        sys.exit(1)

    return results

# --- Parser Functions ---

def parse_flake8_output(output):
    """Parse flake8 output (default format)."""
    issues = []
    if not output:
        return issues
    
    # Flake8 default format is: file:line:column: code message
    for line in output.strip().split('\n'):
        if not line.strip():
            continue
        
        try:
            # Parse file path, line, column, code, and message
            file_info, message = line.split(':', 3)[3].split(' ', 1)
            file_path, line_num, col = line.split(':', 3)[:3]
            code = message.split(' ')[0]
            message = message.split(' ', 1)[1] if ' ' in message else message
            
            issues.append({
                'file': file_path,
                'line': int(line_num),
                'column': int(col),
                'code': code,
                'message': message.strip(),
                'severity': 'medium',  # Flake8 doesn't provide severity, default to medium
                'tool': 'flake8'
            })
        except (ValueError, IndexError) as e:
            logger.error(f"Warning: Could not parse flake8 line: {line} - {e}")

    return issues

def parse_bandit_json_output(output):
    """Parse bandit JSON output."""
    issues = []
    if not output:
        return issues
    
    try:
        data = json.loads(output)
        results = data.get('results', [])
        
        for result in results:
            issues.append({
                'file': result.get('filename', 'Unknown'),
                'line': result.get('line_number', 0),
                'column': '',  # Bandit doesn't provide column
                'code': f"B{result.get('test_id', '000')}",
                'message': result.get('issue_text', 'Unknown issue'),
                'severity': result.get('issue_severity', 'UNKNOWN').lower(),
                'confidence': result.get('issue_confidence', 'UNKNOWN'),
                'tool': 'bandit'
            })
    except json.JSONDecodeError as e:
        logger.error(f"Error parsing Bandit JSON output: {e}")
        logger.error(f"Raw output: {output[:500]}...")

    return issues

def parse_eslint_json_output(output):
    """Parse ESLint JSON output."""
    issues = []
    if not output:
        return issues
    
    try:
        data = json.loads(output)
        
        for file_result in data:
            file_path = file_result.get('filePath', 'Unknown')
            
            for message in file_result.get('messages', []):
                severity_map = {1: 'warning', 2: 'error'}
                severity = severity_map.get(message.get('severity', 2), 'error')
                
                issues.append({
                    'file': file_path,
                    'line': message.get('line', 0),
                    'column': message.get('column', 0),
                    'code': message.get('ruleId', 'Unknown'),
                    'message': message.get('message', 'Unknown issue'),
                    'severity': severity,
                    'tool': 'eslint'
                })
    except json.JSONDecodeError as e:
        logger.error(f"Error parsing ESLint JSON output: {e}")
        logger.error(f"Raw output: {output[:500]}...")
    
    return issues

def parse_golangci_lint_json_output(output):
    """Parse golangci-lint JSON output."""
    issues = []
    if not output:
        return issues
    
    try:
        data = json.loads(output)
        
        for issue in data.get('Issues', []):
            issues.append({
                'file': issue.get('Pos', {}).get('Filename', 'Unknown'),
                'line': issue.get('Pos', {}).get('Line', 0),
                'column': issue.get('Pos', {}).get('Column', 0),
                'code': issue.get('FromLinter', 'Unknown'),
                'message': issue.get('Text', 'Unknown issue'),
                'severity': 'error',  # golangci-lint doesn't provide severity, default to error
                'tool': 'golangci-lint'
            })
    except json.JSONDecodeError as e:
        logger.error(f"Error parsing golangci-lint JSON output: {e}")
        logger.error(f"Raw output: {output[:500]}...")

    return issues

def parse_gosec_json_output(output):
    """Parse gosec JSON output."""
    issues = []
    if not output:
        return issues
    
    try:
        data = json.loads(output)
        
        for issue in data.get('Issues', []):
            severity = issue.get('severity', 'UNKNOWN')
            confidence = issue.get('confidence', 'UNKNOWN')
            
            issues.append({
                'file': issue.get('file', 'Unknown'),
                'line': issue.get('line', 0),
                'column': '',  # gosec doesn't provide column
                'code': issue.get('rule_id', 'Unknown'),
                'message': issue.get('details', 'Unknown issue'),
                'severity': f"{severity}",
                'confidence': f"{confidence}",
                'tool': 'gosec'
            })
    except json.JSONDecodeError as e:
        logger.error(f"Error parsing gosec JSON output: {e}")
        logger.error(f"Raw output: {output[:500]}...")

    return issues

def parse_rubocop_json_output(output):
    """Parse RuboCop JSON output."""
    issues = []
    if not output:
        return issues
    
    try:
        data = json.loads(output)
        
        for file_data in data.get('files', []):
            file_path = file_data.get('path', 'Unknown')
            
            for offense in file_data.get('offenses', []):
                severity = offense.get('severity', 'convention').lower()
                # Map RuboCop severities to standardized severities
                severity_map = {
                    'convention': 'low',
                    'warning': 'medium',
                    'error': 'high',
                    'fatal': 'critical'
                }
                
                issues.append({
                    'file': file_path,
                    'line': offense.get('location', {}).get('line', 0),
                    'column': offense.get('location', {}).get('column', 0),
                    'code': offense.get('cop_name', 'Unknown'),
                    'message': offense.get('message', 'Unknown issue'),
                    'severity': severity_map.get(severity, 'medium'),
                    'tool': 'rubocop'
                })
    except json.JSONDecodeError as e:
        logger.error(f"Error parsing RuboCop JSON output: {e}")
        logger.error(f"Raw output: {output[:500]}...")
    
    return issues

def parse_brakeman_json_output(output):
    """Parse Brakeman JSON output."""
    issues = []
    if not output:
        return issues
    
    try:
        data = json.loads(output)
        
        for warning in data.get('warnings', []):
            # Map Brakeman confidence to standardized confidence
            confidence_map = {
                'High': 'high',
                'Medium': 'medium',
                'Low': 'low'
            }
            confidence = confidence_map.get(warning.get('confidence', 'Medium'), 'medium')
            
            issues.append({
                'file': warning.get('file', 'Unknown'),
                'line': warning.get('line', 0),
                'column': '',  # Brakeman doesn't provide column
                'code': warning.get('warning_type', 'Unknown'),
                'message': warning.get('message', 'Unknown issue'),
                'severity': 'high',  # Brakeman warnings are security issues, default to high
                'confidence': confidence,
                'tool': 'brakeman'
            })
    except json.JSONDecodeError as e:
        logger.error(f"Error parsing Brakeman JSON output: {e}")
        logger.error(f"Raw output: {output[:500]}...")

    return issues

def parse_retirejs_json_output(output):
    """Parse RetireJS JSON output."""
    issues = []
    if not output:
        return issues
    
    try:
        data = json.loads(output)
        
        for result in data:
            file_path = result.get('file', 'Unknown')
            
            for component in result.get('results', []):
                component_name = component.get('component', 'Unknown')
                component_version = component.get('version', 'Unknown')
                
                for vulnerability in component.get('vulnerabilities', []):
                    severity = vulnerability.get('severity', 'high')  # Default to high if not specified
                    if not severity:
                        severity = 'high'  # RetireJS often doesn't specify severity, default to high
                    
                    # Create a meaningful message
                    message = f"{component_name} {component_version} has vulnerability: {vulnerability.get('info', 'Unknown vulnerability')}"
                    
                    issues.append({
                        'file': file_path,
                        'line': 0,  # RetireJS doesn't provide line numbers
                        'column': '',
                        'code': vulnerability.get('identifiers', {}).get('CVE', ['Unknown'])[0] if vulnerability.get('identifiers', {}).get('CVE') else 'RetireJS',
                        'message': message,
                        'severity': severity,
                        'tool': 'retirejs'
                    })
    except json.JSONDecodeError as e:
        logger.error(f"Error parsing RetireJS JSON output: {e}")
        logger.error(f"Raw output: {output[:500]}...")
    
    return issues

def parse_typescript_check_output(output):
    """Parse TypeScript compiler output."""
    issues = []
    if not output:
        return issues
    
    try:
        data = json.loads(output)
        
        for file_result in data:
            file_path = file_result.get('filePath', 'Unknown')
            
            for message in file_result.get('messages', []):
                severity_map = {1: 'warning', 2: 'error'}
                severity = severity_map.get(message.get('severity', 2), 'error')
                
                issues.append({
                    'file': file_path,
                    'line': message.get('line', 0),
                    'column': message.get('column', 0),
                    'code': message.get('ruleId', 'Unknown'),
                    'message': message.get('message', 'Unknown issue'),
                    'severity': severity,
                    'tool': 'typescript'
                })
    except json.JSONDecodeError as e:
        logger.error(f"Error parsing TypeScript compiler output: {e}")
        logger.error(f"Raw output: {output[:500]}...")

    return issues

def generate_report(results, output_dir=None):
    """
    Generates a comprehensive Markdown report from the scan results.
    Also creates a JSON file with structured data for AI-assisted remediation.
    Prompts for output directory if not provided.
    """
    print_section("Generating Report")
    spinner.start("Processing scan results...")
    
    # If no output directory specified, prompt for it
    if not output_dir:
        output_dir = input("\nEnter the directory path where you want to save the reports: ").strip()
    
    # Check if directory exists
    if not os.path.exists(output_dir):
        create = input(f"\nDirectory '{output_dir}' does not exist. Would you like to create it? (y/n): ").lower().strip()
        if create == 'y':
            try:
                os.makedirs(output_dir)
                print(f"Created directory: {output_dir}")
            except Exception as e:
                logger.error(f"Error creating directory: {e}")
                return False
        else:
            print("Report generation cancelled - no valid output directory")
            return False
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Initialize report sections
    report_md = f"# Vibe Code Scan Report\n\nGenerated: {timestamp}\n\n"
    
    # Initialize structured data for AI remediation
    ai_friendly_data = {
        "timestamp": timestamp,
        "tool_summary": {
            "successful": [],
            "failed": [],
            "skipped": []
        },
        "issues": [],
        "resources": {}
    }
    
    # Process tool execution results
    execution_issues = []
    
    for tool, result in results.items():
        if isinstance(result, dict) and "error" in result:
            # Tool had a pre-execution error
            execution_issues.append(f"`{tool}: Pre-execution Error ({result['error']})`")
            ai_friendly_data["tool_summary"]["skipped"].append({
                "tool": tool,
                "reason": result["error"]
            })
        elif isinstance(result, dict) and "returncode" in result:
            # Tool was executed
            if result["returncode"] != 0:
                # Tool execution failed
                execution_issues.append(f"`{tool}: Execution Failed (Exit: {result['returncode']})`")
                ai_friendly_data["tool_summary"]["failed"].append({
                    "tool": tool,
                    "exit_code": result["returncode"],
                    "stderr": result.get("stderr", "")[:200]  # Limit stderr length
                })
            else:
                # Tool executed successfully
                ai_friendly_data["tool_summary"]["successful"].append({
                    "tool": tool
                })
    
    # Add execution summary to report if there were issues
    if execution_issues:
        report_md += "## Tool Execution Summary\n\n"
        report_md += "The following tools encountered issues or were skipped:\n"
        for issue in execution_issues:
            report_md += f"- {issue}\n"
        report_md += "\nCheck console output for more details.\n\n"
    
    # Process and parse results from each tool
    all_issues = []
    
    spinner.stop("Processing tool results...")
    
    # Parse Flake8 results
    if "flake8" in results and isinstance(results["flake8"], dict) and results["flake8"].get("returncode") == 0:
        spinner.start("Processing Flake8 results...")
        try:
            flake8_issues = parse_flake8_output(results["flake8"]["stdout"])
            all_issues.extend(flake8_issues)
            logger.info(f"Found {len(flake8_issues)} issues from flake8")
            spinner.stop(f"Found {len(flake8_issues)} issues from Flake8")
        except Exception as e:
            logger.error(f"  Skipping flake8 parsing due to error: {e}")
            spinner.stop("Error processing Flake8 results")
            ai_friendly_data["tool_summary"]["failed"].append({
                "tool": "flake8",
                "reason": f"Parsing error: {str(e)}"
            })
    
    # Parse Bandit results
    if "bandit" in results and isinstance(results["bandit"], dict) and results["bandit"].get("returncode") == 0:
        spinner.start("Processing Bandit results...")
        try:
            bandit_issues = parse_bandit_json_output(results["bandit"]["stdout"])
            all_issues.extend(bandit_issues)
            logger.info(f"Found {len(bandit_issues)} issues from bandit")
            spinner.stop(f"Found {len(bandit_issues)} issues from Bandit")
        except Exception as e:
            logger.error(f"  Skipping bandit parsing due to error: {e}")
            spinner.stop("Error processing Bandit results")
            ai_friendly_data["tool_summary"]["failed"].append({
                "tool": "bandit",
                "reason": f"Parsing error: {str(e)}"
            })
    
    # Parse ESLint results
    if "eslint" in results and isinstance(results["eslint"], dict) and results["eslint"].get("returncode") == 0:
        spinner.start("Processing ESLint results...")
        try:
            eslint_issues = parse_eslint_json_output(results["eslint"]["stdout"])
            all_issues.extend(eslint_issues)
            logger.info(f"Found {len(eslint_issues)} issues from eslint")
            spinner.stop(f"Found {len(eslint_issues)} issues from ESLint")
        except Exception as e:
            logger.error(f"  Skipping eslint parsing due to error: {e}")
            spinner.stop("Error processing ESLint results")
            ai_friendly_data["tool_summary"]["failed"].append({
                "tool": "eslint",
                "reason": f"Parsing error: {str(e)}"
            })
    
    # Parse RetireJS results
    if "retirejs" in results and isinstance(results["retirejs"], dict) and results["retirejs"].get("returncode") == 0:
        spinner.start("Processing RetireJS results...")
        try:
            logger.info("  Parsing retirejs output...")
            retirejs_issues = parse_retirejs_json_output(results["retirejs"]["stdout"])
            all_issues.extend(retirejs_issues)
            logger.info(f"Found {len(retirejs_issues)} issues from retirejs")
            spinner.stop(f"Found {len(retirejs_issues)} issues from RetireJS")
        except Exception as e:
            logger.error(f"  Error parsing retirejs output: {e}")
            logger.error(f"    Raw stdout:\n{results['retirejs']['stdout'][:500]}...")
            spinner.stop("Error processing RetireJS results")
            ai_friendly_data["tool_summary"]["failed"].append({
                "tool": "retirejs",
                "reason": f"Parsing error: {str(e)}"
            })
    
    # Parse TypeScript results
    if "typescript" in results and isinstance(results["typescript"], dict) and results["typescript"].get("returncode") == 0:
        spinner.start("Processing TypeScript results...")
        try:
            typescript_issues = parse_typescript_check_output(results["typescript"]["stdout"])
            all_issues.extend(typescript_issues)
            logger.info(f"Found {len(typescript_issues)} issues from typescript")
            spinner.stop(f"Found {len(typescript_issues)} issues from TypeScript")
        except Exception as e:
            logger.error(f"  Skipping typescript parsing due to execution failure (Exit Code: {results['typescript'].get('returncode')}).")
            spinner.stop("Error processing TypeScript results")
            ai_friendly_data["tool_summary"]["failed"].append({
                "tool": "typescript",
                "reason": f"Parsing error: {str(e)}"
            })
    
    # Parse golangci-lint results
    if "golangci-lint" in results and isinstance(results["golangci-lint"], dict) and results["golangci-lint"].get("returncode") == 0:
        spinner.start("Processing golangci-lint results...")
        try:
            golangci_issues = parse_golangci_lint_json_output(results["golangci-lint"]["stdout"])
            all_issues.extend(golangci_issues)
            logger.info(f"Found {len(golangci_issues)} issues from golangci-lint")
            spinner.stop(f"Found {len(golangci_issues)} issues from golangci-lint")
        except Exception as e:
            logger.error(f"  Skipping golangci-lint parsing due to error: {e}")
            spinner.stop("Error processing golangci-lint results")
            ai_friendly_data["tool_summary"]["failed"].append({
                "tool": "golangci-lint",
                "reason": f"Parsing error: {str(e)}"
            })
    
    # Parse gosec results
    if "gosec" in results and isinstance(results["gosec"], dict) and results["gosec"].get("returncode") == 0:
        spinner.start("Processing gosec results...")
        try:
            gosec_issues = parse_gosec_json_output(results["gosec"]["stdout"])
            all_issues.extend(gosec_issues)
            logger.info(f"Found {len(gosec_issues)} issues from gosec")
            spinner.stop(f"Found {len(gosec_issues)} issues from gosec")
        except Exception as e:
            logger.error(f"  Skipping gosec parsing due to error: {e}")
            spinner.stop("Error processing gosec results")
            ai_friendly_data["tool_summary"]["failed"].append({
                "tool": "gosec",
                "reason": f"Parsing error: {str(e)}"
            })
    
    # Parse RuboCop results
    if "rubocop" in results and isinstance(results["rubocop"], dict) and results["rubocop"].get("returncode") == 0:
        spinner.start("Processing RuboCop results...")
        try:
            rubocop_issues = parse_rubocop_json_output(results["rubocop"]["stdout"])
            all_issues.extend(rubocop_issues)
            logger.info(f"Found {len(rubocop_issues)} issues from rubocop")
            spinner.stop(f"Found {len(rubocop_issues)} issues from RuboCop")
        except Exception as e:
            logger.error(f"  Skipping rubocop parsing due to error: {e}")
            spinner.stop("Error processing RuboCop results")
            ai_friendly_data["tool_summary"]["failed"].append({
                "tool": "rubocop",
                "reason": f"Parsing error: {str(e)}"
            })
    
    # Parse Brakeman results
    if "brakeman" in results and isinstance(results["brakeman"], dict) and results["brakeman"].get("returncode") == 0:
        spinner.start("Processing Brakeman results...")
        try:
            brakeman_issues = parse_brakeman_json_output(results["brakeman"]["stdout"])
            all_issues.extend(brakeman_issues)
            logger.info(f"Found {len(brakeman_issues)} issues from brakeman")
            spinner.stop(f"Found {len(brakeman_issues)} issues from Brakeman")
        except Exception as e:
            logger.error(f"  Skipping brakeman parsing due to error: {e}")
            spinner.stop("Error processing Brakeman results")
            ai_friendly_data["tool_summary"]["failed"].append({
                "tool": "brakeman",
                "reason": f"Parsing error: {str(e)}"
            })
    
    # Sort issues by file and line number
    spinner.start("Sorting and organizing issues...")
    all_issues.sort(key=lambda x: (x.get("file", ""), x.get("line", 0)))
    
    # Add issues to AI-friendly data
    ai_friendly_data["issues"] = all_issues
    
    # Generate issues table if there are issues
    if all_issues:
        report_md += "## Issues Found\n\n"
        report_md += "| File | Line | Severity | Tool | Message | Rule ID |\n"
        report_md += "|------|------|----------|------|---------|--------|\n"
        
        for issue in all_issues:
            file = issue.get("file", "Unknown")
            line = issue.get("line", "N/A")
            severity = issue.get("severity", "Unknown")
            message = issue.get("message", "No message provided")
            tool = issue.get("tool", "Unknown")
            rule_id = issue.get("rule_id", "N/A")
            
            # Escape pipe characters in message to avoid breaking the table
            message = message.replace("|", "\\|")
            
            report_md += f"| {file} | {line} | {severity} | {tool} | {message} | {rule_id} |\n"
    else:
        report_md += "**Congratulations! No issues were found by the successfully executed scanners.**\n\n"
        if execution_issues:
            report_md += "**Note:** Some tools were skipped or failed during execution. See summary above.\n\n"
    
    # Add remediation guidance
    report_md += "## How to Fix Issues\n\n"
    report_md += "For guidance on fixing the issues found, refer to the following resources:\n\n"
    report_md += "- **Python**: [Flake8 Rules](https://flake8.pycqa.org/en/latest/user/error-codes.html), [Bandit Documentation](https://bandit.readthedocs.io/en/latest/)\n"
    report_md += "- **JavaScript/TypeScript**: [ESLint Rules](https://eslint.org/docs/rules/)\n"
    report_md += "- **Go**: [golangci-lint](https://golangci-lint.run/usage/linters/), [gosec](https://github.com/securego/gosec)\n"
    report_md += "- **Ruby**: [RuboCop](https://docs.rubocop.org/rubocop/), [Brakeman](https://brakemanscanner.org/docs/warning_types/)\n"
    
    # Add AI remediation guidance
    report_md += "\n## AI-Assisted Remediation\n\n"
    report_md += "A JSON file with structured data has been generated alongside this report to help AI tools remediate the issues found.\n"
    report_md += "You can use this file with AI assistants like Windsurf or other AI-powered code editors to help fix the issues.\n\n"
    report_md += "```\n"
    report_md += "vibe_scan_report.json\n"
    report_md += "```\n"
    
    # Add resources to AI-friendly data
    ai_friendly_data["resources"] = {
        "python": {
            "flake8": "https://flake8.pycqa.org/en/latest/user/error-codes.html",
            "bandit": "https://bandit.readthedocs.io/en/latest/"
        },
        "javascript": {
            "eslint": "https://eslint.org/docs/rules/"
        },
        "typescript": {
            "eslint": "https://eslint.org/docs/rules/",
            "typescript": "https://www.typescriptlang.org/docs/"
        },
        "go": {
            "golangci-lint": "https://golangci-lint.run/usage/linters/",
            "gosec": "https://github.com/securego/gosec"
        },
        "ruby": {
            "rubocop": "https://docs.rubocop.org/rubocop/",
            "brakeman": "https://brakemanscanner.org/docs/warning_types/"
        }
    }
    
    spinner.stop("Report preparation complete")
    
    # Write the report to a file
    spinner.start("Writing report files...")
    try:
        report_path = os.path.join(output_dir, REPORT_FILENAME)
        with open(report_path, "w") as f:
            f.write(report_md)
        
        # Write AI-friendly JSON data
        json_path = os.path.join(output_dir, JSON_REPORT_FILENAME)
        with open(json_path, "w") as f:
            json.dump(ai_friendly_data, f, indent=2)
        
        spinner.stop(f"Report files generated successfully: {report_path} and {json_path}")
        print(f"Report generated: {report_path}")
        print(f"AI-friendly data generated: {json_path}")
        
        return True
    except Exception as e:
        logger.error(f"Error writing report: {e}")
        spinner.stop(f"Error writing report: {e}")
        return False

def run_eslint(project_path, files_to_scan):
    """Run ESLint on JavaScript and TypeScript files."""
    try:
        # Check if ESLint is available
        eslint_path = shutil.which("eslint")
        if not eslint_path:
            logger.error("ESLint requires 'eslint' which was not found in PATH.")
            logger.error("Please ensure ESLint is installed and in your PATH.")
            return {"error": "eslint not found in PATH", "stdout": None, "stderr": None, "returncode": -1}
        
        # Check for TypeScript files
        ts_files_exist = any(f.endswith(('.ts', '.tsx')) for f in files_to_scan)
        
        # Check for tsconfig.json if TypeScript files exist
        tsconfig_path = os.path.join(project_path, 'tsconfig.json')
        if ts_files_exist and not os.path.exists(tsconfig_path):
            logger.info("No tsconfig.json found. Creating a default configuration for TypeScript linting.")
            default_tsconfig = {
                "compilerOptions": {
                    "target": "es2020",
                    "module": "commonjs",
                    "strict": True,
                    "esModuleInterop": True,
                    "skipLibCheck": True,
                    "forceConsistentCasingInFileNames": True,
                    "jsx": "react"
                },
                "include": ["**/*.ts", "**/*.tsx"],
                "exclude": ["node_modules", "dist", "build"]
            }
            try:
                with open(tsconfig_path, 'w') as f:
                    json.dump(default_tsconfig, f, indent=2)
                logger.info("Created default tsconfig.json for TypeScript linting")
            except Exception as e:
                logger.warning(f"Failed to create default tsconfig.json: {e}")
                # Continue without it, the linting will be less effective but still work
        
        # Look for ESLint configuration
        eslint_config_js = os.path.join(project_path, 'eslint.config.js')
        eslint_rc_js = os.path.join(project_path, '.eslintrc.js')
        eslint_rc_json = os.path.join(project_path, '.eslintrc.json')
        eslint_rc = os.path.join(project_path, '.eslintrc')
        package_json = os.path.join(project_path, 'package.json')
        
        # Check if there's ESLint config in package.json
        has_package_json_config = False
        if os.path.exists(package_json):
            try:
                with open(package_json, 'r') as f:
                    pkg_data = json.load(f)
                    if 'eslintConfig' in pkg_data:
                        has_package_json_config = True
                        logger.info("Found ESLint configuration in package.json")
            except Exception as e:
                logger.warning(f"Error reading package.json: {e}")
        
        # Determine which config file to use
        config_path = None
        is_flat_config = False
        
        if os.path.exists(eslint_config_js):
            config_path = eslint_config_js
            is_flat_config = True
            logger.info(f"Found ESLint flat configuration: {eslint_config_js}")
        elif os.path.exists(eslint_rc_js):
            config_path = eslint_rc_js
            logger.info(f"Found ESLint configuration: {eslint_rc_js}")
        elif os.path.exists(eslint_rc_json):
            config_path = eslint_rc_json
            logger.info(f"Found ESLint configuration: {eslint_rc_json}")
        elif os.path.exists(eslint_rc):
            config_path = eslint_rc
            logger.info(f"Found ESLint configuration: {eslint_rc}")
        elif has_package_json_config:
            config_path = package_json
            logger.info("Using ESLint configuration from package.json")
        else:
            logger.warning("Could not find ESLint configuration. Using default configuration.")
            # Use our bundled configuration
            config_path = "/home/scanner/.eslintrc.js"
            logger.info(f"Using default ESLint configuration: {config_path}")
        
        # Install TypeScript ESLint parser if needed
        if ts_files_exist:
            logger.info("TypeScript files detected, ensuring TypeScript ESLint parser is available")
            try:
                # Check if TypeScript ESLint parser is available
                check_cmd = ["eslint", "--no-eslintrc", "--parser", "@typescript-eslint/parser", "--version"]
                result = subprocess.run(check_cmd, cwd=project_path, capture_output=True, text=True)
                
                if result.returncode == 0:
                    logger.info("TypeScript ESLint parser is available")
                else:
                    # Install TypeScript parser locally if needed
                    logger.info("TypeScript ESLint parser not available, attempting installation")
                    # Use specific versions that are compatible with ESLint 8.x
                    install_cmd = ["npm", "install", "--no-save", 
                                  "@typescript-eslint/parser@6.21.0", 
                                  "@typescript-eslint/eslint-plugin@6.21.0",
                                  "typescript@latest"]
                    logger.info(f"Installing TypeScript ESLint parser: {' '.join(install_cmd)}")
                    try:
                        subprocess.run(install_cmd, cwd=project_path, check=True, capture_output=True, timeout=120)
                        logger.info("TypeScript ESLint parser installed successfully")
                    except subprocess.TimeoutExpired:
                        logger.warning("TypeScript ESLint parser installation timed out after 120 seconds")
                    except subprocess.CalledProcessError as e:
                        logger.warning(f"Failed to install TypeScript ESLint parser: {e}")
                        logger.warning("Will continue with basic ESLint configuration")
            except Exception as e:
                logger.warning(f"Error checking for TypeScript ESLint parser: {e}")
        
        # Build the ESLint command
        js_files = [f for f in files_to_scan if f.endswith(('.js', '.jsx'))]
        ts_files = [f for f in files_to_scan if f.endswith(('.ts', '.tsx'))]
        
        # Combine all files to scan
        all_files = js_files + ts_files
        
        if not all_files:
            logger.warning("No JavaScript or TypeScript files found to scan")
            return {"error": "No JavaScript or TypeScript files found to scan", "stdout": None, "stderr": None, "returncode": 0}
        
        # Build the ESLint command based on config type
        if is_flat_config:
            # For ESLint 8.x with flat config
            eslint_cmd = ["eslint", "--config", config_path, "-f", "json"]
        else:
            # For ESLint with traditional config
            eslint_cmd = ["eslint", "--config", config_path, "-f", "json"]
        
        # Add files to scan
        eslint_cmd.extend(all_files)
        
        logger.info(f"Running ESLint command: {' '.join(eslint_cmd)}")
        result = _run_command_and_capture(eslint_cmd, cwd=project_path)
        
        # Check if we got any output
        if result["returncode"] != 0 and not result["stdout"]:
            # If ESLint fails with no output, try running with --no-eslintrc to bypass config issues
            logger.warning("ESLint failed with no output. Trying with --no-eslintrc flag.")
            fallback_cmd = ["eslint", "--no-eslintrc", "-f", "json"]
            fallback_cmd.extend(all_files)
            logger.info(f"Running fallback ESLint command: {' '.join(fallback_cmd)}")
            result = _run_command_and_capture(fallback_cmd, cwd=project_path)
        
        # Clean up the temporary tsconfig.json if we created one
        if ts_files_exist and not os.path.exists(os.path.join(project_path, 'tsconfig.json')) and os.path.exists(tsconfig_path):
            try:
                os.remove(tsconfig_path)
                logger.info("Removed temporary tsconfig.json")
            except Exception as e:
                logger.warning(f"Failed to remove temporary tsconfig.json: {e}")
        
        return result
    except Exception as e:
        logger.error(f"Error running ESLint: {e}")
        return {"error": f"Error running ESLint: {e}", "stdout": None, "stderr": str(e), "returncode": -1}

def run_typescript_check(project_path):
    """Run TypeScript compiler in noEmit mode to check for errors."""
    try:
        # Check if TypeScript is already installed globally
        check_cmd = ["tsc", "--version"]
        try:
            result = subprocess.run(check_cmd, cwd=project_path, capture_output=True, text=True)
            if result.returncode == 0:
                logger.info("TypeScript is already installed globally")
            else:
                # Install TypeScript locally if needed
                install_cmd = ["npm", "install", "--no-save", "typescript"]
                logger.info(f"Installing TypeScript: {' '.join(install_cmd)}")
                try:
                    subprocess.run(install_cmd, cwd=project_path, check=True, capture_output=True, timeout=60)
                    logger.info("TypeScript installed successfully")
                except subprocess.TimeoutExpired:
                    logger.warning("TypeScript installation timed out after 60 seconds")
                except subprocess.CalledProcessError as e:
                    logger.warning(f"Failed to install TypeScript: {e}")
                    # Continue anyway as it might be already installed globally
        except Exception as e:
            logger.warning(f"Error checking for TypeScript: {e}")
            # Continue without installing

        # Check for tsconfig.json
        tsconfig_path = os.path.join(project_path, 'tsconfig.json')
        tsconfig_args = []
        
        if os.path.exists(tsconfig_path):
            logger.info(f"Found TypeScript configuration: {tsconfig_path}")
        else:
            logger.warning("No tsconfig.json found. Using default TypeScript configuration.")
            # When no tsconfig.json exists, we need to specify files explicitly
            # Find TypeScript files manually
            ts_files = []
            for root, dirs, files in os.walk(project_path):
                # Skip node_modules, dist, and build directories
                if any(excluded in root for excluded in ['node_modules', 'dist', 'build']):
                    continue
                    
                for file in files:
                    if file.endswith(('.ts', '.tsx')):
                        ts_files.append(os.path.join(root, file))
            
            if not ts_files:
                logger.warning("No TypeScript files found to check")
                return {"warning": "No TypeScript files found to check"}
                
            # Convert to relative paths
            ts_files = [os.path.relpath(f, project_path) for f in ts_files]
            tsconfig_args.extend(ts_files)

        # Build the TypeScript check command
        cmd = ["tsc", "--noEmit"]
        cmd.extend(tsconfig_args)
        
        logger.info(f"Running command: {' '.join(cmd)}")
        
        # Run TypeScript compiler with a timeout
        try:
            result = subprocess.run(cmd, cwd=project_path, capture_output=True, text=True, timeout=60)
            
            # TypeScript compiler returns 0 if no errors, non-zero if errors
            if result.returncode != 0:
                # This is expected for files with type errors
                logger.info(f"TypeScript found issues (Exit Code: {result.returncode})")
                
            # Format the output to match our expected format
            output = []
            if result.stderr:
                # Parse the TypeScript error output
                error_lines = result.stderr.splitlines()
                for line in error_lines:
                    if ': error TS' in line:
                        parts = line.split(': error TS')
                        if len(parts) >= 2:
                            file_loc = parts[0]
                            message = 'error TS' + parts[1]
                            
                            # Try to extract file, line, and column
                            file_parts = file_loc.split('(')
                            file_path = file_parts[0]
                            line_col = "1:1"  # Default
                            
                            if len(file_parts) > 1:
                                line_col = file_parts[1].rstrip(')')
                            
                            line_col_parts = line_col.split(',')
                            line = line_col_parts[0] if len(line_col_parts) > 0 else "1"
                            col = line_col_parts[1] if len(line_col_parts) > 1 else "1"
                            
                            output.append({
                                "filePath": file_path,
                                "messages": [{
                                    "ruleId": "typescript",
                                    "severity": 2,
                                    "message": message,
                                    "line": int(line),
                                    "column": int(col)
                                }]
                            })
            
            return output
                
        except subprocess.TimeoutExpired:
            logger.error("TypeScript compiler process timed out after 60 seconds")
            return {"error": "TypeScript compiler process timed out after 60 seconds"}
            
    except Exception as e:
        logger.error(f"Error running TypeScript compiler: {e}")
        return {"error": f"Error running TypeScript compiler: {e}"}

def main(project_path, language_arg, output_dir=None):
    """
    Main function to orchestrate the scanning process.
    """
    logger.info(f"Starting scan for project at: {project_path}")
    print(f"Starting scan for project at: {project_path}")
    spinner.start("Initializing scan...")
    
    if not os.path.isdir(project_path):
        logger.error(f"Error: Path '{project_path}' is not a valid directory.")
        spinner.stop("Error: Invalid project path")
        sys.exit(1)

    detected_language = detect_language(project_path, language_arg)

    if not detected_language:
        logger.error("\n" + "#"*80)
        logger.error("ERROR: Could not determine project language.")
        logger.error(f"Please specify using --language {' or --language '.join(SUPPORTED_LANGUAGES)},")
        logger.error("or ensure the project contains recognizable files (e.g., package.json, requirements.txt, .py, .js, etc.).")
        logger.error("\nSee README.md for more information on supported languages and detection.")
        logger.error("#"*80)
        spinner.stop("Error: Could not determine project language")
        sys.exit(1)

    spinner.stop("Scan initialization complete")
    spinner.start("Running tools...")
    analysis_results = run_tools(project_path, detected_language)
    spinner.stop("Tool execution complete")

    # Check if any tools were actually attempted (i.e., results dict is not empty)
    if not analysis_results:
        logger.error("\n" + "#"*80)
        logger.error("ERROR: No analysis tools were attempted for the detected language.")
        logger.error("This might indicate an internal script error.")
        logger.error("\nPlease check README.md for troubleshooting information.")
        logger.error("#"*80)
        spinner.stop("Error: No tools were attempted")
        sys.exit(1)
    # Further check if all attempted tools failed or were not found
    elif all(isinstance(r, dict) and r.get("error") for r in analysis_results.values()):
         logger.warning("\n" + "#"*80)
         logger.warning("WARNING: All attempted analysis tools failed or were not found.")
         logger.warning("Please check tool installations and console output above.")
         logger.warning("\nSee README.md for installation instructions for required tools.")
         logger.warning("#"*80 + "\n")
         spinner.stop("Warning: All tools failed or were not found")
         # Continue to generate the report, which will show the errors

    spinner.start("Generating report...")
    if not generate_report(analysis_results, output_dir):
        print("\nReport generation failed. Please check the log file for details.")
        return
    spinner.stop("Report generation complete")

    print("\nScan finished.")
    print("Report generated: " + os.path.abspath(os.path.join(output_dir, REPORT_FILENAME)))
    print(f"Log file with detailed messages: {os.path.abspath(LOG_FILENAME)}")
    print("\nIf tools were missing, please see README.md for installation instructions.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Scan a project directory for best practices and security issues.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s /path/to/project -l python    # Scan Python project
  %(prog)s /path/to/project -l typescript # Scan TypeScript project
"""
    )
    parser.add_argument("project_path", help="Path to the project directory to scan")
    parser.add_argument("-l", "--language", help="Specify language to scan (python, javascript, typescript, go, ruby)")
    parser.add_argument("-o", "--output", help="Specify output directory for reports (optional, will prompt if not provided)")
    args = parser.parse_args()

    # Print a welcome banner
    print("\n" + "=" * 80)
    print(" VIBE CODE SCANNER ".center(80, "="))
    print("=" * 80)
    print(" Scanning your code for best practices and security issues ".center(80))
    print("=" * 80 + "\n")

    try:
        # Create output directory if it doesn't exist
        if args.output:
            os.makedirs(args.output, exist_ok=True)
        
        main(args.project_path, args.language, args.output)

        # Print a completion banner
        print("\n" + "=" * 80)
        print(" Scan Complete ".center(80, "="))
        print("=" * 80)
        print(f" Report saved to: {os.path.abspath(os.path.join(args.output, REPORT_FILENAME))} ".center(80))
        print(f" JSON data saved to: {os.path.abspath(os.path.join(args.output, JSON_REPORT_FILENAME))} ".center(80))
        print(f" Log file saved to: {os.path.abspath(LOG_FILENAME)} ".center(80))
        print("=" * 80)
        print(" Use these files with AI assistants like Windsurf for remediation ".center(80))
        print("=" * 80 + "\n")

    except KeyboardInterrupt:
        print("\n\nScan interrupted by user. Exiting...")
        spinner.stop("Scan interrupted")
        sys.exit(1)
    except Exception as e:
        print(f"\n\nAn unexpected error occurred: {e}")
        spinner.stop("Error occurred")
        logger.error(f"Unexpected error: {e}", exc_info=True)
        sys.exit(1)
