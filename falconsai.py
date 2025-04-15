import os
import error
from error import Error
from PIL import Image
from transformers import pipeline

class Model:

    def __init__(self):
        pass

    def __str__(self):
        return f'{self.classifier}'
    
    def load(self,path):

        print("Load model:", path)

        try:
            self.classifier = pipeline("image-classification", model=path)
            print("Success")
            return True
        except Exception as ex:
            print("Failure:", ex)
            return False
     
    def process(self,filename):
        '''
        The NSFW score is returned after inference based on the picture path. A negative number indicates inference failure
        '''
                
        if os.path.exists(filename) == False:
            raise Error(error.FILE_NOT_FOUND, f"file not found:{filename}")
        
        img = Image.open(filename)

        # [{'label': 'normal', 'score': 0.9997023940086365}, {'label': 'nsfw', 'score': 0.00029755846480838954}]
        out = self.classifier(img)
        for result in out:
            if result['score'] > 0.8:
                return result['label']
        return 'unknown'
        