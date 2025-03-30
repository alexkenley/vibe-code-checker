# Ruby on Rails Test App

This is a Ruby on Rails test application with intentional code quality issues and security vulnerabilities to help test and demonstrate the capabilities of the Vibe Code Scanner.

## Intentional Issues

### Security Issues

1. **Vulnerable Dependencies:**
   - Outdated gems in Gemfile with known vulnerabilities (Rails 5.2.3, Nokogiri 1.10.3, etc.)
   - These should be detected by RuboCop and Brakeman

2. **Insecure Code Patterns:**
   - Use of `eval()` in `app/controllers/application_controller.rb`
   - Hardcoded credentials in multiple files
   - Command injection vulnerabilities in controller actions
   - SQL injection vulnerability in model queries
   - Weak hash function (MD5) in multiple files
   - XSS vulnerability in views
   - Mass assignment vulnerability in models
   - Unsafe deserialization in utility classes
   - Path traversal vulnerability in file handling
   - YAML deserialization vulnerability in configuration
   - Insecure random number generation in token generation
   - Weak SSL/TLS configuration in initializers
   - Timing attack vulnerability in authentication
   - CSRF vulnerability (missing CSRF protection)
   - Session fixation vulnerability in authentication
   - HTTP header injection in response handling
   - Insecure direct object reference in controllers
   - XML external entity (XXE) vulnerability in XML parsing
   - Insecure cookie settings in session management
   - Open redirect vulnerability in redirect handling

### Code Quality Issues

1. **RuboCop Detectable Issues:**
   - Unused variables throughout the codebase
   - Unused methods in controllers and models
   - Bare rescue clause in error handling
   - Redundant conditions in business logic
   - Global variables in initializers
   - Missing documentation
   - Style violations (indentation, line length, etc.)
   - Complexity issues (too many lines in methods, etc.)

## Security Scanning Tools

This test app is designed to be scanned by Ruby on Rails security scanning tools:

1. **RuboCop:** Detects code quality issues and some security issues
2. **Brakeman:** Detects security vulnerabilities in Rails applications

## Setup

```bash
bundle install
```

## Running the Scanner

From the root of the Vibe Code Scanner project:

```bash
docker run -v "$(pwd)/test-apps/ruby-test-app:/code" vibe-code-scanner /code
```

## File Structure

- **app/controllers/:** Controllers with various security vulnerabilities
- **app/models/:** Models with insecure queries and mass assignment issues
- **app/views/:** Views with XSS vulnerabilities
- **config/:** Configuration files with security issues
- **lib/:** Utility classes with additional vulnerabilities
- **Gemfile:** Dependencies with known vulnerabilities
- **Gemfile.lock:** Locked dependencies with specific versions
