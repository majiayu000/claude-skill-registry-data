---
name: aid-discover
description: >
  Populate the Knowledge Base from a codebase that already exists. Use this skill when you
  are starting AID on a project with existing code, and its architecture, conventions, and
  patterns need to be written down before any later phase can rely on them. It reads all
  repository content -- code, configuration, and documentation -- drafts the KB documents,
  reviews them, asks you what it could not infer, fixes what it finds, and takes your
  approval. It advances one step per run, so you can stop and resume. Run `/aid-config`
  first to scaffold the KB.
allowed-tools: Read Glob Grep Bash Shell Terminal Write Edit Agent
argument-hint: "[--grade A] minimum acceptable grade (default: A)  [--reset] clear KB and restart"
---

# Brownfield Project Discovery

Analyze an existing project repository — all code, configuration, and documentation — and
produce a structured `.aid/knowledge/` directory by orchestrating 5 specialized discovery subagents.
Includes a built-in quality gate that reviews, grades, and fixes KB documents.

**State machine — each `/aid-discover` invocation drives the state machine until it hits a natural pause point per [`.aid/runtime/templates/state-machine-chaining.md`](../../aid/templates/state-machine-chaining.md). Mechanical states and inline-question states auto-chain; only PAUSE-FOR-USER-ACTION, PAUSE-FOR-USER-DECISION, and HALT stop the run.**

---

## ⛔ PRIME DIRECTIVE: NO ASSUMPTIONS — DEFER TO THE USER

**This rule governs every state, every sub-agent, and the orchestrator itself. It overrides
convenience, speed, and confidence.**

Discovery's job is to report **what the project actually is**, never what an agent *guesses* it
is. So whenever ANYTHING is unclear, ambiguous, contradictory, or a judgment call — an
undefinable term, a discrepancy between two sources, an uncertain classification, which of two
things is authoritative, in-or-out-of-scope, how to resolve a conflict — **DO NOT resolve it by
assumption. Record a question and DEFER the decision to the user.**

- A `LIKELY` / `UNCERTAIN` / `probably` / "I'll assume" answer written into the KB is a
  **FAILURE**, not a finding. Turn it into a Q&A entry.
- Never silently reconcile a contradiction — record both sides and **ask** which is right.
- State a fact only when you can ground it from the artifacts **with certainty** (cite the
  source). Otherwise, **ASK.**

**The deferral machinery is already built in — use it:** the Step 0cx (domain), 0d (doc-set),
0f (path), and Step 5c (term-exclusion) gates are PAUSE-FOR-USER-DECISION points; sub-agents
write open questions to `.aid/knowledge/.scout-questions.tmp`; Step 6b consolidates them into
`STATE.md ## Q&A (Pending)`; and the **Q-AND-A** state resolves them *with the user* before
approval. Every disambiguation flows through this path — none is decided silently.

**Why:** AID is used by people who distrust AI. One unconfirmed assumption presented as fact
reads as hallucination and breaks that trust. Visible deference — "here is what I found, here is
what I am unsure of, **you** decide" — IS the product. **When in doubt, ASK.**

---

## ⚠️ Pre-flight Checks

Run `bash .aid/runtime/scripts/kb/discover-preflight.sh .aid/knowledge/` to verify:
1. `.aid/knowledge/STATE.md` is present and non-empty (self-created from template if absent)
2. Not in Plan Mode (subagents need write access)

Check 1 is now self-healing: if STATE.md is absent the script creates it from
`discovery-state-template.md` and continues — no "run /aid-config first" hard-stop.
The check only fails (exit 1) if STATE.md cannot be written or is empty after the
self-create attempt (e.g. a zero-byte file left by a prior interrupted run).
If Check 2 fails: Tell user to press `Shift+Tab` to exit Plan Mode, then re-run.

---

## ⚠️ Pre-flight Cleanup (orchestrator-only — never grade these)

