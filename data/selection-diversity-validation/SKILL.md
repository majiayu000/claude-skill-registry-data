---
name: selection-diversity-validation
description: "FAIL LOUDLY pattern for selection constraints. Trigger when: (1) correlated stocks selected together, (2) min_crypto_positions ignored, (3) constraints violated silently."
author: Claude Code
date: 2026-01-01
---

# Selection Diversity Validation - Research Notes

## Experiment Overview
| Item | Details |
|------|---------|
| **Date** | 2026-01-01 |
| **Goal** | Ensure selection constraints (max_correlation, min_crypto_positions) are ENFORCED, not silently ignored |
| **Environment** | alpaca_trading/selection/universe.py, tests/test_selection_diversity.py |
| **Status** | Success |

## Context

User reported MSFT and GOOGL both appearing in portfolio despite `max_correlation=0.60` setting. Additionally, crypto was not being selected despite `min_crypto_positions=1`.

**Root Cause**: Selection had two silent failure modes:
1. Notebook re-sorted by trainability AFTER diversity optimization, defeating correlation filtering
2. `min_crypto_positions` searched only top-ranked symbols instead of all symbols passing hard filters

The fundamental problem: **constraints were checked but not enforced** - failures were silent.

## The Pattern: FAIL LOUDLY

### Key Principle
> If a constraint is supposed to be enforced, it MUST raise an error when violated.
> Silent failures lead to production bugs that waste time and money.

### Implementation

```python
def validate_selection_constraints(
    symbols: List[str],
    config: SelectionConfig,
    result: 'UniverseSelectionResult',
) -> None:
    """
    Validate that selection result meets ALL constraints.

    This function FAILS LOUDLY if any constraint is violated.
    It should be called at the END of selection to catch bugs.

    Raises:
        ValueError: If any constraint is violated (NOT silent!)
    """
    errors = []

    # 1. Check crypto count
    crypto_count = sum(1 for s in symbols if s.endswith('USD') or '/' in s)
    if crypto_count < config.min_crypto_positions:
        errors.append(
            f"CRYPTO VIOLATION: Required min_crypto_positions={config.min_crypto_positions}, "
            f"but portfolio has {crypto_count} crypto symbols"
        )

    # 2. Check correlation (if matrix available)
    if result.correlation_matrix is not None:
        for i, sym1 in enumerate(symbols):
            for sym2 in symbols[i+1:]:
                try:
                    corr = abs(result.correlation_matrix.get_correlation(sym1, sym2))
                    if corr >= config.max_correlation:
                        errors.append(
                            f"CORRELATION VIOLATION: {sym1}/{sym2} correlation={corr:.2f} "
                            f">= max_correlation={config.max_correlation}"
                        )
                except (KeyError, IndexError):
                    pass  # Symbol not in matrix

    # 3. FAIL LOUDLY if any errors
    if errors:
        error_msg = (
            f"\n{'='*70}\n"
            f"SELECTION CONSTRAINT VIOLATION - THIS IS A BUG!\n"
            f"{'='*70}\n"
            f"Portfolio: {symbols}\n"
            f"\nViolations:\n" +
            "\n".join(f"  - {e}" for e in errors) +
            f"\n\nThe selection system is NOT enforcing constraints correctly.\n"
            f"{'='*70}"
        )
        logger.error(error_msg)
        raise ValueError(error_msg)

    # Log success
    logger.info(
        f"Selection validation PASSED: {len(symbols)} symbols, "
        f"{crypto_count} crypto, max_correlation={config.max_correlation}"
    )
```

### Integration Point

Call validation at the END of `select_compatible_universe()`:

```python
def select_compatible_universe(...) -> Tuple[List[str], UniverseSelectionResult]:
    # ... selection logic ...

    top_symbols = result.get_top_symbols(n=target_size)

    # VALIDATE CONSTRAINTS - FAIL LOUDLY IF VIOLATED
    if top_symbols:
        validate_selection_constraints(top_symbols, config, result)

    return top_symbols, result
```

## Failed Attempts (Critical)

| Attempt | Why it Failed | Lesson Learned |
|---------|---------------|----------------|
| Log warning on constraint violation | Warnings are ignored in production | Use `raise ValueError` not `logger.warning` |
| Notebook re-sorts after selection | Trainability sort defeats diversity optimization | Use `selected_symbols` directly, don't re-sort |
| Search ranked_symbols for crypto | Crypto may not rank high by trainability | Search ALL symbols that passed hard filters |
| MAX_EQUITIES = 200 limit | Arbitrary limit missed good candidates | Default to None (scan all ~11k) |
| Silent constraint checks | Failures go unnoticed until production | ALWAYS fail loudly on violations |

