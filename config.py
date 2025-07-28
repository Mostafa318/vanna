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
    
    # PostgreSQL settings
    POSTGRES_HOST = os.getenv('POSTGRES_HOST', 'localhost')
    POSTGRES_PORT = int(os.getenv('POSTGRES_PORT', 5432))
    POSTGRES_DB = os.getenv('POSTGRES_DB', 'vanna_farsi')
    POSTGRES_USER = os.getenv('POSTGRES_USER', 'postgres')
    POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', '')
    POSTGRES_CONNECTION_STRING = os.getenv('POSTGRES_CONNECTION_STRING', '')
    
    # AI Model settings
    AI_PROVIDER = os.getenv('AI_PROVIDER', 'ollama')  # ollama, openai
    OLLAMA_BASE_URL = os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434')
    OLLAMA_MODEL = os.getenv('OLLAMA_MODEL', 'llama2')
    
    # OpenAI settings
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
    OPENAI_MODEL = os.getenv('OPENAI_MODEL', 'gpt-3.5-turbo')
    OPENAI_TEMPERATURE = float(os.getenv('OPENAI_TEMPERATURE', '0.7'))
    
    # Vector Database settings
    VECTOR_DB_TYPE = os.getenv('VECTOR_DB_TYPE', 'chromadb')  # chromadb, pgvector
    VECTOR_DB_PATH = os.getenv('VECTOR_DB_PATH', './chroma_db')
    
    # Vanna settings
    VECTOR_DB_IMPL = os.getenv('VECTOR_DB_IMPL', 'duckdb+parquet')
    
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
            if cls.POSTGRES_CONNECTION_STRING:
                return {
                    'connection_string': cls.POSTGRES_CONNECTION_STRING
                }
            else:
                return {
                    'host': cls.POSTGRES_HOST,
                    'port': cls.POSTGRES_PORT,
                    'database': cls.POSTGRES_DB,
                    'user': cls.POSTGRES_USER,
                    'password': cls.POSTGRES_PASSWORD,
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
        """Get Vanna configuration based on AI provider and vector DB type"""
        config = {}
        
        # AI Provider configuration
        if cls.AI_PROVIDER == 'openai':
            config.update({
                'api_key': cls.OPENAI_API_KEY,
                'model': cls.OPENAI_MODEL,
                'temperature': cls.OPENAI_TEMPERATURE,
            })
        else:  # ollama
            config.update({
                'ollama_base_url': cls.OLLAMA_BASE_URL,
                'model': cls.OLLAMA_MODEL,
            })
        
        # Vector DB configuration
        if cls.VECTOR_DB_TYPE == 'pgvector':
            db_config = cls.get_database_config()
            if 'connection_string' in db_config:
                config['connection_string'] = db_config['connection_string']
            else:
                # Build connection string from components
                config['connection_string'] = f"postgresql://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}"
        else:  # chromadb
            config.update({
                'chroma_db_impl': cls.VECTOR_DB_IMPL,
                'persist_directory': cls.VECTOR_DB_PATH,
            })
        
        return config

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