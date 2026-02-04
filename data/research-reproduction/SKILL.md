---
name: research-reproduction
description: Reproduce research papers into working code. Use when user wants to implement ML/AI papers, reproduce experiments, extract algorithms from PDFs, or convert research into executable code. Handles multiple interconnected papers with multi-agent extraction, equation verification, and benchmark validation.
---

# Research Paper Reproduction Skill

Transform research papers into production-ready, verified code with multi-agent orchestration, equation-first verification, and benchmark validation.

## When to Use

- User provides research paper(s) (PDF, arXiv URL, or paper content)
- User wants to reproduce experiments from papers
- User needs to implement algorithms described in academic literature
- User wants verified, tested code matching paper specifications
- Multiple interconnected papers need coordinated implementation

## Quick Start

```
User: "Reproduce this paper" + [attaches PDF or provides arXiv URL]

You: 
1. Clarify intent (validate/implement/extend)
2. Spawn extraction agent(s) per paper
3. Create context documents
4. Implement with equation verification
5. Format, test, document
6. Init git, ready for execution
```

## Core Workflow

```
┌─────────────────────────────────────────────────────────────────┐
│                    RESEARCH REPRODUCTION PIPELINE                │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Phase 0: INTENT CLARIFICATION                                  │
│  ├─ What: Validate understanding / Implement / Extend / Benchmark│
│  ├─ Papers: Single / Multiple related / Paper family            │
│  ├─ Scope: Full paper / Specific algorithm / Core contribution  │
│  └─ Resources: Local / Colab / GPU requirements                 │
│                                                                  │
│  Phase 1: PARALLEL EXTRACTION (Multi-Agent)                     │
│  ├─ Spawn one extraction agent per paper                        │
│  ├─ Each agent creates context document (NOT full paper)        │
│  ├─ Extract: equations, algorithms, architecture, hyperparams   │
│  └─ Output: .context.md files in project root                   │
│                                                                  │
│  Phase 2: CONTEXT SYNTHESIS                                     │
│  ├─ Orchestrator reads all .context.md files                    │
│  ├─ Build dependency graph (which paper depends on which)       │
│  ├─ Create unified implementation plan                          │
│  └─ Output: IMPLEMENTATION_PLAN.md                              │
│                                                                  │
│  Phase 3: EQUATION-FIRST IMPLEMENTATION                         │
│  ├─ For EACH equation: write test FIRST                         │
│  ├─ Implement module to pass test                               │
│  ├─ Verify shapes, gradients, numerical stability               │
│  └─ Output: src/ with tests/ alongside                          │
│                                                                  │
│  Phase 4: CODE QUALITY                                          │
│  ├─ Format with ruff                                            │
│  ├─ Type check with ty (Astral)                                 │
│  ├─ Verify all tests pass                                       │
│  └─ Output: Clean, typed, formatted code                        │
│                                                                  │
│  Phase 5: DOCUMENTATION                                         │
│  ├─ Generate README.md with usage instructions                  │
│  ├─ Create ARCHITECTURE.md with diagrams                        │
│  ├─ Document each module's paper reference                      │
│  └─ Output: docs/ folder + root README                          │
│                                                                  │
│  Phase 6: GIT & EXECUTION PREP                                  │
│  ├─ git init, .gitignore, initial commit                        │
│  ├─ Prepare for gh repo create                                  │
│  ├─ Create run scripts (notebook + CLI)                         │
│  └─ Output: Ready for git push and execution                    │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Phase 0: Intent Clarification

**ALWAYS START HERE.** Ask the user:

```markdown
## Research Reproduction - Let's clarify your goals

**1. What's your intent?**
- [ ] Validate understanding - Quick implementation to verify I understand the paper
- [ ] Full reproduction - Complete implementation matching paper's experiments  
- [ ] Specific component - Implement only [specific algorithm/module]
- [ ] Extend/modify - Build on paper with custom changes
- [ ] Benchmark only - Run existing code, verify results

**2. Paper scope:**
- [ ] Single paper
- [ ] Multiple related papers (specify dependencies)
- [ ] Paper family (e.g., TITANS → MIRAS → Hope)

