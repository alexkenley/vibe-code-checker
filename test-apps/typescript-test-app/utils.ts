/**
 * Utility functions for the TypeScript test application.
 * Contains intentional issues for the Vibe Code Scanner to detect.
 */

import * as crypto from 'crypto';
import * as fs from 'fs';
import * as path from 'path';

// Global configuration with hardcoded secrets (security issue)
export const GLOBAL_CONFIG = {
  apiKey: '1234567890abcdef',
  secret: 'super_secret_value',
  database: {
    host: 'localhost',
    user: 'admin',
    password: 'admin123', // Hardcoded password (security issue)
  }
};

// Type with missing properties
export type DataProcessor = {
  process: (data: any) => any;
  // Missing validate method that's used later
};

/**
 * Insecure cipher function using weak encryption
 * @param text Text to encrypt
 * @returns 'Encrypted' text
 */
export function insecureCipher(text: string): string {
  // Base64 is not encryption (security issue)
  return Buffer.from(text).toString('base64');
}

/**
 * Weak hash function for passwords
 * @param password Password to hash
 * @returns Hashed password using MD5 (weak)
 */
export function weakHashFunction(password: string): string {
  // MD5 is a weak hash function (security issue)
  return crypto.createHash('md5').update(password).digest('hex');
}

/**
 * Process data with potential issues
 * @param data Data to process
 * @param callback Optional callback function
 * @returns Processed data
 */
export function processData(data: any, callback?: Function): any {
  // Unused variable (code quality issue)
  const tempData: string = "This variable is never used";
  
  // Regex with potential catastrophic backtracking (security issue)
  const emailPattern = /^([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})$/;
  
  if (typeof data === 'object' && data !== null) {
    // Potential key error without proper handling
    return data.value;
  }
  
  // Return value not used (code quality issue)
  validateInput(data);
  
  // Callback invocation without checking if it exists (code quality issue)
  // @ts-ignore
  callback(data);
  
  return data.toUpperCase();
}

/**
 * Validate input with potential issues
 * @param data Data to validate
 * @returns True if valid, False otherwise
 */
export function validateInput(data: any): boolean {
  // Type coercion issue (code quality issue)
  if (data == null) {
    return false;
  }
  
  // Redundant condition (code quality issue)
  if (data.length > 0 && data.length !== 0) {
    return true;
  }
  
  return false;
}

/**
 * Get user data with potential path traversal vulnerability
 * @param userId User ID to retrieve
 * @returns User data (simulated)
 */
export function getUserData(userId: string): any {
  // Path traversal vulnerability (security issue)
  const filename = `user_${userId}.json`;
  const path = `data/${filename}`;
  
  // Simulated file read
  console.log(`Reading from ${path}`);
  
  // Return hardcoded data for simulation
  return {
    id: userId,
    name: 'Test User',
    email: 'test@example.com'
  };
}

/**
 * Unsafe deserialization function
 * @param data Data to deserialize
 * @returns Deserialized object
 */
export function unsafeDeserialization(data: string): any {
  // Unsafe deserialization (security issue)
  return JSON.parse(data);
}

/**
 * Insecure file operations
 * @param filename Filename to read
 * @returns File content
 */
export function readFileInsecure(filename: string): string {
  // Path traversal vulnerability (security issue)
  return fs.readFileSync(filename, 'utf8');
}

/**
 * Insecure cookie setting
 * @param name Cookie name
 * @param value Cookie value
 * @returns Cookie string
 */
export function setInsecureCookie(name: string, value: string): string {
  // Insecure cookie (security issue)
  return `${name}=${value}; path=/`;
}

/**
 * Function with memory leak
 * @returns Large array
 */
export function memoryLeakFunction(): number[] {
  // Potential memory leak (code quality issue)
  const largeArray: number[] = [];
  for (let i = 0; i < 1000000; i++) {
    largeArray.push(i);
  }
  return largeArray;
}

/**
 * Function with race condition
 * @param sharedResource Shared resource
 */
export function raceConditionFunction(sharedResource: any): void {
  // Race condition (security issue)
  sharedResource.value += 1;
  // No synchronization mechanism
}

// Class with intentional issues
export class InsecureProcessor {
  private data: any;
  
  constructor(data: any) {
    this.data = data;
  }
  
  // Method with prototype pollution
  public extend(source: any): void {
    // Prototype pollution (security issue)
    for (const key in source) {
      this.data[key] = source[key];
    }
  }
  
  // Method with timing attack vulnerability
  public compareToken(userToken: string, actualToken: string): boolean {
    // Timing attack vulnerability (security issue)
    return userToken === actualToken;
  }
}
