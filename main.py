import os
import cv2
import hashlib

from flask import Flask, request, jsonify
from falconsai import Model

app = Flask(__name__)
model = Model()
file_path = os.getenv("FILE_PATH","./data")
model_path = os.getenv("MODEL_PATH","./model/Falconsai")

@app.route('/detect/image', methods=['POST'])
def image_handler():
    try:
        data = request.get_json()
        filename = data.get('filename', '')        
        filepath = os.path.join(file_path, filename)
        if os.path.exists(filepath) == False:
            raise Exception("file not found")
        
        result = model.process(filepath)
        response = {
            'stats': result,
        }
        return jsonify(response)

    except Exception as e:
        response = {
            'stats': "failed",
            'message': str(e)
        }
        return jsonify(response)    
        
    finally:
        print(f'{filename}: {response}')
        

@app.route('/detect/video', methods=['POST'])
def video_handler():
    try:
        data = request.get_json()
        filename = data.get('filename', '')        
        filepath = os.path.join(file_path, filename)
        if not os.path.exists(filepath):
            raise Exception("File not found")
        
        cap = cv2.VideoCapture(filepath)
        if not cap.isOpened():
            raise Exception("Failed to open video")
        
        fps = int(cap.get(cv2.CAP_PROP_FPS)) #每秒帧数
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) #总帧数
        if fps == 0 or frame_count == 0:
            raise Exception("Invalid video file")
        
        # 计算抽帧间隔：至少1秒抽1帧，最多抽64帧
        frame_interval = max(int(fps), frame_count // 64)
        frame_indices = list(range(0, frame_count, frame_interval))[:64]
        detail = {"nsfw": 0, "normal": 0, "unknown": 0}

        # 使用文件名 hash 作为帧图文件名前缀
        file_hash = hashlib.md5(filepath.encode('utf-8')).hexdigest()

        # 创建视频解码目录
        frame_dir = "./data/frames"
        os.makedirs(frame_dir, exist_ok=True) 

        for frame_id in frame_indices:
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_id)
            success, frame = cap.read()
            if not success:
                continue

            temp_path = f"{frame_dir}/temp_{file_hash}_{frame_id}.jpg"
            cv2.imwrite(temp_path, frame)

            label = model.process(temp_path)
            detail[label] = detail.get(label, 0) + 1

            if os.path.exists(temp_path):
                os.remove(temp_path)
                pass

        cap.release()

        result = max(detail, key=detail.get)
        response = {
            'stats': result,
            'detail': detail
        }
        return jsonify(response)
    except Exception as e:
        response = {
            'stats': "failed",
            'message': str(e)
        }
        return jsonify(response)    
        
    finally:
        print(f'{filename}: {response}')

def main():
    print(f'Start Service, Root Path: {file_path}')

    if model.load(model_path) == False:
        return
    app.run(host="0.0.0.0", port=5000, debug=True)
    
    print("Exit")

if __name__ == '__main__':
    main()