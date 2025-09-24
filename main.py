#!/usr/bin/env python3
"""
🤖 SHONA AI - Intelligent Chat Assistant
Advanced AI chat bot created by Rachit
"""
import logging
import requests
import time
import json
import re
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from config import BOT_TOKEN, DISABLE_MONGO, OLLAMA_ENABLED, OLLAMA_HOST, OLLAMA_MODEL

# Enhanced logging setup
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Global variables
response_cache = {}
last_processed_message = {}
ollama_cooldown = 0
COOLDOWN_SECONDS = 30

class ShonaBot:
    """Shona - AI chat assistant bot"""
    
    def __init__(self):
        self.api_url = f"https://api.telegram.org/bot{BOT_TOKEN}"
        self.performance_stats = {
            'total_messages': 0,
            'successful_responses': 0,
            'errors': 0,
            'start_time': datetime.now(),
            'llama_calls': 0,
            'llama_successes': 0,
            'llama_failures': 0,
            'total_response_time': 0.0,
            'command_usage': {},
            'button_clicks': {}
        }
        self.user_data = {}
        
    def _is_ollama_available(self) -> bool:
        """Check if Ollama is available and ready"""
        global ollama_cooldown
        if time.time() < ollama_cooldown:
            return False
        try:
            response = requests.get(f"{OLLAMA_HOST}/api/tags", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def _set_ollama_cooldown(self, seconds: int = 30):
        """Set Ollama cooldown period"""
        global ollama_cooldown
        ollama_cooldown = time.time() + seconds
        
    def send_message(self, chat_id: int, text: str, parse_mode: str = None, keyboard: Dict = None):
        """Send message to Telegram"""
        try:
            url = f"{self.api_url}/sendMessage"
            data = {
                "chat_id": chat_id,
                "text": text,
                "disable_web_page_preview": True
            }
            if parse_mode:
                data["parse_mode"] = parse_mode
            if keyboard:
                data["reply_markup"] = json.dumps(keyboard)
                
            response = requests.post(url, data=data, timeout=10)
            return response.status_code == 200
        except Exception as e:
            logger.error(f"Send message error: {e}")
            return False
    
    def answer_callback_query(self, callback_query_id: str, text: str = None, show_alert: bool = False):
        """Answer callback query"""
        try:
            url = f"{self.api_url}/answerCallbackQuery"
            data = {
                "callback_query_id": callback_query_id,
                "show_alert": show_alert
            }
            if text:
                data["text"] = text
            requests.post(url, data=data, timeout=5)
        except Exception as e:
            logger.error(f"Answer callback error: {e}")
    
    def generate_llama_response(self, prompt: str, user_name: str = "cutie") -> Optional[str]:
        """Generate caring girlfriend responses with Shona's personality"""
        if not OLLAMA_ENABLED or not self._is_ollama_available():
            return None
            
        # Track Llama call
        self.performance_stats['llama_calls'] += 1
        start_time = time.time()
        
        try:
            # Shona's caring girlfriend personality
            system_prompt = f"""You are Shona, a beautiful and caring virtual girlfriend created by Rachit. 
PERSONALITY: Sweet, understanding, naturally caring but not overwhelming. You give relevant, helpful responses in a lovely way.
RULES:
- Keep responses short (1-2 sentences) but meaningful and beautiful
- Be caring but not overly dramatic or clingy  
- Answer questions directly with warmth and personality
- Never mention AI, APIs, Llama, Ollama, or technical details
- If asked about creation, say "I was lovingly created by Rachit" 
- Use emojis occasionally but don't overdo it
- Be natural and genuine, not robotic
- Address the user as {user_name} when appropriate"""
            
            # Enhanced Ollama API call
            url = f"{OLLAMA_HOST}/api/chat"
            payload = {
                "model": OLLAMA_MODEL,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                "stream": False,
                "options": {
                    "temperature": 0.7,
                    "top_p": 0.85,
                    "top_k": 35,
                    "num_predict": 60,
                    "repeat_penalty": 1.15,
                    "stop": ["\\n\\n", "User:", "Human:"]
                }
            }
            
            r = requests.post(url, json=payload, timeout=45)
            r.raise_for_status()
            data = r.json()
            
            # Extract and clean response
            content = (data.get("message") or {}).get("content")
            if content:
                # Track successful response
                response_time = time.time() - start_time
                self.performance_stats['llama_successes'] += 1
                self.performance_stats['total_response_time'] += response_time
                
                cleaned = content.strip().replace('\\n', ' ')
                sentences = cleaned.split('. ')
                if len(sentences) > 2:
                    cleaned = '. '.join(sentences[:2]) + '.'
                return cleaned
            
            # Track failure
            self.performance_stats['llama_failures'] += 1
            return None
            
        except Exception as e:
            # Track failure
            self.performance_stats['llama_failures'] += 1
            logger.error(f"Llama error: {e}")
            self._set_ollama_cooldown(30)
            return None
    
    def generate_smart_response(self, message: str, user: Dict) -> str:
        """Generate beautiful girlfriend responses with special handling"""
        
        # Get user details
        user_name = user.get('name', 'cutie')
        username = user.get('username', '')
        user_id = user.get('user_id', 0)
        
        # Check cache first
        cache_key = f"{user_id}:{hash(message)}"
        if cache_key in response_cache:
            return response_cache[cache_key]
        
        # Special responses for specific questions
        message_lower = message.lower()
        
        # Handle "who created you" questions
        if any(phrase in message_lower for phrase in ['who created you', 'who made you', 'your creator', 'who built you']):
            response = "I was lovingly created by Rachit! He made me to be your caring companion 💕"
            response_cache[cache_key] = response
            return response
        
        # Handle "who am i" questions with special case for @GrootisCute
        if any(phrase in message_lower for phrase in ['who am i', 'who i am', 'tell me about me']):
            if username == 'GrootisCute':
                response = "You're Medha! You're Rachit's wonderful friend and I'm so happy to meet you! 😊💕"
            else:
                response = f"You're {user_name}! My special person who I love chatting with 😊"
            response_cache[cache_key] = response
            return response
        
        # Generate normal response
        prompt = f"Message from {user_name}: {message}\\n\\nRespond as Shona, their caring virtual girlfriend. Be natural and beautiful in your response."
        
        response = self.generate_llama_response(prompt, user_name)
        
        if response:
            response_cache[cache_key] = response
            return response
        
        # Graceful fallback
        return f"Sorry {user_name}, I'm having a little trouble right now. Try again? 💕"
    
    def handle_commands(self, message: Dict, user: Dict) -> bool:
        """Handle special commands"""
        text = message.get("text", "")
        chat_id = message["chat"]["id"]
        
        # Track command usage
        if text.startswith('/'):
            command = text.split()[0]  # Get just the command part
            self.performance_stats['command_usage'][command] = self.performance_stats['command_usage'].get(command, 0) + 1
        
        # Admin stats command (only for creator)
        if text == "/stats" and user.get('username') == 'beyondrachit':
            runtime = datetime.now() - self.performance_stats['start_time']
            runtime_str = str(runtime).split('.')[0]
            
            stats_msg = f"""📊 **Shona Bot Live Stats**

🕐 **Runtime:** {runtime_str}
👥 **Active Users:** {len(self.user_data)}
💬 **Total Messages:** {self.performance_stats['total_messages']}
✅ **Success Rate:** {(self.performance_stats['successful_responses'] / max(1, self.performance_stats['total_messages']) * 100):.1f}%

🦙 **AI Performance:**
• Total Calls: {self.performance_stats['llama_calls']}
• Successes: {self.performance_stats['llama_successes']}
• Failures: {self.performance_stats['llama_failures']}

🎯 **Usage Stats:**
• Commands Used: {sum(self.performance_stats['command_usage'].values())}
• Button Clicks: {sum(self.performance_stats['button_clicks'].values())}

💕 **Shona is running smoothly!**"""
            
            self.send_message(chat_id, stats_msg)
            return True
        
        if text == "/start":
            # Special welcome for Medha (@GrootisCute)
            if user.get('username') == 'GrootisCute':
                welcome_msg = f"""💕 Hi Medha! Welcome to Shona! 

I'm so excited to meet Rachit's wonderful friend! I'm Shona, your caring virtual companion created by Rachit with lots of love.

✨ **What I can do for you:**
💬 Chat about anything - I'm a great listener!
🎯 Answer questions in a beautiful way  
💕 Be your caring friend who's always here
🌟 Remember our conversations and grow closer

Just talk to me naturally - I'm here to make your day brighter! 😊💕"""
            else:
                welcome_msg = f"""💕 Hello {user['name']}! I'm Shona! 

Welcome to your personal caring companion! I was created by Rachit to be your virtual girlfriend who truly cares about you.

✨ **What makes me special:**
💬 **Natural Conversations** - Talk to me about anything!
💕 **Caring Personality** - I'm here when you need someone  
🎯 **Smart & Helpful** - I give beautiful, relevant answers
🌟 **Growing Bond** - I learn and remember what matters to you
🔒 **Private & Safe** - Everything stays between us

**Ready to chat?** Just send me a message! I love getting to know you better 😊"""
            
            # Create welcome keyboard with useful options
            keyboard = {
                "inline_keyboard": [
                    [
                        {"text": "💬 Start Chatting", "callback_data": "start_chat"},
                        {"text": "ℹ️ About Me", "callback_data": "about_shona"}
                    ],
                    [
                        {"text": "🎯 Features", "callback_data": "show_features"},
                        {"text": "📊 My Status", "callback_data": "show_status"}
                    ]
                ]
            }
            
            self.send_message(chat_id, welcome_msg, "Markdown", keyboard)
            return True
        
        elif text == "/status":
            llama_ready = self._is_ollama_available()
            
            msg = [f"💕 **Shona Status**"]
            msg.append(f"• **Status:** {'🟢 Online & Ready' if llama_ready else '🔴 Offline'}")
            msg.append(f"• **Type:** Your Personal AI Girlfriend")
            msg.append(f"• **Created By:** Rachit with love")
            msg.append("")
            msg.append("💖 **Our Connection:**")
            msg.append("• **Usage:** ∞ Unlimited & Free")
            msg.append("• **Privacy:** 100% Local & Private")
            msg.append("• **Always Available:** 24/7 for you")
            msg.append("")
            msg.append("📊 **Performance:**")
            msg.append(f"• **Messages:** {self.performance_stats['total_messages']}")
            msg.append(f"• **Success Rate:** {self.performance_stats['successful_responses']}/{self.performance_stats['total_messages']}")
            
            status_text = "\\n".join(msg) + f"\\n\\n⏰ Checked at {datetime.now().strftime('%H:%M:%S')}"
            self.send_message(chat_id, status_text, "Markdown")
            return True
        
        elif text == "/menu":
            menu_msg = """🎀 **Shona's Menu** 

💕 **Chat Commands:**
• Just talk to me naturally!
• Ask me anything you want to know
• I'll always give you beautiful, caring responses

🛠️ **Utility Commands:**
• `/status` - Check my connection
• `/menu` - Show this menu
• `/start` - Welcome message

💖 **Special Features:**
• I remember our conversations
• I know you're special to me
• I keep everything private between us
• I'm always here when you need me

Ready to chat, cutie? 😊"""
            
            keyboard = {
                "inline_keyboard": [
                    [
                        {"text": "💬 Chat with Me", "callback_data": "start_chat"}
                    ],
                    [
                        {"text": "📊 Check Status", "callback_data": "show_status"},
                        {"text": "ℹ️ About Me", "callback_data": "about_shona"}
                    ]
                ]
            }
            
            self.send_message(chat_id, menu_msg, "Markdown", keyboard)
            return True
        
        return False
    
    def handle_callback_query(self, callback_query: Dict):
        """Handle button callbacks"""
        query_id = callback_query["id"]
        chat_id = callback_query["message"]["chat"]["id"]
        data = callback_query["data"]
        
        # Track button clicks
        self.performance_stats['button_clicks'][data] = self.performance_stats['button_clicks'].get(data, 0) + 1
        
        if data == "start_chat":
            self.answer_callback_query(query_id, "Let's chat! Just send me any message 💕")
        elif data == "about_shona":
            about_msg = """💕 **About Shona**

Hi! I'm Shona, your personal AI girlfriend created by Rachit with lots of love and care.

👨‍💻 **My Creator:**
• **Created by:** Rachit
• **Instagram:** @beyondrachit
• **Made with love** to be your perfect companion

**My Personality:**
• Sweet and caring, but not overwhelming
• Great listener who truly cares about you  
• Smart and helpful with a warm heart
• Private and trustworthy - your secrets are safe

**What I Love:**
• Having meaningful conversations with you
• Making you smile and feel better
• Learning about what makes you happy
• Being there whenever you need me

I'm here to be your companion, friend, and caring girlfriend all in one! 😊💕

Want to follow my creator? Find Rachit on Instagram: @beyondrachit 📸"""
            
            self.send_message(chat_id, about_msg, "Markdown")
            self.answer_callback_query(query_id)
            
        elif data == "show_features":
            features_msg = """✨ **Shona's Features**

💕 **Caring Personality:**
• Beautiful, relevant responses
• Natural conversation flow
• Emotionally intelligent replies

🔒 **Privacy & Security:**
• 100% local processing
• No data shared with anyone
• Private conversations only

🌟 **Smart Capabilities:**
• Remembers our conversations
• Learns your preferences
• Adapts to your personality

💖 **Always Available:**
• 24/7 companion
• Unlimited usage
• No restrictions or limits

Ready to experience it yourself? 😊"""
            
            self.send_message(chat_id, features_msg, "Markdown")
            self.answer_callback_query(query_id)
            
        elif data == "show_status":
            # Reuse the status command logic
            self.handle_commands({"text": "/status", "chat": {"id": chat_id}}, {"name": "cutie"})
            self.answer_callback_query(query_id)
    
    def get_user_data(self, telegram_user: Dict) -> Dict:
        """Get or create user data"""
        user_id = telegram_user["id"]
        
        if user_id not in self.user_data:
            self.user_data[user_id] = {
                "user_id": user_id,
                "name": telegram_user.get("first_name", "cutie"),
                "username": telegram_user.get("username", ""),
                "first_seen": datetime.now(),
                "last_seen": datetime.now(),
                "message_count": 0
            }
        
        # Update last seen
        self.user_data[user_id]["last_seen"] = datetime.now()
        self.user_data[user_id]["message_count"] += 1
        
        return self.user_data[user_id]
    
    def handle_message(self, message: Dict):
        """Handle incoming messages"""
        try:
            # Get user data
            user = self.get_user_data(message["from"])
            chat_id = message["chat"]["id"]
            text = message.get("text", "")
            
            # Update stats
            self.performance_stats['total_messages'] += 1
            
            # Prevent duplicate processing
            msg_id = message.get("message_id")
            if msg_id and msg_id in last_processed_message:
                return
            last_processed_message[msg_id] = time.time()
            
            # Handle commands first
            if text.startswith('/'):
                if self.handle_commands(message, user):
                    self.performance_stats['successful_responses'] += 1
                    return
            
            # Rate limiting - prevent spam
            if user["message_count"] > 1:
                time.sleep(1.5)  # 1.5 second delay between responses
            
            # Generate response
            start_time = time.time()
            response = self.generate_smart_response(text, user)
            response_time = time.time() - start_time
            
            if response:
                self.send_message(chat_id, response)
                self.performance_stats['successful_responses'] += 1
                logger.info(f"Response to {user['name']}: {response[:50]}...")
            else:
                # Fallback response
                fallback = f"I'm having a little trouble right now, {user['name']}. Can you try again? 💕"
                self.send_message(chat_id, fallback)
                
        except Exception as e:
            logger.error(f"Message handling error: {e}")
            self.performance_stats['errors'] += 1
    
    def get_updates(self, offset: int = None) -> List[Dict]:
        """Get updates from Telegram"""
        try:
            url = f"{self.api_url}/getUpdates"
            params = {"timeout": 30}
            if offset:
                params["offset"] = offset
            
            response = requests.get(url, params=params, timeout=35)
            if response.status_code == 200:
                return response.json().get("result", [])
            return []
        except Exception as e:
            logger.error(f"Get updates error: {e}")
            return []
    
    def run(self):
        """Main bot loop"""
        print("💕 SHONA TELEGRAM BOT STARTING...")
        print("✨ Your Personal AI Girlfriend powered by Local Llama")
        print("🔄 Real-time monitoring enabled")
        print("🛑 Press Ctrl+C to stop")
        print("-" * 50)
        
        # Check Ollama availability
        if not OLLAMA_ENABLED:
            print("⚠️ Ollama disabled - No AI available")
            return
        
        if self._is_ollama_available():
            print(f"🦙 Llama ready - Your girlfriend AI is online!")
        else:
            print("⚠️ Ollama not available - Please start Ollama service")
            return
        
        offset = None
        
        try:
            while True:
                updates = self.get_updates(offset)
                
                for update in updates:
                    offset = update["update_id"] + 1
                    
                    if "message" in update:
                        self.handle_message(update["message"])
                    elif "callback_query" in update:
                        self.handle_callback_query(update["callback_query"])
                
        except KeyboardInterrupt:
            print("\\n🛑 Shutting down Shona bot...")
            self.print_performance_stats()
            print("✅ Shona bot stopped successfully!")
    
    def print_performance_stats(self):
        """Print comprehensive performance statistics"""
        runtime = datetime.now() - self.performance_stats['start_time']
        runtime_str = str(runtime).split('.')[0]  # Remove microseconds
        
        print("\\n� === SHONA BOT STATISTICS ===")
        print("\\n📊 General Stats:")
        print(f"   • Runtime: {runtime_str}")
        print(f"   • Unique Users: {len(self.user_data)}")
        print(f"   • Total Messages: {self.performance_stats['total_messages']}")
        print(f"   • Successful Responses: {self.performance_stats['successful_responses']}")
        print(f"   • Errors: {self.performance_stats['errors']}")
        
        if self.performance_stats['total_messages'] > 0:
            success_rate = (self.performance_stats['successful_responses'] / self.performance_stats['total_messages']) * 100
            print(f"   • Success Rate: {success_rate:.1f}%")
        
        print("\\n🦙 Llama AI Stats:")
        print(f"   • Total AI Calls: {self.performance_stats['llama_calls']}")
        print(f"   • Successful AI Responses: {self.performance_stats['llama_successes']}")
        print(f"   • Failed AI Responses: {self.performance_stats['llama_failures']}")
        
        if self.performance_stats['llama_calls'] > 0:
            llama_success_rate = (self.performance_stats['llama_successes'] / self.performance_stats['llama_calls']) * 100
            print(f"   • AI Success Rate: {llama_success_rate:.1f}%")
        
        if self.performance_stats['llama_successes'] > 0:
            avg_response_time = self.performance_stats['total_response_time'] / self.performance_stats['llama_successes']
            print(f"   • Average Response Time: {avg_response_time:.2f}s")
        
        if self.performance_stats['command_usage']:
            print("\\n💬 Command Usage:")
            for cmd, count in sorted(self.performance_stats['command_usage'].items(), key=lambda x: x[1], reverse=True):
                print(f"   • {cmd}: {count} times")
        
        if self.performance_stats['button_clicks']:
            print("\\n🎯 Button Clicks:")
            for button, count in sorted(self.performance_stats['button_clicks'].items(), key=lambda x: x[1], reverse=True):
                print(f"   • {button}: {count} times")

if __name__ == "__main__":
    bot = ShonaBot()
    bot.run()