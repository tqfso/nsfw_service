import requests
import os
import time

print(os.getcwd())

# 创建图片下载目录
download_path = "data/images"
os.makedirs(download_path, exist_ok=True)

def fetch_image_content(url):
    try:
        content = requests.get(url=url).content        
    except Exception as e:
        return None

    return content

def main():
    with open('data/wallhaven.csv') as f:

        lines = f.readlines()
        for line in lines:
            parts = line.strip().split(',')
            levels = parts[0]
            types = parts[1]
            url = parts[2]

            fname = url.replace('https://th.wallhaven.cc/orig/', '').replace('/', '_')
            fpath = f'{download_path}/{levels}_{types}_{fname}'

            print(f'Download:{fname}')

            # 文件存在则跳过
            if os.path.exists(fpath):
                continue

            content = fetch_image_content(url)
            if content == None:
                print("Failure")
                time.sleep(60)
                continue
            else:
                print("Success")            

            with open(fpath, 'wb') as f:
                f.write(content)
            
            time.sleep(3)

if __name__ == '__main__':
    main()