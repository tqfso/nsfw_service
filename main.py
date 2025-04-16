import os

from flask import Flask, request, jsonify
from falconsai import Model
from error import Error,Code

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
        result = model.process(filepath)
        response = {
            'result': result,
            'code': 0
        }
        return jsonify(response)

    except Error as e:
        response = {
            'result': "failed",
            'code': e.code,
            'msg': e.msg
        }
        return jsonify(response)

    except Exception as e:
        response = {
            'result': "failed",
            'code': Code.FAILURE,
            'msg': str(e)
        }
        return jsonify(response)    
        
    finally:
        print(f'{filename}: {response}')
        

@app.route('/detect/video', methods=['POST'])
def video_handler():
    pass
        
def main():
    print(f'Start Service, Root Path: {file_path}')

    if model.load(model_path) == False:
        return
    app.run(host="0.0.0.0", port=5000, debug=True)
    
    print("Exit")

if __name__ == '__main__':
    main()