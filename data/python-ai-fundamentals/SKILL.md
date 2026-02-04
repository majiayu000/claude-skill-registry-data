---
name: Python AI Fundamentals
description: Expert guidance for Python AI development fundamentals, essential libraries, data structures, async programming, and best practices for AI/ML projects
version: 1.0.0
---

# Python AI Fundamentals

Expert-level knowledge for Python AI/ML development, including core libraries, patterns, and best practices.

## Core Python Libraries for AI/ML

### Essential AI/ML Stack
```python
# Core numerical computing
import numpy as np
import pandas as pd

# Machine Learning
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# Deep Learning
import torch
import torch.nn as nn
import tensorflow as tf

# Data visualization
import matplotlib.pyplot as plt
import seaborn as sns

# API development
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

# Async operations
import asyncio
import aiohttp
```

### Environment Management
```bash
# Using uv (fast package manager)
pip install uv
uv venv
source .venv/bin/activate

# Or traditional virtualenv
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Install dependencies
pip install numpy pandas scikit-learn torch transformers
```

## Data Handling Patterns

### Working with DataFrames
```python
import pandas as pd
import numpy as np

# Load and explore data
df = pd.read_csv('data.csv')
print(df.info())
print(df.describe())
print(df.head())

# Handle missing values
df.fillna(df.mean(), inplace=True)
df.dropna(subset=['important_column'], inplace=True)

# Feature engineering
df['new_feature'] = df['col1'] * df['col2']
df['date'] = pd.to_datetime(df['date_string'])

# One-hot encoding
df_encoded = pd.get_dummies(df, columns=['category'])

# Train-test split
from sklearn.model_selection import train_test_split
X = df.drop('target', axis=1)
y = df['target']
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
```

### NumPy Operations
```python
import numpy as np

# Array creation
arr = np.array([1, 2, 3, 4, 5])
matrix = np.random.randn(3, 4)
zeros = np.zeros((2, 3))
ones = np.ones((3, 3))

# Operations
mean = np.mean(arr)
std = np.std(arr)
normalized = (arr - mean) / std

# Broadcasting
result = matrix + arr[:, np.newaxis]
```

## Async Programming for AI Applications

### Basic Async Pattern
```python
import asyncio
import aiohttp

async def fetch_data(url: str) -> dict:
    """Async HTTP request"""
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()

async def process_multiple_requests(urls: list[str]):
    """Process multiple requests concurrently"""
    tasks = [fetch_data(url) for url in urls]
    results = await asyncio.gather(*tasks)
    return results

# Run async code
asyncio.run(process_multiple_requests(urls))
```

### Async with Semaphore (Rate Limiting)
```python
async def fetch_with_limit(url: str, semaphore: asyncio.Semaphore):
    """Rate-limited async requests"""
    async with semaphore:
        return await fetch_data(url)

async def batch_process(urls: list[str], max_concurrent: int = 5):
    """Process with concurrency limit"""
    semaphore = asyncio.Semaphore(max_concurrent)
    tasks = [fetch_with_limit(url, semaphore) for url in urls]
    return await asyncio.gather(*tasks)
```

## Type Hints and Validation

### Pydantic Models
```python
from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime

class TrainingConfig(BaseModel):
    """Model configuration with validation"""
    model_name: str = Field(..., min_length=1)
    learning_rate: float = Field(0.001, gt=0, lt=1)
    batch_size: int = Field(32, ge=1)
    epochs: int = Field(10, ge=1)
    device: str = Field("cuda", pattern="^(cuda|cpu|mps)$")

    @validator('learning_rate')
    def validate_lr(cls, v):
        if v > 0.1:
            raise ValueError('Learning rate too high')
        return v

class PredictionRequest(BaseModel):
    """API request model"""
    text: str = Field(..., min_length=1, max_length=1000)
    model_id: str
    temperature: float = Field(0.7, ge=0, le=2)
    max_tokens: Optional[int] = Field(None, ge=1, le=4096)

class PredictionResponse(BaseModel):
    """API response model"""
    result: str
    confidence: float
    processing_time: float
    timestamp: datetime
```

### Type Hints Best Practices
```python
from typing import Dict, List, Optional, Union, Tuple, Callable
import numpy as np
from numpy.typing import NDArray

def preprocess_data(
    data: pd.DataFrame,
    columns: List[str],
    scaler: Optional[StandardScaler] = None
) -> Tuple[NDArray, StandardScaler]:
    """
    Preprocess data with proper type hints

    Args:
        data: Input dataframe
        columns: Columns to process
        scaler: Optional pre-fitted scaler

    Returns:
        Tuple of processed array and scaler
    """
    X = data[columns].values

    if scaler is None:
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
    else:
        X_scaled = scaler.transform(X)

    return X_scaled, scaler

# Type hints for callbacks
def train_model(
    model: nn.Module,
    data_loader: torch.utils.data.DataLoader,
    callback: Optional[Callable[[int, float], None]] = None
) -> nn.Module:
    """Train with optional callback"""
    for epoch, (inputs, labels) in enumerate(data_loader):
        loss = compute_loss(model, inputs, labels)
        if callback:
            callback(epoch, loss.item())
    return model
```

## Error Handling and Logging

