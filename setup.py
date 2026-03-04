# -*- coding: utf-8 -*-
"""
سكريبت التثبيت التلقائي
"""

import subprocess
import sys
import os
import platform

def check_python_version():
    """التحقق من إصدار Python"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ يتطلب Python 3.8 أو أحدث")
        print(f"الإصدار الحالي: {version.major}.{version.minor}.{version.micro}")
        sys.exit(1)
    print(f"✅ Python {version.major}.{version.minor}.{version.micro}")

def install_requirements():
    """تثبيت المتطلبات"""
    print("\n📦 جاري تثبيت المتطلبات...")

    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "--upgrade", "pip"
        ])
        print("✅ تم تحديث pip")

        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ])
        print("✅ تم تثبيت جميع المتطلبات")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ فشل تثبيت المتطلبات: {e}")
        return False

def check_ffmpeg():
    """التحقق من FFmpeg"""
    print("\n🎬 التحقق من FFmpeg...")

    try:
        subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
        print("✅ FFmpeg مثبت")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("⚠️ FFmpeg غير مثبت")
        print("\n📝 تعليمات التثبيت:")

        system = platform.system()
        if system == "Windows":
            print("""
            Windows:
            1. قم بتحميل FFmpeg من: https://ffmpeg.org/download.html
            2. استخرج الملفات
            3. أضف مجلد bin إلى PATH
            """)
        elif system == "Darwin":  # macOS
            print("""
            macOS:
            استخدم Homebrew:
            brew install ffmpeg
            """)
        else:  # Linux
            print("""
            Linux:
            Ubuntu/Debian:
            sudo apt update && sudo apt install ffmpeg

            Fedora:
            sudo dnf install ffmpeg

            Arch:
            sudo pacman -S ffmpeg
            """)

        return False

def create_directories():
    """إنشاء المجلدات المطلوبة"""
    print("\n📁 إنشاء المجلدات...")

    directories = ['downloads', 'whatsapp_session']
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✅ {directory}")

def setup():
    """تشغيل الإعداد الكامل"""
    print("=" * 60)
    print("🎌 إعداد بوت تحميل الأنمي للواتساب 🎌")
    print("=" * 60)

    # التحقق من Python
    check_python_version()

    # تثبيت المتطلبات
    if not install_requirements():
        print("\n❌ فشل الإعداد")
        sys.exit(1)

    # التحقق من FFmpeg
    ffmpeg_installed = check_ffmpeg()

    # إنشاء المجلدات
    create_directories()

    # إنشاء ملف .env إذا لم يكن موجوداً
    if not os.path.exists('.env'):
        with open('.env', 'w', encoding='utf-8') as f:
            f.write("# إعدادات البوت\n")
            f.write("BOT_LANGUAGE=ar\n")
        print("✅ تم إنشاء ملف .env")

    print("\n" + "=" * 60)
    print("✅ تم الإعداد بنجاح!")
    print("=" * 60)

    if not ffmpeg_installed:
        print("\n⚠️ تحذير: FFmpeg غير مثبت")
        print("لن تعمل ميزة ضغط الفيديو بدونه")
        print("يرجى تثبيت FFmpeg ثم تشغيل البوت مرة أخرى")

    print("\n🚀 لتشغيل البوت:")
    print("   python run.py")
    print("\n💡 أو استخدم:")
    print("   python whatsapp_bot.py")
    print()

if __name__ == "__main__":
    setup()
