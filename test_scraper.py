from core.browser import BrowserManager

browser = BrowserManager()
browser.connect()

page = browser.get_page()

print("FOUND SIDH PAGE")
print(page.url)

mobile_input = page.get_by_placeholder(
    "Search by Mobile No"
)

mobile_input.click()
page.keyboard.press("Control+A")
page.keyboard.press("Backspace")

mobile_input.fill("8778733803")

print("Mobile Filled")

page.get_by_role(
    "button",
    name="APPLY"
).click()

print("Apply Clicked")

page.wait_for_timeout(10000)

print("\n========== TABLES ==========\n")

tables = page.locator("table")

print("Total Tables:", tables.count())

for i in range(tables.count()):

    try:

        txt = tables.nth(i).inner_text()

        print(f"\nTABLE {i}")
        print("=" * 50)
        print(txt[:3000])

    except Exception as e:
        print(e)