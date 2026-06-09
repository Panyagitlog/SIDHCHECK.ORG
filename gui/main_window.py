import customtkinter as ctk
from tkinter import filedialog, messagebox
import threading
import subprocess
import time
import os
from datetime import datetime

from core.process_excel import process_excel


class MainWindow(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("SIDH Candidate Checker")
        self.geometry("1000x700")

        self.input_excel = ""
        self.output_folder = ""

        self.create_widgets()

    def create_widgets(self):

        title = ctk.CTkLabel(
            self,
            text="SIDH Candidate Checker",
            font=("Arial", 24, "bold")
        )
        title.pack(pady=20)

        # Input Excel

        input_frame = ctk.CTkFrame(self)
        input_frame.pack(fill="x", padx=20, pady=10)

        self.input_label = ctk.CTkLabel(
            input_frame,
            text="No Input Excel Selected"
        )
        self.input_label.pack(side="left", padx=10)

        ctk.CTkButton(
            input_frame,
            text="Browse Excel",
            command=self.select_input
        ).pack(side="right", padx=10)

        # Output Folder

        output_frame = ctk.CTkFrame(self)
        output_frame.pack(fill="x", padx=20, pady=10)

        self.output_label = ctk.CTkLabel(
            output_frame,
            text="No Output Folder Selected"
        )
        self.output_label.pack(side="left", padx=10)

        ctk.CTkButton(
            output_frame,
            text="Browse Folder",
            command=self.select_output_folder
        ).pack(side="right", padx=10)

        # Progress Bar

        self.progress = ctk.CTkProgressBar(self)
        self.progress.pack(
            fill="x",
            padx=20,
            pady=20
        )
        self.progress.set(0)

        self.status_label = ctk.CTkLabel(
            self,
            text="Ready"
        )
        self.status_label.pack()

        # Start Button

        self.start_button = ctk.CTkButton(
            self,
            text="START PROCESSING",
            height=45,
            command=self.start_processing
        )
        self.start_button.pack(pady=20)

        # Logs

        self.logs = ctk.CTkTextbox(
            self,
            height=350
        )

        self.logs.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )

    def log(self, text):

        self.logs.insert(
            "end",
            str(text) + "\n"
        )

        self.logs.see("end")

        self.update()

    def select_input(self):

        file_path = filedialog.askopenfilename(
            title="Select Input Excel",
            filetypes=[
                ("Excel Files", "*.xlsx")
            ]
        )

        if file_path:

            self.input_excel = file_path

            self.input_label.configure(
                text=file_path
            )

    def select_output_folder(self):

        folder = filedialog.askdirectory(
            title="Select Output Folder"
        )

        if folder:

            self.output_folder = folder

            self.output_label.configure(
                text=folder
            )

    def start_processing(self):

        if not self.input_excel:

            messagebox.showerror(
                "Error",
                "Please Select Input Excel"
            )

            return

        if not self.output_folder:

            messagebox.showerror(
                "Error",
                "Please Select Output Folder"
            )

            return

        self.start_button.configure(
            state="disabled"
        )

        threading.Thread(
            target=self.process,
            daemon=True
        ).start()

    def process(self):

        try:

            timestamp = datetime.now().strftime(
                "%Y%m%d_%H%M%S"
            )

            output_excel = os.path.join(
                self.output_folder,
                f"results_{timestamp}.xlsx"
            )

            self.log("")
            self.log("================================")
            self.log("JOB STARTED")
            self.log("================================")
            self.log(f"Input : {self.input_excel}")
            self.log(f"Output: {output_excel}")

            self.progress.set(0.10)

            chrome_running = False

            try:

                import requests

                response = requests.get(
                    "http://127.0.0.1:9222/json/version",
                    timeout=2
                )

                if response.status_code == 200:
                    chrome_running = True

            except:
                pass

            if chrome_running:

                self.log(
                    "Chrome Debug Already Running"
                )

            else:

                self.log(
                    "Starting Chrome Debug..."
                )

                subprocess.Popen([
                    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                    "--remote-debugging-port=9222",
                    "--user-data-dir=C:\ChromeDebug"
                ])

                time.sleep(5)

                self.log(
                    "Chrome Started"
                )

            self.progress.set(0.30)

            messagebox.showinfo(
                "SIDH Login",
                "Login SIDH and open Enrollment Page.\n\nThen click OK."
            )

            self.progress.set(0.50)

            self.log("SIDH Ready")
            self.log("Starting Excel Processing...")

            self.progress.set(0.70)

            process_excel(
                self.input_excel,
                output_excel,
                self.log
            )

            self.progress.set(1)

            self.status_label.configure(
                text="Completed"
            )

            self.log("")
            self.log("================================")
            self.log("PROCESS COMPLETED")
            self.log("================================")
            self.log(f"Output Saved : {output_excel}")

            self.start_button.configure(
                state="normal"
            )

            messagebox.showinfo(
                "Success",
                f"Processing Completed\n\n{output_excel}"
            )

        except Exception as e:

            self.start_button.configure(
                state="normal"
            )

            messagebox.showerror(
                "Error",
                str(e)
            )