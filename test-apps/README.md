# Test Applications for Vibe Code Scanner

This directory contains test applications with intentional code quality issues and security vulnerabilities to help test and demonstrate the capabilities of the Vibe Code Scanner.

## Available Test Applications

### JavaScript Test App (`js-test-app`)

A simple JavaScript application with intentional issues:
- Vulnerable dependencies
- Code quality issues (unused variables, missing semicolons)
- Security issues (eval usage, insecure patterns)

To run the scanner on this app:
```bash
docker run -v "$(pwd)/test-apps/js-test-app:/code" vibe-code-scanner /code
```

### TypeScript Test App (`typescript-test-app`)

A TypeScript application with intentional issues:
- Vulnerable dependencies in package.json
- Code quality issues (unused variables, empty catch blocks)
- Security issues (eval usage, prototype pollution, weak crypto)

To run the scanner on this app:
```bash
docker run -v "$(pwd)/test-apps/typescript-test-app:/code" vibe-code-scanner /code
```

### Python Test App (`python-test-app`)

A Python application with intentional issues:
- Vulnerable dependencies in requirements.txt
- Code quality issues (unused imports, variables)
- Security issues (eval usage, command injection, SQL injection)

To run the scanner on this app:
```bash
docker run -v "$(pwd)/test-apps/python-test-app:/code" vibe-code-scanner /code -l python
```

### Go Test App (`go-test-app`)

A Go application with intentional issues:
- Vulnerable dependencies in go.mod
- Code quality issues (unused variables, deprecated packages)
- Security issues (command injection, SQL injection, weak crypto)

To run the scanner on this app:
```bash
docker run -v "$(pwd)/test-apps/go-test-app:/code" vibe-code-scanner /code -l go
```

### Ruby Test App (`ruby-test-app`)

A Ruby on Rails application with intentional issues:
- Vulnerable gems in Gemfile
- Code quality issues (unused variables, bare rescues)
- Security issues (eval usage, command injection, unsafe deserialization)
- Rails-specific vulnerabilities (CSRF, mass assignment, etc.)

To run the scanner on this app:
```bash
docker run -v "$(pwd)/test-apps/ruby-test-app:/code" vibe-code-scanner /code -l ruby
```

## Adding New Test Applications

When adding new test applications, please follow these guidelines:

1. Create a new directory with a descriptive name (e.g., `python-test-app`, `go-test-app`)
2. Include intentional issues that the scanner should detect
3. Document the issues in a README.md file within the test app directory
4. Keep the test app small and focused on demonstrating specific scanner capabilities

## Purpose

These test applications serve several purposes:

1. **Demonstration**: They showcase the types of issues that the Vibe Code Scanner can detect.
2. **Testing**: They provide a consistent test bed for verifying that the scanner is working correctly.
3. **Development**: They help in developing and refining the scanner's detection capabilities.
4. **Documentation**: They serve as examples of what constitutes problematic code.

Each test application contains README.md files with more detailed information about the specific issues included.

## Contributing

Feel free to add new test applications or improve existing ones. Make sure to document the intentional issues so others can understand what the scanner should detect.
