---
name: memory-and-improvement
description: "Captures project-specific and cross-project memory in the right place. Use when a command fails unexpectedly, the user corrects you, a feature is missing, your knowledge is outdated, or you discover a better recurring approach. Global memory stores durable facts, preferences, history, and stable cross-project lessons; project memory stores repo-specific facts, conventions, lessons, and errors; reusable procedures should become Codex skills under ~/.codex/skills/."
metadata:
  short-description: Capture and route project and global memory
---

# Memory-and-Improvement Skill

Log learnings, errors, facts, conventions, and feature requests into project memory or global memory.

This skill is Codex-only.
`~/global-memory/` should contain durable cross-project memory and curated initialization context, not transient adapter files or per-session scratch prompts.
If something is really a reusable procedure, extract it into a skill under `~/.codex/skills/`.
For deeper maintainer policy, use `references/maintainer-reference.md`; keep this file focused on runtime behavior that the agent needs while executing.

## Core Rule

Route in this order:

1. Is this mainly a reusable procedure?
2. If not, would this still help in a different repository next week?

Capture favors recall. Promotion favors precision.

- `.learnings/` is intentionally a high-recall layer
- if something seems worth recording, it is usually acceptable to capture it in `.learnings/` first
- `global memory`, `SUMMARY.md`, and skills are higher-precision layers and should stay more selective

Routing:

- If it is mainly a reusable procedure, extract or update a skill under `~/.codex/skills/`
- Otherwise, if it would help in a different repository next week, log it to global memory: `~/global-memory/namespaces/<namespace>/.learnings/`
- Otherwise, log it to project memory: `./.learnings/`

## Closed-Loop Runtime Contract

Use this skill as a four-stage loop:

- Recall: make an explicit recall decision before every reply; default to performing the smallest relevant recall step first for every non-trivial turn, and allow a safe-skip judgment only for narrow trivial turns
- Reason: decide whether the current layer is enough or whether you need `recall-memory.sh`, `review-memory.sh`, `search-memory.sh`, structured factual files, or raw `.learnings/*.md`
- Respond/Act: answer or act while honoring the recalled constraints and repo conventions
- Reflect: after any meaningful work product, make an explicit reflect decision; default to running a structured reflect check after implementation, debugging, testing, review, documentation changes, planning that changes execution, or memory-management turns unless the turn is clearly too small to produce a durable candidate

Strict runtime standard:

- preserve the baseline contract to perform a recall step before every reply, but make the decision explicit rather than implicit
- strong-default recall: repo work, debugging, planning, implementation, review, memory operations, and user/profile/history-dependent answers should run recall rather than rely on safe-skip
- narrow skip only: safe-skip is intended for casual chat, pure rewriting, pure summarization of user-provided text, or pure translation where cross-turn memory is unlikely to matter
- no silent skip: if recall is skipped for a trivial or self-contained turn, the main session must still record why that skip is safe, even if the user-facing reply does not spell it out
- stronger-default reflect: implementation, debugging, testing, review, documentation changes, planning that changes execution, and memory-management turns should run reflect rather than rely on an implicit no-op
- no silent omission: after any meaningful work product, do not end the turn without either a reflect check or an internal "no candidate" judgment
- the explicit decision belongs to the main session, not to a hook, wrapper, or helper script
- helper scripts can support the decision, but they do not replace the main session's judgment
- do not force user-visible "no recall needed" or "no reflect needed" filler; surface the judgment only when it changes the answer, plan, audit status, or logging outcome

Reason checklist after the recall decision:

1. What relevant memory, if any, did recall surface?
2. If recall was skipped, why is that skip safe for this turn?
3. Is the current layer already enough to answer or act safely?
4. If not, what is the next deeper source: `review-memory.sh`, `search-memory.sh`, a structured factual file, or raw `.learnings/*.md`?
5. Does the recalled context, or the safe-skip judgment, impose planning constraints such as repo conventions, prior failures, or audit requirements?

Reason escalation rules:

