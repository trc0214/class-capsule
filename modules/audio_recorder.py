import pyaudio
import threading
import time

class AudioRecorder:
    def __init__(self, recognizer):
        self.recognizer = recognizer
        self.sample_rate = 16000
        self.channels = 1
        self.format = pyaudio.paInt16
        self.chunk = 4096  # 調整 chunk 到 4096（更大）
        self.audio_interface = pyaudio.PyAudio()
        self.stream = None
        self.recording_thread = None
        self.is_recording = False

    def start_recording(self, duration=None):
        if self.is_recording:
            return

        self.is_recording = True
        self.stream = self.audio_interface.open(format=self.format,
                                                channels=self.channels,
                                                rate=self.sample_rate,
                                                input=True,
                                                frames_per_buffer=self.chunk)
        self.recording_thread = threading.Thread(target=self._record, args=(duration,))
        self.recording_thread.start()

    def _record(self, duration):
        start_time = time.time()
        try:
            while self.is_recording:
                data = self.stream.read(self.chunk)
                self.recognizer.process_audio(data)
                if duration and (time.time() - start_time) >= duration:
                    self.stop_recording()
        except OSError as e:
            print(f"Error during recording: {e}")
            self._restart_recording(duration)
        except Exception as e:
            print(f"Unexpected error during recording: {e}")
        finally:
            self._cleanup()

    def _restart_recording(self, duration):
        print("Restarting recording...")
        self._cleanup()
        self.start_recording(duration)

    def stop_recording(self):
        if not self.is_recording:
            return

        self.is_recording = False
        if self.recording_thread is not None:
            self.recording_thread.join()
        self._cleanup()

    def _cleanup(self):
        if self.stream is not None:
            self.stream.stop_stream()
            self.stream.close()
            self.stream = None

    def __del__(self):
        self.audio_interface.terminate()