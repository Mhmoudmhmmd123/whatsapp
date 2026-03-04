# -*- coding: utf-8 -*-
"""
ملف الإعدادات
"""

import os
from pathlib import Path

# المسارات
BASE_DIR = Path(__file__).parent
DOWNLOADS_DIR = BASE_DIR / "downloads"
SESSION_DIR = BASE_DIR / "whatsapp_session"
DATABASE_FILE = BASE_DIR / "anime_bot.db"

# إعدادات التحميل
DEFAULT_QUALITY = "720p"
DEFAULT_COMPRESSION = True
MAX_FILE_SIZE_MB = 16  # حد أقصى لحجم ملف الواتساب
DOWNLOAD_TIMEOUT = 300  # 5 دقائق

# إعدادات الضغط
COMPRESSION_QUALITY = "medium"  # low, medium, high
TARGET_SIZE_MB = 15  # الحجم المستهدف بعد الضغط

# إعدادات الواتساب
WHATSAPP_WEB_URL = "https://web.whatsapp.com"
MESSAGE_DELAY = 1  # تأخير بين الرسائل (بالثواني)
FILE_SEND_DELAY = 2  # تأخير بعد إرسال الملفات

# إعدادات المتصفح
HEADLESS_MODE = False  # تشغيل المتصفح في الخلفية (False لرؤية المتصفح)
BROWSER_TIMEOUT = 30  # مهلة انتظار العناصر

# رسائل البوت
MESSAGES = {
    "ar": {
        "welcome": """
🎌 مرحباً بك في بوت تحميل الأنمي! 🎌

يمكنني مساعدتك في تحميل حلقات الأنمي من أكثر من 50 موقع!

✨ الميزات:
• تحميل من 55+ موقع أنمي
• اختيار الجودة المناسبة
• ضغط تلقائي للفيديو
• إرسال مباشر على الواتساب

للبدء، اكتب "ابدأ" أو /start
        """,
        "select_site": "🌐 اختر الموقع الذي تريد التحميل منه:",
        "enter_anime": "📝 أدخل اسم الأنمي:",
        "enter_season": "🎬 أدخل رقم الموسم (مثال: 1):",
        "enter_episode": "📺 أدخل رقم الحلقة (مثال: 5):",
        "select_quality": "🎥 اختر الجودة:",
        "select_server": "🖥️ اختر سيرفر التحميل:",
        "searching": "🔍 جاري البحث...",
        "downloading": "⏳ جاري التحميل... قد يستغرق بضع دقائق",
        "compressing": "✅ تم التحميل! جاري الضغط...",
        "sending": "📤 جاري إرسال الملف...",
        "success": "✅ تم إرسال الحلقة بنجاح! 🎉",
        "error": "❌ حدث خطأ",
        "cancelled": "تم الإلغاء. اكتب /start للبدء من جديد",
        "invalid_site": "❌ رقم موقع غير صحيح. حاول مرة أخرى",
        "invalid_quality": "❌ جودة غير صحيحة. اختر من القائمة",
        "invalid_server": "❌ سيرفر غير صحيح. اختر من القائمة",
        "not_found": "❌ لم يتم العثور على الأنمي",
        "download_failed": "❌ فشل التحميل",
    },
    "en": {
        "welcome": """
🎌 Welcome to Anime Download Bot! 🎌

I can help you download anime episodes from 50+ sites!

✨ Features:
• Download from 55+ anime sites
• Choose quality
• Auto compression
• Direct WhatsApp delivery

Type "start" or /start to begin
        """,
        "select_site": "🌐 Select the site to download from:",
        "enter_anime": "📝 Enter anime name:",
        "enter_season": "🎬 Enter season number (e.g., 1):",
        "enter_episode": "📺 Enter episode number (e.g., 5):",
        "select_quality": "🎥 Select quality:",
        "select_server": "🖥️ Select download server:",
        "searching": "🔍 Searching...",
        "downloading": "⏳ Downloading... This may take a few minutes",
        "compressing": "✅ Downloaded! Compressing...",
        "sending": "📤 Sending file...",
        "success": "✅ Episode sent successfully! 🎉",
        "error": "❌ An error occurred",
        "cancelled": "Cancelled. Type /start to begin again",
        "invalid_site": "❌ Invalid site number. Try again",
        "invalid_quality": "❌ Invalid quality. Choose from list",
        "invalid_server": "❌ Invalid server. Choose from list",
        "not_found": "❌ Anime not found",
        "download_failed": "❌ Download failed",
    }
}

# اللغة الافتراضية
DEFAULT_LANGUAGE = "ar"

def get_message(key, lang=None):
    """الحصول على رسالة بلغة معينة"""
    lang = lang or DEFAULT_LANGUAGE
    return MESSAGES.get(lang, MESSAGES["ar"]).get(key, "")

def create_directories():
    """إنشاء المجلدات المطلوبة"""
    DOWNLOADS_DIR.mkdir(exist_ok=True)
    SESSION_DIR.mkdir(exist_ok=True)

# إنشاء المجلدات عند الاستيراد
create_directories()
