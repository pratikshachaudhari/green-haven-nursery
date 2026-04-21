"""
Green Haven Nursery - Input Validators
Validates user input for security and data integrity
"""

import re


def validate_email(email):
    """
    Validate email format
    
    Args:
        email (str): Email address to validate
    
    Returns:
        bool: True if valid, False otherwise
    """
    if not email:
        return False
    
    # Basic email regex pattern
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_pattern, email) is not None


def validate_password(password):
    """
    Validate password strength
    
    Args:
        password (str): Password to validate
    
    Returns:
        bool: True if valid, False otherwise
    
    Rules:
        - Minimum 6 characters
    """
    if not password:
        return False
    
    return len(password) >= 6


def validate_phone(phone):
    """
    Validate phone number format
    
    Args:
        phone (str): Phone number to validate
    
    Returns:
        bool: True if valid, False otherwise
    
    Accepts formats:
        - (555) 123-4567
        - 555-123-4567
        - 5551234567
        - +1 555 123 4567
    """
    if not phone:
        return False
    
    # Remove all non-digit characters except +
    cleaned = re.sub(r'[^\d+]', '', phone)
    
    # Check if it has at least 10 digits
    digit_count = len(re.findall(r'\d', cleaned))
    
    return digit_count >= 10


def sanitize_string(text, max_length=None):
    """
    Sanitize string input by removing potentially dangerous characters
    
    Args:
        text (str): Text to sanitize
        max_length (int, optional): Maximum allowed length
    
    Returns:
        str: Sanitized text
    """
    if not text:
        return ""
    
    # Remove leading/trailing whitespace
    sanitized = text.strip()
    
    # Truncate if max_length specified
    if max_length and len(sanitized) > max_length:
        sanitized = sanitized[:max_length]
    
    return sanitized


def validate_positive_number(value, max_value=None):
    """
    Validate that a value is a positive number
    
    Args:
        value: Value to validate
        max_value (int/float, optional): Maximum allowed value
    
    Returns:
        bool: True if valid, False otherwise
    """
    try:
        num = float(value)
        if num <= 0:
            return False
        
        if max_value is not None and num > max_value:
            return False
        
        return True
    except (TypeError, ValueError):
        return False


def validate_integer(value, min_value=None, max_value=None):
    """
    Validate that a value is an integer within optional bounds
    
    Args:
        value: Value to validate
        min_value (int, optional): Minimum allowed value
        max_value (int, optional): Maximum allowed value
    
    Returns:
        bool: True if valid, False otherwise
    """
    try:
        num = int(value)
        
        if min_value is not None and num < min_value:
            return False
        
        if max_value is not None and num > max_value:
            return False
        
        return True
    except (TypeError, ValueError):
        return False
