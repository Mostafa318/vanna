#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Setup script for Vanna Farsi
This script helps users set up the application with proper configuration.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        sys.exit(1)
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")

def install_dependencies():
    """Install required dependencies"""
    print("📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully")
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        sys.exit(1)

def setup_environment():
    """Setup environment configuration"""
    print("🔧 Setting up environment...")
    
    env_file = Path(".env")
    if env_file.exists():
        print("⚠️  .env file already exists. Skipping environment setup.")
        return
    
    # Copy example environment file
    example_env = Path(".env.example")
    if example_env.exists():
        shutil.copy(example_env, env_file)
        print("✅ Environment file created from .env.example")
        print("📝 Please edit .env file with your configuration")
    else:
        print("❌ .env.example file not found")

def setup_database():
    """Setup database configuration"""
    print("🗄️  Database setup options:")
    print("1. SQLite (default, no setup required)")
    print("2. PostgreSQL (requires Docker or local PostgreSQL)")
    
    choice = input("Choose database type (1/2): ").strip()
    
    if choice == "2":
        print("🐘 PostgreSQL setup:")
        print("1. Use Docker Compose (recommended)")
        print("2. Use local PostgreSQL installation")
        
        db_choice = input("Choose setup method (1/2): ").strip()
        
        if db_choice == "1":
            setup_postgresql_docker()
        else:
            print("📝 Please configure PostgreSQL connection in .env file")

def setup_postgresql_docker():
    """Setup PostgreSQL using Docker"""
    print("🐳 Setting up PostgreSQL with Docker...")
    
    # Check if Docker is available
    try:
        subprocess.run(["docker", "--version"], check=True, capture_output=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Docker is not installed or not available")
        print("📝 Please install Docker or configure PostgreSQL manually")
        return
    
    # Start PostgreSQL container
    try:
        subprocess.run(["docker-compose", "-f", "docker-compose.postgresql.yml", "up", "-d"], check=True)
        print("✅ PostgreSQL container started")
        print("📊 pgAdmin available at http://localhost:5050")
        print("   Email: admin@vanna.com")
        print("   Password: admin123")
    except subprocess.CalledProcessError:
        print("❌ Failed to start PostgreSQL container")

def setup_ai_provider():
    """Setup AI provider configuration"""
    print("🤖 AI Provider setup options:")
    print("1. Ollama (local, requires Ollama installation)")
    print("2. OpenAI (cloud, requires API key)")
    
    choice = input("Choose AI provider (1/2): ").strip()
    
    if choice == "2":
        print("🔑 OpenAI setup:")
        api_key = input("Enter your OpenAI API key: ").strip()
        
        if api_key:
            # Update .env file
            update_env_file("AI_PROVIDER", "openai")
            update_env_file("OPENAI_API_KEY", api_key)
            print("✅ OpenAI configuration updated")
        else:
            print("⚠️  No API key provided. Please update .env file manually")

def update_env_file(key, value):
    """Update a key in .env file"""
    env_file = Path(".env")
    if not env_file.exists():
        return
    
    lines = env_file.read_text().splitlines()
    updated = False
    
    for i, line in enumerate(lines):
        if line.startswith(f"{key}="):
            lines[i] = f"{key}={value}"
            updated = True
            break
    
    if not updated:
        lines.append(f"{key}={value}")
    
    env_file.write_text("\n".join(lines))

def main():
    """Main setup function"""
    print("🚀 Vanna Farsi Setup")
    print("=" * 50)
    
    # Check Python version
    check_python_version()
    
    # Install dependencies
    install_dependencies()
    
    # Setup environment
    setup_environment()
    
    # Setup database
    setup_database()
    
    # Setup AI provider
    setup_ai_provider()
    
    print("\n🎉 Setup completed!")
    print("\n📋 Next steps:")
    print("1. Edit .env file with your configuration")
    print("2. Run: python app.py")
    print("3. Open http://localhost:5000 in your browser")
    
    print("\n📚 Documentation:")
    print("- README.md: General information")
    print("- QUICK_START.md: Quick start guide")
    print("- .env.example: Configuration options")

if __name__ == "__main__":
    main()