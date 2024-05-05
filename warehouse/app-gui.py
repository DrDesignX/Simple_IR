import tkinter as tk
from tkinter import filedialog
import os

def browse_for_folder():
  global input_folder_path
  input_folder_path.set(tk.filedialog.askdirectory())
  folder_name_label.config(text=f"Input Folder: {input_folder_path.get()}")

def process_files(log_area):
  if not input_folder_path.get():
    log_area.insert(tk.END, "Error: Please select an input folder.\n")
    return

  log_area.insert(tk.END, f"Processing files in: {input_folder_path.get()}\n")
  for filename in os.listdir(input_folder_path.get()):
    log_area.insert(tk.END, f"- Processing file: {filename}\n")
  log_area.insert(tk.END, "Processing completed.\n")

# Main window
root = tk.Tk()
root.title("File Processor")

# Input folder selection
input_folder_path = tk.StringVar()
folder_name_label = tk.Label(root, text="Input Folder:")
folder_name_label.pack()

browse_button = tk.Button(root, text="Browse", command=browse_for_folder)
browse_button.pack()

# Log area
log_area = tk.Text(root, height=10, width=50)
log_area.pack()

def add_custom_log(log_area, message, tag=None):
    log_area.insert(tk.END, message + "\n", tag)

# Process button
process_button = tk.Button(root, text="Process Files", command=lambda: process_files(log_area))
process_button.pack()
root.mainloop()


