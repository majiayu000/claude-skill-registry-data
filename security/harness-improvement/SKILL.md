---
name: harness-improvement
description: Use when the coding agent repeatedly misses the same class of bug, verification, context, security, UX, session-continuity, cross-harness, packaging, skill-routing, install, or retry-loop issue; turn evidenced friction into the smallest tested sensor, rule, schema, reference, or Skill improvement without auto-promoting one-off observations.
---
# Harness Improvement

1. Gather concrete failures and evidence. Do not redesign the harness from one anecdote unless the failure is severe and the human explicitly accepts the scope.
2. Capture recurring observations as project-scoped lesson candidates with `.ai/scripts/lesson_candidate.py`; include evidence references and confidence.
3. Never let learned/imported observations auto-edit shipped Skills. Promotion must satisfy `.ai/LEARNING_POLICY.json` and explicit human approval.
4. Classify the missing capability: context, procedure, correctness sensor, runtime visibility, security verifier, architecture invariant, session continuity, cross-harness drift, packaging/ownership, skill activation, repo-trust mapping, or retry-loop control.
5. Prefer the smallest durable mechanism:
   - knowledge -> concise reference;
   - repeated procedure -> compact Skill;
   - correctness bug -> deterministic test/lint/schema;
   - runtime blindness -> browser/log/metric/probe sensor;
   - architecture drift -> structural check;
   - lost work -> verified checkpoint/state/resume;
   - adapter drift -> canonical-source + surface validator;
   - packaging drift -> manifest/ownership/exact-artifact test;
   - skill-routing uncertainty -> positive/negative routing eval plus trustworthy telemetry or paired causal eval;
   - repository uncertainty -> `observed`/`declared`/`inferred` mapping, never inferred execution by default;
   - repeated identical failure -> loop guard + changed-hypothesis requirement;
   - false positives -> stronger evidence threshold.
6. Use the lightest execution profile that preserves truth. `native` avoids unnecessary durable state; `portable`/`audited` persist verified progress only. Never remove trait-required product checks just to save tokens.
7. For harness changes set `traits.harness_modification=true` and record `harness-security`, `surface-drift`, `package-contract`, `harness-self-test`, and `skill-eval-contract` evidence. If a shipped Skill changes, also set `skill_modification=true`; do not treat Skill presence or self-report as runtime acceptance.
8. Test the mechanism against the failure that motivated it. Preserve the regression in `self_test.py` or a narrower deterministic test.
9. Keep Skills compact and progressively loaded. Do not import large external skill/agent catalogs merely because they are popular.
10. Check license/provenance before copying external implementation details. Prefer reimplementation of mechanisms when a smaller local control is enough.
11. Before release run `package_release.py`; verify and re-extract the exact ZIP rather than trusting the source directory.
