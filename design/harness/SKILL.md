---
name: harness
description: "When maintaining, assessing or redesigning the agent harness itself — skills, agents, extensions, hooks, tools, setup, docs and tests — or absorbing upstream designs into it."
---

# Harness

Judge the harness by the outcomes it gives the agent and the user, not by the
files it has today. Nothing earns protection by already existing: add, rewrite,
merge, move or delete whatever makes the harness better, and preserve the useful
behavior, not the component that carried it. `write-skill` owns skill-level
consolidation and `architecture` owns structural alternatives when either helps.

Pick the posture the request needs:

- **Assess** — measure the current harness and report drift, conflicts, overlap
  and waste. Stays local: no upstream fetch or checkpoint change.
- **Reassess or redesign** — after a model, host or recurring-failure change, or
  when asked to reorganize or simplify.
- **Absorb upstream** — on an explicit request to review sources.

Both deeper postures load [Review](references/REVIEW.md), which owns coverage,
native-host checks, the single approved plan and ledger checkpoints, and uses
[Behavior probes](references/BEHAVIOR_PROBES.md) when comparison evidence is needed.

## Inspect every layer

Each layer earns its keep differently. Judge it on its own test, and against the
host's current native features: a component built around a host gap becomes waste
when a release closes the gap.

- **Skill** — gives a useful stance on its intended turns. Tell a weak trigger
  from missing discovery, selection or observation before retiring it.
- **Agent preset** — holds a role the fleet cannot already cover, and returns
  evidence the parent could not gather inline.
- **Extension, hook or tool** — owns state, commands, UI, gates or lifecycle that
  a skill cannot carry, as one shared piece rather than one per caller.
- **Setup and package surface** — keeps source, installed copies and runtime
  resources separate, and preserves unrelated user files.
- **Doc** — states truth the environment cannot be asked for. Anything a script,
  config or `--help` answers is a cache that will go stale.
- **Test** — catches real regressions in executable contracts, rather than pinning
  prose or certifying behavior it never exercised.

Also look across layers for instruction drift between `AGENTS.md`/`CLAUDE.md`
copies, permission and preset conflicts, stale memory, weak navigation pointers,
and two owners of one fact.

For a repeated mechanical mistake, inspect existing tests, lint, scripts and CI:
a missing, unwired or broken check may be the defect. Prefer a focused deterministic
check over another prose rule. Keep judgment and non-obvious authority boundaries
in guidance; do not install a hook merely because one is absent.

## Measure the skill layer

Resolve `SKILL_DIR` to the directory containing this loaded `SKILL.md`, not a
checkout-relative path. For an isolated source inventory, run:

```bash
bun "$SKILL_DIR/scripts/skill-cleaner.ts" --root PATH --root-only --no-logs
```

Use `--help` for options. Log scans read private history and need that scope;
`--log-root PATH` replaces the default Pi/Claude roots. Do not widen roots merely to
fill gaps. Default inventory omits project `.claude/skills` and package resources;
add them only as explicit roots. Prefer an actual host-exported inventory:
filesystem presence and frontmatter eligibility are not effective selection.

Read coverage and skipped/error/byte counts before interpreting results. Missing
signals, partial logs and inherited context are unknown, not proof of disuse.
Token figures are character-ratio estimates of listings and bodies, not native
prompts, retention or savings; reference and inherited-context costs stay unmeasured.

## Ground rules

Current config and command output outrank memory. Fix the owned source, not an
unexplained deployed copy. Similarity is a lead, not identity or permission to
overwrite. Preserve user files; deletion of user-owned material needs authority.
A clean assessment writes nothing.

Deliver: posture, layer coverage and evidence limits, ranked findings with owning
paths, the proposed changes (including removals and moves) with preserved or
retired behavior, and the validation still unrun.
