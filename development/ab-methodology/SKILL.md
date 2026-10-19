---
name: ab-methodology
description: "Use for reusable ab methodology recipes in software and coding-agent work."
---

# A/B methodology & attribution — recipes (generic tier)

On-demand recipes (2). Trigger→action heuristics; pull the relevant one when its situation arises.

#### 1. Port to a new language using the source's test assertions as the parity oracle; prove correctness via frame-parity
`generic`

When porting one implementation to another language/runtime, use the SOURCE's existing test assertions (its recorded fixtures and hard-coded expected values) as the parity oracle rather than building a fresh ground-truth generator; treat byte/frame-level parity as a proxy for CORRECTNESS, distinct from whether it performs as well. Parity is only meaningful over the deterministic prefix before the first RNG/nondeterministic branch -- a contiguous divergence that never recovers is the expected signature of a correct port, while intermittent re-convergence signals a real logic bug; adding a shared master seed to both sides extends measurable parity. When cloning code into a new version, do a behavior-preserving copy first -- change only identity-bearing tokens (export symbols, ABI constants, image/build identifiers, display labels) and keep logic identical so any later A/B is attributable to deliberate changes, not copy drift; keep the reference strictly additive so it stays a valid oracle, and prefer surgical behavioral edits over rewrites. (Illustrative: a Nim perception pipeline ported to Python matched byte-for-byte ~2500 frames / 87%, reaching 100% on imposter paths once a shared --seed was added.)
  <sub>sources: auggie:5d1ff8d5-2505-4dca-af45-56d3070363e2, codex:019e02f7-0f59-7f43-ad7b-f4e3c2d37a2f, codex:019dfece-78f8-7722-8301-f4e0fafc2cd9, opencode:ses_224322057ffexj7SYlcfVA0zgy (+5)</sub>

#### 2. Validate an agent-harness change with a one-variable A/B that exposes the failure and includes a false-positive case
`generic`

Validate an agent-harness change with a controlled A/B that varies exactly ONE variable across arms and compares qualitative process signals (tool-use count, depth, whether the prescribed ritual actually fired) rather than just pass/fail. Two non-negotiables: the task must EXPOSE the target failure mode (e.g. include hidden dependencies in files the agent wouldn't think to open, or all arms solve it identically and mask the effect), and include at least one false-positive scenario where the framework should NOT apply so over-fitting is detectable.
  <sub>sources: metta/agent-plugins/kitchensink/skills/ks.agent-harness-design/SKILL.m</sub>
