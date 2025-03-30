# Python Test App

This is a test application with intentional code quality issues and security vulnerabilities to help test and demonstrate the capabilities of the Vibe Code Scanner.

## Intentional Issues

### Security Issues

1. **Vulnerable Dependencies:**
   - Outdated packages in requirements.txt with known vulnerabilities
   - These should be detected by the scanner

2. **Insecure Code Patterns:**
   - Use of `eval()` in `main.py` (line 29)
   - Hardcoded credentials in multiple files
   - Command injection vulnerabilities in `main.py` (lines 49-53)
   - SQL injection vulnerability in `main.py` (line 39)
   - Insecure deserialization with `pickle` in `main.py` (line 57)
   - Weak hash function (MD5) in `utils.py` (line 29)
   - Insecure "encryption" using base64 in `utils.py` (line 43)

### Code Quality Issues

1. **Flake8 Detectable Issues:**
   - Unused imports and variables throughout the codebase
   - Bare except clause in `main.py` (line 85)
   - Mutable default argument in `main.py` (line 89)
   - Redundant conditions in `utils.py` (line 76)
   - Comparison using `is` instead of `==` for strings in `utils.py` (line 72)

## Setup

```bash
pip install -r requirements.txt
```

## Running the Scanner

From the root of the Vibe Code Scanner project:

```bash
docker run -v "$(pwd)/test-apps/python-test-app:/code" vibe-code-scanner /code -l python
```

## File Structure

- **main.py:** Main application file with various code issues
- **utils.py:** Utility functions with additional issues
- **requirements.txt:** Dependencies with known vulnerabilities