- summary hit and sufficient -> proceed without forcing deeper reads
- summary hit but underspecified -> open `review-memory.sh` or the relevant structured factual file
- no summary hit but the task clearly depends on history, preferences, prior failures, or corrections -> use `search-memory.sh`
- chronology, evidence, debugging context, or exact correction history needed -> open raw `.learnings/*.md`
- when changing `memory-and-improvement` workflow/docs/spec/roadmap/diagram behavior, treat the repo's audit convention as a planning input before edits begin, not as a post-hoc cleanup step

For this repository, `memory-and-improvement` workflow/docs/spec/roadmap/diagram changes are audit-sensitive work. When runtime rules and user permission allow it, run an audit-focused subagent before considering the work complete or moving to the next phase. If you cannot run one, say so explicitly rather than silently weakening the repo rule.
In short: run an audit-focused subagent before considering the work complete or moving on when runtime rules and user permission allow it.

Respond/Act execution boundary:

- normal execution: replies, searches, memory review/logging, and repo work that does not change `memory-and-improvement` workflow/docs/spec/roadmap/diagram behavior
- audit-aware execution: substantial `memory-and-improvement` workflow/docs/spec/roadmap/diagram changes that can reshape the skill's behavior, contract, or maintainer guidance

When audit-aware execution applies:

- surface in the plan or commentary that the work is audit-sensitive before edits begin
- keep an audit step in scope before treating the work as complete or moving to the next phase
- if runtime rules or user permission block subagent use, state that the audit requirement remains unmet instead of pretending the work was fully audited
- keep the main session as final decision maker; the audit step informs completion but does not replace the main session's judgment

## Runtime Routing Summary

Keep the live decision model short:

- use project memory for repo-specific facts, conventions, failures, and requests
- use global memory for durable cross-project facts, preferences, history, and operating lessons
- use a skill when the main value is a reusable procedure
- use a structured factual file when the content is a stable factual snapshot that will likely be loaded repeatedly
- keep raw `.learnings/*.md` for chronology, corrections, evidence, tentative items, and debugging context
- use the Closed-Loop Runtime Contract above as the per-turn operating model

## Adaptive Routing Strategy

This section is auto-managed by `scripts/maintenance/update-skill-policy.sh`.
It may rewrite only the strategy hints below; it must not rewrite the rest of this skill.

<!-- memory-auto-skill-policy:start -->
- none promoted yet
<!-- memory-auto-skill-policy:end -->

Runtime loading order:

1. `INIT.md` when early cross-project orientation is needed
2. `SUMMARY.md`
3. structured factual files
4. `REVIEW.md`
5. raw `.learnings/*.md`
6. asset index (`project: .learnings/assets/INDEX.md`; `global: assets/INDEX.md`)
7. concrete asset files only if needed

Runtime guardrails:

- after recall, explicitly decide whether the current layer is enough before acting
- when a required memory read is blocked by sandbox permissions, immediately request the narrowest necessary access from the user; do not silently skip or bypass the memory step
- if recall is skipped, explicitly decide why the skip is safe for this turn, but only surface that judgment when it affects the user-visible response
- skip global memory when the task is repo-local, casual, or creative
- when the user asks a memory-system meta question, prefer the formal memory-system recall mode or inspect the relevant state/namespace sources directly instead of inferring from the current repo or scanning arbitrary roots first
- if no relevant memory is found at higher layers, answer without forcing deeper reads
- keep `review-memory.sh` summary/review-first by default; only fall back to raw entry previews when higher layers are absent or explicitly requested
- keep `search-memory.sh` staged by default; stop after the first layer with hits unless an explicit exhaustive search is requested
- do not open raw `.learnings/*.md` until higher layers are insufficient
- repo-local agent instructions still belong in `AGENTS.md`, not project memory
- do not assume every stable item must be promoted; raw history is a first-class layer, not a failure state
- keep logging to `.learnings/` permissive; keep promotion to `global`, `SUMMARY.md`, and skills conservative
- `writeback-memory.sh` should only distill advisory `promote_to_summary` candidates that clear the writeback threshold; raw recurrence alone is not enough, and nightly maintenance must not collapse capture and promotion together
- after substantial work, explicitly decide whether reflection produced a candidate to log, promote later, or extract into a skill

