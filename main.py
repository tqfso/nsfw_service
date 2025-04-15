import os
import error

from flask import Flask, request, jsonify
from falconsai import Model
from error import Error

app = Flask(__name__)
model = Model()
file_path = os.getenv("FILE_PATH","./data/")
model_path = os.getenv("MODEL_PATH","./model/Falconsai")

@app.route('/detect/image', methods=['POST'])
def image_handler():
    try:
        data = request.get_json()
        filename = data.get('filename', '')
        filepath = file_path + filename
        result = model.process(filepath)
        response = {
            'detection': result,
            'code': 0
        }
        return jsonify(response), 200
    except Error as e:
        return jsonify({'code': e.code, 'msg': e.msg}), 400
    except Exception as e:
        return jsonify({'code': error.UNKNOWN, 'msg': str(e)}), 400

@app.route('/detect/video', methods=['POST'])
def video_handler():
    pass
        
def main():

    print(f'Start Service, Root Path: {file_path}')

    if model.load(model_path) == False:
        return

    app.run(host="0.0.0.0", port=5000, debug=False)
    
    print("Exit")

if __name__ == '__main__':
    main()