import tkinter as tk
from tkinter import messagebox, scrolledtext, filedialog
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
        self.is_recording = False
        self.summary_save_path = None  # 儲存總結後內容路徑
        self.create_widgets()

    def create_widgets(self):
        # 單一按鈕用於開始/停止錄音
        self.toggle_button = tk.Button(self.master, text="Start Recording", command=self.toggle_recording)
        self.toggle_button.grid(row=0, column=0, padx=5, pady=5)
        # Transcript display area
        self.transcript_box = scrolledtext.ScrolledText(self.master, width=60, height=20)
        self.transcript_box.grid(row=1, column=0, columnspan=2, padx=5, pady=5)
        # Generate summary button
        self.summary_button = tk.Button(self.master, text="Generate Summary", command=self.generate_summary)
        self.summary_button.grid(row=2, column=0, columnspan=2, pady=5)
        # 新增按鈕：選擇儲存辨識內容的路徑並儲存內容
        self.save_transcript_button = tk.Button(self.master, text="儲存辨識內容", command=self.save_transcript)
        self.save_transcript_button.grid(row=3, column=0, padx=5, pady=5)
        # 新增按鈕：設定總結後內容儲存路徑
        self.set_summary_path_button = tk.Button(self.master, text="設定總結儲存路徑", command=self.choose_summary_output_path)
        self.set_summary_path_button.grid(row=3, column=1, padx=5, pady=5)

    def toggle_recording(self):
        if not self.is_recording:
            # 開始錄音
            self.is_recording = True
            self.toggle_button.config(text="Stop Recording")
            # 啟動連續轉錄與錄音的執行緒
            threading.Thread(target=self.recorder.start_recording, daemon=True).start()
            threading.Thread(target=self.recognizer.start_continuous_recognition, daemon=True).start()
            # 開始即時更新 transcript_box 的內容
            self.update_transcript()
            messagebox.showinfo("Info", "Recording started")
        else:
            # 停止錄音
            self.recorder.stop_recording()
            self.recognizer.stop_continuous_recognition()
            self.is_recording = False
            self.toggle_button.config(text="Start Recording")
            # 最後更新一次轉錄內容
            transcript = self.recognizer.get_transcript()
            self.transcript_box.delete(1.0, tk.END)
            self.transcript_box.insert(tk.END, transcript)
            messagebox.showinfo("Info", "Recording stopped")

    def update_transcript(self):
        if self.is_recording:
            transcript = self.recognizer.get_transcript()
            self.transcript_box.delete(1.0, tk.END)
            self.transcript_box.insert(tk.END, transcript)
            # 每 500ms 再次更新
            self.master.after(500, self.update_transcript)

    def save_transcript(self):
        transcript = self.recognizer.get_transcript()
        if not transcript:
            messagebox.showwarning("Warning", "尚無辨識內容可儲存")
            return
        file_path = filedialog.asksaveasfilename(title="儲存辨識內容",
                                                 defaultextension=".txt",
                                                 filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            try:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(transcript)
                messagebox.showinfo("Info", f"辨識內容已儲存於：{file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"儲存失敗：{e}")

    def choose_summary_output_path(self):
        directory = filedialog.askdirectory(title="選擇總結儲存目錄")
        if directory:
            self.summary_save_path = directory
            messagebox.showinfo("設定", f"總結儲存路徑設定為：{directory}")

    def generate_summary(self):
        transcript = self.recognizer.get_transcript()
        summary = self.processor.generate_summary(transcript, "Course Title", "Course Topic")
        # 儲存摘要至設定的路徑，如未設定則顯示摘要
        if self.summary_save_path:
            file_path = f"{self.summary_save_path}/summary.md"
            try:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(summary)
                messagebox.showinfo("Summary", f"摘要已儲存於：{file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"摘要儲存失敗：{e}")
        else:
            messagebox.showinfo("Summary", summary)
    
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
