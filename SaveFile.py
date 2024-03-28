import tkinter as tk
from tkinter import filedialog

class File:
	def __init__(self):
		self.filePath = None

	def loadFile(self):
		"""
		Opens a file dialog that allows the user to select a file for opening.
		Returns the path of the selected file.
		"""
		root = tk.Tk()
		root.withdraw()  # Hide the Tkinter root window

		# Set options for the open file dialog
		options = {
			'defaultextension': '.rcr',  # Default file extension
			'filetypes': [('rcRacer files', '*.rcr'), ('Text files', '*.txt')],  # Allowed file types
			'initialdir': 'C:\\',  # Initial directory
			'title': 'Select file to open'  # Dialog title
		}

		# Open the dialog and get the selected file path
		tempFilePath = filedialog.askopenfilename(**options)

		if not tempFilePath:
			self.filePath = None
		else:
			self.filePath = tempFilePath

	def saveFile(self):
		"""
		Opens a save file dialog that allows the user to select a directory and enter a file name.
		"""
		root = tk.Tk()
		root.withdraw()  # Hide the Tkinter root window

		# Set options for the save dialog
		options = {
			'defaultextension': '.rcr',  # Default file extension
			'filetypes': [('rcRacer files', '*.rcr'), ('Text files', '*.txt')],  # Allowed file types
			'initialdir': 'C:\\',  # Initial directory
			'title': 'Save as...'  # Dialog title
		}

		# Open the dialog and get the selected file name
		self.filePath = filedialog.asksaveasfilename(**options)

		if not self.filePath:
			print("No file was selected.")
			return

		# Create an empty file at the specified path
		try:
			with open(self.filePath, 'w') as file:
				pass  # Just create the file, don't write anything
			print(f"File saved: {self.filePath}")
		except Exception as e:
			print(f"Failed to save the file: {e}")