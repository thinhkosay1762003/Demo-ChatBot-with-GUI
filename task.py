import webbrowser as wb
from unidecode import unidecode
import wikipedia
from pyvi import ViTokenizer
from googletrans import Translator
import datetime
import requests
from bs4 import BeautifulSoup
import re
import schedule
import time
import threading
from tkinter import messagebox

def find_document(message):
    ignore_word = ['cho','tôi','tài','liệu','môn','học','giáo','trình','cung','cấp','bài','giảng','tìm']
    infor = message.lower().split(' ')
    search = ''
    for i in infor:
        if i not in ignore_word:
            search = search + ' ' + i
    thong_bao =f"Đây là tài liệu cho môn {search} mà bạn đang tìm "
    search = "-".join(unidecode(search).split()).lower()
    url = f"https://cuuduongthancong.com/s/{search}"
    wb.get().open(url)
    return thong_bao


def find_on_wikipedia(message):
    wikipedia.set_lang("vi")
    ignore_word=["tìm","cho","tôi","là","ai","gì","biết", "khái niệm","về","ý nghĩa"]
    infor = message.lower().split(' ')
    search=''
    for i in infor:
        if i not in ignore_word:
            search=search+' '+ i
    try:
        information = wikipedia.summary(search,sentences=3)
        return information
    except Exception as e:
        return f"Không tìm thấy thông tin liên quan: {e}"

def translate_text(text, target_language='en'):
    translator = Translator()
    translated = translator.translate(text, dest=target_language)
    return translated.text

def dich_thuat(message):
    text_match = re.search(r'"(.*?)"', message)

    if text_match:
        text_to_translate = text_match.group(1)  # Store the text to be translated in a separate variable
    else:
        return 'Để hỗ trợ chuẩn xác nhất cho dịch thuật, hãy nhập văn bản bạn cần dịch trong " " và ngôn ngữ bạn cần dịch'

    language_codes = {
        "tiếng việt": "vi",
        "tiếng anh": "en",
        "tiếng pháp": "fr",
        "tiếng hàn": "ko",
        "tiếng nhật": "ja",
        "tiếng nga": "ru",
        "tiếng trung": "zh-cn",
        "việt": "vi",
        "anh": "en",
        "pháp": "fr",
        "hàn": "ko",
        "nhật": "ja",
        "nga": "ru",
        "trung": "zh-cn"
    }

    non_translate_string = re.sub(r'"(.*?)"', '', message)

    translated_text = text_to_translate  # Initialize translated_text with the original text

    for language in language_codes:
        if language in non_translate_string:
            translated_text = translate_text(text_to_translate, language_codes[language])

    return f"Đoạn văn bản được dịch thành:\n{translated_text}"

def find_on_google(message):
    ignore_word = ["tìm","kiếm","google","trên","cho","tôi","biết", "về","bạn","có","thể","mở"]
    infor = message.lower().split(' ')
    search = ''
    for i in infor:
        if i not in ignore_word:
            search = search + ' ' + i
    if len(search)<=1:
        return "Hãy cung cấp kĩ hơn kết quả bạn mốn tìm kiếm trên Google"
    url = f"https://www.google.com/search?q=+{search}"
    wb.get().open(url)
    return f'Đây là kết quả cho {search} của bạn trên Google'
def find_on_youtube(message):
    ignore_word = ["video","youtube","mở","cho","tôi","về","trên","tìm","bạn","?","có","thể","tìm","được","không","muốn","cần"]
    infor = message.lower().split(' ')
    search = ''
    for i in infor:
        if i not in ignore_word:
            search = search + ' ' + i
    if len(search) <=1:
        return "Hãy cung cấp kĩ hơn video bạn mốn tìm kiếm trên Youtube"
    url = f"https://youtube.com/search?q={search}"
    wb.get().open(url)
    return f'Đây là kết quả cho {search} của bạn trên Youtube'
def open_code_ptit(message):
    url="https://code.ptit.edu.vn/student/question"
    wb.get().open(url)
    return "Tất nhiên rồi, đây là bài tập trên Code Ptit để bạn có thể luyện thêm khả năng code.\nNgoài ra bạn có thể tham khảo tử CodeLearn, CodeAcademy, LeetCode để trao dồi thêm."
def show(message):
    print("Đánh giá hôm nay của bạn trên Code PTIT\n")
def search_wikihow(message):
    tutor = f"Đây là hướng dẫn cho {message}:\n"
    base_url = "https://www.wikihow.vn"
    search_url = f"{base_url}/wikiHowTo?search={message}"

    try:
        response = requests.get(search_url)
        response.raise_for_status()  # Check for request success
        soup = BeautifulSoup(response.text, 'html.parser')
        search_results = soup.find_all("a", class_="result_link")

        if search_results:
            # Access the first result (you may iterate over results if needed)
            result = search_results[0]
            link = requests.get(result["href"])
            soup = BeautifulSoup(link.text, 'html.parser')
            phuong_phap = soup.find_all("div", class_="method_label")

            for i, method in enumerate(phuong_phap, 1):
                div_text = method.text.strip()
                h3_text = method.find_next("h3").text.strip()
                tutor += f"{div_text} {h3_text}\n"
                tutor_texts = method.find_next("b", class_="whb")
                a = 1
                tutor += f" 1.{tutor_texts.text}\n"

                while tutor_texts and tutor_texts.find_next("div", class_="step_num") and tutor_texts.find_next("div",
                                                                                                                class_="step_num").text != '1':
                    tutor_texts = tutor_texts.find_next("b", class_="whb")
                    a += 1
                    tutor += f" {a}.{tutor_texts.text}\n"
        else:
            tutor = "Không tìm thấy hướng dẫn phù hợp."
    except Exception as e:
        tutor = f"Có lỗi xảy ra: {str(e)}"

    return tutor


def find_code(message):
    search_query = message
    url = 'https://www.google.com/search?sitesearch=freetuts.net'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82',
    }
    parameters = {'q': search_query}
    content = requests.get(url, headers=headers, params=parameters).text
    soup = BeautifulSoup(content, 'html.parser')
    search = soup.find(id='search')
    if search:
        first_link = search.find('a')
        if first_link:
            first_link_url = first_link['href']
            response = requests.get(first_link_url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                code = soup.find_all('pre', class_='brush:cpp;')

                if not code:
                    code = soup.find_all('pre', class_='brush:python;')

                if not code:
                    code = soup.find_all('pre', class_='brush:java;')

                if code:
                    result = code[-1].get_text()
                    return(f"Đây là hướng dẫn cho {message} của bạn:\n {result}")
        return "Xin lỗi tôi không có hướng dẫn cho đoạn code này."



