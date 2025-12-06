import sqlite3
import datetime
from typing import Optional, Dict, List
from config import DATABASE_PATH

class Database:
    def __init__(self):
        self.conn = sqlite3.connect(DATABASE_PATH, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.create_tables()
    
    def create_tables(self):
        """Create all necessary database tables"""
        cursor = self.conn.cursor()
        
        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                first_name TEXT,
                last_name TEXT,
                language_code TEXT DEFAULT 'en',
                join_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_blocked BOOLEAN DEFAULT 0,
                is_premium BOOLEAN DEFAULT 0
            )
        ''')
        
        # User statistics
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_stats (
                user_id INTEGER PRIMARY KEY,
                message_count INTEGER DEFAULT 0,
                file_count INTEGER DEFAULT 0,
                ai_count INTEGER DEFAULT 0,
                payment_count INTEGER DEFAULT 0,
                FOREIGN KEY (user_id) REFERENCES users (user_id)
            )
        ''')
        
        # Message logs
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS message_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                message_type TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (user_id)
            )
        ''')
        
        # File processing logs
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS file_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                file_type TEXT,
                file_size INTEGER,
                processing_time REAL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (user_id)
            )
        ''')
        
        # Broadcast history
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS broadcasts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                admin_id INTEGER,
                message_text TEXT,
                sent_count INTEGER,
                failed_count INTEGER,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        self.conn.commit()
    
    def add_user(self, user_id: int, username: str = None, first_name: str = None, 
                 last_name: str = None, language_code: str = 'en') -> bool:
        """Add or update user in database"""
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                INSERT OR REPLACE INTO users 
                (user_id, username, first_name, last_name, language_code, last_active)
                VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
            ''', (user_id, username, first_name, last_name, language_code))
            
            # Initialize stats if new user
            cursor.execute('''
                INSERT OR IGNORE INTO user_stats (user_id)
                VALUES (?)
            ''', (user_id,))
            
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error adding user: {e}")
            return False
    
    def get_user(self, user_id: int) -> Optional[Dict]:
        """Get user information"""
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
        row = cursor.fetchone()
        return dict(row) if row else None
    
    def update_last_active(self, user_id: int):
        """Update user's last active timestamp"""
        cursor = self.conn.cursor()
        cursor.execute('''
            UPDATE users SET last_active = CURRENT_TIMESTAMP WHERE user_id = ?
        ''', (user_id,))
        self.conn.commit()
    
    def get_user_stats(self, user_id: int) -> Dict:
        """Get user statistics"""
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM user_stats WHERE user_id = ?', (user_id,))
        row = cursor.fetchone()
        return dict(row) if row else {
            'message_count': 0, 'file_count': 0, 
            'ai_count': 0, 'payment_count': 0
        }
    
    def increment_stat(self, user_id: int, stat_type: str):
        """Increment a specific user statistic"""
        valid_stats = ['message_count', 'file_count', 'ai_count', 'payment_count']
        if stat_type not in valid_stats:
            return
        
        cursor = self.conn.cursor()
        cursor.execute(f'''
            UPDATE user_stats 
            SET {stat_type} = {stat_type} + 1 
            WHERE user_id = ?
        ''', (user_id,))
        self.conn.commit()
    
    def log_message(self, user_id: int, message_type: str):
        """Log a message interaction"""
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO message_logs (user_id, message_type)
            VALUES (?, ?)
        ''', (user_id, message_type))
        self.conn.commit()
    
    def log_file_processing(self, user_id: int, file_type: str, 
                           file_size: int, processing_time: float):
        """Log file processing event"""
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO file_logs (user_id, file_type, file_size, processing_time)
            VALUES (?, ?, ?, ?)
        ''', (user_id, file_type, file_size, processing_time))
        self.conn.commit()
    
    def get_total_users(self) -> int:
        """Get total number of users"""
        cursor = self.conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM users')
        return cursor.fetchone()[0]
    
    def get_active_users_today(self) -> int:
        """Get users active in last 24 hours"""
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT COUNT(*) FROM users 
            WHERE last_active >= datetime('now', '-1 day')
        ''')
        return cursor.fetchone()[0]
    
    def get_new_users_24h(self) -> int:
        """Get new users in last 24 hours"""
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT COUNT(*) FROM users 
            WHERE join_date >= datetime('now', '-1 day')
        ''')
        return cursor.fetchone()[0]
    
    def get_total_messages(self) -> int:
        """Get total message count"""
        cursor = self.conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM message_logs')
        return cursor.fetchone()[0]
    
    def get_messages_24h(self) -> int:
        """Get messages in last 24 hours"""
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT COUNT(*) FROM message_logs 
            WHERE timestamp >= datetime('now', '-1 day')
        ''')
        return cursor.fetchone()[0]
    
    def get_all_user_ids(self) -> List[int]:
        """Get all user IDs for broadcasting"""
        cursor = self.conn.cursor()
        cursor.execute('SELECT user_id FROM users WHERE is_blocked = 0')
        return [row[0] for row in cursor.fetchall()]
    
    def close(self):
        """Close database connection"""
        self.conn.close()

# Global database instance
db = Database()
