# JavaScript Test App

This is a test application with intentional code quality issues and security vulnerabilities to help test and demonstrate the capabilities of the Vibe Code Scanner.

## Intentional Issues

### Security Issues

1. **Vulnerable Dependencies:**
   - Outdated jQuery, Lodash, and Moment.js with known vulnerabilities
   - These should be detected by RetireJS

2. **Insecure Code Patterns:**
   - Use of `eval()` in `index.js` (line 14)
   - Insecure regex patterns with unnecessary escape characters in `utils.js` (line 24)
   - Unsafe prototype access in `utils.js` (line 50)
   - Hardcoded credentials in `utils.js` (lines 20-21)
   - SQL injection vulnerability in `api.js` (line 15)
   - XSS vulnerability in `index.js` (line 55)

### Code Quality Issues

1. **ESLint Detectable Issues:**
   - Unused variables throughout the codebase
   - Missing semicolons in `index.js`
   - Unreachable code in `index.js` (line 32)
   - Duplicate object keys in `index.js` (line 26)
   - Unnecessary console statements
   - Use of `==` instead of `===` in `utils.js` (line 13)

## Setup

```bash
npm install
```

## Running the Scanner

From the root of the Vibe Code Scanner project:

```bash
docker run -v "$(pwd)/test-apps/js-test-app:/code" vibe-code-scanner /code
```

## File Structure

- **index.js:** Main application file with various code issues
- **utils.js:** Utility functions with additional issues
- **api.js:** API handling functions with security vulnerabilities
- **index.html:** HTML file that integrates the JavaScript files
- **package.json:** Dependencies with known vulnerabilities
