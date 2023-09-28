import requests
from bs4 import BeautifulSoup
import json
from os import path

filename = "file.json"

if path.isfile(filename) is False:
    raise Exception("File not found")

file_data = ""

BASE_URL = "https://www.juscorpus.com/category/blogs/page/"

NUM_PAGES = 5

with open(filename, "w") as f:
  f.write("[")
for i in range(NUM_PAGES):
    new_url = BASE_URL + str(i) + "/"
    page = requests.get(new_url)
    soup = BeautifulSoup(page.content, "html.parser")
    blogs = soup.find_all("h3", class_="entry-title")
    for blog in blogs:
        page_new = requests.get(blog.find("a")["href"])
        soup_new = BeautifulSoup(page_new.content, "html.parser")
        page_title = soup_new.find("div", class_="page-title-title").find("h1").text
        print(page_title)
        page_contents = soup_new.find("div", class_="elementor-text-editor elementor-clearfix")
        page_content_final = ""
        for page_content in page_contents:
            page_content_final += page_content.text + "\n"
        with open(filename, 'a', encoding='utf-8') as f:
            f.write(json.dumps({ "title": page_title, "content": page_content_final}, ensure_ascii=False, indent=4) + ",")
        print(page_content_final)
with open(filename, "a") as f:
    f.write("]")
with open(filename, "r") as f:
    file_data = f.read()
with open(filename, "w") as f:
    f.write(file_data.replace(",]", "]"))
