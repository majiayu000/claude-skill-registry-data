---
name: ai-brain-dump
description: Start and run a listen-first braindump session for tickets, issues, ADRs, worktasks, PR descriptions, requirements, designs, or implementation plans. Use when the user says they want to braindump, think out loud, capture rough requirements, or provide context incrementally before asking the agent to synthesize, update a ticket, create docs, or perform implementation work.
models:
  claude: opus      # high-complexity; multi-turn synthesis and deep requirement reasoning
  copilot: auto
  codex: gpt-5.5
---

# Brain Dump

## Modes & Switches

All switches are **OFF by default**. With no switches the skill behaves exactly as a silent listen-first
capture: no questions, no tools, no synthesis until asked.

| Switch | Effect |
|--------|--------|
| _(none)_ | Pure listen-first. Capture silently; never ask, never browse. |
| `--oktoask` | Permit clarifying questions during Listen. Cadence is **sparse** — only genuine blockers or contradictions that would corrupt capture; 1–2 questions; **non-blocking** ("keep dumping, answer when you can"). Stays **tool-free**. |
| `--thinking` | Make questioning **liberal** during Listen — ask whenever something is unclear, including detail gaps. Implies `--oktoask`. |
| `--oktoreaddocs` | Permit reading local code/docs to ground a question (promotes the Phase 3 "Compare" tools into the Listen phase on demand). Implies `--oktoask`. |
| `--oktowebsearch` | Permit web search to ground a question or fill a gap. Implies `--oktoask`. |

**Implication rule:** `--thinking`, `--oktoreaddocs`, and `--oktowebsearch` each imply `--oktoask`. If any
of them is passed without `--oktoask`, treat `--oktoask` as on.

**Cost note:** `--oktoask` and `--thinking` are cheap — they add conversational turns, not tool-result
bloat. `--oktoreaddocs` and `--oktowebsearch` are expensive — they re-enable the file/web payloads that
get injected into context and re-billed every turn, which is the very cost the listen-first default avoids.
Use the tool switches deliberately.

## Core Posture

Run a low-friction capture session. The user is thinking out loud; do not prematurely organize, debate, or act.

Default behavior:

- Acknowledge that the session is active.
- State that you will listen and hold context until explicitly asked to synthesize or update an artifact.
- Do not modify tickets, files, docs, code, or remote systems during the listening phase.
- Keep responses short while the user is dumping context.
- Preserve rough phrasing, intent, trade-offs, decisions, open questions, and contradictions.
- Treat later user corrections as authoritative.

## Session Phases

### 1. Initialize

When the user starts a braindump, reply briefly:

```text
Absolutely. Braindump away.

I’ll listen and hold the context for [target if known]; I won’t update anything until you explicitly ask me to.
```

If the target artifact is ambiguous, still start listening. Do not block the session unless acting later would be impossible without clarification.

### 2. Listen

For each braindump message:

- Confirm capture in one or two sentences.
- Summarize only the newly added information or the evolving theme.
- Do not produce a full requirements spec unless asked.

Questioning during Listen depends on the active switches (see Modes & Switches):

- **Default (no switch):** Do not ask clarifying questions. Capture silently.
- **`--oktoask` (sparse):** Ask only when an item is a genuine blocker or internally contradictory in a way
  that would corrupt capture. Keep to 1–2 questions, non-blocking — invite the user to keep dumping and
  answer when convenient. Stay tool-free.
- **`--thinking` (liberal):** Ask whenever something is unclear, including detail and wording gaps. Still
  non-blocking; still batch related questions rather than dripping one per item.

Browsing/tools during Listen:

- **Default / `--oktoask` / `--thinking`:** tool-free — do not browse, inspect code, or use external tools.
- **`--oktoreaddocs`:** you may read local code/docs to ground a question or confirm a reference.
- **`--oktowebsearch`:** you may run a web search to ground a question or fill a gap.
- Even with tool switches on, grounding is the only thing widened — do not synthesize or modify anything
  during Listen.

Good listening response:

```text
Captured. Adding that the pre-pipeline should fetch the diff with patch data, detect `configuration.json`, and continue normally unless deeper analysis is requested later.
```

### 3. Compare Or Clarify

If the user asks whether there are questions, whether the dump matches the current solution, or whether anything is unclear:

- Inspect the relevant local code/docs or remote issue only as needed.
- Ask targeted questions grounded in discovered reality.
- Keep questions concrete and numbered.
- Separate true blockers from wording improvements.
- Do not update artifacts yet unless explicitly asked.

Question style:

```text
Yes, a few clarifying questions before we finalize the dump:

1. Should the old flag be removed entirely or kept as a compatibility alias?
2. When detection succeeds, should this ticket only log and continue, or should it suppress dispatch?
```

### 4. Synthesize On Request

Only when the user asks to update/create/synthesize an artifact:

- **Conclusion Q&A (when any questioning switch is on):** Before producing the artifact, run ONE liberal
  numbered clarification round covering everything still unresolved. Separate true blockers from
  nice-to-haves. This is a single bounded pass, not an open-ended loop — proceed to synthesis once
  answered (or once the user says to proceed regardless). In the default no-switch mode, skip this and
  surface open questions inside the artifact instead.
- Confirm the target if multiple were mentioned.
- Use the accumulated context and any final decisions.
- Produce the requested artifact directly: issue description, ADR, worktask, PR body, implementation checklist, acceptance criteria, etc.
- Preserve decisions and non-goals explicitly.
- Include open questions only when still unresolved.

If the user asks to update a live ticket or file, perform the update with the appropriate tool and report the exact target changed.

## Capture Model

Maintain a mental running capture with these buckets:

- Target artifact or ticket
- Problem statement
- Desired behavior
- Defaults and configuration
- Current-system references
- Implementation shape
- Tests and documentation
- Decisions made during clarification
- Open questions
- Explicit non-goals

Do not expose the whole capture every turn. Surface it when the user asks to finalize, review, or synthesize.

## Guardrails

- Do not treat a braindump as permission to implement.
- Do not clean up the user's rough wording during the listening phase except in tiny confirmations.
- Do not over-question early; braindumps often become clear after several messages.
- Do not lose changed targets. If the user later names a different issue or file, use the latest explicit target and mention the switch.
- If the user asks you to "just listen," obey that even when you notice likely issues — this overrides any
  questioning switch for as long as it stands.
- If the user asks you to compare against code, tools are allowed, but final output should still be questions or observations unless they ask for edits.
- In `--oktoask` (sparse) mode, do not nitpick wording or ask about details that later messages will
  likely clarify — sparse means blockers only. (`--thinking` relaxes this to allow detail/wording gaps.)
- Batch related questions into one message; do not drip a question after every dumped item.
- A questioning switch is not permission to act. `--oktoreaddocs` / `--oktowebsearch` widen *grounding*
  only; the no-implement, no-modify rule still holds until the user explicitly asks to synthesize or update.

## Finalization Output

When finalizing requirements, prefer this shape unless the requested artifact has its own format:

- Requirement Specification
- Functional Requirements
- Implementation Notes
- Documentation Updates
- Acceptance Criteria
- Non-Goals
- Open Questions, only if any remain

Keep the final artifact specific enough for another engineer or agent to execute without needing the whole conversation.
