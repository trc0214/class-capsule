import pyaudio
import wave
import threading
import time


class Recorder:
    def __init__(
        self,
        filename="output.wav",
        chunk=1024,
        format=pyaudio.paInt16,
        channels=2,
        rate=44100,
    ):
        self.filename = filename
        self.chunk = chunk
        self.format = format
        self.channels = channels
        self.rate = rate
        self.frames = []
        self.is_recording = False
        self.thread = None

        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(
            format=self.format,
            channels=self.channels,
            rate=self.rate,
            input=True,
            frames_per_buffer=self.chunk,
        )

    def start_recording(self):
        """開始錄音 (背景執行)"""
        if self.is_recording:
            print("Recording is already in progress...")
            return
        self.is_recording = True
        self.frames = []
        self.thread = threading.Thread(target=self._record)
        self.thread.start()

    def _record(self):
        """錄音執行緒"""
        while self.is_recording:
            try:
                data = self.stream.read(self.chunk, exception_on_overflow=False)
                self.frames.append(data)
            except Exception as e:
                print(f"Error while recording: {e}")
            time.sleep(0.01)

    def stop_recording(self):
        """停止錄音"""
        if not self.is_recording:
            print("No active recording to stop.")
            return
        self.is_recording = False
        if self.thread:
            self.thread.join()  # 等待執行緒結束

    def save_recording(self):
        """儲存錄音檔案"""
        with wave.open(self.filename, "wb") as wf:
            wf.setnchannels(self.channels)
            wf.setsampwidth(self.p.get_sample_size(self.format))
            wf.setframerate(self.rate)
            wf.writeframes(b"".join(self.frames))
        print(f"Recording saved to {self.filename}")

    def close(self):
        """釋放錄音裝置"""
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()


# 測試錄音
if __name__ == "__main__":
    recorder = Recorder()
    print("Recording... Press Enter to stop.")
    recorder.start_recording()
    input()
    recorder.stop_recording()
    recorder.save_recording()
    recorder.close()
    print("Recording saved successfully!")
