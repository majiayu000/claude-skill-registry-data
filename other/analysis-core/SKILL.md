---
name: analysis-core
version: "1.3.0"
user-invocable: false
description: "Shared analysis-stage methodology for PDCA fix workflows: temporary-change permission and rollback gate, red-capable reproduction loop before hypothesis lists (user-pasted evidence excluded), instrumentation-debug with runtime-evidence-debug as default entry, analysis step skeleton (existence → research routing → phenomenon/locate/root-cause/upstream-eval/impact), mandatory analysis gate output block, and debug-verify loop. Parameterizes the post-analysis exit as {next-stage}. Referenced by PDCA hosts via frontmatter dependencies. Triggers — 「分析阶段核心」「分析核心」「临时改动门控」「红环门控」「打点调试门控」「调试验证闭环」「分析门控」 / analysis stage core, red-capable loop gate, temp-change gate, instrumentation debug gate, analysis gate output block, debug-verify loop."
dependencies:
  - known-issue-research
  - runtime-evidence-debug
  - browser-debug-toolkit
  - hybrid-debug
  - upstream-dependency-debug
---

# Analysis Core

> Internal shared skill. Single source of truth for **analysis-stage methodology** used by PDCA fix workflows. Workflows keep their own orchestration (exits, manual/auto mode, OpenSpec/Jira artifact sinks, intentional divergences).
>
> **Prerequisite check**: this skill declares strong dependencies in frontmatter. On load, verify each is available; if any is missing, abort and print the install command (`npx skills add FuDesign2008/open-skills -g --skill '*' --yes`). No silent fallback.

## Placeholder contracts

This skill is shared by workflows with different stage numbering. Never hardcode a workflow's stage numbers or titles here.

| Placeholder | Meaning | Who maps it |
|-------------|---------|-------------|
| `{next-stage}` | Stage to enter after analysis exit gate / after instrumentation resolves | Referencing workflow, at the reference line (number + name) |
| `{root-cause step}` / `{impact-assessment step}` / `{upstream-eval step}` | Step numbers inside the analysis stage for `known-issue-research` | Same reference line (existing known-issue-research contract) |

## 1. Temporary-change permission and rollback gate

Analysis is read-only by default. Analysis-assist edits only are allowed; they must be registered and fully rolled back before entering `{next-stage}`. Fix implementation belongs in the workflow's execution stage — not here.

**Allowed (analysis-assist only):**
- Instrumentation, temporary logs, reproduction scripts
- Hypothesis-validation edits (e.g. flip a condition to observe behavior) — restore after validation

**Forbidden:** edits whose purpose is to implement the fix.

**Register (mandatory):** for every temporary edit, record immediately: file + location + original content + purpose (rollback basis).

**Exit gate (must complete before `{next-stage}`):**
1. Restore originals one-by-one from the register (**register is authoritative**; `git diff` only helps confirm register items are clear — the worktree may already have user edits)
2. Output「临时改动清单 + 回滚验证」
3. If anything remains unrolled-back, do not enter `{next-stage}`; keeping an edit requires explicit user confirmation
4. Close the stage output with the §5 analysis gate output block (its temporary-changes line carries this list)

**Tool limits (analysis stage):** ✅ Read/Grep/SemanticSearch; ✅ WebSearch (research routing / quick search / upstream-eval / `runtime-evidence-debug` escape hatch); ✅ Edit/Write only for analysis-assist edits above; ✅ Bash for read-only verification commands — running the app under debug or reproduction steps still needs user confirmation (see §3).

## 2. Analysis step skeleton

1. **Existence check** (gate — always first)
   - Locate relevant code with Read/Grep/SemanticSearch
   - Act on the verdict:

   | Verdict | Action |
   |---------|--------|
   | ✅ Problem exists | Continue to step 2 → 3–8 |
   | ❌ Problem gone | Report it may already be fixed or logic changed, cite locations, **stop and wait for user** |
   | ⚠️ Description mismatches code | Report the mismatch, **return to the workflow's problem-clarification stage** |

2. **Research routing** — load `known-issue-research` and follow it (triage + known-issue quick search + industry-wide evaluation). The referencing workflow's reference line supplies `{root-cause step}` / `{impact-assessment step}` / `{upstream-eval step}` maps. Report templates: `known-issue-research/reference.md`. When the expected outcome is a result the user can see or operate, load `competitive-research` and run its lean layer-selected path before that behavior is treated as confirmed. The question names the user action and the observable result. When that behavior will be adopted as the target, include repeat, step back one level, reach zero, and interaction with an already shipped behavior. Do not restate that skill's method. If the load fails, abort with the install command. When the outcome is not user-visible, skip this load.

