const fileDropArea = document.querySelector(`[data-item="file-drop-area"]`);
const uploadedImage = document.querySelector(`[data-item="uploaded-image"]`);
const uploadInput = document.querySelector(`[data-item="upload-input"]`);
const changeImageBtn = document.querySelector(`[data-item="change-image"]`);
const classifyBtn = document.querySelector(`[data-item="classify-btn"]`);
const predictionContainer = document.querySelector(
  `[data-item="prediction-container"]`
);
const predictedOutput = document.querySelector(
  `[data-item="predicted-output"]`
);

const highlight = (event) => {
  event.preventDefault();
  event.stopPropagation();
  fileDropArea.classList.add("file-enter");
};

const unhighlight = (event) => {
  event.preventDefault();
  event.stopPropagation();
  fileDropArea.classList.remove("file-enter");
};

fileDropArea.addEventListener("dragenter", highlight, false);
fileDropArea.addEventListener("dragover", highlight, false);

fileDropArea.addEventListener("dragleave", unhighlight, false);
fileDropArea.addEventListener("drop", unhighlight, false);
fileDropArea.addEventListener(
  "drop",
  async (event) => {
    const dataTransfer = event.dataTransfer;
    uploadInput.files = dataTransfer.files;
  },
  false
);

uploadInput.addEventListener("change", (event) => {
  const file = uploadInput.files[0];
  if (file) {
    const url = URL.createObjectURL(file);
    uploadedImage.src = url;

    uploadedImage.classList.remove("hidden");
    fileDropArea.classList.add("hidden");
    changeImageBtn.classList.remove("hidden");
    classifyBtn.classList.remove("hidden");
  }
});

changeImageBtn.addEventListener("click", (event) => {
  uploadInput.value = null;
  uploadInput.click();
});

classifyBtn.addEventListener("click", (event) => {
  const file = uploadInput.files[0];
  predict(file);
});

async function predict(file) {
  if (!file) return;

  const data = new FormData();
  data.append("file", file);

  try {
    const response = await fetch("/api/predict", {
      method: "POST",
      body: data,
    });
    const responseData = await response.json();
    const output = responseData.label;
    predictedOutput.innerText = output;
    predictionContainer.classList.remove("hidden");
  } catch (err) {
    console.error(err);
  }
}
