---
name: paper-to-code
description: Implement AI/ML research papers from scratch when no official code exists. Use when the user wants to reproduce a paper, implement an algorithm from a PDF, build a model architecture from a research paper, or create working code from academic publications. Handles papers from arXiv, NeurIPS, ICML, ICLR, CVPR, and other venues. Produces UV-managed, GPU-ready Python projects with tests, demos, and documentation.
---

# LeCoder: From Scratch Implementation

Implement AI/ML research papers from scratch. Produces production-ready, UV-managed Python projects.

**Motto**: Less Code, More Reproduction

## Workflow Overview

```
PDF → Markdown → Algorithm Extraction → Implementation → Testing → Packaging
```

## Phase 1: Paper Analysis

### 1.1 Convert Paper to Markdown

Use markitdown to convert the PDF for searchable algorithm extraction:

```python
from markitdown import MarkItDown

md = MarkItDown()
result = md.convert("paper.pdf")

# Save for grep-based extraction
with open("paper.md", "w") as f:
    f.write(result.text_content)
```

### 1.2 Extract Key Components

Search for algorithms, definitions, and equations:

```bash
# Find algorithms
grep -n -i "algorithm\|procedure\|method" paper.md

# Find definitions  
grep -n -i "definition\|theorem\|lemma\|proposition" paper.md

# Find equations (look for equation numbers)
grep -n -E "\([0-9]+\)|\{[0-9]+\}" paper.md

# Find architecture descriptions
grep -n -i "architecture\|layer\|block\|module" paper.md
```

### 1.3 Create Implementation Checklist

Extract and document before coding:

```markdown
## Implementation Checklist

### Core Algorithms
- [ ] Algorithm 1: [Name] (Equations X-Y)
- [ ] Algorithm 2: [Name] (Section Z)

### Model Components
- [ ] Component A: [Description]
- [ ] Component B: [Description]

### Key Equations
- [ ] Equation N: [Purpose]
- [ ] Equation M: [Purpose]

### Hyperparameters (from paper)
| Parameter | Value | Reference |
|-----------|-------|-----------|
| lr | 0.001 | Section 4.2 |
```

## Phase 2: Project Setup

### 2.1 Initialize UV Project

```bash
# Create project
uv init project-name
cd project-name

# Pin Python version
uv python pin 3.11

# Add core dependencies
uv add torch numpy scipy
uv add --dev pytest ruff mypy

# Add optional dependencies
uv add --group demo gradio
uv add --group docs sphinx
```

### 2.2 Create Project Structure

```
project-name/
├── .gitignore              # CRITICAL: Include from day 1
├── .python-version         # UV Python pin
├── pyproject.toml          # UV project config
├── uv.lock                 # Lockfile (commit this)
├── README.md               # Quickstart-first documentation
├── requirements.txt        # For non-UV users
├── src/
│   ├── __init__.py
│   ├── core/               # Optimizers, memory systems
│   │   ├── __init__.py
│   │   └── [components].py
│   └── models/             # Architectures
│       ├── __init__.py
│       └── [models].py
├── tests/
│   └── test_components.py  # Comprehensive tests
├── demo/
│   └── app.py              # Gradio interactive demo
├── notebooks/
│   └── quickstart.ipynb    # Minimal sanity check
├── configs/                # Model configurations
│   ├── small.yaml
│   ├── medium.yaml
│   └── large.yaml
├── docs/
│   └── ALGORITHMS.md       # Mathematical formulations
└── train.py                # Training entrypoint
```

### 2.3 Essential .gitignore

```gitignore
# Environments
.venv/
venv/
env/

# Caches
__pycache__/
*.pyc
.pytest_cache/
.ruff_cache/
.mypy_cache/

# UV
.uv/

# Logs and outputs
logs/
outputs/
checkpoints/
*.log
wandb/

# Secrets (CRITICAL)
*.env
.env*
*credentials*
*secret*
*.json  # Be careful with config files containing keys

# IDE
.vscode/
.idea/

# OS
.DS_Store
Thumbs.db
```

## Phase 3: Implementation

### 3.1 Implementation Order

1. **Utility functions first**: Activation functions, normalization, etc.
2. **Core algorithms**: Optimizers, memory systems
3. **Building blocks**: Attention, MLP blocks
4. **Full architectures**: Complete models
5. **Training loop**: Data loading, optimization

### 3.2 Code Patterns

**Device-agnostic code**:
```python
def get_device():
    if torch.cuda.is_available():
        return torch.device("cuda")
    elif torch.backends.mps.is_available():
        return torch.device("mps")
    return torch.device("cpu")

# Use throughout
device = get_device()
model = Model().to(device)
```

**Factory functions for easy instantiation**:
```python
def create_model(
    d_model: int = 512,
    num_layers: int = 6,
    **kwargs
) -> Model:
    """Create model with sensible defaults."""
    config = ModelConfig(d_model=d_model, num_layers=num_layers, **kwargs)
    return Model(config)
```

**Config dataclasses**:
```python
from dataclasses import dataclass

@dataclass
class ModelConfig:
    d_model: int = 512
    num_layers: int = 6
    num_heads: int = 8
    d_hidden: int = 2048
    dropout: float = 0.1
```

### 3.3 Mathematical Documentation

Document equations in docstrings:
```python
def forward(self, x: torch.Tensor) -> torch.Tensor:
    """
    Forward pass implementing Equation 57 from the paper:
    
    W_{t+1} = W_t(I - η' x x^T) - η' ∇L ⊗ x
    
    where η' = η / (1 + η) for normalized inputs.
    
    Args:
        x: Input tensor of shape (batch, seq_len, d_model)
    
    Returns:
        Output tensor of shape (batch, seq_len, d_model)
    """
```

