import requests
from bs4 import BeautifulSoup


def web_search(query):
    try:
        url = "https://html.duckduckgo.com/html/"

        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        response = requests.post(
            url,
            data={"q": query},
            headers=headers,
            timeout=10
        )

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        results = []

        for item in soup.select(".result"):
            title = item.select_one(".result__a")
            snippet = item.select_one(".result__snippet")

            if title:
                name = title.get_text(" ", strip=True)
                link = title.get("href")

                text = ""

                if snippet:
                    text = snippet.get_text(" ", strip=True)

                results.append(
                    f"{name}\n{link}\n{text}"
                )

        if not results:
            return "No web results found."

        return "\n\n".join(results[:5])

    except Exception as e:
        return f"Web error: {e}"
