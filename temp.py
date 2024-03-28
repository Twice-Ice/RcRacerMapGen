import tkinter as tk
from tkinter import filedialog

def open_file():
    """
    Opens a file dialog that allows the user to select a file for opening.
    Returns the path of the selected file.
    """
    root = tk.Tk()
    root.withdraw()  # Hide the Tkinter root window

    # Set options for the open file dialog
    options = {
        'defaultextension': '.txt',  # Default file extension
        'filetypes': [('All files', '*.*')],  # Allowed file types
        'initialdir': 'C:\\',  # Initial directory
        'title': 'Select file to open'  # Dialog title
    }

    # Open the dialog and get the selected file path
    file_path = filedialog.askopenfilename(**options)

    if not file_path:
        print("No file was selected.")
        return None
    else:
        return file_path

if __name__ == "__main__":
    selected_file = open_file()
    if selected_file:
        print(f"Selected file: {selected_file}")
