import re
import time


class CandidateScraper:

    def __init__(self, page):
        self.page = page

    def search_mobile(self, mobile_no):

        try:

            self.page.bring_to_front()

            # Clear mobile field

            mobile_input = self.page.get_by_placeholder(
                "Search by Mobile No"
            )

            mobile_input.click()

            self.page.keyboard.press("Control+A")
            self.page.keyboard.press("Backspace")

            mobile_input.fill(
                str(mobile_no)
            )

            # Click Apply

            self.page.get_by_role(
                "button",
                name="APPLY"
            ).click()

            print(f"Searching : {mobile_no}")

            time.sleep(5)

            tables = self.page.locator("table")

            # Search all tables

            for i in range(tables.count()):

                try:

                    table_text = tables.nth(i).inner_text()

                    match = re.search(
                        r"(CAN_\d+)\s+([A-Za-z .]+?)\s+(Male|Female)",
                        table_text,
                        re.IGNORECASE
                    )

                    if match:

                        can_id = match.group(1).strip()

                        sidh_name = match.group(2).strip()

                        print(
                            f"Found : {can_id} | {sidh_name}"
                        )

                        return {
                            "found": True,
                            "can_id": can_id,
                            "sidh_name": sidh_name
                        }

                except Exception:
                    pass

            print("Candidate Not Found")

            return {
                "found": False,
                "can_id": "",
                "sidh_name": ""
            }

        except Exception as e:

            print(
                f"Scraper Error : {e}"
            )

            return {
                "found": False,
                "can_id": "",
                "sidh_name": ""
            }