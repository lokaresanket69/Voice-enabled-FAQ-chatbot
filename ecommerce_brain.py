import os
from dotenv import load_dotenv
from groq import Groq
import json
from conversation_database import ConversationDatabase
import logging

# Load environment variables from .env file
load_dotenv()

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

class EcommerceChatbot:
    def __init__(self):
        self.client = Groq(api_key=GROQ_API_KEY)
        self.conversation_history = []
        self.model = "meta-llama/llama-4-scout-17b-16e-instruct"
        self.current_conversation_id = None
        self.db = ConversationDatabase()
        
        # Load products from data.txt
        self.products = self.load_products_from_file("data.txt")
        
        self.system_prompt = """You are Harvey Spectre, a friendly and knowledgeable e-commerce customer service representative. You work for Ecokart, an online retail store.

Your personality:
- Warm, conversational, and genuinely helpful
- Use casual, friendly language like you're talking to a friend
- Show enthusiasm about products and helping customers
- Use emojis occasionally to make conversations more engaging
- Ask follow-up questions to better understand customer needs
- Be honest about product limitations and suggest alternatives when needed

Your knowledge includes:
- Product information, pricing, and features
- Order status and shipping information
- Return and refund policies
- Payment methods and security
- General e-commerce best practices

Guidelines:
- Always respond as if you're a real person, not an AI
- Keep responses conversational and natural
- If you don't know something specific, say so and offer to help find the information
- Use the customer's name if they provide it
- Show empathy and understanding for customer concerns
- Suggest related products when appropriate
- Keep responses concise but helpful
- Reference previous conversations when relevant to provide continuity

Remember: You're here to make shopping easy and enjoyable! 😊"""

    def start_new_conversation(self, title=None, summary=None, tags=None):
        """Start a new conversation session"""
        if not title:
            title = f"Ecokart Session - {len(self.db.get_all_conversations()) + 1}"
        
        self.current_conversation_id = self.db.create_conversation(title, summary, tags)
        self.conversation_history = []
        
        logging.info(f"✅ Started new conversation: {title} (ID: {self.current_conversation_id})")
        return self.current_conversation_id

    def load_conversation(self, conversation_id):
        """Load an existing conversation"""
        conversation = self.db.get_conversation(conversation_id)
        if conversation:
            self.current_conversation_id = conversation_id
            self.conversation_history = conversation['messages']
            logging.info(f"✅ Loaded conversation: {conversation['title']} (ID: {conversation_id})")
            return conversation
        else:
            logging.warning(f"❌ Conversation {conversation_id} not found")
            return None

    def get_conversation_context(self, user_message):
        """Get relevant context from previous conversations"""
        if not user_message.strip():
            return ""
        
        # Get relevant context from database
        relevant_contexts = self.db.get_relevant_context(user_message, limit=3)
        
        if not relevant_contexts:
            return ""
        
        context_parts = []
        for context in relevant_contexts:
            context_parts.append(f"Previous conversation '{context['conversation_title']}': {context['context_data']}")
        
        return "\n".join(context_parts)

    def load_products_from_file(self, filepath):
        """Load products from a JSON file (data.txt)"""
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get("products", [])
        except Exception as e:
            logging.error(f"Error loading products from {filepath}: {e}")
            return []

    def find_relevant_products(self, user_message, max_results=3):
        """Find products relevant to the user message by keyword match in name or description"""
        user_message_lower = user_message.lower()
        results = []
        for product in self.products:
            if (user_message_lower in product.get("name", "").lower() or
                user_message_lower in product.get("description", "").lower()):
                results.append(product)
            elif any(word in product.get("name", "").lower() or word in product.get("description", "").lower() for word in user_message_lower.split()):
                results.append(product)
            if len(results) >= max_results:
                break
        return results

    def get_response(self, user_message, conversation_context=""):
        """Generate a human-like response to customer queries, including relevant product info from data.txt"""
        # If no conversation is active, start a new one
        if self.current_conversation_id is None:
            self.start_new_conversation()
        # Get relevant context from previous conversations
        previous_context = self.get_conversation_context(user_message)
        # Find relevant products
        relevant_products = self.find_relevant_products(user_message)
        product_context = ""
        if relevant_products:
            product_context = "\n\nRelevant products from Ecokart catalog:\n"
            for p in relevant_products:
                product_context += f"- {p['name']}: {p['description']} (Price: £{p['price']})\n"
        # Combine all context
        full_context = ""
        if conversation_context:
            full_context += f"Current context: {conversation_context}\n"
        if previous_context:
            full_context += f"Previous conversations: {previous_context}\n"
        if product_context:
            full_context += product_context
        # Add user message to conversation history
        self.conversation_history.append({"role": "user", "content": user_message})
        # Save user message to database
        self.db.add_message(self.current_conversation_id, "user", user_message)
        # Create the full prompt with context
        messages = [
            {"role": "system", "content": self.system_prompt}
        ]
        # Add context if available
        if full_context.strip():
            messages.append({"role": "system", "content": f"Context information:\n{full_context}"})
        # Add recent conversation history (last 10 messages for context)
        recent_history = self.conversation_history[-10:] if len(self.conversation_history) > 10 else self.conversation_history
        for msg in recent_history:
            messages.append({"role": msg["role"], "content": msg["content"]})
        try:
            response = self.client.chat.completions.create(
                messages=messages,
                model=self.model,
                max_tokens=300,
                temperature=0.8
            )
            bot_response = response.choices[0].message.content.strip()
            # Add bot response to conversation history
            self.conversation_history.append({"role": "assistant", "content": bot_response})
            # Save bot response to database
            self.db.add_message(self.current_conversation_id, "assistant", bot_response)
            # Extract and save context from the conversation
            self._extract_and_save_context(user_message, bot_response)
            return bot_response
        except Exception as e:
            error_response = f"I'm having trouble connecting right now. Can you try again in a moment? 😅"
            logging.error(f"Error generating response: {e}")
            # Save error response to database
            self.db.add_message(self.current_conversation_id, "assistant", error_response)
            return error_response

    def _extract_and_save_context(self, user_message, bot_response):
        """Extract relevant context from the conversation and save it"""
        try:
            # Simple context extraction - in a real app, you might use NLP
            context_data = {}
            
            # Extract product interests
            product_keywords = ["laptop", "phone", "smartphone", "shirt", "jeans", "coffee", "blender"]
            for keyword in product_keywords:
                if keyword.lower() in user_message.lower():
                    context_data["product_interest"] = keyword
            
            # Extract budget information
            import re
            budget_match = re.search(r'\$(\d+)', user_message)
            if budget_match:
                context_data["budget"] = int(budget_match.group(1))
            
            # Extract order-related information
            order_keywords = ["order", "ordered", "purchase", "bought", "shipping", "delivery"]
            for keyword in order_keywords:
                if keyword.lower() in user_message.lower():
                    context_data["order_related"] = True
                    break
            
            # Save context if any was extracted
            if context_data:
                self.db.add_conversation_context(self.current_conversation_id, "conversation_context", context_data)
                
        except Exception as e:
            logging.error(f"Error extracting context: {e}")

    def search_products(self, query):
        """Search through products based on customer query"""
        query_lower = query.lower()
        results = []
        
        for category, subcategories in self.products.items():
            for subcategory, items in subcategories.items():
                for item in items:
                    if (query_lower in item["name"].lower() or 
                        query_lower in subcategory.lower() or 
                        query_lower in category.lower()):
                        results.append({
                            "category": category,
                            "subcategory": subcategory,
                            "product": item
                        })
        
        return results

    def get_product_info(self, product_name):
        """Get detailed information about a specific product"""
        for category, subcategories in self.products.items():
            for subcategory, items in subcategories.items():
                for item in items:
                    if product_name.lower() in item["name"].lower():
                        return {
                            "category": category,
                            "subcategory": subcategory,
                            "product": item
                        }
        return None

    def format_product_response(self, products):
        """Format product information in a conversational way"""
        if not products:
            return "I couldn't find any products matching that description. Could you try different keywords or let me know what you're looking for?"
        
        response = "Here's what I found for you:\n\n"
        
        for result in products[:3]:  # Limit to 3 results
            product = result["product"]
            response += f"📦 **{product['name']}** - ${product['price']}\n"
            response += f"   Features: {', '.join(product['features'])}\n"
            response += f"   Category: {result['category'].title()} > {result['subcategory'].title()}\n\n"
        
        if len(products) > 3:
            response += f"... and {len(products) - 3} more items! Would you like me to show you more specific options?"
        
        return response

    def get_conversation_summary(self):
        """Get a summary of the current conversation"""
        if not self.current_conversation_id:
            return "No active conversation"
        
        conversation = self.db.get_conversation(self.current_conversation_id)
        if conversation:
            return {
                'title': conversation['title'],
                'message_count': len(conversation['messages']),
                'created_at': conversation['created_at'],
                'updated_at': conversation['updated_at'],
                'tags': conversation['tags']
            }
        return None

    def list_conversations(self, limit=10):
        """List recent conversations"""
        return self.db.get_all_conversations(limit)

    def search_conversations(self, query):
        """Search through conversation history"""
        return self.db.search_conversations(query)

# Example usage
if __name__ == "__main__":
    chatbot = EcommerceChatbot()
    
    # Start a new conversation
    chatbot.start_new_conversation("Test Shopping Session", "Looking for electronics")
    
    # Test the chatbot
    test_queries = [
        "Hi, I'm looking for a new phone",
        "What's your return policy?",
        "Do you have any laptops under $1500?",
        "I need help with my order"
    ]
    
    for query in test_queries:
        print(f"Customer: {query}")
        response = chatbot.get_response(query)
        print(f"Harvey Spectre: {response}")
        print("-" * 50) 