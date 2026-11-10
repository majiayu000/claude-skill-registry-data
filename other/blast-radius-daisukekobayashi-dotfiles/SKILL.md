---
name: blast-radius
description: Use only when the user explicitly invokes blast-radius to test the assumptions a change's safety depends on. May create isolated verification artifacts; does not repair the implementation.
license: MIT
disable-model-invocation: true
---

# Blast Radius

Run only when the user explicitly invokes `blast-radius`, such as `$blast-radius`
in Codex or `/blast-radius` in Claude Code. A generic impact question or a
reference from another skill does not activate this workflow.

Identify the one or few facts a change's safety depends on, then test them.
A caller list is a starting point, not the result.

## Establish the claim

1. Resolve the target, baseline, intended behavior, and current working-tree
   changes. Include changed configuration, schemas, generated interfaces, and
   consumers outside the immediate language or repository when evidenced.
2. State the safety premise precisely: which inputs, versions, ordering, actors,
   and invariants make the change safe? Trace a concrete failure if it is false.
3. Follow what symbol search misses: serialization, persisted data, framework
   dispatch, lifecycle timing, feature flags, retries, and downstream consumers.
   Inspect pinned dependency source when it is material.

Use [how](../how/SKILL.md) and [why](../why/SKILL.md) when mechanism or intent
needs grounding. Do not manufacture distant callers or speculative risks.

## Test the premise

Choose the smallest check that could falsify the safety claim. Prefer an
existing documented check against the actual implementation. Follow repository
execution-context guidance; a script calling a reimplementation proves little.

Temporary probes and isolated test data are allowed by this invocation.
Classify them and place them in an ignored task directory or /tmp. Preserve
production code, existing tests, user data, and unrelated changes. Do not repair
the target, add a permanent test, start a shared service, change dependencies,
or mutate remote state without authorization covering that action.

Inspect the side effects of a proposed command before running it. Prefer local
fixtures and owned runtime instances. A dry-run label is not evidence that
external state is untouched. Stop unsafe probes and report the missing proof.

Use a known counterexample or negative control when practical to establish that
the check can detect the failure. Run against the actual changed code and
capture the command, input identity, result, and relevant output. Do not replace
a failed check with one that merely passes.

Use [prove-it-works](../prove-it-works/SKILL.md) to assess the evidence.
Stop processes you started and retain useful evidence.

## Report the actual coverage

For each consequential premise, label the strongest evidence obtained:

- asserted only;
- traced to source;
- failure path ruled out under stated assumptions;
- exercised through real code;
- reproduced through the running application.

Return what changed, the safety premises and their scope, confirmed risks,
risks checked and cleared, and unproven assumptions with the cheapest next
check. Attach evidence pointers and runtime limitations. Do not turn a limited
successful probe into a blanket safety or merge verdict.

## Source

Adapted from Lauren Tan's [pstack blast-radius](https://github.com/cursor/plugins/blob/12d587dfb20741cafc376c42c696c5f6e2a64487/pstack/skills/blast-radius/SKILL.md).
Local changes: explicit invocation, isolated experiments, no automatic repairs
or permanent artifacts, and preserved mutation approvals. See [LICENSE](LICENSE).
