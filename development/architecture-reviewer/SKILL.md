---
name: architecture-reviewer
description: Review code against PRISM target architecture patterns from REFACTORING_DESIGN_DOCUMENT.md. This skill should be used during refactoring to ensure new Runner and Trainer classes follow AbstractRunner/AbstractTrainer patterns.
---

# Architecture Reviewer

Review code against PRISM's target architecture patterns to ensure consistency with the refactoring design.

## Purpose

This skill validates that new and refactored code follows PRISM's architectural patterns, specifically the Template Method pattern for Runners and the Strategy pattern for Trainers.

## When to Use

Use this skill when:
- Creating new Runner classes (PRISMRunner, MoPIERunner)
- Creating new Trainer classes (ProgressiveTrainer, EpochalTrainer)
- Refactoring existing procedural code to object-oriented patterns
- Verifying Template Method pattern implementation
- Checking Strategy pattern usage
- Reviewing pull requests that modify core architecture

## Target Architecture Patterns

### Pattern 1: AbstractRunner (Template Method)

The Template Method pattern defines a skeleton workflow with customizable hooks:

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import Optional
import torch
from torch.utils.tensorboard import SummaryWriter

@dataclass
class ExperimentResult:
    """Result of an experiment run."""
    ssims: list[float]
    psnrs: list[float]
    rmses: list[float]
    final_reconstruction: torch.Tensor
    log_dir: Path
    elapsed_time: float

class AbstractRunner(ABC):
    """Abstract base class for experiment runners.

    Implements Template Method pattern: run() defines the workflow,
    subclasses implement hook methods.
    """

    def __init__(self, args):
        self.args = args
        self.config = None
        self.device = None
        self.log_dir = None
        self.writer: Optional[SummaryWriter] = None

    def run(self) -> ExperimentResult:
        """Template method - DO NOT OVERRIDE in subclasses."""
        self.setup()              # Hook 1: Environment setup
        self.load_data()          # Hook 2: Load image/pattern
        self.create_components()  # Hook 3: Create model/trainer
        result = self.run_experiment()  # Hook 4: Run training
        self.save_results(result) # Hook 5: Save outputs
        self.cleanup()            # Hook 6: Resource cleanup
        return result

    @abstractmethod
    def setup(self) -> None:
        """Hook 1: Set up device, logging, directories."""
        ...

    @abstractmethod
    def load_data(self) -> None:
        """Hook 2: Load image and generate pattern."""
        ...

    @abstractmethod
    def create_components(self) -> None:
        """Hook 3: Create model, telescope, trainer."""
        ...

    @abstractmethod
    def run_experiment(self) -> ExperimentResult:
        """Hook 4: Run training and return results."""
        ...

    @abstractmethod
    def save_results(self, result: ExperimentResult) -> None:
        """Hook 5: Save checkpoint and visualizations."""
        ...

    def cleanup(self) -> None:
        """Hook 6: Cleanup (default implementation)."""
        if self.writer:
            self.writer.close()
```

### Pattern 2: AbstractTrainer (Strategy Pattern)

The Strategy pattern allows interchangeable training algorithms:

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass
import torch
from torch import nn, Tensor

@dataclass
class TrainingResult:
    """Final training result."""
    ssims: list[float]
    psnrs: list[float]
    rmses: list[float]
    final_reconstruction: Tensor
    total_time: float
    converged: bool

class AbstractTrainer(ABC):
    """Abstract base class for training strategies."""

    def __init__(
        self,
        model: nn.Module,
        device: torch.device,
        config: 'TrainingConfig'
    ):
        self.model = model
        self.device = device
        self.config = config

    @abstractmethod
    def train(self) -> TrainingResult:
        """Main training loop - must be implemented."""
        ...

    @abstractmethod
    def train_step(self, batch_idx: int) -> dict:
        """Single training step - must be implemented."""
        ...

    def compute_metrics(self) -> tuple[float, float, float]:
        """Compute RMSE, SSIM, PSNR (can be overridden)."""
        return self.model.errors()

    def should_stop(self) -> bool:
        """Early stopping check (can be overridden)."""
        return False

    def save_checkpoint(self, path: Path) -> None:
        """Save checkpoint (can be overridden)."""
        torch.save({
            'model_state': self.model.state_dict(),
            'config': self.config,
        }, path)
```

### Pattern 3: Concrete Runner Example

```python
class PRISMRunner(AbstractRunner):
    """Runner for PRISM algorithm."""

    def setup(self) -> None:
        self.device = setup_device(self.args)
        self.config = load_config(self.args)
        self.log_dir = Path(self.args.log_dir) / self.args.name
        self.writer = SummaryWriter(self.log_dir)

    def load_data(self) -> None:
        self.image = load_image(self.args.obj_name).to(self.device)
        self.centers = generate_pattern(self.args, self.config)

    def create_components(self) -> None:
        self.telescope = Telescope(...).to(self.device)
        self.model = ProgressiveDecoder(...).to(self.device)
        self.trainer = ProgressiveTrainer(self.model, ...)

    def run_experiment(self) -> ExperimentResult:
        result = self.trainer.train()
        return ExperimentResult(
            ssims=result.ssims,
            psnrs=result.psnrs,
            rmses=result.rmses,
            final_reconstruction=result.final_reconstruction,
            log_dir=self.log_dir,
            elapsed_time=result.total_time
        )

    def save_results(self, result: ExperimentResult) -> None:
        save_checkpoint(self.model, self.log_dir / 'checkpoint.pt')
        create_visualization(result, self.log_dir)
```

