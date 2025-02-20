import re

class TextProcessor:
    def clean_text(self, text):
        # 只保留英文字母、數字、空格和中文
        cleaned_text = re.sub(r'[^\w\s\u4e00-\u9fff]', '', text)
        return cleaned_text

    def summarize(self, text):
        # 暫時未實作
        pass