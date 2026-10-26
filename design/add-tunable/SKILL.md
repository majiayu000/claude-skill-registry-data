---
name: add-tunable
description: Make a hardcoded behaviour constant user-editable through Settings → Expert Tunables. Use when a magic number should be configurable, when the user says "that should be a setting" or "make that configurable", or when tempted to edit a constant directly.
---

# Adding an Expert Tunable

Full rationale in `docs/system/rules/60-adding-a-tunable.md`. This is the procedure.

## First: should it be exposed at all?

Expose it when a **trader** would want to move it. Not when a **developer**
notices a magic number.

Leave hardcoded: protocol values, display constants, contract size, broker
timezone offsets, and engine calibration (ADX/ATR band edges, lookbacks, ML
retrain cadence). Their interactions are only verified by the suite; exposing
them makes the safe envelope meaningless.

## The rule that cannot be broken

> **The default must be byte-identical to the constant it replaces.**

Nothing trades differently until a human moves a dial. A release that silently
retunes the strategy is worse than the hardcoded value was.

## Steps

**1. Add the spec** — `backend/src/services/risk/expert_params.py`:

```python
ExpertParam(
    key="max_signal_age_s", label="Maximum signal age", default=240,
    min=30, max=3600, unit="s", domain="Signal handling", integer=True,
    desc="Signals older than this at processing time are recorded as "
         "historical and never executed. Raised carelessly, this is how a "
         "backfilled signal fills minutes late at a worse price.",
),
```

- `default` = the exact current constant.
- `desc` explains **the effect and the risk**, not the name. It is what
  someone reads before changing something that can cost money.
- `min`/`max` must make every value in range survivable — the clamp is a
  safety control, not input tidying. A 0 in an R:R floor opens trades the
  system currently refuses.
- `integer=True` for counts and cycles.

**2. Replace the constant with an accessor.** Never call
`expert_params.get()` at module import — the value would freeze at startup.

```python
def max_signal_age_secs() -> int:
    """Was a 4-minute constant; now Settings > Expert Tunables."""
    return expert_params.get("max_signal_age_s")
```

Update the call sites to use the accessor.

**3. Add the default to `EXPECTED_DEFAULTS`** in
`tests/core/test_expert_params.py`.

**4. Add both wiring tests** in `tests/core/test_expert_params_wiring.py`:

```python
def test_the_default_signal_age_cutoff_is_still_240s():
    assert scan_staleness.max_signal_age_secs() == 240

def test_the_signal_age_cutoff_follows_the_catalogue():
    ep.set_params({"max_signal_age_s": 600})
    assert scan_staleness.max_signal_age_secs() == 600
```

Both. The first alone lets you ship a control wired to nothing; the second
alone lets the default drift. Together they pin the value *and* the
connection.

**5. The UI needs no work.** `frontend/pages/expert_tunables.py` renders the
catalogue generically. That is the entire point of the design.

**6. Verify.**

```bash
pytest tests/core/test_expert_params.py tests/core/test_expert_params_wiring.py -q
python -m tools.checks all
```

## If the parameter gates order placement

Say so in the report. These do: the R:R floors, the directional cap, the
signal-age cutoff, the broker-close miss threshold. They should get a pass in
the next demo-account session, and `docs/system/rules/20-trading-safety.md` lists them.
