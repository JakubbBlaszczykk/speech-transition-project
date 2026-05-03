# Speech-to-Speech Translation System

## Description

This project implements a speech-to-speech translation pipeline for both audio files and browser microphone input.

The system can accept either an input `.mp3` file or a browser microphone recording, detect the spoken language, transcribe the speech, translate the text and generate translated speech as an output `.mp3` file.

Supported languages:

- Polish (`pl`)
- English (`en`)
- Portuguese (`pt`)

## Key Features

- Custom CNN-based spoken language identification
- Whisper-based speech recognition
- Text translation between supported languages
- Text-to-speech synthesis to output `.mp3`
- Command-line interface for file-based processing
- FastAPI web demo with browser microphone recording

## Pipeline

```text
Input audio (.mp3 or microphone)
   -> custom language classifier
   -> Whisper ASR
   -> text translation
   -> text-to-speech
   -> output audio (.mp3)
```

The custom part of the project is the CNN-based spoken language classifier. Whisper, translation and TTS are used as external components in the later stages of the pipeline.

## Project Structure

```text
app/                      CLI and FastAPI application entrypoints
frontend/                 browser interface files
src/data/                 data loading and preprocessing
src/model/                CNN model and inference code
src/pipeline/             ASR, translation, TTS and full pipeline modules
scripts/                  development and integration test scripts
docs/                     project documentation
models/                   trained model files
```

## Data Source

The language identification dataset was assembled from Mozilla Data Collective datasets:

- [Common Voice Scripted Speech 25.0 - Polish](https://mozilladatacollective.com/datasets/cmn27nz69015hmm0720txf781)
- [Common Voice Scripted Speech 25.0 - Portuguese](https://mozilladatacollective.com/datasets/cmn29f4cb017bmm07pd9yd8mw)
- [Common Voice Spontaneous Speech 3.0 - English](https://mozilladatacollective.com/datasets/cmn1pv5hi00uto1072y1074y7)

The Common Voice datasets are listed on Mozilla Data Collective as `ASR` datasets in `MP3` format under the `CC0-1.0` license. During testing, some samples were found to be noisy or mislabeled, so manually verified audio files were also used for end-to-end pipeline validation.

## Environment Setup

The recommended setup uses Conda because Whisper requires `ffmpeg`.

Create the environment:

```bash
conda env create -f environment.yml
```

Activate it:

```bash
conda activate speech-env
```

If you prefer using `pip`, install Python dependencies with:

```bash
pip install -r requirements.txt
```

When using `pip`, make sure `ffmpeg` is installed and available in your system `PATH`.

## Quick Start

### CLI

Run the complete speech-to-speech pipeline:

```bash
python app/cli.py path/to/input.mp3 --target-language en --output-path path/to/output.mp3
```

Example:

```bash
python app/cli.py data/test_audio/input/sample_pt.mp3 --target-language en --output-path data/test_audio/output/sample_pt_translated_en.mp3
```

The command prints a JSON summary containing:

- detected source language
- classifier confidence
- class probabilities
- transcript
- translated text
- generated audio path

### Web Demo

The project also includes a small FastAPI web interface for demo purposes.

Start the server:

```bash
python -m uvicorn app.api:app --reload
```

Then open:

```text
http://127.0.0.1:8000
```

The interface allows you to:

- select a microphone input device
- record speech directly in the browser
- select a target language
- run the full speech-to-speech pipeline
- inspect the detected language, transcript and translated text
- play the generated output audio in the browser

The frontend was created with assistance from **Codex / AI** as a development support tool. It is intended as a demo interface around the existing speech-to-speech pipeline.

Recommended demo flow:

1. Open the web interface in the browser
2. Select the microphone input device
3. Record a short utterance
4. Choose the target language
5. Run the translation
6. Play the generated translated audio

## Development Tests

The repository includes helper scripts for testing individual pipeline stages:

```bash
python scripts/test_classifier.py
python scripts/test_asr.py
python scripts/test_translation.py
python scripts/test_tts.py
python scripts/test_language_to_text.py
python scripts/test_speech_to_speech.py
```

These scripts were used during development to verify every module separately before running the full pipeline.

## Current Limitations

- The command-line version is still file-based, while microphone input is currently available in the web interface.
- The quality of the full pipeline depends strongly on the language classifier.
- Some dataset samples were found to be noisy or mislabeled.
- ASR, translation and TTS are handled by external libraries.
- CPU inference can be slow, especially for Whisper.
- Practical evaluation of English and Portuguese output is less reliable than Polish because the final tester is not a native speaker of those languages.

## Current Status

The current version already supports:

- file-based speech-to-speech processing
- browser microphone recording
- language detection for `pl`, `en`, `pt`
- transcript generation
- translation
- speech synthesis
- browser playback of the generated output

## Documentation

More details are available in:

- `docs/01_ML_pipeline.md`
- `docs/02_speech_to_speech_pipeline.md`
