# Go Test App

This is a test application with intentional code quality issues and security vulnerabilities to help test and demonstrate the capabilities of the Vibe Code Scanner.

## Intentional Issues

### Security Issues

1. **Vulnerable Dependencies:**
   - Outdated packages in go.mod with known vulnerabilities
   - These should be detected by the scanner

2. **Insecure Code Patterns:**
   - Command injection vulnerability in `main.go` (line 39)
   - SQL injection vulnerability in `main.go` (line 49)
   - Weak hash function (MD5) in `main.go` (line 56)
   - Insecure file permissions in `main.go` (line 64)
   - Reflected XSS vulnerability in `main.go` (line 74)
   - Hardcoded credentials in multiple files
   - Path traversal vulnerability in `utils.go` (line 83)
   - Timing attack vulnerability in `utils.go` (line 89)

### Code Quality Issues

1. **Golangci-lint Detectable Issues:**
   - Unused variables throughout the codebase
   - Deprecated package usage (`io/ioutil`) in `main.go` (line 8)
   - Duplicate map key in `main.go` (line 23)
   - Unused function in `main.go` (line 28)
   - Redundant conditions in `utils.go` (line 44)
   - Potential nil pointer dereference in `utils.go` (line 77)

## Setup

```bash
go mod download
```

## Running the Scanner

From the root of the Vibe Code Scanner project:

```bash
docker run -v "$(pwd)/test-apps/go-test-app:/code" vibe-code-scanner /code -l go
```

## File Structure

- **main.go:** Main application file with various code issues
- **utils.go:** Utility functions with additional issues
- **go.mod:** Dependencies with known vulnerabilities
