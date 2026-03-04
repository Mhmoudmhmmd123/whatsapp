# -*- coding: utf-8 -*-
"""
بوت واتساب لتحميل الأنمي
"""

import os
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import pickle

from database import Database
from anime_downloader import AnimeDownloader
from video_compressor import VideoCompressor
from anime_sites import ANIME_SITES, get_sites_list, QUALITY_OPTIONS, DOWNLOAD_SERVERS

class WhatsAppBot:
    def __init__(self):
        self.db = Database()
        self.downloader = AnimeDownloader()
        self.compressor = VideoCompressor()
        self.driver = None
        self.wait = None
        self.setup_driver()

    def setup_driver(self):
        """إعداد متصفح Chrome"""
        print("🌐 جاري إعداد المتصفح...")

        chrome_options = Options()
        chrome_options.add_argument("--user-data-dir=./whatsapp_session")
        chrome_options.add_argument("--profile-directory=Default")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])

        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=chrome_options
        )
        self.wait = WebDriverWait(self.driver, 30)
        print("✅ تم إعداد المتصفح")

    def login_whatsapp(self):
        """تسجيل الدخول إلى واتساب ويب"""
        print("📱 جاري الاتصال بواتساب ويب...")
        self.driver.get("https://web.whatsapp.com")

        try:
            # انتظار تحميل الواجهة
            self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[contenteditable='true']")))
            print("✅ تم الاتصال بواتساب ويب بنجاح!")
            return True
        except:
            print("⚠️ يرجى مسح رمز QR للدخول...")
            input("اضغط Enter بعد المسح...")
            return True

    def find_chat(self, contact_name):
        """البحث عن محادثة"""
        try:
            search_box = self.wait.until(
                EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]'))
            )
            search_box.clear()
            search_box.send_keys(contact_name)
            time.sleep(2)

            # النقر على أول نتيجة
            first_result = self.wait.until(
                EC.presence_of_element_located((By.XPATH, '//div[@class="_8nE1Y"]'))
            )
            first_result.click()
            time.sleep(1)
            return True
        except Exception as e:
            print(f"خطأ في البحث عن المحادثة: {e}")
            return False

    def send_message(self, message):
        """إرسال رسالة"""
        try:
            message_box = self.wait.until(
                EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]'))
            )
            message_box.clear()
            message_box.send_keys(message)
            message_box.send_keys(Keys.ENTER)
            time.sleep(1)
            return True
        except Exception as e:
            print(f"خطأ في إرسال الرسالة: {e}")
            return False

    def send_file(self, file_path, caption=""):
        """إرسال ملف"""
        try:
            if not os.path.exists(file_path):
                print(f"الملف غير موجود: {file_path}")
                return False

            # النقر على زر المرفقات
            attach_btn = self.wait.until(
                EC.presence_of_element_located((By.XPATH, '//div[@title="Attach"]'))
            )
            attach_btn.click()
            time.sleep(1)

            # تحديد زر الصور والفيديو
            file_input = self.driver.find_element(By.CSS_SELECTOR, 'input[type="file"]')
            file_input.send_keys(os.path.abspath(file_path))
            time.sleep(3)

            # إضافة تعليق إن وجد
            if caption:
                caption_box = self.wait.until(
                    EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]'))
                )
                caption_box.send_keys(caption)

            # إرسال
            send_btn = self.wait.until(
                EC.presence_of_element_located((By.XPATH, '//span[@data-icon="send"]'))
            )
            send_btn.click()
            time.sleep(2)

            print(f"✅ تم إرسال الملف: {os.path.basename(file_path)}")
            return True
        except Exception as e:
            print(f"خطأ في إرسال الملف: {e}")
            return False

    def get_last_message(self):
        """الحصول على آخر رسالة واردة"""
        try:
            messages = self.driver.find_elements(By.CSS_SELECTOR, 'div.message-in span.selectable-text')
            if messages:
                return messages[-1].text
            return ""
        except Exception as e:
            print(f"خطأ في قراءة الرسالة: {e}")
            return ""

    def process_user_request(self, phone, message):
        """معالجة طلب المستخدم"""
        # الحصول على الجلسة الحالية
        step, data = self.db.get_session(phone)

        # البدء من جديد
        if message.lower() in ['/start', 'بداية', 'ابدأ']:
            self.db.clear_session(phone)
            self.db.add_user(phone)
            return self.get_welcome_message()

        # إلغاء
        if message.lower() in ['/cancel', 'إلغاء']:
            self.db.clear_session(phone)
            return "تم الإلغاء. اكتب /start للبدء من جديد"

        # خطوات التحميل
        if not step or step == 'welcome':
            # اختيار الموقع
            self.db.update_session(phone, 'select_site', {})
            return self.get_sites_selection_message()

        elif step == 'select_site':
            # حفظ الموقع
            site_id = message.strip()
            if site_id not in ANIME_SITES:
                return "❌ رقم موقع غير صحيح. حاول مرة أخرى أو اكتب /cancel للإلغاء"

            data['site_id'] = site_id
            data['site_info'] = ANIME_SITES[site_id]
            self.db.update_session(phone, 'enter_anime', data)
            return "📝 أدخل اسم الأنمي:"

        elif step == 'enter_anime':
            data['anime_name'] = message.strip()
            self.db.update_session(phone, 'enter_season', data)
            return "🎬 أدخل رقم الموسم (مثال: 1):"

        elif step == 'enter_season':
            data['season'] = message.strip()
            self.db.update_session(phone, 'enter_episode', data)
            return "📺 أدخل رقم الحلقة (مثال: 5):"

        elif step == 'enter_episode':
            data['episode'] = message.strip()
            self.db.update_session(phone, 'select_quality', data)
            return self.get_quality_selection_message()

        elif step == 'select_quality':
            quality = message.strip().upper()
            if quality not in QUALITY_OPTIONS:
                return "❌ جودة غير صحيحة. اختر من القائمة أو اكتب /cancel"

            data['quality'] = quality
            self.db.update_session(phone, 'select_server', data)
            return self.get_server_selection_message()

        elif step == 'select_server':
            server = message.strip().lower()
            if server not in DOWNLOAD_SERVERS:
                return "❌ سيرفر غير صحيح. اختر من القائمة أو اكتب /cancel"

            data['server'] = server
            self.db.update_session(phone, 'downloading', data)

            # بدء التحميل
            return self.start_download(phone, data)

        return "استخدم /start للبدء"

    def get_welcome_message(self):
        """رسالة الترحيب"""
        return """
🎌 مرحباً بك في بوت تحميل الأنمي! 🎌

يمكنني مساعدتك في تحميل حلقات الأنمي من أكثر من 50 موقع!

✨ الميزات:
• تحميل من 55+ موقع أنمي
• اختيار الجودة المناسبة
• ضغط تلقائي للفيديو
• إرسال مباشر على الواتساب

للبدء، اكتب "ابدأ" أو /start
        """

    def get_sites_selection_message(self):
        """رسالة اختيار الموقع"""
        sites_list = get_sites_list()
        return f"""
🌐 اختر الموقع الذي تريد التحميل منه:

{sites_list}

أدخل الرقم المقابل للموقع:
        """

    def get_quality_selection_message(self):
        """رسالة اختيار الجودة"""
        qualities = "\n".join([f"{i+1}. {q}" for i, q in enumerate(QUALITY_OPTIONS)])
        return f"""
🎥 اختر الجودة:

{qualities}

أدخل الجودة (مثال: 720p):
        """

    def get_server_selection_message(self):
        """رسالة اختيار السيرفر"""
        servers = "\n".join([f"{i+1}. {s}" for i, s in enumerate(DOWNLOAD_SERVERS[:10])])
        return f"""
🖥️ اختر سيرفر التحميل:

{servers}

أدخل اسم السيرفر (مثال: mega):
        """

    def start_download(self, phone, data):
        """بدء عملية التحميل"""
        try:
            site_info = data['site_info']
            anime_name = data['anime_name']
            season = data['season']
            episode = data['episode']
            quality = data['quality']
            server = data['server']

            # إنشاء سجل في قاعدة البيانات
            download_id = self.db.add_download(
                phone, anime_name, episode, season,
                site_info['name'], quality, server, 'downloading'
            )

            self.send_message("⏳ جاري البحث والتحميل... قد يستغرق بضع دقائق")

            # التحميل
            file_path, status = self.downloader.download_anime_episode(
                site_info['url'], anime_name, season, episode, quality, server
            )

            if status != 'success' or not file_path:
                self.db.update_download_status(download_id, 'failed')
                self.db.clear_session(phone)
                return f"❌ فشل التحميل: {status}\n\nجرب موقعاً آخر أو اكتب /start"

            self.send_message("✅ تم التحميل! جاري الضغط...")

            # الضغط
            compressed_file, compress_status = self.compressor.compress_for_whatsapp(file_path)

            if compress_status == 'success' and compressed_file:
                final_file = compressed_file
            else:
                final_file = file_path

            # إرسال الملف
            self.send_message("📤 جاري إرسال الملف...")
            caption = f"🎌 {anime_name}\n📺 S{season}E{episode}\n🎥 {quality}"

            if self.send_file(final_file, caption):
                self.db.update_download_status(download_id, 'completed', final_file)
                self.db.clear_session(phone)

                # حذف الملفات المؤقتة
                try:
                    if os.path.exists(file_path):
                        os.remove(file_path)
                    if compressed_file and os.path.exists(compressed_file):
                        os.remove(compressed_file)
                except:
                    pass

                return "✅ تم إرسال الحلقة بنجاح! 🎉\n\nاكتب /start لتحميل حلقة أخرى"
            else:
                self.db.update_download_status(download_id, 'send_failed', final_file)
                return f"❌ فشل إرسال الملف\nالملف محفوظ في: {final_file}"

        except Exception as e:
            self.db.clear_session(phone)
            return f"❌ حدث خطأ: {str(e)}\n\nاكتب /start للمحاولة مرة أخرى"

    def run(self):
        """تشغيل البوت"""
        print("🤖 بوت واتساب جاهز!")
        print("=" * 50)

        if not self.login_whatsapp():
            print("فشل الاتصال بواتساب")
            return

        print("\n✅ البوت يعمل الآن!")
        print("💡 أرسل رسالة من أي محادثة لبدء التفاعل\n")

        last_processed_message = ""

        while True:
            try:
                # البحث عن رسائل جديدة
                unread_chats = self.driver.find_elements(By.CSS_SELECTOR, 'span[data-icon="unread-count"]')

                if unread_chats:
                    # فتح أول محادثة غير مقروءة
                    unread_chats[0].click()
                    time.sleep(2)

                    # قراءة آخر رسالة
                    message = self.get_last_message()

                    if message and message != last_processed_message:
                        print(f"\n📨 رسالة جديدة: {message}")

                        # استخراج رقم الهاتف (تقريبي)
                        try:
                            chat_title = self.driver.find_element(By.CSS_SELECTOR, 'span[dir="auto"]').text
                            phone = chat_title
                        except:
                            phone = "unknown"

                        # معالجة الطلب
                        response = self.process_user_request(phone, message)

                        # إرسال الرد
                        self.send_message(response)
                        last_processed_message = message

                        print(f"✅ تم الرد")

                time.sleep(2)

            except KeyboardInterrupt:
                print("\n\n👋 إيقاف البوت...")
                break
            except Exception as e:
                print(f"خطأ: {e}")
                time.sleep(5)

        self.driver.quit()

if __name__ == "__main__":
    bot = WhatsAppBot()
    bot.run()
