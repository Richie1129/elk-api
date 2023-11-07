import urllib.request as req
from bs4 import BeautifulSoup
import os
import re
import hashlib
from urllib.error import HTTPError
from urllib.parse import urljoin

# 函數：替換特殊字符並限制檔案名稱的長度
def clean_filename(filename):
    valid_chars = '-_() abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    cleaned_filename = ''.join(c if c in valid_chars else '_' for c in filename)
    return cleaned_filename[:255]  # 限制檔名長度

# 指定網頁 URL
url = "https://twsf.ntsec.gov.tw/activity/race-1/62/senior.html"

# 設置請求標頭
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
}

# 創建目錄用於保存 PDF 檔案
output_directory = "62屆"
os.makedirs(output_directory, exist_ok=True)

request = req.Request(url, headers=headers)

with req.urlopen(request) as response:
    data = response.read().decode("utf-8")
    soup = BeautifulSoup(data, "html.parser")

# 尋找所有科別
categories = soup.find_all("span", class_="Stitle04")
for category in categories:
    category_name = category.text.strip()
    print(f"科別: {category_name}")

    # 尋找當前科別下的所有作品
    works = category.find_next("tbody").find_all("td", {"data-title": "作品名稱"})
    
    # 將作品按名稱排序
    works.sort(key=lambda work: work.a.text.strip())

    for work in works:
        work_name = work.a.text.strip()
        pdf_link = work.a.get("href")

        if pdf_link.endswith(".pdf"):
            full_pdf_link = urljoin(url, pdf_link)
            print(f"Full PDF Link: {full_pdf_link}")  # 新增的 print 語句，用於顯示 full_pdf_link
            
            # 使用哈希值作為檔案名稱
            file_hash = hashlib.md5(full_pdf_link.encode()).hexdigest()
            pdf_filename = os.path.join(output_directory, category_name, f"{file_hash}.pdf")
            os.makedirs(os.path.join(output_directory, category_name), exist_ok=True)

            try:
                req.urlretrieve(full_pdf_link, pdf_filename)
                print(f"下載完成: {pdf_filename}")
            except HTTPError as e:
                print(f"無法下載檔案: {pdf_filename}, 錯誤訊息: {e}")
