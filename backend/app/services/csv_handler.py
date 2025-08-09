import pandas as pd
from io import StringIO
from typing import List

def extract_fields_from_csv(file_content: bytes) -> List[str]:
    """Extract column headers from CSV file"""
    df = pd.read_csv(StringIO(file_content.decode('utf-8')), nrows=0)
    return df.columns.tolist()

def validate_csv_structure(file_content: bytes) -> bool:
    """Validate CSV file structure"""
    try:
        df = pd.read_csv(StringIO(file_content.decode('utf-8')), nrows=0)
        return len(df.columns) > 0
    except:
        return False