**3. Execution environment:**
- [ ] Local CPU only
- [ ] Local GPU (specify VRAM)
- [ ] Google Colab (Free/Pro - specify units budget)
- [ ] Cloud GPU (specify provider)

**4. Output preferences:**
- [ ] Jupyter notebook for experimentation
- [ ] CLI scripts for training/inference
- [ ] Both notebook + scripts
```

## Phase 1: Parallel Extraction

For EACH paper, spawn an extraction subagent:

```bash
# Subagent task (do NOT load full paper into orchestrator context)
Task: Extract from [paper_name]
Output: [paper_name].context.md

The extraction agent will:
1. Convert PDF to markdown (markitdown)
2. Extract ALL equations with LaTeX
3. Extract ALL algorithms (pseudocode)
4. Extract architecture diagrams (describe in text)
5. Extract hyperparameters and training details
6. Extract benchmark datasets and metrics
7. Note dependencies on other papers
```

**Extraction Agent Prompt:** See [prompts/extraction-agent.md](prompts/extraction-agent.md)

**Context Document Format:** See [templates/context-document.md](templates/context-document.md)

### Multi-Paper Dependency Handling

When papers reference each other:

```
Paper A (Foundation) ──────► Paper B (Extension) ──────► Paper C (Application)
    │                            │                            │
    ▼                            ▼                            ▼
A.context.md                B.context.md                C.context.md
    │                            │                            │
    └────────────────────────────┴────────────────────────────┘
                                 │
                                 ▼
                    IMPLEMENTATION_PLAN.md
                    (ordered by dependency)
```

## Phase 2: Context Synthesis

After all extraction agents complete:

1. Read all `.context.md` files
2. Build dependency graph from cross-references
3. Create implementation order (topological sort)
4. Generate `IMPLEMENTATION_PLAN.md`

**Synthesis Template:** See [templates/implementation-plan.md](templates/implementation-plan.md)

## Phase 3: Equation-First Implementation

**CRITICAL: Write test BEFORE implementation for EVERY equation.**

### Equation Verification Pattern

```python
# tests/test_equation_3_memory_update.py
"""
Paper: TITANS (arXiv:2501.00663)
Equation 3: M_{t+1} = M_t + η · ∇l(M_t; x_t)
Description: Memory update rule with gradient-based learning
"""
import torch
import pytest

def test_equation_3_shapes():
    """Verify tensor shapes match paper specification."""
    batch_size, memory_size, dim = 4, 64, 256
    M_t = torch.randn(batch_size, memory_size, dim)
    x_t = torch.randn(batch_size, dim)
    eta = 0.01
    
    # Your implementation
    from src.memory import memory_update
    M_t_plus_1 = memory_update(M_t, x_t, eta)
    
    assert M_t_plus_1.shape == M_t.shape, f"Expected {M_t.shape}, got {M_t_plus_1.shape}"

def test_equation_3_gradient_flow():
    """Verify gradients flow correctly through memory update."""
    M_t = torch.randn(4, 64, 256, requires_grad=True)
    x_t = torch.randn(4, 256)
    
    from src.memory import memory_update
    M_t_plus_1 = memory_update(M_t, x_t, eta=0.01)
    loss = M_t_plus_1.sum()
    loss.backward()
    
    assert M_t.grad is not None, "Gradients should flow to M_t"
    assert not torch.isnan(M_t.grad).any(), "Gradients should not be NaN"

def test_equation_3_numerical_stability():
    """Verify numerical stability with extreme values."""
    M_t = torch.randn(4, 64, 256) * 1000  # Large values
    x_t = torch.randn(4, 256) * 1000
    
    from src.memory import memory_update
    M_t_plus_1 = memory_update(M_t, x_t, eta=0.01)
    
    assert not torch.isnan(M_t_plus_1).any(), "Should handle large values"
    assert not torch.isinf(M_t_plus_1).any(), "Should not overflow"
```

### Implementation Pattern

```python
# src/memory.py
"""
Memory module implementing TITANS neural memory.

Paper References:
- Equation 3: memory_update()
- Equation 5: surprise_metric()
- Algorithm 1: MemoryLayer forward pass
"""
import torch
import torch.nn as nn

