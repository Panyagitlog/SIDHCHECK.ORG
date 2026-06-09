import re
import time


class CandidateScraper:

    def __init__(self, page):
        self.page = page

    def search_mobile(self, mobile_no):

        try:

            self.page.bring_to_front()

            mobile_input = self.page.get_by_placeholder(
                "Search by Mobile No"
            )

            mobile_input.click()
            mobile_input.fill("")

            mobile_input.fill(
                str(mobile_no)
            )

            self.page.get_by_role(
                "button",
                name="APPLY"
            ).click()

            time.sleep(4)

            body_text = self.page.locator(
                "body"
            ).inner_text()

            match = re.search(
                r"(CAN_\d+)\s+([A-Za-z .]+)",
                body_text
            )

            if match:

                can_id = match.group(1).strip()

                sidh_name = match.group(2).strip()

                return {
                    "found": True,
                    "can_id": can_id,
                    "sidh_name": sidh_name
                }

            return {
                "found": False,
                "can_id": "",
                "sidh_name": ""
            }

        except Exception as e:

            print(e)

            return {
                "found": False,
                "can_id": "",
                "sidh_name": ""
            }