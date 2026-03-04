# البدء السريع

## تثبيت وتشغيل بأمر واحد

```bash
python run.py
```

هذا الأمر سيقوم تلقائياً بـ:
- ✅ التحقق من Python
- ✅ تثبيت جميع المتطلبات
- ✅ إنشاء قاعدة البيانات
- ✅ تشغيل البوت

## الخطوات بعد التشغيل

### 1. مسح QR Code
```
عند أول تشغيل:
1. سيفتح متصفح اتوماتيكياً
2. امسح رمز QR من هاتفك
3. اضغط Confirm على الهاتف
```

### 2. الاستخدام
```
أرسل أي رسالة من واتساب وابدأ الحوار:

❯ ابدأ
  اختر الموقع (1-55)
  اسم الأنمي
  رقم الموسم
  رقم الحلقة
  الجودة
  سيرفر التحميل
  
✅ سيتم التحميل والضغط والإرسال تلقائياً!
```

## الملفات الرئيسية

| الملف | الوصف |
|------|--------|
| `run.py` | نقطة الدخول الرئيسية |
| `whatsapp_bot.py` | بوت الواتساب |
| `anime_downloader.py` | محمل الأنمي |
| `video_compressor.py` | ضاغط الفيديو |
| `database.py` | إدارة قاعدة البيانات SQLite |
| `anime_sites.py` | قائمة المواقع (55 موقع) |

## المجلدات

```
project/
├── downloads/          # ملفات الفيديو المحملة
├── whatsapp_session/   # جلسة الواتساب
└── anime_bot.db        # قاعدة البيانات
```

## الأوامر المتاحة

```
/start    - بدء تفاعل جديد
/cancel   - إلغاء العملية الحالية
```

## استكشاف الأخطاء

### المشكلة: "FFmpeg غير مثبت"
```bash
# Ubuntu/Debian
sudo apt install ffmpeg

# macOS
brew install ffmpeg

# Windows
# حمّل من: https://ffmpeg.org/download.html
```

### المشكلة: "خطأ في تثبيت المتطلبات"
```bash
pip install --upgrade pip
pip install -r requirements.txt --no-cache-dir
```

### المشكلة: "Selenium لا يعمل"
```bash
pip uninstall selenium webdriver-manager -y
pip install selenium==4.15.2 webdriver-manager==4.0.1
```

## دعم اللغات

- العربية (افتراضي)
- الإنجليزية (قريباً)

## المتطلبات الأدنى

- Python 3.8+
- 500 MB RAM
- اتصال إنترنت
- Google Chrome مثبت

## الإعدادات

عدّل `config.py` لتغيير:
- جودة الضغط
- حجم الملف الأقصى
- اللغة
- أوقات التأخير

---

**مزيد من التفاصيل:** اقرأ `README.md` و `INSTALL.md`
