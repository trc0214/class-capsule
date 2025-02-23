# 🎤 Class Capsule

**Class Capsule** 是一個 Python 專案，能夠 **即時錄音、語音轉文字**，並透過 AI 進行 **文字摘要**，適用於課堂筆記、會議記錄等場景。

---

## 🚀 功能
1. **即時背景錄音** 🎙️（自動記錄音訊）
2. **語音轉文字** 📝（使用 Microsoft Azure Speech-to-Text API）
3. **文字摘要** ✨（利用 Azure OpenAI 服務生成筆記）

---

## 📂 專案結構
```
class-capsule/
│── .env                     # 環境變數 (API 金鑰、參數)
│── .env.example             # 環境變數範例檔案
│── .gitignore               # Git 忽略設定
│── LICENSE                  # 授權條款
│── main.py                  # 主程式
│── modules/                # 核心模組
│   │── __init__.py
│   │── audio_recorder.py     # 及時背景錄音
│   │── speech_recognizer.py  # 語音轉文字（Azure Speech 服務）
│   │── text_processor.py     # 文本處理與摘要
│── output/                  # 轉錄後的文字與摘要輸出
│── requirements.txt         # 依賴庫清單
│── tests/                   # 測試文件（若執行 pytest 可使用）
```

---

## 🛠️ 安裝與使用

### 1️⃣ 環境設定
請確保已安裝 **Python 3.8+**，然後執行以下指令：
```sh
git clone https://github.com/your-username/class-capsule.git
cd class-capsule
python -m venv env
# Windows 用 `env\Scripts\activate`；Linux/macOS 用 `source env/bin/activate`
source env/bin/activate
pip install -r requirements.txt
```

### 2️⃣ 設定 API 金鑰
建立一個 .env 檔案（或複製 `.env.example`)，設定你的 API 金鑰：
```python
AZURE_SPEECH_KEY = "your-azure-key"
AZURE_REGION = "your-region"

AZURE_OPENAI_API_KEY = "your-azure-openai-api-key"
AZURE_OPENAI_ENDPOINT = "your-azure-openai-endpoint"
AZURE_OPENAI_DEPLOYMENT_NAME = "your-azure-openai-deployment-name"
```

### 3️⃣ 開始使用
執行主程式以啟動即時錄音與文字轉換：
```sh
python main.py
```

運行期間，錄音內容會即時透過 speech_recognizer.py 處理並儲存，文字摘要則由 text_processor.py 生成。輸出結果及日誌分別儲存在 output/ 與日誌檔中（例如 speech.log 與 text_processor.log）。

---

## ⚙️ 依賴
- Python 3.8+
- **Microsoft Azure Speech-to-Text API**
- `pyaudio`（錄音）
- `wave`（音檔處理）
- `openai` 或 `transformers`（AI 摘要）
- `python-dotenv`（環境變數設定）
- 文本處理相關：`jieba`, `markdown`, `deepmultilingualpunctuation`, `rapidfuzz`, `pdfplumber`

所有依賴皆可透過以下指令安裝：
```sh
pip install -r requirements.txt
```

---

## 📝 開發進度
- [x] 即時背景錄音
- [x] 語音轉文字
- [ ] 文字摘要（測試中）
- [ ] GUI 介面（未來計畫）

---

## 📜 授權
本專案採用 MIT License。歡迎自由使用與貢獻！🚀
```

You can replace the repository URL and API 金鑰資訊 with your real details.
You can replace the repository URL and API 金鑰資訊 with your real details.