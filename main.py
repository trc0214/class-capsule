from modules.speech_recognizer import SpeechRecognizer
from modules.audio_recorder import AudioRecorder

def main():
    open("speech.log", "w").close()  # 啟動時清空舊內容
    recognizer = SpeechRecognizer()
    recorder = AudioRecorder(recognizer)

    print("Starting real-time transcription. Press Enter to stop.")
    recognizer.start_continuous_recognition()
    recorder.start_recording()

    input()  # Wait for user input to stop

    recorder.stop_recording()
    recognizer.stop_continuous_recognition()

    print("Transcription result:")
    print(recognizer.get_transcript())

if __name__ == "__main__":
    main()