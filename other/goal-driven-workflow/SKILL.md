---
name: goal-driven-workflow
version: "0.10.0"
user-invocable: true
description: "Goal-Driven long-run workflow: run an agent autonomously for hours toward a verifiable goal. Five stages — ① deep intake interview & output contract (approach frozen before launch) ② layer acceptance criteria + design the /goal condition (measurable end state, stated check, constraints, turn/time cap) ③ sub-agent division & context management (context-rot mitigation) ④ launch the long run (/goal, claude -p non-interactive, or manual-loop fallback) ⑤ completion report & human acceptance. Built on top of Claude Code's native /goal harness, with a generic fallback for environments without /goal. Triggers — 「goal 长跑」「goal run」「goal-driven」「目标驱动长跑」「一个 goal 下去跑」「长跑目标」「无人值守跑任务」「goal-run」 / goal run, goal-driven, long-run goal, autonomous run, run until done."
dependencies:
  - report-output-discipline
  - clarifying-question-discipline
  - completion-evidence-discipline
  - design-approval-gate
  - intake-interview-discipline
  - ai-proxy-discipline
  - context-budget-discipline
  - figma-pixel-implement
  - figma-pixel-verify
---

# Goal-Driven Long-Run Workflow

> Run an agent autonomously for hours toward a **verifiable** goal. Primary harness example: Claude Code's native `/goal` (condition + evaluator loop). This skill adds requirement alignment, acceptance layering, sub-agent context management, and post-run reporting — plus a generic fallback when `/goal` is unavailable.
> Stages 1–3 are read-only **design**; stage 4 is the run; stage 5 is reporting/acceptance. Default is manual mode (pause at each stage exit). On a **standalone** invocation, 「自动模式」/「自动跑」 / "auto mode" still pauses at stages 1–3 and at Stage 4 launch approval; it does not skip those confirms and does not start the harness. Queue-child invocations follow `Stage-exit policy` (see below).
> **Output templates**: [reference.md](reference.md).

## Invocation Conventions

- **Trigger words** (per `description`): 「goal 长跑」「goal run」「goal-driven」「目标驱动长跑」「一个 goal 下去跑」「长跑目标」「无人值守跑任务」「goal-run」 / goal run, goal-driven, long-run goal, autonomous run, run until done
- **Command form**: `/goal-driven-workflow xxx`, `/goal-run xxx`
- **Default behavior**: treat `xxx` as the task to run as a goal; enter stage 1 (clarify). If `xxx` already has a concrete verifiable goal + acceptance criteria, skip ahead to stage 2 after outputting Template 1 (frozen block or an explicit stage-1-N/A line) and obtaining one confirmation of it — that confirmation counts as stage 1 complete for Design-checked.
- **Not applicable**: single-step edits, tasks with no verifiable end state, or tasks better served by recurring `/loop`-style polling or plain single-turn auto approvals. Single-run tasks shaped for stage-gated PDCA (per-stage artifacts and verdicts rather than a run-to-completion loop) route to `solve-workflow` / `opsx-solve-workflow` directly — engine selection at dispatch belongs to the queue layer (`goal-driven-queue`).

## Strong dependencies

Frontmatter `dependencies`; prerequisite check must pass or the flow aborts:

- `report-output-discipline` — owns the derived HTML contract and the shared renderer
- `clarifying-question-discipline` — stage 1 clarification
- `completion-evidence-discipline` — stage 2/5 acceptance evidence
- `design-approval-gate` — standalone Stage 4 launch-approval pause that enters Armed (see long-run divergence below)
- `intake-interview-discipline` — stage 1 deep intake (fog-bounded interview → approach comparison → freeze → pre-launch self-review); stage 4 in-run self-answer rules; stage 5 ledger surfacing
- `ai-proxy-discipline` — proxy checkpoints (`Stage-exit policy: ai-proxy`): absent-mode intake Q&A, bounded contract approval (Arm, not Launch), stage 5 report check; abort only when a card carries that policy and the skill is missing
- `context-budget-discipline` — stage 3 context-plan quantification (compaction threshold / phase→reset-boundary map / ledger path) and stage-4 threshold checks at budget milestones
- `figma-pixel-implement` / `figma-pixel-verify` — required installed; load both when the goal text contains `figma.com` or `node-id=`, or the user asks for pixel restore

**Related (informational)**: `solve-workflow` (full PDCA); handbook §8 of `docs/7x24-agent-reliability-handbook.md`.

**Adapter**: the review/evidence pages come from the loaded `goal-driven-queue` skill. It is not a frontmatter dependency because the queue already depends on this workflow; its missing-adapter handling is in Stage 5.

