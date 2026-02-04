---
name: computer-vision
description: Build computer vision solutions - image classification, object detection, and transfer learning
version: "1.4.0"
sasmp_version: "1.4.0"
bonded_agent: 06-computer-vision
bond_type: PRIMARY_BOND

# Parameter Validation
parameters:
  required:
    - name: images
      type: tensor|array
      validation: "4D tensor [B, C, H, W] or list of images"
  optional:
    - name: model_name
      type: string
      default: "efficientnet_b0"
    - name: num_classes
      type: integer
      default: 1000

# Retry Logic
retry_logic:
  strategy: exponential_backoff
  max_attempts: 3
  base_delay_ms: 1000

# Observability
logging:
  level: info
  metrics: [inference_time, batch_size, image_size]
---

# Computer Vision Skill

> Build visual AI systems from classification to detection.

## Quick Start

```python
import torch
import timm
from PIL import Image
from torchvision import transforms

# Load pretrained model
model = timm.create_model('efficientnet_b0', pretrained=True, num_classes=10)
model.eval()

# Preprocessing
transform = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

# Inference
image = Image.open('image.jpg').convert('RGB')
input_tensor = transform(image).unsqueeze(0)

with torch.no_grad():
    output = model(input_tensor)
    predicted_class = output.argmax(dim=1).item()
```

## Key Topics

### 1. Data Augmentation

```python
import albumentations as A
from albumentations.pytorch import ToTensorV2

train_transform = A.Compose([
    A.RandomResizedCrop(224, 224, scale=(0.8, 1.0)),
    A.HorizontalFlip(p=0.5),
    A.ShiftScaleRotate(shift_limit=0.1, scale_limit=0.1, rotate_limit=15),
    A.ColorJitter(brightness=0.2, contrast=0.2),
    A.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ToTensorV2()
])

val_transform = A.Compose([
    A.Resize(256, 256),
    A.CenterCrop(224, 224),
    A.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ToTensorV2()
])
```

### 2. Transfer Learning

| Model | Params | ImageNet Acc | Speed |
|-------|--------|--------------|-------|
| **EfficientNet-B0** | 5.3M | 77% | Fast |
| **ResNet-50** | 25.6M | 76% | Fast |
| **ViT-B/16** | 86M | 84% | Slow |

```python
import timm

class TransferClassifier(torch.nn.Module):
    def __init__(self, backbone='efficientnet_b0', num_classes=10):
        super().__init__()
        self.backbone = timm.create_model(backbone, pretrained=True, num_classes=0)
        self.classifier = torch.nn.Linear(self.backbone.num_features, num_classes)

        # Freeze backbone
        for param in self.backbone.parameters():
            param.requires_grad = False

    def unfreeze(self):
        for param in self.backbone.parameters():
            param.requires_grad = True

    def forward(self, x):
        features = self.backbone(x)
        return self.classifier(features)
```

### 3. Object Detection (YOLOv8)

```python
from ultralytics import YOLO

# Load model
model = YOLO('yolov8n.pt')

# Train
results = model.train(
    data='dataset.yaml',
    epochs=100,
    imgsz=640,
    batch=16
)

# Inference
results = model('image.jpg')
for r in results:
    boxes = r.boxes
    for box in boxes:
        print(f"Class: {r.names[int(box.cls)]}, Conf: {box.conf:.2f}")
```

### 4. Image Segmentation

```python
import segmentation_models_pytorch as smp

# Create U-Net model
model = smp.Unet(
    encoder_name='resnet50',
    encoder_weights='imagenet',
    in_channels=3,
    classes=21
)

# Loss function
loss_fn = smp.losses.DiceLoss(mode='multiclass')
```

### 5. Model Evaluation

```python
from sklearn.metrics import classification_report, confusion_matrix

def evaluate_classifier(model, dataloader, device):
    model.eval()
    all_preds, all_labels = [], []

    with torch.no_grad():
        for images, labels in dataloader:
            outputs = model(images.to(device))
            preds = outputs.argmax(dim=1)
            all_preds.extend(preds.cpu().numpy())
            all_labels.extend(labels.numpy())

    return {
        'report': classification_report(all_labels, all_preds),
        'confusion_matrix': confusion_matrix(all_labels, all_preds)
    }
```

## Best Practices

### DO
- Use pretrained models
- Apply consistent augmentation
- Use mixed precision training
- Normalize with ImageNet stats
- Visualize predictions

### DON'T
- Don't train from scratch on small data
- Don't use same augmentations for val
- Don't ignore class imbalance
- Don't skip visual error analysis

## Exercises

### Exercise 1: Transfer Learning
```python
# TODO: Fine-tune EfficientNet on CIFAR-10
# Freeze backbone first, then unfreeze
```

### Exercise 2: Object Detection
```python
# TODO: Train YOLOv8 on custom dataset
# Create dataset.yaml and train
```

## Unit Test Template

```python
import pytest
import torch

def test_model_output_shape():
    """Test model output dimensions."""
    model = TransferClassifier(num_classes=10)
    x = torch.randn(4, 3, 224, 224)

    output = model(x)

    assert output.shape == (4, 10)

def test_augmentation_preserves_shape():
    """Test augmentation output shape."""
    import numpy as np
    image = np.random.randint(0, 255, (256, 256, 3), dtype=np.uint8)

    augmented = train_transform(image=image)['image']

    assert augmented.shape == (3, 224, 224)
```

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| Overfitting | Small dataset | More augmentation |
| Slow training | Large images | Resize, use AMP |
| Poor detection | Wrong anchors | Adjust anchor sizes |
| Memory error | Batch too large | Reduce batch size |

## Related Resources

- **Agent**: `06-computer-vision`
- **Previous**: `nlp-basics`
- **Next**: `ml-deployment`
- **Docs**: [timm](https://huggingface.co/docs/timm)

---

**Version**: 1.4.0 | **Status**: Production Ready
