from backend.inference.efficientnet_v2_s import EfficientNetV2
from pathlib import Path

import pandas as pd
import torch

from backend.inference.dataset import PetDataset

DF = pd.read_csv(Path(__file__).parent / 'inference' / 'data' / 'data.csv')
IDX_TO_CLASSNAME = {idx_class_name : class_name
                    for idx_class_name, class_name in enumerate(DF['class'].sort_values().unique().tolist())}

def predict(image_path):
    data_path = Path(__file__).parent / 'data'
    csv_path = data_path / 'data.csv'
    df = pd.read_csv(csv_path)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = EfficientNetV2(num_classes=18)
    model_path = Path(__file__).parent / 'inference' / 'models' / 'best.pth'
    model.load_state_dict(torch.load(model_path, map_location=device))
    model.eval()
    with torch.inference_mode():
        image = torch.load(image_path).unsqueeze(0)
        logits = model(image)
        predicted_class_idx = logits.softmax(dim=1).argmax(dim=1).item()
    return IDX_TO_CLASSNAME[predicted_class_idx]