**Before dispatching the REVIEW reviewer, sweep the KB for mechanical drift that should never appear as a "finding".** These are housekeeping items the orchestrator owns; they pollute reviewer attention and burn cycles if left for the reviewer to surface.

**Sweep categories (auto-correct silently):**

- **Volatile-citation drift** — replace any bare `file:LINE` citation or inline line-count with a durable anchor (file path + grep-recoverable symbol/heading), per kb-authoring P1(d). Durable anchors don't rot, so this sweep shrinks every cycle.
- **Aggregate counts** — per-skill or per-tree file/script/reference totals computed from current disk state (`find ... | wc -l`).
- **Path & citation hygiene** — bare citations missing skill prefix (`SKILL.md` → `.agents/skills/<skill>/SKILL.md`); references to files that no longer exist.
- **Math** — verify any `%` calculations using real values (e.g., "X% over Y" assertions). If the underlying numbers changed, recompute.
- **Ghost references** — once confirmed a file/feature was removed, delete references to it (don't leave "(retired)" or "(see below)" stubs in current-state docs; historical change-log entries are fine).
- **Meta-doc counting** — `INDEX.md` / `README.md` feature counts and file-type tallies (line counts are not stored — see Volatile-citation drift above).

**Out of KB scope — never check, never claim:**

- **The installed tree at the repo root** (`.aid/runtime/` and the skill mirror under `.agents/skills/`, placed by the CLI install) — this is the **dogfood install** (AID applied to AID itself), conceptually identical to any user's install after the CLI install. The KB makes **no claims** about it. Byte-identity comparisons are scoped to the **canonical sources and the release payload built from them**, NOT the installed copies.

**Why pre-flight cleanup matters:**
- Reviewer focus should be **semantic** quality (missing post-merge content, internal contradictions, factually wrong claims that mislead downstream phases) — not arithmetic drift.
- Sweeping these first lets the reviewer score the KB on what actually matters.
- Edits in this sweep should be **manual one-by-one** (not regex scripts). Scripts generalize and produce new defects (replacing historical-narrative values, mangling section headers via context-bleed, embedding authoring annotations as user-facing prose, missing inline variants the anchor didn't anticipate). Each edit should see its full surrounding context.

> **State machine for this skill:**
> ```
> aid-discover  ▸ one step per run
>   [ ELICIT ] → [ GENERATE ] → [ REVIEW ] → [ Q-AND-A ] → [ FIX ] → [ APPROVAL ] → [ DONE ]
> ```
> Each run detects which state to enter from disk and does exactly that step.

## Arguments

| Argument | Effect |
|----------|--------|
| `--grade X` | Set minimum acceptable grade. Format: `[A-F][-+]?` (e.g., A, A-, B+). Default: `A`. Persists in `.aid/knowledge/STATE.md`. |
| `--reset` | Clear entire `.aid/knowledge/` directory and restart from scratch. |

**Grade persistence:** Saved to `.aid/knowledge/STATE.md` on first run. `--grade` updates it; omitting it reads the stored value.

---

## Dispatch Protocol (L1+L2+L3 subagent visibility)

Every subagent dispatch in this skill MUST follow this protocol so the user
sees mid-wait progress instead of going silent for 10–25+ minutes. The full
protocol lives in two reference docs; this section is a checklist citing them.

**Before each dispatch:**

1. **Look up ETA** in `.aid/runtime/templates/rough-time-hints.md` for the
   subagent's operation class. Capture LOW–HIGH band.
2. **Read heartbeat config** via
   `bash .aid/runtime/scripts/config/read-setting.sh --path traceability.heartbeat_interval --default 1`
   (resolves from `.aid/settings.yml`; default 1; `0` = disabled).
3. **Pre-create heartbeat file** (always — unconditional):
   - Pre-create `.aid/.heartbeat/<agent-name>-<unix-ts>.txt`
   - Include `HEARTBEAT_FILE=<path>` + `HEARTBEAT_INTERVAL=Nm` in dispatch prompt with explicit instruction to update during long phases
   - SKIP only if `traceability.heartbeat_interval: 0` (user-explicit opt-out in `.aid/settings.yml`)
4. **Arm 3 L2 timers as SEPARATE background dispatches** (always — even for short ETAs use minimums 60s/120s/180s; never gate on ETA). Each timer is its OWN `Bash(..., run_in_background=true)` call:
   - Call A: `sleep <min(LOW/2, 270) in s> && echo "... <agent> still running (Xm elapsed of ~LOW–HIGH)"` — own background dispatch
   - Call B: `sleep <min(LOW, 540) in s> && echo "... <agent> at estimated time (LOWm elapsed)"` — own background dispatch
   - Call C: `sleep <min(1.5×LOW, 810) in s> && echo "⚠️ <agent> EXCEEDED estimate (1.5×LOWm elapsed); consider checking on it or cancelling"` — own background dispatch
   - **Keep-warm re-arm:** when the last timer fires and the sub-agent is still running, arm one more `sleep 270 && echo "... <agent> still running (Xm elapsed)"` (own background dispatch), and again on each fire, until the completion notification arrives. Every fire is a request that re-reads the cached context and refreshes its 5-minute prompt-cache TTL; a silent gap over 5 minutes re-writes the whole context at full price.
   - ⚠️ **DO NOT chain timers with `&` inside a single wrapper Bash call.** If you do, the wrapper exits when the last `&` is queued, orphaning the sleeps — their stdout is silently lost and you'll never see the timer fire. Each timer needs its own `run_in_background: true` task so the harness can track and notify on completion.

**During dispatch:**

- **On L2 timer fire:** surface the timer output. If heartbeat file exists,
  also read it and append `[from heartbeat] state: <state> · progress: <progress>
  · activity: <activity>` to the narration.

**On completion / failure:**

- **Success:** emit `✓ <agent> done in <actual>` with measured time. This skill's own
  dispatches are not task-scoped, so they have no persisted target: the work-level
  Calibration Log / Dispatches views are derived solely from per-task `dispatch_log`
  entries (`work-state-template.yml`), which discovery's dispatches never populate.
  The console line above is the sole record. Mandatory wherever a target exists
  (never optional, never "if tracked"). Delete heartbeat file.
- **Failure:** emit `✗ <agent> FAILED after <elapsed> (reason: <one-line>)`.
  Decide whether to re-dispatch, fall back, or surface to user. Delete
  heartbeat file.

**References:**

- `.aid/runtime/templates/long-wait-protocol.md` — full L2 spec
- `.aid/runtime/templates/subagent-heartbeat-protocol.md` — full L3 spec
- `.aid/runtime/templates/rough-time-hints.md` — current measured ETAs
- `aid-*` agent definitions, `## Heartbeat protocol` section — subagent-side contract

The existing `▶ <agent> starting (~<ETA>)` and `✓ <agent> done` bracket-pair
lines elsewhere in this skill body remain in place; this protocol just makes
them more informative by adding mid-wait check-ins + structured progress.

---

## State Detection

State detection reads the files on disk, every run. Nothing remembered from an
earlier run or from this conversation counts as state, because the files may
have changed since.

Read the filesystem to determine which mode to enter:

```
State 0: `## Discovery Elicitation` absent, or `**Resolved:** no` → ELICIT mode
State 1: Missing or empty KB docs                     → GENERATE mode
State 2: All docs populated, no GRADE file             → REVIEW mode
State 3: GRADE file, ANY Pending Q&A (regardless of grade/Impact) → Q-AND-A mode
State 4: GRADE file, grade < min, ZERO Pending Q&A     → FIX mode
State 5: GRADE file, grade >= min, ZERO Pending Q&A,
         not user-approved                              → APPROVAL mode
State 6: GRADE file, grade >= min, ZERO Pending Q&A,
         user-approved                                  → DONE
```

**Detection logic:**

0. Check `.aid/knowledge/STATE.md` for a `## Discovery Elicitation` block. If it is absent, or
   present with `**Resolved:** no`, this cycle's elicitation is not yet resolved → **ELICIT**
   (State 0); do not evaluate States 1–6 below until it resolves. Once the block carries
   `**Resolved:** yes`, detection falls through to the ladder below unchanged — ELICIT runs
   exactly once per cycle (`--reset` clears the block).
1. Check `.aid/knowledge/` for the documents in the project's declared doc-set
   (read via `read-setting.sh --path discovery.doc_set` → list-filenames accessor,
   `references/doc-set-resolve.md` §2.1; default seed when the section is unset).
2. A document is "populated" only if it contains real content (files with only `❌ Pending` = missing). If any are missing → **GENERATE**
3. If all declared docs populated and `.aid/knowledge/STATE.md`'s `kb_grade` frontmatter scalar (or the legacy `**Current Grade:**` header-blockquote line, for an un-migrated file) is `Pending` or absent → **REVIEW**
4. If all declared docs populated but no `.aid/knowledge/STATE.md` → **REVIEW** (legacy)
5. If `.aid/knowledge/STATE.md` exists with a grade:
   - Read current/minimum grade (`kb_grade` frontmatter scalar, legacy `**Current Grade:**` fallback); if `--grade` provided, update minimum
   - Read `## Q&A (Pending)` section of `.aid/knowledge/STATE.md` for `**Status:** Pending` entries
   - **If ANY `**Status:** Pending` entry exists → Q-AND-A** (regardless of grade OR Impact —
     discovery is NOT complete while any question is unanswered; `Impact` only orders the work,
     it never gates completion). Q-AND-A self-answers every question it can CONFIRM from source
     (no assumptions) and asks the user the rest, until ZERO remain Pending.
   - Else (ZERO Pending Q&A): if grade < minimum → **FIX**; if grade >= minimum →
     `**User Approved:** yes` → **DONE**, otherwise → **APPROVAL**.

**Grade ordering** (highest to lowest):
`A+, A, A-, B+, B, B-, C+, C, C-, D+, D, D-, E+, E, E-, F`

Print the state-entry line with description, then the "you are here" state-map. Use one of these depending on the detected state:

**ELICIT:**
```
[State: ELICIT] — Capture the project's external sources and tool integrations before GENERATE runs.
aid-discover  ▸ you are here
  [● ELICIT ] → [ GENERATE ] → [ REVIEW ] → [ Q-AND-A ] → [ FIX ] → [ APPROVAL ] → [ DONE ]
```

**GENERATE:**
```
[State: GENERATE] — Populate missing KB documents by orchestrating parallel discovery sub-agents.
aid-discover  ▸ you are here
  [✓ ELICIT ] → [● GENERATE ] → [ REVIEW ] → [ Q-AND-A ] → [ FIX ] → [ APPROVAL ] → [ DONE ]
```

**REVIEW:**
```
[State: REVIEW] — Grade all KB documents for accuracy, completeness, and evidence quality.
aid-discover  ▸ you are here
  [✓ ELICIT ] → [✓ GENERATE ] → [● REVIEW ] → [ Q-AND-A ] → [ FIX ] → [ APPROVAL ] → [ DONE ]
```

**Q-AND-A:**
```
[State: Q-AND-A] — Resolve pending questions with the user before attempting automated fixes.
aid-discover  ▸ you are here
  [✓ ELICIT ] → [✓ GENERATE ] → [✓ REVIEW ] → [● Q-AND-A ] → [ FIX ] → [ APPROVAL ] → [ DONE ]
```

**FIX:**
```
[State: FIX] — Apply Q&A answers and reviewer feedback to bring KB documents up to minimum grade.
aid-discover  ▸ you are here
  [✓ ELICIT ] → [✓ GENERATE ] → [✓ REVIEW ] → [✓ Q-AND-A ] → [● FIX ] → [ APPROVAL ] → [ DONE ]
```

**APPROVAL:**
```
[State: APPROVAL] — KB meets minimum grade; ask the user to confirm it is ready for Interview.
aid-discover  ▸ you are here
  [✓ ELICIT ] → [✓ GENERATE ] → [✓ REVIEW ] → [✓ Q-AND-A ] → [✓ FIX ] → [● APPROVAL ] → [ DONE ]
```

**DONE:**
```
[State: DONE] — Discovery is complete and user-approved; KB is ready for Interview.
aid-discover  ▸ you are here
  [✓ ELICIT ] → [✓ GENERATE ] → [✓ REVIEW ] → [✓ Q-AND-A ] → [✓ FIX ] → [✓ APPROVAL ] → [● DONE ]
```

---

## Dispatch

| State | Detail | Worker | Advance |
|-------|--------|--------|---------|
| ELICIT | `references/state-elicit.md` | inline | → GENERATE |
| GENERATE | `references/state-generate.md` | `aid-architect` | → REVIEW |
| REVIEW | `references/state-review.md` | `aid-architect` | → Q-AND-A |
| Q-AND-A | `references/state-q-and-a.md` | inline | → FIX |
| FIX | `references/state-fix.md` | `aid-architect` | → APPROVAL |
| APPROVAL | `references/state-approval.md` | inline | → halt |
| DONE | `references/state-done.md` | inline | → halt |

> **Sub-agent fanout (GENERATE):** The `aid-architect` Worker for GENERATE dispatches
> discovery sub-agents internally — `aid-researcher` (Step 1 pre-scan, sequential), then
> four `aid-researcher` instances parameterized by doc-set in parallel (Steps 2–5). The full
> fanout protocol is documented inside `references/state-generate.md`. The Dispatch Protocol above
> (L1+L2+L3 visibility) applies to all sub-agent dispatches.

> **REVIEW scope (semantic only).** The REVIEW reviewer's job is to grade
> **semantic quality** — missing post-merge content, internal contradictions,
> factual claims that would mislead a downstream phase (architecture,
> module-map, coding-standards weighted highest). **Mechanical drift is OUT
> of scope** — volatile-citation drift, aggregate counts, path/citation
> hygiene, math arithmetic, ghost references, meta-doc counting are
> orchestrator-side **Pre-flight Cleanup** (above), swept BEFORE the
> reviewer is dispatched. The reviewer should never need to flag mechanical
> drift as a finding; if it does, the pre-flight sweep was incomplete.

> **FIX parallelism (parallel-agent dispatch when independent).** The
> `aid-architect` Worker for FIX **partitions the reviewer's findings by KB
> file** and dispatches **one sub-agent per affected file** (typically
> `aid-tech-writer` for KB docs, or `aid-researcher` if depth is needed). All agents
> run in **parallel** — single message with multiple `Agent` tool calls.
> Each agent's prompt contains only that file's finding list and a clear
> manual-edits directive (no regex scripts — scripts generalize and produce
> new defects). Each agent commits-stages its file's changes only. After
> ALL agents return, the orchestrator runs a **sequential aggregate step**:
> regenerate-and-confirm generated files (per `state-fix.md` Step 3-4),
> then a single `git commit` + `git push`. The serial constraint exists
> only at the commit/push boundary; the edits themselves are
> parallel-safe because each file has exactly one writer. Semantic
> re-verification of the changes is the next cycle's REVIEW state job.

On state entry, print `[State: NAME]` + the "you are here" map from State Detection above.
When a state completes, route by its `**Advance:**` type (per [`state-machine-chaining.md`](../../aid/templates/state-machine-chaining.md)):
- **CHAIN** → begin the next state's reference doc within the same invocation; no exit.
- **PAUSE-FOR-USER-ACTION** / **PAUSE-FOR-USER-DECISION** → print the pause reason + resume command and exit.
- **HALT** → print the closing summary and exit.

---

## Targeted Discovery (Re-entry)

When a Q&A entry in `.aid/knowledge/STATE.md` or an IMPEDIMENT triggers re-discovery:

1. Read the Q&A entry in STATE.md `## Q&A (Pending)` or the IMPEDIMENT to understand what's missing
2. Identify which subagent owns the document using the `owns-<agent>` accessor
   from the project's declared doc-set (`references/doc-set-resolve.md` §2.1):

   ```bash
   raw="$(bash .aid/runtime/scripts/config/read-setting.sh \
           --path discovery.doc_set 2>/dev/null || true)"
   # owns-<agent>: which files does a given agent own in THIS project?
   resolve_doc_set "$raw" | awk -F'\t' -v a="<agent-name>" '$2==a{print $1}'
   ```

   The declared set is the single authority on ownership. For the default seed
   (no `discovery.doc_set` override), the ownership resolves as follows
   (illustrative — actual ownership is always driven by the declared set):

   | Sub-agent | Default-seed KB documents |
   |---|---|
   | `aid-researcher` (pre-scan) | project-structure.md, external-sources.md |
   | `aid-researcher` (architecture doc-set) | architecture.md, technology-stack.md |
   | `aid-researcher` (analyst doc-set) | module-map.md, coding-standards.md, schemas.md |
   | `aid-researcher` (integrator doc-set) | pipeline-contracts.md, integration-map.md, domain-glossary.md |
   | `aid-researcher` (quality doc-set) | test-landscape.md, tech-debt.md, infrastructure.md |
   | orchestrator (no sub-agent) | feature-inventory.md, README.md, INDEX.md |

3. Dispatch ONLY the relevant subagent
4. Regenerate README.md and INDEX.md
5. Update README.md revision history
6. Reset the `kb_grade` frontmatter scalar in STATE.md to `Pending` (`bash .aid/runtime/scripts/summarize/writeback-state.sh --set kb_grade Pending`) so next run re-reviews
7. Report completion

---

## Quality Checklist

- [ ] No overlap between KB documents
- [ ] Claims grounded in code evidence (file paths + grep-recoverable symbol/heading anchors, not bare line numbers)
- [ ] Inferred info marked with ⚠️
- [ ] `.aid/knowledge/STATE.md` Q&A captures everything needing human input
- [ ] external-sources.md documents all sources (or states none provided)
- [ ] README.md reflects completeness and revision history
- [ ] INDEX.md has 2-3 line summaries per document
- [ ] the declared C9 capability/feature doc exists (e.g., feature-inventory.md, or capability-inventory.md / content-inventory.md per the domain doc-set) (template or populated)
- [ ] AGENTS.md placeholders filled with discovered data
- [ ] All issues have severity: [CRITICAL], [HIGH], or [MEDIUM]
- [ ] Minimum 10 spot-checks in `.aid/knowledge/STATE.md` `## Verification Spot-Checks`

---

## Grading Criteria

| Grade | Meaning |
|-------|---------|
| A+ | Exceptional — comprehensive, accurate, evidence-rich, immediately useful |
| A | Thorough — covers expected scope with solid evidence |
| B+ | Good — minor gaps or missing details that don't block work |
| B | Adequate — covers basics but lacks depth in important areas |
| B- | Shallow — lists things without explaining patterns or relationships |
| C+ | Significant gaps — missing important sections or inaccurate in places |
| C | Barely useful — agent would need to re-discover most information |
| D | Misleading — wrong information that could cause bad decisions |
| F | Missing or empty |

**Overall grade** = weighted average where architecture, module-map, and coding-standards
count double (referenced most by downstream phases).

---

## Document Expectations

Read `references/document-expectations.md` for the full expectations per document,
including "Must have" and "Red flags" for each declared KB document plus meta-documents.
