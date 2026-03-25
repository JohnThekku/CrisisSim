import os
from newsapi import NewsApiClient
from dotenv import load_dotenv

load_dotenv()


def fetch_headlines(query: str, max_articles: int = 10) -> list[dict]:
    api_key = os.getenv("NEWSAPI_KEY")

    if not api_key:
        raise ValueError("NEWSAPI_KEY not found in .env file")

    newsapi = NewsApiClient(api_key=api_key)

    response = newsapi.get_everything(
        q=query,
        language="en",
        sort_by="publishedAt",
        page_size=max_articles,
    )

    articles = response.get("articles", [])

    headlines = []
    for article in articles:
        if article.get("title") and article.get("description"):
            headlines.append({
                "title": article["title"],
                "description": article["description"],
                "source": article["source"]["name"],
                "published": article["publishedAt"],
            })

    return headlines


def format_headlines_for_prompt(headlines: list[dict]) -> str:
    if not headlines:
        return "No recent headlines found."

    formatted = []
    for i, article in enumerate(headlines, 1):
        formatted.append(
            f"{i}. [{article['source']}] {article['title']}\n"
            f"   {article['description']}"
        )

    return "\n\n".join(formatted)