import sqlite3
import os
from datetime import datetime

class HistoryDatabase:
    def __init__(self, db_path='./history.db'):
        self.db_path = db_path
        self._init_database()
    
    def _init_database(self):
        """初始化数据库，创建历史记录表"""
        # 确保数据库目录存在
        db_dir = os.path.dirname(self.db_path)
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir)
        
        # 创建数据库连接
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 创建历史记录表
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS generation_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_input TEXT NOT NULL,
            poetry_title TEXT NOT NULL,
            poetry_content TEXT NOT NULL,
            poetry_comment TEXT,
            image_path TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        # 创建索引以提高查询性能
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_created_at ON generation_history(created_at)')
        
        conn.commit()
        conn.close()
    
    def save_history(self, user_input, poetry_title, poetry_content, poetry_comment, image_path):
        """保存生成历史记录"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
        INSERT INTO generation_history (user_input, poetry_title, poetry_content, poetry_comment, image_path)
        VALUES (?, ?, ?, ?, ?)
        ''', (user_input, poetry_title, poetry_content, poetry_comment, image_path))
        
        history_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return history_id
    
    def get_history(self, limit=10, offset=0):
        """获取历史记录列表"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
        SELECT id, user_input, poetry_title, poetry_content, poetry_comment, image_path, created_at
        FROM generation_history
        ORDER BY created_at DESC
        LIMIT ? OFFSET ?
        ''', (limit, offset))
        
        records = cursor.fetchall()
        conn.close()
        
        # 将记录转换为字典列表
        history_list = []
        for record in records:
            history_list.append({
                'id': record[0],
                'user_input': record[1],
                'poetry_title': record[2],
                'poetry_content': record[3],
                'poetry_comment': record[4],
                'image_path': record[5],
                'created_at': record[6]
            })
        
        return history_list
    
    def get_history_by_id(self, history_id):
        """根据ID获取单个历史记录"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
        SELECT id, user_input, poetry_title, poetry_content, poetry_comment, image_path, created_at
        FROM generation_history
        WHERE id = ?
        ''', (history_id,))
        
        record = cursor.fetchone()
        conn.close()
        
        if record:
            return {
                'id': record[0],
                'user_input': record[1],
                'poetry_title': record[2],
                'poetry_content': record[3],
                'poetry_comment': record[4],
                'image_path': record[5],
                'created_at': record[6]
            }
        return None
    
    def delete_history(self, history_id):
        """删除历史记录"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM generation_history WHERE id = ?', (history_id,))
        affected_rows = cursor.rowcount
        
        conn.commit()
        conn.close()
        
        return affected_rows > 0
    
    def get_total_count(self):
        """获取历史记录总数"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM generation_history')
        count = cursor.fetchone()[0]
        
        conn.close()
        return count

# 创建全局实例供应用使用
history_db = HistoryDatabase()
