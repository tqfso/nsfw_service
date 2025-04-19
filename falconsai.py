import os
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
        
        img = Image.open(filename)

        result = {}
        out = self.classifier(img)
        for data in out:
            if data['score'] >= 0.5:
                result['label'] = data['label']
                result['score'] = data['score']
                break

        return result
        