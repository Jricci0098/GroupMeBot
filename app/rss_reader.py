import requests
from bs4 import BeautifulSoup

def get_nab_daily_reading():
    try:
        url = "https://bible.usccb.org/readings/calendar.rss"
        res = requests.get(url, timeout=10)
        soup = BeautifulSoup(res.content, 'xml')

        first_item = soup.find('item')
        title = first_item.title.text.strip()
        description_html = first_item.description.text.strip()
        description = BeautifulSoup(description_html, 'html.parser').get_text(separator='\n')

        return f"*{title}*\n\n{description}"
    except Exception:
        return "📖 Unable to fetch today's reading from USCCB."
