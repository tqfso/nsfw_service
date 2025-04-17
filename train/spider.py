import time
import requests
import re
import os
import sys

print(os.getcwd())

host = 'https://wallhaven.cc/search'
spider_path = "data"
current_page = 2
final_page = 1000

if len(sys.argv) >= 2:
    current_page = int(sys.argv[1])

headers = {
    'accept': 'text/html, */*; q=0.01',
    'cookie': 'remember_web_59ba36addc2b2f9401580f014c7f58ea4e30989d=eyJpdiI6ImtxZVpnQlQ5MjV5N3pGbXNocVIwZGc9PSIsInZhbHVlIjoibkg1QXpSVyttR1BES1kyTFE4T1IxVUpwU0M3YURwc0E4UnAyd1ZpZFg4SW1kUkQ0VFwvbkQ4SXR2RWFVRVhtZmRTMER4b1MxY3Q2WHZHeUZMSlVZSjliMFNzSVY4eStSYWs5RTJrZm0zTXJBZXVleUN6MTc2dTNqNHM0blFIXC9LNTBUbDhvaERLT2tCZkQ1Y0xZTWI3ZUVVdGxjNTlJT0VtQWN3SGpjaEZhbnM9IiwibWFjIjoiMGZlNTA5ZjA2MjA3NzU5NjEzZGVjM2YyY2NiNmNkZTkwMDVmMDYwY2VlZjk4MmY3ZmRmZjcyNmRlMTY2NGIwMCJ9; _pk_id.1.01b8=c6a37b55ce63dc75.1636800243.; XSRF-TOKEN=eyJpdiI6IkZGcXpQTmtab1wvQlB5NWpxYXgybTZnPT0iLCJ2YWx1ZSI6IjllQ0F5aG45TzhrRzc2bGFBUGptNlZKUUpFYlQwbnZINmZaTDFvXC9zcFNyUEx3Wm14cEMrbEVEY29rQXIwUzN1IiwibWFjIjoiMzg1ZjZkOThlNjNiNGIwMmI2MTA0ZGQyOGQ0YTRlYzEzMDFkZjY5YWU1NTczN2NmNWI1Nzc0NzliZWZhYTk3ZSJ9; wallhaven_session=eyJpdiI6IndwUGlDQUdPemtUdURMdUJJanczQ2c9PSIsInZhbHVlIjoiYmJiWnNnNitDMEM5ZmlWbVAxNE5FRjIrQW9WQnFCRGtUakpFSUdvQ0pRYkM5aFwvb281UlY3Mng0ajNVT3lKMkkiLCJtYWMiOiIxZjk2NTFkNWMzYjU4YTlkM2ZmMWM0YmUyY2NiMDM5ZDYwYzViMTQ4NGNjMGY2YmYxMDM2ZjhlNzk0MjVlODZiIn0%3D',
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

    print(f'Spide from page: {current_page}')

    while current_page <= final_page:

        if spide(current_page) == False:
            print(f'Page{current_page} Failure')
            time.sleep(60)
            continue
                
        print(f'Page{current_page} Success')

        current_page += 1

        time.sleep(3)

    print('Spide done!!!')

if __name__ == '__main__':
    main()    

