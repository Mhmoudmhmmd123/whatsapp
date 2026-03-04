# -*- coding: utf-8 -*-
"""
ضغط ملفات الفيديو
"""

import os
import subprocess
import ffmpeg
from pathlib import Path

class VideoCompressor:
    def __init__(self):
        self.check_ffmpeg()

    def check_ffmpeg(self):
        """التحقق من توفر FFmpeg"""
        try:
            subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("⚠️ تحذير: FFmpeg غير مثبت")
            return False

    def get_video_info(self, input_file):
        """الحصول على معلومات الفيديو"""
        try:
            probe = ffmpeg.probe(input_file)
            video_info = next(s for s in probe['streams'] if s['codec_type'] == 'video')
            duration = float(probe['format']['duration'])
            size = int(probe['format']['size'])
            bitrate = int(probe['format']['bit_rate'])

            return {
                'duration': duration,
                'size': size,
                'bitrate': bitrate,
                'width': video_info['width'],
                'height': video_info['height'],
                'codec': video_info['codec_name']
            }
        except Exception as e:
            print(f"خطأ في الحصول على معلومات الفيديو: {e}")
            return None

    def compress_video(self, input_file, output_file=None, target_size_mb=25, quality="medium"):
        """
        ضغط الفيديو

        Args:
            input_file: ملف الإدخال
            output_file: ملف الإخراج (اختياري)
            target_size_mb: الحجم المستهدف بالميغابايت
            quality: جودة الضغط (low, medium, high)
        """
        try:
            if not os.path.exists(input_file):
                return None, "الملف غير موجود"

            # تحديد ملف الإخراج
            if not output_file:
                base, ext = os.path.splitext(input_file)
                output_file = f"{base}_compressed{ext}"

            # الحصول على معلومات الفيديو
            info = self.get_video_info(input_file)
            if not info:
                return None, "فشل الحصول على معلومات الفيديو"

            print(f"📊 حجم الملف الأصلي: {info['size'] / (1024*1024):.2f} MB")
            print(f"⏱️ المدة: {info['duration']:.2f} ثانية")

            # حساب البت ريت المستهدف
            target_size_bits = target_size_mb * 8 * 1024 * 1024
            target_bitrate = int((target_size_bits / info['duration']) * 0.95)  # 95% للأمان

            # إعدادات الجودة
            crf_values = {
                'low': 28,
                'medium': 23,
                'high': 18
            }
            crf = crf_values.get(quality, 23)

            print(f"🎬 جاري الضغط بجودة {quality}...")

            # ضغط الفيديو باستخدام FFmpeg
            stream = ffmpeg.input(input_file)
            stream = ffmpeg.output(
                stream,
                output_file,
                video_bitrate=f'{target_bitrate}',
                vcodec='libx264',
                crf=crf,
                preset='medium',
                acodec='aac',
                audio_bitrate='128k',
                **{'movflags': '+faststart'}
            )
            stream = ffmpeg.overwrite_output(stream)

            # تنفيذ الضغط
            ffmpeg.run(stream, capture_stdout=True, capture_stderr=True)

            # التحقق من النتيجة
            if os.path.exists(output_file):
                output_size = os.path.getsize(output_file) / (1024 * 1024)
                print(f"✅ تم الضغط بنجاح!")
                print(f"📊 الحجم الجديد: {output_size:.2f} MB")
                print(f"💾 التوفير: {((info['size']/(1024*1024)) - output_size):.2f} MB")

                return output_file, "success"
            else:
                return None, "فشل إنشاء الملف المضغوط"

        except Exception as e:
            print(f"❌ خطأ في الضغط: {e}")
            return None, f"خطأ: {str(e)}"

    def compress_for_whatsapp(self, input_file, output_file=None):
        """
        ضغط الفيديو للواتساب (حد أقصى 16 ميغا)
        """
        return self.compress_video(input_file, output_file, target_size_mb=15, quality="medium")

    def extract_thumbnail(self, video_file, output_file=None, timestamp='00:00:01'):
        """استخراج صورة مصغرة من الفيديو"""
        try:
            if not output_file:
                base = os.path.splitext(video_file)[0]
                output_file = f"{base}_thumb.jpg"

            stream = ffmpeg.input(video_file, ss=timestamp)
            stream = ffmpeg.output(stream, output_file, vframes=1)
            stream = ffmpeg.overwrite_output(stream)
            ffmpeg.run(stream, capture_stdout=True, capture_stderr=True)

            if os.path.exists(output_file):
                return output_file
            return None
        except Exception as e:
            print(f"خطأ في استخراج الصورة المصغرة: {e}")
            return None

    def convert_to_whatsapp_format(self, input_file, output_file=None):
        """
        تحويل الفيديو إلى صيغة متوافقة مع الواتساب
        """
        try:
            if not output_file:
                base = os.path.splitext(input_file)[0]
                output_file = f"{base}_whatsapp.mp4"

            print("📱 جاري التحويل لصيغة الواتساب...")

            stream = ffmpeg.input(input_file)
            stream = ffmpeg.output(
                stream,
                output_file,
                vcodec='libx264',
                acodec='aac',
                video_bitrate='500k',
                audio_bitrate='128k',
                vf='scale=640:-2',  # تصغير الدقة
                **{
                    'movflags': '+faststart',
                    'profile:v': 'baseline',
                    'level': '3.0'
                }
            )
            stream = ffmpeg.overwrite_output(stream)
            ffmpeg.run(stream, capture_stdout=True, capture_stderr=True)

            if os.path.exists(output_file):
                size = os.path.getsize(output_file) / (1024 * 1024)
                print(f"✅ تم التحويل! الحجم: {size:.2f} MB")
                return output_file, "success"

            return None, "فشل التحويل"
        except Exception as e:
            return None, f"خطأ: {str(e)}"
