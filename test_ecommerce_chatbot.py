#!/usr/bin/env python3
"""
Test script for the E-commerce Voice Assistant
This script demonstrates the chatbot's capabilities without requiring voice input
"""

import os
from dotenv import load_dotenv
from ecommerce_brain import EcommerceChatbot

# Load environment variables
load_dotenv()

def test_chatbot():
    """Test the e-commerce chatbot with various scenarios"""
    
    print("🛍️ ShopSmart E-commerce Chatbot Test")
    print("=" * 50)
    
    # Initialize chatbot
    chatbot = EcommerceChatbot()
    
    # Test scenarios
    test_scenarios = [
        {
            "category": "Greeting",
            "queries": [
                "Hi there!",
                "Hello, I need help",
                "Good morning"
            ]
        },
        {
            "category": "Product Search",
            "queries": [
                "I'm looking for a new phone",
                "Show me laptops under $1500",
                "Do you have any smartphones?",
                "I need a coffee maker"
            ]
        },
        {
            "category": "E-commerce Support",
            "queries": [
                "What's your return policy?",
                "How long does shipping take?",
                "Do you accept credit cards?",
                "I need help with my order"
            ]
        },
        {
            "category": "Specific Products",
            "queries": [
                "Tell me about the iPhone 15 Pro",
                "What features does the Samsung Galaxy S24 have?",
                "How much is the MacBook Pro?",
                "I want to buy a t-shirt"
            ]
        },
        {
            "category": "Complex Queries",
            "queries": [
                "I need a laptop for gaming and work, what do you recommend?",
                "What's the best smartphone for photography under $800?",
                "I'm looking for a gift for my mom, she likes cooking"
            ]
        }
    ]
    
    # Run tests
    for scenario in test_scenarios:
        print(f"\n📋 Testing: {scenario['category']}")
        print("-" * 30)
        
        for query in scenario['queries']:
            print(f"\n👤 Customer: {query}")
            response = chatbot.get_response(query)
            print(f"🤖 Alex: {response}")
            print("-" * 40)
    
    # Test product search functionality
    print("\n🔍 Testing Product Search Functionality")
    print("=" * 50)
    
    search_queries = ["phone", "laptop", "shirt", "coffee"]
    
    for query in search_queries:
        print(f"\n🔎 Searching for: '{query}'")
        results = chatbot.search_products(query)
        
        if results:
            print(f"Found {len(results)} products:")
            for i, result in enumerate(results[:3], 1):
                product = result['product']
                print(f"  {i}. {product['name']} - ${product['price']}")
                print(f"     Category: {result['category']} > {result['subcategory']}")
        else:
            print("No products found")
    
    print("\n✅ Test completed!")

def test_conversation_flow():
    """Test a natural conversation flow"""
    
    print("\n💬 Testing Natural Conversation Flow")
    print("=" * 50)
    
    chatbot = EcommerceChatbot()
    
    # Simulate a conversation
    conversation = [
        "Hi, I'm looking for a new smartphone",
        "I want something under $1000",
        "How's the camera on the iPhone 15 Pro?",
        "What about battery life?",
        "That sounds good. What's your return policy?",
        "How long does shipping take?",
        "Perfect! Thanks for your help"
    ]
    
    print("Starting conversation...\n")
    
    for i, user_message in enumerate(conversation, 1):
        print(f"👤 Customer: {user_message}")
        response = chatbot.get_response(user_message)
        print(f"🤖 Alex: {response}")
        print("-" * 50)

def main():
    """Main test function"""
    
    # Check if API key is available
    if not os.environ.get("GROQ_API_KEY"):
        print("❌ GROQ_API_KEY not found in environment variables")
        print("Please set up your .env file with your API keys")
        return
    
    try:
        # Run basic tests
        test_chatbot()
        
        # Run conversation flow test
        test_conversation_flow()
        
        print("\n🎉 All tests completed successfully!")
        print("\nTo run the full voice assistant:")
        print("  python ecommerce_voice_assistant.py")
        print("\nTo run the web interface:")
        print("  python ecommerce_gradio_app.py")
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        print("Please check your API keys and internet connection")

if __name__ == "__main__":
    main() 