from os import getenv

# Telegram Bot Configuration
BOT_TOKEN = getenv("BOT_TOKEN", "8340954149:AAGu8zs7zJMH_yoJJL8cP_Sqw_mv923VkUI")
BOT_ID = getenv("BOT_ID", "8340954149")  # token first 10 digits

# MongoDB Configuration (for learning system) - optional
MONGO_URL = getenv("MONGO_URL", "")

# Optional flags
# Set to true to run without MongoDB (lightweight mode - recommended)
DISABLE_MONGO = getenv("DISABLE_MONGO", "true").lower() in ("1", "true", "yes")

# Ollama (local LLM) Configuration
# Your personal AI girlfriend powered by local Llama model
OLLAMA_ENABLED = getenv("OLLAMA_ENABLED", "true").lower() in ("1", "true", "yes")
OLLAMA_HOST = getenv("OLLAMA_HOST", "http://127.0.0.1:11434")
OLLAMA_MODEL = getenv("OLLAMA_MODEL", "llama3.2:3b")

# Bot Settings
BOT_NAME = "Shona - Your AI Girlfriend"
DEFAULT_RESPONSE = "Sorry cutie, I didn't quite get that. Try asking me differently? 💕"