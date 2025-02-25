import tkinter as tk
from tkinter import messagebox, scrolledtext
import threading
from modules.speech_recognizer import SpeechRecognizer
from modules.audio_recorder import AudioRecorder
from modules.text_processor import TextProcessor

class App:
    def __init__(self, master):
        self.master = master
        master.title("Class Capsule GUI")
        self.recognizer = SpeechRecognizer()
        self.recorder = AudioRecorder(self.recognizer)
        self.processor = TextProcessor()
        self.create_widgets()

    def create_widgets(self):
        # Start and Stop buttons
        self.start_button = tk.Button(self.master, text="Start Recording", command=self.start_recording)
        self.start_button.grid(row=0, column=0, padx=5, pady=5)
        self.stop_button = tk.Button(self.master, text="Stop Recording", command=self.stop_recording)
        self.stop_button.grid(row=0, column=1, padx=5, pady=5)
        # Transcript display area
        self.transcript_box = scrolledtext.ScrolledText(self.master, width=60, height=20)
        self.transcript_box.grid(row=1, column=0, columnspan=2, padx=5, pady=5)
        # Generate summary button
        self.summary_button = tk.Button(self.master, text="Generate Summary", command=self.generate_summary)
        self.summary_button.grid(row=2, column=0, columnspan=2, pady=5)

    def start_recording(self):
        threading.Thread(target=self.recognizer.start_continuous_recognition, daemon=True).start()
        threading.Thread(target=self.recorder.start_recording, daemon=True).start()
        messagebox.showinfo("Info", "Recording started")

    def stop_recording(self):
        self.recorder.stop_recording()
        self.recognizer.stop_continuous_recognition()
        transcript = self.recognizer.get_transcript()
        self.transcript_box.delete(1.0, tk.END)
        self.transcript_box.insert(tk.END, transcript)
        messagebox.showinfo("Info", "Recording stopped")

    def generate_summary(self):
        transcript = self.recognizer.get_transcript()
        summary = self.processor.generate_summary(transcript, "Course Title", "Course Topic")
        messagebox.showinfo("Summary", summary)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
