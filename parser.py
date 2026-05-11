import re

OTT_KEYWORDS = [

    "ott",
    "streaming",
    "now streaming",
    "digital premiere",
    "watch now",
    "available on",
    "premieres on",
    "streaming on",
    "digital release",
    "now on"

]

OTT_PLATFORMS = [

    "netflix",
    "prime video",
    "hotstar",
    "disney+ hotstar",
    "sony liv",
    "sonyliv",
    "zee5",
    "aha"

]

MOVIE_KEYWORDS = [

    "trailer",
    "teaser",
    "first look",
    "motion poster",
    "in cinemas",
    "releasing",
    "worldwide release",
    "official trailer",
    "title poster",
    "announcement",
    "shooting",
    "release date",
    "coming soon",
    "glimpse",
    "update"

]
REMOVE_WORDS = [

    "Trailer",
    "Teaser",
    "FirstLook",
    "FirstLookLaunch",
    "MotionPoster",
    "OfficialTrailer",
    "Update"

]


def extract_movie_names(hashtags):

    movie_names = []

    for tag in hashtags:

        cleaned = tag

        for word in REMOVE_WORDS:

            cleaned = cleaned.replace(word, "")

        cleaned = cleaned.strip()

        if len(cleaned) > 2:
            movie_names.append(cleaned)

    return movie_names

def analyze_post(text):

    if not text:
        return {
            "is_movie_news": False,
            "is_ott_post": False,
            "hashtags": []
        }

    # CLEAN TEXT
    cleaned_text = (
        text.replace("*", "")
            .replace("_", "")
            .replace("`", "")
            .strip()
    )

    text_lower = cleaned_text.lower()

    # HASHTAGS
    hashtags = re.findall(r"#(\w+)", cleaned_text)

    # OTT CHECK
    has_platform = any(
        platform in text_lower
        for platform in OTT_PLATFORMS
    )

    has_ott_keyword = any(
        keyword in text_lower
        for keyword in OTT_KEYWORDS
    )

    is_ott = has_platform or has_ott_keyword

    # MOVIE NEWS CHECK
    has_movie_keyword = any(
        keyword in text_lower
        for keyword in MOVIE_KEYWORDS
    )

    is_movie_news = has_movie_keyword or len(hashtags) > 0
    movie_names = extract_movie_names(hashtags)

    return {

        "is_movie_news": is_movie_news,
        "is_ott_post": is_ott,
        "hashtags": hashtags,
        "movie_names": movie_names,
        "cleaned_text": cleaned_text
        

    }