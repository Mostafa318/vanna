# Vanna Farsi - دستیار هوشمند SQL

یک دستیار هوشمند برای تبدیل سوالات فارسی به کوئری SQL با پشتیبانی از OpenAI API و PostgreSQL.

## ✨ ویژگی‌ها

- 🤖 **پشتیبانی از چندین AI Provider**: OpenAI API و Ollama
- 🗄️ **پشتیبانی از چندین دیتابیس**: SQLite، PostgreSQL
- 🔍 **جستجوی برداری**: ChromaDB و PostgreSQL pgvector
- 📊 **نمودارهای تعاملی**: با استفاده از Plotly
- 🌐 **رابط کاربری وب**: Flask با WebSocket
- 📱 **پاسخ‌های فوری**: با استفاده از WebSocket

## 🚀 نصب و راه‌اندازی سریع

### 1. کلون کردن مخزن

```bash
git clone <repository-url>
cd vanna-farsi
```

### 2. اجرای اسکریپت نصب

```bash
python setup.py
```

### 3. تنظیم متغیرهای محیطی

فایل `.env` را ویرایش کنید:

```bash
cp .env.example .env
# فایل .env را ویرایش کنید
```

### 4. اجرای برنامه

```bash
python app.py
```

### 5. باز کردن مرورگر

```
http://localhost:5000
```

## ⚙️ پیکربندی

### AI Provider

#### OpenAI API

```env
AI_PROVIDER=openai
OPENAI_API_KEY=your-api-key-here
OPENAI_MODEL=gpt-3.5-turbo
OPENAI_TEMPERATURE=0.7
```

#### Ollama (محلی)

```env
AI_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama2
```

### دیتابیس

#### SQLite (پیش‌فرض)

```env
DATABASE_TYPE=sqlite
```

#### PostgreSQL

```env
DATABASE_TYPE=postgresql
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=vanna_farsi
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_password
```

یا استفاده از connection string:

```env
POSTGRES_CONNECTION_STRING=postgresql://user:password@host:port/database
```

### Vector Database

#### ChromaDB (پیش‌فرض)

```env
VECTOR_DB_TYPE=chromadb
VECTOR_DB_PATH=./chroma_db
VECTOR_DB_IMPL=duckdb+parquet
```

#### PostgreSQL pgvector

```env
VECTOR_DB_TYPE=pgvector
```

## 🐳 استفاده با Docker

### PostgreSQL با Docker Compose

```bash
# راه‌اندازی PostgreSQL
docker-compose -f docker-compose.postgresql.yml up -d

# تنظیم متغیرهای محیطی برای PostgreSQL
export DATABASE_TYPE=postgresql
export VECTOR_DB_TYPE=pgvector
```

### اجرای برنامه با Docker

```bash
# ساخت image
docker build -t vanna-farsi .

# اجرای container
docker run -p 5000:5000 --env-file .env vanna-farsi
```

## 📊 نمونه سوالات

- "۱۰ مشتری برتر بر اساس تعداد سفارشات"
- "میانگین حقوق کارمندان در هر بخش"
- "فروش کل محصولات"
- "تعداد سفارشات در هر شهر"
- "محصولات پرفروش"

## 🔧 API Endpoints

### سوال پرسیدن

```http
POST /api/ask
Content-Type: application/json

{
    "question": "۱۰ مشتری برتر بر اساس تعداد سفارشات"
}
```

### دریافت پیشنهادات

```http
GET /api/suggestions
```

### بررسی سلامت سیستم

```http
GET /api/health
```

## 🏗️ معماری

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Flask App     │    │   AI Provider   │
│   (HTML/JS)     │◄──►│   (Python)      │◄──►│   (OpenAI/      │
│                 │    │                 │    │    Ollama)      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌─────────────────┐
                       │   Database      │
                       │   (SQLite/      │
                       │    PostgreSQL)  │
                       └─────────────────┘
                              │
                              ▼
                       ┌─────────────────┐
                       │ Vector Store    │
                       │ (ChromaDB/      │
                       │  pgvector)      │
                       └─────────────────┘
```

## 🧪 تست

```bash
# اجرای تست‌ها
python -m pytest tests/

# تست با coverage
python -m pytest --cov=src tests/
```

## 📝 لاگ‌ها

لاگ‌ها در فایل `vanna_farsi.log` ذخیره می‌شوند:

```bash
tail -f vanna_farsi.log
```

## 🔒 امنیت

- تغییر `SECRET_KEY` در محیط production
- استفاده از HTTPS در محیط production
- محدود کردن دسترسی به API endpoints
- رمزگذاری اطلاعات حساس

## 🤝 مشارکت

1. Fork کنید
2. Branch جدید ایجاد کنید (`git checkout -b feature/amazing-feature`)
3. Commit کنید (`git commit -m 'Add amazing feature'`)
4. Push کنید (`git push origin feature/amazing-feature`)
5. Pull Request ایجاد کنید

## 📄 لایسنس

این پروژه تحت لایسنس MIT منتشر شده است. برای جزئیات بیشتر فایل `LICENSE` را مطالعه کنید.

## 🆘 پشتیبانی

- 📧 ایمیل: [your-email@example.com]
- 🐛 Issues: [GitHub Issues](https://github.com/your-repo/issues)
- 📖 مستندات: [Wiki](https://github.com/your-repo/wiki)

## 🙏 تشکر

- [Vanna](https://github.com/vanna-ai/vanna) برای فریم‌ورک اصلی
- [OpenAI](https://openai.com/) برای API
- [Ollama](https://ollama.ai/) برای مدل‌های محلی
- [PostgreSQL](https://www.postgresql.org/) برای دیتابیس
- [Flask](https://flask.palletsprojects.com/) برای وب فریم‌ورک
