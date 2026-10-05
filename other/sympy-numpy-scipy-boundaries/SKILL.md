---
name: sympy-numpy-scipy-boundaries
description: >-
  Use when symbolic mathematics must cross into NumPy vector evaluation or SciPy
  numerical algorithms: lambdify contracts, domains, dtypes, parameters, residuals,
  tolerances, and symbolic-versus-numeric verification. Do not use for work confined
  entirely to one of those libraries.
---

# SymPy, NumPy, and SciPy boundaries

Keep exact structure symbolic until a numerical consumer is chosen. Then compile an
explicit numeric contract and verify the numerical result against the original
mathematics.

Inspect the installed version of SymPy, NumPy, and SciPy and exact signatures before
depending on translation mappings or solver options.

## Boundary workflow

1. State symbols, assumptions, parameter order, units, real/complex domain, and valid
   input region in SymPy.
2. Simplify or differentiate symbolically only when the transformation preserves the
   intended domain. Record excluded singularities introduced or removed by algebra.
3. Choose a numeric backend explicitly with `lambdify`; use `modules="numpy"` for
   vector evaluation and a SciPy-capable mapping only when required functions are not
   provided by NumPy.
4. Define the callable's input shapes, broadcasting contract, output shape, dtype, and
   behavior at singular or invalid points.
5. Feed the callable to SciPy only after adapting its signature to the solver's
   contract. Do not rely on implicit symbol order.
6. Validate convergence using residuals and constraints. When a solution can be
   local or initialization-sensitive, also use multiple starts or a justified
   bracket—not the solver success flag alone.
7. Cross-check representative results against higher-precision SymPy/mpmath or an
   independent formulation.

Read [translation.md](references/translation.md),
[solver-contracts.md](references/solver-contracts.md), and
[verification.md](references/verification.md).

## Canonical scalar solve

```python
import numpy as np
import sympy as sp
from scipy import optimize

x, a = sp.symbols("x a", real=True)
expr = sp.exp(-a * x) - x
numeric = sp.lambdify((x, a), expr, modules="numpy")

parameter = 2.0
root = optimize.brentq(lambda value: float(numeric(value, parameter)), 0.0, 1.0)
residual = abs(float(numeric(root, parameter)))
if not np.isfinite(root) or residual > 1e-10:
    raise RuntimeError(f"unverified root: residual={residual:g}")
```

Use a bracketed solver when a sign-changing interval is available. Use a local solver
only when an initial estimate and basin assumptions are defensible.

## Decision rules

- Many machine-precision evaluations: `lambdify` once, then use NumPy arrays.
- One exact or high-precision evaluation: keep SymPy/mpmath rather than forcing NumPy.
- Symbolic Jacobian available and tractable: lambdify it and pass it to the SciPy
  algorithm; verify its shape and values with finite differences at sample points.
- Piecewise or branch-sensitive expression: test every branch and boundary; generated
  NumPy code may evaluate masked branches and emit warnings.
- Untrusted expression: do not pass it to `sympify`/`lambdify` as a security boundary;
  parse against an explicit safe grammar outside this workflow.

## Completion checks

- Symbol and parameter ordering is explicit and tested.
- Shape, dtype, domain, and nonfinite behavior are asserted.
- Solver termination, residual, and constraints all pass.
- At least one boundary/singularity case and one independent numerical check pass.
- No result is called exact after it has crossed into floating-point computation.
