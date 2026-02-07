import os
from pathlib import Path

import pandas as pd
import torch
from torchvision.transforms import v2
from torch import nn
from torch.utils.data import DataLoader

from backend.inference.dataset import PetDataset
from backend.inference.trainer import Trainer
from backend.inference.efficientnet_v2_s import EfficientNetV2
from backend.inference.metrics import acc_fn


if __name__ == '__main__':

    BATCH_SIZE = 32

    device = 'cuda' if torch.cuda.is_available() else 'cpu'

    print('[SYSTEM] Device being used: ', device)
    data_path = Path(__file__).parent / 'data'
    csv_path = data_path / 'data.csv'
    df = pd.read_csv(csv_path)

    transforms = v2.Compose(
        [
            v2.Resize((224, 224)),
            v2.RandomHorizontalFlip(),
            v2.RandomVerticalFlip(),
            v2.ColorJitter(
                brightness=0.1,
                contrast=0.1,
                saturation=0.05,
                hue=0.02
            )
        ]
    )
        
    train_data = PetDataset(df, data_path, 'train', transform=transforms)
    val_data = PetDataset(df, data_path, 'val', transform=transforms)

    train_dataloader = DataLoader(dataset=train_data, batch_size=BATCH_SIZE, shuffle=True, num_workers=os.cpu_count())
    val_dataloader = DataLoader(dataset=val_data, batch_size=BATCH_SIZE, shuffle=True, num_workers=os.cpu_count())
              
    model = EfficientNetV2(num_classes=len(train_data.class_name_to_idx))

    loss_fn = nn.CrossEntropyLoss()
    optim = torch.optim.Adam(model.parameters(), lr=0.001)
    model_path = Path(__file__).parent / 'models'
    model_path.mkdir(parents=True, exist_ok=True)
    trainer = Trainer(epochs=100,
                      model=model,
                      model_name='EfficientNetV2',
                      train_dataloader=train_dataloader,
                      val_dataloader=val_dataloader,
                      optimizer=optim,
                      output_path=model_path,
                      loss_fn=loss_fn,
                      acc_fn=acc_fn,
                      device=device)        
    trainer.train()