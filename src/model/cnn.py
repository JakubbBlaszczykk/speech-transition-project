import torch
import torch.nn as nn
import torch.nn.functional as F

class CNNModel(nn.Module):
    def __init__(self):
        super().__init__()

        # Convolutional layers
        self.conv1 = nn.Conv2d(1, 16, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(16, 32, kernel_size=3, padding=1)
        self.conv3 = nn.Conv2d(32, 64, kernel_size=3, padding=1)

        self.pool = nn.MaxPool2d(2, 2)

        # fully connected
        self.fc1 = nn.Linear(64 * 16 * 11, 128)
        self.fc2 = nn.Linear(128, 3)

    def forward(self, x):
        # x: (batch, 1, 128, ~100)

        x = self.pool(F.relu(self.conv1(x)))  # (16, 64, ~50)
        x = self.pool(F.relu(self.conv2(x)))  # (32, 32, ~25)
        x = self.pool(F.relu(self.conv3(x)))  # (64, 16, ~12)

        x = x.view(x.size(0), -1)

        x = F.relu(self.fc1(x))
        x = self.fc2(x)

        return x