def memory_update(M_t: torch.Tensor, x_t: torch.Tensor, eta: float) -> torch.Tensor:
    """
    Equation 3: M_{t+1} = M_t + η · ∇l(M_t; x_t)
    
    Args:
        M_t: Current memory state [batch, memory_size, dim]
        x_t: Input token [batch, dim]
        eta: Learning rate
    
    Returns:
        M_t_plus_1: Updated memory [batch, memory_size, dim]
    """
    # Implementation here
    ...
```

**Full verification patterns:** See [references/equation-patterns.md](references/equation-patterns.md)

## Phase 4: Code Quality

Run these checks before considering implementation complete:

```bash
# 1. Format with ruff
uv run ruff format src/ tests/

# 2. Lint with ruff  
uv run ruff check src/ tests/ --fix

# 3. Type check with ty (Astral's type checker)
uv run ty check src/

# 4. Run all tests
uv run pytest tests/ -v --tb=short

# 5. Check test coverage
uv run pytest tests/ --cov=src --cov-report=term-missing
```

**Quality Script:** See [scripts/quality_check.py](scripts/quality_check.py)

## Phase 5: Documentation

Generate comprehensive documentation:

### README.md Structure

```markdown
# [Paper Name] Reproduction

> [One-line paper description]

## Quick Start

\`\`\`bash
# Clone and setup
git clone [repo]
cd [repo]
uv sync

# Run example
uv run python -m src.main --config configs/default.yaml
\`\`\`

## Paper Reference

- **Title:** [Full title]
- **Authors:** [Authors]
- **arXiv:** [Link]
- **Original Code:** [If exists]

## Implementation Status

| Component | Paper Section | Status | Tests |
|-----------|--------------|--------|-------|
| Memory Module | §3.1, Eq 3-5 | ✅ | 12/12 |
| Attention Layer | §3.2, Eq 8-10 | ✅ | 8/8 |
| Training Loop | §4.1 | ✅ | 5/5 |

## Architecture

[ASCII diagram or Mermaid]

## Usage

### Training
\`\`\`bash
uv run python -m src.train --config configs/train.yaml
\`\`\`

### Inference
\`\`\`bash
uv run python -m src.inference --checkpoint checkpoints/best.pt
\`\`\`

## Benchmarks

| Dataset | Paper Result | Our Result | Status |
|---------|-------------|------------|--------|
| WikiText-103 | 17.2 PPL | TBD | ⏳ |

## Project Structure

\`\`\`
├── src/
│   ├── __init__.py
│   ├── model.py       # Main model (§3)
│   ├── memory.py      # Memory module (§3.1)
│   └── train.py       # Training loop (§4)
├── tests/
│   ├── test_memory.py
│   └── test_model.py
├── configs/
│   └── default.yaml
├── notebooks/
│   └── exploration.ipynb
└── docs/
    └── ARCHITECTURE.md
\`\`\`
```

**Documentation Template:** See [templates/readme-template.md](templates/readme-template.md)

## Phase 6: Git & Execution Prep

### Initialize Repository

```bash
# Initialize git
git init

# Create .gitignore
cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
.venv/
*.egg-info/

# UV
.python-version

# IDE
.vscode/
.idea/

# Data & Models
data/
checkpoints/
*.pt
*.pth
wandb/

# Jupyter
.ipynb_checkpoints/
EOF

# Initial commit
git add .
git commit -m "Initial implementation: [Paper Name]

- Core model implementation (§3)
- Equation-verified modules (Eq 3-10)
- Test suite with X% coverage
- Documentation and examples

Paper: [arXiv link]"
```

### Prepare for GitHub

```bash
# Create repo (requires gh CLI authenticated)
gh repo create [repo-name] --public --source=. --remote=origin

# Or prepare for manual push
echo "Ready to push:"
echo "  git remote add origin git@github.com:USER/REPO.git"
echo "  git push -u origin main"
```

### Create Run Scripts

**CLI Script:**
```bash
#!/usr/bin/env bash
# run_training.sh
set -e
uv run python -m src.train "$@"
```

**Notebook Entry:**
```python
# notebooks/quickstart.ipynb
# Cell 1: Setup
!uv sync
from src.model import Model
from src.train import Trainer

# Cell 2: Quick test
model = Model.from_config("configs/default.yaml")
print(f"Parameters: {sum(p.numel() for p in model.parameters()):,}")
```

