from math import ceil

from torch import nn
from torchvision.models.efficientnet import efficientnet_v2_s

class EfficientNetV2(nn.Module):
    def __init__(self, num_classes):
        super().__init__()
        self.net = efficientnet_v2_s()
        self.head = nn.Sequential(
            nn.ReLU(),
            nn.Dropout(p=0.1),
            nn.Linear(in_features=1000, out_features=num_classes)
        )
    def forward(self, x):
        x = self.net(x)
        return  self.head(x)