## Prerequisite Skill Check

> Run at startup, before stage 1, against every strong dependency.

1. Scan available skills
2. All present → continue
3. Any missing → print the missing-dependency notice ([reference.md](reference.md) § Prerequisite Skill Check — Missing Notice) and **abort immediately**

> **No-downgrade**: missing strong dependency aborts — never silently simplify.

---

## Path Selection (lightweight)

Long-run scale is already expressed by the goal condition and budget in stage 2. For a single-file high-certainty change, keep stage 2/3 lean (one goal condition + minimal sub-agent planning); for multi-module / cross-domain work, plan sub-agent division and context technique in full. Stage 5 (report + human acceptance) is never skipped.

---

## Stage overview

| Stage | Tool permission | Manual stop | Required output |
|-------|-----------------|-------------|-----------------|
| 1 Clarify & output contract | ❌ Read/Write | ⛔ stop, wait confirm | restatement + Template 1 |
| 2 Acceptance + goal condition | ✅ Read; ❌ Edit/Write | ⛔ stop, wait confirm | Template 2 + 4-part condition |
| 3 Sub-agent division & context | ✅ Read; ❌ Edit/Write | ⛔ stop, wait confirm | Template 3 |
| 4 Launch the long run | ✅ Everything | standalone: ⛔ Armed, wait for Launch / queue child: start when card supplies the run | Template 4 + run log |
| 5 Report & acceptance | ✅ Bash; ❌ Edit/Write | ⛔ stop, wait confirm | Template 5 |

> Manual mode pauses at each ⛔. On **standalone** invocations, auto mode still pauses at stages 1, 2, 3, and the Stage 4 launch-approval pause (Armed); it does not start the harness until an explicit Launch instruction; stage 5 always ends with human acceptance. Queue-child invocations follow `Stage-exit policy` and do not enter the standalone Armed wait.

### Queue child vs standalone

This invocation is a **queue child** only when **this turn's** user/orchestrator dispatch message already **inlined** a frozen task card (at least the frozen-decisions block) as stage 1 input. Conversation history and on-disk `.goal-driven/` cards do **not** count. Do not scan `.goal-driven/queues/`. Do not require a `queue-child` flag the caller did not send. All other invocations are **standalone**.

### Standalone pre-run states

- **Design-checked**: stages 1–3 confirmed at the human seat **and** Stage 4 launch approval (final goal condition + budget + companion checklist) confirmed. Skip-ahead still needs Template 1 + one confirm (above).
- **Armed**: Design-checked is complete. Announce that the long run will not start until an explicit Launch instruction. Do not start Stage 4 execute.
- **Launch**: start Stage 4 execute only on 「开跑」 / "launch" / "start the run" / 「开始长跑」 (and obvious same-phrase translations). **Not** Launch: 「自动模式」 / 「自动跑」 / "auto mode"; bare 「好的」 / "ok" / 「继续」 / "confirm". After Launch, do not re-ask stages 1–4. Incomplete Design-checked **refuses** Launch and continues the remaining checks.
- Queue children skip this state machine; the card's recorded approval is the 留痕 for the launch-approval gate.

---

## Stage 1: Clarify Requirements & Output Contract

