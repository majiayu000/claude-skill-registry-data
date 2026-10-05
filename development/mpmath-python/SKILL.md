---
name: mpmath-python
description: Use for writing, reviewing, debugging, testing, or validating Python mpmath arbitrary-precision numerical code. Trigger on mpf, mpc, mp.dps, workdps, interval arithmetic, high-precision quadrature, root finding, special functions, matrices, inverse transforms, or precision/convergence failures. Do not use for ordinary NumPy vectorization, SymPy symbolic manipulation, decimal currency arithmetic, or machine-float code with no precision requirement.
argument-hint: "[mpmath computation, precision target, code, or failure]"
---

# mpmath Python

Produce arbitrary-precision numerical code with explicit input precision,
working precision, conditioning, convergence evidence, and output accuracy.

## Core model

| Object/context | Meaning | Rule |
|---|---|---|
| `mp.mpf` | Arbitrary-precision real floating value. | Construct from strings/integers when decimal input must be preserved. |
| `mp.mpc` | Arbitrary-precision complex value. | Define branch and complex-domain expectations. |
| `mp` context | Global/default precision and algorithms. | Avoid leaking precision changes across callers. |
| `workdps`/`workprec` | Scoped absolute decimal/binary working precision. | Prefer when the function owns a precision target. |
| `extradps`/`extraprec` | Scoped precision added to the current context. | Prefer when guard precision is relative to the caller. |
| `iv` context | Interval arithmetic values. | Use only with interval-specific containment semantics. |
| matrix | Dense arbitrary-precision matrix. | Suitable for modest sizes; define conditioning and shape. |

Arbitrary precision does not repair an inexact Python float. `mp.mpf(0.1)`
captures the already-rounded binary value; `mp.mpf("0.1")` represents the
decimal input at current precision. Precision controls arithmetic performed
after construction, not hidden source accuracy. Read [numbers and precision](references/precision.md).

## Ordered workflow

1. Define the mathematical quantity, real/complex domain, target error (absolute,
   relative, or digits), and credible input accuracy.
2. Construct constants without premature binary-float rounding.
3. Estimate conditioning/singularities and choose a stable formulation and
   algorithm before increasing precision.
4. Compute inside scoped guard digits; never change global `mp.dps` without
   restoring it.
5. Repeat at higher working precision or with another method and compare a
   residual, enclosure, or known identity.
6. Round/serialize only at the output boundary and report achieved evidence,
   not merely configured digits.
7. Test near singularities, cancellation, complex branches, poor initial guesses,
   non-convergence, and inputs whose original accuracy is lower than `mp.dps`.

## Intent map

- Use direct special functions before reimplementing series or converting
  through machine floats.
- Use `quad`/specialized quadrature after splitting discontinuities or difficult
  intervals and defining endpoint behavior.
- Use `findroot` with an initial guess/interval suited to the solver, then check
  the residual independently. `verify=False` removes one check; it does not make
  a root valid.
- Use `diff`, numerical sums/products, ODE, transform, or matrix routines only
  after checking their documented convergence and domain contract.
- Use `workdps(total_digits)` for a local absolute precision target; use
  `extraprec`/`extradps` when guard precision is relative to the caller.
- Use interval arithmetic when a guaranteed enclosure is required and the
  interval algorithm actually provides it. Do not assume `iv.findroot` encloses
  a root; the official documentation explicitly warns otherwise.

Read [algorithms and validation](references/operations.md).

## Canonical anchor

```python
from mpmath import mp


def _exp_ratio_at(x_text: str, work_digits: int) -> mp.mpf:
    with mp.workdps(work_digits):
        # Construct inside the context: mpf rounds input at current precision.
        x = mp.mpf(x_text)
        return mp.expm1(x) / x if x else mp.one


def stable_cancellation(x_text: str, digits: int = 50) -> mp.mpf:
    if digits < 2:
        raise ValueError("digits must be at least 2")
    lower = _exp_ratio_at(x_text, digits + 10)
    higher = _exp_ratio_at(x_text, digits + 20)
    with mp.workdps(digits):
        lower_rounded = +lower
        higher_rounded = +higher
        if lower_rounded != higher_rounded:
            raise ArithmeticError("result did not stabilize at requested precision")
        return higher_rounded
```

The stable formulation matters more than simply raising `mp.dps`. Constructing
the input inside each working context prevents caller precision from truncating
the decimal first. Unary plus inside `workdps(digits)` explicitly rounds the
returned value to the requested precision; merely leaving a context does not.

## High-risk rules

- Never seed a high-precision computation with an accidental Python float when
  the original decimal or exact ratio is available.
- Do not promise `dps` correct digits. Guard digits and precision-doubling tests
  provide evidence; ill-conditioning can consume them.
- Do not compare high-precision outputs to machine-float expected values as the
  oracle. Use exact identities, strings, independent methods, or higher precision.
- Root-finding success requires a small residual and the intended root/domain.
  Multiple roots and steep/flat functions can defeat naive convergence checks.
- Quadrature requires singularity, oscillation, infinite interval, and branch
  analysis. Split intervals or select specialized methods under a documented rule.
- Global context mutations create order-dependent tests and concurrency hazards.
  Scope them with context managers or clone a context where isolation is needed.
- Mixing mpmath and NumPy often creates `object` arrays or downcasts to float.
  Make conversion, vectorization, and precision loss explicit.
- Formatting many digits is not evidence they are correct.

## Version grounding and completion

Official current documentation identifies mpmath 1.3.0. It is not installed in
this foundry. Inspect version, context behavior, and exact callable signatures
before relying on them. Read [verification](references/verification.md).

Completion requires exact input construction, a scoped precision policy, a
stable algorithm, residual/enclosure or precision-doubling evidence, domain and
failure handling, and serialization that does not silently reduce accuracy.

## References

- [Numbers and precision](references/precision.md)
- [Algorithms and validation](references/operations.md)
- [Verification and grounding](references/verification.md)