Examples of structured factual files include `PROFILE.md`, `ACADEMIC_PROFILE.md`, `PUBLICATIONS.md`, `FUNDING_HISTORY.md`, and `RECORDS.md`.
Prefer short summaries or redacted excerpts over raw command output.

## Workflow

When an error, correction, or better pattern appears:

1. Apply the Core Rule to choose skill vs global memory vs project memory.
2. Before replying, make a recall decision:
   - if recall is needed, start with `bash ~/.codex/skills/memory-and-improvement/scripts/recall/recall-memory.sh --scope auto`
   - if recall is skipped, record why the turn is safe to answer without it; do not surface that note unless it matters to the reply or plan
3. If the higher layers are not enough, escalate deliberately:
   - `bash ~/.codex/skills/memory-and-improvement/scripts/recall/review-memory.sh --scope project`
   - `bash ~/.codex/skills/memory-and-improvement/scripts/recall/search-memory.sh --scope project --query "..."`
   - for memory-system meta questions, prefer `bash ~/.codex/skills/memory-and-improvement/scripts/recall/recall-memory.sh --mode memory-system`
4. Log manually with the structured helper:
   - `bash ~/.codex/skills/memory-and-improvement/scripts/capture/log-memory.sh --scope project --type learning --summary "..." --details "..." --suggested-action "..."`
5. After substantial work, make a reflect decision:
   - if a structured reflect check would help, run `bash ~/.codex/skills/memory-and-improvement/scripts/recall/reflect-memory.sh --scope project --summary "..."`
   - otherwise make an internal note that no durable candidate was found and why; only mention it when it affects the outcome the user should know about

For initialization, organization, writeback, git history, nightly maintenance, extraction, and long-form examples, use the README and `references/maintainer-reference.md` instead of expanding this runtime prompt.

## Memory Candidate Workflow

Use a lightweight candidate workflow so memory does not turn into an automatic dump.

Bias toward capture for `.learnings/`: if something feels worth remembering, worth revisiting, or worth debugging later, it is usually a valid candidate even if you are not yet sure it deserves promotion.

Consider a memory candidate when you notice:

- a durable user preference
- a durable cross-project fact
- a repo-specific convention or constraint
- a recurring failure pattern
- a real missing capability request
- any other event, observation, correction, or decision that seems worth recording for future recall

Final logging stays manual:

1. Inspect the candidate.
2. Choose skill vs project memory vs global memory.
3. Call `log-memory.sh` directly with the chosen scope and type.

## Detection Triggers

Use the same candidate signals from the Memory Candidate Workflow above as the default logging triggers during a turn.
The most common immediate trigger is a correction, but any event that still seems worth recording for future recall, debugging, or pattern detection remains a valid candidate.

Typical correction cues:

- "No, that's not right..."
- "Actually, it should be..."
- "You're wrong about..."
- "That's outdated..."

## Key Scripts

Core scripts:

- `scripts/hooks/activator.sh`
- `scripts/bootstrap/init-memory.sh`
- `scripts/recall/recall-memory.sh`
- `scripts/recall/reflect-memory.sh`
- `scripts/recall/review-memory.sh`
- `scripts/capture/log-memory.sh`
- `scripts/recall/search-memory.sh`
- `scripts/maintenance/suggest-promotions.sh`
- `scripts/capture/log-asset.sh`
- `scripts/maintenance/git-memory.sh`
- `scripts/maintenance/organize-memory.sh`
- `scripts/maintenance/writeback-memory.sh`
- `scripts/maintenance/update-skill-policy.sh`
- `scripts/maintenance/remove-project-memory.sh`
- `scripts/maintenance/nightly-maintenance.sh`
- `scripts/maintenance/interval-maintenance.sh`
- `scripts/maintenance/install-nightly-maintenance.sh`
- `scripts/maintenance/install-windows-maintenance.ps1`
- `scripts/maintenance/run-windows-maintenance.ps1`
- `scripts/maintenance/run-windows-maintenance-hidden.vbs`
- `scripts/shared/file-lock.sh`
- `scripts/capture/extract-skill.sh`

