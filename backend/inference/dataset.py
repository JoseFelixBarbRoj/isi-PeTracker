from pathlib import Path

import pandas as pd
import cv2
import torch
from torch.utils.data import Dataset
import numpy as np

class PetDataset(Dataset):
    def __init__(self, df: pd.DataFrame, dataset_path: str | Path, partition: str, transform: torch.nn.Module | None = None):
        self.dataset_path = Path(dataset_path)
        self.partition = partition

        self.class_name_to_idx: dict[str, int] = {class_name: idx_class_name
                                                  for idx_class_name, class_name in enumerate(df['class'].sort_values().unique().tolist())}
        self.class_idx_to_name: dict[int, str] = {idx_class_name: class_name for class_name, idx_class_name in self.class_name_to_idx.items()}

        self.df = df[df['partition'] == self.partition]
        self.transform = transform


    def __getitem__(self, idx_item: int) -> tuple[torch.Tensor, int]:
       data_item = self.df.iloc[idx_item]

       image = cv2.imread(self.dataset_path / data_item['path'], cv2.IMREAD_COLOR_RGB).transpose(2, 0, 1).astype(np.float32)
       image /= 255
       image = torch.from_numpy(image).to(torch.get_default_dtype())

       if self.transform:
           image = self.transform(image)

       return image, self.class_name_to_idx[data_item['class']]
    
    def __len__(self):
        return len(self.df)