import os
from dotenv import load_dotenv
import azure.cognitiveservices.speech as speechsdk
import logging
from datetime import datetime

class SpeechRecognizer:
    def __init__(self):
        load_dotenv()
        self.speech_key = os.getenv('AZURE_SPEECH_KEY')
        self.region = os.getenv('AZURE_REGION')
        self.audio_stream = speechsdk.audio.PushAudioInputStream()
        self.audio_config = speechsdk.audio.AudioConfig(stream=self.audio_stream)
        self.speech_config = speechsdk.SpeechConfig(subscription=self.speech_key, region=self.region)
        self.speech_config.speech_recognition_language = "zh-CN"  # 設置語音識別語言為中文（簡體）
        self.speech_config.request_word_level_timestamps()  # 開啟詞級時間戳
        self.speech_config.enable_dictation()  # 開啟聽寫模式
        self.recognizer = speechsdk.SpeechRecognizer(speech_config=self.speech_config, audio_config=self.audio_config)
        self.transcript = []

        # 設置日誌記錄
        logging.basicConfig(filename='speech.log', level=logging.INFO, format='%(asctime)s - %(message)s')

        self.recognizer.recognized.connect(self._recognized_handler)
        self.recognizer.session_started.connect(lambda evt: print("Session started"))
        self.recognizer.session_stopped.connect(lambda evt: print("Session stopped"))
        self.recognizer.canceled.connect(self._canceled_handler)

    def _recognized_handler(self, evt):
        if evt.result.reason == speechsdk.ResultReason.RecognizedSpeech:
            print(f"完整識別: {evt.result.text}")
            logging.info(f"完整識別: {evt.result.text}")
            self.transcript.append(evt.result.text)
            self._write_hourly_log(evt.result.text)
        elif evt.result.reason == speechsdk.ResultReason.NoMatch:
            print("No speech could be recognized")
            logging.warning("No speech could be recognized")

    def _canceled_handler(self, evt):
        print(f"Canceled: {evt.reason}")
        logging.error(f"Canceled: {evt.reason}")

    def process_audio(self, data):
        self.audio_stream.write(data)

    def start_continuous_recognition(self):
        self.recognizer.start_continuous_recognition()

    def stop_continuous_recognition(self):
        self.recognizer.stop_continuous_recognition()

    def get_transcript(self):
        return ' '.join(self.transcript)

    def _write_hourly_log(self, text):
        current_time = datetime.now()
        output_dir = "output"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        filename = os.path.join(output_dir, current_time.strftime("speech_%Y-%m-%d_%H.txt"))
        with open(filename, "a", encoding="utf-8") as f:
            f.write(text + "\n")