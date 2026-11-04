---
name: skill-diet
description: "Put an existing skill on a measured diet: remove duplication and stale tool guidance, then compare old, new, and no-skill behavior before accepting the rewrite. Invoke explicitly for skill slimming or drift audits; do not automatically launch model evaluations for every skill edit."
disable-model-invocation: true
license: MIT
---

# Skill Diet

Keep instructions only where they change behavior, and verify that cutting them does not lose what matters. Adapted from Nico Bailon’s skill-diet; see [source notes](UPSTREAM.md).

## Freeze the question before cutting

Inspect the skill, references, consumers, and any tool it teaches. Record a baseline copy and its description/body/reference sizes. Use task-scoped session examples when available; do not trawl unrelated histories or copy credentials into an evaluator.

Write representative cases, safety boundaries, expected outcomes, and acceptance criteria while only the old version exists. Include the user’s motivating case and likely near-misses. Keep a no-skill baseline: instructions that merely repeat reliable model behavior may not earn their cost.

## Cut at the right layer

1. Prefer a clearer tool error, type, or deterministic check when it prevents the mistake directly.
2. Edit the existing rule rather than append a duplicate. Keep incident history and provenance outside runtime instructions.
3. Keep triggers in the description, common judgment in SKILL.md, occasional detail in linked references, and current CLI/API syntax in working help where that help is adequate.
4. Remove generic ceremony, repeated examples, and stale facts. Preserve concise permission, privacy, and data-preservation boundaries; a few successful trials do not make safety rules redundant.

Prove alleged tool drift through source or safe calls. Keep necessary guidance when help is absent or misleading; do not cut it merely to hit a token target. Do not change vendor-managed files without an explicit local-fork decision.

## Compare honestly

Use fresh contexts, matched models and inputs, repeated trials, deterministic end-state checks where possible, and blinded judgment for qualitative outcomes. Test that the intended skill is supplied and other versions, memory, and global rules do not contaminate comparisons. Record exactly what the evaluator can and cannot exercise.

The repository’s [evaluation guide](references/evaluation.md) describes the local text-only harness. It does not test tool execution or automatic discovery. Complete every planned cell; changed inputs require a new frozen evaluation. Missing results, failed adapters, or stale records are not passes.

Accept a smaller skill only with adequate evidence for its intended use. Inspect failures before changing either the skill or the rubric. No detected regression is not statistical proof of equivalence. If evidence is insufficient, keep the rewrite a candidate and report the gap rather than declaring the diet successful.