3. **Phenomenon** — reproduction conditions/steps; when the issue is browser-reproducible, prefer `browser-debug-toolkit` to reproduce and observe runtime state (not limited to UI/CSS/DOM; follow that skill's degradation path if browser automation is unavailable).

4. **Locate** — file paths + line numbers, key functions/classes.

5. **Red-capable loop gate** (before multi-hypothesis root-cause guessing)
   - A **red-capable loop** = a deterministic, agent-runnable failing reproduction (command, test, or equivalent observed failure) that has **already been run at least once** in this analysis stage and observed red/failing.
   - A user-reported symptom (pasted log, verbal description, screenshot) does **not** count as an agent-observed red.
   - **If missing:** do **not** emit a speculative multi-hypothesis “likely root causes” list. First establish the loop (repro steps, instrumentation per §3). If no agent-runnable loop can be established, the escape MUST land as an explicit user handoff — instrumentation and reproduction steps handed to the user per `runtime-evidence-debug`'s human-AI division — or a stop with the gap stated; never a silent pass.
   - **If present:** proceed to step 6. The stage output closes with the §5 analysis gate output block (red-loop line included).

6. **Root cause** — data flow and call-chain analysis; falsifiable hypotheses only after step 5 is satisfied.

7. **Upstream dependency fix evaluation** (optional) — when root cause is an upstream dependency bug, or step 2 found an upstream fixed version: load `upstream-dependency-debug` and follow it. Outcomes: low-risk upgrade → recommend upgrade in solution exploration; risky → list upgrade alongside workarounds; unfixed → workaround marked temporary.

8. **Impact** — affected modules/features.

If existence fails or description mismatches, do not proceed to solution exploration.

### Analysis-stage red flags

- Research route is 🔵/🟣 but known-issue quick search is skipped; or 🟢 with quick-search triggers hit yet WebSearch is skipped for “read code first”
- Named third-party lib/framework in the root cause without checking upstream Changelog/Release Notes before piling workarounds
- Using “analysis” to ship a fix — temporary edits beyond hypothesis validation, or entering `{next-stage}` without rollback
- Temporary edits not registered, or missing「临时改动清单 + 回滚验证」before `{next-stage}`
- Emitting multi-hypothesis root-cause guesses **without** a red-capable loop (or an explicit, user-visible statement that no loop is possible)

## 3. Instrumentation debug (runtime observation — default entry)

**State-based triggers** (any one; prefer before entering `{next-stage}`):
- Static analysis stalled — module roughly known, concrete mechanism or path unconfirmable by reading code
- Retry/continue — a fix based on static analysis was applied and the problem remains
- Silent failure — call chain and logs look correct but behavior is wrong
- Fix verification needs before/after runtime evidence

**Default entry**: when any trigger fires, load `runtime-evidence-debug` first and follow its lifecycle (escalation decision → instrumentation design → reproduction → evidence tiers → confidence gating → escape hatch → fix verification). Entry is a state judgment ("runtime observation is needed"), not a self-assessed confidence verdict; the skill's own static-first escalation decision remains authoritative.

**Scenario composition** (on demand; each keeps its own authority):
- Browser-reproducible → instrumentation delegates tool selection to `browser-debug-toolkit`; if the phenomenon step already did browser repro, continue here only if static analysis still stalls
- Hybrid app (native shell + WebView/WKWebView/Electron + H5) → consult `hybrid-debug` for layer localization before instrumenting
- Real-device observation → compose channel enablers (e.g. `android-webview-debug` to establish the connection); `runtime-evidence-debug` decides what to observe, evidence tier, and when confidence suffices

Execution details, confidence gating, and escape hatches live in each skill's current SKILL.md — read before invoking.

**Tool limits:** ✅ Read/Grep to choose instrumentation sites; instrumentation and validation edits follow §1 (AI may add instrumentation and must register it); ❌ do not run reproduction steps without user confirmation.

## 4. Debug-verify loop (verification stage)

When the analysis stage used a debug skill to find the root cause, the workflow's verification stage MUST use the **same** skill to verify the fix (not tests alone):

- Browser-reproducible (`browser-debug-toolkit`) → same skill; before/after runtime state (DOM / computed style / box model / console / network); confirm the anomaly is gone
- Runtime evidence (`runtime-evidence-debug`) → re-check original instrumentation sites; before/after evidence; confirm abnormal behavior is gone
- Hybrid (`hybrid-debug`) → verify affected layers (L1–L4); no new cross-layer side effects

## 5. Analysis gate output block (mandatory stage-closing block)

Single source of truth for the block that MUST close every referencing workflow's analysis-stage output before entering `{next-stage}`. Workflows reference this block with a thin pointer; they never restate its fields.

```
【Analysis gate / 分析门控】
Red loop: ✅ <command + one-line red evidence observed this stage> / ❌ <why unestablished + handoff already proposed: instrumentation/repro steps handed to the user>
Debug entry: runtime-evidence-debug loaded (trigger: static stalled / retry / silent failure / before-after verification) / not needed (one-line Tier 1–2 evidence)
Scenario supplements: browser-debug-toolkit / hybrid-debug / channel enabler (e.g. android-webview-debug): engaged(<which>) / not needed
Temporary changes: none / <registered list + rollback verified>
```

Rules:

- A missing or unfilled block blocks entry to `{next-stage}` — filling it is the entry condition, and being unable to fill a line (e.g. red loop) is itself the escalation signal.
- "Not needed" fills are legal but require their one-line evidence; blank or evasive fills are not.
- Red-loop line follows §2 step 5 (user-pasted evidence does not satisfy it); debug-entry line follows §3 (state-based trigger).

## Integration guide (for referencing workflows)

- **Declare** `analysis-core` in frontmatter `dependencies`; abort at workflow startup if missing.
- **Thin reference shape (preferred):** one short「委托 `analysis-core`」block with `{next-stage}` + known-issue-research step maps (number + name only); do **not** restate §§1–3 prose or re-list the analysis step skeleton.
- **Keep in the workflow body:** orchestration only — exits/mode, OpenSpec/Jira sinks, intentional divergences (形似神异), difficulty/path tables.
- **Verify stage:** one line pointing at §4 — do not paste debug-verify bullets.
- **reference.md:** point to this skill for methodology; keep workflow-specific output templates; do not duplicate gate prose.
- **Do not** sink intentional divergences (coverage-gate strength, test-suite-ensure blocking, industry-eval Jira gate, etc.) into this skill.
