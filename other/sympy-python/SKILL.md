---
name: sympy-python
description: Use for writing, reviewing, debugging, testing, or optimizing Python SymPy symbolic mathematics. Trigger on Symbol, assumptions, Expr, Eq, solve/solveset, simplify, factor, expand, calculus, matrices, exact arithmetic, lambdify, code generation, or symbolic-to-numeric conversion. Do not use for NumPy-only arrays, mpmath-only arbitrary-precision numerics, CVXPY optimization models, or parsing untrusted mathematical text.
argument-hint: "[SymPy expression, equation, derivation, conversion, or error]"
---

# SymPy Python

Produce exact, assumption-aware symbolic code whose expression domain,
transformation goal, solution set, and numeric boundary are explicit.

## Core object model

| Object | Meaning | Use it for |
|---|---|---|
| `Symbol` and assumptions | Atomic unknown with declared mathematical properties. | Variables whose domain affects simplification and solving. |
| `Expr` | Immutable symbolic expression tree. | Algebra, calculus, substitution, rewriting, and exact evaluation. |
| `Eq`/relations | Symbolic proposition, not assignment. | Equations and inequalities. |
| `Set` | Exact solution/domain representation. | `solveset`, intervals, unions, finite/conditional solutions. |
| `Poly` | Polynomial with explicit generators/domain. | Polynomial algorithms and coefficient domains. |
| `Matrix` / matrix expressions | Concrete symbolic entries or symbolic linear algebra. | Shape-aware linear algebra. |

SymPy expressions are immutable; operations return new objects. Python integers
and `sympy.Integer` can participate exactly, but a Python float introduces a
binary approximation before SymPy sees it. Assumptions are attached when a
Symbol is created; redefining the same printed name does not mutate the old
symbol. Read [expressions, domains, and assumptions](references/object-model.md).

## Ordered workflow

1. Define symbols, domains, assumptions, and whether the required result is an
   expression, identity, equation, set, proof condition, or approximation.
2. Construct exact inputs with SymPy numbers/rationals and explicit functions.
3. Choose a targeted transformation from the desired normal form; avoid
   undirected `simplify()` when a specific operation is known.
4. Solve in the declared domain and preserve conditions/unsolved cases.
5. Verify symbolically by substitution, residual simplification, equivalence
   under assumptions, or differentiation/integration as applicable.
6. Cross the numeric boundary deliberately with `evalf` for a few values or
   `lambdify` for repeated array evaluation; define backend and precision.
7. Test singularities, excluded domain points, branch cuts, multiple/no/infinite
   solutions, exact-versus-float input, and equivalent forms.

## Rigorous-use contract

Use SymPy in three distinct modes, and state which mode produced the result:

| Mode | SymPy's role | Required evidence |
|---|---|---|
| Discovery | Generate patterns, candidate formulas, examples, or counterexamples. | Reproducible inputs and the unproved status. |
| Verification | Check a stated claim under explicit assumptions. | Original-domain contract plus symbolic residual or independent check. |
| Numerical support | Approximate an exact object or test a conjecture. | Precision, residual/error, stability check, and sampled regimes. |

Do not promote discovery or sampled agreement to proof. Classify the final
claim as symbolically established under stated assumptions, numerically
supported, sampled only, conjectured, or unresolved. If SymPy returns an
unevaluated result, `ConditionSet`, or an inconclusive `None`, preserve that
uncertainty instead of converting it to failure or success.

Before large computation, reduce the problem with symmetry, parity, scaling,
invariants, substitutions, or a normalized representation. Keep the original,
transformed, and claimed expressions separately. Search deliberately for
boundary, degenerate, sign-changing, singular-nearby, and smallest-dimensional
counterexamples. Read [rigorous symbolic practice](references/rigorous-practice.md)
for the complete decision checklist and reusable verification anchors.

## Decision rules

- Use `subs` for structural substitution. It does not mutate. For simultaneous
  or order-sensitive replacement, inspect and specify the installed contract.
