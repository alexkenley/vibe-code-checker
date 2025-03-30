#!/usr/bin/env python3
"""
Main module for the Python test application.
Contains intentional issues for the Vibe Code Scanner to detect.
"""

import os
import sys
import json
import pickle  # nosec - Intentional security issue
import subprocess  # nosec - Intentional security issue
from utils import process_data, GLOBAL_CONFIG

# Unused import (flake8: F401)
import random

# Global variable (not necessarily an issue, but often flagged)
DEBUG = True

# Hardcoded credentials (security issue)
API_KEY = "1234567890abcdef"
DB_PASSWORD = "super_secret_password"


def insecure_function(user_input):
    """
    Intentionally insecure function that uses eval.
    
    Args:
        user_input: User-provided input
    """
    # Insecure use of eval (security issue)
    result = eval(user_input)  # nosec - Intentional security issue
    return result


def sql_injection_vulnerable(user_id):
    """
    Function with SQL injection vulnerability.
    
    Args:
        user_id: User ID to query
    """
    # SQL injection vulnerability (security issue)
    query = "SELECT * FROM users WHERE id = " + user_id
    # Execute query (simulated)
    return f"Executing query: {query}"


def command_injection_vulnerable(filename):
    """
    Function with command injection vulnerability.
    
    Args:
        filename: Filename to process
    """
    # Command injection vulnerability (security issue)
    os.system(f"ls {filename}")  # nosec - Intentional security issue
    
    # Another command injection vulnerability
    subprocess.call(f"echo {filename}", shell=True)  # nosec - Intentional security issue


def insecure_deserialization(data):
    """
    Function with insecure deserialization.
    
    Args:
        data: Data to deserialize
    """
    # Insecure deserialization (security issue)
    return pickle.loads(data)  # nosec - Intentional security issue


def unused_function():
    """This function is never called (code quality issue)."""
    pass


def main():
    """Main function."""
    # Unused variable (code quality issue)
    unused_var = "This variable is never used"
    
    # Print debugging information
    if DEBUG:
        print("Debug mode is enabled")
    
    # Hardcoded path (potential issue)
    config_path = "/etc/app/config.json"
    
    # Try-except with bare except (code quality issue)
    try:
        with open(config_path) as f:
            config = json.load(f)
    except:  # noqa: E722 - Intentional bare except
        print("Error loading configuration")
    
    # Mutable default argument (code quality issue)
    def process_items(items=[]):  # noqa: B006 - Intentional mutable default
        items.append("processed")
        return items
    
    # Call the function with potential security issues
    user_input = "2 + 2"  # Simulated user input
    result = insecure_function(user_input)
    print(f"Result: {result}")
    
    # Call SQL injection vulnerable function
    user_id = "1; DROP TABLE users;"  # Simulated malicious input
    sql_injection_vulnerable(user_id)
    
    # Call command injection vulnerable function
    filename = "file.txt; rm -rf /"  # Simulated malicious input
    command_injection_vulnerable(filename)
    
    # Return statement with no return value (code quality issue)
    return


if __name__ == "__main__":
    main()
