import requests
import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

CHAT_ID = os.getenv("CHAT_ID")
import re


def clean_caption(text):

    if not text:
        return ""

    # Remove markdown symbols
    text = re.sub(r"\*+", "", text)
    text = re.sub(r"_+", "", text)
    text = re.sub(r"`+", "", text)

    # Remove excessive empty lines
    text = re.sub(r"\n\s*\n", "\n\n", text)

    return text.strip()


def send_message(text):

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    data = {

        "chat_id": CHAT_ID,
        "text": text

    }

    response = requests.post(
        url,
        data=data
    )

    return response.json()

def send_photo(photo_path, caption):

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"

    with open(photo_path, "rb") as photo:

        files = {
            "photo": photo
        }

        data = {

            "chat_id": CHAT_ID,
            "caption": caption

        }

        response = requests.post(
            url,
            data=data,
            files=files
        )

    return response.json()