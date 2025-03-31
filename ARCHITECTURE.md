# Vibe Code Scanner Architecture

## Overview

Vibe Code Scanner is designed as a command-line Python script (`scan.py`) intended to be run locally by developers to identify code quality and security issues in their projects.

## Docker-Based Execution Model

**Important:** Vibe Code Scanner is designed to be run within a Docker container, not directly on the host system. This design choice ensures:

1. **Consistent Environment:** All required tools and dependencies are pre-installed in the container.
2. **No Local Tool Installation:** Users don't need to install language-specific tools on their machines.
3. **Cross-Platform Compatibility:** Works the same way across Windows, macOS, and Linux.
4. **Isolation:** Scanning operations run in an isolated environment.

The workflow is:
1. Build the Docker image using the provided Dockerfile
2. Run the scanner by mounting the target code directory into the container
3. View the generated reports in the target directory

Direct execution of `scan.py` on the host system is not recommended and will likely fail due to missing dependencies.

## Guiding Principle: Simplicity ("Follow the Bouncing Ball")

**Target Audience:** Developers with less coding experience (e.g., designers who code, "vibe coders").
**Core Goal:** Make code quality and security scanning accessible and easy.
**Implications:**
    *   **Minimal Setup:** Keep dependencies and configuration straightforward.
    *   **Simple Execution:** Single command execution.
    *   **Clear, Jargon-Free Reporting:** Explain findings in plain language.
    *   **Focus:** Prioritize common, high-impact best practice and security issues.
    *   **Actionable Output:** The report should clearly guide the user on potential next steps (e.g., using the report with an IDE AI assistant).

## Core Components

1.  **Command-Line Interface (CLI):**
    *   Uses Python's `argparse` module to accept the target project directory path and optional language specification.
    *   Provides helpful examples and guidance in the help text.
    *   Supports scanning GitHub repositories directly with the `--github` flag.

2.  **Language Detection Module:**
    *   A function within `scan.py` that analyzes the target directory's contents to determine the primary language.
    *   Detects languages based on file extensions and configuration files (e.g., `package.json`, `requirements.txt`, `tsconfig.json`).
    *   Supports Python, JavaScript, TypeScript, Go, and Ruby.
    *   Prioritizes user-specified language over auto-detection.

3.  **GitHub Repository Cloning:**
    *   Clones specified GitHub repositories to temporary directories.
    *   Supports cloning specific branches with the `-b` flag.
    *   Handles authentication for private repositories using personal access tokens.
    *   Automatically cleans up temporary directories after scanning.
    *   Handles errors gracefully with appropriate user feedback.

4.  **Prerequisite Checker:**
    *   Checks if required tools are installed before attempting to run them.
    *   Provides clear, actionable feedback when tools are missing.
    *   Directs users to the README for installation instructions.
    *   Uses `shutil.which()` to verify tool availability in the system PATH.

5.  **Static Analysis Tool Runner:**
    *   Uses Python's `subprocess` module to execute language-specific static analysis tools.
    *   Captures stdout, stderr, and return codes from each tool.
    *   Handles tool execution errors gracefully.
    *   Supported tools:
        *   **Python:** Flake8, Bandit
        *   **JavaScript/TypeScript:** ESLint (via npx)
        *   **Go:** golangci-lint, gosec
        *   **Ruby:** RuboCop (for code quality), Brakeman (for Rails security scanning)

6.  **Output Parsers:**
    *   Dedicated parser functions for each tool's output format.
    *   Handles both plain text and JSON output formats.
    *   Normalizes tool-specific output into a consistent issue format.
    *   Includes robust error handling for parsing failures.
    *   **Note:** While parsers are still included for backward compatibility, the primary approach now focuses on preserving raw tool outputs.

7.  **Report Generator:**
    *   Saves raw tool outputs to individual files for detailed analysis.
    *   Creates a JSON report with file references for AI assistant integration.
    *   Includes a summary of tool execution status.
    *   Provides links to documentation for fixing identified issues.
    *   Handles edge cases like missing tools or empty results.
    *   Focuses on preserving complete, unmodified tool outputs for maximum utility.

## Data Flow

1.  User executes one of the following:
    *   `python scan.py <project_path> [-l language]` to scan a local directory
    *   `python scan.py --github <repo_url> [-b branch]` to scan a GitHub repository
    *   `python scan.py --github <repo_url> --token <token>` to scan a private GitHub repository
2.  If a GitHub repository is specified:
    *   The script clones the repository to a temporary directory
    *   For private repositories, it uses the provided token for authentication
    *   The temporary directory is used as the project path for scanning
3.  The script validates the project path and detects or uses the specified language.
4.  For each applicable tool:
    *   Checks if the tool is installed and provides feedback if not.
    *   Executes the tool and captures its output.
    *   Saves the raw output to a dedicated file (`raw_<tool>_output.txt`).
5.  A JSON report is generated with:
    *   Tool execution summary
    *   References to raw output files
    *   Resource links
6.  The reports are written to the `reports` directory in the target project:
    *   `vibe_scan_report.json` - JSON report for AI assistants
    *   `raw_<tool>_output.txt` - Raw tool outputs for detailed analysis
7.  If a GitHub repository was cloned, the temporary directory is cleaned up.

## Error Handling

1.  **Missing Prerequisites:**
    *   Clearly identifies missing tools with specific installation instructions.
    *   Continues execution with available tools rather than failing completely.

2.  **Tool Execution Errors:**
    *   Captures and reports non-zero exit codes and stderr output.
    *   Distinguishes between "successful with issues found" and "execution failure" cases.

3.  **Parsing Errors:**
    *   Handles malformed tool output gracefully.
    *   Provides debugging information for troubleshooting.

4.  **Report Generation Errors:**
    *   Catches and reports file I/O errors.
    *   Ensures the user is informed if report generation fails.

## Security Considerations

*   When using GitHub personal access tokens, the token is never logged or displayed in error messages.
*   Temporary directories are securely created and properly cleaned up after scanning.
*   The scanner does not store or transmit any GitHub credentials.
*   Users should follow GitHub's best practices for token management, including:
    *   Using tokens with minimal required permissions (repo scope is sufficient)
    *   Regularly rotating tokens
    *   Not sharing tokens in public repositories or discussions

## Dependencies

*   **Core:** Python 3.x with standard library modules (argparse, os, subprocess, json, re, datetime, shutil, sys)
*   **External CLI tools:** (installed separately by the user)
    *   **Python:** flake8, bandit
    *   **JavaScript/TypeScript:** Node.js with npx (for ESLint)
    *   **Go:** golangci-lint, gosec
    *   **Ruby:** rubocop, brakeman (requires Rails application)

## Future Considerations

*   Configuration file for customizing tool settings and rule sets.
*   Support for additional GitHub features like:
    *   SSH key authentication
    *   Webhook integration for CI/CD pipelines
    *   GitHub Actions integration
*   Additional output formats (HTML, IDE-specific).
*   Automatic installation of missing tools.
*   Support for additional languages and frameworks.
*   Integration with CI/CD pipelines.
*   Custom rule definitions for project-specific standards.
