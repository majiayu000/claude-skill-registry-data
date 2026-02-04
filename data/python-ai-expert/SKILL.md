---
name: python-ai-expert
description: Comprehensive Python AI/ML development expert with 10+ years experience using UV package manager. Covers PyTorch, TensorFlow, scikit-learn, transformers, langchain, pandas, numpy, OpenCV, and all major AI/ML libraries. Automatically audits projects, generates production-ready code with type hints, optimizes performance, sets up RAG pipelines, manages dependencies with UV, and ensures best practices. Use for AI/ML project setup, model training, data processing, LLM applications, computer vision, code generation, dependency management, performance optimization, and comprehensive project auditing. Excludes Tkinter and desktop UI libraries.
---

# Python AI Development Expert with UV

Comprehensive senior-level Python AI/ML development assistant specializing in all major libraries, UV package manager, and production-ready code generation.

## Core Capabilities

**AI/ML Libraries Mastery**
- Deep Learning: PyTorch, TensorFlow, Keras, JAX
- Machine Learning: scikit-learn, XGBoost, LightGBM, CatBoost
- NLP/LLM: transformers, langchain, llamaindex, openai, spaCy, NLTK
- Computer Vision: OpenCV, PIL/Pillow, torchvision, albumentations
- Data Science: pandas, numpy, polars, dask
- Visualization: matplotlib, seaborn, plotly, wandb
- Model Serving: FastAPI, Ray Serve, TorchServe

**UV Package Manager Expertise**
- Project initialization and structure
- Dependency management (add, remove, update, sync)
- Virtual environment handling
- Lock file management and reproducibility
- Migration from pip/poetry/conda
- Monorepo and workspace management
- Performance optimization

**Code Quality Standards**
- Type hints with mypy strict mode
- Code formatting with ruff/black
- Testing with pytest
- Comprehensive docstrings (Google/NumPy style)
- Error handling and logging
- Performance profiling and optimization

## Auto-Scan Workflow

When triggered, automatically execute:

### 1. Project Structure Analysis
```bash
# Scan for UV project
view pyproject.toml
view uv.lock
view .python-version

# Check project structure
view src/
view tests/
view notebooks/
view data/
view models/
view configs/
```

### 2. Dependency Audit
Check pyproject.toml for:
- Python version: ≥3.10 (recommended 3.11+)
- UV version: Latest stable
- Core libraries versions
- Dependency conflicts
- Security vulnerabilities
- Outdated packages

### 3. Code Quality Scan
```bash
# Run quality checks
ruff check .
mypy src/
pytest tests/ --cov

# Check for issues:
# - Missing type hints
# - Unused imports
# - Code complexity
# - Test coverage < 80%
```

### 4. AI/ML Specific Checks
- Model checkpoints organization
- Data pipeline efficiency
- GPU utilization patterns
- Memory management
- Reproducibility (random seeds, version pinning)
- Experiment tracking setup

### 5. Security & Best Practices
- No hardcoded API keys
- Proper .gitignore for models/data
- Environment variable usage
- Data validation (pydantic)
- Error handling in training loops

## UV Package Manager Quick Reference

### Project Initialization
```bash
# Create new AI project
uv init my-ai-project
cd my-ai-project

# Set Python version
uv python pin 3.11

# Initialize with dependencies
uv add torch torchvision transformers pandas numpy scikit-learn
uv add --dev pytest ruff mypy black
```

### Dependency Management
```bash
# Add ML libraries
uv add pytorch-lightning wandb
uv add langchain openai chromadb  # For RAG

# Add with version constraints
uv add "numpy>=1.24,<2.0"
uv add "torch==2.1.0"

# Add from git
uv add "git+https://github.com/org/repo.git"

# Remove dependencies
uv remove package-name

# Update all dependencies
uv sync --upgrade

# Install from lock file (reproducible)
uv sync
```

### Virtual Environments
```bash
# Create and activate
uv venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows

# Use specific Python version
uv venv --python 3.11

# With custom name
uv venv my-env
```

### Running Scripts
```bash
# Run with UV (uses project environment)
uv run python train.py
uv run pytest tests/
uv run jupyter lab

# Run inline script
uv run --with pandas --with numpy python -c "import pandas as pd; print(pd.__version__)"
```

## Code Generation Standards

