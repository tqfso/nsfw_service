
# 下载爬到的图片，保存到本地的文件名规则：级别_类型_XX

import requests
import os
import time
import spider

print(f'current path: {os.getcwd()}')

# 创建图片下载目录
path = "data/images"
os.makedirs(path, exist_ok=True)

def fetch_image_content(url):
    try:
        content = requests.get(url=url).content        
    except Exception as e:
        return None

    return content

def main():
    with open(spider.file_name) as f:

        lines = f.readlines()
        for index, line in enumerate(lines):
            parts = line.strip().split(',')
            levels = parts[0]
            types = parts[1]
            url = parts[2]

            fname = url.replace('https://th.wallhaven.cc/orig/', '').replace('/', '_')
            fpath = f'{path}/{levels}_{types}_{fname}'

            # 只下载不合规图片
            # if levels == '0':
            #     continue

            # 文件存在则跳过
            if os.path.exists(fpath):
                continue

            print(f'Download_{index}: {fname}')

            content = fetch_image_content(url)
            if content == None:
                print("Failure")
                time.sleep(30)
                continue
            else:
                print("Success")            

            with open(fpath, 'wb') as f:
                f.write(content)
            
            time.sleep(1)

if __name__ == '__main__':
    main()