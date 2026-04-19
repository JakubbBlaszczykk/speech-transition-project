from pathlib import Path

import torch

from src.data.loader import LABELS
from src.data.preprocessing import extract_features
from src.model.cnn import CNNModel

ID_TO_LABEL = {value: key for key, value in LABELS.items()}


class LanguageClassifier:
    def __init__(self, model_path, device=None):
        self.model_path = Path(model_path)
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.model = self._load_model()

    def _load_model(self):
        model = CNNModel().to(self.device)

        dummy = torch.zeros((1, 1, 80, 94), dtype=torch.float32, device=self.device)
        model(dummy)

        state_dict = torch.load(self.model_path, map_location=self.device)
        if isinstance(state_dict, dict) and "model_state_dict" in state_dict:
            state_dict = state_dict["model_state_dict"]

        model.load_state_dict(state_dict)
        model.eval()
        return model

    def predict_proba(self, audio_path):
        features = extract_features(audio_path, random_crop=False)
        tensor = torch.tensor(features, dtype=torch.float32).unsqueeze(0).unsqueeze(0)
        tensor = tensor.to(self.device)

        with torch.no_grad():
            logits = self.model(tensor)
            probabilities = torch.softmax(logits, dim=1).cpu().numpy()[0]

        return {
            ID_TO_LABEL[index]: float(probability)
            for index, probability in enumerate(probabilities)
        }

    def predict(self, audio_path):
        probabilities = self.predict_proba(audio_path)
        label = max(probabilities, key=probabilities.get)
        return {
            "language": label,
            "confidence": probabilities[label],
            "probabilities": probabilities,
        }
