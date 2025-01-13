import requests
from bs4 import BeautifulSoup


def scrape_book_content(url: str):
    try:
        # Shift-JISでエンコードされたHTMLを取得
        response = requests.get(url)
        response.encoding = "shift_jis"
        print("url:", url)
        # BeautifulSoupでHTMLをパース
        soup = BeautifulSoup(response.text, "html.parser")

        text = soup.find("div", {"class": "main_text"}).text
        return text
    except Exception as e:
        print(f"Error scraping book content: {e}")
        return None
