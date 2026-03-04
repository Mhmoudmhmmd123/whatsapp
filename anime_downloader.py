# -*- coding: utf-8 -*-
"""
محمل الأنمي من مواقع متعددة
"""

import os
import requests
import cloudscraper
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time
import re
from fake_useragent import UserAgent
from tqdm import tqdm

class AnimeDownloader:
    def __init__(self):
        self.scraper = cloudscraper.create_scraper()
        self.ua = UserAgent()
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': self.ua.random
        })

    def search_anime(self, site_url, anime_name):
        """البحث عن أنمي في الموقع"""
        try:
            search_url = f"{site_url}/search?q={anime_name}"
            response = self.scraper.get(search_url, timeout=30)

            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'lxml')
                # البحث عن روابط الأنمي (يختلف حسب كل موقع)
                results = soup.find_all('a', href=re.compile(r'anime|series'))

                anime_list = []
                for result in results[:10]:  # أول 10 نتائج
                    title = result.get_text(strip=True)
                    link = urljoin(site_url, result.get('href'))
                    anime_list.append({'title': title, 'link': link})

                return anime_list
            return []
        except Exception as e:
            print(f"خطأ في البحث: {e}")
            return []

    def get_episodes(self, anime_url, season=None):
        """الحصول على قائمة الحلقات"""
        try:
            response = self.scraper.get(anime_url, timeout=30)
            soup = BeautifulSoup(response.content, 'lxml')

            # البحث عن الحلقات (يختلف حسب كل موقع)
            episodes = soup.find_all('a', href=re.compile(r'episode|ep'))

            episode_list = []
            for ep in episodes:
                ep_number = re.search(r'\d+', ep.get_text())
                if ep_number:
                    episode_list.append({
                        'number': ep_number.group(),
                        'link': urljoin(anime_url, ep.get('href'))
                    })

            return episode_list
        except Exception as e:
            print(f"خطأ في الحصول على الحلقات: {e}")
            return []

    def get_download_links(self, episode_url, quality="720p", server=""):
        """استخراج روابط التحميل"""
        try:
            response = self.scraper.get(episode_url, timeout=30)
            soup = BeautifulSoup(response.content, 'lxml')

            # البحث عن روابط التحميل
            download_links = []

            # البحث عن أزرار التحميل
            download_buttons = soup.find_all('a', href=re.compile(r'download|dl|get'))

            for button in download_buttons:
                link = button.get('href')
                text = button.get_text(strip=True).lower()

                # فلترة حسب الجودة
                if quality.lower() in text or 'download' in text:
                    download_links.append({
                        'url': urljoin(episode_url, link),
                        'quality': quality,
                        'text': text
                    })

            # البحث في iframe
            iframes = soup.find_all('iframe')
            for iframe in iframes:
                src = iframe.get('src')
                if src:
                    download_links.append({
                        'url': urljoin(episode_url, src),
                        'quality': quality,
                        'text': 'iframe_source'
                    })

            return download_links
        except Exception as e:
            print(f"خطأ في استخراج الروابط: {e}")
            return []

    def get_direct_link(self, download_page_url):
        """الحصول على الرابط المباشر من صفحة التحميل"""
        try:
            response = self.scraper.get(download_page_url, timeout=30)
            soup = BeautifulSoup(response.content, 'lxml')

            # البحث عن الرابط المباشر
            direct_links = []

            # محاولات متعددة للعثور على الرابط
            video_tags = soup.find_all('video')
            for video in video_tags:
                src = video.get('src')
                if src:
                    direct_links.append(urljoin(download_page_url, src))

            # البحث في source tags
            source_tags = soup.find_all('source')
            for source in source_tags:
                src = source.get('src')
                if src:
                    direct_links.append(urljoin(download_page_url, src))

            # البحث عن روابط mp4/mkv
            all_links = soup.find_all('a', href=re.compile(r'\.(mp4|mkv|avi|webm)'))
            for link in all_links:
                direct_links.append(urljoin(download_page_url, link.get('href')))

            return direct_links[0] if direct_links else None
        except Exception as e:
            print(f"خطأ في الحصول على الرابط المباشر: {e}")
            return None

    def download_file(self, url, output_path, chunk_size=8192):
        """تحميل الملف مع شريط التقدم"""
        try:
            response = self.session.get(url, stream=True, timeout=60)
            total_size = int(response.headers.get('content-length', 0))

            with open(output_path, 'wb') as file:
                with tqdm(total=total_size, unit='B', unit_scale=True, desc=os.path.basename(output_path)) as pbar:
                    for chunk in response.iter_content(chunk_size=chunk_size):
                        if chunk:
                            file.write(chunk)
                            pbar.update(len(chunk))

            return True
        except Exception as e:
            print(f"خطأ في التحميل: {e}")
            return False

    def download_anime_episode(self, site_url, anime_name, season, episode, quality, server, output_dir="downloads"):
        """تحميل حلقة أنمي كاملة"""
        try:
            # إنشاء مجلد التحميلات
            os.makedirs(output_dir, exist_ok=True)

            # البحث عن الأنمي
            print(f"🔍 البحث عن: {anime_name}")
            anime_results = self.search_anime(site_url, anime_name)

            if not anime_results:
                return None, "لم يتم العثور على الأنمي"

            # اختيار أول نتيجة
            anime_url = anime_results[0]['link']
            print(f"✅ تم العثور على: {anime_results[0]['title']}")

            # الحصول على الحلقات
            print("📋 جاري الحصول على قائمة الحلقات...")
            episodes = self.get_episodes(anime_url, season)

            # البحث عن الحلقة المطلوبة
            target_episode = None
            for ep in episodes:
                if ep['number'] == str(episode):
                    target_episode = ep
                    break

            if not target_episode:
                return None, f"الحلقة {episode} غير متوفرة"

            # الحصول على روابط التحميل
            print(f"🔗 جاري الحصول على روابط التحميل للحلقة {episode}...")
            download_links = self.get_download_links(target_episode['link'], quality, server)

            if not download_links:
                return None, "لم يتم العثور على روابط تحميل"

            # محاولة التحميل من الروابط المتاحة
            for link_info in download_links:
                print(f"⬇️ محاولة التحميل من: {link_info['text']}")

                # الحصول على الرابط المباشر
                direct_link = self.get_direct_link(link_info['url'])

                if not direct_link:
                    direct_link = link_info['url']

                # اسم الملف
                filename = f"{anime_name.replace(' ', '_')}_S{season}_E{episode}_{quality}.mp4"
                output_path = os.path.join(output_dir, filename)

                # التحميل
                if self.download_file(direct_link, output_path):
                    print(f"✅ تم التحميل بنجاح: {filename}")
                    return output_path, "success"

            return None, "فشل التحميل من جميع الروابط"

        except Exception as e:
            return None, f"خطأ: {str(e)}"
              
