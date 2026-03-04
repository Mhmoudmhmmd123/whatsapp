# 📦 دليل التثبيت الكامل

## المتطلبات الأساسية

### 1. Python 3.8 أو أحدث

**التحقق من التثبيت:**
```bash
python3 --version
```

**التثبيت:**

**Windows:**
- حمّل من: https://www.python.org/downloads/
- تأكد من تفعيل "Add Python to PATH"

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install python3 python3-pip
```

**macOS:**
```bash
brew install python3
```

### 2. Google Chrome

**التثبيت:**
- Windows/macOS: https://www.google.com/chrome/
- Linux: `sudo apt install google-chrome-stable`

### 3. FFmpeg (اختياري لكن موصى به)

**Windows:**
1. حمّل من: https://ffmpeg.org/download.html
2. استخرج إلى `C:\ffmpeg`
3. أضف `C:\ffmpeg\bin` إلى PATH

**Linux:**
```bash
sudo apt install ffmpeg
```

**macOS:**
```bash
brew install ffmpeg
```

## طرق التثبيت

### الطريقة 1: تلقائي (موصى به) ⭐

```bash
python run.py
```

سيقوم تلقائياً بـ:
1. ✅ التحقق من Python
2. ✅ تثبيت المكتبات
3. ✅ إنشاء المجلدات
4. ✅ تشغيل البوت

### الطريقة 2: يدوي

**الخطوة 1: تثبيت المكتبات**
```bash
pip install -r requirements.txt
```

**الخطوة 2: تشغيل الإعداد**
```bash
python setup.py
```

**الخطوة 3: تشغيل البوت**
```bash
python whatsapp_bot.py
```

### الطريقة 3: باستخدام سكريبت Shell (Linux/macOS)

```bash
chmod +x start.sh
./start.sh
```

## التحقق من التثبيت

```bash
python test_installation.py
```

يجب أن ترى:
```
✅ Python: 3.x.x
✅ جميع الملفات موجودة
✅ جميع المكتبات مثبتة
```

## حل مشاكل التثبيت

### المشكلة 1: pip غير موجود

**الحل:**
```bash
python -m ensurepip --upgrade
```

### المشكلة 2: خطأ في تثبيت المكتبات

**الحل:**
```bash
pip install --upgrade pip
pip install -r requirements.txt --no-cache-dir
```

### المشكلة 3: selenium لا يعمل

**الحل:**
```bash
pip uninstall selenium webdriver-manager
pip install selenium==4.15.2 webdriver-manager==4.0.1
```

### المشكلة 4: FFmpeg غير موجود

**الحل:**
- راجع قسم "المتطلبات الأساسية" أعلاه
- البوت سيعمل بدون FFmpeg لكن بدون ضغط

### المشكلة 5: صلاحيات في Linux

**الحل:**
```bash
chmod +x start.sh
chmod +x *.py
```

## التثبيت في بيئة افتراضية (موصى به)

### إنشاء البيئة
```bash
python -m venv venv
```

### تفعيل البيئة

**Windows:**
```cmd
venv\Scripts\activate
```

**Linux/macOS:**
```bash
source venv/bin/activate
```

### تثبيت المكتبات
```bash
pip install -r requirements.txt
```

### التشغيل
```bash
python run.py
```

## التثبيت على خادم (Server)

### استخدام screen

```bash
screen -S anime-bot
python run.py
# Ctrl+A ثم D للخروج
```

### العودة للجلسة
```bash
screen -r anime-bot
```

### استخدام tmux

```bash
tmux new -s anime-bot
python run.py
# Ctrl+B ثم D للخروج
```

### العودة للجلسة
```bash
tmux attach -t anime-bot
```

## التثبيت على Docker (متقدم)

### إنشاء Dockerfile

```dockerfile
FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    chromium \
    chromium-driver \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "run.py"]
```

### بناء وتشغيل

```bash
docker build -t anime-bot .
docker run -it anime-bot
```

## ما بعد التثبيت

### 1. اختبار التثبيت
```bash
python test_installation.py
```

### 2. تشغيل البوت
```bash
python run.py
```

### 3. مسح QR Code
- افتح واتساب على هاتفك
- اذهب إلى الإعدادات > الأجهزة المرتبطة
- امسح QR Code من المتصفح

### 4. إرسال رسالة اختبار
- أرسل `/start` من أي محادثة
- تابع التعليمات

## التحديث

### تحديث المكتبات
```bash
pip install --upgrade -r requirements.txt
```

### تحديث الكود
```bash
git pull  # إذا كنت تستخدم Git
```

## إلغاء التثبيت

### حذف البيئة الافتراضية
```bash
rm -rf venv/
```

### حذف المكتبات
```bash
pip uninstall -r requirements.txt -y
```

### حذف الملفات
```bash
rm -rf whatsapp_session/
rm -rf downloads/
rm anime_bot.db
```

## الأمان

### ملفات يجب حمايتها
- `whatsapp_session/` - جلسة الواتساب
- `anime_bot.db` - قاعدة البيانات
- `.env` - المتغيرات (إن وجد)

### الصلاحيات الموصى بها
```bash
chmod 700 whatsapp_session/
chmod 600 anime_bot.db
```

## الدعم

إذا واجهت مشاكل:
1. ✅ راجع `test_installation.py`
2. ✅ تحقق من `README.md`
3. ✅ راجع هذا الملف
4. ✅ ابحث عن الخطأ

---

✅ **جاهز؟ ابدأ الآن:**

```bash
python run.py
```

🎉 **استمتع!**
