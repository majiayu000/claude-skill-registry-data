---
name: trace-spec-to-plan
description: "Use before converting a plan into epics/beads/worktrees, and whenever you need to know whether a plan actually implements its spec. Walks EVERY requirement in the spec forward into the plan, one item at a time, and reports PLANNED / NAME-ONLY / ABSENT / PARTIAL. Distinct from verify-against-source, which reads the ARTIFACT and asks 'does this honor its source' — this reads the SPEC and asks 'where did this land'. Triggers - about to run project-setup, about to create epics or beads, plan review, 'does the plan cover the spec', 'did we miss anything', 'is the plan complete'."
---

# Trace Spec → Plan

**Announce at start:** "I'm using trace-spec-to-plan to walk every spec requirement into the plan."

## Why this exists

> 🔑 **A reviewer reading an artifact cannot see what isn't in it.**

That sentence is the whole justification. Every other review in the pipeline reads the **plan** and asks *"is this sound?"* — so it can only find defects in what is present. **Absence has nothing to look at.**

⇒ **This replaces ad-hoc extra audits in the standard flow rather than supplementing them.**

## When it runs

**Immediately before `project-setup` creates epics and beads.** That is the last moment the spec is still in the room. Once a requirement is missing from the plan **and** absent from the beads, the beads become the working set, nobody consults the spec again, and the gap stops being discoverable at all.

Also valid: any time someone asks whether a plan is complete against its source.

### Two hard preconditions

🚫 **NEVER run by the plan's own author.** Self-review cannot catch a requirement the author never perceived — same person, same anchoring, same blind spot. **Dispatch it.**

⚠️ **Run against a FROZEN plan.** A sweep racing live edits produces stale findings that cost more to triage than they are worth.

## Sizing — the judgment call

1. **COUNT THE SPEC ITEMS FIRST, NOT PAGES.** Include every sub-item: `A3.1–3.4`, `P1–P8`, each ruled-out branch, each contradiction disposition, each named sequencing constraint. A spec that reads as "20-something sections" was **~65 discrete requirements**.
2. **≤ ~15 items ⇒ one agent. More ⇒ partition at ~12–15 items per agent.**
3. 🔴 **PARTITION BY SPEC ITEM, NEVER BY PLAN SECTION.** Section-partitioning manufactures false ABSENTs whenever a requirement is covered in a phase that auditor wasn't given. **Every agent searches the WHOLE plan for its own items.**
4. Write the shared instructions to **one file** (`resources/sweep-agent-prompt.md`) and give each agent only its item list. Keeps dispatches short and identical.
5. Use `efficient-multi-agent-research` for launch-and-wait mechanics.

## The four verdicts

| Verdict | Means |
|---|---|
| **PLANNED** | A task exists with concrete steps that would make the requirement true — files named, code or commands shown. |
| **NAME-ONLY** | The plan mentions, quotes, or asserts the requirement — but no task carries out steps. |
| **ABSENT** | Not mentioned anywhere. |
| **PARTIAL** | Part is planned; a named part is not. Say which. |

🔑 **NAME-ONLY IS THE LOAD-BEARING VERDICT AND THE ONE AN AGENT WILL AVOID ASSIGNING.** It feels harsh against well-written prose, and PLANNED is always the cheaper answer. **A requirement restated in a warning box, a doc comment, an architecture paragraph, or a Definition-of-Done row is NAME-ONLY unless a task carries out steps.**

### Worked example — the judgement that decides this skill's value

```go
// assess computes one agent's verdict from the joined snapshot. It decides
// from PROCESS EVIDENCE — PID pair union session presence — and never from a
// self-written timestamp. It writes nothing.
func assess(s *Snapshot, j *Joined, agentID string) Verdict
```

A correct doc comment restating the spec, a precise signature, and it is **consumed by a task elsewhere in the plan**. It reads as covered.

**Verdict: NAME-ONLY.** There is no body and no task anywhere implements one. That function *was* the reconciler. **The tell is not the quality of the prose — it is that no step produces the thing.**

## Three questions per requirement

1. **Is there a task?** Naming a mechanism is not doing it.
2. 🔴 **Does the plan contain every step to make it true — INCLUDING CREATING SUBSTRATE THAT DOES NOT EXIST YET?** Open the real struct / table / interface at the plan's authored-against SHA. **A mechanism operating on a substrate that cannot hold the data is a silent no-op.** *Highest-yield question here:* a paired-write primitive was fully and correctly specified while the struct lacked the field and the table lacked the column.
3. **Would anything FAIL if it regressed?** A property with an implementation but no failing test is not achieved. **A manual grep in a Definition of Done cannot fail next month.**

## Framing — do not get this backwards

🔴 **A gap is a MISSING STEP IN THE PLAN, never a defect in the spec.** The spec is owner-ruled. If a requirement needs a field that does not exist, **the plan must add the field** — that is what plans are for.

**Never report a requirement as "impossible" and never suggest narrowing one.** "Impossible" points the next reader at scoping down the spec, which is the opposite of the repair.

🚫 **The spec is never edited by this skill or its findings.** A finding that appears to require a spec change is an escalation to the owner, never an action.

## Reporting rules

- **Write the report to a FILE first and append as you go.** The final message is a summary; the file is the deliverable. *(Dispatched agents have completed full audits whose final text never reached the parent. The agent does not notice.)*
- **Record PLANNED items too.** A map that lists only holes cannot show what is safe to build on, and cannot be checked for completeness.
- **Report what could not be resolved**, naming the search run — never guess. An honest "unresolved" is what makes the PLANNED verdicts worth anything.
- 🔴 **If a partition returns ALL PLANNED with zero NAME-ONLY, hand-verify two PLANNED rows at random and show the working.** **An all-clear is the result most likely to be produced by not looking.**

## After the sweep — the dispatcher's job

1. **Consolidate into ONE numbered list** across all partitions. Never act on partial batches.
2. **Filter stale findings** if the plan moved during the sweep — and say so rather than counting them.
3. **Close every gap before epics are created.** That is the entire point of running it here; a filed-and-deferred gap is the failure this skill exists to prevent.
4. **Spot-verify any finding that names a file, line, or symbol** before acting. Auditors misread cites, and a correction carries the same evidence bar as the finding it replaces.

## What this does NOT cover

**Compositional defects.** Per-item traversal cannot see *"every phase individually fine, the whole broken."* Measured example: an end state that would run **two concurrent reconcilers**, violating the premise of the design's own no-multi-writer ruling — while every individual requirement was satisfied.

⇒ **Pair this with a compositional pass.** They are different lenses and neither substitutes for the other. **The standard flow wants two audits, not eight.**

## Failure modes of this skill itself

| Failure | Symptom | Guard |
|---|---|---|
| Folded into `verify-against-source` as redundant | "we already check coverage" | The traversal direction differs; keep both |
| Run by the plan's author | Everything PLANNED | Dispatch it |
| Partitioned by plan section | False ABSENTs | Partition by spec item |
| Agent avoids NAME-ONLY | Zero NAME-ONLY across a large partition | Mandatory hand-verify of two rows |
| Findings filed, not fixed | Gaps reach the beads anyway | Close before epics |
