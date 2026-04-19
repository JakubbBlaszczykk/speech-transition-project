import torch
import torch.nn as nn
import torch.nn.functional as F


class CNNModel(nn.Module):
    def __init__(self):
        super().__init__()

        # Convolutional layers with increased capacity
        self.conv1 = nn.Conv2d(1, 32, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, padding=1)
        self.conv3 = nn.Conv2d(64, 128, kernel_size=3, padding=1)
        self.conv4 = nn.Conv2d(128, 256, kernel_size=3, padding=1)

        # Batch normalization layers for training stability
        self.bn1 = nn.BatchNorm2d(32)
        self.bn2 = nn.BatchNorm2d(64)
        self.bn3 = nn.BatchNorm2d(128)
        self.bn4 = nn.BatchNorm2d(256)

        # Max pooling to reduce spatial dimensions
        self.pool = nn.MaxPool2d(2, 2)

        # Dropout for regularization
        self.dropout = nn.Dropout(0.2)

        # Fully connected layers (initialized dynamically)
        self.fc1 = None
        self.fc2 = None

    def _initialize_fc(self, x):
        # Flatten input and determine number of features
        x = x.view(x.size(0), -1)
        in_features = x.shape[1]

        # Define fully connected layers based on computed size
        self.fc1 = nn.Linear(in_features, 256)
        self.fc2 = nn.Linear(256, 3)

    def forward(self, x):
        # Apply convolution, batch normalization, activation and pooling
        x = self.pool(F.relu(self.bn1(self.conv1(x))))
        x = self.pool(F.relu(self.bn2(self.conv2(x))))
        x = self.pool(F.relu(self.bn3(self.conv3(x))))
        x = self.pool(F.relu(self.bn4(self.conv4(x))))

        # Initialize fully connected layers during first forward pass
        if self.fc1 is None:
            self._initialize_fc(x)

        # Flatten before fully connected layers
        x = x.view(x.size(0), -1)

        # Apply fully connected layers with dropout
        x = self.dropout(F.relu(self.fc1(x)))
        x = self.fc2(x)

        return x