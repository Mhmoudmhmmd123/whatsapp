# -*- coding: utf-8 -*-
"""
إدارة قاعدة البيانات SQLite
"""

import sqlite3
import json
from datetime import datetime

class Database:
    def __init__(self, db_file="anime_bot.db"):
        self.db_file = db_file
        self.init_database()

    def init_database(self):
        """إنشاء جداول قاعدة البيانات"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()

        # جدول المستخدمين
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                phone TEXT PRIMARY KEY,
                name TEXT,
                created_at TIMESTAMP,
                last_active TIMESTAMP,
                preferences TEXT
            )
        ''')

        # جدول التحميلات
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS downloads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_phone TEXT,
                anime_name TEXT,
                episode TEXT,
                season TEXT,
                site TEXT,
                quality TEXT,
                server TEXT,
                status TEXT,
                file_path TEXT,
                download_date TIMESTAMP,
                FOREIGN KEY (user_phone) REFERENCES users(phone)
            )
        ''')

        # جدول الجلسات
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sessions (
                phone TEXT PRIMARY KEY,
                current_step TEXT,
                temp_data TEXT,
                updated_at TIMESTAMP
            )
        ''')

        conn.commit()
        conn.close()

    def add_user(self, phone, name=""):
        """إضافة مستخدم جديد"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()

        cursor.execute('''
            INSERT OR REPLACE INTO users (phone, name, created_at, last_active)
            VALUES (?, ?, ?, ?)
        ''', (phone, name, datetime.now(), datetime.now()))

        conn.commit()
        conn.close()

    def update_session(self, phone, step, data):
        """تحديث جلسة المستخدم"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()

        cursor.execute('''
            INSERT OR REPLACE INTO sessions (phone, current_step, temp_data, updated_at)
            VALUES (?, ?, ?, ?)
        ''', (phone, step, json.dumps(data, ensure_ascii=False), datetime.now()))

        conn.commit()
        conn.close()

    def get_session(self, phone):
        """الحصول على جلسة المستخدم"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()

        cursor.execute('SELECT current_step, temp_data FROM sessions WHERE phone = ?', (phone,))
        result = cursor.fetchone()
        conn.close()

        if result:
            return result[0], json.loads(result[1]) if result[1] else {}
        return None, {}

    def clear_session(self, phone):
        """مسح جلسة المستخدم"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM sessions WHERE phone = ?', (phone,))
        conn.commit()
        conn.close()

    def add_download(self, user_phone, anime_name, episode, season, site, quality, server, status, file_path=""):
        """إضافة سجل تحميل"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO downloads
            (user_phone, anime_name, episode, season, site, quality, server, status, file_path, download_date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (user_phone, anime_name, episode, season, site, quality, server, status, file_path, datetime.now()))

        conn.commit()
        download_id = cursor.lastrowid
        conn.close()
        return download_id

    def update_download_status(self, download_id, status, file_path=""):
        """تحديث حالة التحميل"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()

        cursor.execute('''
            UPDATE downloads SET status = ?, file_path = ? WHERE id = ?
        ''', (status, file_path, download_id))

        conn.commit()
        conn.close()

    def get_user_downloads(self, phone, limit=10):
        """الحصول على تحميلات المستخدم"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT anime_name, episode, season, site, quality, status, download_date
            FROM downloads
            WHERE user_phone = ?
            ORDER BY download_date DESC
            LIMIT ?
        ''', (phone, limit))

        results = cursor.fetchall()
        conn.close()
        return results
