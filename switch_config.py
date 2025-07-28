#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
from pathlib import Path

def read_env_file():
    """Read the current .env file"""
    env_file = Path(".env")
    if not env_file.exists():
        return {}
    
    config = {}
    with open(env_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                config[key] = value
    
    return config

def write_env_file(config):
    """Write configuration to .env file"""
    env_file = Path(".env")
    
    # Read existing file to preserve comments and structure
    lines = []
    if env_file.exists():
        with open(env_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    
    # Update or add configuration values
    updated_keys = set()
    new_lines = []
    
    for line in lines:
        if line.strip() and not line.strip().startswith('#') and '=' in line:
            key = line.split('=', 1)[0]
            if key in config:
                new_lines.append(f"{key}={config[key]}\n")
                updated_keys.add(key)
            else:
                new_lines.append(line)
        else:
            new_lines.append(line)
    
    # Add new keys
    for key, value in config.items():
        if key not in updated_keys:
            new_lines.append(f"{key}={value}\n")
    
    # Write back to file
    with open(env_file, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)

def switch_to_openai():
    """Switch to OpenAI configuration"""
    print("🤖 Switching to OpenAI configuration...")
    
    config = read_env_file()
    
    # AI Provider settings
    config.update({
        'AI_PROVIDER': 'openai',
        'OPENAI_MODEL': 'gpt-3.5-turbo',
        'OPENAI_TEMPERATURE': '0.7'
    })
    
    # Remove Ollama settings
    config.pop('OLLAMA_BASE_URL', None)
    config.pop('OLLAMA_MODEL', None)
    
    write_env_file(config)
    print("✅ Switched to OpenAI configuration")
    print("📝 Please add your OpenAI API key to the .env file:")
    print("   OPENAI_API_KEY=your-api-key-here")

def switch_to_ollama():
    """Switch to Ollama configuration"""
    print("🦙 Switching to Ollama configuration...")
    
    config = read_env_file()
    
    # AI Provider settings
    config.update({
        'AI_PROVIDER': 'ollama',
        'OLLAMA_BASE_URL': 'http://localhost:11434',
        'OLLAMA_MODEL': 'llama2'
    })
    
    # Remove OpenAI settings
    config.pop('OPENAI_API_KEY', None)
    config.pop('OPENAI_MODEL', None)
    config.pop('OPENAI_TEMPERATURE', None)
    
    write_env_file(config)
    print("✅ Switched to Ollama configuration")
    print("📝 Make sure Ollama is running:")
    print("   ollama serve")

def switch_to_postgresql():
    """Switch to PostgreSQL configuration"""
    print("🐘 Switching to PostgreSQL configuration...")
    
    config = read_env_file()
    
    # Database settings
    config.update({
        'DATABASE_TYPE': 'postgresql',
        'POSTGRES_HOST': 'localhost',
        'POSTGRES_PORT': '5432',
        'POSTGRES_DB': 'vanna_farsi',
        'POSTGRES_USER': 'postgres',
        'POSTGRES_PASSWORD': 'postgres123'
    })
    
    # Vector database settings
    config.update({
        'VECTOR_DB_TYPE': 'pgvector'
    })
    
    # Remove SQLite settings
    config.pop('DATABASE_URL', None)
    
    write_env_file(config)
    print("✅ Switched to PostgreSQL configuration")
    print("📝 Make sure PostgreSQL is running:")
    print("   docker-compose -f docker-compose.postgresql.yml up -d")

def switch_to_sqlite():
    """Switch to SQLite configuration"""
    print("💾 Switching to SQLite configuration...")
    
    config = read_env_file()
    
    # Database settings
    config.update({
        'DATABASE_TYPE': 'sqlite',
        'DATABASE_URL': 'sqlite:///sample_data.db'
    })
    
    # Vector database settings
    config.update({
        'VECTOR_DB_TYPE': 'chromadb',
        'VECTOR_DB_PATH': './chroma_db',
        'VECTOR_DB_IMPL': 'duckdb+parquet'
    })
    
    # Remove PostgreSQL settings
    config.pop('POSTGRES_HOST', None)
    config.pop('POSTGRES_PORT', None)
    config.pop('POSTGRES_DB', None)
    config.pop('POSTGRES_USER', None)
    config.pop('POSTGRES_PASSWORD', None)
    config.pop('POSTGRES_CONNECTION_STRING', None)
    
    write_env_file(config)
    print("✅ Switched to SQLite configuration")

def show_current_config():
    """Show current configuration"""
    print("📋 Current Configuration")
    print("=" * 50)
    
    config = read_env_file()
    
    if not config:
        print("❌ No .env file found")
        return
    
    # AI Provider
    ai_provider = config.get('AI_PROVIDER', 'ollama')
    print(f"🤖 AI Provider: {ai_provider}")
    
    if ai_provider == 'openai':
        model = config.get('OPENAI_MODEL', 'gpt-3.5-turbo')
        api_key = config.get('OPENAI_API_KEY', 'Not set')
        print(f"   Model: {model}")
        print(f"   API Key: {'✅ Set' if api_key != 'Not set' else '❌ Not set'}")
    else:
        base_url = config.get('OLLAMA_BASE_URL', 'http://localhost:11434')
        model = config.get('OLLAMA_MODEL', 'llama2')
        print(f"   Base URL: {base_url}")
        print(f"   Model: {model}")
    
    # Database
    db_type = config.get('DATABASE_TYPE', 'sqlite')
    print(f"\n🗄️  Database: {db_type}")
    
    if db_type == 'postgresql':
        host = config.get('POSTGRES_HOST', 'localhost')
        port = config.get('POSTGRES_PORT', '5432')
        db = config.get('POSTGRES_DB', 'vanna_farsi')
        print(f"   Host: {host}:{port}")
        print(f"   Database: {db}")
    else:
        db_url = config.get('DATABASE_URL', 'sqlite:///sample_data.db')
        print(f"   URL: {db_url}")
    
    # Vector Database
    vector_db = config.get('VECTOR_DB_TYPE', 'chromadb')
    print(f"\n🔍 Vector Database: {vector_db}")
    
    if vector_db == 'chromadb':
        path = config.get('VECTOR_DB_PATH', './chroma_db')
        print(f"   Path: {path}")

def main():
    """Main function"""
    print("🔄 Vanna Farsi Configuration Switcher")
    print("=" * 50)
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python switch_config.py show          - Show current configuration")
        print("  python switch_config.py openai        - Switch to OpenAI")
        print("  python switch_config.py ollama        - Switch to Ollama")
        print("  python switch_config.py postgresql    - Switch to PostgreSQL")
        print("  python switch_config.py sqlite        - Switch to SQLite")
        print("  python switch_config.py openai-pg     - Switch to OpenAI + PostgreSQL")
        print("  python switch_config.py ollama-sqlite - Switch to Ollama + SQLite")
        return
    
    command = sys.argv[1].lower()
    
    if command == 'show':
        show_current_config()
    elif command == 'openai':
        switch_to_openai()
    elif command == 'ollama':
        switch_to_ollama()
    elif command == 'postgresql':
        switch_to_postgresql()
    elif command == 'sqlite':
        switch_to_sqlite()
    elif command == 'openai-pg':
        switch_to_openai()
        switch_to_postgresql()
    elif command == 'ollama-sqlite':
        switch_to_ollama()
        switch_to_sqlite()
    else:
        print(f"❌ Unknown command: {command}")
        print("Use 'show', 'openai', 'ollama', 'postgresql', 'sqlite', 'openai-pg', or 'ollama-sqlite'")

if __name__ == "__main__":
    main()