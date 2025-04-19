import os
import torch
import torchvision
import torchvision.transforms as transforms
from PIL import Image

class Trained(torch.nn.Module):
    def __init__(self):
        super().__init__()

        self.fc = torch.nn.Sequential(
            torch.nn.Linear(512, 512),
            torch.nn.ReLU(),
            torch.nn.Dropout(0.2),
            torch.nn.Linear(512, 2)
        )

    def forward(self, x):
        return self.fc(x)

class Model:

    def __init__(self):
        pass

    def __str__(self):
        return f'{self.model}'
    
    def load(self,path):

        print("Load model:", path)

        try:

            # 推理设备
            self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

            # 数据预处理器
            self.transform = transforms.Compose([
                lambda x: x.convert('RGB'),
                torchvision.transforms.Resize(256),
                torchvision.transforms.CenterCrop(224),
                transforms.ToTensor(),
                transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                    std=[0.229, 0.224, 0.225])
            ])

            # 使用预训练模型
            resnet = torchvision.models.resnet18(weights=None)
            resnet_state_dict = torch.load(f"{path}/resnet18-f37072fd.pth", weights_only=True, map_location=torch.device('cpu'))
            resnet.load_state_dict(resnet_state_dict)

            # 剪掉最后一层
            resnet = list(resnet.children())[:-1]
            self.resnet = torch.nn.Sequential(*resnet)
            self.resnet.eval()

            # 加载自己训练的分类器
            self.model = Trained()            
            state_dict = torch.load(f'{path}/model.mdl', weights_only=True, map_location=torch.device('cpu'))
            self.model.load_state_dict(state_dict)
            self.model.eval()
        
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
        out = self._predict_proba(img)
        result = {
            'label': "normal",
            'score': float(out[0])
        }

        if out[0] < 0.5:
            result['label'] = "nsfw"
            result['score'] = float(out[1])

        return result
                
    def _predict_proba(self, image):
        with torch.no_grad():
            img = self.transform(image)
            img = img.unsqueeze(0)
            features = self.resnet(img)
            features = features.view(features.size(0), -1)
            output = self.model(features)
            probs = torch.softmax(output, dim=1).cpu().numpy().flatten()
            return probs