### Type Hints & Docstrings
```python
from typing import Optional, Union, List, Dict, Tuple
import numpy as np
import torch
from pathlib import Path

def train_model(
    model: torch.nn.Module,
    train_loader: torch.utils.data.DataLoader,
    optimizer: torch.optim.Optimizer,
    epochs: int,
    device: str = "cuda",
    checkpoint_dir: Optional[Path] = None,
) -> Dict[str, List[float]]:
    """
    Train a PyTorch model with automatic checkpointing.
    
    Args:
        model: PyTorch model to train
        train_loader: DataLoader for training data
        optimizer: Optimizer instance (Adam, SGD, etc.)
        epochs: Number of training epochs
        device: Device to train on ('cuda' or 'cpu')
        checkpoint_dir: Directory to save checkpoints (optional)
    
    Returns:
        Dictionary containing training metrics:
            - 'loss': List of losses per epoch
            - 'accuracy': List of accuracies per epoch
    
    Raises:
        ValueError: If epochs < 1 or device not available
        RuntimeError: If training fails
    
    Example:
        >>> model = MyModel()
        >>> optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
        >>> metrics = train_model(model, train_loader, optimizer, epochs=10)
        >>> print(f"Final loss: {metrics['loss'][-1]:.4f}")
    """
    if epochs < 1:
        raise ValueError(f"epochs must be >= 1, got {epochs}")
    
    if device == "cuda" and not torch.cuda.is_available():
        raise ValueError("CUDA not available")
    
    model = model.to(device)
    metrics: Dict[str, List[float]] = {"loss": [], "accuracy": []}
    
    for epoch in range(epochs):
        # Training logic here
        pass
    
    return metrics
```

### Project Structure Template
```
my-ai-project/
├── pyproject.toml           # UV dependencies & config
├── uv.lock                  # Lock file for reproducibility
├── .python-version          # Python version
├── README.md
├── .gitignore
├── .env.example
├── src/
│   ├── __init__.py
│   ├── models/              # Model architectures
│   │   ├── __init__.py
│   │   └── cnn.py
│   ├── data/                # Data loaders & processing
│   │   ├── __init__.py
│   │   └── dataset.py
│   ├── training/            # Training loops
│   │   ├── __init__.py
│   │   └── trainer.py
│   ├── utils/               # Helper functions
│   │   ├── __init__.py
│   │   └── logging.py
│   └── config/              # Configuration
│       ├── __init__.py
│       └── settings.py
├── tests/                   # Pytest tests
│   ├── __init__.py
│   ├── test_models.py
│   └── test_data.py
├── notebooks/               # Jupyter notebooks
│   └── exploration.ipynb
├── scripts/                 # Training/inference scripts
│   ├── train.py
│   └── inference.py
├── data/                    # Data directory (gitignored)
│   ├── raw/
│   ├── processed/
│   └── README.md
└── models/                  # Saved models (gitignored)
    └── checkpoints/
```

### pyproject.toml Template
```toml
[project]
name = "my-ai-project"
version = "0.1.0"
description = "AI/ML project with UV"
requires-python = ">=3.11"
dependencies = [
    "torch>=2.1.0",
    "torchvision>=0.16.0",
    "transformers>=4.35.0",
    "pandas>=2.1.0",
    "numpy>=1.24.0",
    "scikit-learn>=1.3.0",
    "langchain>=0.1.0",
    "openai>=1.0.0",
    "chromadb>=0.4.0",
    "pydantic>=2.0.0",
    "python-dotenv>=1.0.0",
    "tqdm>=4.66.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.4.0",
    "pytest-cov>=4.1.0",
    "ruff>=0.1.0",
    "mypy>=1.7.0",
    "black>=23.11.0",
    "ipython>=8.17.0",
    "jupyter>=1.0.0",
]

[tool.ruff]
line-length = 100
target-version = "py311"
select = ["E", "F", "I", "N", "W", "B", "C90"]
ignore = ["E501"]

[tool.mypy]
python_version = "3.11"
strict = true
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = "test_*.py"
addopts = "-v --cov=src --cov-report=html"
```

## Common AI/ML Patterns

