/**
 * Main module for the TypeScript test application.
 * Contains intentional issues for the Vibe Code Scanner to detect.
 */

import * as fs from 'fs';
import * as path from 'path';
import * as crypto from 'crypto';
import axios from 'axios';
import { processData, GLOBAL_CONFIG } from './utils';

// Unused import (code quality issue)
import * as http from 'http';

// Global variable (not necessarily an issue, but often flagged)
const DEBUG: boolean = true;

// Hardcoded credentials (security issue)
const API_KEY: string = '1234567890abcdef';
const DB_PASSWORD: string = 'super_secret_password';

// Interface with missing properties
interface User {
  id: number;
  name: string;
  // Missing email property that's used later
}

// Class with intentional issues
class UserManager {
  private users: Record<string, User> = {};
  
  // Hardcoded path (potential issue)
  private configPath: string = '/etc/app/config.json';
  
  constructor() {
    // Empty constructor
  }
  
  // Insecure method using eval (security issue)
  public insecureFunction(userInput: string): any {
    // Insecure use of eval (security issue)
    // @ts-ignore
    const result = eval(userInput); // eslint-disable-line no-eval
    return result;
  }
  
  // SQL injection vulnerability (security issue)
  public sqlInjectionVulnerable(userId: string): void {
    // SQL injection vulnerability (security issue)
    const query = `SELECT * FROM users WHERE id = ${userId}`;
    // Execute query (simulated)
    console.log(`Executing query: ${query}`);
  }
  
  // Command injection vulnerability (security issue)
  public commandInjectionVulnerable(filename: string): void {
    // Command injection vulnerability (security issue)
    const { execSync } = require('child_process');
    execSync(`ls ${filename}`);
    
    // Another command injection vulnerability
    execSync(`echo ${filename}`);
  }
  
  // Weak hash function (security issue)
  public weakHash(password: string): string {
    // MD5 is a weak hash function (security issue)
    return crypto.createHash('md5').update(password).digest('hex');
  }
  
  // Method with multiple issues
  public processUserInput(input: string): void {
    // Unused variable (code quality issue)
    const unusedVar: string = "This variable is never used";
    
    // Try-catch with empty catch (code quality issue)
    try {
      const config = JSON.parse(fs.readFileSync(this.configPath, 'utf8'));
    } catch (error) {
      // Empty catch block (code quality issue)
    }
    
    // Function with mutable default parameter (code quality issue)
    function processItems(items: string[] = []): string[] {
      items.push("processed");
      return items;
    }
    
    // Call the function with potential security issues
    const userInput: string = "2 + 2"; // Simulated user input
    const result = this.insecureFunction(userInput);
    console.log(`Result: ${result}`);
    
    // Call SQL injection vulnerable function
    const userId: string = "1; DROP TABLE users;"; // Simulated malicious input
    this.sqlInjectionVulnerable(userId);
    
    // Call command injection vulnerable function
    const filename: string = "file.txt; rm -rf /"; // Simulated malicious input
    this.commandInjectionVulnerable(filename);
    
    // Potential null reference (code quality issue)
    const user: User = { id: 1, name: 'John' };
    // @ts-ignore
    console.log(user.email.toLowerCase()); // Will cause runtime error
  }
  
  // Unused method (code quality issue)
  public unusedMethod(): void {
    console.log("This method is never called");
  }
  
  // XSS vulnerability (security issue)
  public renderUserProfile(userInput: string): string {
    // XSS vulnerability (security issue)
    const html = `<div>Welcome, ${userInput}!</div>`;
    return html;
  }
  
  // Insecure direct object reference (security issue)
  public getUserData(userId: string): User {
    // No authorization check (security issue)
    return this.users[userId];
  }
  
  // Prototype pollution vulnerability (security issue)
  public mergeObjects(target: any, source: any): any {
    // Prototype pollution vulnerability (security issue)
    for (const key in source) {
      if (typeof source[key] === 'object' && source[key] !== null) {
        if (!target[key]) target[key] = {};
        this.mergeObjects(target[key], source[key]);
      } else {
        target[key] = source[key];
      }
    }
    return target;
  }
}

// Main execution
function main(): void {
  // Create a new user manager
  const manager = new UserManager();
  
  // Process user input (simulated)
  manager.processUserInput("2 + 2");
  
  // Print debugging information
  if (DEBUG) {
    console.log("Debug mode is enabled");
  }
  
  // Render user profile with potential XSS
  const html = manager.renderUserProfile("<script>alert('XSS')</script>");
  console.log(`Rendered HTML: ${html}`);
  
  // Insecure random values (security issue)
  const insecureRandom = Math.random(); // Not cryptographically secure
  
  // Hardcoded JWT secret (security issue)
  const jwtSecret = "your-256-bit-secret";
  
  // Return statement with no return value (code quality issue)
  return;
}

// Call the main function
main();
