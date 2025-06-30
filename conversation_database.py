import sqlite3
import json
import datetime
from typing import List, Dict, Optional, Tuple
import logging
import os

# Check for Render environment and set DB path accordingly
IS_RENDER_ENV = 'RENDER' in os.environ
DB_DIR = "/var/data"
DB_NAME = "conversation_history.db"

if IS_RENDER_ENV:
    # Create the data directory if it doesn't exist
    os.makedirs(DB_DIR, exist_ok=True)
    DATABASE_PATH = os.path.join(DB_DIR, DB_NAME)
else:
    DATABASE_PATH = DB_NAME
    
logging.basicConfig(level=logging.INFO)

class ConversationDatabase:
    def __init__(self, db_path=DATABASE_PATH):
        """Initialize the conversation database"""
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize database tables"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Create conversations table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS conversations (
                        conversation_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        summary TEXT,
                        tags TEXT
                    )
                """)
                
                # Create messages table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS messages (
                        message_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        conversation_id INTEGER,
                        role TEXT NOT NULL,
                        content TEXT NOT NULL,
                        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        message_type TEXT DEFAULT 'text',
                        metadata TEXT,
                        FOREIGN KEY (conversation_id) REFERENCES conversations (conversation_id)
                    )
                """)
                
                # Create conversation context table for cross-references
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS conversation_context (
                        context_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        conversation_id INTEGER,
                        context_type TEXT NOT NULL,
                        context_data TEXT NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (conversation_id) REFERENCES conversations (conversation_id)
                    )
                """)
                
                # Create indexes for better performance
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_conversation_id ON messages(conversation_id)")
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_timestamp ON messages(timestamp)")
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_role ON messages(role)")
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_context_conversation ON conversation_context(conversation_id)")
                
                conn.commit()
                logging.info("✅ Database initialized successfully")
                
        except Exception as e:
            logging.error(f"❌ Error initializing database: {e}")
            raise
    
    def create_conversation(self, title: str, summary: str = None, tags: List[str] = None) -> int:
        """Create a new conversation and return its ID"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                tags_json = json.dumps(tags) if tags else None
                
                cursor.execute("""
                    INSERT INTO conversations (title, summary, tags)
                    VALUES (?, ?, ?)
                """, (title, summary, tags_json))
                
                conversation_id = cursor.lastrowid
                conn.commit()
                
                logging.info(f"✅ Created conversation: {title} (ID: {conversation_id})")
                return conversation_id
                
        except Exception as e:
            logging.error(f"❌ Error creating conversation: {e}")
            raise
    
    def add_message(self, conversation_id: int, role: str, content: str, 
                   message_type: str = "text", metadata: Dict = None) -> int:
        """Add a message to a conversation"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                metadata_json = json.dumps(metadata) if metadata else None
                
                cursor.execute("""
                    INSERT INTO messages (conversation_id, role, content, message_type, metadata)
                    VALUES (?, ?, ?, ?, ?)
                """, (conversation_id, role, content, message_type, metadata_json))
                
                message_id = cursor.lastrowid
                
                # Update conversation's updated_at timestamp
                cursor.execute("""
                    UPDATE conversations 
                    SET updated_at = CURRENT_TIMESTAMP 
                    WHERE conversation_id = ?
                """, (conversation_id,))
                
                conn.commit()
                
                logging.info(f"✅ Added message to conversation {conversation_id}")
                return message_id
                
        except Exception as e:
            logging.error(f"❌ Error adding message: {e}")
            raise
    
    def get_conversation(self, conversation_id: int) -> Optional[Dict]:
        """Get a conversation with all its messages"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Get conversation details
                cursor.execute("""
                    SELECT conversation_id, title, created_at, updated_at, summary, tags
                    FROM conversations 
                    WHERE conversation_id = ?
                """, (conversation_id,))
                
                conv_row = cursor.fetchone()
                if not conv_row:
                    return None
                
                conversation = {
                    'conversation_id': conv_row[0],
                    'title': conv_row[1],
                    'created_at': conv_row[2],
                    'updated_at': conv_row[3],
                    'summary': conv_row[4],
                    'tags': json.loads(conv_row[5]) if conv_row[5] else []
                }
                
                # Get all messages
                cursor.execute("""
                    SELECT message_id, role, content, timestamp, message_type, metadata
                    FROM messages 
                    WHERE conversation_id = ?
                    ORDER BY timestamp ASC
                """, (conversation_id,))
                
                messages = []
                for row in cursor.fetchall():
                    message = {
                        'message_id': row[0],
                        'role': row[1],
                        'content': row[2],
                        'timestamp': row[3],
                        'message_type': row[4],
                        'metadata': json.loads(row[5]) if row[5] else {}
                    }
                    messages.append(message)
                
                conversation['messages'] = messages
                return conversation
                
        except Exception as e:
            logging.error(f"❌ Error getting conversation: {e}")
            raise
    
    def get_all_conversations(self, limit: int = 50) -> List[Dict]:
        """Get all conversations with basic info"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    SELECT conversation_id, title, created_at, updated_at, summary, tags,
                           (SELECT COUNT(*) FROM messages WHERE conversation_id = c.conversation_id) as message_count
                    FROM conversations c
                    ORDER BY updated_at DESC
                    LIMIT ?
                """, (limit,))
                
                conversations = []
                for row in cursor.fetchall():
                    conversation = {
                        'conversation_id': row[0],
                        'title': row[1],
                        'created_at': row[2],
                        'updated_at': row[3],
                        'summary': row[4],
                        'tags': json.loads(row[5]) if row[5] else [],
                        'message_count': row[6]
                    }
                    conversations.append(conversation)
                
                return conversations
                
        except Exception as e:
            logging.error(f"❌ Error getting conversations: {e}")
            raise
    
    def search_conversations(self, query: str) -> List[Dict]:
        """Search conversations by content"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    SELECT DISTINCT c.conversation_id, c.title, c.created_at, c.updated_at, c.summary, c.tags,
                           (SELECT COUNT(*) FROM messages WHERE conversation_id = c.conversation_id) as message_count
                    FROM conversations c
                    JOIN messages m ON c.conversation_id = m.conversation_id
                    WHERE c.title LIKE ? OR c.summary LIKE ? OR m.content LIKE ?
                    ORDER BY c.updated_at DESC
                """, (f'%{query}%', f'%{query}%', f'%{query}%'))
                
                conversations = []
                for row in cursor.fetchall():
                    conversation = {
                        'conversation_id': row[0],
                        'title': row[1],
                        'created_at': row[2],
                        'updated_at': row[3],
                        'summary': row[4],
                        'tags': json.loads(row[5]) if row[5] else [],
                        'message_count': row[6]
                    }
                    conversations.append(conversation)
                
                return conversations
                
        except Exception as e:
            logging.error(f"❌ Error searching conversations: {e}")
            raise
    
    def get_conversation_context(self, conversation_id: int, context_type: str = None) -> List[Dict]:
        """Get context information for a conversation"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                if context_type:
                    cursor.execute("""
                        SELECT context_id, context_type, context_data, created_at
                        FROM conversation_context
                        WHERE conversation_id = ? AND context_type = ?
                        ORDER BY created_at DESC
                    """, (conversation_id, context_type))
                else:
                    cursor.execute("""
                        SELECT context_id, context_type, context_data, created_at
                        FROM conversation_context
                        WHERE conversation_id = ?
                        ORDER BY created_at DESC
                    """, (conversation_id,))
                
                contexts = []
                for row in cursor.fetchall():
                    context = {
                        'context_id': row[0],
                        'context_type': row[1],
                        'context_data': json.loads(row[2]),
                        'created_at': row[3]
                    }
                    contexts.append(context)
                
                return contexts
                
        except Exception as e:
            logging.error(f"❌ Error getting conversation context: {e}")
            raise
    
    def add_conversation_context(self, conversation_id: int, context_type: str, context_data: Dict):
        """Add context information to a conversation"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                context_json = json.dumps(context_data)
                
                cursor.execute("""
                    INSERT INTO conversation_context (conversation_id, context_type, context_data)
                    VALUES (?, ?, ?)
                """, (conversation_id, context_type, context_json))
                
                conn.commit()
                logging.info(f"✅ Added context to conversation {conversation_id}")
                
        except Exception as e:
            logging.error(f"❌ Error adding conversation context: {e}")
            raise
    
    def get_relevant_context(self, current_query: str, limit: int = 5) -> List[Dict]:
        """Get relevant context from previous conversations based on current query"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Search for relevant conversations and their context
                cursor.execute("""
                    SELECT DISTINCT c.conversation_id, c.title, cc.context_type, cc.context_data, cc.created_at
                    FROM conversations c
                    JOIN conversation_context cc ON c.conversation_id = cc.conversation_id
                    JOIN messages m ON c.conversation_id = m.conversation_id
                    WHERE m.content LIKE ? OR c.title LIKE ? OR c.summary LIKE ?
                    ORDER BY cc.created_at DESC
                    LIMIT ?
                """, (f'%{current_query}%', f'%{current_query}%', f'%{current_query}%', limit))
                
                contexts = []
                for row in cursor.fetchall():
                    context = {
                        'conversation_id': row[0],
                        'conversation_title': row[1],
                        'context_type': row[2],
                        'context_data': json.loads(row[3]),
                        'created_at': row[4]
                    }
                    contexts.append(context)
                
                return contexts
                
        except Exception as e:
            logging.error(f"❌ Error getting relevant context: {e}")
            raise
    
    def update_conversation_summary(self, conversation_id: int, summary: str):
        """Update conversation summary"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    UPDATE conversations 
                    SET summary = ?, updated_at = CURRENT_TIMESTAMP
                    WHERE conversation_id = ?
                """, (summary, conversation_id))
                
                conn.commit()
                logging.info(f"✅ Updated summary for conversation {conversation_id}")
                
        except Exception as e:
            logging.error(f"❌ Error updating conversation summary: {e}")
            raise
    
    def delete_conversation(self, conversation_id: int):
        """Delete a conversation and all its messages"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Delete messages first (due to foreign key constraint)
                cursor.execute("DELETE FROM messages WHERE conversation_id = ?", (conversation_id,))
                
                # Delete context
                cursor.execute("DELETE FROM conversation_context WHERE conversation_id = ?", (conversation_id,))
                
                # Delete conversation
                cursor.execute("DELETE FROM conversations WHERE conversation_id = ?", (conversation_id,))
                
                conn.commit()
                logging.info(f"✅ Deleted conversation {conversation_id}")
                
        except Exception as e:
            logging.error(f"❌ Error deleting conversation: {e}")
            raise
    
    def get_conversation_statistics(self) -> Dict:
        """Get database statistics"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Get total conversations
                cursor.execute("SELECT COUNT(*) FROM conversations")
                total_conversations = cursor.fetchone()[0]
                
                # Get total messages
                cursor.execute("SELECT COUNT(*) FROM messages")
                total_messages = cursor.fetchone()[0]
                
                # Get recent activity
                cursor.execute("""
                    SELECT COUNT(*) FROM conversations 
                    WHERE updated_at >= datetime('now', '-7 days')
                """)
                recent_conversations = cursor.fetchone()[0]
                
                # Get average messages per conversation
                cursor.execute("""
                    SELECT AVG(message_count) FROM (
                        SELECT conversation_id, COUNT(*) as message_count 
                        FROM messages 
                        GROUP BY conversation_id
                    )
                """)
                avg_messages = cursor.fetchone()[0] or 0
                
                return {
                    'total_conversations': total_conversations,
                    'total_messages': total_messages,
                    'recent_conversations': recent_conversations,
                    'average_messages_per_conversation': round(avg_messages, 2)
                }
                
        except Exception as e:
            logging.error(f"❌ Error getting statistics: {e}")
            raise

# Example usage and testing
if __name__ == "__main__":
    # Test the database
    db = ConversationDatabase()
    
    # Create a test conversation
    conv_id = db.create_conversation("Test Shopping Session", "Looking for electronics", ["electronics", "shopping"])
    
    # Add some messages
    db.add_message(conv_id, "user", "I'm looking for a new laptop")
    db.add_message(conv_id, "assistant", "I can help you find a laptop. What's your budget?")
    db.add_message(conv_id, "user", "Around $1000")
    
    # Add context
    db.add_conversation_context(conv_id, "product_interest", {"category": "laptops", "budget": 1000})
    
    print("✅ Database test completed successfully!") 