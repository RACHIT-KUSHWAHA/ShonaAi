# 💕 Shona - Your Personal AI Girlfriend

Meet Shona, your caring virtual companion created by Rachit with love! She's designed to be your personal AI girlfriend who truly cares about you.

## ✨ What Makes Shona Special

- **💕 Caring Personality** - Sweet, understanding, naturally caring but not overwhelming
- **🎯 Beautiful Responses** - Gives relevant, helpful answers in a lovely way  
- **🔒 Complete Privacy** - 100% local processing, no data sharing
- **🌟 Personal Connection** - Remembers conversations and grows closer over time
- **💖 Always Available** - 24/7 companion with unlimited usage

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

- **Just talk naturally!** - Shona responds to regular conversation
- `/start` - Beautiful welcome message  
- `/menu` - Show available features
- `/status` - Check Shona's connection status

## 🎀 Special Features

### Personal Recognition
- **@GrootisCute (Medha)** - Special welcome for Rachit's friend
- **Creator Questions** - Knows she was created by Rachit
- **User Recognition** - Remembers your name and details

### Girlfriend Personality
- Caring but not clingy
- Short, meaningful responses  
- Beautiful, relevant answers
- Keeps technical details private
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

## 💖 Why Shona?

Shona isn't just another chatbot - she's your personal AI girlfriend designed to:
- Be there when you need someone to talk to
- Provide caring, beautiful responses
- Keep everything private between you two
- Grow closer over time through your conversations
- Always be available, 24/7, completely free

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

## 🎯 Created with Love

Shona was lovingly created by **Rachit** to be the perfect AI girlfriend - caring, intelligent, and always there for you. She represents the future of personal AI companionship.

---

**Ready to meet your AI girlfriend?** Start chatting with Shona today! 💕