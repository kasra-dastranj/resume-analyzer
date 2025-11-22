# 📄 Resume Analyzer - AI-Powered CV Analysis

یک ابزار هوشمند برای تحلیل و ارزیابی رزومه‌ها با استفاده از هوش مصنوعی Groq

![Python](https://img.shields.io/badge/python-3.9+-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-1.46+-red.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

---

## ✨ ویژگی‌ها

- 🤖 **تحلیل هوشمند**: استفاده از Groq AI برای تحلیل دقیق رزومه‌ها
- 📊 **گزارش جامع**: تولید گزارش‌های ساختاریافته و بهینه
- 📁 **پشتیبانی از فرمت‌های مختلف**: PDF, DOCX, تصاویر
- 🚀 **رابط کاربری ساده**: با Streamlit
- ⚡ **پردازش بهینه**: مدیریت هوشمند فایل‌های بزرگ
- 🔄 **پردازش دسته‌ای**: تحلیل چندین رزومه به صورت همزمان

---

## 🚀 نصب و راه‌اندازی

### پیش‌نیازها

- Python 3.9 یا بالاتر
- API Key از [Groq](https://groq.com)

### مراحل نصب

```bash
# 1. کلون کردن پروژه
git clone https://github.com/kasra-dastranj/resume-analyzer.git
cd resume-analyzer

# 2. ساخت محیط مجازی
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows

# 3. نصب وابستگی‌ها
pip install -r requirements.txt

# 4. اجرا
streamlit run streamlit_app.py
```

---

## 🎮 نحوه استفاده

### 1️⃣ دریافت API Key

1. برو به [Groq Console](https://console.groq.com)
2. ثبت‌نام کن یا لاگین کن
3. API Key بساز
4. کپی کن

### 2️⃣ اجرای برنامه

```bash
streamlit run streamlit_app.py
```

### 3️⃣ آپلود رزومه

1. API Key خودت رو وارد کن
2. فایل‌های رزومه رو آپلود کن (PDF, DOCX, یا تصویر)
3. روی "Analyze" کلیک کن
4. منتظر تحلیل بمون
5. گزارش‌ها رو دانلود کن

---

## 📁 ساختار پروژه

```
resume-analyzer/
├── streamlit_app.py              # فایل اصلی Streamlit
├── cv_parser.py                  # پارسر رزومه‌ها
├── optimized_report_generator.py # تولید گزارش بهینه
├── requirements.txt              # وابستگی‌های Python
├── README.md                     # این فایل
└── .gitignore                    # فایل‌های نادیده گرفته شده
```

---

## 🔧 تنظیمات

### فرمت‌های پشتیبانی شده

- **PDF**: فایل‌های PDF استاندارد
- **DOCX**: اسناد Word
- **تصاویر**: PNG, JPG, JPEG (با OCR)

### محدودیت‌ها

- حداکثر حجم فایل: 10MB
- فرمت‌های پشتیبانی شده: PDF, DOCX, PNG, JPG

---

## 🤝 مشارکت

از مشارکت شما استقبال می‌کنیم!

1. Fork کنید
2. Branch جدید بسازید (`git checkout -b feature/amazing-feature`)
3. تغییرات رو Commit کنید (`git commit -m 'feat: add amazing feature'`)
4. Push کنید (`git push origin feature/amazing-feature`)
5. Pull Request بسازید

📖 [راهنمای مشارکت](CONTRIBUTING.md)

---

## 📊 نمونه خروجی

برنامه این اطلاعات رو از رزومه استخراج می‌کنه:

- ✅ اطلاعات شخصی
- ✅ تحصیلات
- ✅ تجربیات کاری
- ✅ مهارت‌ها
- ✅ پروژه‌ها
- ✅ زبان‌ها
- ✅ گواهینامه‌ها

---

## 🐛 مشکلات رایج

### خطای API Key
```
❌ Error initializing API clients
```
**راه‌حل**: مطمئن شو API Key درست وارد شده

### خطای OCR
```
❌ Tesseract not found
```
**راه‌حل**: 
```bash
# Windows
# دانلود از: https://github.com/UB-Mannheim/tesseract/wiki

# Linux
sudo apt install tesseract-ocr

# Mac
brew install tesseract
```

---

## 📄 مجوز

این پروژه تحت مجوز MIT منتشر شده. [LICENSE](LICENSE)

---

## 🙏 تشکر

- [Groq](https://groq.com) - AI API
- [Streamlit](https://streamlit.io) - Web Framework
- [PDFPlumber](https://github.com/jsvine/pdfplumber) - PDF Parser
- [python-docx](https://python-docx.readthedocs.io) - DOCX Parser

---

## 📞 ارتباط

- **GitHub**: [@kasra-dastranj](https://github.com/kasra-dastranj)
- **Email**: kasra.dastranj80@gmail.com
- **Hugging Face**: [Resume Analyzer Space](https://huggingface.co/spaces/Kasradastranj/resume-analyzer-space)

---

## 🌟 Demo

🚀 **Live Demo**: [Hugging Face Space](https://huggingface.co/spaces/Kasradastranj/resume-analyzer-space)

---

<div align="center">

**ساخته شده با ❤️ توسط Kasra Dastranj**

⭐ اگه این پروژه بهت کمک کرد، یه ستاره بهش بده!

</div>
