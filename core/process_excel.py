from difflib import SequenceMatcher

from core.excel_handler import ExcelHandler
from core.browser import BrowserManager
from core.candidate_scraper import CandidateScraper


def process_excel(
    input_excel,
    output_excel,
    log_callback=None
):

    excel = ExcelHandler(input_excel)

    browser = BrowserManager()

    browser.connect()

    page = browser.get_page()

    scraper = CandidateScraper(page)

    total = excel.get_total_rows()

    if log_callback:
        log_callback(f"Total Records : {total}")

    for i in range(total):

        try:

            row = excel.get_row(i)

            excel_name = row["name"].strip()
            mobile = row["mobile"].strip()

            if not mobile:

                excel.update_row(
                    i,
                    "",
                    "",
                    "MOBILE EMPTY"
                )

                continue

            if log_callback:
                log_callback(
                    f"[{i+1}/{total}] Searching {mobile}"
                )

            result = scraper.search_mobile(
                mobile
            )

            if result["found"]:

                can_id = result["can_id"]
                sidh_name = result["sidh_name"]

                similarity = SequenceMatcher(
                    None,
                    excel_name.upper(),
                    sidh_name.upper()
                ).ratio()

                if similarity >= 0.85:

                    status = "MATCH"

                else:

                    status = "MISMATCH"

                excel.update_row(
                    i,
                    can_id,
                    sidh_name,
                    status
                )

                if log_callback:

                    log_callback(
                        f"FOUND -> {can_id} | {sidh_name} | {status} | Similarity: {round(similarity * 100, 2)}%"
                    )

            else:

                excel.update_row(
                    i,
                    "",
                    "",
                    "NOT REGISTERED"
                )

                if log_callback:
                    log_callback(
                        "NOT REGISTERED"
                    )

            # Save after every row
            excel.save(output_excel)

        except Exception as e:

            excel.update_row(
                i,
                "",
                "",
                f"ERROR"
            )

            excel.save(output_excel)

            if log_callback:
                log_callback(
                    f"ERROR ROW {i+1} : {str(e)}"
                )

    excel.save(output_excel)

    if log_callback:

        log_callback("")
        log_callback("================================")
        log_callback("PROCESS COMPLETED")
        log_callback("================================")
        log_callback(f"Output File : {output_excel}")