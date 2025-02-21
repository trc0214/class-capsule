import os
from dotenv import load_dotenv
from openai import AzureOpenAI
import jieba
import jieba.analyse
import markdown
from deepmultilingualpunctuation import PunctuationModel
from rapidfuzz import process, fuzz
import re
import logging
import pdfplumber


class TextProcessor:
    def __init__(self):
        load_dotenv()
        self.punctuation_model = PunctuationModel()
        self.deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
        self.client = AzureOpenAI(
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            api_version="2024-02-01",  # 固定 API 版本
        )
        self.prompt = """
    這是一份教授講課的語音轉文字記錄，大約 8000 字，內容較長。請你根據以下要求幫我整理成條理清晰的筆記：

    1. 提煉重點：萃取課程的關鍵概念、理論、範例，避免冗長的對話內容。
    2. 結構清晰：以大標題（主題）、小標題（子議題）與條列式重點（重點敘述）組織筆記。
    3. 條理分明：可使用 概念解析、關鍵詞、核心論點、應用範例、教授的額外補充 來幫助理解。
    4. 保留專業術語，但用簡潔明瞭的語言來闡述，讓筆記易讀易懂。
    5. 如果內容包含數據、案例或教授的特別見解，請標註，讓筆記更具價值。
    6. 請使用 Markdown 格式，如 # 主題、## 子議題、- 重要概念
    7. 如果適合，請以表格呈現比較資訊
    """

        logging.basicConfig(
            filename="text_processor.log",
            level=logging.INFO,
            format="%(asctime)s:%(levelname)s:%(message)s",
        )

    def enhance_readability(self, input_text: str, topics_reference: list[str] = None) -> str:
        """
        將輸入文本分段後依次進行自動標點、句子切分及依參考主題修正，再合併成更易讀的文本。
        """
        try:
            # 將文本按每 500 個字拆分成多個段落
            chunk_size = 500
            text_chunks = [input_text[i:i+chunk_size] for i in range(0, len(input_text), chunk_size)]
            processed_chunks = []
            for chunk in text_chunks:
                # 自動標點修復
                punctuated_text = self.punctuation_model.restore_punctuation(chunk)
                # 切分句子
                sentence_list = re.split(r"[。！？!?;\n]+", punctuated_text)
                readable_sentences = [s.strip() for s in sentence_list if s.strip()]
                
                # 根據參考主題修正詞彙
                if topics_reference:
                    for i, sentence in enumerate(readable_sentences):
                        words = list(jieba.cut(sentence, cut_all=False))
                        for j, word in enumerate(words):
                            best_match = process.extractOne(word, topics_reference, scorer=fuzz.partial_ratio)
                            if best_match and isinstance(best_match, tuple) and best_match[1] > 80:
                                words[j] = best_match[0]
                        readable_sentences[i] = "".join(words)
                
                processed_chunks.append("。".join(readable_sentences))
            
            return "。".join(processed_chunks) + "。"
        except Exception as error:
            logging.error(f"格式化文本時發生錯誤: {error}")
            return "文本格式化失敗"

    def generate_summary(
        self, input_text: str, course_title: str, course_topic: str, supplementary_material: str = ""
    ) -> str:
        """
        傳入完整課程內容、課程名稱與主題，利用 Azure OpenAI 服務生成摘要。
        """
        try:
            response = self.client.chat.completions.create(
                model=self.deployment_name,
                messages=[
                    {
                        "role": "system",
                        "content": self.prompt,
                    },
                    {
                        "role": "user",
                        "content": f"""
                        這是課程的名稱: {course_title},
                        這是課程的主題: {course_topic},
                        這是完整的課程內容（請根據以下內容整理筆記）: {input_text}
                        這是課程的補充資料: {supplementary_material}
""",
                    },
                ],
                temperature=0.3,
            )
            return (
                response.choices[0].message.content
                if response.choices
                else "無法生成摘要"
            )
        except Exception as error:
            logging.error(f"摘要時發生錯誤: {error}")
            return "摘要生成失敗"

    def extract_main_keywords(self, input_text: str, top_n: int = 5) -> list[str]:
        """
        利用 jieba 提取文本中最主要的關鍵詞。
        """
        try:
            keywords = jieba.analyse.extract_tags(input_text, topK=top_n)
            return keywords
        except Exception as error:
            logging.error(f"提取關鍵詞時發生錯誤: {error}")
            return []

    def extract_topics(self, input_text: str, num_topics: int = 3) -> list[str]:
        """
        使用 OpenAI 服務從文本中提取指定數量的主題，以逗號分隔返回。
        """
        try:
            response = self.client.chat.completions.create(
                model=self.deployment_name,
                messages=[
                    {
                        "role": "system",
                        "content": f"請從以下文本中提取 {num_topics} 個關鍵主題，以逗號分隔：",
                    },
                    {"role": "user", "content": input_text},
                ],
                temperature=0.3,
            )
            topics_raw_text = (
                response.choices[0].message.content if response.choices else "None"
            )
            topic_list = re.split(r"[，,；]", topics_raw_text)
            return [topic.strip() for topic in topic_list if topic.strip()]
        except Exception as error:
            logging.error(f"主題建模時發生錯誤: {error}")
            return []

    def convert_text_to_markdown(self, input_text: str) -> str:
        """
        將純文本轉換為 Markdown 格式。
        """
        try:
            return markdown.markdown(input_text)
        except Exception as error:
            logging.error(f"轉換文本為 Markdown 時發生錯誤: {error}")
            return "文本格式化失敗"

    def merge_topic_lists(
        self, input_text: str, topics_reference: list[str] = None
    ) -> list[str]:
        """
        合併從文本中提取的主題與使用者提供的參考主題，返回一個總清單。
        """
        try:
            extracted_topics = self.extract_topics(input_text)
            combined_topics = set(extracted_topics) | set(topics_reference or [])
            return list(combined_topics)
        except Exception as error:
            logging.error(f"合併主題清單時發生錯誤: {error}")
            return []

    def extract_text_from_pdf(pdf_path: str) -> str:
        """
        從 PDF 文件中提取純文本內容，並回傳該文本。
        此函數使用 pdfplumber，其對中文抽取精度較高。
        """
        all_text = ""
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    all_text += page_text + "\n"
        return all_text


if __name__ == "__main__":
    processor = TextProcessor()
    with open("output/speech_2025-02-21_13.txt", "r", encoding="utf-8") as file:
        source_text = file.read()
    # enhanced_text = processor.enhance_readability(source_text)
    # print(enhanced_text)
    summary = processor.generate_summary(
        source_text, "英文", "課堂介紹"
    )
    print(summary)
