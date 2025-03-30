// Utility functions with intentional issues

// Missing strict mode declaration
// 'use strict'; - intentionally omitted

// Unused parameters (no-unused-params)
function formatData(data, options, callback) {
    return JSON.stringify(data); // options and callback are never used
}

// Comparison with type conversion (eqeqeq)
function checkValue(value) {
    if (value == 0) { // Should use === for strict equality
        return "zero";
    }
    return "non-zero";
}

// Hardcoded credentials (no-hardcoded-credentials)
const API_KEY = "sk_live_12345abcdefghijklmnopqrstuvwxyz";
const DATABASE_PASSWORD = "P@ssw0rd123!";

// Inefficient regex (optimize-regex)
const EMAIL_REGEX = /^([a-zA-Z0-9_\.\-])+\@(([a-zA-Z0-9\-])+\.)+([a-zA-Z0-9]{2,4})+$/;

// Insecure random values for security purposes
function generateSecretKey() {
    return Math.floor(Math.random() * 1000000).toString(); // Not cryptographically secure
}

// Buffer constructor deprecation warning
function createBuffer(data) {
    return new Buffer(data); // Should use Buffer.from() instead
}

// Potential timing attack vulnerability
function compareSecrets(secret1, secret2) {
    return secret1 === secret2; // Vulnerable to timing attacks
}

// Insecure cipher algorithm
function encryptData(data, key) {
    // This is just a placeholder - in real code, this would use an insecure algorithm
    return data + key; // Simplistic representation of weak encryption
}

// Prototype pollution
function mergeObjects(target, source) {
    for (const key in source) {
        if (source.hasOwnProperty(key)) {
            target[key] = source[key]; // Vulnerable to prototype pollution
        }
    }
    return target;
}

// Export functions
module.exports = {
    formatData,
    checkValue,
    generateSecretKey,
    createBuffer,
    compareSecrets,
    encryptData,
    mergeObjects
};