## Scripts Reference

This skill includes UV single-file scripts for complex operations:

| Script | Purpose | Usage |
|--------|---------|-------|
| `scripts/extract_paper.py` | Convert PDF to markdown, extract equations | `uv run scripts/extract_paper.py paper.pdf` |
| `scripts/quality_check.py` | Run ruff + ty + pytest | `uv run scripts/quality_check.py` |
| `scripts/verify_equations.py` | Run equation-specific tests | `uv run scripts/verify_equations.py` |
| `scripts/benchmark_runner.py` | Run benchmarks, compare to paper | `uv run scripts/benchmark_runner.py` |
| `scripts/generate_docs.py` | Generate README and architecture docs | `uv run scripts/generate_docs.py` |

## Tools Reference

- [tools/paper-intake.md](tools/paper-intake.md) - PDF/URL ingestion
- [tools/equation-extractor.md](tools/equation-extractor.md) - LaTeX extraction and mapping
- [tools/verification-engine.md](tools/verification-engine.md) - Test generation patterns
- [tools/benchmark-validator.md](tools/benchmark-validator.md) - Results comparison

## Templates Reference

- [templates/context-document.md](templates/context-document.md) - Extraction output format
- [templates/implementation-plan.md](templates/implementation-plan.md) - Synthesis output
- [templates/readme-template.md](templates/readme-template.md) - Project README
- [templates/test-template.md](templates/test-template.md) - Equation test structure

## Prompts Reference

- [prompts/extraction-agent.md](prompts/extraction-agent.md) - Per-paper extraction agent
- [prompts/implementation-agent.md](prompts/implementation-agent.md) - Code implementation agent
- [prompts/verification-agent.md](prompts/verification-agent.md) - Test writing agent
- [prompts/documentation-agent.md](prompts/documentation-agent.md) - Docs generation agent

## Project Structure Output

```
[paper-name]-reproduction/
├── .gitignore
├── .python-version
├── pyproject.toml
├── uv.lock
├── README.md
├── ARCHITECTURE.md
├── IMPLEMENTATION_PLAN.md
│
├── papers/                    # Original papers (gitignored if large)
│   └── [paper].context.md     # Extracted context (committed)
│
├── src/
│   ├── __init__.py
│   ├── model.py               # Main model
│   ├── layers/                # Individual layers/modules
│   │   ├── __init__.py
│   │   ├── memory.py          # Memory module
│   │   └── attention.py       # Attention variants
│   ├── train.py               # Training loop
│   ├── inference.py           # Inference utilities
│   └── utils/
│       ├── __init__.py
│       └── config.py          # Configuration handling
│
├── tests/
│   ├── __init__.py
│   ├── test_equations/        # Equation-specific tests
│   │   ├── test_eq3_memory.py
│   │   └── test_eq5_surprise.py
│   ├── test_layers/
│   │   └── test_memory.py
│   └── test_integration.py
│
├── configs/
│   ├── default.yaml
│   ├── small.yaml             # Quick testing config
│   └── paper.yaml             # Paper's exact config
│
├── notebooks/
│   ├── exploration.ipynb      # Development notebook
│   └── quickstart.ipynb       # User-facing notebook
│
├── scripts/
│   ├── train.sh
│   └── evaluate.sh
│
└── docs/
    ├── equations.md           # All equations with implementations
    └── benchmarks.md          # Benchmark results
```

## Checklist Before Completion

- [ ] All equations have corresponding tests
- [ ] All tests pass (`uv run pytest`)
- [ ] Code formatted (`uv run ruff format`)
- [ ] Types checked (`uv run ty check src/`)
- [ ] README complete with quick start
- [ ] ARCHITECTURE.md describes design
- [ ] Git initialized with meaningful commit
- [ ] Can run basic example without errors
- [ ] Paper references documented in code

## Integration with LeCoder-cgpu

After code is ready and verified locally:

```bash
# Connect to Colab GPU
lecoder-cgpu connect

# Upload project
lecoder-cgpu upload ./

# Run training
lecoder-cgpu run "cd [project] && uv sync && uv run python -m src.train"

# Download results
lecoder-cgpu download checkpoints/
```

See [tools/colab-execution.md](tools/colab-execution.md) for detailed Colab integration.
