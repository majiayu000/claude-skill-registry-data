---
name: component-repair
description: Repair the code behind a verification finding — a level-2 bug, or on request a level-1 spec<->code discordance — completely and across components if needed, and open a PR a non-expert can approve from the evidence. Runs the vendored repair-agent; acceptance is decided by repair_accept_repo.sh, never by the agent.
argument-hint: "<component> <OBLIGATION-ID> --callees <mods> --base <rev>"
---

> **Frozen 2026-10-09.** This skill moved to [ai-native-storage-workbench](https://github.com/AI-native-Systems-Research/ai-native-storage-workbench) (`fv/skills/`). Edit it there; this copy is not updated. Install the current version with `fv/install.sh <this-repo>`.


# component-repair

Fixes the CODE behind a verification finding:
- a **level-2 bug**: a property spec and code agree on (or the code's own documented guarantee) that
  formal verification refuted; or
- on request, a **level-1 discordance** from `verif/discordances.yaml`. Step one is to CONFIRM it with a
  test that fails on today's code; if none can be written it was a misreading — report it withdrawn and
  change nothing.

**Record the test's verdict on the discordance — every time, in the component's own verif dir** (Cornel,
2026-10-05: a confirmed row must not keep saying "candidate"). This applies to BOTH modes: a level-2 bug
repair whose RED-FIRST test exercises a requirement that is also a level-1 discordance confirms that
discordance too (the EPO stale-handle repair confirmed `D-FR-012-lru_list.rs:109-…`).
```
python3 ../component-verify/gate/record_confirmation.py components/<c>/verif <discordance-id> \
    confirmed|withdrawn --evidence "<test file> failed|passed on <rev> before any fix" [--fix "PR #<n>"]
python3 ../component-verify/gate/level1.py components/<c>/verif
python3 ../component-verify/gate/render_discordances.py components/<c>/verif
```
`confirmed` = the test FAILED on the unfixed code (RED-FIRST leg 2b passed). `withdrawn` = it PASSED: the
code does it and the code reader missed it. Commit `verif/discordance_confirmations.yaml` and the
regenerated pair on both verif branches of the component. The verdict comes from the test, never from
reading or from the agent's own claim.

The person who approves the PR may not read Rust (Cornel, 2026-10-04), so the agent does the whole job:
it chooses the fix, implements it wherever the root cause lives — several components, a shared
interface — adds regression tests, makes the target proofs prove, keeps every touched verified
component verified, and writes a short plain-English PR. It never edits an obligation, a spec, or a
proof that already exists.

## What is here
- `spec.yaml` — the agent spec (agent_builder schema). Validates with 0 errors / 0 warnings.
- `repair_accept.sh` — the acceptance check, run by code. A repair passes only if it is
  PROVED (callee modules + a new verify_<id> prove; its mutant fails with the prover having run),
  REAL (src/ changed), RED-FIRST (its own repair_test_*.rs fails on the unfixed code), TESTED
  (cargo test passes) and HARMLESS (no module that proved before stops proving).
- `repair_oracle.sh` — the proof part of that check.
- `repair_accept_repo.sh` — the REPOSITORY-level check the agent's oracle runs: (A) every touched crate
  and every crate depending on one compiles (a crate whose native library is missing on this machine is
  listed, never silently passed); (B) their tests pass; (C) each target passes `repair_accept.sh`;
  (D) the proof model was updated wherever a function it cites changed; (E) every touched, published
  component is re-scored by its gate BEFORE and AFTER the repair, same gate and scope, with nothing lost.
  It prints the evidence table that goes into the PR.
- `evals/` — held-out tests the agent never sees, run against the real code.
- `agent/` — the generated agent and the workbench runtime kit, VENDORED (see `agent/VENDORED.yaml`
  for the exact workbench commit). We own this copy; workbench changes do not reach it.

## Run it (attended)
```
export AGENT_RESOURCE_AI_NATIVE_STORAGE_CERTUS=<your certus checkout>
export AGENT_RESOURCE_CREUSOT=<creusot tree>      # for creusot-std
export REPAIR_GATE_DIR=<repo>/.claude/skills/component-verify/gate   # the gate re-verification runs
.claude/skills/component-repair/agent/agents/repair-agent/run.sh run \
  --input repository=<checkout> --input component=<c> --input obligation_id=<ID> \
  --input bundle=components/<c>/verif/unified_properties.yaml \
  --input callee_modules=<mods> --input base_rev=<rev> \
  --input oracle_dir=.claude/skills/component-repair
```
The agent chooses the fix and explains the alternatives it rejected. After `repair_accept_repo.sh`
passes it asks for **approval; approving pushes a branch and opens a PR** whose description has four
parts — what was wrong (one sentence), what changed, the evidence table, the risks. Set `REPAIR_AGENT_NO_PR=1` to keep the
verified commit local instead. Evaluation runs never push or open a PR.

## Rules
- A level-1 discordance is handed to the agent only on request, and is confirmed by a failing test first.
- The operator names `callee_modules`; the agent must not choose its own evidence.
- A bug appears on a component's scoring page only once its fix is merged.
