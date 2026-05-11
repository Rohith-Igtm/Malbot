from groq import Groq
import json
import os

from dotenv import load_dotenv

load_dotenv()
client = Groq(

    api_key=os.getenv("GROQ_API_KEY")

)


def extract_movie_info(text):

    prompt = f"""
You are an AI movie news extractor.

Analyze this Telegram post and return ONLY valid JSON.

Rules:
- Identify Malayalam movie news
- Extract movie name if present
- Detect OTT related news
- No explanations
- No markdown

Return format:

{{
  "movie_name": "",
  "is_movie_news": true,
  "is_ott_news": false
}}

POST:
{text}
"""

    try:

        completion = client.chat.completions.create(

            model="llama-3.1-8b-instant",

            messages=[

                {
                    "role": "user",
                    "content": prompt
                }

            ],

            temperature=0

        )

        result = completion.choices[0].message.content

        parsed = json.loads(result)

        return parsed

    except Exception as e:

        return {

            "error": str(e)

        }