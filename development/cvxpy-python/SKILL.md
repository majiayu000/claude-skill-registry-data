---
name: cvxpy-python
description: Use for writing, reviewing, debugging, testing, or optimizing Python CVXPY optimization models. Trigger on Variable, Parameter, Expression, Constraint, Objective, Problem, DCP, DPP, DGP, DQCP, solver selection/status, dual values, mixed-integer, cone, or repeated parametric solves. Do not use for scipy.optimize-only, PyMC inference, symbolic algebra without optimization, or hand-written solver implementations.
argument-hint: "[CVXPY model, mathematics, solver status, or error]"
---

# CVXPY Python

Translate an optimization problem into CVXPY without changing its mathematics.
Make dimensions, domains, curvature, solver capability, status handling, and
numerical validation explicit.

## Core objects

| Object | Meaning | Rule |
|---|---|---|
| `Variable` | Unknown decision value, optionally with structural attributes. | Domain and shape belong here or in explicit constraints. |
| `Parameter` | Symbolic constant whose `.value` changes between solves. | Use for repeated instances; it is never optimized. |
| `Expression` | Symbolic computation with shape, sign, and curvature. | Use CVXPY atoms/operators, not NumPy evaluation on variables. |
| `Constraint` | Symbolic equality, inequality, or cone relation. | Store explicit constraints when dual values matter. |
| `Objective` | `Minimize(convex)` or `Maximize(concave)` under DCP. | Direction is part of the model. |
| `Problem` | Immutable objective plus constraint list. | `solve()` canonicalizes, invokes a solver, and populates status/values. |

Model construction does not solve. `solve()` returns an objective value and
updates `problem.status`, `problem.value`, variable values, constraint duals,
and solver statistics when available. Problems are immutable; use Parameters
for data changes or construct a new Problem for mathematical changes. Read
[the symbolic and curvature model](references/object-model.md).

## Ordered workflow

1. Write the mathematical sets, indices, units, decision variables, objective,
   constraints, and allowed approximation before code.
2. Determine shapes and domains; distinguish scalar `()`, vector `(n,)`, and
   column `(n, 1)` deliberately.
3. Build symbolic expressions using CVXPY atoms and `@` for matrix products.
4. Check `problem.is_dcp()` or the intended ruleset before solver selection. Use
   `is_dcp(dpp=True)` for a repeated DCP parameterization.
5. Select a solver from the problem class and locally installed capabilities;
   pass only supported options.
6. Solve, branch on status, and reject missing/nonfinite values before use.
7. Independently validate primal feasibility, integrality, objective, and—when
   needed—duality/KKT residuals at tolerances justified by scale.

## Decision rules

- Use a `Parameter` when coefficients or bounds change but the optimization
  structure remains. Require DPP for claimed recompilation speedups.
- Use variable attributes (`nonneg`, `boolean`, `integer`, `PSD`, sparsity) when
  analyzer information or reduced representation matters. Use explicit
  constraints when dual variables are required; attributes do not record their
  own duals.
- Use `cp.sum`, `cp.sum_squares`, `cp.norm`, `cp.maximum`, and other atoms on
  expressions. Python `sum` or NumPy functions can be slow, object-typed, or
  semantically wrong.
- Use separate constraints `x >= 0` and `x <= 1`; chained comparisons and strict
  inequalities do not define valid CVXPY constraints.
- If a convex expression is marked unknown, rewrite it using a recognized atom
  or equivalent formulation; never suppress DCP errors without proving a
  different ruleset applies.
- Choose mixed-integer, conic, quadratic, or nonlinear solvers from installed
  solver support and licensing. Solver name is deployment configuration, not a
  universally portable constant.

Read [modeling, solving, and validation](references/operations.md) for DCP/DPP,
status gates, tolerances, solver choice, and repeated solves.

## Canonical anchor

```python
import cvxpy as cp
import numpy as np


def bounded_least_squares(design: np.ndarray, target: np.ndarray) -> tuple[np.ndarray, float]:
    coefficients = cp.Variable(design.shape[1])
    problem = cp.Problem(
        cp.Minimize(cp.sum_squares(design @ coefficients - target)),
        [coefficients >= 0, coefficients <= 1],
    )
    if not problem.is_dcp():
        raise ValueError("model must satisfy DCP")
    value = problem.solve()
    if problem.status not in {cp.OPTIMAL, cp.OPTIMAL_INACCURATE}:
        raise RuntimeError(f"solve failed: {problem.status}")
    if value is None or not np.isfinite(value):
        raise RuntimeError("solver returned no finite objective")
    if coefficients.value is None or not np.isfinite(coefficients.value).all():
        raise RuntimeError("solver returned no finite primal solution")
    return coefficients.value.copy(), float(value)
```

Production code must decide whether `OPTIMAL_INACCURATE` is acceptable and
validate residuals accordingly. Do not return `.value` before the status gate.

## High-risk rules

- Do not multiply decision variables together in a DCP model. Inspect curvature
  and use a recognized atom/formulation if the mathematics is convex.
- `/`, `*`, and `@` have different scalar/elementwise/matrix meanings. Assert
  every expression shape; do not rely on accidental broadcasting.
- Do not read `variable.value` or `constraint.dual_value` until a successful
  solve and appropriate status check.
- Infeasible, unbounded, and `infeasible_or_unbounded` are distinct outcomes.
  Handle them separately; an infinite objective is not a usable solution.
- `OPTIMAL_INACCURATE` is evidence of a solver tolerance/status, not equivalent
  to exact optimality. Validate domain residuals.
- Warm start and Parameters do not guarantee DPP or speed. Check the compiled
  model and measure repeated solves.
- Scaling affects numerical reliability. Normalize units or use solver options
  based on diagnostics, not by accepting a loose tolerance until tests pass.
- Solver-specific options and availability drift. Query `cp.installed_solvers()`
  and inspect the environment.

## Version grounding and completion

The official current tutorial documents DCP, DPP, solver status, variable
attributes, and performance guidance; CVXPY is not installed locally at this
authoring stage. Inspect version, installed solvers, atom/signature, and solver
options before execution. Read [verification](references/verification.md).

Completion requires the code to match the written mathematics; ruleset checks
to pass; solver capability to be explicit; all statuses to be handled; primal
values and residuals to be validated; repeated solve behavior to be tested when
claimed; and deterministic fixtures for feasible, infeasible, and boundary
instances.

## References

- [Symbolic and curvature model](references/object-model.md)
- [Modeling, solving, and validation](references/operations.md)
- [Verification and grounding](references/verification.md)
