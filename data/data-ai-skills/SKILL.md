---
name: data-ai-skills
description: Master machine learning, data engineering, AI engineering, LLMs, prompt engineering, and MLOps. Build intelligent systems with Python.
sasmp_version: "1.3.0"
skill_type: atomic
version: "2.0.0"

parameters:
  domain:
    type: string
    enum: [ml, deep-learning, llm, data-engineering, analytics]
    default: ml
  framework:
    type: string
    enum: [pytorch, tensorflow, sklearn, langchain]
    default: pytorch

validation_rules:
  - pattern: "^[a-z_][a-z0-9_]*$"
    target: function_names
    message: Use snake_case for Python functions
  - pattern: ".*\\.py$"
    target: script_files
    message: Python files must end with .py

retry_config:
  max_attempts: 5
  backoff: exponential
  initial_delay_ms: 2000
  max_delay_ms: 60000

logging:
  on_entry: "[ML] Starting: {task}"
  on_success: "[ML] Completed: {task} - Metrics: {metrics}"
  on_error: "[ML] Failed: {task} - {error}"

dependencies:
  agents:
    - data-ai-engineer
---

# Data & AI Engineering Skills

## Python Fundamentals

```python
import numpy as np
import pandas as pd
from typing import Optional, List

# NumPy arrays with type hints
def process_array(arr: np.ndarray) -> np.ndarray:
    """Process numpy array with validation."""
    if arr.size == 0:
        raise ValueError("Empty array not allowed")
    return np.clip(arr, 0, 1)

# Pandas DataFrames with error handling
def load_data(path: str) -> pd.DataFrame:
    """Load data with validation."""
    try:
        df = pd.read_csv(path)
        if df.empty:
            raise ValueError(f"Empty dataset: {path}")
        return df
    except FileNotFoundError:
        raise FileNotFoundError(f"Data file not found: {path}")
```

## Machine Learning with Scikit-Learn

```python
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import logging

logger = logging.getLogger(__name__)

def train_model(X, y, n_estimators=100, random_state=42):
    """Train model with logging and validation."""
    logger.info(f"Training with {len(X)} samples")

    # Validate input
    if len(X) != len(y):
        raise ValueError("X and y must have same length")

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=random_state, stratify=y
    )

    # Train
    model = RandomForestClassifier(n_estimators=n_estimators)
    model.fit(X_train, y_train)

    # Evaluate
    y_pred = model.predict(X_test)
    report = classification_report(y_test, y_pred, output_dict=True)

    logger.info(f"Accuracy: {report['accuracy']:.4f}")
    return model, report
```

## Deep Learning with PyTorch

```python
import torch
import torch.nn as nn
from torch.utils.data import DataLoader

class SimpleNet(nn.Module):
    def __init__(self, input_dim: int, hidden_dim: int = 64):
        super().__init__()
        self.fc1 = nn.Linear(input_dim, hidden_dim)
        self.fc2 = nn.Linear(hidden_dim, 1)
        self.relu = nn.ReLU()
        self.dropout = nn.Dropout(0.2)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = self.relu(self.fc1(x))
        x = self.dropout(x)
        return torch.sigmoid(self.fc2(x))

def train_epoch(model, dataloader, optimizer, loss_fn, device):
    """Train one epoch with gradient clipping."""
    model.train()
    total_loss = 0

    for batch_x, batch_y in dataloader:
        batch_x, batch_y = batch_x.to(device), batch_y.to(device)

        optimizer.zero_grad()
        output = model(batch_x)
        loss = loss_fn(output, batch_y)
        loss.backward()

        # Gradient clipping
        torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)

        optimizer.step()
        total_loss += loss.item()

    return total_loss / len(dataloader)
```

## LLM Applications (2025 Best Practices)

