---
name: kanso-task
description: Use when the user wants a task done well rather than fast, wants a rough or underspecified request sharpened before it runs, or asks for a careful, principled pass at a piece of work.
argument-hint: "[the thing you want done, in plain language]"
disable-model-invocation: true
allowed-tools: Bash(git *) Bash(rg *) Bash(find *) Bash(wc *)
---

# kanso-task

The user types `/kanso-task <rough request>`. This skill turns that rough request into a sharp prompt, then executes the task in the same chat with both `kanso-prompting` and `kanso-principles` standing as context. The output should be measurably better than what the user would have got from typing the same words into the chat directly.

Three phases:

- **Phase A — Clarify (only if needed).** Run the ambiguity pre-flight. If a trigger fires, ask one tight batch of questions and fold the answers in. If the input is already concrete — or the user waved the skip valve — go straight to formatting with no questions.
- **Phase B — Rewrite.** Apply the `kanso-prompting` rules to produce a sharp version of the prompt. Show it to the user. Wait for approval.
- **Phase C — Execute.** Run the rewritten prompt inline in the current chat. Any code produced during execution follows `kanso-principles`.

## Always run inline

This skill runs in the calling chat. Never dispatch the rewrite, the approval gate, or the execution via the Agent or Task tool. Never spawn a subagent. The user has to be able to see the rewritten prompt before it runs, intervene during execution, and inspect the result without switching windows. A subagent dispatch defeats the entire workflow.

## Phase A — Clarify

A pre-flight ambiguity check that runs before formatting. Its only job is to catch the gaps that would force a guess. Concrete input passes through untouched — the yap-and-go feel survives; the pause is earned, not routine.

### The skip valve — check this first

Two ways an input skips questioning entirely:

1. **Explicit.** The user signalled skip. The unambiguous form is the `--go` flag. A plain-language equivalent (`just format it`, `no questions`) counts only when it is a directive *about* the request rather than part of it — a trailing or standalone instruction to the skill, not a phrase inside the task being described. `/kanso-task format the users table, no questions about the schema yet` is a task that happens to contain "no questions"; it is not a skip signal. When a plain-language form is genuinely ambiguous, treat it as task content and run the triggers. Honour a real skip without comment: format silently, even if a trigger would otherwise fire. The user has taken the wheel.
2. **Inferred.** The input is high-confidence — a trained reader could produce a sharp prompt from it without inventing anything load-bearing. Format silently.

Only when neither applies do you run the triggers below.

### Ambiguity triggers

Ask when any one is genuinely true. If none are, don't ask — formatting a clear request is the default, not the exception.

1. **Acceptance criteria unclear** — "done" has no observable shape. `make search faster` doesn't say how much faster or how you'd know.
2. **Scope boundaries fuzzy** — what's explicitly out of scope is undefined, and the request could plausibly balloon. `tidy up the auth module` — one function, or the directory?
3. **Unstated technical choice** — a decision is being assumed rather than stated. `add caching` — where, what eviction, in-memory or shared?
4. **Undefined term or referent** — a word or pointer with no fixed meaning here. `fix the thing we discussed`, `the legacy path`.

A missing file/module target usually surfaces as trigger 2 or 4 — treat "which code?" as an ambiguity, not a separate checklist item.

### The questioning rules

- **One batch, then format.** Ask every question in a single round. No conversational back-and-forth, no follow-up interrogation. Take the answers, fold them in, format.
- **Cap at three. Fewer is better.** One sharp question beats three padded ones. If only one trigger fired, ask one thing.
- **Aim at the ambiguity, not at a spec.** Each question exists to sharpen the formatted prompt. This is a prompt optimiser, not a spec tool — no EARS, no acceptance-criteria tables, no ceremony. Keep it loose.
- **No cosmetic or scope-creep questions.** Never ask "would you like me to also…" — that negotiates scope under cover of clarifying. Ask only what removes a guess.

If the input is still unworkable after one round, say so plainly rather than formatting a vague request into a vague-but-prettier one.

## Phase B — Rewrite

Apply `kanso-prompting` to produce the sharp version. The rewrite should reliably:

- **Lead with the verb and the artefact.** `Audit`, `Refactor`, `Write`, `Implement`, `Explain`. Name what the model should produce.
- **State the target precisely.** File paths, function names, line ranges, branches. Not "the auth module" but `src/auth/session.ts`.
- **Carry the *why*.** A one-sentence reason. The model generalises better with motivation than without.
- **State constraints explicitly.** Frameworks, dependencies, things-not-to-touch, output shape.
- **State the stopping condition.** When is the model done? `Stop after the report and do not edit files` or `Apply the fix and run the existing tests`.
- **Drop the noise.** No `CRITICAL`, no ALL CAPS, no "please carefully think step by step". Modern Claude doesn't need it and it now degrades output.
- **Match the user's voice.** If the user is terse, the rewrite is terse. If the user is conversational, the rewrite stays conversational. Don't impose a house style.

The rewritten prompt earns its length the same way code does. Don't pad. A two-line rewrite is fine if two lines is enough.

## The approval gate

Always end Phase B with this block and stop:

