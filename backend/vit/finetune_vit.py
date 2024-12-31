import numpy as np
from PIL import Image, ImageFile

import torch
from transformers import (
    ViTForImageClassification,
    TrainingArguments,
    Trainer,
    AutoImageProcessor,
)
from peft import LoraConfig, get_peft_model
import evaluate
from torchvision.transforms import (
    CenterCrop,
    Compose,
    Normalize,
    RandomHorizontalFlip,
    RandomResizedCrop,
    Resize,
    ToTensor,
)
from datasets import load_dataset

import warnings

warnings.filterwarnings("ignore")

ImageFile.LOAD_TRUNCATED_IMAGES = True


metric = evaluate.load("accuracy")


def compute_metrics(eval_pred):
    predictions = np.argmax(eval_pred.predictions, axis=1)
    return metric.compute(predictions=predictions, references=eval_pred.label_ids)


def collate_fn(examples):
    pixel_values = torch.stack([example["pixel_values"] for example in examples])
    labels = torch.tensor([example["label"] for example in examples])
    return {"pixel_values": pixel_values, "labels": labels}


device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

image_processor = AutoImageProcessor.from_pretrained(
    "google/vit-base-patch16-224-in21k"
)
normalize = Normalize(mean=image_processor.image_mean, std=image_processor.image_std)

train_transforms = Compose(
    [
        RandomResizedCrop(image_processor.size["height"]),
        RandomHorizontalFlip(),
        ToTensor(),
        normalize,
    ]
)

val_transforms = Compose(
    [
        Resize(image_processor.size["height"]),
        CenterCrop(image_processor.size["height"]),
        ToTensor(),
        normalize,
    ]
)


def preprocess_train(example_batch):
    """Apply train_transforms across a batch."""
    example_batch["pixel_values"] = [
        train_transforms(Image.open(image).convert("RGB"))
        for image in example_batch["image"]
    ]
    return example_batch


def preprocess_val(example_batch):
    """Apply val_transforms across a batch."""
    example_batch["pixel_values"] = [
        val_transforms(Image.open(image).convert("RGB"))
        for image in example_batch["image"]
    ]
    return example_batch


# dataset = load_dataset("imagefolder", data_dir="./data", split="train", drop_labels=True)
train_ds = load_dataset("csv", data_files="./data/train.csv", split="train")
val_ds = load_dataset("csv", data_files="./data/val.csv", split="train")
test_ds = load_dataset("csv", data_files="./data/test.csv", split="train")

train_ds.set_transform(preprocess_train)
val_ds.set_transform(preprocess_val)
test_ds.set_transform(preprocess_val)

model = ViTForImageClassification.from_pretrained(
    "google/vit-base-patch16-224-in21k", num_labels=15
)

peft_config = LoraConfig(
    r=16,
    lora_alpha=16,
    target_modules=["query", "value", "key", "dense"],
    lora_dropout=0.1,
    bias="none",
    modules_to_save=["classifier"],
)

peft_model = get_peft_model(model, peft_config)
peft_model.print_trainable_parameters()

training_args = TrainingArguments(
    output_dir="./results",
    num_train_epochs=20,
    learning_rate=1e-3,
    logging_steps=10,
    per_device_train_batch_size=64,
    per_device_eval_batch_size=64,
    remove_unused_columns=False,
    evaluation_strategy="epoch",
    save_strategy="epoch",
    load_best_model_at_end=True,
    metric_for_best_model="accuracy",
    seed=42,
    fp16=True,
    dataloader_num_workers=4,
    label_names=["labels"],
)

trainer = Trainer(
    model=peft_model,
    args=training_args,
    train_dataset=train_ds,
    eval_dataset=val_ds,
    compute_metrics=compute_metrics,
    data_collator=collate_fn,
)

trainer.train()

peft_model_id = "google/vit-base-patch16-224-in21k-lora-indian_food"
trainer.model.save_pretrained(peft_model_id)

print(trainer.evaluate(test_ds))
