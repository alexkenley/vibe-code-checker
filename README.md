# Vibe Code Scanner

A simple tool to scan your code for security vulnerabilities and quality issues, designed for developers of all experience levels.

## Quick Start Guide for Beginners

This guide will walk you through the entire process of getting and using Vibe Code Scanner, even if you've never used GitHub or Docker before.

### Step 1: Get the Code from GitHub

1. **Download the repository**:
   - Go to https://github.com/alexkenley/vibe-code-scanner
   - Click the green "Code" button
   - Select "Download ZIP"
   - Extract the ZIP file to a location on your computer (e.g., your Documents folder)

   Alternatively, if you're familiar with Git:
   ```bash
   git clone https://github.com/alexkenley/vibe-code-scanner.git
   ```

### Step 2: Install Docker Desktop

1. **Download Docker Desktop**:
   - Go to [docker.com](https://www.docker.com/products/docker-desktop/)
   - Click "Download for Windows" (or Mac/Linux depending on your system)
   - Create a free Docker account if prompted during download

2. **Install Docker Desktop**:
   - Run the installer you downloaded
   - Follow the installation prompts
   - On Windows: Select the option to use WSL 2 if prompted
   - After installation completes, restart your computer if required

3. **Start Docker Desktop**:
   - Launch Docker Desktop from your applications/programs menu
   - Wait for Docker to fully start (the whale icon in the taskbar will stop animating)
   - Sign in to Docker Desktop:
     - Click "Sign in" in the top-right corner
     - Enter your Docker account credentials
     - Wait for the login process to complete

### Step 3: Build the Scanner

1. **Open a terminal/command prompt**:
   - On Windows: Press Win+R, type "cmd" and press Enter
   - On Mac: Open Terminal from Applications > Utilities
   - On Linux: Open your terminal application

2. **Navigate to the Vibe Code Scanner directory**:
   ```bash
   cd path/to/vibe-code-scanner
   ```
   Replace "path/to/vibe-code-scanner" with the actual path where you extracted the ZIP file

3. **Build the Docker image**:
   ```bash
   docker build -t vibe-code-scanner .
   ```
   (Note: Don't forget the period at the end!)

4. **Wait for the build to complete**:
   - This may take a few minutes the first time
   - You'll see a lot of text scrolling as Docker downloads and installs all the necessary tools

### Step 4: Scan Your Project

1. **Navigate to your project directory** in the terminal:
   ```bash
   cd path/to/your/project
   ```
   Replace "path/to/your/project" with the path to the code you want to scan

2. **Run the scanner** with one of these commands:

   **Windows (PowerShell):**
   ```powershell
   docker run -v "${PWD}:/code" vibe-code-scanner /code
   ```

   **Windows (Command Prompt):**
   ```cmd
   docker run -v "%cd%:/code" vibe-code-scanner /code
   ```

   **Mac/Linux:**
   ```bash
   docker run -v "$(pwd):/code" vibe-code-scanner /code
   ```

3. **For specific language scanning**, add the `-l` flag:
   ```bash
   docker run -v "$(pwd):/code" vibe-code-scanner /code -l python
   ```
   
   Supported language options: `javascript`, `typescript`, `python`, `go`, `ruby`

### Step 5: View the Results

1. After the scan completes, the results will be saved in a new `reports` directory in your project:
   - `reports/vibe_scan_report.md` - Human-readable Markdown report
   - `reports/vibe_scan_report.json` - Machine-readable JSON data

2. Open the Markdown report in any Markdown viewer or text editor to see the issues found

3. Use the report with AI assistants like Windsurf or Cursor to help fix the identified issues:
   - Open your AI-powered IDE
   - Point it to your project and the report
   - Ask for help fixing specific issues

### Troubleshooting Docker

If you encounter issues with Docker:

1. **Docker not starting**: Ensure virtualization is enabled in your BIOS/UEFI settings
2. **Permission errors**: On Linux, you may need to add your user to the docker group
3. **Volume mounting issues**: Make sure you're using the correct syntax for your operating system
4. **Docker Desktop not running**: Look for the Docker icon in your system tray and ensure it's running

## Purpose

This script helps developers, especially those newer to coding ("vibe coders"), ensure their code aligns with common standards before potentially using AI assistants in IDEs (like Windsurf, Cursor) for targeted fixes. It runs tools for Python, JavaScript, TypeScript, Go, and Ruby, and generates a consolidated report.

## Supported Languages and Tools

The scanner includes the following pre-installed tools:

- **JavaScript/TypeScript**: ESLint, RetireJS, TypeScript Compiler
- **Python**: Flake8, Bandit
- **Go**: golangci-lint, gosec
- **Ruby on Rails**: RuboCop, Brakeman (security scanner)

## Test Applications

The repository includes test applications with intentional code quality issues and security vulnerabilities in the `test-apps` directory. These applications help demonstrate the capabilities of the scanner and can be used for testing.

### JavaScript Test App

A simple JavaScript application with intentional issues:
- Vulnerable dependencies
- Code quality issues (unused variables, missing semicolons)
- Security issues (eval usage, insecure patterns)

### TypeScript Test App

A TypeScript application with intentional issues:
- Vulnerable dependencies in package.json
- Code quality issues (unused variables, empty catch blocks)
- Security issues (eval usage, prototype pollution, weak crypto)

### Python Test App

A Python application with intentional issues:
- Vulnerable dependencies in requirements.txt
- Code quality issues (unused imports, variables)
- Security issues (eval usage, command injection, SQL injection)

### Go Test App

A Go application with intentional issues:
- Vulnerable dependencies in go.mod
- Code quality issues (unused variables, deprecated packages)
- Security issues (command injection, SQL injection, weak crypto)

### Ruby Test App

A Ruby on Rails application with intentional issues:
- Vulnerable gems in Gemfile
- Code quality issues (unused variables, bare rescues)
- Security issues (eval usage, command injection, unsafe deserialization)
- Rails-specific vulnerabilities (CSRF, mass assignment, etc.)

To run the scanner on any test app:

```bash
# From the root of the Vibe Code Scanner project
docker run -v "$(pwd)/test-apps/js-test-app:/code" vibe-code-scanner /code
docker run -v "$(pwd)/test-apps/typescript-test-app:/code" vibe-code-scanner /code
docker run -v "$(pwd)/test-apps/python-test-app:/code" vibe-code-scanner /code -l python
docker run -v "$(pwd)/test-apps/go-test-app:/code" vibe-code-scanner /code -l go
docker run -v "$(pwd)/test-apps/ruby-test-app:/code" vibe-code-scanner /code -l ruby
```

For more details, see the [Test Applications README](./test-apps/README.md).

## Advanced Installation: Manual Setup

If you prefer not to use Docker, you can install the tools manually. This is more complex and requires installing multiple dependencies.

### Important: Basic Requirements

**Python 3.x is required to run the scanner itself**, regardless of what language you're scanning. [Download Python from python.org](https://www.python.org/downloads/) if you don't have it installed.

**Additional requirements by language:**
- **JavaScript/TypeScript scanning:** Requires Node.js installed ([nodejs.org](https://nodejs.org/))
- **Go scanning:** Requires Go installed ([go.dev](https://go.dev/doc/install))
- **Ruby scanning:** Requires Ruby and Rails installed ([ruby-lang.org](https://www.ruby-lang.org/) and [rubyonrails.org](https://rubyonrails.org/))

## Prerequisites: Required Tools by Language

The scanner requires specific tools for each language you want to scan. You only need to install the tools for the languages you want to scan!

### Python
- **Base requirement:** Python 3.x
- **Required tools:** flake8, bandit
- **What they check:** Style/errors, security

### JavaScript/TypeScript
- **Base requirement:** Node.js
- **Required tools:** eslint, retire
- **What they check:** Style/errors, security vulnerabilities

### Go
- **Base requirement:** Go
- **Required tools:** golangci-lint, gosec
- **What they check:** Linting, security

### Ruby
- **Base requirement:** Ruby, RubyGems
- **Required tools:** rubocop, brakeman
- **What they check:** Style/errors, security

**Remember**: You only need to install the tools for the languages you want to scan!

## Installation Instructions

### 1. Install Python 3 (Required for All Users)

1. Download from [python.org](https://www.python.org/downloads/)
2. During installation, check the box that says "Add Python to PATH"
3. Verify installation by opening a command prompt and typing:
   
   cmd line:
   python --version
   
   You should see something like `Python 3.x.x`

### 2. Install Language-Specific Tools

#### For Python Projects

cmd line:
pip install flake8 bandit

#### For JavaScript/TypeScript Projects

1. **Install Node.js** from [nodejs.org](https://nodejs.org/) (LTS version recommended)
   - During installation:
     - Make sure to select the option to add Node.js to your PATH
     - You do NOT need to check "Automatically install the necessary tools" for native modules - this is not required for the scanner
   - This will install both `node` and `npm` commands
   - `npx` (Node Package Execute) is also included with Node.js installation - it's a tool that allows running packages without installing them globally

2. Verify installation:
   
   cmd line:
   node --version
   npm --version
   npx --version
   
3. Install ESLint (for style/error checking):
   
   cmd line:
   # Navigate to your project folder first
   cd path\to\your\project
   npm install eslint@8.56.0 --save-dev
   
   Note: The scanner uses `npx` to run the locally installed ESLint in your project.
   
4. Install RetireJS (for security scanning):
   
   cmd line:
   npm install -g retire
   
   After installation, verify it works:
   
   cmd line:
   retire --version

**Troubleshooting Node.js Tools:**

If you see errors like "npx not found" or "retire not found" even after installing Node.js:

1. **Restart your command prompt** - Sometimes the PATH environment variable isn't updated in existing command prompts
2. **Verify tools work outside the scanner** - Try running `npx --version` and `retire --version` directly
3. **Run the scanner from the same command prompt** where these commands work
4. **Check your PATH environment variable** - Make sure it includes the Node.js installation directory

   To manually add Node.js to your PATH on Windows:
   - Right-click on "This PC" or "My Computer" and select "Properties"
   - Click on "Advanced system settings"
   - Click the "Environment Variables" button
   - Under "System variables", find and select "Path", then click "Edit"
   - Click "New" and add the Node.js installation directory (typically `C:\Program Files\nodejs\`)
   - Click "OK" on all dialogs to save changes
   - Close and reopen any command prompts for changes to take effect

5. **Try restarting your computer** - This ensures all environment variables are properly updated

#### For Go Projects

1. Install Go from [go.dev/doc/install](https://go.dev/doc/install)
2. Install the required tools:
   
   cmd line:
   # Install golangci-lint
   go install github.com/golangci/golangci-lint/cmd/golangci-lint@latest
   
   # Install gosec
   go install github.com/securego/gosec/v2/cmd/gosec@latest
   
3. Make sure Go's bin directory is in your PATH

#### For Ruby Projects

1. Install Ruby from [ruby-lang.org](https://www.ruby-lang.org/en/documentation/installation/)
2. Install the required tools:
   
   cmd line:
   gem install rubocop
   gem install brakeman

## How to Run the Scanner

1.  Open your command line (see guide above).
2.  Navigate to the folder where you saved the `scan.py` script using the `cd` command.
3.  Run the script, telling it where your project code is located. Replace `/path/to/your/project` with the actual path to the folder containing the code you want to scan:
   
   cmd line:
   python scan.py /path/to/your/project
   
   *   Example for a project in `C:\Projects\MyWebApp`:
       ```
python scan.py C:\Projects\MyWebApp
```
   *   If your path has spaces, use quotes:
       ```
python scan.py "C:\My Projects\MyWebApp"
```
4.  The script will try to detect the language, run the installed tools, and print messages.
5.  A report file named `vibe_scan_report.md` will be created in the *same folder as the `scan.py` script*.
6.  A log file named `vibe_scan_log.txt` will contain detailed messages about any errors or missing tools.

### Optional: Specifying Language

If the scanner can't automatically detect your project's language, or you want to scan for a specific language, use the `-l` or `--language` option:
   
cmd line:
python scan.py /path/to/your/project -l python

Supported language options: `python`, `javascript`, `typescript`, `go`, `ruby`

## Troubleshooting

If you see errors about missing tools:

1. Check the log file (`vibe_scan_log.txt`) for detailed error messages
2. Make sure you've installed the required tools for your language (see table above)
3. Ensure the tools are in your system PATH
4. For JavaScript/TypeScript projects, make sure you're running the scan from the project root where ESLint is installed

## Understanding the Report

The generated `vibe_scan_report.md` file contains:

1. A summary of any tools that couldn't be run or encountered errors
2. A table of all issues found, including:
   - File path and line number
   - Severity of the issue
   - Rule or code that was violated
   - Description of the problem

You can use this report with AI assistants like those in Windsurf or Cursor to help fix the identified issues.
