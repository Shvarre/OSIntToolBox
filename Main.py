import tkinter as tk
from tkinter import ttk
from YTDLPFrame import YTDLPFrame
from ExifToolFrame import ExifToolFrame

# Create the main window
root = tk.Tk()
root.title("OSINT Toolkit")

# Create the tab control
tab_control = ttk.Notebook(root)

# Create the yt-dlp tab
yt_dlp_tab = YTDLPFrame(tab_control)
tab_control.add(yt_dlp_tab, text='Yt-dlp')

# Create the ExifTool tab
exif_tool_tab = ExifToolFrame(tab_control)
tab_control.add(exif_tool_tab, text='ExifTool')

# Show the tab control
tab_control.pack(expand=1, fill='both')

# Run the GUI
root.mainloop()
