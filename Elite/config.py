import os
from dotenv import load_dotenv
load_dotenv()

# Telegram
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Odds & Stats
ODDSAPI_KEY = os.getenv("ODDSAPI_KEY")
API_FOOTBALL_KEY = os.getenv("API_FOOTBALL_KEY")
API_BASKETBALL_KEY = os.getenv("API_BASKETBALL_KEY")

# News & Injuries
NEWSAPI_KEY = os.getenv("NEWSAPI_KEY")
X_BEARER_TOKEN = os.getenv("X_BEARER_TOKEN")

# Bot settings
CONFIDENCE_ALERT_MIN = int(os.getenv("CONFIDENCE_ALERT_MIN", 90))
POLL_SECONDS = int(os.getenv("POLL_SECONDS", 60))