```
Original:
  <one-line echo of what the user typed>

Rewritten:
  <the sharp version, as it would be sent>

Proceed?
  y          — execute the rewritten prompt inline, with kanso-principles loaded
  edit       — amend the rewritten prompt
  send-original — execute the original instead (rare; only when the rewrite drifted)
  n          — stop, leave the rewrite in the transcript
```

If the user approves, move to Phase C. If they pick `edit`, take the amended prompt and re-emit the gate. If they pick `send-original`, use the original.

## Phase C — Execute

Run the prompt in the current chat. During execution:

- `kanso-principles` is standing context. Any code written, modified, or reviewed follows the anti-dilution taxonomy. Deletion over addition, no defensive theatre, no filler variables, no tautological comments. The principles override default verbosity.
- `kanso-prompting` is standing context for any *meta* prompts produced during execution (e.g. asking a subagent for research — though this skill itself does not dispatch subagents).
- Existing kanso skills apply where they fit. If the rewritten task is a refactor, `/kanso-refactor` rules govern. If it produces commits, `/kanso-commit` rules govern. If it ends with a PR, `/kanso-pr` rules govern. Don't reimplement those — invoke them or let them auto-load.
- Maintain a running `implementation-notes.md` file (see below) for any non-trivial execution.
- The model executes the task the same way it would if the user had typed the rewritten prompt directly — with full tool access, in the current chat, with the user able to interrupt.

When execution finishes, report what changed. One short summary block. No marketing. If a notes file was written, point at it.

## Implementation notes during execution

No matter how sharp the rewritten prompt is, ambiguities and unknown-unknowns surface during execution. The model has to make small judgment calls — a naming choice, a library version, a structural decision, a deviation from what the spec implied. Stopping to ask about each one breaks momentum; making them silently leaves the user blind.

During Phase C, maintain a running `implementation-notes.md` file in the working directory. This is the model's sanctioned way to make a call without interrupting, while keeping the user fully in the loop after the fact. The file is reviewable at the end and converts cleanly into a PR description or a commit body.

Append (don't overwrite) a timestamped section per `/kanso-task` run:

```markdown
## 2026-05-25 14:32 — <one-line task description>

### Decisions made outside the spec
- <choice, with the reasoning in one sentence>

### Things changed from what the prompt implied
- <deviation and why it was needed>

### Tradeoffs taken
- <what was given up, what was gained>

### Anything else you should know
- <surprises, follow-ups worth doing, things you may want to revisit>
```

Rules:

- **Append, never overwrite.** If the file exists, add a new dated section at the bottom.
- **Skip for trivial executions.** If the task was a single one-line edit, a question that didn't touch the codebase, or anything where no judgment call was made, don't write the file. A notes file with empty sections is noise.
- **One sentence per entry.** The notes are a log, not a reflection. Long entries belong in the commit body.
- **Omit empty sections.** If no tradeoffs were taken, the heading goes too.
- **Reference the notes in the final summary.** `Notes: implementation-notes.md (3 decisions, 1 tradeoff)` so the user sees there's something to read.

The file lives alongside the user's repo; it's their artefact, not a hidden one. They can keep it, paste it into a PR, delete it after review, or `.gitignore` it. The skill doesn't manage its lifecycle beyond writing to it.

## What this skill never does

- Run via the Agent or Task tool, or dispatch any phase to a subagent or parallel runner.
- Execute the rewritten prompt without showing it to the user first.
- Pad the rewrite to look more rigorous. Length is not signal.
- Ask more than three clarifying questions, or spread them across more than one round. The pre-flight is a single batch.
- Question a concrete input, or one where the user waved the skip valve. High-confidence input and an explicit `--go` both format silently.
- Re-introduce the noise patterns `kanso-prompting` warns against (`CRITICAL`, ALL CAPS, anti-laziness scaffolds).
- Silently change the user's intent under cover of "sharpening". The rewrite is faithful — only the wording improves.
- Edit `kanso-principles` or `kanso-prompting` during execution. Those are reference docs, not work targets.
- Skip the approval gate. The user always sees the prompt before it runs.

## Failure modes to avoid

- Rewriting a vague prompt into a longer vague prompt. If the source is empty of intent, ask — don't pad.
- Asking clarifying questions the user already answered in the original request.
- Running the ambiguity triggers when the input is plainly concrete. A pause that isn't earned kills the yap-and-go feel the skill exists to protect.
- Re-stating the original request in the rewrite. The rewrite is a different artefact, not a paraphrase.
- Drifting from the user's actual ask by adding plausible-sounding scope ("I'll also write tests for it"). Stay faithful; if you think more is needed, surface it as a follow-up after execution, not as a silent expansion.
- Treating "execute inline" as licence to skip the principles. `kanso-principles` is the whole point of routing through this skill rather than typing the prompt directly.
- Producing a beautiful rewrite and then running it via a subagent. The whole loop is in-chat, every time.
- Skipping the implementation notes on a non-trivial execution because "nothing notable came up". If the task involved any decision the user didn't pre-approve, write it down.
- Writing implementation notes that read like marketing or apology. They're a log: one short sentence per entry, factual, no hedging.
