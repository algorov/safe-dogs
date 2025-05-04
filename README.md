# 🐶 Dog Muzzle Detector

## 📌 Description

Dog Muzzle Detector is a web service powered by a YOLOv8 neural network that detects whether a dog is wearing a muzzle in a given image. This system is designed to help monitor compliance with leash and muzzle laws in public areas.

Users upload an image, the model analyzes it, and the result is displayed with bounding boxes and labels. The interface clearly shows whether a muzzle was detected or not.


## 🧠 Technologies Used

- YOLOv8 — a state-of-the-art real-time object detection model.
- Python / FastAPI — for the backend server and image processing.
- Bootstrap 5 / HTML / CSS — for a modern dark-themed frontend.
- Docker — for containerized deployment.
- Jinja2 — for HTML template rendering.


## 🚀 How to Run

1. Clone the repository
```bash
git clone https://github.com/algorov/safe-dogs.git
cd safe-dogs
```
2. Build the Docker container
```bash
docker build -t safe-dogs .
```
3. Run the container
```bash
docker run -p 8000:8000 safe-dogs
```

Access the app at: http://localhost:8000


## 📸 How It Works

1. User uploads a photo of a dog.
2. The YOLOv8 model analyzes the image.
3. The result is displayed with bounding boxes and labels:
- ✅ Muzzle detected
- ❌ No muzzle detected


## 🛠 Model Training

The model was trained on a custom dataset of dogs with and without muzzles using the ultralytics library. Training was performed for 50 epochs with the AdamW optimizer and image caching in RAM.
