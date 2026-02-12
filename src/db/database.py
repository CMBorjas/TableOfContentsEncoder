import sqlite3
import os
import hashlib
from typing import Optional, Tuple, List
from ..core.models import EncodedItem, TOCItem

class Database:
    DB_FILE = "encodings.db"

    def __init__(self):
        # Store in the root of the project or adjacent to src
        base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        self.db_path = os.path.join(base_path, self.DB_FILE)
        self._init_db()

    def _init_db(self):
        """Initialize the database schema."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # encodings table
        # Unique constraint on book_hash + chapter_index (assuming sequential processing)
        # OR book_hash + page + title
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS encodings (
                book_hash TEXT,
                chapter_index INTEGER,
                page INTEGER,
                title TEXT,
                locus TEXT,
                actor TEXT,
                imagery TEXT,
                scent_pos TEXT,
                scent_neg TEXT,
                PRIMARY KEY (book_hash, chapter_index)
            )
        ''')
        conn.commit()
        conn.close()

    @staticmethod
    def compute_book_hash(filepath: str) -> str:
        """Computes a SHA256 hash of the file content (first 8KB is usually enough for id output)."""
        # Proper hashing should read the whole file, or reasonable chunks
        sha = hashlib.sha256()
        try:
            with open(filepath, 'rb') as f:
                while True:
                    data = f.read(65536)
                    if not data:
                        break
                    sha.update(data)
            return sha.hexdigest()
        except Exception:
            return "unknown"

    def get_encoding(self, book_hash: str, chapter_index: int) -> Optional[Tuple]:
        """Retrieves encoding for a specific item."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT locus, actor, imagery, scent_pos, scent_neg FROM encodings WHERE book_hash=? AND chapter_index=?", (book_hash, chapter_index))
        row = cursor.fetchone()
        conn.close()
        return row

    def save_encoding(self, book_hash: str, chapter_index: int, item: EncodedItem):
        """Saves encoding to the database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO encodings (book_hash, chapter_index, page, title, locus, actor, imagery, scent_pos, scent_neg)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            book_hash, 
            chapter_index, 
            item.toc_item.page, 
            item.toc_item.title,
            item.locus, 
            item.actor, 
            item.imagery, 
            item.scent_positive, 
            item.scent_negative
        ))
        conn.commit()
        conn.close()
