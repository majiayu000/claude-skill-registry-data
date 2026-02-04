---
name: ml-reviewer
description: |
  WHEN: Machine Learning/Deep Learning code review, PyTorch/TensorFlow patterns, Model training optimization, MLOps checks
  WHAT: Model architecture review + Training patterns + Data pipeline checks + GPU optimization + Experiment tracking
  WHEN NOT: Data analysis only → python-data-reviewer, General Python → python-reviewer
---

# ML Reviewer Skill

## Purpose
Reviews Machine Learning and Deep Learning code for PyTorch, TensorFlow, scikit-learn, and MLOps best practices.

## When to Use
- ML/DL project code review
- "PyTorch", "TensorFlow", "Keras", "scikit-learn", "model training" mentions
- Model performance, training optimization inspection
- Projects with ML framework dependencies

## Project Detection
- `torch`, `tensorflow`, `keras`, `sklearn` in requirements.txt/pyproject.toml
- `.pt`, `.pth`, `.h5`, `.pkl` model files
- `train.py`, `model.py`, `dataset.py` files
- Jupyter notebooks with ML imports

## Workflow

### Step 1: Analyze Project
```
**Framework**: PyTorch / TensorFlow / scikit-learn
**Python**: 3.10+
**CUDA**: 11.x / 12.x
**Task**: Classification / Regression / NLP / CV
**Stage**: Research / Production
```

### Step 2: Select Review Areas
**AskUserQuestion:**
```
"Which areas to review?"
Options:
- Full ML pattern check (recommended)
- Model architecture review
- Training loop optimization
- Data pipeline efficiency
- MLOps/deployment patterns
multiSelect: true
```

## Detection Rules

### PyTorch Patterns
| Check | Recommendation | Severity |
|-------|----------------|----------|
| Missing model.eval() | Inconsistent inference | HIGH |
| Missing torch.no_grad() | Memory leak in inference | HIGH |
| In-place operations in autograd | Gradient computation error | CRITICAL |
| DataLoader num_workers=0 | CPU bottleneck | MEDIUM |
| Missing gradient clipping | Exploding gradients | MEDIUM |

```python
# BAD: Missing eval() and no_grad()
def predict(model, x):
    return model(x)  # Dropout/BatchNorm inconsistent!

# GOOD: Proper inference mode
def predict(model, x):
    model.eval()
    with torch.no_grad():
        return model(x)

# BAD: In-place operation breaking autograd
x = torch.randn(10, requires_grad=True)
x += 1  # In-place! Breaks gradient computation

# GOOD: Out-of-place operation
x = torch.randn(10, requires_grad=True)
x = x + 1

# BAD: DataLoader bottleneck
loader = DataLoader(dataset, batch_size=32)  # num_workers=0

# GOOD: Parallel data loading
loader = DataLoader(
    dataset,
    batch_size=32,
    num_workers=4,
    pin_memory=True,  # For GPU
    persistent_workers=True,
)

# BAD: No gradient clipping
optimizer.step()

# GOOD: Clip gradients
torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
optimizer.step()
```

### TensorFlow/Keras Patterns
| Check | Recommendation | Severity |
|-------|----------------|----------|
| Missing @tf.function | Performance loss | MEDIUM |
| Eager mode in production | Slow inference | HIGH |
| Large model in memory | OOM risk | HIGH |
| Missing mixed precision | Training inefficiency | MEDIUM |

```python
# BAD: No @tf.function
def train_step(x, y):
    with tf.GradientTape() as tape:
        pred = model(x)
        loss = loss_fn(y, pred)
    gradients = tape.gradient(loss, model.trainable_variables)
    optimizer.apply_gradients(zip(gradients, model.trainable_variables))

# GOOD: Use @tf.function
@tf.function
def train_step(x, y):
    with tf.GradientTape() as tape:
        pred = model(x, training=True)
        loss = loss_fn(y, pred)
    gradients = tape.gradient(loss, model.trainable_variables)
    optimizer.apply_gradients(zip(gradients, model.trainable_variables))

# BAD: Missing mixed precision
model.fit(x_train, y_train, epochs=10)

# GOOD: Enable mixed precision
tf.keras.mixed_precision.set_global_policy('mixed_float16')
model.fit(x_train, y_train, epochs=10)
```

### scikit-learn Patterns
| Check | Recommendation | Severity |
|-------|----------------|----------|
| fit_transform on test data | Data leakage | CRITICAL |
| Missing cross-validation | Overfitting risk | HIGH |
| No feature scaling | Model performance | MEDIUM |
| Hardcoded random_state | Reproducibility | LOW |

```python
# BAD: Data leakage
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.fit_transform(X_test)  # LEAK! Re-fitting

# GOOD: transform only on test
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)  # No re-fit

# BAD: No cross-validation
model.fit(X_train, y_train)
score = model.score(X_test, y_test)

# GOOD: Use cross-validation
from sklearn.model_selection import cross_val_score
scores = cross_val_score(model, X, y, cv=5)
print(f"CV Score: {scores.mean():.3f} (+/- {scores.std():.3f})")

# BAD: Pipeline without scaling
model = LogisticRegression()
model.fit(X_train, y_train)

# GOOD: Use Pipeline with scaling
from sklearn.pipeline import Pipeline
pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('classifier', LogisticRegression())
])
pipeline.fit(X_train, y_train)
```

### Data Pipeline
| Check | Problem | Solution |
|-------|---------|----------|
| Loading full dataset to memory | OOM | Use generators/tf.data |
| No data augmentation | Overfitting | Add augmentation |
| Unbalanced classes | Biased model | Oversample/undersample/weights |
| No validation split | No early stopping | Use validation set |

