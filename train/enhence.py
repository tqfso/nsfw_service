
# 数据增强，违规图片和正常图片数量保持差不多

import os
import download
import spider
from PIL import Image

path = "data/enhences"
os.makedirs(path, exist_ok=True)

# 获取不同等级的图片数量
def stats_levels():
    l0,l1,l2 = 0,0,0
    with open(spider.file_name) as f:
        lines = f.readlines()
        for line in lines:
            parts = line.strip().split(',')
            level = parts[0]
            if level == '0':
                l0 += 1
            elif level == '1':
                l1 += 1
            elif level == '2':
                l2 += 1

    return (l0, l1, l2)

def main():

    # 提前统计，正常图片是违规图片的3倍左右
    stats = stats_levels()
    print(f'dataset dis: {stats}')

    for file in os.listdir('pic'):
        if 'copy' in file or 'flip' in file:
            continue
        if file[0] == '0':
            continue

        print(file)
        
        im = Image.open(download.path + file)
        im.save(path + file[:-4] + '_copy.jpg')
        im = im.transpose(Image.FLIP_LEFT_RIGHT)
        im.save(path + file[:-4] + '_flip.jpg')
        im.save(path + file[:-4] + '_flip_copy.jpg')

if __name__ == "main":
    main()