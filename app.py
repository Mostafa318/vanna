#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import json
import logging
from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_sock import Sock
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.utils import PlotlyJSONEncoder
import sqlite3
from datetime import datetime
import uuid

# Add the parent directory to the path to import vanna modules
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

# Import the new FarsiVanna class
from vanna.farsi_vanna import FarsiVanna

# Import configuration
from config import get_config

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get configuration
config = get_config()

app = Flask(__name__)
app.config['SECRET_KEY'] = config.SECRET_KEY
sock = Sock(app)

# Initialize Vanna with configuration
vanna_config = config.get_vanna_config()
vanna_config.update({
    'ai_provider': config.AI_PROVIDER,
    'vector_db_type': config.VECTOR_DB_TYPE,
})

vn = FarsiVanna(config=vanna_config)

# Database connection function
def get_database_connection():
    """Get database connection based on configuration"""
    if config.DATABASE_TYPE == 'postgresql':
        import psycopg2
        db_config = config.get_database_config()
        if 'connection_string' in db_config:
            # Parse connection string
            conn_str = db_config['connection_string']
            return psycopg2.connect(conn_str)
        else:
            return psycopg2.connect(
                host=db_config['host'],
                port=db_config['port'],
                database=db_config['database'],
                user=db_config['user'],
                password=db_config['password']
            )
    else:
        # SQLite
        return sqlite3.connect('sample_data.db')

# Sample database setup
def setup_sample_database():
    """Create a sample database with Persian data"""
    conn = get_database_connection()
    cursor = conn.cursor()
    
    if config.DATABASE_TYPE == 'postgresql':
        # PostgreSQL setup
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS customers (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255),
                city VARCHAR(100),
                registration_date DATE
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                id SERIAL PRIMARY KEY,
                customer_id INTEGER,
                product_name VARCHAR(255),
                quantity INTEGER,
                price DECIMAL(10,2),
                order_date DATE,
                FOREIGN KEY (customer_id) REFERENCES customers (id)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS employees (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                department VARCHAR(100),
                salary DECIMAL(10,2),
                hire_date DATE
            )
        ''')
    else:
        # SQLite setup
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT,
                city TEXT,
                registration_date DATE
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY,
                customer_id INTEGER,
                product_name TEXT,
                quantity INTEGER,
                price REAL,
                order_date DATE,
                FOREIGN KEY (customer_id) REFERENCES customers (id)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS employees (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                department TEXT,
                salary REAL,
                hire_date DATE
            )
        ''')
    
    # Insert sample data
    customers_data = [
        ('علی احمدی', 'ali@example.com', 'تهران', '2023-01-15'),
        ('فاطمه محمدی', 'fateme@example.com', 'اصفهان', '2023-02-20'),
        ('محمد رضایی', 'mohammad@example.com', 'مشهد', '2023-03-10'),
        ('زهرا کریمی', 'zahra@example.com', 'شیراز', '2023-04-05'),
        ('حسن نوری', 'hasan@example.com', 'تبریز', '2023-05-12'),
    ]
    
    orders_data = [
        (1, 'لپ‌تاپ', 1, 25000000, '2023-06-01'),
        (2, 'موبایل', 2, 15000000, '2023-06-05'),
        (3, 'تبلت', 1, 12000000, '2023-06-10'),
        (4, 'لپ‌تاپ', 1, 28000000, '2023-06-15'),
        (5, 'موبایل', 1, 16000000, '2023-06-20'),
        (1, 'تبلت', 1, 11000000, '2023-07-01'),
        (2, 'لپ‌تاپ', 1, 26000000, '2023-07-05'),
    ]
    
    employees_data = [
        ('احمد رضایی', 'فروش', 45000000, '2022-01-01'),
        ('مریم احمدی', 'مالی', 38000000, '2022-02-01'),
        ('علی محمدی', 'فروش', 42000000, '2022-03-01'),
        ('فاطمه کریمی', 'فناوری اطلاعات', 55000000, '2022-04-01'),
        ('محمد نوری', 'فروش', 40000000, '2022-05-01'),
    ]
    
    # Clear existing data and insert new data
    cursor.execute('DELETE FROM orders')
    cursor.execute('DELETE FROM customers')
    cursor.execute('DELETE FROM employees')
    
    cursor.executemany('INSERT INTO customers (name, email, city, registration_date) VALUES (%s, %s, %s, %s)', customers_data)
    cursor.executemany('INSERT INTO orders (customer_id, product_name, quantity, price, order_date) VALUES (%s, %s, %s, %s, %s)', orders_data)
    cursor.executemany('INSERT INTO employees (name, department, salary, hire_date) VALUES (%s, %s, %s, %s)', employees_data)
    
    conn.commit()
    conn.close()

