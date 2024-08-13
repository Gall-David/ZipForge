from src.file_processor import FileProcessor
from src.application import Application

import sys
import threading
from tkinter import scrolledtext
import tkinter as tk


class RedirectText:
    """
    Class to redirect stdout to a text widget
    """
    def __init__(self, text_widget: scrolledtext.ScrolledText) -> None:
        """
        Constructor for the RedirectText class
        Parameters:
            text_widget: scrolledtext.ScrolledText: The text widget to redirect the output to
        Returns:
            None
        """
        self.output = text_widget

    def write(self, string: str) -> None:
        """
        Write the string to the text widget
        Parameters:
            string: str: The string to write
        Returns:
            None
        """
        self.output.insert(tk.END, string)
        self.output.see(tk.END)

    def flush(self) -> None:
        """
        Required to override the flush method
        Parameters:
            None
        Returns:
            None
        """
        pass

class UI:
    def __init__(self, master: tk.Tk) -> None:
        """
        Constructor for the UI class
        Parameters:
            master: tk.Tk: The root window
        Returns:
            None
        """
        self.master = master
        master.title("File Processor")

        # Input textbox for config file path
        self.path_label = tk.Label(master, text="Config File Path:")
        self.path_label.pack()
        self.path_entry = tk.Entry(master, width=50)
        self.path_entry.pack()

        # Output textbox for logs
        self.log_label = tk.Label(master, text="Logs:")
        self.log_label.pack()
        self.log_text = scrolledtext.ScrolledText(master, height=20)
        self.log_text.pack()

        # Run button
        self.run_button = tk.Button(master, text="Run", command=self.run_processor)
        self.run_button.pack()

        # Redirect stdout to the log textbox
        sys.stdout = RedirectText(self.log_text)

        # Store the original stdout
        self.original_stdout = sys.stdout

        # Add a flag to track if processing is running
        self.processing = False

        # Bind the window close event
        master.protocol("WM_DELETE_WINDOW", self.on_closing)

    def run_processor(self) -> None:
        """
        Run the file processor
        Parameters:
            None
        Returns:
            None
        """
        config_path = self.path_entry.get()

        def run():
            self.processing = True
            print("Starting file processing...")
            Application.run(config_path)
            print("File processing completed.")
            self.processing = False

        # Run the processor in a separate thread to prevent UI freezing
        self.process_thread = threading.Thread(target=run)
        self.process_thread.start()

    def on_closing(self) -> None:
        """
        Handle the window close event
        Parameters:
            None
        Returns:
            None
        """
        if self.processing:
            print("Processing is still running. Attempting to stop...")

            FileProcessor.stop_processing = True

            # Wait for the processing thread to finish (with a timeout)
            self.process_thread.join(timeout=5)

            if self.process_thread.is_alive():
                print("Warning: Processing did not stop in time.")
            else:
                print("Processing stopped successfully.")

        # Restore the original stdout
        sys.stdout = self.original_stdout

        # Close the window and exit the application
        self.master.destroy()
        sys.exit(0)