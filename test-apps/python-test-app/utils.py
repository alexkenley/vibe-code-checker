"""
Utility functions for the Python test application.
Contains intentional issues for the Vibe Code Scanner to detect.
"""

import hashlib
import base64
import re

# Global configuration with hardcoded secrets (security issue)
GLOBAL_CONFIG = {
    "api_key": "1234567890abcdef",
    "secret": "super_secret_value",
    "database": {
        "host": "localhost",
        "user": "admin",
        "password": "admin123",  # Hardcoded password (security issue)
    }
}


def weak_hash_function(password):
    """
    Use a weak hash function for passwords (security issue).
    
    Args:
        password: Password to hash
    
    Returns:
        Hashed password using MD5 (weak)
    """
    # MD5 is a weak hash function (security issue)
    return hashlib.md5(password.encode()).hexdigest()  # nosec - Intentional security issue


def insecure_cipher(text):
    """
    Use a very weak encryption method (security issue).
    
    Args:
        text: Text to encrypt
    
    Returns:
        'Encrypted' text using base64 (not actual encryption)
    """
    # Base64 is not encryption (security issue)
    return base64.b64encode(text.encode()).decode()


def process_data(data, callback=None):
    """
    Process data with potential issues.
    
    Args:
        data: Data to process
        callback: Optional callback function
    
    Returns:
        Processed data
    """
    # Unused variable (code quality issue)
    temp_data = "This variable is never used"
    
    # Regex with potential catastrophic backtracking (security issue)
    email_pattern = r'^([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})$'
    
    if isinstance(data, dict):
        # Potential key error without proper handling
        return data["value"]
    
    # Return value not used (code quality issue)
    validate_input(data)
    
    return data.upper()


def validate_input(data):
    """
    Validate input with potential issues.
    
    Args:
        data: Data to validate
    
    Returns:
        True if valid, False otherwise
    """
    # Comparison using "is" instead of "==" (code quality issue)
    if data is None or data is "":  # noqa: E711 - Intentional comparison issue
        return False
    
    # Redundant condition (code quality issue)
    if len(data) > 0 and not len(data) == 0:
        return True
    
    return False


def get_user_data(user_id):
    """
    Get user data with potential path traversal vulnerability.
    
    Args:
        user_id: User ID to retrieve
    
    Returns:
        User data (simulated)
    """
    # Path traversal vulnerability (security issue)
    filename = f"user_{user_id}.json"
    path = f"data/{filename}"
    
    # Simulated file read
    print(f"Reading from {path}")
    
    # Return hardcoded data for simulation
    return {
        "id": user_id,
        "name": "Test User",
        "email": "test@example.com"
    }