> ⚠️ Follow `clarifying-question-discipline` (one question per turn; multi-round until clear; clarify first, do not rush to answer).
> 🔒 Deep intake: **load `intake-interview-discipline`** and run its §A (deep interview → approach freeze → bounded pre-launch self-review). Its **presence tiers** govern depth: present (default) = per-decision questioning with high-impact escalation and the three-part base; declared/structural absence = once-confirm + full ledger, unchanged.
> 📦 **Optional traceability**: when the project has an `openspec/` directory and a usable openspec CLI (or equivalent), offer `traceability: openspec | none` as an intake decision — default off; project policy may mandate on; the user's explicit choice wins. Record it in Template 1.
> 🎭 **Stage-exit policy**: record `manual | ai-proxy | auto` in Template 1 (queue children inherit it from the card's interaction-budget ticket; it overrides trigger-word mode propagation). `proxy` = `ai-proxy-discipline` occupies the human seat at the enumerated checkpoints (absent-mode intake Q&A, contract approval as bounded pre-authorization **that Arms, not Launches**, stage 5 report check) under its charter; `manual` = manual mode pauses; `auto` = who answers mid-run questions (named escapes + §B). On standalone, `auto` MUST NOT skip stages 1–3 confirmation, MUST NOT skip the Stage 4 launch-approval pause, and MUST NOT count as Launch.

1. **Restate the goal**; extract goal / deliverables / constraints / expected outcome.
2. **Ask exactly ONE most critical question per turn** until no blocking fog remains (selection per `clarifying-question-discipline`; graduation per `intake-interview-discipline`). Prefer structured single-select with a recommended answer; fall back to prose if the host has no structured UI.
3. **Approach comparison & freeze** — per the loaded discipline, §A steps 4–6 (approach comparison → freeze → pre-launch self-review); the frozen-decisions block lands in Template 1 ([reference.md](reference.md) § Stage 1).
4. **Output contract**: agree on deliverable(s) and what "done" looks like.
5. **Pre-judge output vs outcome** (see stage 2): mark which standards the agent can self-verify (output-type) vs which need human judgment (outcome-type).
6. Fill **Template 1** ([reference.md](reference.md) § Stage 1), including the frozen-decisions block.

> **Unattended intake**: when the queue-child predicate holds, the inlined card's frozen decisions supply this stage; if that card has no frozen decisions, run the interview in self-answer mode (`intake-interview-discipline` integration guide §4) and flag every answer as an assumption. Standalone invocations MUST NOT complete Design-checked via self-answer — absent human-seat confirmation, refuse Launch.

**Red Flags**: dumping multiple clarifying questions/open points in one message; rushing to answer during clarification; rushing past clarification into the run; fuzzy "just make it good" goals; skipping scope/out-of-scope boundaries; launching without a frozen approach + self-review (deep-intake freeze skipped); treating on-disk `.goal-driven/` cards as queue-child supply.

---

## Stage 2: Acceptance Criteria + Goal Condition

> The goal condition derives from the frozen approach (stage 1 freeze): this stage layers acceptance criteria on top of it — it does not revisit the direction. If the frozen approach looks wrong here, say so before launch, not after.

1. **Layer acceptance criteria** into three tiers ([reference.md](reference.md) § Stage 2 — Template 2):
   - **Hard** (machine-verifiable) → agent self-verifies; these become the goal-harness condition
   - **Soft** (LLM-judge + deterministic checker) → optional quality gate
   - **Human** (outcome-type) → human acceptance in stage 5
   - Pixel geometry is **Hard** when the goal text contains `figma.com` or `node-id=`, or the user asks for pixel restore (像素级还原). That substring is the scope fact. The stated check is `scripts/check-figma-verify-report.mjs` from `figma-pixel-verify` exiting 0. Those rows are not Soft and not Human. A probe of visible text, a visibility flag, or a list length does not satisfy the hard item. Load `figma-pixel-implement` and `figma-pixel-verify` and follow them during the run. When that same text also contains `参考`, `match the existing`, or `same as`, pass that fact into verify so the named control's interaction states become rows.
2. **Design the goal condition** using four parts. Primary harness (`/goal`) evaluators **only read the transcript** — they do not run commands or read files — so the condition must be something the agent's own output can demonstrate:

   ```
   <one measurable end state> + <stated check: how the agent proves it> + <constraints that must not change> + <budget clause: "or stop after N turns / N minutes">
   ```

   - Good: `all tests in test/auth pass and the lint step is clean`
   - Good: `every call site of the old API is migrated and the build succeeds, stop after 20 turns`
   - Bad: `the app is production-ready` (nothing verifiable in the transcript)
3. **Budget is mandatory** — primary `/goal` harness has **no built-in token budget**. Always add `or stop after N turns` (or a time clause).
4. **Split compound objectives** into a **chain of sequential goals**, each with its own verifiable end state.
5. Output **Template 2 + the final 4-part condition** for confirmation.

> With `traceability: openspec` on, the artifacts map: proposal ← stage 1 frozen approach + why, design ← this stage's acceptance layering + condition, tasks ← stage 3's plan (`openspec new change "<slug>"`; maintain checkboxes as the run progresses).

**Red Flags**: vague conditions (infinite loop or hallucinated success); compound mega-goals in one harness run; no budget clause; constraints that could silently be violated.

---

## Stage 3: Sub-agent Division & Context Management

**Why**: **context rot** — recall accuracy drops as the transcript grows. Long runs that keep everything in one context degrade. Splitting is a requirement, not an optimization.

1. **Division principle**: the main agent holds the **high-level plan + synthesis** (and the goal condition); sub-agents do deep work in **clean contexts** and return only a **condensed summary (1–2k tokens)**.
2. **Pick the context technique** ([reference.md](reference.md) § Stage 3):
   - **Sub-agent architecture** — parallel exploration / multi-module work
   - **Compaction** — long conversational flows; threshold and recovery rules per `context-budget-discipline` (proactive ~60–70% of the window, never near-limit only)
   - **Structured note-taking** — milestone-driven iterative work (NOTES.md / memory)
3. **Quantify the context plan** per `context-budget-discipline`: name (a) the compaction threshold as a fraction of the context window, (b) the phase→reset-boundary map for the planned lifecycle, (c) the ledger path for session handoffs — a plan missing any element blocks Stage-4 launch approval.
4. Define each sub-agent's task, minimal tool set, output contract, completion condition, and failure handling. Prefer an **independent harness** (writer vs reviewer separation) to avoid cross-bias.
5. Fill **Template 3**.

**Red Flags**: main agent absorbing sub-agent details (context flows back in); sub-agents without output contracts; unbounded tool sets.

---

## Stage 4: Launch the Long Run

> **Launch approval** (standalone): load `design-approval-gate` for the approval pattern. Confirm the final goal condition + budget + companion checklist. That confirmation enters **Armed** and MUST NOT start the harness — including for low-impact runs and including in auto mode (`design-approval-gate`'s generic auto escape does not skip this pause). High-impact conditions (unattended / large budget / irreversible) are covered by the same pause; they do not create a second fire-on-approve step. Queue children use the inlined card's recorded approval as 留痕 and do not take this standalone pause.
>
> **Launch instruction** (standalone): start execute only after Armed **and** an explicit Launch phrase from the closed list above. 「自动跑」 / "auto mode" / bare confirm are not Launch. The proxy MAY complete Design-checked; it MUST NOT issue Launch.

1. **Pre-flight** (intent-first; [reference.md](reference.md) § Stage 4). Primary-harness examples in parentheses:
   - **Per-turn project convention file** at repo root (e.g. `CLAUDE.md`) — encode architecture, coding conventions, acceptance rules for multi-turn consistency.
   - **Post-edit validation hooks** (e.g. PostToolUse lint/type-check) — catch issues mid-run.
   - **Auto-approval mode** for routine tool writes — without it, long runs stall on every file write.
   - **Frozen decisions ride along**: the run prompt/contract carries the frozen approach + ticket ledger path (`intake-interview-discipline`), and the openspec change path when traceability is on, so the run can answer "what was frozen" without the human.
   - Confirm budget (turns/time/token) from stage 2.
2. **Launch** (choose by environment):
   - Interactive goal harness: e.g. `/goal <condition>` when available.
   - Non-interactive agent CLI wrapping the harness: e.g. `claude -p "/goal <condition>" --output-format stream-json --verbose`.
   - **Fallback** (no goal harness): manual bounded loop — do work → verify against acceptance checklist → continue if unmet (budget-bounded) → else stop; explicit stop clause required.
3. **In-run decision rules**: mid-run decisions follow `intake-interview-discipline` §B (self-answer priority: frozen contract → investigated fact → conservative default; evidence falsifying the frozen approach → **clean stop + ticket report**, never a silent pivot).
4. **Monitor**: check harness status (elapsed, turns, tokens, latest evaluator reason); interrupt early via the environment's cancel control (e.g. Ctrl+C / `/goal clear`). At each budget milestone (every half/third of the budget), record one run-log line — evaluator reason, remaining budget, anomalies; at each milestone also evaluate the compaction threshold per `context-budget-discipline` (crossed → reset at the next safe point, ledger entry first); sustained no-progress triggers the early interrupt instead of burning the full budget.
5. Output **Template 4**. On standalone: if Design-checked is incomplete, refuse Launch and continue checks; if Armed, wait for a closed-list Launch instruction; only then start the harness. On a queue child, start execute per `Stage-exit policy` (card approval already 留痕).

**Red Flags**: skipping auto-approval mode (run stalls on writes); no budget; no per-turn convention file; one giant goal instead of a chain; silent mid-run approach pivot (violates `intake-interview-discipline` iron rule 2); starting the harness while Design-checked is incomplete; treating 「自动跑」 or bare "ok"/"confirm" as Launch; bundling launch approval with starting the run.

---

## Stage 5: Completion Report & Human Acceptance

> Follow `completion-evidence-discipline`: any "done / pass" claim needs **fresh current-turn evidence** (command output / test results / file diffs). Label each item `Executed` (command + output summary) or `Pending` (manual action required).

1. Main agent produces a **structured completion report** ([reference.md](reference.md) § Stage 5 — Template 5): goal recap, acceptance status (hard/soft/human), a **numbered verification checklist** — goal achievement vs the restated contract / frozen-approach comparison + deviations / tests & evidence with Executed–Pending labels / side effects split functional + non-functional / logic end-to-end review — deliverables + verification evidence, leftovers/risks, spend, and the **decision/assumption ledger** (`intake-interview-discipline` §C — surface unresolved tickets, low-confidence assumptions, and high-impact-if-wrong entries for human judgment; clean-stop tickets included). With `Stage-exit policy: ai-proxy`, the checklist goes to a fresh-context proxy per `ai-proxy-discipline` (tagged verdicts; failing items bounce back for re-verification or ticket).
The explanation (说明), the evidence record (证据留痕), and the acceptance verdict (验收裁决) stay separate. The explanation states the problem, the cause, and the completed fix. The evidence record shows a screenshot when a check opened a screen, and the command with a short output summary when it did not. The acceptance verdict is the person's decision that a finished card is accepted or returned. The evidence record does not carry that decision. On a standalone run, write one review JSON (problem, cause, fix) and one evidence JSON, then generate both HTML pages with `goal-driven-queue`'s `renderReviewPage` / `renderEvidencePage` — never hand-written HTML. The evidence page path is `.goal-driven/runs/<local-YYYYMMDD-HHmm>/evidence.html`. The evidence page title and kicker follow the human's conversation language. Do not overwrite an existing directory. Copy each non-empty png, jpg, jpeg, or webp into that directory and reference it by a relative path. A check that did not open a UI shows the command and the output summary and has no image. A missing or empty image is pending and states the capture still required. Do not invent an image. Before an opened-UI image supports the check, inspect it per `completion-evidence-discipline`. Put each item's pending status and inspection note on the evidence JSON so the evidence page shows the copied image and that inspection. An empty evidence list still gets the page, and the page states that no checks were recorded and contains no image. The review page path is `.goal-driven/runs/<local-YYYYMMDD-HHmm>/review.html`. Record the review page path and the evidence page path on the completion report. The review page does not add a standalone evidence link. Pass the same shared navigation block into both pages (via `navHtml` from `renderNav`, or `--nav`), with relative items that at least cross-link review ↔ evidence; mark a missing target unavailable. Load the renderer from the loaded `goal-driven-queue` skill directory (`<queue-skill-dir>/scripts/render-html.mjs`) by path; if that module is missing, print the `.md` / JSON paths and continue without HTML — do not hand-write it. Ensure the target repository ignores `.goal-driven/**/*.html` by appending that line. On a queue child, the completion report includes the problem, the cause, and the completed fix, and an evidence list. Each evidence item is an opened-UI check citing a png, jpg, jpeg, or webp path, or a non-UI check citing the command and a short output summary. A missing or empty image is pending and states the capture still required. Do not invent an image. Before an opened-UI image supports the check, inspect it per `completion-evidence-discipline`. This run does not write the HTML page and does not write the evidence HTML.

2. With `traceability: openspec` on: run `openspec validate` on the change, archive it (syncing main specs) once machine-verifiable evidence is complete, and record both as report evidence items. Outcome-type findings flow back as new or revised changes, not as archive blockers.
3. **Human acceptance**:
   - Machine-verifiable items: reported by agent + spot-check.
   - Outcome-level items: **judged by the human** — harness evaluators verify output, never outcome.
4. **Feedback loop**: acceptance findings feed the next run's Template 1.

**Red Flags**: claiming "done" without evidence; agent auto-marking outcome items as passed.

---

## Mode Lifecycle

- **Manual (default)**: pauses at stages 1, 2, 3, the Stage 4 launch-approval pause (Armed), and stage 5. Launch still needs a closed-list instruction.
- **Auto** (「自动模式」/「自动跑」 / "auto mode"): on **standalone**, still pauses at stages 1, 2, 3, and the Stage 4 launch-approval pause; does not skip those confirms; does not start the harness (auto-mode words are not Launch); stage 5 always ends at human acceptance. On a **queue child**, follow `Stage-exit policy` for who answers mid-run questions; do not insert a second Armed wait.
- **Revert-to-manual**: auto always reverts to manual on completion (including after stage-5 acceptance) or on any interruption. Re-entering auto requires an explicit trigger; implicit continuation never re-activates it.
- **Long-run specific**: when a run ends (goal met or budget exhausted), return control to the human — do not auto-start a new goal or auto-extend the budget without explicit confirmation.

---

## Common Mistakes

| Mistake | Consequence | Fix |
|---------|-------------|-----|
| Self-correction without a deterministic checker | A "fix" worsens a working result | Only iterate on deterministic-checker failures; re-verify after each fix |
| Agent marks outcome items as passed | "Done" without real acceptance | Outcome-type standards are judged by the human in stage 5 |
| Treating primary-harness CLI as the only platform | Other agents cannot run the skill | Follow intent-first launch + generic fallback in stage 4 |
