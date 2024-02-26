import tkinter as tk
from tkinter import ttk, filedialog
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

        # Define options for Quality and Format Dropdowns
        self.quality_options = ['1080p', '720p', '480p', '360p', '240p']
        self.format_options = ['mp4', 'webm', 'flv']

        # Frame for Video Options
        self.video_options_frame = tk.LabelFrame(self, text="Video Options", padx=10, pady=10)
        self.video_options_frame.pack(padx=10, pady=10, fill="both")

        # Quality Dropdown within Video Options Frame
        self.quality_label = tk.Label(self.video_options_frame, text="Choose quality")
        self.quality_label.pack(side=tk.TOP, anchor="w")
        self.quality_combobox = ttk.Combobox(self.video_options_frame, values=self.quality_options)
        self.quality_combobox.pack(side=tk.TOP, anchor="w")

        # Format Dropdown within Video Options Frame
        self.format_label = tk.Label(self.video_options_frame, text="Choose Format:")
        self.format_label.pack(side=tk.TOP, anchor="w")
        self.format_combobox = ttk.Combobox(self.video_options_frame, values=self.format_options)
        self.format_combobox.pack(side=tk.TOP, anchor="w")

        # Geo-Restriction Checkbox
        self.geo_restriction_var = tk.BooleanVar()
        self.geo_restriction_checkbox = tk.Checkbutton(self.video_options_frame, text="Bypass Geo-restrictions", variable=self.geo_restriction_var)
        self.geo_restriction_checkbox.pack(side=tk.TOP, anchor="w")

        # Checkbox for Subtitles within Video Options Frame
        self.subtitles_var = tk.BooleanVar(value=False)
        self.subtitles_checkbox = tk.Checkbutton(self.video_options_frame, text="Download Subtitles (--write-subs)", variable=self.subtitles_var)
        self.subtitles_checkbox.pack(side=tk.TOP, anchor="w")

        # LabelFrame for 'Audio Only' and lydformatindstillinger
        self.audio_options_frame = tk.LabelFrame(self, text="Options for Audio Only", padx=10, pady=10)
        self.audio_options_frame.pack(padx=10, pady=10, fill="both")

        # Checkbox for 'Audio Only'
        self.audio_only_var = tk.BooleanVar(value=False)
        self.audio_only_checkbox = tk.Checkbutton(self.audio_options_frame, text="Download Audio Only", variable=self.audio_only_var, command=self.toggle_audio_options)
        self.audio_only_checkbox.pack(side=tk.LEFT)

        # Combobox for choose audio format
        self.audio_format_label = tk.Label(self.audio_options_frame, text="Format:")
        self.audio_format_label.pack(side=tk.LEFT)
        self.audio_format_options = ['mp3', 'aac', 'ogg', 'wav', 'flac']
        self.audio_format_combobox = ttk.Combobox(self.audio_options_frame, values=self.audio_format_options, state='disabled')
        self.audio_format_combobox.pack(side=tk.LEFT)

        # Download Button
        self.download_button = tk.Button(self, text="Download", command=self.download_video)
        self.download_button.pack()

        # Status Label
        self.status_label = tk.Label(self, text="")
        self.status_label.pack()
    
    def toggle_audio_options(self):
        # Activate or deactivate combobox based on checkbox-condition
        if self.audio_only_var.get():
            self.audio_format_combobox.config(state='normal')
        else:
            self.audio_format_combobox.config(state='disabled')

    def download_video(self):
        """Download the video using yt-dlp."""
        url = self.url_entry.get()
        save_path = self.folder_path.get()
        quality = self.quality_combobox.get()
        format_option = self.format_combobox.get()

        if not url or not save_path:
            self.status_label.config(text="Please enter a URL and select a save path.")
            return

        # Basic yt-dlp command
        command = f'yt-dlp "{url}" -o "{save_path}/%(title)s.%(ext)s"'

        # Add quality and format settings
        if quality:
            command += f" -f {quality}"
        if format_option:
            command += f" --recode-video {format_option}"

        # Add subtitle flag based on checkbox
        if self.subtitles_var.get():
            command += " --write-subs"
        else:
            command += " --no-write-subs"
        
        # Check for 'Audio Only'
        if self.audio_only_var.get():
            command += " -x"  # '-x' flag for extract audio
            audio_format = self.audio_format_combobox.get()
            if audio_format:
                command += f" --audio-format {audio_format}"

        try:
            subprocess.run(command, check=True, shell=True)
            self.status_label.config(text="Download completed.")
        except subprocess.CalledProcessError:
            self.status_label.config(text="Download failed.")

    def select_folder(self):
        """Select a folder to save the video."""
        folder_selected = filedialog.askdirectory()
        self.folder_path.set(folder_selected)
