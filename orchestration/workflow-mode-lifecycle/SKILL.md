---
name: workflow-mode-lifecycle
version: "1.1.0"
user-invocable: false
description: "Shared lifecycle contract for manual/auto control-flow plus optional ai-proxy overlay recognition in workflow skills: auto and overlay always revert to manual on completion or interruption; re-entry needs an explicit trigger; implicit continuation never re-activates them; batch orchestrators pass Stage-exit policy explicitly. Overlay maps to auto carrier + policy; charter stays in ai-proxy-discipline. Hosts that omit ai-proxy triggers ignore overlay. Referenced via frontmatter dependencies. Triggers — 「模式生命周期」「切换自动模式」「切换 ai-proxy」 / workflow mode lifecycle. Do NOT use as the proxy charter or as a third control-flow enum."
---

# Workflow Mode Lifecycle

> Internal shared skill. Prevents **mode stickiness** — the user being unaware that the AI is still making automatic decisions. Referencing workflows declare it in frontmatter `dependencies` and abort at startup if it is missing.

## Mode recognition

- On hosts that list ai-proxy triggers, overlay phrases (「ai-proxy 模式」「AI 代理模式」 / "ai-proxy mode", or mid-run 「切换 ai-proxy」 / "switch to ai-proxy") request overlay first (section below). If both an overlay trigger and 「自动*」 appear, overlay+freeze wins over naked auto.
- Else trigger contains "自动" (auto) → **auto mode**; otherwise → **manual mode** (default).
- Mid-run switching: user says "切换自动模式" / "切换手动模式" to switch; overlay mid-run switch is 「切换 ai-proxy」 / "switch to ai-proxy".
- Manual: pause at each stage exit for user confirmation. Auto: proceed end-to-end, pausing only at workflow-defined limits (e.g. review-loop cap).

## ai-proxy overlay (not a third control-flow mode)

Hosts that list ai-proxy triggers in `description` recognize an **overlay** on top of manual/auto:

- 「ai-proxy 模式」「AI 代理模式」 / "ai-proxy mode" request overlay; 「切换 ai-proxy」 / "switch to ai-proxy" switches mid-run.
- Overlay maps to **auto carrier** plus **pending** `Stage-exit policy: ai-proxy` (verbal trigger is not occupancy; freeze writes the policy). Occupancy and thin freeze live in `ai-proxy-discipline` — this skill MUST NOT restate the charter.
- If both an auto trigger (「自动*」) and an overlay trigger appear, **overlay + freeze wins** over naked auto (named-escape pass-through).
- On full-flow completion or any interruption, overlay reverts to manual **and** clears `Stage-exit policy` (same revert table as auto). Re-entering overlay requires an explicit trigger. Implicit continuation — "继续", "再改一下", "深入分析" — MUST NOT re-activate overlay.
- Hosts whose `description` omits ai-proxy triggers (including `write-workflow`) MUST ignore overlay; 「ai-proxy 模式」 does not change their two-state recognition.

## Core rule: auto always reverts to manual

Auto mode **automatically reverts to manual mode** when:

| Scenario | Note |
|----------|------|
| Full flow completes normally | Including the case where a new cycle is decided — a new cycle starts in manual by default |
| Flow is interrupted in any way | Failure abort, user-initiated stop, termination after a review-cap pause |

The workflow-specific completion point (e.g. PR merged, archive done) is defined by each workflow's own differences block, but the revert rule itself is universal.

## Re-entering auto mode: explicit only

After reverting to manual, re-entering auto mode requires an **explicit trigger**:

- "自动 xxx" / "自动分析" / "自动解决" / "切换自动模式"

Implicit continuation — "继续", "再改一下", "深入分析" — **must NOT** re-activate auto mode.

## Batch scenarios

In batch orchestration (e.g. `goal-driven-queue`; `jira-fix-queue` / `opsx-jira-fix-queue` are trigger shells that enqueue into it), the orchestrator passes **`Stage-exit policy` (and thus overlay vs auto vs manual) explicitly per sub-invocation**. The single-run revert rule above does not propagate across sub-invocations.

## Integration guide (for referencing workflows)

- **Keep in your own body**: your trigger-word table (triggers differ per workflow), the manual/auto stop-point summary per stage, and a **workflow-specific differences** block.
- **Delegate to this skill**: the revert-to-manual core rule, explicit re-entry, implicit-continuation prohibition, the batch rule, and overlay recognition (if the host lists ai-proxy triggers). Do NOT copy their full text inline. Do NOT copy the `ai-proxy-discipline` charter here.
- **Differences block examples** (stay in the workflow, never move here): `--retry` resets to manual; `--resume` keeps the checkpoint mode; validation-failure rollback keeps mode within N attempts; archive failure counts as interruption.
