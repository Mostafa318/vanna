#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Setup script for Vanna Farsi
This script helps users set up the application with proper configuration.
"""

import os
import sys
import subprocess
import platform
import json
from pathlib import Path

def print_banner():
    """Print application banner"""
    banner = """
╔══════════════════════════════════════════════════════════════╗
║                    وانا فارسی - نسخه محلی                    ║
║                دستیار هوشمند SQL به زبان فارسی                ║
╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ خطا: Python 3.8 یا بالاتر مورد نیاز است")
        print(f"نسخه فعلی: {sys.version}")
        return False
    print(f"✅ Python {sys.version.split()[0]} - OK")
    return True

def install_ollama():
    """Install Ollama based on the operating system"""
    system = platform.system().lower()
    
    print("\n🔧 نصب Ollama...")
    
    if system == "linux":
        print("در حال نصب Ollama برای Linux...")
        try:
            subprocess.run([
                "curl", "-fsSL", "https://ollama.ai/install.sh"
            ], shell=True, check=True)
            print("✅ Ollama نصب شد")
            return True
        except subprocess.CalledProcessError:
            print("❌ خطا در نصب Ollama")
            return False
    
    elif system == "darwin":  # macOS
        print("در حال نصب Ollama برای macOS...")
        try:
            subprocess.run(["brew", "install", "ollama"], check=True)
            print("✅ Ollama نصب شد")
            return True
        except subprocess.CalledProcessError:
            print("❌ خطا در نصب Ollama. لطفاً Homebrew را نصب کنید")
            return False
    
    elif system == "windows":
        print("❌ برای Windows، لطفاً Ollama را از https://ollama.ai دانلود کنید")
        return False
    
    else:
        print(f"❌ سیستم عامل {system} پشتیبانی نمی‌شود")
        return False

def install_python_dependencies():
    """Install Python dependencies"""
    print("\n📦 نصب وابستگی‌های Python...")
    
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
        print("✅ وابستگی‌های Python نصب شدند")
        return True
    except subprocess.CalledProcessError:
        print("❌ خطا در نصب وابستگی‌های Python")
        return False

def download_ollama_model():
    """Download Ollama model"""
    print("\n🤖 دانلود مدل Ollama...")
    
    try:
        # Start Ollama service
        subprocess.run(["ollama", "serve"], start_new_session=True)
        
        # Wait a moment for service to start
        import time
        time.sleep(3)
        
        # Download model
        subprocess.run(["ollama", "pull", "llama2"], check=True)
        print("✅ مدل llama2 دانلود شد")
        return True
    except subprocess.CalledProcessError:
        print("❌ خطا در دانلود مدل")
        return False

def create_env_file():
    """Create .env file with default configuration"""
    env_content = """# Vanna Farsi Configuration

# Flask settings
SECRET_KEY=vanna-farsi-secret-key-change-in-production
DEBUG=True
HOST=0.0.0.0
PORT=5000

# Database settings
DATABASE_TYPE=sqlite
DATABASE_URL=sqlite:///sample_data.db

# Ollama settings
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama2

# Vanna settings
VECTOR_DB_TYPE=chromadb
VECTOR_DB_PATH=./chroma_db

# Sample data
SAMPLE_DATA_ENABLED=True

# Logging
LOG_LEVEL=INFO
LOG_FILE=vanna_farsi.log
"""
    
    if not os.path.exists('.env'):
        with open('.env', 'w', encoding='utf-8') as f:
            f.write(env_content)
        print("✅ فایل .env ایجاد شد")
    else:
        print("ℹ️ فایل .env از قبل وجود دارد")

def create_directories():
    """Create necessary directories"""
    directories = ['chroma_db', 'logs', 'data']
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
    
    print("✅ دایرکتوری‌های مورد نیاز ایجاد شدند")

def run_tests():
    """Run basic tests"""
    print("\n🧪 اجرای تست‌های اولیه...")
    
    try:
        # Test Ollama connection
        import requests
        response = requests.get('http://localhost:11434/api/tags', timeout=5)
        if response.status_code == 200:
            print("✅ اتصال به Ollama موفق")
        else:
            print("❌ خطا در اتصال به Ollama")
            return False
    except Exception as e:
        print(f"❌ خطا در تست Ollama: {e}")
        return False
    
    return True

def print_next_steps():
    """Print next steps for the user"""
    next_steps = """
🎉 نصب و راه‌اندازی کامل شد!

📋 مراحل بعدی:

1. اطمینان حاصل کنید که Ollama در حال اجرا است:
   ollama serve

2. برنامه را اجرا کنید:
   python app.py

3. مرورگر را باز کنید و به آدرس زیر بروید:
   http://localhost:5000

4. سوالات خود را به فارسی بپرسید!

📚 راهنما:
- برای تغییر تنظیمات، فایل .env را ویرایش کنید
- برای استفاده از مدل‌های دیگر، فایل config.py را بررسی کنید
- برای پشتیبانی، issues در GitHub ارسال کنید

🔗 لینک‌های مفید:
- مستندات Ollama: https://ollama.ai/docs
- مدل‌های موجود: https://ollama.ai/library
    """
    print(next_steps)

def main():
    """Main setup function"""
    print_banner()
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Create directories
    create_directories()
    
    # Install Python dependencies
    if not install_python_dependencies():
        sys.exit(1)
    
    # Install Ollama
    if not install_ollama():
        print("⚠️ نصب Ollama ناموفق بود. لطفاً به صورت دستی نصب کنید")
    
    # Download model
    if not download_ollama_model():
        print("⚠️ دانلود مدل ناموفق بود. لطفاً به صورت دستی دانلود کنید")
    
    # Create environment file
    create_env_file()
    
    # Run tests
    if not run_tests():
        print("⚠️ برخی تست‌ها ناموفق بودند")
    
    # Print next steps
    print_next_steps()

if __name__ == "__main__":
    main()