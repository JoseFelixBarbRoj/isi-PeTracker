from backend.inference.efficientnet_v2_s import EfficientNetV2
from pathlib import Path

import numpy as np
import pandas as pd
import torch
import cv2

DF = pd.read_csv(Path(__file__).parent / 'inference' / 'data' / 'data.csv')
IDX_TO_CLASSNAME = {idx_class_name : class_name
                    for idx_class_name, class_name in enumerate(DF['class'].sort_values().unique().tolist())}

def predict(image_path):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = EfficientNetV2(num_classes=18)
    model_path = Path(__file__).parent / 'inference' / 'models' / 'best.pth'
    model.load_state_dict(torch.load(model_path, map_location=device))
    model.eval()
    with torch.inference_mode():
        image = cv2.imread(str(image_path), cv2.IMREAD_COLOR_RGB)
        if image is None:
            return None
        image = image.transpose(2, 0, 1).astype(np.float32)
        image /= 255.0
        image_tensor = torch.from_numpy(image).unsqueeze(0).to(device)
        logits = model(image_tensor)
        predicted_class_idx = logits.softmax(dim=1).argmax(dim=1).item()
    return IDX_TO_CLASSNAME[predicted_class_idx]