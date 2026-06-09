import requests
from playwright.sync_api import sync_playwright


class BrowserManager:

    def __init__(self):
        self.browser = None
        self.page = None

    def chrome_running(self):

        try:

            response = requests.get(
                "http://127.0.0.1:9222/json/version",
                timeout=2
            )

            return response.status_code == 200

        except:

            return False

    def connect(self):

        playwright = sync_playwright().start()

        self.browser = playwright.chromium.connect_over_cdp(
            "http://127.0.0.1:9222"
        )

        return self.browser

    def find_sidh_page(self):

        if not self.browser:
            self.connect()

        for context in self.browser.contexts:

            for page in context.pages:

                if "view-batch-details" in page.url:

                    self.page = page

                    print("FOUND SIDH PAGE")
                    print(page.url)

                    return page

        return None

    def get_page(self):

        page = self.find_sidh_page()

        if page is None:

            raise Exception(
                "SIDH Enrollment Page Not Found"
            )

        page.bring_to_front()

        return page