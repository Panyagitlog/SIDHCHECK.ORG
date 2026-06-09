import pandas as pd


class ExcelHandler:

    def __init__(self, excel_path):

        self.excel_path = excel_path

        self.df = pd.read_excel(
            excel_path,
            dtype=str
        )

        self.df = self.df.fillna("")

        if "CAN ID" not in self.df.columns:
            self.df["CAN ID"] = ""

        if "SIDH Name" not in self.df.columns:
            self.df["SIDH Name"] = ""

        if "Status" not in self.df.columns:
            self.df["Status"] = ""

    def get_total_rows(self):

        return len(self.df)

    def get_row(self, index):

        return {
            "name": str(
                self.df.at[index, "Name"]
            ).strip(),

            "mobile": str(
                self.df.at[index, "Mobile No"]
            ).strip()
        }

    def update_row(
        self,
        index,
        can_id,
        sidh_name,
        status
    ):

        self.df.loc[index, "CAN ID"] = str(can_id)
        self.df.loc[index, "SIDH Name"] = str(sidh_name)
        self.df.loc[index, "Status"] = str(status)

    def save(self, output_file):

        self.df.to_excel(
            output_file,
            index=False
        )