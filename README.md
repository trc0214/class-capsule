# 🎤 Class Capsule

**Class Capsule** 是一個 Python 專案，能夠 **即時錄音、語音轉文字**，並透過 AI 進行 **文字摘要**，適用於課堂筆記、會議記錄等場景。

---

## 🚀 功能
1. **即時背景錄音** 🎙️（自動記錄音訊）
2. **語音轉文字** 📝（使用 Microsoft Azure Speech-to-Text API）
3. **文字摘要** ✨（AI 生成簡短重點筆記）

---

## 📂 專案結構
```
class-capsule/
│── env/                   # 虛擬環境 (不納入 Git 版控)
│── src/                   # 核心程式碼
│   │── main.py            # 主程式
│   │── recorder.py        # 及時背景錄音
│   │── speech_to_text.py  # 語音轉文字 (Azure API)
│   │── summarizer.py      # 文字摘要 (AI NLP)
│   │── config.py          # 設定檔 (API 金鑰、參數)
│── logs/                  # 日誌紀錄
│── output/                # 轉錄後的文字與摘要
│── requirements.txt       # 依賴庫清單
│── README.md              # 專案說明
│── .gitignore             # Git 忽略設定
```

---

## 🛠️ 安裝與使用

### 1️⃣ **環境設定**
請確保已安裝 **Python 3.8+**，然後執行：
```sh
git clone https://github.com/your-username/class-capsule.git
cd class-capsule
python -m venv env
source env/bin/activate  # Windows 用 `env\Scripts\activate`
pip install -r requirements.txt
```

### 2️⃣ **設定 API 金鑰**
請在 `.env` 設定你的 **Azure Speech-to-Text API 金鑰**：
```python
AZURE_SPEECH_KEY = "your-azure-key"
AZURE_REGION = "your-region"
```

### 3️⃣ **開始錄音**
執行主程式：
```sh
python src/main.py
```

---

## ⚙️ 依賴
- Python 3.8+
- **Microsoft Azure Speech-to-Text API**
- `pyaudio`（錄音）
- `soundfile`（音檔處理）
- `openai` 或 `transformers`（AI 摘要）

安裝所有依賴：
```sh
pip install -r requirements.txt
```

---

## 📝 開發進度
- [x] 即時背景錄音
- [x] 語音轉文字
- [ ] 文字摘要（開發中）
- [ ] GUI 介面（未來計畫）

---

## 📜 授權
本專案採用 **MIT License**。歡迎自由使用與貢獻！🚀
```

---