## Phase 4: Testing

### 4.1 Test Categories

```python
import pytest
import torch

class TestComponent:
    """Test individual component."""
    
    def test_output_shape(self):
        """Verify output dimensions match expected."""
        model = Component(d_model=64)
        x = torch.randn(2, 16, 64)
        out = model(x)
        assert out.shape == x.shape
    
    def test_gradient_flow(self):
        """Verify gradients propagate correctly."""
        model = Component(d_model=64)
        x = torch.randn(2, 16, 64, requires_grad=True)
        out = model(x)
        loss = out.sum()
        loss.backward()
        assert x.grad is not None
        assert not torch.isnan(x.grad).any()
    
    def test_device_placement(self):
        """Verify model works on available device."""
        device = get_device()
        model = Component(d_model=64).to(device)
        x = torch.randn(2, 16, 64, device=device)
        out = model(x)
        assert out.device == device
```

### 4.2 Lightweight Smoke Test

Keep GPU tests small to avoid OOM:
```python
def test_training_step():
    """Quick training step - keep tensors small."""
    model = Model(d_model=64, num_layers=2)  # Small config
    optimizer = torch.optim.Adam(model.parameters())
    
    x = torch.randn(2, 32, 64)  # Small batch
    loss = model(x).sum()
    loss.backward()
    optimizer.step()
    
    assert loss.item() > 0  # Sanity check
```

## Phase 5: Demo & Documentation

### 5.1 Gradio Demo Template

```python
import gradio as gr
import torch

def demo_function(input_text: str, config: str) -> str:
    """Demo function with config selection."""
    # Load appropriate config
    model = load_model(config)
    result = model.process(input_text)
    return result

demo = gr.Interface(
    fn=demo_function,
    inputs=[
        gr.Textbox(label="Input"),
        gr.Dropdown(["small", "medium", "large"], label="Config")
    ],
    outputs=gr.Textbox(label="Output"),
    title="Paper Name Demo",
    description="Interactive demo of [Paper Title]"
)

if __name__ == "__main__":
    demo.launch()
```

### 5.2 README Structure (Quickstart-First)

```markdown
# Project Name

Brief description + paper links.

## Quick Start

```bash
git clone https://github.com/user/repo.git
cd repo

# UV setup (recommended)
uv venv && source .venv/bin/activate
uv sync

# Run tests
uv run pytest tests/

# Launch demo
uv run python demo/app.py

# Train (configs: small/medium/large)
uv run python train.py --config small --steps 500
```

## What is [Paper Concept]?

2-3 sentence explanation.

## Architecture Overview

ASCII diagram of architecture.

## Components

Brief list with links to docs.

## Citation

BibTeX entry.
```

### 5.3 Quickstart Notebook

```python
# notebooks/quickstart.ipynb
# Cell 1: Install
# !pip install -r requirements.txt

# Cell 2: Import and test
from src.models import create_model
import torch

model = create_model(d_model=64, num_layers=2)
x = torch.randn(1, 16, 64)
out = model(x)
print(f"Input: {x.shape} → Output: {out.shape}")

# Cell 3: Training step
optimizer = torch.optim.Adam(model.parameters())
loss = out.sum()
loss.backward()
optimizer.step()
print("✓ Forward and backward pass successful")
```

## Phase 6: Packaging

### 6.1 Final Checklist

```markdown
## Pre-Release Checklist

### Files
- [ ] .gitignore present and comprehensive
- [ ] requirements.txt generated: `uv export > requirements.txt`
- [ ] All __init__.py files export public API
- [ ] No credentials or secrets in any file

### Tests
- [ ] All tests pass: `uv run pytest -v`
- [ ] Tests are lightweight (no OOM on small GPUs)

### Documentation  
- [ ] README leads with quickstart
- [ ] Concrete example commands provided
- [ ] Hardware requirements noted (CPU vs GPU)
- [ ] Paper links included

### Demo
- [ ] Gradio demo runs: `uv run python demo/app.py`
- [ ] Notebook executes without errors

### Training
- [ ] Config presets work: small, medium, large
- [ ] CPU fallback documented
```

### 6.2 Export Requirements

```bash
# Generate requirements.txt for pip users
uv export --format requirements-txt > requirements.txt

# Or with dev dependencies
uv export --format requirements-txt --all-extras > requirements-dev.txt
```

## Best Practices Summary

1. **Start clean**: .gitignore + no secrets from commit 1
2. **Quickstart first**: README leads with copy-paste commands
3. **Small defaults**: Config presets start small for quick testing
4. **Device agnostic**: Code works on CPU, CUDA, MPS
5. **Lightweight tests**: Avoid large tensors that OOM
6. **Factory functions**: Easy model instantiation
7. **Document math**: Equations in docstrings with paper references
8. **UV-first**: Modern Python packaging throughout

## References

- `references/paper-analysis.md` - Deep dive on algorithm extraction
- `references/implementation-patterns.md` - Code patterns and anti-patterns
- `references/packaging-checklist.md` - Complete packaging guide

## Example Projects

This skill was validated on:
- **Nested Learning (NeurIPS 2025)**: HOPE architecture, CMS, DGD optimizer
  - Successfully trained on A100 via Colab
  - All code correct from first generation
  - Friction was documentation, not code
