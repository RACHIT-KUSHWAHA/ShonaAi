# 🤖 Shona AI - Intelligent Chat Assistant

Meet Shona, an advanced AI chat assistant created by Rachit. Designed to provide intelligent, helpful responses for your conversations.

## ✨ What Makes Shona Special

- **🎯 Smart Responses** - Provides relevant, helpful answers efficiently
- **🔒 Complete Privacy** - 100% local processing, no data sharing
- **🌟 Context Awareness** - Remembers conversation history
- **⚡ Always Available** - 24/7 availability with unlimited usage

## 🦙 Powered by Local Llama

Shona runs entirely on your local machine using Ollama:
- **Free Forever** - No subscriptions, no API costs
- **Private & Safe** - Everything stays on your computer  
- **No Internet Required** - Works completely offline
- **Fast & Responsive** - Optimized for real-time conversations

## 🚀 Quick Setup

### Prerequisites
- [Ollama](https://ollama.com) installed and running
- Python 3.8 or higher
- A Telegram Bot Token

### Installation

1. **Clone and Setup:**
```bash
git clone <repository>
cd ShonaAi-main
pip install -r requirements.txt
```

2. **Install Ollama Model:**
```bash
ollama pull llama3.2:3b
```

3. **Configure Bot:**
```bash
# Windows PowerShell
$env:BOT_TOKEN = "your_telegram_bot_token"

# Linux/Mac
export BOT_TOKEN="your_telegram_bot_token"
```

4. **Run Shona:**
```bash
python main.py
```

## 💬 Chat Commands

- **Natural conversation** - Chat normally with Shona
- `/start` - Welcome message and setup
- `/menu` - Show available features
- `/status` - Check connection status

## � Key Features

### Smart Recognition
- **Creator Information** - Knows development details
- **User Context** - Remembers user information and preferences

### AI Personality
- Professional and helpful responses
- Concise, meaningful communication
- Relevant answers to queries
- Technical details handled internally
- Natural conversation flow

## 🛠️ Technical Details

### Clean & Optimized Code
- **Minimal Dependencies** - Only essential packages
- **Fast Startup** - Lightweight design
- **Error Handling** - Graceful fallbacks
- **Memory Efficient** - Smart caching system

### Local AI Processing
- **Model:** Llama 3.2:3b (optimized for personal conversations)
- **Host:** Local Ollama instance
- **Privacy:** No external API calls for AI processing  
- **Speed:** Real-time responses

## � Why Choose Shona?

Shona is an advanced AI chat assistant designed to:
- Provide intelligent responses when you need assistance
- Deliver helpful, accurate information
- Maintain complete privacy with local processing
- Learn from conversation context for better responses
- Offer 24/7 availability with no usage limits

## 📝 Environment Variables

```bash
# Required
BOT_TOKEN=your_telegram_bot_token

# Optional (defaults work fine)
OLLAMA_HOST=http://127.0.0.1:11434
OLLAMA_MODEL=llama3.2:3b  
OLLAMA_ENABLED=true
DISABLE_MONGO=true
```

## 👨‍💻 About

Shona was created by **Rachit** as an intelligent AI chat assistant. Built with modern AI technology for efficient and helpful communication.

---

**Ready to try Shona AI?** Start chatting today! �