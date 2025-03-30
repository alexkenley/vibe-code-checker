# Vibe Code Scanner

A simple script to scan a project codebase for common best practice and security issues using various open-source static analysis tools.

## Purpose

This script helps developers, especially those newer to coding ("vibe coders"), ensure their code aligns with common standards before potentially using AI assistants in IDEs (like Windsurf, Cursor) for targeted fixes. It runs tools for Python, JavaScript, TypeScript, Go, and Ruby, and generates a consolidated report.

## Important: Basic Requirements

**Python 3.x is required to run the scanner itself**, regardless of what language you're scanning. [Download Python from python.org](https://www.python.org/downloads/) if you don't have it installed.

**Additional requirements by language:**
- **JavaScript/TypeScript scanning:** Requires Node.js installed ([nodejs.org](https://nodejs.org/))
- **Go scanning:** Requires Go installed ([go.dev](https://go.dev/doc/install))
- **Ruby scanning:** Requires Ruby installed ([ruby-lang.org](https://www.ruby-lang.org/))

## Simplified Installation: Using Docker (Recommended)

If you have Docker installed, you can skip all the complex tool installations and run the scanner in a container with all tools pre-installed!

### Docker Container Details

The Docker container includes the following pre-installed tools:

- **Python 3.x** with flake8 and bandit
- **Node.js 18.x** with ESLint 8.56.0, TypeScript ESLint 6.21.0, and RetireJS 4.3.2
- **Go 1.22.1** with golangci-lint and gosec
- **Ruby** with RuboCop and Brakeman

This ensures all tools are compatible and properly configured, avoiding common installation and version compatibility issues.

### Using Docker (Windows)

1. Install [Docker Desktop](https://www.docker.com/products/docker-desktop/) if you don't have it already
   - You'll need to create a free Docker account during installation
   - During installation, make sure to select the option to use WSL 2 if prompted
   - After installation, you may need to restart your computer

2. **Important:** Make sure you're logged in to Docker Desktop
   - Open Docker Desktop application
   - Click "Sign in" in the top-right corner
   - Enter your Docker account credentials
   - Wait for the login process to complete

3. Open a command prompt in the scanner directory

4. Run the scanner with:

   cmd line:
   docker-scan.bat "C:\path\to\your\project" [-l language]

### Using Docker (Mac/Linux)

1. Install Docker if you don't have it already
   - For Mac: Install [Docker Desktop](https://www.docker.com/products/docker-desktop/) (requires a free Docker account)
   - For Linux: Install Docker Engine using your distribution's package manager (no account required)

2. **For Mac users:** Make sure you're logged in to Docker Desktop
   - Open Docker Desktop application
   - Sign in with your Docker account credentials

3. Open a terminal in the scanner directory

4. Make the script executable: `chmod +x docker-scan.sh`

5. Run the scanner with:

   cmd line:
   ./docker-scan.sh /path/to/your/project [-l language]

The Docker approach automatically handles all tool installations and PATH issues for you!

### Troubleshooting Docker Issues

If you encounter authentication errors or other issues when building or running the Docker container:

1.  **Confirm Docker Email:** Ensure you have confirmed the email address associated with your Docker Hub account.
2.  **Restart Docker Desktop:** Try quitting and restarting Docker Desktop.
3.  **Check Login Status:** Make sure you are logged into Docker Desktop. You might need to log out and log back in.
4.  **Restart Your Computer:** Sometimes a simple system restart can resolve unexpected issues.
5.  **Check Network:** Ensure you have a stable internet connection, as Docker needs to download images.

If problems persist, consider using the manual installation method described below.

## Manual Installation (Alternative)

If you prefer not to use Docker, you can install the required tools manually. This approach requires more setup but doesn't require Docker.

## How to Use the Command Line (for Beginners on Windows)

If you've never used a command line or terminal before, here's a quick guide:

1.  **Open Command Prompt:**
    *   Click the Windows Start button (usually in the bottom-left corner).
    *   Type `cmd` or `Command Prompt`.
    *   Click on the "Command Prompt" application that appears.
    *   A black window with text will open. This is the command line!

2.  **Running Commands:**
    *   You type commands into this window and press `Enter` to run them.
    *   Commands are usually short instructions for the computer.
    *   For example, to install the Python tools needed for this scanner, you'll type the `pip install ...` command shown below and press `Enter`.

3.  **Changing Directories (Folders):**
    *   Sometimes you need to tell the command line which folder to work in.
    *   Use the `cd` command (which stands for "change directory").
    *   Example: If your project is in `C:\Users\YourName\Documents\MyProject`, you would type:
        ```
cd C:\Users\YourName\Documents\MyProject
```
    *   **Important:** If the path to your folder has spaces in it (like `C:\Users\Your Name\My Project`), you **must** put double quotes (`"`) around the whole path:
        ```
cd "C:\Users\Your Name\My Project"
```
    *   (Replace `YourName` and `MyProject` with your actual folder names!)
    *   You can copy the folder path from Windows File Explorer's address bar.

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
