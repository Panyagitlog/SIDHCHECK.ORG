from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp("http://127.0.0.1:9222")

    print("Connected!")

    for context_index, context in enumerate(browser.contexts):
        print(f"\nContext {context_index}")

        for page_index, page in enumerate(context.pages):
            print(f"\nTAB {page_index}")
            print("URL :", page.url)

            try:
                print("TITLE :", page.title())
            except:
                print("TITLE : Unable to read")