```python
# BAD: Full dataset in memory
images = []
for path in all_image_paths:
    images.append(load_image(path))  # OOM for large datasets!

# GOOD: Use generator
def data_generator(paths, batch_size):
    for i in range(0, len(paths), batch_size):
        batch_paths = paths[i:i+batch_size]
        yield np.array([load_image(p) for p in batch_paths])

# GOOD: Use tf.data
dataset = tf.data.Dataset.from_tensor_slices(paths)
dataset = dataset.map(load_and_preprocess)
dataset = dataset.batch(32).prefetch(tf.data.AUTOTUNE)

# BAD: No class weights for imbalanced data
model.fit(X_train, y_train)

# GOOD: Add class weights
from sklearn.utils.class_weight import compute_class_weight
weights = compute_class_weight('balanced', classes=np.unique(y), y=y)
class_weights = dict(enumerate(weights))
model.fit(X_train, y_train, class_weight=class_weights)
```

### GPU/Performance
| Check | Recommendation | Severity |
|-------|----------------|----------|
| CPU tensor operations | Use GPU tensors | HIGH |
| Frequent GPU-CPU transfer | Batch transfers | HIGH |
| No gradient accumulation | OOM for large batch | MEDIUM |
| Missing torch.cuda.empty_cache() | Memory fragmentation | LOW |

```python
# BAD: CPU operations
x = torch.randn(1000, 1000)
y = torch.randn(1000, 1000)
z = x @ y  # CPU computation

# GOOD: GPU operations
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
x = torch.randn(1000, 1000, device=device)
y = torch.randn(1000, 1000, device=device)
z = x @ y  # GPU computation

# BAD: Frequent CPU-GPU transfer
for x, y in dataloader:
    x = x.cuda()
    y = y.cuda()
    loss = model(x, y)
    print(loss.item())  # Sync every iteration!

# GOOD: Batch logging
losses = []
for x, y in dataloader:
    x, y = x.to(device), y.to(device)
    loss = model(x, y)
    losses.append(loss)
if step % log_interval == 0:
    print(torch.stack(losses).mean().item())

# Gradient accumulation for large effective batch
accumulation_steps = 4
for i, (x, y) in enumerate(dataloader):
    loss = model(x, y) / accumulation_steps
    loss.backward()
    if (i + 1) % accumulation_steps == 0:
        optimizer.step()
        optimizer.zero_grad()
```

### MLOps/Experiment Tracking
| Check | Recommendation | Severity |
|-------|----------------|----------|
| No experiment tracking | Reproducibility | HIGH |
| Hardcoded hyperparameters | Config management | MEDIUM |
| No model versioning | Deployment issues | MEDIUM |
| Missing seed setting | Non-reproducible | HIGH |

```python
# BAD: No seed setting
model = train_model(X, y)

# GOOD: Set all seeds
import random
import numpy as np
import torch

def set_seed(seed=42):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.deterministic = True

set_seed(42)

# BAD: Hardcoded hyperparameters
lr = 0.001
batch_size = 32
epochs = 100

# GOOD: Use config file or hydra
import hydra
from omegaconf import DictConfig

@hydra.main(config_path="configs", config_name="train")
def train(cfg: DictConfig):
    model = build_model(cfg.model)
    optimizer = torch.optim.Adam(model.parameters(), lr=cfg.lr)

# GOOD: Use experiment tracking
import wandb
wandb.init(project="my-project", config=cfg)
for epoch in range(epochs):
    loss = train_epoch(model, dataloader)
    wandb.log({"loss": loss, "epoch": epoch})
wandb.finish()
```

## Response Template
```
## ML Code Review Results

**Project**: [name]
**Framework**: PyTorch/TensorFlow/scikit-learn
**Task**: Classification/Regression/NLP/CV
**Files Analyzed**: X

### Model Architecture
| Status | File | Issue |
|--------|------|-------|
| MEDIUM | models/resnet.py | Missing dropout for regularization |
| LOW | models/transformer.py | Consider gradient checkpointing |

### Training Loop
| Status | File | Issue |
|--------|------|-------|
| HIGH | train.py | Missing model.eval() in validation (line 45) |
| HIGH | train.py | No gradient clipping (line 67) |

### Data Pipeline
| Status | File | Issue |
|--------|------|-------|
| CRITICAL | data/dataset.py | fit_transform on test data (line 23) |
| HIGH | data/loader.py | DataLoader num_workers=0 |

### MLOps
| Status | File | Issue |
|--------|------|-------|
| HIGH | train.py | No seed setting for reproducibility |
| MEDIUM | train.py | Hardcoded hyperparameters |

### Recommended Actions
1. [ ] Add model.eval() and torch.no_grad() for inference
2. [ ] Fix data leakage in preprocessing
3. [ ] Set random seeds for reproducibility
4. [ ] Add experiment tracking (wandb/mlflow)
```

## Best Practices
1. **Training**: eval mode, no_grad, gradient clipping, mixed precision
2. **Data**: No leakage, proper splits, augmentation, balanced classes
3. **Performance**: GPU operations, batch transfers, gradient accumulation
4. **MLOps**: Seed setting, experiment tracking, config management
5. **Testing**: Unit tests for data pipeline, model output shape tests

## Integration
- `python-reviewer` skill: General Python code quality
- `python-data-reviewer` skill: Data preprocessing patterns
- `test-generator` skill: ML test generation
- `docker-reviewer` skill: ML containerization

## Notes
- Based on PyTorch 2.x, TensorFlow 2.x, scikit-learn 1.x
- Supports distributed training patterns (DDP, FSDP)
- Includes MLOps patterns (wandb, mlflow, hydra)
