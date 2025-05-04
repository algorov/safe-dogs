from fastapi import FastAPI, File, UploadFile, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import os
import uuid
import cv2
import numpy as np
from ultralytics import YOLO

# ───── Настройки ─────
app = FastAPI()

STATIC_DIR = "app/static"
RESULTS_DIR = os.path.join(STATIC_DIR, "results")
TEMPLATES_DIR = "app/templates"
MODEL_PATH = "app/models/best.pt"

os.makedirs(RESULTS_DIR, exist_ok=True)

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
templates = Jinja2Templates(directory=TEMPLATES_DIR)

model = YOLO(MODEL_PATH)

# ───── Вспомогательные функции ─────

def decode_image(contents: bytes) -> np.ndarray:
    """Декодирует изображение из байтов"""
    image_np = np.frombuffer(contents, np.uint8)
    return cv2.imdecode(image_np, cv2.IMREAD_COLOR)

def run_detection(image: np.ndarray, model: YOLO) -> tuple[np.ndarray, bool]:
    """Запускает модель и отрисовывает результаты"""
    temp_path = f"temp_{uuid.uuid4()}.jpg"
    cv2.imwrite(temp_path, image)

    results = model(temp_path)[0]
    os.remove(temp_path)

    muzzle_detected = False

    for box in results.boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        cls_id = int(box.cls[0])
        label = model.names[cls_id]
        conf = float(box.conf[0])

        if "muzzle" in label.lower():
            muzzle_detected = True

        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(image, f"{label} ({conf:.2f})", (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (36, 255, 12), 2)

    return image, muzzle_detected

def save_result_image(image: np.ndarray) -> str:
    """Сохраняет результат в папку и возвращает URL путь"""
    filename = f"result_{uuid.uuid4()}.jpg"
    result_path = os.path.join(RESULTS_DIR, filename)
    cv2.imwrite(result_path, image)
    return f"/static/results/{filename}"

# ───── Роуты ─────

@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/detect", response_class=HTMLResponse)
async def detect(request: Request, file: UploadFile = File(...)):
    contents = await file.read()
    image = decode_image(contents)
    processed_image, muzzle_detected = run_detection(image, model)
    result_path = save_result_image(processed_image)

    message = "Muzzle detected" if muzzle_detected else "No muzzle detected"

    return templates.TemplateResponse("index.html", {
        "request": request,
        "result_path": result_path,
        "message": message
    })
