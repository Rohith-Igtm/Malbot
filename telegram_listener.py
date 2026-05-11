from telethon import TelegramClient, events
from ai_parser import extract_movie_info
from tmdb import verify_malayalam_movie
from telethon.sessions import StringSession
import os

import asyncio

# =========================
# TELEGRAM API CREDENTIALS
# =========================

api_id = os.getenv("API_ID")
api_hash = os.getenv("API_HASH")

# =========================
# SOURCE CHANNEL
# =========================

CHANNEL_NAME = "streamingdue"

# =========================
# DESTINATION CHANNEL
# =========================

DESTINATION_CHANNEL = os.getenv("CHANNEL_LINK")

# =========================
# CREATE CLIENT
# =========================

session_string = os.getenv(
    "SESSION_STRING"
)

client = TelegramClient(
    StringSession(session_string),
    api_id,
    api_hash
)

# =========================
# FILTER KEYWORDS
# =========================

FILTER_KEYWORDS = [

    "#",
    "trailer",
    "teaser",
    "first look",
    "motion poster",
    "release",
    "releasing",
    "cinemas",
    "official"

]

# =========================
# REAL-TIME LISTENER
# =========================

@client.on(events.NewMessage(chats=CHANNEL_NAME))
async def handler(event):

    message = event.message

    print("\n" + "=" * 60)

    # =========================
    # SKIP EMPTY TEXT
    # =========================

    if not message.text:
        return

    # =========================
    # BASIC FILTERING
    # =========================

    text_lower = message.text.lower()

    if not any(
        keyword in text_lower
        for keyword in FILTER_KEYWORDS
    ):
        return

    # =========================
    # SHOW MESSAGE
    # =========================

    print("\nMESSAGE:")
    print(message.text)

    # =========================
    # AI ANALYSIS
    # =========================

    print("\n🤖 RUNNING AI ANALYSIS...")

    result = extract_movie_info(
        message.text
    )

    await asyncio.sleep(2)

    # =========================
    # HANDLE AI FAILURE
    # =========================

    if "error" in result:

        print("\n❌ AI PARSING FAILED")
        return

    # =========================
    # CHECK MOVIE NEWS
    # =========================

    if not result.get("is_movie_news"):

        print("\n❌ NOT MOVIE NEWS")
        return

    # =========================
    # GET MOVIE NAME
    # =========================

    movie_name = result.get("movie_name")

    if not movie_name:

        print("\n❌ NO MOVIE NAME FOUND")
        return

    print("\n🎬 MOVIE:")
    print(movie_name)

    # =========================
    # TMDB VERIFICATION
    # =========================

    print("\n🔍 VERIFYING WITH TMDB...")

    verified = verify_malayalam_movie(
        movie_name
    )

    await asyncio.sleep(2)

    if not verified:

        print("\n❌ NOT A MALAYALAM MOVIE")
        return

    print("\n✅ VERIFIED MALAYALAM MOVIE")

    # =========================
    # FORWARD ORIGINAL MESSAGE
    # =========================

    await client.forward_messages(
        DESTINATION_CHANNEL,
        message
    )

    print("\n📤 MESSAGE FORWARDED")

    print("=" * 60)

# =========================
# START CLIENT
# =========================

print("\n🚀 Malayalam Movie Agent Running...")

client.connect()
client.run_until_disconnected()