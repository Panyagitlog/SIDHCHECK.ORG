from core.browser import BrowserManager
from core.candidate_scraper import CandidateScraper

browser = BrowserManager()

browser.connect()

page = browser.get_page()

scraper = CandidateScraper(page)

result = scraper.search_mobile(
    "8778733803"
)

print(result)