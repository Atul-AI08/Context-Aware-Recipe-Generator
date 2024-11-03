from fastapi import FastAPI, HTTPException, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image, ImageFile
from transformers import AutoImageProcessor, AutoModelForImageClassification

ImageFile.LOAD_TRUNCATED_IMAGES = True

app = FastAPI(
    title="Dish Classifier",
    version="1.0",
    description="A dish classifier using Vision Transformer",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

image_processor = AutoImageProcessor.from_pretrained(
    "google/vit-base-patch16-224-in21k"
)
id2label = {
    0: "Dabeli",
    1: "Jalebi",
    2: "Vadapav",
    3: "Pani-Puri",
    4: "Pakora",
    5: "Paneer-Tikka",
    6: "Dal",
    7: "Pav-Bhaji",
    8: "Kathi Roll",
    9: "Kofta",
    10: "Naan",
    11: "Dosa",
    12: "Dhokla",
    13: "Chole-Bhature",
    14: "Biryani",
}

model_checkpoint = "google/vit-base-patch16-224-in21k-lora-indian_food"

model = AutoModelForImageClassification.from_pretrained(model_checkpoint, num_labels=15)


def predict(image):
    inputs = image_processor(images=image, return_tensors="pt")
    outputs = model(**inputs)

    logits = outputs.logits
    predicted_class = logits.argmax(-1).item()
    return predicted_class


@app.post("/predict")
async def predict_dish(file: UploadFile = File(...)):
    try:
        image = Image.open(file.file).convert("RGB")
        return {"dish": id2label[predict(image)]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8000)
