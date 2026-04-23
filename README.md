# Speech-to-Speech Translation System

## Description

This project implements a file-based speech-to-speech translation pipeline.

The system accepts an input `.mp3` file, detects the spoken language, transcribes the speech, translates the text and generates translated speech as an output `.mp3` file.

Supported languages:

- Polish (`pl`)
- English (`en`)
- Portuguese (`pt`)

## Pipeline

```text
Input audio (.mp3)
   -> custom language classifier
   -> Whisper ASR
   -> text translation
   -> text-to-speech
   -> output audio (.mp3)
```

The custom part of the project is the CNN-based spoken language classifier. Whisper, translation and TTS are used as external components in the later stages of the pipeline.

## Project Structure

```text
src/data/                 data loading and preprocessing
src/model/                CNN model and inference code
src/pipeline/             ASR, translation, TTS and full pipeline modules
scripts/                  development and integration test scripts
docs/                     project documentation
models/                   trained model files
```

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

## Usage

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

## Web Interface

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

- upload an audio file
- select a target language
- run the full speech-to-speech pipeline
- inspect the detected language, transcript and translated text
- play the generated output audio in the browser

The frontend was created with assistance from **Codex / AI** as a development support tool. It is intended as a demo interface around the existing speech-to-speech pipeline.

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

- The current version supports file input only, not microphone input.
- The quality of the full pipeline depends strongly on the language classifier.
- Some dataset samples were found to be noisy or mislabeled.
- ASR, translation and TTS are handled by external libraries.
- CPU inference can be slow, especially for Whisper.

## Documentation

More details are available in:

- `docs/01_ML_pipeline.md`
- `docs/02_speech_to_speech_pipeline.md`
