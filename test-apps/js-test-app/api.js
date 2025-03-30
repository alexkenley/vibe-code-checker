// API handling functions with intentional security and code quality issues

const utils = require('./utils');

// Command injection vulnerability
function executeCommand(command) {
    const { exec } = require('child_process');
    exec(command); // Command injection vulnerability
    return `Executed: ${command}`;
}

// Path traversal vulnerability
function readUserFile(filename) {
    const fs = require('fs');
    const path = require('path');
    
    // Path traversal vulnerability - no sanitization of filename
    const filePath = path.join('./user_files', filename);
    return fs.readFileSync(filePath, 'utf8');
}

// Insecure deserialization
function deserializeUserData(data) {
    return JSON.parse(data); // No validation before parsing
}

// Improper error handling exposing sensitive information
function getUserData(userId) {
    try {
        // Simulating database query
        if (!userId) {
            throw new Error("Database connection failed: credentials in /etc/db_config.json are invalid");
        }
        return { id: userId, name: "Test User" };
    } catch (error) {
        // Error message contains sensitive information
        console.error(`Error fetching user: ${error.message}`);
        return { error: error.message }; // Leaks sensitive error details to client
    }
}

// Insecure cookie settings
function setAuthCookie(res, token) {
    res.cookie('auth_token', token, {
        // Missing security flags
        // httpOnly: true,
        // secure: true,
        // sameSite: 'strict'
    });
}

// Weak password validation
function validatePassword(password) {
    return password.length >= 6; // Too short, no complexity requirements
}

// No rate limiting on authentication
function authenticateUser(username, password) {
    // No rate limiting implemented
    if (username === "admin" && password === "password") {
        return { success: true, token: utils.generateSecretKey() };
    }
    return { success: false };
}

// Insecure redirect
function redirectUser(req, res) {
    const redirectUrl = req.query.redirect;
    res.redirect(redirectUrl); // No validation of redirect URL
}

// Missing CSRF protection
function updateUserProfile(req, res) {
    // No CSRF token validation
    const user = {
        name: req.body.name,
        email: req.body.email
    };
    return { success: true, user };
}

module.exports = {
    executeCommand,
    readUserFile,
    deserializeUserData,
    getUserData,
    setAuthCookie,
    validatePassword,
    authenticateUser,
    redirectUser,
    updateUserProfile
};
