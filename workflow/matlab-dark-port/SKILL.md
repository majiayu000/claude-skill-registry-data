---
name: matlab-dark-port
description: "Port legacy MATLAB engineering code to Python through the legal deny-list gate — extract example data, audit branded names, build regression tests, and commit to nested repo correctly."
type: procedure
version: 1.3.0
category: data
related_skills:
- dark-intelligence-workflow
- legal-sanity-scan
tags:
- matlab
- legacy-extraction
- dark-port
- ip-compliance
- engineering-calculations
- dnv
triggers:
- darkly port
- port matlab
- matlab to python
- dark port
- legacy matlab
---

# MATLAB Dark Port Workflow

## Overview

Port legacy MATLAB engineering code (copyrighted, branded) into clean Python
implementations that pass the legal deny-list scan. Extracts only methodology
and numerical constants from the published standard — never copies function
structure or variable names.

## When to Use

- User says "darkly port" or "dark port" MATLAB code
- Legacy MATLAB with copyright headers, branded tool names, named authors
- `.legal-deny-list.yaml` has entries blocking the original tool/firm/author

## Procedure

### Step 0 — Legal Audit BEFORE Writing Any Code

1. Read `.legal-deny-list.yaml` to know BLOCKED patterns.
2. Scan ALL MATLAB files with regex to catalog:
   ```python
   # Function names
   re.findall(r'function\s+.*?=?\s*(\w+)\s*\(', content)
   # Branded strings (version headers, tool names)
   re.findall(r"VersionDetail.*?'(.*?)'", content)
   # Author names
   re.findall(r'(?:Author|By|Modified|Name)\s*[:=]\s*([A-Z][a-z]+ [A-Z][a-z]+)', content)
   ```
3. Build a MATLAB→Python naming map. Present to user for approval.
4. Any name containing a deny-list hit MUST be renamed.

### Step 1 — Check Existing Python Implementation

The Python modules may ALREADY exist from a prior clean-room pass:
```bash
find */src/*/subsea/pipeline/free_span/ -name "*.py" | xargs wc -l
```
Check for `NotImplementedError` / `pass` — if real code exists, you only need
to add the missing module + tests, not rewrite everything.

### Step 2 — Extract Example Data from MATLAB

- Read the "Setup" or "default generation" function — it contains hardcoded
  example inputs (pipe dimensions, current profiles, S-N curves, safety factors).
  This is the PRIMARY source of test vectors — it writes a sample .dat file
  with all default parameters and is often the only "worked example" available.
- Read the "GetInputs" function for safety factor tables and parameter derivation.
- These numerical values become regression test vectors.
- NEVER copy variable names or function structure.
- **Expect no result files.** Legacy MATLAB typically has no saved outputs —
  only .xlsm post-processing workbooks. Build tests from inputs + standard
  equations, not captured outputs.

### Step 3 — Port Missing Modules Only

- Write new modules with completely independent names.
- Reference only the public standard (DNV-RP-F105 section numbers in docstrings).
- Use standard Python patterns (dataclasses, scipy, numpy).

### Step 3b — Resolve Cross-Module Import Dependencies

If the ported code depends on a module only available in the nested repo
(e.g., `digitalmodel.structural.fatigue.sn_curves`), build a **self-contained
fallback module** with `_` prefix (private) inside the same package:

```python
# _bilinear_sn.py — self-contained fallback
_DNV_SN_TABLE = {"F": {"air": {"A1": 1.73e11, "m1": 3.0, ...}, ...}}

def get_sn_curve(curve_class, environment="air"):
    """Built-in DNV-RP-C203 Table 2-1 lookup."""
    ...
```

Then in the consumer module, use try/except fallback:
```python
def _load_sn_curve(self):
    try:
        from digitalmodel.structural.fatigue.sn_curves import get_dnv_curve
        return get_dnv_curve(self._inp.sn_curve_class)
    except (ImportError, ModuleNotFoundError):
        pass
    from ._bilinear_sn import get_sn_curve
    return get_sn_curve(curve_class=..., environment=...)
```

This pattern:
- Works in both workspace-hub overlay AND digitalmodel venv
- Uses the richer upstream module when available
- Keeps the package self-contained and testable
- Eliminates ALL skip markers from tests

### Step 4 — Build Regression Tests

- Create a pytest fixture using the extracted numerical values.
- Guard tests that depend on uninstalled submodules:
  ```python
  try:
      from digitalmodel.structural.fatigue.sn_curves import get_dnv_curve
      _HAS_STRUCTURAL = True
  except ImportError:
      _HAS_STRUCTURAL = False

  @pytest.mark.skipif(not _HAS_STRUCTURAL, reason="...")
  def test_fatigue_life_positive(self): ...
  ```
- Verify safety factor tables match BOTH the standard AND the MATLAB defaults.
- Try importing the module first — legacy code may have syntax errors.

### Step 5 — Legal Scan + Commit

1. `bash scripts/legal/legal-sanity-scan.sh --diff-only` → must PASS
2. Double-check: `grep -inE 'PATTERN1|PATTERN2' new_files` → must be empty
3. Commit tests in workspace-hub, implementation in digitalmodel (nested repo).

## Pitfalls

