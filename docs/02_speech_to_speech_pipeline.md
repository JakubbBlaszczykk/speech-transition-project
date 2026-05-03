# 02. Speech-to-Speech Pipeline

## 1. Goal

The goal of this stage was to extend the custom language classification model into a complete **speech-to-speech system**.

The target pipeline is:

```text
Input audio (.mp3 or microphone)
   -> Language identification
   -> Speech-to-text (ASR)
   -> Machine translation
   -> Text-to-speech (TTS)
   -> Output audio (.mp3)
```

The system currently works with three languages:

* Polish (`pl`)
* English (`en`)
* Portuguese (`pt`)

---

## 2. General System Architecture

The implemented pipeline consists of four main stages.

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

### `app/cli.py`

Responsible for:

* running the complete pipeline from the terminal
* accepting an input audio path, target language and optional output path
* printing a JSON summary of the result

### `app/api.py`

Responsible for:

* exposing the pipeline through a FastAPI backend
* accepting browser microphone recordings
* converting recorded audio into a pipeline-friendly format
* returning detected language, transcript, translation and output audio URL

---

## 4. Data Source

The language identification dataset used in this project was assembled from Mozilla Data Collective resources:

* [Common Voice Scripted Speech 25.0 - Polish](https://mozilladatacollective.com/datasets/cmn27nz69015hmm0720txf781)
* [Common Voice Scripted Speech 25.0 - Portuguese](https://mozilladatacollective.com/datasets/cmn29f4cb017bmm07pd9yd8mw)
* [Common Voice Spontaneous Speech 3.0 - English](https://mozilladatacollective.com/datasets/cmn1pv5hi00uto1072y1074y7)

The Common Voice datasets are published on Mozilla Data Collective as `ASR` datasets in `MP3` format under the `CC0-1.0` license.

During practical testing, some files appeared to be noisy or mislabeled, which is important because this can directly affect language classifier performance.

---

## 5. Web Interface

A simple frontend was added for demonstration purposes.

The frontend allows the user to:

* select a microphone input device
* record audio directly in the browser
* select the target language
* run the full speech-to-speech pipeline
* inspect the detected language and classifier confidence
* read the transcript and translated text
* play the generated output audio in the browser

The frontend was created with assistance from **Codex / AI** as a development support tool. The purpose of this interface is to make the existing speech-to-speech pipeline easier to test and present.

---

## 6. Processing Flow

The implemented processing flow is:

1. Load input `.mp3` file or browser microphone recording
2. Detect spoken language with the custom classifier
3. Transcribe speech using Whisper
4. Translate transcript into the target language
5. Generate translated speech as output `.mp3`

This means the project already supports an end-to-end **audio-to-audio translation workflow** for both file input and browser-based microphone recording.

---

## 7. Example Workflow

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

## 8. Testing and Observations

The pipeline was tested on manually selected audio samples for all three supported languages.

### Positive results

* the end-to-end pipeline works correctly for `.mp3` input files
* Whisper transcription works correctly for verified test recordings
* translation and TTS stages produce valid output audio files
* English and Portuguese examples produced good end-to-end results
* the FastAPI interface makes the system easier to demonstrate
* the browser frontend adds microphone-based interaction without changing the core pipeline
* in practical microphone tests, `pl -> en` produced good results and `pl -> pt` was also usable

### Main issue observed

The largest source of errors was not the pipeline integration itself, but the **language classification stage**.

In some cases:

* the classifier confused Polish with English
* confidence values for Portuguese were relatively low
* errors in language identification propagated to the ASR stage

This means that the overall quality of the system depends strongly on the quality of the initial language detection.

---

## 9. Dataset Quality Issue

During testing, an important issue was discovered in the dataset:

* some recordings inside language folders appeared to contain speech in the wrong language
* this suggests that the dataset is at least partially **noisy or mislabeled**

This observation is important because noisy labels can directly reduce classifier performance.

As a result:

* part of the classification error may come from model limitations
* part of it may come from incorrect training data labels

This should be treated as an important limitation of the current system.

---

## 10. Evaluation Limitations

The final practical evaluation also has a human-side limitation:

* the author is a native Polish speaker
* evaluation of English and Portuguese output was therefore less reliable than evaluation of Polish input and transcription
* because of this, directions such as `pl -> en` and `pl -> pt` could be tested functionally, but subtle errors in English and Portuguese fluency may still remain

This should be considered when interpreting the final demo results.

---

## 11. Current Project Status

At this stage, the project already includes a working **speech-to-speech pipeline for audio files and browser microphone input**.

Implemented functionality:

* input from `.mp3` file
* microphone recording through the browser frontend
* language identification with a custom classifier
* speech transcription with Whisper
* text translation
* speech synthesis to output `.mp3`
* command-line interface
* FastAPI web interface

This satisfies the core idea of a speech-to-speech system for file-based input.

---

## 12. Limitations

The current version still has several limitations:

* microphone input currently works through the browser frontend rather than a standalone desktop recorder
* system quality depends on the accuracy of the language classifier
* noisy or mislabeled training data can reduce classification performance
* external libraries are used for ASR, translation and TTS
* inference currently runs on CPU, which makes processing slower
* the current frontend is a demo interface and can still be improved
* final quality assessment for English and Portuguese is limited by the evaluator's non-native proficiency

---

## 13. Possible Future Improvements

The next logical improvements are:

### 1. Real-time audio playback

Play generated translated speech directly through speakers.

### 2. Better dataset curation

Clean mislabeled or noisy samples from the training data.

### 3. Improved language classifier

Train the classifier on cleaner and better-balanced data.

### 4. More robust evaluation

Prepare a larger manually verified test set for all supported languages.

### 5. Improved user interface

Extend the frontend with microphone recording, better loading states, clearer confidence visualization and a more polished demo flow.

---

## 14. Summary

This stage of the project successfully transformed the custom language classifier into a complete **speech-to-speech pipeline**.

The final system is able to:

* accept an audio file as input
* detect the spoken language
* transcribe the speech
* translate the content
* generate translated speech as output audio
* expose the workflow through both CLI and web interface

The core original contribution remains the custom CNN-based language identification model, while external tools are used for ASR, translation and TTS. The web frontend was created with support from Codex / AI to make the project easier to present and test.