Shortcut wrappers:

- `scripts/shortcuts/remember-project-fact.sh`
- `scripts/shortcuts/remember-global-fact.sh`
- `scripts/shortcuts/remember-error.sh`
- `scripts/shortcuts/index-factual-file.sh`
- `scripts/shortcuts/index-asset.sh`
- `scripts/shortcuts/list-registered-project-memories.sh`

## Memory Git opt-out

A .memory-no-git file in a memory directory or an ancestor disables this skill's Git initialization, status initialization, and commits for that subtree. Check for this marker before invoking Git directly. Preserve it when synchronizing memory. Capture and maintenance continue normally even when older settings request automatic commits.

Codex SyncKit creates this marker for shared global memory. Keep Git archives outside the sync directory. Existing Git history requires a separately authorized archive or removal.

## Hook Integration

Hooks are opt-in.
Recommended default: enable `SessionStart` so each new Codex session begins with memory locations plus loading rules, then use `UserPromptSubmit` to reinforce the main session's recall and reflect decisions.

Hook role:

- hooks may trigger reminders or inject runtime guidance
- hooks must not decide recall routing or safe-skip justification
- hooks must not decide project-vs-global routing or memory type
- the main session remains responsible for every recall, skip, reflect, and logging decision

Minimal setup uses `scripts/hooks/activator.sh`.
Current behavior:

- `activator.sh` injects runtime guidance on `SessionStart`, not an automatic preload of memory contents
- Windows CodexKit runs `memory-project-coverage.ps1` on `SessionStart`: it initializes the standard empty `.learnings/` structure for every existing Codex sidebar project, registers those project memories, and includes the current project even before it appears in the sidebar
- missing sidebar roots are reported but never fabricated; paths inside the managed global-memory namespace are classified as `global-managed` instead of being duplicated in the project registry
- this bootstrap is structural only: it must not invent learnings, make routing decisions, or silently convert arbitrary project documents into memory
- `user-prompt-recall-reminder.sh` reinforces recall and reflect expectations on every prompt but does not run general project/global recall or reflection itself; for explicit user-profile cues it may inject the small `user-profile/SUMMARY.md` layer
- project memory remains the detected project root's `.learnings/` directory, even when that root is `~`
- when the skill is installed from CodexKit, the project registry lives at `CodexKit/memory-system/project-memory-registry.tsv`
- local project records include the current device name; OneDrive project records use `onedrive`, no device identity (`-`), and a path relative to the OneDrive root
- registry lookup ignores another device's local records and resolves OneDrive records against the current device's OneDrive root
- the legacy machine-local `project-memory-registry.txt` is migrated when a project memory is next registered or unregistered
- the CodexKit installer also merges a legacy machine-local registry immediately, preserving existing shared records
- registry writes are skipped when the record already exists, and the write lock remains machine-local rather than being synchronized through OneDrive
- OneDrive conflict-copy TSV files are read and folded back into the canonical registry on the next real registry update
- logs, interval timestamps, hook reflect markers, removed-project archives, scheduled-task instances, and Git metadata remain device-local by design
- the startup guide points the main session toward `recall-memory.sh`; `UserPromptSubmit` remains reminder-first, with only the explicit user-profile summary exception described above
- shortcut wrappers stay convenience entrypoints only; they must keep delegating to the core scripts

## References

Use these deeper docs only when needed:

- `references/maintainer-reference.md` for stable policy, promotion rules, asset policy, and anti-overpromotion guidance
- `references/hooks-setup.md` for hook configuration details
- `references/windows-maintenance.md` for Windows Task Scheduler setup and verification
- `README.md`
- `README.zh-CN.md`

## End-of-Task Prompt

If no hook is enabled, use this manual reminder:

> After completing this task, evaluate whether any project or global learnings should be logged using the memory-and-improvement format, and whether any reusable procedure should become a skill under `~/.codex/skills/`.