## Test Suite for Constraints

```python
# tests/test_selection_diversity.py

class TestMaxCorrelationEnforcement:
    """Tests that max_correlation constraint is ACTUALLY enforced."""

    def test_highly_correlated_pairs_excluded(self):
        """CRITICAL: If MSFT and GOOGL are both selected, this is a BUG."""
        # Create highly correlated returns
        np.random.seed(42)
        base = np.random.randn(500)
        returns = {
            'MSFT': pd.Series(base + np.random.randn(500) * 0.1),
            'GOOGL': pd.Series(base + np.random.randn(500) * 0.1),  # Correlated
            'JPM': pd.Series(np.random.randn(500)),  # Independent
        }

        # ... run selection with max_correlation=0.60 ...

        # CRITICAL ASSERTION
        both_selected = 'MSFT' in selected and 'GOOGL' in selected
        assert not both_selected, (
            f"DIVERSITY BUG: Both MSFT and GOOGL selected despite high correlation\n"
            f"Selected: {selected}\n"
            f"This means max_correlation is NOT being enforced!"
        )

class TestMinCryptoPositionsEnforcement:
    """Tests that min_crypto_positions is ACTUALLY enforced."""

    def test_crypto_guaranteed(self):
        """If min_crypto_positions=1 and no crypto, this is a BUG."""
        config = SelectionConfig(min_crypto_positions=1)
        # ... run selection ...
        crypto_count = sum(1 for s in selected if s.endswith('USD'))
        assert crypto_count >= 1, "min_crypto_positions=1 but no crypto selected!"
```

## Removing Arbitrary Limits

### Problem
```python
MAX_EQUITIES = 200  # Why 200? Arbitrary!
MAX_CRYPTO = 50     # Why 50? Arbitrary!
```

### Solution
```python
# pipeline.py
def list_equities_by_market_cap(max_symbols: Optional[int] = None) -> List[str]:
    """Return equity universe. None = no limit (all ~11k)."""
    if max_symbols is not None:
        return api_symbols[:max_symbols]
    return api_symbols  # All symbols

# notebook
MAX_EQUITIES = None  # Scan all ~11k equities
MAX_CRYPTO = None    # Scan all crypto
```

**Why remove limits?**
- Alpaca has ~11k equities - why only scan 200?
- Statistical selection will filter down to best candidates anyway
- Artificial limits may exclude good opportunities

## Key Insights

### 1. Silent Failures Are Bugs
If a config parameter exists (like `max_correlation`), the system MUST enforce it. Silent violation of constraints is a production bug waiting to happen.

### 2. Validate at the END, Not During
Don't scatter constraint checks throughout the code. Add a single validation function that runs AFTER selection completes and raises on ANY violation.

### 3. Test Constraint Enforcement, Not Just Logic
Don't just test that the function runs. Test that violations actually get caught:
```python
# BAD: Only tests that it runs
assert len(selected) > 0

# GOOD: Tests that constraint is enforced
assert not (both_msft_and_googl_selected), "Correlation constraint violated!"
```

### 4. Don't Override Selection Results
If the selection system returns a diversity-optimized portfolio, USE IT. Don't re-sort or filter afterwards - that defeats the optimization.

## Files Modified

```
alpaca_trading/selection/universe.py:
  - Added validate_selection_constraints() function
  - Called at end of select_compatible_universe()

alpaca_trading/data/pipeline.py:
  - Changed max_symbols default from 50 to None
  - list_equities_by_market_cap() scans all by default
  - list_crypto_symbols() scans all by default

notebooks/training.ipynb:
  - MAX_EQUITIES = None (was 200)
  - MAX_CRYPTO = None (was 50)
  - Use selected_symbols directly (no re-sorting)

tests/test_selection_diversity.py: (NEW)
  - 7 tests for constraint enforcement
```

## References
- `alpaca_trading/selection/universe.py`: validate_selection_constraints()
- `tests/test_selection_diversity.py`: Constraint enforcement tests
- `.skills/plugins/trading/symbol-selection-statistical/`: Statistical selection guide
- `.skills/plugins/trading/drawdown-guardrails-pattern/`: Similar "fail loudly" pattern
