---
name: using-jax
description: Applies JAX patterns for scientific Python development. Use when working with JAX, distrax, numpyro, blackjax, or scientific computing. Covers vmap, JIT, RNG handling.
version: 2.0.0
---

# JAX Scientific Computing

## Core Rules

1. **Pure functions** - No side effects
2. **JIT outer functions** - `@jax.jit` on hot paths
3. **vmap not loops** - `jax.vmap(fn)` instead of list comprehensions
4. **Split RNG keys** - Never reuse keys

## Patterns

```python
# RNG: always split
key, k1, k2 = jax.random.split(key, 3)

# Batching: vmap not loops
batched = jax.vmap(fn)(inputs)

# Loops: use scan
_, results = jax.lax.scan(step_fn, init, xs)
```

## Gotchas

- Arrays are immutable
- No Python control flow in JIT - use `jax.lax.cond`, `jax.lax.scan`
- Check NaNs: `jnp.isnan(x).any()`
