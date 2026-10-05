---
name: numpyro-python
description: Use for writing, reviewing, debugging, testing, or diagnosing NumPyro probabilistic programs on JAX, including sample sites, plates, distribution batch/event shapes, PRNG keys, MCMC/NUTS, SVI guides, Predictive, handlers, and JIT/vectorization constraints. Trigger on duplicate sites, shape or plate errors, reused random keys, recompilation, divergences, and posterior prediction. Do not use for NumPy numerical arrays, Pyro/PyTorch, PyMC models, ArviZ-only diagnostics, or deterministic JAX code without NumPyro.
argument-hint: "[NumPyro model, inference, JAX shape, PRNG, or diagnostic]"
---

# NumPyro Python

Build a pure-shape-stable probabilistic program, make independence explicit,
thread JAX randomness correctly, choose inference from model structure, and
verify both sampler diagnostics and predictive behavior.

## Boundary

This is the skill for the official `pyro-ppl/numpyro` project. “numpypro” in a
request is interpreted as NumPyro only when Bayesian/JAX context confirms the
intent. Use PyMC for a PyTensor model, Pyro guidance for PyTorch, and ArviZ when
the task starts from completed draws.

## Know the objects

| Object | Runtime meaning | Use it for |
|---|---|---|
| Model callable | A Python function whose primitives define a probability program when traced under handlers. | One generative model with observed inputs optional for prediction. |
| Sample site | A unique named distribution draw, optionally conditioned with `obs=`. | Latent variables and likelihood observations. |
| `plate` | A named conditionally independent batch axis, optionally subsampled. | Declaring independence and scaling minibatch likelihoods. |
| Distribution batch/event shape | Batch indexes independent distributions; event axes form one dependent outcome. | Making log-probability and plate alignment correct. |
| PRNG key | Explicit immutable JAX random state. | Supplying independent randomness by splitting/folding, never mutation. |
| Handler/trace | An effectful interpretation of sites: seed, condition, substitute, mask, scale, trace, and so on. | Inspection and controlled program transformation. |
| MCMC kernel / `MCMC` | Exact-asymptotic posterior sampling machinery and its collected chain state. | NUTS/HMC or compatible kernels when posterior sampling is feasible. |
| Guide / `SVI` state | A variational approximation plus optimizer state and loss. | Approximate scalable inference with explicit adequacy checks. |
| `Predictive` | Forward execution conditioned on prior or posterior samples. | Prior predictive, posterior predictive, and new-data predictions. |

Site names are the interface joining model, guide, posterior sample dictionaries,
and predictive execution. Shapes are part of that interface. Read [the program
and shape contract](references/object-model.md) before adding a plate, `.to_event`,
vectorization, or JIT.

## Ordered workflow

1. State the estimand, likelihood, observation unit, independence structure,
   missing-data policy, latent support, and prediction target.
2. Write the model with `y=None` or equivalent for predictive execution. Give
   every site a stable unique name; keep data-dependent Python control flow out
   of traced/JIT paths.
3. Work out each distribution's batch and event shape on paper. Add plates for
   actual conditional independence and `.to_event` only for dependent event axes.
4. Validate input dtype and shape before entering JAX. Enable required numeric
   precision before creating arrays or compiling.
5. Obtain one root PRNG key, split it for independent operations, and never
   reuse a consumed key for another stochastic result.
6. Run a seeded trace/shape check, prior predictive simulation, and small
   simulated-data recovery before expensive inference.
7. Choose MCMC or SVI from posterior geometry, scale, discrete structure, and
   accuracy requirement. Record all inference and initialization choices.
8. Diagnose MCMC or validate SVI against a trusted small problem. Generate
   posterior predictive samples with a fresh key and `obs=None`.
9. Convert to labeled `InferenceData` when chain/draw diagnostics, persistence,
   or model comparison are required; supply coords/dims rather than guessing.

## Decision map