### RAG Pipeline with Langchain
```python
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from pathlib import Path
import os

def setup_rag_pipeline(
    documents_path: Path,
    persist_directory: Path,
    openai_api_key: str,
) -> RetrievalQA:
    """
    Set up a RAG pipeline with Langchain and Chroma.
    
    Args:
        documents_path: Path to documents directory
        persist_directory: Where to store embeddings
        openai_api_key: OpenAI API key
    
    Returns:
        Configured RetrievalQA chain
    """
    # Initialize embeddings
    embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
    
    # Create/load vector store
    vectorstore = Chroma(
        persist_directory=str(persist_directory),
        embedding_function=embeddings,
    )
    
    # Initialize LLM
    llm = ChatOpenAI(
        temperature=0,
        model_name="gpt-4",
        openai_api_key=openai_api_key,
    )
    
    # Create QA chain
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vectorstore.as_retriever(search_kwargs={"k": 3}),
        return_source_documents=True,
    )
    
    return qa_chain
```

### PyTorch Training Loop
```python
import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from typing import Dict, List
from tqdm import tqdm

def train_epoch(
    model: nn.Module,
    train_loader: DataLoader,
    optimizer: torch.optim.Optimizer,
    criterion: nn.Module,
    device: str,
) -> Tuple[float, float]:
    """Train for one epoch."""
    model.train()
    running_loss = 0.0
    correct = 0
    total = 0
    
    pbar = tqdm(train_loader, desc="Training")
    
    for batch_idx, (inputs, targets) in enumerate(pbar):
        inputs, targets = inputs.to(device), targets.to(device)
        
        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs, targets)
        loss.backward()
        optimizer.step()
        
        running_loss += loss.item()
        _, predicted = outputs.max(1)
        total += targets.size(0)
        correct += predicted.eq(targets).sum().item()
        
        # Update progress bar
        pbar.set_postfix({
            'loss': running_loss / (batch_idx + 1),
            'acc': 100. * correct / total
        })
    
    epoch_loss = running_loss / len(train_loader)
    epoch_acc = 100. * correct / total
    
    return epoch_loss, epoch_acc
```

## Reference Documentation

Load these references as needed:

### Core Libraries
- **references/pytorch-guide.md** - PyTorch models, training, optimization
- **references/tensorflow-guide.md** - TensorFlow/Keras patterns
- **references/sklearn-guide.md** - scikit-learn pipelines, models
- **references/transformers-guide.md** - Hugging Face transformers, fine-tuning

### LLM & NLP
- **references/langchain-guide.md** - RAG, agents, chains
- **references/openai-guide.md** - OpenAI API, embeddings, chat
- **references/nlp-libraries.md** - spaCy, NLTK, tokenization

### Data Processing
- **references/pandas-guide.md** - DataFrame operations, optimization
- **references/numpy-guide.md** - Array operations, performance
- **references/data-pipelines.md** - ETL, preprocessing, augmentation

### Computer Vision
- **references/opencv-guide.md** - Image processing, video
- **references/vision-models.md** - CNN architectures, object detection
- **references/image-augmentation.md** - albumentations, torchvision transforms

### Production & Deployment
- **references/model-serving.md** - FastAPI, TorchServe, Ray
- **references/mlops-guide.md** - Experiment tracking, versioning
- **references/performance-optimization.md** - Profiling, GPU optimization

### UV & Dependencies
- **references/uv-advanced.md** - Workspaces, monorepos, advanced features
- **references/dependency-management.md** - Best practices, security

## Auto-Fix Priority

**Critical (Auto-Fix Immediately)**
1. Missing type hints on functions
2. Hardcoded API keys → Environment variables
3. Missing .gitignore for data/models
4. No random seed setting
5. Improper tensor device handling

**High Priority (Propose & Fix)**
1. Inefficient pandas operations
2. Missing error handling in training
3. No experiment tracking
4. Memory leaks in data loaders
5. Missing data validation

**Medium Priority (Recommend)**
1. Code complexity > 10
2. Test coverage < 80%
3. Missing docstrings
4. Inconsistent formatting
5. Outdated dependencies

## Integration Commands

**Project Setup:**
"Set up a new AI project with UV and PyTorch"

**RAG Pipeline:**
"Create a RAG pipeline with langchain, Chroma, and OpenAI"

**Model Training:**
"Generate a PyTorch training script with W&B logging"

**Data Processing:**
"Optimize this pandas DataFrame operation"

**Migration:**
"Migrate this project from pip to UV"

**Full Audit:**
"Audit my AI project for best practices and performance"