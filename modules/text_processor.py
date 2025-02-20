import os
from dotenv import load_dotenv
import openai
import jieba
import jieba.analyse
import markdown
from deepmultilingualpunctuation import PunctuationModel
from rapidfuzz import process
import re
import logging

class TextProcessor:
    def __init__(self):
        load_dotenv()
        self.punctuation_model = PunctuationModel()
        self.openai_api_key = os.getenv('AZURE_OPENAI_API_KEY')
        self.openai_endpoint = os.getenv('AZURE_OPENAI_ENDPOINT')
        self.openai_api_version = os.getenv('AZURE_OPENAI_API_VERSION')
        self.deployment_name = os.getenv('AZURE_OPENAI_DEPLOYMENT_NAME')
        openai.api_key = self.openai_api_key
        openai.api_base = self.openai_endpoint
        openai.api_version = self.openai_api_version

        # 設置日誌系統
        logging.basicConfig(filename='text_processor.log', level=logging.ERROR, 
                            format='%(asctime)s:%(levelname)s:%(message)s')

    def format_text_for_readability(self, text: str, manual_topics: list[str] = None) -> str:
        try:
            # 自動標點
            text = self.punctuation_model.restore_punctuation(text)
            
            # 句子分割（確保句子級別斷句）
            sentences = re.split(r'[。！？\n]', text)
            formatted_text = [sent.strip() for sent in sentences if sent.strip()]  # 去除空白

            # 根據手動提供的主題修正拼寫錯誤
            if manual_topics:
                for i, sent in enumerate(formatted_text):
                    words = list(jieba.cut(sent, cut_all=False))  # 分詞處理
                    for j, word in enumerate(words):
                        best_match = process.extractOne(word, manual_topics, scorer=process.fuzz.partial_ratio)
                        if best_match and best_match[1] > 80:
                            words[j] = best_match[0]  # 只修正錯誤的詞
                    formatted_text[i] = ''.join(words)  # 重新組合回句子

            return "。".join(formatted_text) + "。"  # 重新組合句子
        except Exception as e:
            logging.error(f"格式化文本時發生錯誤: {e}")
            return "文本格式化失敗"

    def summarize_text(self, text: str, max_summary_length: int = 200) -> str:
        try:
            if len(text) > 2000:  # 過長文本的處理方式
                text = text[:2000] + "..."  # 只取前 2000 個字，避免 API 輸入長度限制

            response = openai.ChatCompletion.create(
                engine=self.deployment_name,
                messages=[
                    {"role": "system", "content": "請用簡單的中文總結以下文本："},
                    {"role": "user", "content": text}
                ],
                temperature=0.3,
                max_tokens=max_summary_length
            )
            return response.choices[0].message.get('content', '無法生成摘要')
        except Exception as e:
            logging.error(f"摘要時發生錯誤: {e}")
            return "摘要生成失敗"

    def extract_keywords(self, text: str, top_n: int = 5) -> list[str]:
        try:
            keywords = jieba.analyse.extract_tags(text, topK=top_n)
            return keywords
        except Exception as e:
            logging.error(f"提取關鍵詞時發生錯誤: {e}")
            return []

    def perform_topic_modeling(self, text: str, num_topics: int = 3) -> list[str]:
        try:
            response = openai.ChatCompletion.create(
                engine=self.deployment_name,
                messages=[
                    {"role": "system", "content": f"請從以下文本中提取 {num_topics} 個關鍵主題，以逗號分隔："},
                    {"role": "user", "content": text}
                ],
                temperature=0.3,
                max_tokens=50
            )
            topics_raw = response.choices[0].message.get('content', '')  # 確保 `content` 存在
            topics = re.split(r'[，,；]', topics_raw)  # 允許不同的標點符號
            return [t.strip() for t in topics if t.strip()]
        except Exception as e:
            logging.error(f"主題建模時發生錯誤: {e}")
            return []

    def format_text(self, text: str) -> str:
        try:
            return markdown.markdown(text)
        except Exception as e:
            logging.error(f"格式化文本為 Markdown 時發生錯誤: {e}")
            return "文本格式化失敗"

    def combine_with_manual_topic(self, text: str, manual_topics: list[str] = None) -> list[str]:
        try:
            topics = self.perform_topic_modeling(text)
            combined_topics = set(topics) | set(manual_topics or [])  # 避免 NoneType 錯誤
            return list(combined_topics)
        except Exception as e:
            logging.error(f"結合手動主題時發生錯誤: {e}")
            return []