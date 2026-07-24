import re


def clean_text(text):
    """
    Clean text using regular expressions
    
    Args:
        text (str): Text to clean
        
    Returns:
        str: Cleaned text
    """
    # Remove extra whitespace
    cleaned = re.sub(r'\s+', ' ', text).strip()
    
    # Remove special characters but keep basic punctuation
    cleaned = re.sub(r'[^\w\s.,!?\'"-]', '', cleaned)
    
    return cleaned


def find_warning_words(text):
    """
    Find warning-related keywords in text using regular expressions
    
    Args:
        text (str): Text to search for warnings
        
    Returns:
        list: List of found warning keywords
    """
    warning_keywords = [
        "warning",
        "danger",
        "avoid",
        "risk",
        "caution",
        "side effects",
        "allergic",
        "serious",
        "emergency",
        "overdose",
        "contraindication",
        "interaction",
        "pregnancy",
        "breastfeeding"
    ]
    
    found_warnings = []
    text_lower = text.lower()
    
    for keyword in warning_keywords:
        # Use regex to find whole words or phrases
        pattern = re.compile(r'\b' + re.escape(keyword) + r'\b', re.I)
        if pattern.search(text_lower):
            found_warnings.append(keyword)
    
    return found_warnings


def validate_medication_name(name):
    """
    Validate medication name using regular expression
    
    Args:
        name (str): Medication name to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    # Allow letters, spaces, hyphens, apostrophes
    pattern = r'^[A-Za-z\s\-&#039;]{2,50}$'
    return re.match(pattern, name.strip()) is not None


def extract_medication_info(text):
    """
    Extract medication information from text using regex
    
    Args:
        text (str): Text to extract information from
        
    Returns:
        dict: Extracted information
    """
    info = {}
    
    # Extract dosage information
    dosage_pattern = r'(\d+)\s*(mg|mcg|g|ml|tablet|capsule)'
    dosages = re.findall(dosage_pattern, text, re.I)
    if dosages:
        info['dosages'] = [f"{d[0]} {d[1]}" for d in dosages]
    
    # Extract frequency
    frequency_pattern = r'(once|twice|three times|daily|weekly|monthly)'
    frequencies = re.findall(frequency_pattern, text, re.I)
    if frequencies:
        info['frequencies'] = frequencies
    
    return info
