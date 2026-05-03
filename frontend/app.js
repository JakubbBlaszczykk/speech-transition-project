const form = document.querySelector("#translate-form");
const microphoneSelect = document.querySelector("#microphone-select");
const startRecordingButton = document.querySelector("#start-recording");
const stopRecordingButton = document.querySelector("#stop-recording");
const submitButton = document.querySelector("#submit-button");
const statusText = document.querySelector("#status");
const results = document.querySelector("#results");
const recordingState = document.querySelector("#recording-state");
const recordingDuration = document.querySelector("#recording-duration");
const recordingPreviewPanel = document.querySelector("#recording-preview-panel");
const recordedAudio = document.querySelector("#recorded-audio");

const sourceLanguage = document.querySelector("#source-language");
const confidence = document.querySelector("#confidence");
const transcript = document.querySelector("#transcript");
const translatedText = document.querySelector("#translated-text");
const outputAudio = document.querySelector("#output-audio");

let mediaRecorder = null;
let mediaStream = null;
let recordedBlob = null;
let recordedUrl = null;
let recordingChunks = [];
let recordingStartedAt = null;
let recordingTimerId = null;

function setStatus(message) {
  statusText.textContent = message;
}

function formatDuration(totalSeconds) {
  const minutes = String(Math.floor(totalSeconds / 60)).padStart(2, "0");
  const seconds = String(totalSeconds % 60).padStart(2, "0");
  return `${minutes}:${seconds}`;
}

function resetRecordingPreview() {
  recordedBlob = null;
  if (recordedUrl) {
    URL.revokeObjectURL(recordedUrl);
    recordedUrl = null;
  }
  recordedAudio.removeAttribute("src");
  recordingPreviewPanel.classList.add("hidden");
  submitButton.disabled = true;
}

async function loadAudioInputs() {
  const devices = await navigator.mediaDevices.enumerateDevices();
  const audioInputs = devices.filter((device) => device.kind === "audioinput");

  microphoneSelect.innerHTML = '<option value="">Default microphone</option>';

  audioInputs.forEach((device, index) => {
    const option = document.createElement("option");
    option.value = device.deviceId;
    option.textContent = device.label || `Microphone ${index + 1}`;
    microphoneSelect.append(option);
  });
}

async function requestAudioPermission() {
  const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
  stream.getTracks().forEach((track) => track.stop());
  await loadAudioInputs();
}

function stopTimer() {
  if (recordingTimerId) {
    clearInterval(recordingTimerId);
    recordingTimerId = null;
  }
}

function startTimer() {
  recordingStartedAt = Date.now();
  recordingDuration.textContent = "00:00";
  stopTimer();
  recordingTimerId = window.setInterval(() => {
    const elapsedSeconds = Math.floor((Date.now() - recordingStartedAt) / 1000);
    recordingDuration.textContent = formatDuration(elapsedSeconds);
  }, 200);
}

async function startRecording() {
  resetRecordingPreview();
  results.classList.add("hidden");

  const selectedDeviceId = microphoneSelect.value;
  const constraints = selectedDeviceId
    ? { audio: { deviceId: { exact: selectedDeviceId } } }
    : { audio: true };

  mediaStream = await navigator.mediaDevices.getUserMedia(constraints);

  const preferredMimeTypes = [
    "audio/webm;codecs=opus",
    "audio/webm",
    "audio/ogg;codecs=opus",
  ];
  const mimeType = preferredMimeTypes.find((candidate) => MediaRecorder.isTypeSupported(candidate));

  mediaRecorder = mimeType
    ? new MediaRecorder(mediaStream, { mimeType })
    : new MediaRecorder(mediaStream);

  recordingChunks = [];

  mediaRecorder.addEventListener("dataavailable", (event) => {
    if (event.data.size > 0) {
      recordingChunks.push(event.data);
    }
  });

  mediaRecorder.addEventListener("stop", () => {
    const blobType = mediaRecorder.mimeType || "audio/webm";
    recordedBlob = new Blob(recordingChunks, { type: blobType });
    recordedUrl = URL.createObjectURL(recordedBlob);
    recordedAudio.src = recordedUrl;
    recordingPreviewPanel.classList.remove("hidden");
    submitButton.disabled = false;
    recordingState.textContent = "Recorded";
  });

  mediaRecorder.start();
  startTimer();
  recordingState.textContent = "Recording";
  setStatus("Recording from microphone...");
  startRecordingButton.disabled = true;
  stopRecordingButton.disabled = false;
}

function stopRecording() {
  if (!mediaRecorder) {
    return;
  }

  mediaRecorder.stop();
  mediaStream?.getTracks().forEach((track) => track.stop());
  mediaStream = null;
  stopTimer();
  setStatus("Recording captured. You can now translate it.");
  startRecordingButton.disabled = false;
  stopRecordingButton.disabled = true;
}

startRecordingButton.addEventListener("click", async () => {
  try {
    await startRecording();
  } catch (error) {
    setStatus(`Could not start recording: ${error.message}`);
    recordingState.textContent = "Unavailable";
  }
});

stopRecordingButton.addEventListener("click", () => {
  stopRecording();
});

form.addEventListener("submit", async (event) => {
  event.preventDefault();

  if (!recordedBlob) {
    setStatus("Record audio before running translation.");
    return;
  }

  const formData = new FormData();
  formData.append("target_language", document.querySelector("#target-language").value);

  const extension = recordedBlob.type.includes("ogg") ? "ogg" : "webm";
  const recordingFile = new File([recordedBlob], `microphone_recording.${extension}`, {
    type: recordedBlob.type,
  });
  formData.append("audio_file", recordingFile);

  submitButton.disabled = true;
  setStatus("Processing recording. This may take a moment on CPU...");
  results.classList.add("hidden");

  try {
    const response = await fetch("/translate", {
      method: "POST",
      body: formData,
    });

    const payload = await response.json();

    if (!response.ok) {
      throw new Error(payload.detail || "Translation failed.");
    }

    sourceLanguage.textContent = payload.source_language;
    confidence.textContent = `Confidence: ${(payload.confidence * 100).toFixed(1)}%`;
    transcript.textContent = payload.transcript || "(empty transcript)";
    translatedText.textContent = payload.translated_text || "(empty translation)";
    outputAudio.src = payload.output_audio_url;

    setStatus("Done. You can unplug headphones and play the translated output through speakers.");
    results.classList.remove("hidden");
  } catch (error) {
    setStatus(error.message);
  } finally {
    submitButton.disabled = false;
  }
});

window.addEventListener("beforeunload", () => {
  stopTimer();
  mediaStream?.getTracks().forEach((track) => track.stop());
  if (recordedUrl) {
    URL.revokeObjectURL(recordedUrl);
  }
});

requestAudioPermission().catch(() => {
  setStatus("Allow microphone access in the browser to start recording.");
  recordingState.textContent = "Permission needed";
});
