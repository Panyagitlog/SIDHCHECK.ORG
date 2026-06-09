from playwright.sync_api import sync_playwright

with sync_playwright() as p:

    # Connect to Chrome Debug
    browser = p.chromium.connect_over_cdp(
        "http://127.0.0.1:9222"
    )

    target_page = None

    # Find SIDH Enrollment Page
    for context in browser.contexts:
        for page in context.pages:
            if "view-batch-details" in page.url:
                target_page = page
                break

    if not target_page:
        print("SIDH Page Not Found")
        exit()

    print("Found SIDH Page")
    print(target_page.url)

    # Bring page to front
    target_page.bring_to_front()

    # Enter Mobile Number
    mobile_input = target_page.get_by_placeholder(
        "Search by Mobile No"
    )

    mobile_input.fill("8778733803")  # Change mobile number here

    print("Mobile Number Filled")

    # Click APPLY
    target_page.get_by_role(
        "button",
        name="APPLY"
    ).click()

    print("Apply Clicked")

    # Wait for results
    target_page.wait_for_timeout(5000)

    # Read all visible page text
    text = target_page.locator("body").inner_text()

    # Save page text for debugging
    with open(
        "output/result_text.txt",
        "w",
        encoding="utf-8"
    ) as f:
        f.write(text)

    can_id = ""
    candidate_name = ""

    # Search candidate row
    for line in text.splitlines():

        line = line.strip()

        if line.startswith("CAN_"):

            print("\nRAW LINE:")
            print(line)

            can_id = line.split()[0]

            remaining = line.replace(can_id, "").strip()

            for gender in ["Male", "Female", "Other"]:

                if gender in remaining:

                    candidate_name = (
                        remaining.split(gender)[0]
                        .strip()
                    )

                    break

            break

    print("\n===================")

    if can_id:

        print("FOUND CANDIDATE")
        print("===================")
        print("CAN ID :", can_id)
        print("NAME   :", candidate_name)

    else:

        print("NOT REGISTERED")
        print("===================")

    # Save Screenshot
    target_page.screenshot(
        path="output/result.png",
        full_page=True
    )

    print("\nScreenshot Saved")
    print("Text Saved -> output/result_text.txt")