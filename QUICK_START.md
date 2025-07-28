# Quick Start Guide - راهنمای شروع سریع

## 🚀 شروع سریع

### گزینه 1: استفاده از SQLite + Ollama (پیش‌فرض)

```bash
# 1. کلون کردن مخزن
git clone <repository-url>
cd vanna-farsi

# 2. نصب وابستگی‌ها
pip install -r requirements.txt

# 3. نصب Ollama (اگر نصب نیست)
curl -fsSL https://ollama.ai/install.sh | sh

# 4. دانلود مدل
ollama pull llama2

# 5. اجرای برنامه
python app.py
```

### گزینه 2: استفاده از OpenAI API + SQLite

```bash
# 1. کلون کردن مخزن
git clone <repository-url>
cd vanna-farsi

# 2. نصب وابستگی‌ها
pip install -r requirements.txt

# 3. تنظیم متغیرهای محیطی
cp .env.example .env

# 4. ویرایش فایل .env
# AI_PROVIDER=openai
# OPENAI_API_KEY=your-api-key-here

# 5. اجرای برنامه
python app.py
```

### گزینه 3: استفاده از PostgreSQL + OpenAI

```bash
# 1. راه‌اندازی PostgreSQL با Docker
docker-compose -f docker-compose.postgresql.yml up -d

# 2. تنظیم متغیرهای محیطی
cp .env.example .env

# 3. ویرایش فایل .env
# DATABASE_TYPE=postgresql
# AI_PROVIDER=openai
# OPENAI_API_KEY=your-api-key-here
# VECTOR_DB_TYPE=pgvector

# 4. اجرای برنامه
python app.py
```

## ⚙️ تنظیمات پیشرفته

### تنظیم OpenAI

```env
AI_PROVIDER=openai
OPENAI_API_KEY=sk-your-api-key-here
OPENAI_MODEL=gpt-4
OPENAI_TEMPERATURE=0.7
```

### تنظیم PostgreSQL

```env
DATABASE_TYPE=postgresql
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=vanna_farsi
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_password
VECTOR_DB_TYPE=pgvector
```

### تنظیم Ollama

```env
AI_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama2
```

## 🔧 عیب‌یابی

### مشکل: اتصال به Ollama

```bash
# بررسی وضعیت Ollama
ollama list

# راه‌اندازی مجدد Ollama
ollama serve

# دانلود مجدد مدل
ollama pull llama2
```

### مشکل: اتصال به PostgreSQL

```bash
# بررسی وضعیت container
docker ps

# بررسی لاگ‌ها
docker logs vanna_postgres

# راه‌اندازی مجدد
docker-compose -f docker-compose.postgresql.yml restart
```

### مشکل: OpenAI API

```bash
# بررسی API key
echo $OPENAI_API_KEY

# تست اتصال
curl -H "Authorization: Bearer $OPENAI_API_KEY" \
     https://api.openai.com/v1/models
```

## 📊 تست عملکرد

### تست سوالات ساده

1. "تعداد کل مشتریان"
2. "میانگین قیمت سفارشات"
3. "کارمندان بخش فروش"

### تست سوالات پیچیده

1. "۱۰ مشتری برتر بر اساس تعداد سفارشات"
2. "فروش ماهانه سال گذشته"
3. "محصولات پرفروش در هر شهر"

## 🐳 Docker

### ساخت Image

```bash
docker build -t vanna-farsi .
```

### اجرای Container

```bash
# با SQLite
docker run -p 5000:5000 vanna-farsi

# با PostgreSQL
docker run -p 5000:5000 --env-file .env \
  --network host vanna-farsi
```

### Docker Compose کامل

```bash
# راه‌اندازی کامل
docker-compose up -d

# مشاهده لاگ‌ها
docker-compose logs -f

# توقف
docker-compose down
```

## 📝 لاگ‌ها

### مشاهده لاگ‌های برنامه

```bash
tail -f vanna_farsi.log
```

### تنظیم سطح لاگ

```env
LOG_LEVEL=DEBUG  # INFO, WARNING, ERROR, DEBUG
```

## 🔒 امنیت

### تغییر Secret Key

```env
SECRET_KEY=your-very-secure-secret-key
```

### محدود کردن دسترسی

```bash
# فقط localhost
HOST=127.0.0.1

# پورت سفارشی
PORT=8080
```

## 📚 منابع بیشتر

- [مستندات کامل](README.md)
- [پیکربندی پیشرفته](config.py)
- [API Endpoints](app.py)
- [مثال‌های استفاده](templates/index.html)