# مستندات وانا فارسی

## فهرست مطالب

1. [معرفی](#معرفی)
2. [ویژگی‌ها](#ویژگی‌ها)
3. [نصب و راه‌اندازی](#نصب-و-راه‌اندازی)
4. [استفاده](#استفاده)
5. [پیکربندی](#پیکربندی)
6. [API](#api)
7. [مثال‌ها](#مثال‌ها)
8. [عیب‌یابی](#عیب‌یابی)
9. [مشارکت](#مشارکت)

## معرفی

وانا فارسی یک نسخه محلی از پروژه Vanna است که برای کاربران فارسی‌زبان طراحی شده است. این برنامه سوالات فارسی را به کوئری SQL تبدیل می‌کند و نتایج را در قالب جدول و نمودار نمایش می‌دهد.

### مزایای نسخه محلی

- **امنیت بالا**: تمام داده‌ها محلی پردازش می‌شوند
- **سرعت بالا**: بدون نیاز به اتصال اینترنت
- **هزینه کم**: بدون نیاز به API های پولی
- **کنترل کامل**: امکان تنظیم و شخصی‌سازی کامل

## ویژگی‌ها

### ✨ ویژگی‌های اصلی

- **پشتیبانی کامل از فارسی**: رابط کاربری و پردازش کاملاً به فارسی
- **اجرای محلی**: بدون نیاز به API خارجی
- **مدل‌های محلی**: استفاده از Ollama و مدل‌های محلی
- **رابط کاربری زیبا**: طراحی مدرن و کاربرپسند
- **پشتیبانی از پایگاه‌های داده مختلف**: SQLite، PostgreSQL، MySQL

### 🎯 قابلیت‌های فنی

- **تبدیل سوال به SQL**: تبدیل سوالات طبیعی فارسی به کوئری SQL
- **نمایش نتایج**: نمایش داده‌ها در قالب جدول
- **نمودار خودکار**: تولید نمودارهای تعاملی
- **پیشنهادات هوشمند**: پیشنهاد سوالات مفید
- **پشتیبانی از RTL**: رابط کاربری راست‌چین

## نصب و راه‌اندازی

### پیش‌نیازها

- Python 3.8 یا بالاتر
- حداقل 4GB RAM
- حداقل 10GB فضای دیسک

### روش 1: نصب خودکار

```bash
# کلون کردن مخزن
git clone <repository-url>
cd vanna-farsi-local

# اجرای اسکریپت نصب
python setup.py
```

### روش 2: نصب دستی

#### 1. نصب Ollama

**Linux:**
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

**macOS:**
```bash
brew install ollama
```

**Windows:**
از [سایت Ollama](https://ollama.ai) دانلود کنید.

#### 2. نصب وابستگی‌های Python

```bash
pip install -r requirements.txt
```

#### 3. دانلود مدل

```bash
ollama pull llama2
```

#### 4. اجرای برنامه

```bash
python app.py
```

### روش 3: استفاده از Docker

```bash
# ساخت و اجرای کانتینر
docker-compose up --build

# یا استفاده از Dockerfile
docker build -t vanna-farsi .
docker run -p 5000:5000 vanna-farsi
```

## استفاده

### شروع کار

1. برنامه را اجرا کنید: `python app.py`
2. مرورگر را باز کنید و به `http://localhost:5000` بروید
3. سوال خود را به فارسی بنویسید
4. نتایج را مشاهده کنید

### مثال‌های سوال

- "نمایش تمام مشتریان"
- "۱۰ مشتری برتر بر اساس تعداد سفارشات"
- "میانگین حقوق کارمندان در هر بخش"
- "فروش کل محصولات"
- "تعداد سفارشات در هر شهر"

### ویژگی‌های رابط کاربری

- **پیشنهادات**: کلیک روی پیشنهادات برای استفاده
- **چت تعاملی**: گفتگو با وانا
- **نمایش SQL**: مشاهده کوئری تولید شده
- **جدول نتایج**: نمایش داده‌ها
- **نمودار**: نمایش بصری نتایج

## پیکربندی

### فایل .env

```env
# Flask settings
SECRET_KEY=your-secret-key
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
```

### تغییر مدل

برای استفاده از مدل‌های دیگر:

```bash
# دانلود مدل جدید
ollama pull mistral

# تغییر در فایل .env
OLLAMA_MODEL=mistral
```

### اتصال به پایگاه‌های داده دیگر

#### PostgreSQL

```env
DATABASE_TYPE=postgresql
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=vanna_farsi
POSTGRES_USER=postgres
POSTGRES_PASSWORD=password
```

#### MySQL

```env
DATABASE_TYPE=mysql
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_DB=vanna_farsi
MYSQL_USER=root
MYSQL_PASSWORD=password
```

## API

### Endpoints

#### `GET /api/health`
بررسی وضعیت برنامه

**Response:**
```json
{
  "status": "healthy",
  "message": "سیستم در حال کار است"
}
```

#### `GET /api/suggestions`
دریافت پیشنهادات سوال

**Response:**
```json
{
  "suggestions": [
    "۱۰ مشتری برتر بر اساس تعداد سفارشات",
    "میانگین حقوق کارمندان در هر بخش",
    "فروش کل محصولات"
  ]
}
```

#### `POST /api/ask`
ارسال سوال و دریافت نتایج

**Request:**
```json
{
  "question": "نمایش تمام مشتریان"
}
```

**Response:**
```json
{
  "sql": "SELECT * FROM customers",
  "data": [
    {"id": 1, "name": "علی احمدی", "city": "تهران"},
    {"id": 2, "name": "فاطمه محمدی", "city": "اصفهان"}
  ],
  "columns": ["id", "name", "city"],
  "chart": "{\"data\": [...], \"layout\": {...}}",
  "question": "نمایش تمام مشتریان"
}
```

## مثال‌ها

### مثال 1: نمایش مشتریان

**سوال:** "نمایش تمام مشتریان"

**SQL تولید شده:**
```sql
SELECT * FROM customers
```

**نتیجه:** جدول تمام مشتریان

### مثال 2: تحلیل فروش

**سوال:** "محصولات پرفروش را نشان بده"

**SQL تولید شده:**
```sql
SELECT product_name, SUM(quantity) as total_quantity 
FROM orders 
GROUP BY product_name 
ORDER BY total_quantity DESC
```

**نتیجه:** نمودار ستونی محصولات بر اساس فروش

### مثال 3: تحلیل کارمندان

**سوال:** "میانگین حقوق در هر بخش"

**SQL تولید شده:**
```sql
SELECT department, AVG(salary) as avg_salary 
FROM employees 
GROUP BY department
```

**نتیجه:** نمودار دایره‌ای میانگین حقوق

## عیب‌یابی

### مشکلات رایج

#### 1. خطای اتصال به Ollama

**مشکل:** `Connection refused to Ollama`

**راه‌حل:**
```bash
# بررسی وضعیت Ollama
ollama list

# راه‌اندازی مجدد
ollama serve
```

#### 2. خطای مدل

**مشکل:** `Model not found`

**راه‌حل:**
```bash
# دانلود مجدد مدل
ollama pull llama2
```

#### 3. خطای پایگاه داده

**مشکل:** `Database connection failed`

**راه‌حل:**
```bash
# حذف و ایجاد مجدد پایگاه داده
rm sample_data.db
python app.py
```

#### 4. خطای پورت

**مشکل:** `Port 5000 already in use`

**راه‌حل:**
```bash
# تغییر پورت در فایل .env
PORT=5001
```

### لاگ‌ها

برای بررسی لاگ‌ها:

```bash
# لاگ‌های برنامه
tail -f vanna_farsi.log

# لاگ‌های Ollama
ollama logs
```

### تست عملکرد

```bash
# اجرای تست‌ها
python test_app.py

# تست با انتظار
python test_app.py --wait
```

## مشارکت

### نحوه مشارکت

1. Fork کردن پروژه
2. ایجاد branch جدید: `git checkout -b feature/new-feature`
3. اعمال تغییرات
4. Commit کردن: `git commit -am 'Add new feature'`
5. Push کردن: `git push origin feature/new-feature`
6. ایجاد Pull Request

### استانداردهای کد

- استفاده از Python 3.8+
- پیروی از PEP 8
- نوشتن docstring برای توابع
- تست‌نویسی برای قابلیت‌های جدید

### گزارش باگ

لطفاً برای گزارش باگ:

1. نسخه Python و سیستم عامل را مشخص کنید
2. خطای دقیق را کپی کنید
3. مراحل تولید خطا را توضیح دهید
4. لاگ‌های مربوطه را ضمیمه کنید

## لینک‌های مفید

- [مستندات Ollama](https://ollama.ai/docs)
- [مدل‌های موجود](https://ollama.ai/library)
- [مستندات Vanna](https://vanna.ai/docs)
- [GitHub Repository](https://github.com/your-repo/vanna-farsi)

## مجوز

این پروژه تحت مجوز MIT منتشر شده است.