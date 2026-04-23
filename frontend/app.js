const form = document.querySelector("#translate-form");
const submitButton = document.querySelector("#submit-button");
const statusText = document.querySelector("#status");
const results = document.querySelector("#results");

const sourceLanguage = document.querySelector("#source-language");
const confidence = document.querySelector("#confidence");
const transcript = document.querySelector("#transcript");
const translatedText = document.querySelector("#translated-text");
const outputAudio = document.querySelector("#output-audio");

form.addEventListener("submit", async (event) => {
  event.preventDefault();

  const formData = new FormData(form);

  submitButton.disabled = true;
  statusText.textContent = "Processing audio. This may take a moment on CPU...";
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

    statusText.textContent = "Done.";
    results.classList.remove("hidden");
  } catch (error) {
    statusText.textContent = error.message;
  } finally {
    submitButton.disabled = false;
  }
});
