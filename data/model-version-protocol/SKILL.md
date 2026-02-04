---
name: model-version-protocol
description: "Model-trader version compatibility protocol: Embed version metadata in checkpoints, validate at load time. Trigger when: (1) training and live trading versions diverge, (2) models fail to load, (3) action interpretation issues."
author: Claude Code
date: 2024-12-29
---

# Model Version Protocol (v2.7.0)

## Experiment Overview
| Item | Details |
|------|---------|
| **Date** | 2024-12-29 |
| **Goal** | Ensure live trader compatibility with trained models across version changes |
| **Environment** | alpaca_trading/model_version.py, ppo_trainer_native.py, live_trader.py |
| **Status** | Success |

## Context

**Problem**: Training code changes frequently, but live trading tests can't keep up. When training changes:
- obs_dim changes (5600 → 5900)
- n_actions changes (3 → 7)
- Action interpretation changes (direction-only → direction+sizing)

Old models become incompatible with new trader code, causing silent failures.

**Solution**: Model Version Protocol - embed version metadata in checkpoints, validate at load time.

## Verified Workflow

### 1. Version Constants (model_version.py)

```python
# Current versions - update when training/trader changes
CURRENT_MODEL_VERSION = "2.7.0"
CURRENT_TRADER_VERSION = "2.7.0"

# Compatibility matrix: model_version -> min_trader_version
MODEL_TRADER_COMPATIBILITY = {
    "2.7.0": "2.7.0",  # 7-action, 59 features
    "2.6.0": "2.4.0",  # 3-action, 56 features
    "2.5.0": "2.4.0",  # 3-action, 56 features
    "2.4.0": "2.4.0",  # 3-action, 56 features (account-aware)
    "2.3.0": "2.3.0",  # 3-action, 53 features
}
```

### 2. Model Specification (model_version.py)

```python
@dataclass
class ModelSpec:
    """Specification for a model version."""
    version: str
    n_features: int
    n_actions: int
    obs_dim: int  # n_features * window (typically 100)
    action_meanings: Dict[int, str]
    breaking_changes: str = ""

MODEL_SPECS = {
    "2.7.0": ModelSpec(
        version="2.7.0",
        n_features=59,
        n_actions=7,
        obs_dim=5900,
        action_meanings={
            0: "HOLD",
            1: "BUY_25%", 2: "BUY_50%", 3: "BUY_75%",
            4: "SELL_25%", 5: "SELL_50%", 6: "SELL_75%",
        },
        breaking_changes="7-action space, 59 features (position sizing)",
    ),
    # ... older versions
}
```

### 3. Checkpoint Metadata (ppo_trainer_native.py)

```python
def save(self, path: str):
    """Save model checkpoint with version metadata."""
    from alpaca_trading.model_version import get_checkpoint_metadata

    version_metadata = get_checkpoint_metadata()

    torch.save({
        "policy_state_dict": policy_to_save.state_dict(),
        "optimizer_state_dict": self.optimizer.state_dict(),
        "global_step": self.global_step,
        "config": self.config,
        # Version metadata (v2.7.0)
        **version_metadata,  # model_version, n_features, n_actions, obs_dim, action_meanings
    }, path)
```

### 4. Version Detection (model_version.py)

```python
def detect_version_from_checkpoint(checkpoint: dict) -> Tuple[str, ModelSpec]:
    """Detect model version from checkpoint data."""
    # First check for explicit version
    if 'model_version' in checkpoint:
        version = checkpoint['model_version']
        if version in MODEL_SPECS:
            return version, MODEL_SPECS[version]

    # Infer from structure (for legacy models)
    if obs_dim == 5900 and n_actions == 7:
        return "2.7.0", MODEL_SPECS["2.7.0"]
    elif obs_dim == 5600 and n_actions == 3:
        return "2.6.0", MODEL_SPECS["2.6.0"]
    # ...
```

### 5. Compatibility Validation (live_trader.py)

```python
class NativeModelWrapper:
    def __init__(self, checkpoint_path: str, strict_version: bool = False):
        from alpaca_trading.model_version import assert_compatibility

        checkpoint = torch.load(checkpoint_path, ...)

        # Validate version compatibility (v2.7.0)
        self.model_spec = assert_compatibility(checkpoint, strict=strict_version)
        self.model_version = checkpoint.get('model_version', 'unknown')
```

### 6. Version-Specific Action Interpretation (model_version.py)

```python
def interpret_action(action: int, spec: ModelSpec) -> Tuple[int, float, str]:
    """Interpret an action using the model's specification."""
    action_name = spec.action_meanings.get(action, f"ACTION_{action}")

    if spec.n_actions == 7:
        # v2.7.0 position sizing
        if action == 0:
            return 0, 0.0, action_name  # HOLD
        elif action <= 3:
            size_mult = [0.25, 0.50, 0.75][action - 1]
            return 1, size_mult, action_name  # BUY
        else:
            size_mult = [0.25, 0.50, 0.75][action - 4]
            return -1, size_mult, action_name  # SELL
    else:
        # Legacy 3-action (default to 50% sizing)
        if action == 1:
            return 1, 0.50, action_name  # BUY
        elif action == 2:
            return -1, 0.50, action_name  # SELL
        return 0, 0.0, action_name  # HOLD
```

## CLI Usage

```bash
# Warn on version mismatch (default - allows trading with warnings)
python scripts/live_trader.py --paper 1

# Strict mode: fail on mismatch (for testing)
python scripts/live_trader.py --paper 1 --strict-version 1
```

## Version Update Workflow

When training changes require version bump:

1. **Update model_version.py**:
   - Increment `CURRENT_MODEL_VERSION`
   - Add new entry to `MODEL_SPECS`
   - Update `MODEL_TRADER_COMPATIBILITY`

2. **Update CURRENT_TRADER_VERSION** if trader code changes

3. **Retrain models** - new models will have new version

4. **Test compatibility**:
   ```bash
   # Test with strict mode
   python scripts/live_trader.py --paper 1 --strict-version 1
   ```

## Failed Attempts

| Attempt | Why it Failed | Lesson Learned |
|---------|---------------|----------------|
| Infer version from obs_dim only | v2.4-v2.6 all have same obs_dim | Need explicit version in checkpoint |
| Store version in filename | Easy to mismatch | Embed in checkpoint for guaranteed accuracy |
| No compatibility matrix | Hard to know which trader works with which model | Explicit compatibility table needed |
| Always strict mode | Breaks legitimate testing with old models | Warn by default, strict for CI/CD |

## Final Parameters

```yaml
# model_version.py
CURRENT_MODEL_VERSION: "2.7.0"
CURRENT_TRADER_VERSION: "2.7.0"

# Compatibility matrix
v2.7.0: requires trader v2.7.0+
v2.4-v2.6: requires trader v2.4.0+
v2.3.0: requires trader v2.3.0+

# Checkpoint metadata
model_version: str
n_features: int
n_actions: int
obs_dim: int
action_meanings: dict
min_trader_version: str
```

## Key Insights

- **Explicit > Implicit**: Storing version in checkpoint is more reliable than inferring
- **Backward Compatibility**: Legacy models without version field can still be detected
- **Soft Fail Default**: Warn rather than fail allows testing with mixed versions
- **Strict for CI/CD**: Use `--strict-version 1` in automated testing
- **Version-Specific Interpretation**: Action meanings differ by version; use spec

## References
- `alpaca_trading/model_version.py`: Full version protocol implementation
- `alpaca_trading/gpu/ppo_trainer_native.py`: Line 1293 (save with metadata)
- `scripts/live_trader.py`: Line 412 (NativeModelWrapper with validation)
