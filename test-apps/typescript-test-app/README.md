# TypeScript Test App

This is a test application with intentional code quality issues and security vulnerabilities to help test and demonstrate the capabilities of the Vibe Code Scanner.

## Running the Scanner

From the root of the Vibe Code Scanner project:

```bash
docker run -v "$(pwd)/test-apps/typescript-test-app:/code" vibe-code-scanner /code
```

## Intentional Issues

### Security Issues

1. **Vulnerable Dependencies:**
   - Outdated packages in package.json with known vulnerabilities
   - These should be detected by RetireJS

2. **Insecure Code Patterns:**
   - Use of `eval()` in `index.ts` (line 42)
   - Hardcoded credentials in multiple files
   - Command injection vulnerabilities in `index.ts` (lines 52-56)
   - SQL injection vulnerability in `index.ts` (line 47)
   - Weak hash function (MD5) in multiple files
   - XSS vulnerability in `index.ts` (line 109)
   - Prototype pollution in `index.ts` (line 120) and `utils.ts` (line 162)
   - Insecure deserialization in `utils.ts` (line 111)
   - Path traversal vulnerability in `utils.ts` (line 92)
   - Timing attack vulnerability in `utils.ts` (line 169)

### Code Quality Issues

1. **ESLint Detectable Issues:**
   - Unused imports and variables throughout the codebase
   - Empty catch blocks in `index.ts` (line 74)
   - Unused methods in `index.ts` (line 104)
   - Potential null reference in `index.ts` (line 91)
   - Type coercion issues in `utils.ts` (line 83)
   - Redundant conditions in `utils.ts` (line 88)
   - Callback invocation without null check in `utils.ts` (line 68)

2. **TypeScript-Specific Issues:**
   - Use of `any` type throughout the codebase
   - Improper type declarations in `types.d.ts`
   - Missing type annotations in function parameters
   - Incorrect interface implementations
   - Use of deprecated TypeScript features
   - Type assertion issues
   - Unused type imports

## File Structure

- **index.ts:** Main application file with various code issues
- **utils.ts:** Utility functions with additional issues
- **types.d.ts:** Type declarations with intentional issues
- **package.json:** Dependencies with known vulnerabilities
- **tsconfig.json:** TypeScript configuration
- **.eslintrc.js:** ESLint configuration for TypeScript
