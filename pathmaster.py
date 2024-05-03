import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import os
import shutil
import threading
import json
import logging

# Setup logging
logging.basicConfig(filename='path_master.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class PathMasterApp:
    def __init__(self, master):
        self.master = master
        master.title("Path Master")
        
        # Load settings
        self.settings = self.load_settings()

        # GUI setup
        self.setup_gui()

    def setup_gui(self):
        # Input Section
        input_frame = tk.Frame(self.master)
        input_frame.pack(padx=10, pady=10)

        tk.Label(input_frame, text="Enter Path:").grid(row=0, column=0)
        self.input_field = tk.Entry(input_frame, width=40)
        self.input_field.grid(row=0, column=1)
        tk.Button(input_frame, text="Browse", command=self.browse_path).grid(row=0, column=2)

        # Action Buttons Frame
        actions_frame = tk.Frame(self.master)
        actions_frame.pack(pady=10)

        tk.Button(actions_frame, text="Analyze", width=12, bg="lightblue", command=lambda: self.start_thread(self.get_path_info)).grid(row=0, column=0, padx=5)
        tk.Button(actions_frame, text="List Contents", width=12, bg="lightgreen", command=lambda: self.start_thread(self.list_directory)).grid(row=0, column=1, padx=5) 
        tk.Button(actions_frame, text="Create Directory", width=12, bg="lightyellow", command=lambda: self.start_thread(self.create_directory)).grid(row=0, column=2, padx=5)
        tk.Button(actions_frame, text="Copy File", width=12, command=lambda: self.start_thread(self.copy_file)).grid(row=1, column=0, padx=5, pady=5)

        # Status Bar
        self.status_bar = tk.Label(self.master, text="Ready", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def browse_path(self):
        path = filedialog.askdirectory()
        self.input_field.delete(0, tk.END)
        self.input_field.insert(0, path)

    def get_path_info(self):
        path = self.input_field.get()
        self.update_status("Analyzing...")
        if not os.path.exists(path):
            messagebox.showerror("Error", "Path does not exist.")
            self.update_status("Ready")
            return
        
        details = (
            f"Absolute Path: {os.path.abspath(path)}\n"
            f"Directory Name: {os.path.dirname(path)}\n"
            f"Base Name: {os.path.basename(path)}\n"
            f"Is File: {os.path.isfile(path)}\n"
            f"Is Directory: {os.path.isdir(path)}\n"
            f"Exists: {os.path.exists(path)}"
        )
        messagebox.showinfo("Path Details", details)
        self.update_status("Analysis complete!")

    def list_directory(self):
        path = self.input_field.get()
        self.update_status("Listing contents...")
        if os.path.isdir(path):
            contents = os.listdir(path)
            content_str = "Contents:\n" + "\n".join(contents) if contents else "<Directory is empty>"
            messagebox.showinfo("Directory Contents", content_str)
        else:
            messagebox.showerror("Error", "Path is not a directory.")
        self.update_status("Ready")

    def create_directory(self):
        path = self.input_field.get()
        self.update_status("Creating directory...")
        try:
            os.makedirs(path, exist_ok=True)
            messagebox.showinfo("Success", "Directory created or already exists.")
        except OSError as e:
            messagebox.showerror("Error", f"Directory creation failed: {e}")
        self.update_status("Ready")

    def copy_file(self):
        src = self.input_field.get()
        dst = filedialog.askdirectory(title="Select destination directory")
        if not dst:
            self.update_status("Copy cancelled.")
            return
        dst = os.path.join(dst, os.path.basename(src))
        self.update_status("Copying file...")
        try:
            shutil.copy(src, dst)
            messagebox.showinfo("Success", f"File copied from '{src}' to '{dst}'")
        except shutil.SameFileError:
            messagebox.showerror("Error", "Source and destination are the same file.")
        except OSError as e:
            messagebox.showerror("Error", f"Error copying file: {e}")
        self.update_status("Ready")

    def update_status(self, text):
        self.status_bar.config(text=text)
        self.master.update_idletasks()

    def start_thread(self, target):
        thread = threading.Thread(target=target)
        thread.start()

    def load_settings(self):
        try:
            with open("settings.json", "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def save_settings(self):
        with open("settings.json", "w") as f:
            json.dump(self.settings, f)

if __name__ == "__main__":
    root = tk.Tk()
    app = PathMasterApp(root)
    root.mainloop()
