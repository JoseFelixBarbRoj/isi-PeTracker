from backend.inference.efficientnet_v2_s import EfficientNetV2
from pathlib import Path

import numpy as np
import torch
import cv2

IDX_TO_CLASSNAME = {
    0: "beagle",
    1: "bengal",
    2: "boxer",
    3: "british_shorthair",
    4: "bulldog",
    5: "chihuahua",
    6: "dachshund",
    7: "doberman",
    8: "husky",
    9: "labrador",
    10: "maine_coon",
    11: "persian",
    12: "pomeranian",
    13: "poodle",
    14: "ragdoll",
    15: "retriever",
    16: "siamese",
    17: "spaniel",
}

def predict(model, image_path, device):
    model.eval()
    model.to(device)
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