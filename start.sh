#!/bin/bash

# سكريبت تشغيل البوت على Linux/macOS

echo "=============================="
echo "🎌 بوت تحميل الأنمي للواتساب"
echo "=============================="
echo ""

# التحقق من Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 غير مثبت"
    echo "يرجى تثبيت Python 3.8 أو أحدث"
    exit 1
fi

echo "✅ Python مثبت: $(python3 --version)"

# التحقق من FFmpeg
if ! command -v ffmpeg &> /dev/null; then
    echo "⚠️ FFmpeg غير مثبت"
    echo ""
    echo "للتثبيت:"
    echo "Ubuntu/Debian: sudo apt install ffmpeg"
    echo "macOS: brew install ffmpeg"
    echo ""
    read -p "هل تريد المتابعة بدون FFmpeg؟ (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
else
    echo "✅ FFmpeg مثبت"
fi

echo ""
echo "🚀 جاري تشغيل البوت..."
echo ""

# تشغيل البوت
python3 run.py

echo ""
echo "👋 تم إيقاف البوت"
