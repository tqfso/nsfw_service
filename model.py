import os
import torch
from PIL import Image
from transformers import AutoModelForImageClassification, ViTImageProcessor

class Model:

    def __init__(self):
        pass

    def __str__(self):
        return f'{self.model}'
    
    def load(self,path):

        print("Load model:", path)

        try:
            self.model = AutoModelForImageClassification.from_pretrained(path)
            self.processor = ViTImageProcessor.from_pretrained(path)
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
        with torch.no_grad():            
            inputs = self.processor(images=img, return_tensors="pt")
            outputs = self.model(**inputs)
            logits = outputs.logits

        predicted_label = logits.argmax(-1).item()
        return self.model.config.id2label[predicted_label]
        