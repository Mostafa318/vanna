#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import logging
from pathlib import Path

# Add the parent directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from config import get_config
from vanna.farsi_vanna import FarsiVanna

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_configuration():
    """Test the configuration setup"""
    print("🧪 Testing Configuration")
    print("=" * 50)
    
    try:
        # Get configuration
        config = get_config()
        print(f"✅ Configuration loaded successfully")
        print(f"   Environment: {os.getenv('FLASK_ENV', 'development')}")
        
        # Test database configuration
        print(f"\n🗄️  Database Configuration:")
        print(f"   Type: {config.DATABASE_TYPE}")
        
        if config.DATABASE_TYPE == 'postgresql':
            db_config = config.get_database_config()
            print(f"   Host: {db_config.get('host', 'N/A')}")
            print(f"   Port: {db_config.get('port', 'N/A')}")
            print(f"   Database: {db_config.get('database', 'N/A')}")
            print(f"   User: {db_config.get('user', 'N/A')}")
        
        # Test AI provider configuration
        print(f"\n🤖 AI Provider Configuration:")
        print(f"   Provider: {config.AI_PROVIDER}")
        
        if config.AI_PROVIDER == 'openai':
            print(f"   Model: {config.OPENAI_MODEL}")
            print(f"   API Key: {'✅ Set' if config.OPENAI_API_KEY else '❌ Not set'}")
        else:
            print(f"   Base URL: {config.OLLAMA_BASE_URL}")
            print(f"   Model: {config.OLLAMA_MODEL}")
        
        # Test vector database configuration
        print(f"\n🔍 Vector Database Configuration:")
        print(f"   Type: {config.VECTOR_DB_TYPE}")
        
        if config.VECTOR_DB_TYPE == 'chromadb':
            print(f"   Path: {config.VECTOR_DB_PATH}")
            print(f"   Implementation: {config.VECTOR_DB_IMPL}")
        
        # Test Vanna configuration
        print(f"\n⚙️  Vanna Configuration:")
        vanna_config = config.get_vanna_config()
        print(f"   Config keys: {list(vanna_config.keys())}")
        
        return True
        
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False

def test_vanna_initialization():
    """Test Vanna initialization"""
    print(f"\n🚀 Testing Vanna Initialization")
    print("=" * 50)
    
    try:
        config = get_config()
        vanna_config = config.get_vanna_config()
        vanna_config.update({
            'ai_provider': config.AI_PROVIDER,
            'vector_db_type': config.VECTOR_DB_TYPE,
        })
        
        # Initialize Vanna
        vn = FarsiVanna(config=vanna_config)
        print("✅ Vanna initialized successfully")
        
        # Test basic functionality
        print(f"   AI Provider: {type(vn.ai_provider).__name__}")
        print(f"   Vector Store: {type(vn.vector_store).__name__}")
        
        return True
        
    except Exception as e:
        print(f"❌ Vanna initialization failed: {e}")
        return False

def test_database_connection():
    """Test database connection"""
    print(f"\n🔌 Testing Database Connection")
    print("=" * 50)
    
    try:
        config = get_config()
        
        if config.DATABASE_TYPE == 'postgresql':
            import psycopg2
            db_config = config.get_database_config()
            
            if 'connection_string' in db_config:
                conn = psycopg2.connect(db_config['connection_string'])
            else:
                conn = psycopg2.connect(
                    host=db_config['host'],
                    port=db_config['port'],
                    database=db_config['database'],
                    user=db_config['user'],
                    password=db_config['password']
                )
            
            cursor = conn.cursor()
            cursor.execute('SELECT version()')
            version = cursor.fetchone()
            print(f"✅ PostgreSQL connected successfully")
            print(f"   Version: {version[0]}")
            
            cursor.close()
            conn.close()
            
        else:
            import sqlite3
            conn = sqlite3.connect('sample_data.db')
            cursor = conn.cursor()
            cursor.execute('SELECT sqlite_version()')
            version = cursor.fetchone()
            print(f"✅ SQLite connected successfully")
            print(f"   Version: {version[0]}")
            
            cursor.close()
            conn.close()
        
        return True
        
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

def test_ai_provider():
    """Test AI provider connection"""
    print(f"\n🧠 Testing AI Provider")
    print("=" * 50)
    
    try:
        config = get_config()
        
        if config.AI_PROVIDER == 'openai':
            import openai
            client = openai.OpenAI(api_key=config.OPENAI_API_KEY)
            
            # Test with a simple request
            response = client.chat.completions.create(
                model=config.OPENAI_MODEL,
                messages=[{"role": "user", "content": "Hello"}],
                max_tokens=10
            )
            print("✅ OpenAI API connected successfully")
            print(f"   Model: {config.OPENAI_MODEL}")
            
        else:
            import requests
            response = requests.get(f"{config.OLLAMA_BASE_URL}/api/tags", timeout=5)
            
            if response.status_code == 200:
                print("✅ Ollama connected successfully")
                print(f"   Base URL: {config.OLLAMA_BASE_URL}")
            else:
                raise Exception(f"Ollama returned status code {response.status_code}")
        
        return True
        
    except Exception as e:
        print(f"❌ AI provider test failed: {e}")
        return False

def main():
    """Main test function"""
    print("🧪 Vanna Farsi Configuration Test")
    print("=" * 60)
    
    tests = [
        ("Configuration", test_configuration),
        ("Vanna Initialization", test_vanna_initialization),
        ("Database Connection", test_database_connection),
        ("AI Provider", test_ai_provider),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} test failed with exception: {e}")
            results.append((test_name, False))
    
    # Print summary
    print(f"\n📊 Test Summary")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if result:
            passed += 1
    
    print(f"\nResults: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Configuration is working correctly.")
    else:
        print("⚠️  Some tests failed. Please check your configuration.")
        print("\n📝 Common issues:")
        print("1. Check your .env file configuration")
        print("2. Ensure all required services are running")
        print("3. Verify API keys and connection strings")
        print("4. Check network connectivity")

if __name__ == "__main__":
    main()