| Condition | Action |
|---|---|
| Continuous differentiable posterior and tractable data | Start with NUTS/HMC; use multiple chains and inspect extra fields/diagnostics. |
| Large data or latency makes MCMC impractical | Use SVI with a guide matched to posterior structure; test approximation bias against MCMC on a smaller fixture. |
| Discrete latent sites | Marginalize/enumerate with supported machinery or choose a compatible method; do not pass them blindly to NUTS. |
| Repeated observations are conditionally independent | Use a named `plate` whose size matches that axis. |
| One multivariate outcome per observation | Mark its dependent axis as event shape; do not create a fake independence plate. |
| Same code recompiles for changing batch length | Pad/bucket to stable shapes or accept bounded recompilation; do not hide dynamic Python shapes inside JIT. |
| Need prior predictive | `Predictive(model, num_samples=...)` with unobserved `y` and a fresh key. |
| Need posterior predictive | `Predictive(model, posterior_samples=...)` with `y=None` and a fresh key. |

Read [inference and JAX execution](references/inference-jax.md) before tuning
chains, guides, devices, precision, JIT, or vectorization.

## Canonical model and MCMC anchor

```python
import jax.numpy as jnp
from jax import random
import numpyro
import numpyro.distributions as dist
from numpyro.infer import MCMC, NUTS, Predictive


def model(x: jnp.ndarray, y: jnp.ndarray | None = None) -> None:
    beta = numpyro.sample("beta", dist.Normal(0, 1).expand((x.shape[1],)).to_event(1))
    intercept = numpyro.sample("intercept", dist.Normal(0, 1.5))
    with numpyro.plate("observation", x.shape[0]):
        numpyro.sample("outcome", dist.Bernoulli(logits=intercept + x @ beta), obs=y)


def fit(x: jnp.ndarray, y: jnp.ndarray, seed: int):
    run_key, predictive_key = random.split(random.key(seed))
    mcmc = MCMC(NUTS(model), num_warmup=1_000, num_samples=1_000, num_chains=4)
    mcmc.run(run_key, x, y)
    samples = mcmc.get_samples(group_by_chain=True)
    predictions = Predictive(model, posterior_samples=mcmc.get_samples())(predictive_key, x, None)
    return mcmc, samples, predictions
```

`group_by_chain=True` preserves diagnostic structure. Draw counts are examples,
not universal defaults; calibrate them to ESS/MCSE and runtime. Inspect the
installed JAX key constructor and NumPyro signatures before copying this anchor.

## Non-negotiable rules

- Never reuse a PRNG key for independent random operations. Split once at the
  ownership boundary and pass subkeys explicitly.
- Never solve a plate error by deleting the plate. Reconcile data axes,
  distribution batch/event shapes, and model independence.
- Site names must be unique across an execution and stable between model, guide,
  samples, and predictions. A guide must cover required latent sites exactly as
  intended.
- JIT traces shapes/dtypes and static Python structure. Avoid data-dependent
  Python branches, mutation, hidden global randomness, and changing site sets.
- More SVI steps do not prove a good variational family. Inspect loss stability,
  multiple initializations, predictive fit, and small-problem comparison.
- More MCMC samples do not repair divergences, funnels, bad initialization, or
  non-identifiability. Reparameterize and standardize before merely tuning.
- Device parallelism and chain method depend on installed JAX devices and
  versions. Inspect, do not assume GPU/TPU or four parallel devices.
- Prediction must omit observed values and use a fresh key. Check returned site
  shapes and preserve chain/draw identity when exporting diagnostics.

Inspect the installed version, then use [testing and version
grounding](references/testing-version.md) for static
trace checks, shape assertions, reproducibility tests, and installed evidence.

## Completion gate

Do not declare completion until every site has unique stable naming; plate,
batch, and event shapes are asserted; PRNG ownership has no reuse; prior
predictive and simulated recovery checks pass; inference choice is justified;
MCMC diagnostics or SVI approximation checks have no unresolved critical
failure; predictive execution uses `obs=None` and a fresh key; JIT inputs have a
documented shape/precision policy; and unavailable devices, package versions,
or skipped statistical checks are reported.

## References

- [Program and shape contract](references/object-model.md)
- [Inference and JAX execution](references/inference-jax.md)
- [Testing and version grounding](references/testing-version.md)
