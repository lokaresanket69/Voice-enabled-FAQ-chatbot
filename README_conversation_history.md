# ShopSmart Conversation History System

## 🗄️ Overview

The ShopSmart Voice Assistant now includes a comprehensive conversation history system that allows you to:

- **Save all conversations** in a SQLite database
- **Reference previous conversations** for context
- **Search through conversation history**
- **Maintain continuity** across multiple sessions
- **Extract and store context** automatically

## ✨ Key Features

### 📚 Conversation Management
- **Automatic conversation creation** - Each chat session is saved as a separate conversation
- **Conversation titles and summaries** - Easy identification and organization
- **Tags and metadata** - Categorize conversations for better organization
- **Message history** - Complete text-based conversation history

### 🔍 Context Awareness
- **Cross-conversation references** - AI remembers previous conversations
- **Automatic context extraction** - Product interests, budgets, order details
- **Relevant conversation retrieval** - Find related conversations based on current queries
- **Continuity maintenance** - Seamless experience across sessions

### 📊 Search and Analytics
- **Full-text search** - Search through all conversations and messages
- **Conversation statistics** - Track usage patterns and engagement
- **Recent activity monitoring** - See your latest conversations
- **Message counting** - Track conversation length and engagement

## 🗂️ Database Structure

### Tables

#### `conversations`
- `conversation_id` - Unique identifier
- `title` - Conversation title
- `created_at` - Creation timestamp
- `updated_at` - Last update timestamp
- `summary` - Conversation summary
- `tags` - JSON array of tags

#### `messages`
- `message_id` - Unique identifier
- `conversation_id` - Foreign key to conversations
- `role` - "user" or "assistant"
- `content` - Message text content
- `timestamp` - Message timestamp
- `message_type` - Type of message (text, voice, etc.)
- `metadata` - Additional message data

#### `conversation_context`
- `context_id` - Unique identifier
- `conversation_id` - Foreign key to conversations
- `context_type` - Type of context (product_interest, budget, etc.)
- `context_data` - JSON context data
- `created_at` - Context creation timestamp

## 🚀 How It Works

### 1. **Automatic Conversation Creation**
```python
# When you start chatting, a new conversation is automatically created
chatbot = EcommerceChatbot()
chatbot.start_new_conversation("Shopping Session", "Looking for electronics")
```

### 2. **Message Storage**
```python
# Every message (user and AI) is automatically saved
response = chatbot.get_response("I need a laptop under $1000")
# This automatically saves both the user message and AI response
```

### 3. **Context Extraction**
```python
# The system automatically extracts relevant context
# - Product interests (laptop, phone, etc.)
# - Budget information ($1000)
# - Order-related queries
# - Shipping and delivery questions
```

### 4. **Cross-Conversation References**
```python
# When you ask "Remember when I ordered that laptop?"
# The system searches previous conversations for relevant context
previous_context = chatbot.get_conversation_context("laptop order")
```

## 💬 Usage Examples

### Starting a New Conversation
```python
chatbot = EcommerceChatbot()
conv_id = chatbot.start_new_conversation(
    title="Electronics Shopping",
    summary="Looking for laptops and phones",
    tags=["electronics", "laptops", "phones"]
)
```

### Loading Previous Conversations
```python
# Load a specific conversation
conversation = chatbot.load_conversation(conversation_id)

# List all conversations
conversations = chatbot.list_conversations(limit=10)

# Search conversations
results = chatbot.search_conversations("laptop order")
```

### Context-Aware Responses
```python
# The AI automatically considers previous conversations
response = chatbot.get_response("What about the laptop I asked about earlier?")
# This will reference previous laptop-related conversations
```

## 🎯 Real-World Scenarios

### Scenario 1: Product Research
1. **Conversation 1**: "I'm looking for a gaming laptop under $1500"
2. **Conversation 2**: "What about the laptop I asked about yesterday?"
   - AI remembers the gaming laptop query and budget
   - Provides relevant follow-up information

### Scenario 2: Order Tracking
1. **Conversation 1**: "I ordered a Samsung Galaxy S24"
2. **Conversation 2**: "Where is my phone order?"
   - AI references the previous Samsung order
   - Provides specific tracking information

