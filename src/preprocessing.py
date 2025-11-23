import re
import string

def normalize_text(text):
    """
    Normalizes transaction description text.
    1. Lowercase
    2. Remove special characters (keep alphanumeric and spaces)
    3. Remove extra spaces
    """
    if not isinstance(text, str):
        return ""
    
    text = text.lower()
    # Replace punctuation with space
    text = text.translate(str.maketrans(string.punctuation, ' ' * len(string.punctuation)))
    # Remove digits (optional, depending on if numbers are useful like store IDs, but usually noise)
    # text = re.sub(r'\d+', '', text) 
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

def preprocess_dataframe(df, text_column="description"):
    """
    Applies normalization to a dataframe column.
    """
    df[f"clean_{text_column}"] = df[text_column].apply(normalize_text)
    return df
