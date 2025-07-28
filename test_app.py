#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test script for Vanna Farsi application
This script tests the basic functionality of the application.
"""

import requests
import json
import time
import sys
import os

def test_ollama_connection():
    """Test connection to Ollama"""
    print("🔍 تست اتصال به Ollama...")
    try:
        response = requests.get('http://localhost:11434/api/tags', timeout=5)
        if response.status_code == 200:
            print("✅ اتصال به Ollama موفق")
            return True
        else:
            print("❌ خطا در اتصال به Ollama")
            return False
    except Exception as e:
        print(f"❌ خطا در اتصال به Ollama: {e}")
        return False

def test_flask_app():
    """Test Flask application"""
    print("🔍 تست برنامه Flask...")
    try:
        response = requests.get('http://localhost:5000/api/health', timeout=5)
        if response.status_code == 200:
            print("✅ برنامه Flask در حال اجرا است")
            return True
        else:
            print("❌ برنامه Flask پاسخ نمی‌دهد")
            return False
    except Exception as e:
        print(f"❌ خطا در اتصال به Flask: {e}")
        return False

def test_api_endpoints():
    """Test API endpoints"""
    print("🔍 تست API endpoints...")
    
    # Test suggestions endpoint
    try:
        response = requests.get('http://localhost:5000/api/suggestions', timeout=5)
        if response.status_code == 200:
            data = response.json()
            if 'suggestions' in data and len(data['suggestions']) > 0:
                print("✅ API suggestions کار می‌کند")
            else:
                print("❌ API suggestions داده‌ای برنمی‌گرداند")
                return False
        else:
            print("❌ API suggestions خطا می‌دهد")
            return False
    except Exception as e:
        print(f"❌ خطا در تست API suggestions: {e}")
        return False
    
    # Test ask endpoint
    try:
        test_question = "نمایش تمام مشتریان"
        response = requests.post('http://localhost:5000/api/ask', 
                               json={'question': test_question}, 
                               timeout=30)
        if response.status_code == 200:
            data = response.json()
            if 'sql' in data and 'data' in data:
                print("✅ API ask کار می‌کند")
                print(f"   SQL تولید شده: {data['sql'][:100]}...")
                print(f"   تعداد رکوردها: {len(data['data'])}")
            else:
                print("❌ API ask داده‌ای برنمی‌گرداند")
                return False
        else:
            print(f"❌ API ask خطا می‌دهد: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ خطا در تست API ask: {e}")
        return False
    
    return True

def test_database():
    """Test database connection and sample data"""
    print("🔍 تست پایگاه داده...")
    try:
        import sqlite3
        conn = sqlite3.connect('sample_data.db')
        cursor = conn.cursor()
        
        # Check if tables exist
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        
        if len(tables) >= 3:  # customers, orders, employees
            print("✅ جداول پایگاه داده وجود دارند")
        else:
            print("❌ جداول پایگاه داده وجود ندارند")
            return False
        
        # Check sample data
        cursor.execute("SELECT COUNT(*) FROM customers")
        customer_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM orders")
        order_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM employees")
        employee_count = cursor.fetchone()[0]
        
        print(f"   تعداد مشتریان: {customer_count}")
        print(f"   تعداد سفارشات: {order_count}")
        print(f"   تعداد کارمندان: {employee_count}")
        
        if customer_count > 0 and order_count > 0 and employee_count > 0:
            print("✅ داده‌های نمونه موجود هستند")
        else:
            print("❌ داده‌های نمونه موجود نیستند")
            return False
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ خطا در تست پایگاه داده: {e}")
        return False

def run_all_tests():
    """Run all tests"""
    print("🧪 شروع تست‌های Vanna Farsi")
    print("=" * 50)
    
    tests = [
        ("Ollama Connection", test_ollama_connection),
        ("Flask Application", test_flask_app),
        ("Database", test_database),
        ("API Endpoints", test_api_endpoints),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📋 تست: {test_name}")
        print("-" * 30)
        
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name} موفق")
            else:
                print(f"❌ {test_name} ناموفق")
        except Exception as e:
            print(f"❌ خطا در {test_name}: {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 نتایج: {passed}/{total} تست موفق")
    
    if passed == total:
        print("🎉 تمام تست‌ها موفق بودند!")
        return True
    else:
        print("⚠️ برخی تست‌ها ناموفق بودند")
        return False

def main():
    """Main function"""
    if len(sys.argv) > 1 and sys.argv[1] == '--wait':
        print("⏳ منتظر شروع برنامه...")
        time.sleep(10)
    
    success = run_all_tests()
    
    if success:
        print("\n🎯 برنامه آماده استفاده است!")
        print("🌐 مرورگر را باز کنید و به http://localhost:5000 بروید")
    else:
        print("\n🔧 لطفاً مشکلات را برطرف کنید و دوباره تست کنید")
        sys.exit(1)

if __name__ == "__main__":
    main()