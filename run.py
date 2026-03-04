# -*- coding: utf-8 -*-
"""
ملف التشغيل الرئيسي مع التثبيت التلقائي
"""

import os
import sys
import subprocess

def check_setup():
    """التحقق من اكتمال الإعداد"""
    # التحقق من المتطلبات
    try:
        import selenium
        import requests
        import cloudscraper
        import bs4
        import ffmpeg
        return True
    except ImportError:
        return False

def run_setup():
    """تشغيل الإعداد"""
    print("🔧 لم يتم العثور على الإعداد المطلوب")
    print("📦 جاري التثبيت التلقائي...\n")

    try:
        subprocess.check_call([sys.executable, "setup.py"])
        print("\n✅ تم الإعداد بنجاح!")
        return True
    except subprocess.CalledProcessError:
        print("\n❌ فشل الإعداد التلقائي")
        print("يرجى تشغيل: python setup.py")
        return False

def main():
    """الوظيفة الرئيسية"""
    print("=" * 60)
    print("🎌 بوت تحميل الأنمي للواتساب 🎌")
    print("=" * 60)
    print()

    # التحقق من الإعداد
    if not check_setup():
        if not run_setup():
            sys.exit(1)
        print("\n⚠️ يرجى إعادة تشغيل البوت بعد التثبيت")
        print("   python run.py")
        sys.exit(0)

    # تشغيل البوت
    try:
        print("🚀 جاري تشغيل البوت...")
        print()

        from whatsapp_bot import WhatsAppBot

        bot = WhatsAppBot()
        bot.run()

    except KeyboardInterrupt:
        print("\n\n👋 تم إيقاف البوت")
    except Exception as e:
        print(f"\n❌ خطأ: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