```python
from anthropic import Anthropic
import backoff

client = Anthropic()

@backoff.on_exception(backoff.expo, Exception, max_tries=3)
def query_llm(prompt: str, max_tokens: int = 1024) -> str:
    """Query LLM with retry logic."""
    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=max_tokens,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return message.content[0].text

# Structured output
def extract_entities(text: str) -> dict:
    """Extract entities with validation."""
    prompt = f"""Extract entities from the text.
    Return JSON with keys: persons, organizations, locations.

    Text: {text}
    """
    response = query_llm(prompt)
    return json.loads(response)
```

## Data Pipeline with Checkpointing

```python
import os
from pathlib import Path

def process_with_checkpoint(
    df: pd.DataFrame,
    checkpoint_dir: str,
    step_name: str
) -> pd.DataFrame:
    """Process with checkpoint recovery."""
    checkpoint_path = Path(checkpoint_dir) / f"{step_name}.parquet"

    if checkpoint_path.exists():
        print(f"Loading checkpoint: {step_name}")
        return pd.read_parquet(checkpoint_path)

    # Process
    result = expensive_transform(df)

    # Save checkpoint
    checkpoint_path.parent.mkdir(parents=True, exist_ok=True)
    result.to_parquet(checkpoint_path)

    return result
```

## MLOps with MLflow

```python
import mlflow
import mlflow.sklearn

def train_with_tracking(X_train, y_train, X_test, y_test, params):
    """Train with experiment tracking."""
    mlflow.set_experiment("model-training")

    with mlflow.start_run():
        # Log parameters
        mlflow.log_params(params)

        # Train
        model = RandomForestClassifier(**params)
        model.fit(X_train, y_train)

        # Evaluate
        accuracy = model.score(X_test, y_test)
        mlflow.log_metric("accuracy", accuracy)

        # Log model
        mlflow.sklearn.log_model(model, "model")

        return model, accuracy
```

## Model Evaluation Metrics

| Task | Primary Metric | Secondary Metrics |
|------|---------------|-------------------|
| Classification | Accuracy, F1 | Precision, Recall, AUC |
| Regression | RMSE, MAE | R², MAPE |
| Ranking | NDCG | MRR, MAP |
| Clustering | Silhouette | Davies-Bouldin |

## Unit Test Template

```python
import pytest
import numpy as np
from your_module import train_model, process_array

class TestMLFunctions:
    @pytest.fixture
    def sample_data(self):
        X = np.random.randn(100, 10)
        y = np.random.randint(0, 2, 100)
        return X, y

    def test_train_model(self, sample_data):
        X, y = sample_data
        model, report = train_model(X, y)

        assert model is not None
        assert 'accuracy' in report
        assert 0 <= report['accuracy'] <= 1

    def test_process_array_empty(self):
        with pytest.raises(ValueError, match="Empty array"):
            process_array(np.array([]))

    def test_process_array_clips(self):
        arr = np.array([−1, 0.5, 2])
        result = process_array(arr)
        assert result.min() >= 0
        assert result.max() <= 1
```

## Troubleshooting Guide

| Symptom | Cause | Solution |
|---------|-------|----------|
| CUDA OOM | Batch too large | Reduce batch, use gradient accumulation |
| Loss NaN | Learning rate too high | Reduce LR, add gradient clipping |
| Overfitting | Model too complex | Add regularization, more data |
| Slow training | I/O bottleneck | Use DataLoader workers |

## Key Concepts Checklist

- [ ] Python basics and NumPy
- [ ] Pandas data manipulation
- [ ] Data visualization (Matplotlib, Seaborn)
- [ ] Supervised learning (classification, regression)
- [ ] Unsupervised learning (clustering)
- [ ] Feature engineering
- [ ] Model evaluation and metrics
- [ ] Hyperparameter tuning
- [ ] Cross-validation
- [ ] Handling imbalanced data
- [ ] Deep learning basics
- [ ] LLM integration
- [ ] Prompt engineering
- [ ] MLOps pipeline setup

---

**Source**: https://roadmap.sh
**Version**: 2.0.0
**Last Updated**: 2025-01-01
