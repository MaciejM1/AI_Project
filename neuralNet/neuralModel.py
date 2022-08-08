import os

import torch
import torch.nn as nn
from torchvision.transforms import transforms
from torch.utils.data import DataLoader
import numpy as np
from torch.autograd import Variable
from torchvision.models import squeezenet1_1
import torch.functional as F
from io import open
from PIL import Image
import torch.optim
import glob

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
torch.cuda.empty_cache()

transformer = transforms.Compose([
    transforms.Resize((150, 150)),
    transforms.ToTensor(),
    transforms.Normalize([0.5, 0.5, 0.5], [0.5, 0.5, 0.5])
])

classes = ['bio', 'glass', 'paper', 'plastic']


class ConvNet(nn.Module):
    def __init__(self, num_classes=4):
        super(ConvNet, self).__init__()

        self.conv1 = nn.Conv2d(in_channels=3, out_channels=12, kernel_size=3, stride=1, padding=1)
        self.bn1 = nn.BatchNorm2d(num_features=12)
        self.relu1 = nn.ReLU()

        self.pool = nn.MaxPool2d(kernel_size=2)

        self.fc = nn.Linear(in_features=75 * 75 * 12, out_features=num_classes)

    def forward(self, input):
        output = self.conv1(input)
        output = self.bn1(output)
        output = self.relu1(output)

        output = self.pool(output)

        output = output.view(-1, 12 * 75 * 75)

        output = self.fc(output)

        return output


model = ConvNet(num_classes=4)

optimizer = torch.optim.Adam(model.parameters(), lr=0.001, weight_decay=0.0001)
lossFunction = nn.CrossEntropyLoss()
path = os.path.dirname(__file__)
checkpoint = torch.load(path + '\\best_checkpoint.model', map_location=torch.device('cpu'))
model = ConvNet(num_classes=4)
model.load_state_dict(checkpoint)
model.eval()


# ConvNet(
#   (conv1): Conv2d(3, 12, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
#   (bn1): BatchNorm2d(12, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)
#   (relu1): ReLU()
#   (pool): MaxPool2d(kernel_size=2, stride=2, padding=0, dilation=1, ceil_mode=False)
#   (fc): Linear(in_features=67500, out_features=4, bias=True)
# )

def prediction(img_path, transformer):
    image = Image.open(img_path)

    image_tensor = transformer(image).float()

    image_tensor = image_tensor.unsqueeze_(0)

    if torch.cuda.is_available():
        image_tensor.cuda()

    input = Variable(image_tensor)

    output = model(input)

    index = output.data.numpy().argmax()

    pred = classes[index]

    return pred