## Architecture Review Checklist

### For AbstractRunner Subclasses

- [ ] **Inheritance**: Class inherits from `AbstractRunner`
- [ ] **Constructor**: Calls `super().__init__(args)` first
- [ ] **Template Method**: Does NOT override `run()`
- [ ] **Hook Implementations**:
  - [ ] `setup()`: Sets device, config, log_dir, writer
  - [ ] `load_data()`: Loads image and pattern only
  - [ ] `create_components()`: Creates model, telescope, trainer
  - [ ] `run_experiment()`: Calls trainer.train(), returns ExperimentResult
  - [ ] `save_results()`: Saves checkpoint and visualizations
- [ ] **Separation of Concerns**: Each hook does one thing
- [ ] **Type Hints**: All methods have proper annotations
- [ ] **Docstrings**: All methods documented

### For AbstractTrainer Subclasses

- [ ] **Inheritance**: Class inherits from `AbstractTrainer`
- [ ] **Constructor**: Calls `super().__init__(model, device, config)`
- [ ] **Required Methods**:
  - [ ] `train()`: Returns TrainingResult
  - [ ] `train_step()`: Single step logic
- [ ] **Metrics**: Uses SSIM, PSNR, RMSE consistently
- [ ] **Checkpointing**: Supports save_checkpoint()
- [ ] **Type Hints**: All methods properly typed

### General Code Quality

- [ ] **Naming**:
  - [ ] Runners end with "Runner" (PRISMRunner, MoPIERunner)
  - [ ] Trainers end with "Trainer" (ProgressiveTrainer, EpochalTrainer)
  - [ ] Methods use snake_case
  - [ ] Classes use PascalCase
- [ ] **No God Functions**: Methods < 50 lines
- [ ] **No Hardcoded Values**: Use config or parameters
- [ ] **Testability**: Components can be instantiated independently

## Anti-Patterns to Avoid

### Anti-Pattern 1: Overriding Template Method
```python
# BAD - Don't override run()
class MyRunner(AbstractRunner):
    def run(self) -> ExperimentResult:  # DON'T DO THIS
        # Custom implementation
        ...
```

### Anti-Pattern 2: Mixing Concerns
```python
# BAD - setup() doing too much
def setup(self) -> None:
    self.device = setup_device(self.args)
    self.image = load_image(...)  # This belongs in load_data()!
    self.model = create_model(...)  # This belongs in create_components()!
```

### Anti-Pattern 3: Trainer Doing Visualization
```python
# BAD - Trainer shouldn't handle visualization
class MyTrainer(AbstractTrainer):
    def train(self) -> TrainingResult:
        result = self._train_loop()
        self._create_plots()  # This belongs in Runner.save_results()!
        return result
```

### Anti-Pattern 4: No Abstraction
```python
# BAD - Doesn't use abstract base
class MoPIERunner:  # Should inherit from AbstractRunner!
    def run(self):
        # Duplicate implementation
        ...
```

### Anti-Pattern 5: Hardcoded Paths
```python
# BAD
def save_results(self, result):
    torch.save(model, '/tmp/checkpoint.pth')  # Use self.log_dir!
```

## Review Workflow

### Step 1: Check Inheritance
```python
# Verify proper inheritance
assert issubclass(MyRunner, AbstractRunner)
assert issubclass(MyTrainer, AbstractTrainer)
```

### Step 2: Check Hook Implementations
```python
# Verify all abstract methods are implemented
required_runner_methods = ['setup', 'load_data', 'create_components',
                           'run_experiment', 'save_results']
for method in required_runner_methods:
    assert hasattr(MyRunner, method)
    assert callable(getattr(MyRunner, method))
```

### Step 3: Check Method Signatures
```python
# Verify return types
import inspect
sig = inspect.signature(MyRunner.run_experiment)
assert sig.return_annotation == ExperimentResult
```

### Step 4: Check for Anti-Patterns
- Search for `def run(self)` in Runner subclasses (shouldn't exist)
- Check that hooks don't overlap in functionality
- Verify no visualization code in Trainers

## Example Review Comments

### Good Implementation
> ✅ Excellent! PRISMRunner correctly implements AbstractRunner pattern.
> All hooks are focused and follow single responsibility.
> Type hints and docstrings are complete.

### Needs Improvement
> ❌ Issues found in MoPIERunner:
> 1. Doesn't inherit from AbstractRunner
> 2. setup() loads data (should be in load_data())
> 3. Missing type hints on run_experiment()
>
> Recommendation: Refactor to follow AbstractRunner pattern.

## Quick Reference

### Runner Template
```
AbstractRunner.run():
  1. setup()           → Device, config, logging
  2. load_data()       → Image, pattern
  3. create_components() → Model, telescope, trainer
  4. run_experiment()  → Training loop
  5. save_results()    → Checkpoint, visualization
  6. cleanup()         → Resource cleanup
```

### Trainer Template
```
AbstractTrainer.train():
  Loop:
    1. train_step()      → Process batch
    2. compute_metrics() → RMSE, SSIM, PSNR
    3. should_stop()     → Early stopping
  Return TrainingResult
```

## Related Skills

- **type-hint-adder**: Add type hints to Runner/Trainer classes
- **unit-test-generator**: Create architecture compliance tests
- **docstring-formatter**: Document patterns in code

## Checklist Before Merge

- [ ] All checklist items verified
- [ ] No anti-patterns detected
- [ ] Follows naming conventions
- [ ] Properly typed and documented
- [ ] Consistent with existing patterns
- [ ] Tests pass
