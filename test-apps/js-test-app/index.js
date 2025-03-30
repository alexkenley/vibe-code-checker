// Main application entry point with intentional issues

// Unused variable (no-unused-vars)
const unusedVariable = "This variable is never used";

// Console statement (no-console)
console.log("Application starting...");

// Global variable without declaration (no-undef)
globalVar = "This is a global variable without proper declaration";

// Security issue: eval usage (no-eval)
function processUserInput(input) {
    return eval(input); // Dangerous use of eval
}

// Inconsistent spacing and missing semicolons (semi)
const add = function(a,b) {
    return a+b
}

// Duplicate key in object (no-dupe-keys)
const config = {
    apiKey: "abc123",
    timeout: 5000,
    apiKey: "xyz789" // Duplicate key
};

// Unreachable code (no-unreachable)
function getData() {
    return "data";
    console.log("This will never be executed"); // Unreachable code
}

// Potential memory leak with event listeners
function setupEventListeners() {
    document.getElementById("button").addEventListener("click", function() {
        console.log("Button clicked");
        // No cleanup for event listener
    });
}

// Insecure random number generation
function generateToken() {
    return Math.random().toString(36).substring(2); // Not cryptographically secure
}

// SQL Injection vulnerability
function queryDatabase(userId) {
    const query = "SELECT * FROM users WHERE id = " + userId; // SQL injection vulnerability
    return query;
}

// XSS vulnerability
function displayUserInput(input) {
    document.getElementById("output").innerHTML = input; // XSS vulnerability
}

// Main application code
function main() {
    console.log("Running main application");
    
    const result = add(5,10);
    console.log("Result:", result);
    
    const token = generateToken();
    console.log("Generated token:", token);
    
    setupEventListeners();
    
    const query = queryDatabase("user_123");
    console.log("Query:", query);
    
    // Potential prototype pollution
    const userInput = { "__proto__": { "polluted": true } };
    const obj = {};
    Object.assign(obj, userInput);
}

// Immediately invoked function with improper spacing
(function(){
    main();
})();