# Train the model with sample data
def train_model():
    """Train the model with sample database schema and data"""
    try:
        # Train with DDL
        if config.DATABASE_TYPE == 'postgresql':
            ddl = """
                CREATE TABLE customers (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    email VARCHAR(255),
                    city VARCHAR(100),
                    registration_date DATE
                );
                
                CREATE TABLE orders (
                    id SERIAL PRIMARY KEY,
                    customer_id INTEGER,
                    product_name VARCHAR(255),
                    quantity INTEGER,
                    price DECIMAL(10,2),
                    order_date DATE,
                    FOREIGN KEY (customer_id) REFERENCES customers (id)
                );
                
                CREATE TABLE employees (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    department VARCHAR(100),
                    salary DECIMAL(10,2),
                    hire_date DATE
                );
            """
        else:
            ddl = """
                CREATE TABLE customers (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    email TEXT,
                    city TEXT,
                    registration_date DATE
                );
                
                CREATE TABLE orders (
                    id INTEGER PRIMARY KEY,
                    customer_id INTEGER,
                    product_name TEXT,
                    quantity INTEGER,
                    price REAL,
                    order_date DATE,
                    FOREIGN KEY (customer_id) REFERENCES customers (id)
                );
                
                CREATE TABLE employees (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    department TEXT,
                    salary REAL,
                    hire_date DATE
                );
            """
        
        vn.train(ddl=ddl)
        
        # Train with sample queries
        sample_queries = [
            "SELECT name, city FROM customers",
            "SELECT product_name, SUM(quantity) as total_quantity FROM orders GROUP BY product_name",
            "SELECT department, AVG(salary) as avg_salary FROM employees GROUP BY department",
            "SELECT c.name, COUNT(o.id) as order_count FROM customers c LEFT JOIN orders o ON c.id = o.customer_id GROUP BY c.id, c.name"
        ]
        
        for query in sample_queries:
            vn.train(sql=query)
            
        logger.info("Model training completed successfully")
        
    except Exception as e:
        logger.error(f"Error training model: {e}")

@app.route('/')
def index():
    """Main page with Farsi interface"""
    return render_template('index.html')

@app.route('/api/ask', methods=['POST'])
def ask_question():
    """Handle Farsi questions and return SQL + results"""
    try:
        data = request.get_json()
        question = data.get('question', '')
        
        if not question:
            return jsonify({'error': 'سوال خالی است'}), 400
        
        # Generate SQL from question
        sql = vn.generate_sql(question)
        
        if not sql:
            return jsonify({'error': 'نمی‌توانم SQL تولید کنم'}), 400
        
        # Execute SQL
        try:
            conn = get_database_connection()
            df = pd.read_sql_query(sql, conn)
            conn.close()
            
            # Generate chart if data is suitable
            chart_data = None
            if len(df) > 0 and len(df.columns) >= 2:
                try:
                    if len(df) <= 10:  # Bar chart for small datasets
                        fig = px.bar(df, x=df.columns[0], y=df.columns[1], 
                                   title=f"نمودار: {question}")
                    else:  # Line chart for larger datasets
                        fig = px.line(df, x=df.columns[0], y=df.columns[1], 
                                    title=f"نمودار: {question}")
                    
                    chart_data = json.dumps(fig, cls=PlotlyJSONEncoder)
                except Exception as e:
                    logger.warning(f"Could not generate chart: {e}")
            
            return jsonify({
                'sql': sql,
                'data': df.to_dict('records'),
                'columns': df.columns.tolist(),
                'chart': chart_data,
                'question': question
            })
            
        except Exception as e:
            return jsonify({'error': f'خطا در اجرای کوئری: {str(e)}'}), 500
            
    except Exception as e:
        logger.error(f"Error processing question: {e}")
        return jsonify({'error': 'خطای داخلی سرور'}), 500

@app.route('/api/suggestions', methods=['GET'])
def get_suggestions():
    """Get suggested Farsi questions"""
    suggestions = [
        "۱۰ مشتری برتر بر اساس تعداد سفارشات",
        "میانگین حقوق کارمندان در هر بخش",
        "فروش کل محصولات",
        "تعداد سفارشات در هر شهر",
        "محصولات پرفروش",
        "کارمندان با بالاترین حقوق",
        "تعداد مشتریان جدید در هر ماه"
    ]
    return jsonify({'suggestions': suggestions})

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'message': 'سیستم در حال کار است'})

@sock.route('/ws')
def websocket(ws):
    """WebSocket for real-time communication"""
    while True:
        try:
            data = ws.receive()
            if data:
                message = json.loads(data)
                if message.get('type') == 'question':
                    # Process question and send response
                    response = process_question(message.get('question', ''))
                    ws.send(json.dumps(response))
        except Exception as e:
            logger.error(f"WebSocket error: {e}")
            break

def process_question(question):
    """Process a question and return response"""
    try:
        sql = vn.generate_sql(question)
        if sql:
            conn = get_database_connection()
            df = pd.read_sql_query(sql, conn)
            conn.close()
            
            return {
                'type': 'response',
                'sql': sql,
                'data': df.to_dict('records'),
                'question': question
            }
        else:
            return {
                'type': 'error',
                'message': 'نمی‌توانم SQL تولید کنم'
            }
    except Exception as e:
        return {
            'type': 'error',
            'message': f'خطا: {str(e)}'
        }

if __name__ == '__main__':
    # Setup database and train model
    print("در حال راه‌اندازی پایگاه داده نمونه...")
    setup_sample_database()
    
    print("در حال آموزش مدل...")
    train_model()
    
    print("شروع سرور...")
    app.run(debug=True, host='0.0.0.0', port=5000)