### Scenario 3: Return Policy
1. **Conversation 1**: "What's your return policy for electronics?"
2. **Conversation 2**: "I want to return the laptop I bought"
   - AI connects the return policy question with the laptop purchase
   - Provides specific return instructions

## 🔧 Technical Implementation

### Database Operations
```python
# Create conversation
conv_id = db.create_conversation(title, summary, tags)

# Add message
db.add_message(conv_id, "user", "I need a laptop")

# Get conversation
conversation = db.get_conversation(conv_id)

# Search conversations
results = db.search_conversations("laptop")

# Get relevant context
context = db.get_relevant_context("laptop order")
```

### Context Extraction
```python
def _extract_and_save_context(self, user_message, bot_response):
    context_data = {}
    
    # Extract product interests
    product_keywords = ["laptop", "phone", "smartphone", "shirt", "jeans"]
    for keyword in product_keywords:
        if keyword.lower() in user_message.lower():
            context_data["product_interest"] = keyword
    
    # Extract budget information
    budget_match = re.search(r'\$(\d+)', user_message)
    if budget_match:
        context_data["budget"] = int(budget_match.group(1))
    
    # Save context
    if context_data:
        self.db.add_conversation_context(conv_id, "conversation_context", context_data)
```

## 📱 Streamlit Interface Features

### Conversation History Panel
- **Expandable section** with all conversations
- **Search functionality** to find specific conversations
- **Load buttons** to switch between conversations
- **Conversation metadata** (title, date, message count)

### Current Conversation Display
- **Active conversation indicator**
- **Message count and timestamp**
- **Tags and summary information**

### Statistics Dashboard
- **Total conversations** count
- **Total messages** count
- **Recent activity** (last 7 days)
- **Average messages per conversation**

## 🔒 Privacy and Security

### Data Storage
- **Local SQLite database** - All data stored locally
- **No cloud storage** - Your conversations stay on your device
- **Text-only storage** - Audio files are not saved, only transcribed text
- **Automatic cleanup** - Temporary files are deleted after processing

### Data Protection
- **No external transmission** - Conversations are not sent to external servers
- **Local processing** - All AI processing happens through secure APIs
- **User control** - You can delete conversations at any time

## 🛠️ Configuration

### Database Location
- **Default**: `conversation_history.db` in the project directory
- **Custom location**: Modify `db_path` in `ConversationDatabase()`

### Backup and Migration
```python
# Backup database
import shutil
shutil.copy("conversation_history.db", "backup_conversations.db")

# Restore database
shutil.copy("backup_conversations.db", "conversation_history.db")
```

## 📈 Performance Considerations

### Database Optimization
- **Indexed queries** for fast searches
- **Efficient storage** with JSON compression
- **Automatic cleanup** of temporary data
- **Connection pooling** for better performance

### Memory Management
- **Lazy loading** of conversation history
- **Pagination** for large conversation lists
- **Context caching** for frequently accessed data

## 🐛 Troubleshooting

### Common Issues

1. **Database not found**
   - Run `python setup.py` to initialize the database
   - Check file permissions in the project directory

2. **Conversation not loading**
   - Verify conversation ID exists
   - Check database integrity with `db.get_conversation_statistics()`

3. **Search not working**
   - Ensure database is properly indexed
   - Check for special characters in search queries

4. **Context not being extracted**
   - Verify message content is being processed
   - Check logging for extraction errors

### Debugging
```python
# Check database status
stats = db.get_conversation_statistics()
print(f"Database has {stats['total_conversations']} conversations")

# Test conversation loading
conversation = db.get_conversation(1)
if conversation:
    print(f"Loaded conversation: {conversation['title']}")

# Test context extraction
contexts = db.get_relevant_context("laptop")
print(f"Found {len(contexts)} relevant contexts")
```

## 🚀 Future Enhancements

### Planned Features
- **Conversation export** (JSON, CSV, PDF)
- **Advanced analytics** and insights
- **Conversation templates** for common scenarios
- **Multi-user support** with user authentication
- **Cloud backup** (optional)
- **Advanced search** with filters and date ranges

### API Extensions
- **REST API** for external integrations
- **Webhook support** for real-time updates
- **Third-party integrations** (CRM, analytics)

---

**The conversation history system transforms your shopping assistant into a truly personalized experience that remembers your preferences, past orders, and shopping patterns! 🛍️✨** 