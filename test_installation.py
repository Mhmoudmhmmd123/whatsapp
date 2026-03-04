# -*- coding: utf-8 -*-
"""
اختبار التثبيت
"""

import sys
import os

def test_python_version():
    """اختبار إصدار Python"""
    version = sys.version_info
    print(f"🐍 Python: {version.major}.{version.minor}.{version.micro}", end=" ")
    if version.major >= 3 and version.minor >= 8:
        print("✅")
        return True
    else:
        print("❌ (يتطلب 3.8+)")
        return False

def test_import(module_name, package_name=None):
    """اختبار استيراد مكتبة"""
    try:
        __import__(module_name)
        print(f"📦 {package_name or module_name}: ✅")
        return True
    except ImportError:
        print(f"📦 {package_name or module_name}: ❌")
        return False

def test_ffmpeg():
    """اختبار FFmpeg"""
    import subprocess
    try:
        subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
        print("🎬 FFmpeg: ✅")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("🎬 FFmpeg: ❌ (اختياري)")
        return False

def test_files():
    """اختبار وجود الملفات"""
    files = [
        'whatsapp_bot.py',
        'anime_downloader.py',
        'video_compressor.py',
        'database.py',
        'anime_sites.py',
        'config.py',
        'requirements.txt'
    ]

    all_exist = True
    for file in files:
        exists = os.path.exists(file)
        status = "✅" if exists else "❌"
        print(f"📄 {file}: {status}")
        if not exists:
            all_exist = False

    return all_exist

def test_directories():
    """اختبار وجود المجلدات"""
    directories = ['downloads', 'whatsapp_session']

    for directory in directories:
        exists = os.path.exists(directory)
        status = "✅" if exists else "⚠️ (سيتم إنشاؤها تلقائياً)"
        print(f"📁 {directory}: {status}")

def main():
    print("=" * 60)
    print("🔍 اختبار التثبيت")
    print("=" * 60)
    print()

    # اختبار Python
    python_ok = test_python_version()
    print()

    # اختبار الملفات
    print("📂 الملفات الأساسية:")
    files_ok = test_files()
    print()

    # اختبار المجلدات
    print("📂 المجلدات:")
    test_directories()
    print()

    # اختبار المكتبات
    print("📚 المكتبات:")
    libs_ok = True
    libs_ok &= test_import('selenium')
    libs_ok &= test_import('requests')
    libs_ok &= test_import('cloudscraper')
    libs_ok &= test_import('bs4', 'beautifulsoup4')
    libs_ok &= test_import('lxml')
    libs_ok &= test_import('ffmpeg', 'ffmpeg-python')
    libs_ok &= test_import('tqdm')
    libs_ok &= test_import('fake_useragent')
    print()

    # اختبار FFmpeg
    ffmpeg_ok = test_ffmpeg()
    print()

    # النتيجة النهائية
    print("=" * 60)
    if python_ok and files_ok and libs_ok:
        print("✅ التثبيت ناجح!")
        if not ffmpeg_ok:
            print("⚠️ FFmpeg غير مثبت - الضغط لن يعمل")
        print()
        print("🚀 لتشغيل البوت:")
        print("   python run.py")
    else:
        print("❌ التثبيت غير مكتمل")
        print()
        print("🔧 لإعادة التثبيت:")
        print("   python setup.py")
    print("=" * 60)

if __name__ == "__main__":
    main()
