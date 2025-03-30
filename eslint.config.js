// @ts-check

// Basic ESLint flat configuration for the scanner
module.exports = [
  {
    // Ignore node_modules and build directories
    ignores: ["**/node_modules/**", "**/dist/**", "**/build/**"]
  },
  {
    // Base configuration for JavaScript files
    files: ["**/*.js", "**/*.jsx"],
    languageOptions: {
      ecmaVersion: 2022,
      sourceType: "module"
    },
    rules: {
      "no-unused-vars": "warn",
      "no-console": "warn"
    }
  },
  {
    // Configuration for TypeScript files
    files: ["**/*.ts", "**/*.tsx"],
    // TypeScript-specific rules will be handled by the .eslintrc.js file
    // This is just a placeholder for the flat config format
    languageOptions: {
      ecmaVersion: 2022,
      sourceType: "module"
    }
  }
];
