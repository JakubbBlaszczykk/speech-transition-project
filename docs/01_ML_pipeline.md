# 01. ML Model Pipeline

## 1. Problem Definition

The goal of this project is to build a model capable of **classifying spoken language** from short audio samples.
We focus on three classes:

* Polish (pl)
* Portuguese (pt)
* English (en)

The input is raw audio (`.mp3`), and the output is a predicted language label.

---

## 2. Initial Approach

### Dataset

We started with a small dataset:

* ~200 samples per language
* Total: ~600 audio files

### Preprocessing (Initial Version)

Each audio file was:

1. Loaded with a sampling rate of 16 kHz
2. Trimmed to a random 3-second segment
3. Converted to **Mel Spectrogram**
4. Normalized

### Model

A simple CNN was used:

* 3 convolutional layers
* 2 fully connected layers
* ReLU activation
* No regularization

---

## 3. First Results — Overfitting

### Observations

The model achieved:

* Training loss → ~0.0006
* Test accuracy → ~96–97%

At first glance, the results seemed excellent.

### Problem

However, this was a clear case of **overfitting**:

* The dataset was too small
* The model memorized patterns instead of generalizing
* Performance was not reliable for unseen data

---

## 4. Dataset Expansion

To address overfitting, we increased dataset size:

* ~600 samples per class
* Total: ~1500 samples

### Impact

After retraining:

* Accuracy dropped to ~85–87%
* Loss increased significantly

### Interpretation

This was expected:

* The task became more realistic
* The model could no longer memorize data
* Generalization became the main challenge

---

## 5. Preprocessing Improvements

### Issue: Inconsistent Input Shapes

We encountered a critical error:

```text
RuntimeError: stack expects each tensor to be equal size
```

Cause:

* Different spectrogram sizes (e.g. 80 vs 128 mel bins)

### Solution

We standardized preprocessing:

* Fixed Mel Spectrogram parameters
* Ensured consistent shape across all samples
* Added safe normalization:

```python
std = np.std(spec_db)
if std == 0:
    std = 1e-6
```

---

## 6. Feature Engineering

We enhanced input representation:

### MFCC + Delta

Instead of raw Mel Spectrograms:

* Extracted MFCC features
* Added delta (temporal change)

This improved:

* Temporal sensitivity
* Phonetic pattern recognition

---

## 7. Regularization and Stability

### Applied Techniques

* Dropout (0.3 → later 0.2)
* Batch Normalization
* Lower learning rate (0.0005)

### Attempt: Class Weights

We experimented with class weighting due to slight imbalance:

* pl: 440
* pt: 466
* en: 546

Result:

* Accuracy dropped (~78%)
* Training became unstable

Conclusion:

* Class imbalance was too small to justify weighting

---

## 8. Model Scaling

### Initial Model Limitation

The model struggled to distinguish:

* Polish vs Portuguese

### Solution: Increase Capacity

Final architecture:

* 4 convolutional layers
* Channels: 32 → 64 → 128 → 256
* BatchNorm after each layer
* Dropout (0.2)
* Larger fully connected layer (256 units)

---

## 9. Final Results

After all improvements:

* Loss: ~0.013
* Test Accuracy: ~92.4%

### Confusion Matrix Insights

* English: most stable class (~92–93%)
* Polish: ~94%
* Portuguese: ~90%
* Most confusion: Polish ↔ Portuguese

---

## 10. Key Lessons

### 1. High accuracy can be misleading

Initial ~97% accuracy was caused by overfitting.

---

### 2. More data reduces apparent performance

Increasing dataset size exposed true model limitations.

---

### 3. Feature quality matters

MFCC + delta significantly improved performance over raw spectrograms.

---

### 4. Model capacity is critical

A larger CNN was necessary to capture subtle phonetic differences.

---

### 5. Not all techniques help

Class weighting degraded performance due to low imbalance.

---

## 11. Final Pipeline

```text
Audio (.mp3)
   ↓
Load (16 kHz)
   ↓
Random 3-second segment
   ↓
MFCC + Delta extraction
   ↓
Normalization
   ↓
CNN (4 layers + BatchNorm + Dropout)
   ↓
Fully Connected Layers
   ↓
Language Prediction
```

---

## 12. Summary

The final model achieves strong performance on a realistic dataset and generalizes well across languages. The main remaining challenge is distinguishing acoustically similar languages, which may require further architectural improvements or more advanced feature extraction in future work.