### 1. Dual src/ paths (overlay vs nested repo)
workspace-hub has BOTH `src/digitalmodel/...` (editable install overlay,
gitignored) AND `digitalmodel/src/digitalmodel/...` (real nested git repo).
- New modules must be copied to BOTH paths for tests to find them.
- `git add` in workspace-hub won't pick up `src/digitalmodel/` (gitignored).
- Implementation commits go to `cd digitalmodel && git add && git commit`.
- Test commits go to workspace-hub root.

### 2. Zero-exceedance probability in Weibull fitting
MATLAB's `round(1e8*(1-cumsum(occ)))/1e8` produces 0.0 for the last entry
when occurrence probabilities sum to 1.0. Must filter `P <= 0` before
calling `log()` — otherwise `math domain error`.

### 3. Cross-module imports not available
`SpanFatigueDamage` depends on `digitalmodel.structural.fatigue.sn_curves`
which may not be available in the workspace-hub overlay. **Preferred fix:**
build a self-contained fallback module (Step 3b above) so tests never need
skip markers. The `_HAS_STRUCTURAL` skip pattern is a temporary workaround
only — replace it with the fallback module in the same session if possible.

### 3b. Environment-specific S-N curve behavior
DNV-RP-C203 seawater_cp curves have **no fatigue limit** (CAFL=0) per
Sec 2.4.4. Tests asserting "zero damage below CAFL" must use IN_AIR
environment, not SEAWATER_CP. The old single-slope code incorrectly
applied the in-air CAFL to all environments.

### 4. Pre-existing syntax errors
Always try importing the target module BEFORE writing tests. Prior commits
may have introduced syntax errors (e.g., double assignment on one line).
Fix these first and include in the commit.

### 5. MATLAB safety factor naming swap
The MATLAB code names onset safety factors OPPOSITE to DNV convention:
- MATLAB: `onsetSafetyFactor_CF = 1.1`, `onsetSafetyFactor_IL = 1.3`
- Python (DNV convention): `gamma_on_IL = 1.1`, `gamma_on_CF = 1.3`
Document this mapping explicitly in test docstrings.

### 6. S-N curve transfer stress calculation
For bilinear S-N curves, the transfer stress is:
`S_transfer = (A2 / N_transfer)^(1/k2)`
Don't assume the result falls in a "typical" range — compute it from
the actual parameters and assert around the computed value.

### 7. Git push for nested repos
`git push` in workspace-hub won't push the nested `digitalmodel/` repo.
Must explicitly: `cd digitalmodel && git push origin main`.

### 8. numpy 2.x compatibility
`np.trapz` was removed in numpy 2.x → use `np.trapezoid`. Compat shim:
```python
_trapz = getattr(np, "trapezoid", None) or np.trapz
```
workspace-hub venv has numpy 2.x. Apply in both source and tests.

### 9. Post-implementation issue hygiene
After completing the port, the user expects:
- Status comment on the parent issue with what was done + what's blocked
- New child issue for any dependency gap (e.g., missing bilinear S-N support)
- Bidirectional links between parent, child, and related issues
- Follow-on issues for enhancement features not in scope (each with clear AC)
- Close parent when all acceptance criteria met, even if follow-ons remain
Use `gh issue create` + `gh issue comment` in the same flow.

### 10. VIV piecewise response: max current ≠ max damage
VIV amplitude models (F105 Fig 4-2, 4-5) are piecewise — the response peaks
at an intermediate reduced velocity (Ur ≈ 7–8 for CF) and drops to zero past
Vr_end (≈16). So the highest current can give LESS damage than a mid-range
current if the reduced velocity overshoots the peak. Never assume "max current
= worst case" in tests — instead find the actual worst bin:
```python
max_single = max(assess(speed).damage_per_year for speed, _ in bins)
assert weighted_damage < max_single  # correct
# NOT: assert weighted_damage < assess(max_speed).damage_per_year  # WRONG
```

### 11. Multi-current probability-weighted damage pattern
The MATLAB approach loops over current bins and sums `D_i × prob_i`. Implement
as a facade method that replaces current_velocity_ms via dataclass `replace()`:
```python
def assess_multi_current(self, current_bins):
    weighted_damage = sum(
        self._assess_at(speed).damage_per_year * prob
        for speed, prob in current_bins
    )
```
Return worst-case screening details (frequencies, amplitudes) from the bin
that produced the highest unweighted damage, but use weighted damage for life.

### 12. JONSWAP spectral velocity integration
When computing wave-induced velocity from sea-state (Hs, Tp, depth):
- JONSWAP gamma auto-selection: phi = Tp/sqrt(Hs), gamma = 5/exp/1
- Dispersion: Newton-Raphson with deep-water initial guess k₀ = ω²/g
- Velocity transfer: G(ω) = ω·cosh(k·z)/sinh(k·h), clip kh < 50
- Spectral moments: M0, M2 via trapezoidal integration
- Uw = 2√M0, Tu = 2π√(M0/M2)
- Hs recovery from JONSWAP integration is ~15% off for high gamma —
  this is a known C_gamma normalisation artifact, not a bug.

## Verification

```bash
# Tests pass
uv run python -m pytest tests/subsea/pipeline/test_*.py -v

# Legal scan clean
bash scripts/legal/legal-sanity-scan.sh --diff-only

# No deny-list patterns in new files
grep -inE '2H.?Offshore|2HSPANVIV|TwoH|AUTHOR_NAME' new_files
```
