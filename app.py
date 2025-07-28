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

from vanna.ollama.ollama_chat import Ollama_Chat
from vanna.chromadb.chromadb_vector import ChromaDB_VectorStore

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FarsiVanna(ChromaDB_VectorStore, Ollama_Chat):
    def __init__(self, config=None):
        ChromaDB_VectorStore.__init__(self, config=config)
        Ollama_Chat.__init__(self, config=config)
        
        # Initialize with Farsi prompts
        self.farsi_prompts = {
            "system": """شما یک دستیار هوشمند برای تولید کوئری SQL هستید. 
            لطفاً سوالات فارسی را به SQL تبدیل کنید.
            همیشه از بهترین شیوه‌های SQL استفاده کنید و نتایج را به فارسی توضیح دهید.""",
            
            "question_to_sql": """سوال کاربر: {question}
            
            لطفاً این سوال را به کوئری SQL تبدیل کنید. 
            فقط کوئری SQL را برگردانید، بدون توضیح اضافی.""",
            
            "explain_results": """نتایج کوئری SQL:
            {sql}
            
            داده‌های نتیجه:
            {data}
            
            لطفاً این نتایج را به فارسی توضیح دهید."""
        }

app = Flask(__name__)
app.config['SECRET_KEY'] = 'vanna-farsi-secret-key'
sock = Sock(app)

# Initialize Vanna with local configuration
vn = FarsiVanna(config={
    'ollama_base_url': 'http://localhost:11434',
    'model': 'llama2',
    'chroma_db_impl': 'duckdb+parquet',
    'persist_directory': './chroma_db'
})

# Sample database setup
def setup_sample_database():
    """Create a sample SQLite database with Persian data"""
    conn = sqlite3.connect('sample_data.db')
    cursor = conn.cursor()
    
    # Create tables
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
        (1, 'علی احمدی', 'ali@example.com', 'تهران', '2023-01-15'),
        (2, 'فاطمه محمدی', 'fateme@example.com', 'اصفهان', '2023-02-20'),
        (3, 'محمد رضایی', 'mohammad@example.com', 'مشهد', '2023-03-10'),
        (4, 'زهرا کریمی', 'zahra@example.com', 'شیراز', '2023-04-05'),
        (5, 'حسن نوری', 'hasan@example.com', 'تبریز', '2023-05-12'),
    ]
    
    orders_data = [
        (1, 1, 'لپ‌تاپ', 1, 25000000, '2023-06-01'),
        (2, 2, 'موبایل', 2, 15000000, '2023-06-05'),
        (3, 3, 'تبلت', 1, 12000000, '2023-06-10'),
        (4, 4, 'لپ‌تاپ', 1, 28000000, '2023-06-15'),
        (5, 5, 'موبایل', 1, 16000000, '2023-06-20'),
        (6, 1, 'تبلت', 1, 11000000, '2023-07-01'),
        (7, 2, 'لپ‌تاپ', 1, 26000000, '2023-07-05'),
    ]
    
    employees_data = [
        (1, 'احمد رضایی', 'فروش', 45000000, '2022-01-01'),
        (2, 'مریم احمدی', 'مالی', 38000000, '2022-02-01'),
        (3, 'علی محمدی', 'فروش', 42000000, '2022-03-01'),
        (4, 'فاطمه کریمی', 'فناوری اطلاعات', 55000000, '2022-04-01'),
        (5, 'محمد نوری', 'فروش', 40000000, '2022-05-01'),
    ]
    
    cursor.executemany('INSERT OR REPLACE INTO customers VALUES (?, ?, ?, ?, ?)', customers_data)
    cursor.executemany('INSERT OR REPLACE INTO orders VALUES (?, ?, ?, ?, ?, ?)', orders_data)
    cursor.executemany('INSERT OR REPLACE INTO employees VALUES (?, ?, ?, ?, ?)', employees_data)
    
    conn.commit()
    conn.close()

# Train the model with sample data
def train_model():
    """Train the model with sample database schema and data"""
    try:
        # Train with DDL
        vn.train(ddl="""
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
        """)
        
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
            conn = sqlite3.connect('sample_data.db')
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
            conn = sqlite3.connect('sample_data.db')
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