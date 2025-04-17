import time
import requests
import re
import os
import sys

host = 'https://wallhaven.cc/search'
spider_path = "../data"
current_page = 2
final_page = 1000

if len(sys.argv) >= 2:
    current_page = int(sys.argv[1])

headers = {
    'accept': 'text/html, */*; q=0.01',
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
}

# 创建爬虫目录
os.makedirs(spider_path, exist_ok=True)

def handle_page_text(text):
    figures = re.findall('<figure.*?</figure>', text)
    for f in figures:
        classes = re.findall('<figure  class="(.*?)"', f)[0].split(' ')

        line = ''

        if classes[2] == 'thumb-sfw':
            line += '0,'
        if classes[2] == 'thumb-sketchy':
            line += '1,'
        if classes[2] == 'thumb-nsfw':
            line += '2,'

        if classes[3] == 'thumb-general':
            line += '0,'
        if classes[3] == 'thumb-anime':
            line += '1,'
        if classes[3] == 'thumb-people':
            line += '2,'

        line += re.findall('data-src="(.*?)"', f)[0]

        with open(f'{spider_path}/wallhaven.csv', 'a') as f:
            f.write(line + '\n')
    
def fetch_page_text(page):
    try:
        params = {
            'categories': '111',
            'purity': '111',
            'ratios': '16x9',
            'sorting': 'random',
            'order': 'desc',
            'seed': 'fahurq',
            'page': page
        }
        text = requests.get(host, params=params, headers=headers).text
    except Exception as e:
        print(str(e))
        return None
    return text

def spide(page) -> bool:
    text = fetch_page_text(page)
    if text == None:
        return False
    
    handle_page_text(text)

def main():

    global current_page

    print(f'Task from page: {current_page}')

    while current_page <= final_page:

        if spide(current_page) == False:
            print(f'Page{current_page} Failure')
            time.sleep(60)
            continue
                
        print(f'Page{current_page} Success')

        current_page += 1

        time.sleep(5)

    print('Task done!!!')

if __name__ == '__main__':
    main()    

