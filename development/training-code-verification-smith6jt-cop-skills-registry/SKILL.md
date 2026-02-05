---
name: training-code-verification
description: "Checklist for editing training code. Trigger when: (1) modifying training notebook, (2) changing GPUEnvConfig, (3) changing reward functions, (4) ANY training-related code changes."
author: Claude Code
date: 2024-12-28
---

# Training Code Verification Checklist

## MANDATORY Before Any Training Code Change

**DO NOT make assumptions. VERIFY everything.**

### 1. File Paths - CHECK ACTUAL FILES

```bash
# List actual files in the repo
ls -la *.txt                    # API key files
ls -la notebooks/               # Notebook files
ls -la alpaca_trading/gpu/      # Training modules
```

**Common mistakes:**
- Assuming `API_key.txt` exists (actual: `API_key_500Paper.txt`, `API_key_100kPaper.txt`)
- Assuming Google Drive paths in Colab (actual: `/content/Alpaca_trading/` after unzip)
- Assuming relative paths work (use absolute paths)

### 2. Configuration Values - READ BEFORE CHANGING

```python
# ALWAYS read current values first
from alpaca_trading.gpu.vectorized_env import GPUEnvConfig
config = GPUEnvConfig()

# Print ALL values before changing anything
print(f"direction_weight: {config.direction_weight}")
print(f"magnitude_weight: {config.magnitude_weight}")
print(f"pnl_weight: {config.pnl_weight}")
print(f"reward_scale: {config.reward_scale}")
# ... etc
```

**Never assume a value. Read it.**

### 3. Version Strings - VERIFY CONSISTENCY

Check ALL places where version is mentioned:
```bash
grep -r "v2\." notebooks/training.ipynb | head -20
```

All version strings must match. Don't leave old versions.

### 4. Notebook Cells - CHECK CELL NUMBERS

Notebook cells can shift. Don't assume "cell 15" is always the same cell.

```python
# Find cell by content, not number
import json
nb = json.load(open('notebooks/training.ipynb'))
for i, cell in enumerate(nb['cells']):
    source = ''.join(cell.get('source', []))
    if 'API_KEYS_FILE' in source:
        print(f"Cell {i}: API_KEYS_FILE config")
```

### 5. Weight Sums - MUST EQUAL 1.0

```python
weight_sum = (
    config.direction_weight +
    config.magnitude_weight +
    config.pnl_weight +
    config.stop_tp_weight +
    config.exploration_weight +
    config.slippage_weight +
    config.drawdown_penalty_weight
)
assert abs(weight_sum - 1.0) < 0.001, f"Weight sum is {weight_sum}, must be 1.0"
```

### 6. Tests - RUN BEFORE COMMITTING

```bash
# Run relevant tests
python -m pytest tests/test_ppo_trainer_native.py -v
python -m pytest tests/test_gpu_training.py -v
python -m pytest tests/test_data_fetcher.py -v
```

### 7. Colab Workflow - UNDERSTAND THE ENVIRONMENT

| Location | Windows Local | Colab After Unzip |
|----------|---------------|-------------------|
| Repo root | `C:\users\smith\Alpaca_trading\` | `/content/Alpaca_trading/` |
| API keys | `API_key_500Paper.txt` | `/content/Alpaca_trading/API_key_500Paper.txt` |
| Notebooks | `notebooks\training.ipynb` | `/content/Alpaca_trading/notebooks/training.ipynb` |
| Drive | N/A | `/content/drive/MyDrive/` (separate from repo) |

## Failed Attempts Log

| Date | Mistake | Impact | Lesson |
|------|---------|--------|--------|
| 2024-12-28 | Assumed `API_key.txt` exists | yfinance fallback used | Check actual filenames |
| 2024-12-28 | Suggested `/content/drive/MyDrive/` path | File not found | Unzip goes to `/content/`, not Drive |
| 2024-12-28 | Silent exception in key loading | No error shown | Add logging, don't swallow exceptions |

## Before Committing Checklist

- [ ] Read current values before changing
- [ ] Verify file paths exist
- [ ] Check all version strings match
- [ ] Verify weight sums equal 1.0
- [ ] Run relevant tests
- [ ] Test in actual environment (Colab if that's target)
- [ ] Check logs show expected behavior

## Key Principle

**Don't assume. Verify.**

Every assumption is a potential bug. Read the actual state. Check the actual files. Run the actual tests.
