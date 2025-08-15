import os
from dotenv import load_dotenv
load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

ODDSAPI_KEY = os.getenv("ODDSAPI_KEY")
API_FOOTBALL_KEY = os.getenv("API_FOOTBALL_KEY")
API_BASKETBALL_KEY = os.getenv("API_BASKETBALL_KEY")

NEWSAPI_KEY = os.getenv("NEWSAPI_KEY")
X_BEARER_TOKEN = os.getenv("X_BEARER_TOKEN")

CONFIDENCE_ALERT_MIN = int(os.getenv("CONFIDENCE_ALERT_MIN", 90))
POLL_SECONDS = int(os.getenv("POLL_SECONDS", 60))