- Use `expand`, `factor`, `cancel`, `apart`, `collect`, `trigsimp`, or `powsimp`
  when that exact form is required. Use `simplify` only when “simpler” is an
  acceptable heuristic result and tests assert meaning rather than spelling.
- Prefer `solveset` when domain and complete set semantics matter. Use `solve`
  only with an explicit expected return contract; its output shape varies with
  equations, symbols, flags, and solution structure.
- Use `Eq(lhs, rhs)` for an equation. `=` is Python assignment and `==` is
  structural equality, not a general mathematical equivalence proof.
- Use `Poly(expr, generators, domain=...)` for polynomial-domain algorithms;
  do not assume every expression in powers is a polynomial over the intended
  coefficient domain.
- Use `lambdify` only for trusted expressions and an explicit numeric backend.
  It uses code-generation/evaluation mechanisms and must not consume untrusted
  input.

Read [operations and numeric boundaries](references/operations.md).

## Canonical anchor

```python
import sympy as sp

x = sp.Symbol("x", real=True)
rate = sp.Symbol("rate", positive=True)
expr = sp.exp(-rate * x)

integral = sp.integrate(expr, (x, 0, sp.oo))
assert sp.simplify(integral - 1 / rate) == 0

roots = sp.solveset(x**2 - 2, x, domain=sp.S.Reals)
assert roots == sp.FiniteSet(-sp.sqrt(2), sp.sqrt(2))
```

Positivity makes the improper integral convergent and permits the intended
result. The solution domain excludes complex roots by contract.

## High-risk rules

- Construct `sp.Rational(1, 3)` or `sp.S(1) / 3`, not `sp.Rational(1 / 3)`;
  the latter receives an already rounded Python float.
- Do not compare symbolic objects in Python `if` unless the relation is known
  boolean. An unresolved relation is not `False`; handle assumptions/conditions.
- Structural `==` can reject mathematically equal expressions. Verify a residual
  with a targeted transform under stated assumptions, while respecting domains
  and singularities.
- Transformations can change apparent domains or branch behavior. Test excluded
  points and complex branches before treating rewritten forms as equivalent.
- Before cancelling an additive rational expression, use `together` and record
  the denominator roots from that uncancelled combined form. `fraction(expr)`
  alone can report denominator `1` for a sum of fractions. If the incoming
  expression already auto-cancelled, its lost exclusions cannot be recovered;
  preserve the original domain contract separately.
- Solvers can return `ConditionSet`, parameterized families, dictionaries,
  tuples, or sets. Do not coerce these to a guessed list and lose conditions.
- Avoid wildcard imports in production; explicit `import sympy as sp` prevents
  collisions with Python/NumPy names.
- `lambdify` chooses numeric semantics from modules and can emit unsafe code for
  untrusted expressions. Keep parsing and evaluation behind a trust boundary.
- Exact symbolic computation can explode in time/memory. Use targeted
  transformations, assumptions, expression-size limits, and numeric fallbacks
  under an explicit accuracy contract.
- Treat solver output as candidates. Substitute finite candidates into the
  original relation; distinguish `True`, `False`, and inconclusive checks.
- Solve symbolic linear systems with an appropriate solver such as `LUsolve`,
  then verify `A * solution - b`; do not form an inverse merely to solve.
- Record convergence conditions for limits, integrals, sums, and series. Local
  series agreement is not a global identity without a separate argument.

## Version grounding and completion

The current stable documentation is SymPy 1.14.0; it is not installed in the
foundry environment. Check the installed version with `sp.__version__`, then inspect
function signatures and solver/printing behavior. Read [verification](references/verification.md).

Completion requires exact inputs, explicit assumptions/domain, the requested
normal form or solution contract, symbolic residual/equivalence checks,
singular/branch tests, safe numeric conversion, and no loss of conditions or
precision at the boundary.

## References

- [Expressions, domains, and assumptions](references/object-model.md)
- [Operations and numeric boundaries](references/operations.md)
- [Rigorous symbolic practice](references/rigorous-practice.md)
- [Verification and grounding](references/verification.md)
