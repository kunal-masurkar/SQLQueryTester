import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    # Database configuration
    DB_TYPE = os.getenv('DB_TYPE', 'sqlite').strip().lower()  # Clean and lowercase the DB_TYPE
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT = os.getenv('DB_PORT', '5432')
    DB_NAME = os.getenv('DB_NAME', 'test_db')
    DB_USER = os.getenv('DB_USER', '')
    DB_PASSWORD = os.getenv('DB_PASSWORD', '')

    # Construct database URI based on type
    if DB_TYPE == 'sqlite':
        DATABASE_URI = f'sqlite:///{DB_NAME}.db'
    elif DB_TYPE == 'postgresql':
        DATABASE_URI = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
    elif DB_TYPE == 'mysql':
        DATABASE_URI = f'mysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
    else:
        # Default to SQLite if an unsupported type is provided
        print(f"Warning: Unsupported database type '{DB_TYPE}'. Defaulting to SQLite.")
        DATABASE_URI = f'sqlite:///{DB_NAME}.db'

    # Application configuration
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev_secret_key_123')
    DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'
    
    # Test configuration
    TEST_CASES_DIR = 'tests/test_cases'
    # Clean and parse MAX_QUERY_EXECUTION_TIME value
    try:
        max_time = os.getenv('MAX_QUERY_EXECUTION_TIME', '5').strip()
        # Remove any comments or extra text
        max_time = max_time.split('#')[0].strip()
        MAX_QUERY_EXECUTION_TIME = float(max_time)
    except ValueError:
        print("Warning: Invalid MAX_QUERY_EXECUTION_TIME value. Defaulting to 5 seconds.")
        MAX_QUERY_EXECUTION_TIME = 5.0

    SQL_INJECTION_PATTERNS = [
        "' OR '1'='1",
        "'; DROP TABLE users; --",
        "' UNION SELECT * FROM users; --",
        "1' OR '1'='1",
        "1; DROP TABLE users; --"
    ]

    # Report configuration
    REPORT_DIR = 'reports'
    REPORT_FORMATS = ['json', 'yaml', 'html'] 