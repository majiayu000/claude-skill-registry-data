---
name: implement
description: Implements a requested change with the smallest complete diff, splitting genuinely independent work across parallel agents with non-overlapping file ownership, then integrates and verifies it. Use when invoked explicitly to build a feature or change.
disable-model-invocation: true
---

# implement

Implement the requested behavior with the smallest complete change.

The task is the text given with this invocation.

---

## Establish the work

1. Read applicable repository instructions, the relevant implementation, tests, and call sites before editing.
2. Translate the request into acceptance criteria and identify dependencies, shared surfaces, migration order, and likely regressions.
3. Record the initial branch, staged/unstaged/untracked files, and diffs. Preserve user work. Never overwrite, stash, reset, or include unrelated changes.
4. Do not add speculative scaffolding, placeholder abstractions, unused extension points, or refactors unrelated to the acceptance criteria.

## Adaptive execution

Scale by real independent work:

- trivial: implement directly or use 1 specialist;
- modest: 2-3 agents;
- normal: 4-7 agents;
- broad, multi-system, or high-risk: 8-12+ agents.

Orthogonality and independence matter more than reaching a count. Parallelize only work that can proceed without consuming another workstream's unfinished output. Launch independent agents concurrently in one dispatch; never permit nested agents.

Tiers: executors run on your default model; an independent verification or review agent runs on your strongest model. Pin the model on every agent; an unpinned agent inherits whatever the session runs on.

Define contracts only where parallel work shares a real surface such as a schema, API, type, protocol, or migration boundary. Do not create contracts or stubs merely to manufacture parallelism. Resolve unstable shared surfaces serially before dispatch.

Give every writer:

- non-overlapping file ownership;
- acceptance criteria and relevant local context;
- explicit forbidden paths;
- required focused tests;
- instruction to preserve pre-existing dirty work.

If ownership would overlap, keep that integration point with the main executor or sequence the work. Agents must report exactly what they changed and verified.

## Integration

Integrate serially:

1. Re-read each change and compare it with its acceptance criteria.
2. Detect unexpected file changes and ownership collisions before combining work.
3. Reconcile shared interfaces, wire components, and apply migrations in dependency order.
4. Keep the resulting diff minimal; remove temporary code and speculative additions.

## Verification

Run focused tests during implementation, then the repository's relevant formatting, lint, type-check, build, and test commands. Use independent verification where risk justifies it. A verifier must not approve its own authored change.

If verification fails, fix the demonstrated cause and repeat. Stop after at most 3 verification rounds; report remaining failures with evidence rather than looping or weakening tests. Do not bypass hooks or checks.

Finish with changed files, acceptance-criterion evidence, fresh command results, and any preserved pre-existing failures or user changes.
