module.exports = {
  "env": {
    "browser": true,
    "commonjs": true,
    "es2021": true,
    "node": true
  },
  "extends": "eslint:recommended",
  "parserOptions": {
    "ecmaVersion": 12
  },
  "rules": {
    "no-unused-vars": "warn",
    "no-undef": "warn",
    "no-eval": "error",
    "semi": ["warn", "always"],
    "no-dupe-keys": "warn",
    "no-unreachable": "warn",
    "no-console": "warn",
    "eqeqeq": ["warn", "always"]
  }
};