### Robust Error Handling
```python
import logging
from functools import wraps
from typing import TypeVar, Callable

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

T = TypeVar('T')

def retry_on_failure(max_retries: int = 3, delay: float = 1.0):
    """Retry decorator for AI operations"""
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        async def wrapper(*args, **kwargs) -> T:
            for attempt in range(max_retries):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    logger.warning(f"Attempt {attempt + 1} failed: {e}")
                    if attempt < max_retries - 1:
                        await asyncio.sleep(delay * (2 ** attempt))
                    else:
                        logger.error(f"All {max_retries} attempts failed")
                        raise
        return wrapper
    return decorator

@retry_on_failure(max_retries=3)
async def call_ai_model(prompt: str) -> str:
    """Call AI model with retry logic"""
    # Model inference code here
    pass
```

### Context Managers
```python
from contextlib import contextmanager
import time

@contextmanager
def timer(name: str):
    """Time code execution"""
    start = time.time()
    try:
        yield
    finally:
        end = time.time()
        logger.info(f"{name} took {end - start:.2f}s")

# Usage
with timer("Model inference"):
    result = model.predict(data)
```

## Best Practices

### Project Structure
```
project/
├── src/
│   ├── __init__.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── classifier.py
│   ├── data/
│   │   ├── __init__.py
│   │   └── preprocessing.py
│   ├── training/
│   │   ├── __init__.py
│   │   └── trainer.py
│   └── api/
│       ├── __init__.py
│       └── endpoints.py
├── tests/
│   ├── __init__.py
│   └── test_models.py
├── notebooks/
│   └── exploration.ipynb
├── configs/
│   └── config.yaml
├── requirements.txt
├── pyproject.toml
└── README.md
```

### Configuration Management
```python
from dataclasses import dataclass
from pathlib import Path
import yaml

@dataclass
class Config:
    """Application configuration"""
    model_path: Path
    data_path: Path
    batch_size: int
    learning_rate: float
    device: str

    @classmethod
    def from_yaml(cls, path: str) -> 'Config':
        """Load config from YAML"""
        with open(path) as f:
            config_dict = yaml.safe_load(f)
        return cls(**config_dict)

    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            'model_path': str(self.model_path),
            'data_path': str(self.data_path),
            'batch_size': self.batch_size,
            'learning_rate': self.learning_rate,
            'device': self.device
        }
```

### Testing
```python
import pytest
import numpy as np
from unittest.mock import Mock, patch

def test_data_preprocessing():
    """Test preprocessing function"""
    # Arrange
    data = pd.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]})

    # Act
    result, scaler = preprocess_data(data, ['a', 'b'])

    # Assert
    assert result.shape == (3, 2)
    assert np.allclose(result.mean(axis=0), 0, atol=1e-7)
    assert np.allclose(result.std(axis=0), 1, atol=1e-7)

@pytest.mark.asyncio
async def test_async_inference():
    """Test async model inference"""
    result = await call_ai_model("test prompt")
    assert isinstance(result, str)
    assert len(result) > 0
```

## Performance Optimization

### Vectorization
```python
# Bad: Loop
result = []
for x in data:
    result.append(x ** 2 + 2 * x + 1)

# Good: Vectorized
result = data ** 2 + 2 * data + 1

# NumPy operations
arr = np.array(data)
result = np.power(arr, 2) + 2 * arr + 1
```

### Memory Management
```python
import gc
import torch

def clear_memory():
    """Clear GPU/CPU memory"""
    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()

# Use generators for large datasets
def data_generator(file_path: str, chunk_size: int = 1000):
    """Generate data chunks"""
    for chunk in pd.read_csv(file_path, chunksize=chunk_size):
        yield preprocess_chunk(chunk)
```

## Common Patterns

### Singleton Pattern for Model Loading
```python
class ModelSingleton:
    """Singleton for expensive model loading"""
    _instance = None
    _model = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def get_model(self):
        if self._model is None:
            self._model = self._load_model()
        return self._model

    def _load_model(self):
        # Expensive model loading
        return load_pretrained_model()
```

### Factory Pattern for Model Creation
```python
from abc import ABC, abstractmethod

class ModelFactory:
    """Factory for creating different model types"""

    @staticmethod
    def create_model(model_type: str, **kwargs):
        if model_type == "classifier":
            return ClassifierModel(**kwargs)
        elif model_type == "regression":
            return RegressionModel(**kwargs)
        else:
            raise ValueError(f"Unknown model type: {model_type}")
```

## Key Principles

1. **Use type hints everywhere** - Improves code quality and IDE support
2. **Validate inputs with Pydantic** - Catch errors early
3. **Async for I/O operations** - Better performance for API calls
4. **Vectorize with NumPy/Pandas** - Avoid Python loops
5. **Log extensively** - Debug production issues easily
6. **Test thoroughly** - Prevent regressions
7. **Use virtual environments** - Isolate dependencies
8. **Profile before optimizing** - Optimize bottlenecks only
9. **Handle errors gracefully** - Retry with exponential backoff
10. **Document with docstrings** - Help future developers

## Resources

- NumPy: https://numpy.org/doc/
- Pandas: https://pandas.pydata.org/docs/
- Pydantic: https://docs.pydantic.dev/
- FastAPI: https://fastapi.tiangolo.com/
- PyTorch: https://pytorch.org/docs/
- scikit-learn: https://scikit-learn.org/
