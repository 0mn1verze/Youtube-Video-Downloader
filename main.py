import os
import sys
from pathlib import Path

import tkinter as tk
from tkinter.filedialog import asksaveasfile
import customtkinter as ctk

from pytube import YouTube

# System Settings
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

res_selected = False

# Download Function
def startDownload():
    global res_selected
    ytLink = link.get()

    finish.pack(padx=10, pady=10)

    resolution.pack_forget()
    percentage.pack_forget()
    progress.pack_forget()

    try:

        yt = YouTube(ytLink, on_progress_callback=on_progress)
        if not res_selected:
            btn.configure(text="Find Video")
            btn.update()

            finish.configure(text=f"Video title - {yt.title}", text_color="white")
            finish.update()

            res = list(filter(lambda x: x is not None, set([streams.resolution for streams in yt.streams])))
            res.sort(reverse=True)

            resolution.configure(values=["Select Resolution"] + res)
            resolution.set("Select Resolution")
            resolution.pack()

            btn.configure(text="Download Video")
            btn.update()

            res_selected = True
        else:
            percentage.pack()
            progress.pack()

            res = resolution.get()

            if res == "Select Resolution":
                finish.configure(text="Defaulting to highest resolution...")
                vid = yt.streams.get_highest_resolution()
            else:
                vid = yt.streams.get_by_resolution(res)

            finish.configure(text="Getting file name from user...")
            finish.update()

            f = asksaveasfile(initialfile="video.mp4", initialdir=str(Path.home() / "Downloads"), defaultextension=".mp4", filetypes=[("All Files","*.*"),("Video Files","*.mp4")])

            fname = os.path.basename(f.name)
            fpath = os.path.dirname(f.name)

            finish.configure(text="Downloading file...")
            finish.update()

            vid.download(output_path=fpath, filename=fname)

            finish.configure(text="Download Complete!")


            res_selected = False

            link.delete(0, last_index=len(link.get()))
            link.update()
            btn.configure(text="Find Video")
            btn.update()
            percentage.pack_forget()
            progress.pack_forget()

    except Exception as e:
        finish.configure(text=f"Error: {str(e)}", text_color="red")

        link.delete(0, last_index=len(link.get()))
        link.update()
        btn.configure(text="Find Video")
        btn.update()
        percentage.pack_forget()
        progress.pack_forget()
    finish.update()
    

def on_progress(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    p = bytes_downloaded / total_size * 100

    # Update percentage
    percentage.configure(text=f"{int(p)}%")
    percentage.update()

    # Update progress bar
    progress.set(p / 100)
    progress.update()

def get_path(file_name):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, file_name)
    else:
        return file_name

# Main program
app = ctk.CTk()
app.geometry("500x380")
app.minsize(500, 380)
app.maxsize(1080, 720)
app.title("Youtube Video Downloader")
app.iconbitmap(get_path("icon.ico"))

# Add UI Elements
title = ctk.CTkLabel(app, text="Insert a youtube link to download a video!")
title.pack(padx=10, pady=10)

# Add url entry
url_var = tk.StringVar()
link = ctk.CTkEntry(app, width=350, height=40, placeholder_text="Enter link", textvariable=url_var)
link.pack()

# Download Button
btn = ctk.CTkButton(app, text="Find Video", command=startDownload)
btn.pack(padx=10, pady=10)

# Resolution selection
res = ctk.StringVar()
resolution = ctk.CTkComboBox(app, variable=res)

# Percentage 
percentage = ctk.CTkLabel(app, text="0%")

# Progress bar
progress = ctk.CTkProgressBar(app, width=400)
progress.set(0)

# Finish label
finish = ctk.CTkLabel(app, text="")

# Run App
app.mainloop()