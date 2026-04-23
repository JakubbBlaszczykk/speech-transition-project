import shutil
import sys
from pathlib import Path
from uuid import uuid4

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))

from src.pipeline.speech_to_speech import SpeechToSpeechPipeline

RUNTIME_DIR = PROJECT_ROOT / "runtime"
UPLOAD_DIR = RUNTIME_DIR / "uploads"
OUTPUT_DIR = RUNTIME_DIR / "outputs"
FRONTEND_DIR = PROJECT_ROOT / "frontend"
MODEL_PATH = PROJECT_ROOT / "models" / "cnn_model.pth"
_pipeline = None

for directory in (UPLOAD_DIR, OUTPUT_DIR):
    directory.mkdir(parents=True, exist_ok=True)

app = FastAPI(title="Speech-to-Speech Translation System")

app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR)), name="static")


def get_pipeline():
    global _pipeline
    if _pipeline is None:
        _pipeline = SpeechToSpeechPipeline(
            model_path=str(MODEL_PATH),
            whisper_model="base",
        )
    return _pipeline


@app.get("/")
def index():
    return FileResponse(FRONTEND_DIR / "index.html")


@app.post("/translate")
def translate_audio(
    target_language: str = Form("en"),
    audio_file: UploadFile = File(...),
):
    if target_language not in {"pl", "en", "pt"}:
        raise HTTPException(status_code=400, detail="Unsupported target language.")

    if not audio_file.filename:
        raise HTTPException(status_code=400, detail="Audio file is required.")

    suffix = Path(audio_file.filename).suffix.lower()
    if suffix not in {".mp3", ".wav", ".m4a"}:
        raise HTTPException(
            status_code=400,
            detail="Unsupported file type. Use .mp3, .wav or .m4a.",
        )

    job_id = uuid4().hex
    input_path = UPLOAD_DIR / f"{job_id}{suffix}"
    output_path = OUTPUT_DIR / f"{job_id}_{target_language}.mp3"

    with input_path.open("wb") as buffer:
        shutil.copyfileobj(audio_file.file, buffer)

    try:
        pipeline = get_pipeline()
        result = pipeline.run(
            audio_path=str(input_path),
            target_language=target_language,
            output_path=str(output_path),
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    return {
        **result,
        "output_audio_url": f"/audio/{output_path.name}",
    }


@app.get("/audio/{filename}")
def get_audio(filename: str):
    if Path(filename).name != filename:
        raise HTTPException(status_code=400, detail="Invalid audio filename.")

    audio_path = OUTPUT_DIR / filename
    if not audio_path.exists():
        raise HTTPException(status_code=404, detail="Audio file not found.")

    return FileResponse(audio_path, media_type="audio/mpeg", filename=filename)
