import os
import numpy as np
import torch
from torch.utils.data import Dataset
import random

LABELS = {
    "pl": 0,
    "pt": 1,
    "en": 2
}


class LanguageDataset(Dataset):
    def __init__(self, root_dir):
        self.data = []

        for lang in LABELS:
            folder = os.path.join(root_dir, lang)

            for file in os.listdir(folder):
                if file.endswith(".npy"):
                    path = os.path.join(folder, file)
                    label = LABELS[lang]

                    self.data.append((path, label))

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        path, label = self.data[idx]

        x = np.load(path)
        x = torch.tensor(x, dtype=torch.float32)

        # augumentaation: add noise with 50% probability
        if random.random() < 0.5:
            x = x + 0.005 * torch.randn_like(x)

        # add channel dimension 
        x = x.unsqueeze(0)

        y = torch.tensor(label, dtype=torch.long)

        return x, y