import tkinter as tk
from tkinter import filedialog
import subprocess

class YTDLPFrame(tk.Frame):
    """Frame for the yt-dlp functionality."""

    def __init__(self, container):
        super().__init__(container)

        # URL Entry
        self.url_label = tk.Label(self, text="Video URL:")
        self.url_label.pack()
        self.url_entry = tk.Entry(self, width=50)
        self.url_entry.pack()

        # Folder Selection
        self.folder_path = tk.StringVar()
        self.folder_label = tk.Label(self, text="Select save path:")
        self.folder_label.pack()
        self.folder_entry = tk.Entry(self, textvariable=self.folder_path, width=50)
        self.folder_entry.pack()
        self.browse_button = tk.Button(self, text="Browse", command=self.select_folder)
        self.browse_button.pack()

        # Download Button
        self.download_button = tk.Button(self, text="Download", command=self.download_video)
        self.download_button.pack()

        # Status Label
        self.status_label = tk.Label(self, text="")
        self.status_label.pack()

    def download_video(self):
        """Download the video using yt-dlp."""
        url = self.url_entry.get()
        save_path = self.folder_path.get()
        if not url or not save_path:
            self.status_label.config(text="Please enter a URL and select a save path.")
            return

        command = f'yt-dlp "{url}" -o "{save_path}/%(title)s.%(ext)s" -i --all-subs'
        try:
            subprocess.run(command, check=True, shell=True)
            self.status_label.config(text="Download completed.")
        except subprocess.CalledProcessError:
            self.status_label.config(text="Download failed.")

    def select_folder(self):
        """Select a folder to save the video."""
        folder_selected = filedialog.askdirectory()
        self.folder_path.set(folder_selected)
