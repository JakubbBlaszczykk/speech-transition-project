# 02. Speech-to-Speech Pipeline

## 1. Goal

The goal of this stage was to extend the custom language classification model into a complete **speech-to-speech system**.

The target pipeline is:

```text
Input audio (.mp3)
   ↓
Language identification
   ↓
Speech-to-text (ASR)
   ↓
Machine translation
   ↓
Text-to-speech (TTS)
   ↓
Output audio (.mp3)

The system currently works for three languages:
- Polish (pl)
- English (en)
- Portuguese (pt)
```
## 2. General System Architecture
The implemented pipeline consists of four main stages:

### 1. Language Identification
The first stage uses the custom CNN-based classifier developed earlier in the project.

Its task is to identify the spoken language from the input audio file and return one of the supported classes:

- pl
- en
- pt
This is the **custom machine learning component** of the project.

### 2. Automatic Speech Recognition (ASR)
After detecting the language, the audio is transcribed into text using **Whisper**.

The predicted language is passed to the ASR module as a hint, so transcription is performed in the detected source language.

### 3. Translation
The transcribed text is translated from the detected source language to the target language.

At the current stage, translation is handled by an external translation library.

### 4. Text-to-Speech (TTS)
Finally, the translated text is converted back into speech and saved as an output audio file.
```
# 02. Speech-to-Speech Pipeline

## 1. Goal

The goal of this stage was to extend the custom language classification model into a complete **speech-to-speech system**.

The target pipeline is:

```text
Input audio (.mp3)
   ↓
Language identification
   ↓
Speech-to-text (ASR)
   ↓
Machine translation
   ↓
Text-to-speech (TTS)
   ↓
Output audio (.mp3)
```

The system currently works for three languages:

* Polish (`pl`)
* English (`en`)
* Portuguese (`pt`)

---

## 2. General System Architecture

The implemented pipeline consists of four main stages:

### 1. Language Identification

The first stage uses the custom CNN-based classifier developed earlier in the project.

Its task is to identify the spoken language from the input audio file and return one of the supported classes:

* `pl`
* `en`
* `pt`

This is the **custom machine learning component** of the project.

### 2. Automatic Speech Recognition (ASR)

After detecting the language, the audio is transcribed into text using **Whisper**.

The predicted language is passed to the ASR module as a hint, so transcription is performed in the detected source language.

### 3. Translation

The transcribed text is translated from the detected source language to the target language.

At the current stage, translation is handled by an external translation library.

### 4. Text-to-Speech (TTS)

Finally, the translated text is converted back into speech and saved as an output audio file.

---

## 3. Implemented Modules

The speech-to-speech system was divided into modular components.

### `src/model/inference.py`

Responsible for:

* loading the trained CNN model
* preprocessing a single audio file
* predicting source language
* returning confidence and class probabilities

### `src/pipeline/asr.py`

Responsible for:

* loading Whisper
* transcribing input speech into text

### `src/pipeline/translator.py`

Responsible for:

* translating text from source language to target language

### `src/pipeline/tts.py`

Responsible for:

* generating output speech from translated text

### `src/pipeline/speech_to_speech.py`

Responsible for:

* connecting all previous modules into one end-to-end pipeline

---

## 4. Processing Flow

The implemented processing flow is:

1. Load input `.mp3` file
2. Detect spoken language with the custom classifier
3. Transcribe speech using Whisper
4. Translate transcript into the target language
5. Generate translated speech as output `.mp3`

This means the project already supports an end-to-end **audio-to-audio translation workflow** for file input.

---

## 5. Example Workflow

Example scenario:

* input: Polish speech recording
* detected language: `pl`
* transcription: Polish text
* translation target: English
* output: synthesized English speech

In practice, the system can perform tasks such as:

* `pl -> en`
* `pt -> en`
* `en -> pl`
* `en -> pt`

depending on the chosen target language.

---

## 6. Testing and Observations

The pipeline was tested on manually selected audio samples for all three supported languages.

### Positive results

* the end-to-end pipeline works correctly for `.mp3` input files
* Whisper transcription works correctly for verified test recordings
* translation and TTS stages produce valid output audio files
* English and Portuguese examples produced good end-to-end results

### Main issue observed

The largest source of errors was not the pipeline integration itself, but the **language classification stage**.

In some cases:

* the classifier confused Polish with English
* confidence values for Portuguese were relatively low
* errors in language identification propagated to the ASR stage

This means that the overall quality of the system depends strongly on the quality of the initial language detection.

---

## 7. Dataset Quality Issue

During testing, an important issue was discovered in the dataset:

* some recordings inside language folders appeared to contain speech in the wrong language
* this suggests that the dataset is at least partially **noisy or mislabeled**

This observation is important because noisy labels can directly reduce classifier performance.

As a result:

* part of the classification error may come from model limitations
* part of it may come from incorrect training data labels

This should be treated as an important limitation of the current system.

---

## 8. Current Project Status

At this stage, the project already includes a working **speech-to-speech pipeline for audio files**.

Implemented functionality:

* input from `.mp3` file
* language identification with a custom classifier
* speech transcription with Whisper
* text translation
* speech synthesis to output `.mp3`

This satisfies the core idea of a speech-to-speech system for file-based input.

---

## 9. Limitations

The current version still has several limitations:

* input works only for audio files, not microphone streaming
* system quality depends on the accuracy of the language classifier
* noisy or mislabeled training data can reduce classification performance
* external libraries are used for ASR, translation and TTS
* inference currently runs on CPU, which makes processing slower

---

## 10. Possible Future Improvements

The next logical improvements are:

### 1. Microphone input

Add recording from microphone instead of relying only on pre-recorded `.mp3` files.

### 2. Real-time audio playback

Play generated translated speech directly through speakers.

### 3. Better dataset curation

Clean mislabeled or noisy samples from the training data.

### 4. Improved language classifier

Train the classifier on cleaner and better-balanced data.

### 5. More robust evaluation

Prepare a larger manually verified test set for all supported languages.

---

## 11. Summary

This stage of the project successfully transformed the custom language classifier into a complete **speech-to-speech pipeline**.

The final system is able to:

* accept an audio file as input
* detect the spoken language
* transcribe the speech
* translate the content
* generate translated speech as output audio

The core original contribution remains the custom CNN-based language identification model, while external tools are used for ASR, translation and TTS.
