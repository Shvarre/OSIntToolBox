import tkinter as tk
from tkinter import filedialog, scrolledtext
import subprocess

class ExifToolFrame(tk.Frame):
    """Frame for the ExifTool functionality."""

    def __init__(self, container):
        super().__init__(container)

        # File Selection
        self.file_label = tk.Label(self, text="Select a file to view EXIF data:")
        self.file_label.pack()
        self.file_path = tk.StringVar()
        self.file_entry = tk.Entry(self, textvariable=self.file_path, width=50)
        self.file_entry.pack()
        self.file_browse_button = tk.Button(self, text="Browse", command=self.select_file)
        self.file_browse_button.pack()

        # Display EXIF Data
        self.exif_output = scrolledtext.ScrolledText(self, wrap=tk.WORD, height=10)
        self.exif_output.pack(pady=5)

        # Remove EXIF Data Button
        self.remove_exif_button = tk.Button(self, text="Remove EXIF Data", command=self.remove_exif_data)
        self.remove_exif_button.pack()

    def select_file(self):
        """Select a file to process."""
        file_selected = filedialog.askopenfilename()
        self.file_path.set(file_selected)
        self.display_exif_data(file_selected)

    def display_exif_data(self, file_path):
        """Display the EXIF data of the selected file."""
        if file_path:
            command = f'exiftool "{file_path}"'
            result = subprocess.run(command, shell=True, text=True, capture_output=True)
            self.exif_output.delete('1.0', tk.END)
            self.exif_output.insert(tk.INSERT, result.stdout)

    def remove_exif_data(self):
        """Remove all EXIF data from the selected file."""
        file_path = self.file_path.get()
        if file_path:
            command = f'exiftool -all= "{file_path}"'
            subprocess.run(command, shell=True)
            self.exif_output.delete('1.0', tk.END)
            self.exif_output.insert(tk.INSERT, "EXIF data removed.")
