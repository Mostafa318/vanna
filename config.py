# Configuration file for Vanna Farsi

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Application configuration"""
    
    # Flask settings
    SECRET_KEY = os.getenv('SECRET_KEY', 'vanna-farsi-secret-key-change-in-production')
    DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'
    HOST = os.getenv('HOST', '0.0.0.0')
    PORT = int(os.getenv('PORT', 5000))
    
    # Database settings
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///sample_data.db')
    DATABASE_TYPE = os.getenv('DATABASE_TYPE', 'sqlite')  # sqlite, postgresql, mysql
    
    # Ollama settings
    OLLAMA_BASE_URL = os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434')
    OLLAMA_MODEL = os.getenv('OLLAMA_MODEL', 'llama2')
    
    # Vanna settings
    VECTOR_DB_TYPE = os.getenv('VECTOR_DB_TYPE', 'chromadb')
    VECTOR_DB_PATH = os.getenv('VECTOR_DB_PATH', './chroma_db')
    
    # UI settings
    APP_TITLE = 'وانا فارسی - دستیار هوشمند SQL'
    APP_SUBTITLE = 'تبدیل سوالات فارسی به کوئری SQL'
    
    # Sample data settings
    SAMPLE_DATA_ENABLED = os.getenv('SAMPLE_DATA_ENABLED', 'True').lower() == 'true'
    
    # Logging settings
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = os.getenv('LOG_FILE', 'vanna_farsi.log')
    
    @classmethod
    def get_database_config(cls):
        """Get database configuration based on type"""
        if cls.DATABASE_TYPE == 'postgresql':
            return {
                'host': os.getenv('POSTGRES_HOST', 'localhost'),
                'port': int(os.getenv('POSTGRES_PORT', 5432)),
                'database': os.getenv('POSTGRES_DB', 'vanna_farsi'),
                'user': os.getenv('POSTGRES_USER', 'postgres'),
                'password': os.getenv('POSTGRES_PASSWORD', ''),
            }
        elif cls.DATABASE_TYPE == 'mysql':
            return {
                'host': os.getenv('MYSQL_HOST', 'localhost'),
                'port': int(os.getenv('MYSQL_PORT', 3306)),
                'database': os.getenv('MYSQL_DB', 'vanna_farsi'),
                'user': os.getenv('MYSQL_USER', 'root'),
                'password': os.getenv('MYSQL_PASSWORD', ''),
            }
        else:  # sqlite
            return {
                'database': 'sample_data.db'
            }
    
    @classmethod
    def get_vanna_config(cls):
        """Get Vanna configuration"""
        return {
            'ollama_base_url': cls.OLLAMA_BASE_URL,
            'model': cls.OLLAMA_MODEL,
            'chroma_db_impl': 'duckdb+parquet',
            'persist_directory': cls.VECTOR_DB_PATH,
        }

# Development configuration
class DevelopmentConfig(Config):
    DEBUG = True
    LOG_LEVEL = 'DEBUG'

# Production configuration
class ProductionConfig(Config):
    DEBUG = False
    LOG_LEVEL = 'WARNING'

# Testing configuration
class TestingConfig(Config):
    TESTING = True
    DATABASE_URL = 'sqlite:///:memory:'
    SAMPLE_DATA_ENABLED = False

# Configuration mapping
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

def get_config():
    """Get configuration based on environment"""
    env = os.getenv('FLASK_ENV', 'development')
    return config.get(env, config['default'])