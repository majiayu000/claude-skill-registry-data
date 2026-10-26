---
name: rite-handoff
description: "User-invoked handoff writer: sync chat-only context into `.devrites/` and write a fresh-agent handoff."
user-invocable: true
disable-model-invocation: true
argument-hint: "[what the next session will focus on]"
---
<!-- loads: {"always":["devrites-lib/reference/standards/core.md","rite-handoff/reference/handoff-template.md","devrites-lib/reference/reply-contract.md"],"triggers":{"hygiene":["devrites-lib/reference/standards/context-hygiene.md"]}} -->
> Read-set manifest: `devrites-engine context --skills-root .pi/skills <slug> --skill rite-handoff` (no workspace: `--out <path>`) bundles every file named below into one deduplicated read. Trigger names map to the conditional rules in the sections that follow.

# /rite-handoff: chat-only context, into a fresh-agent doc

DevRites' workspace `.devrites/work/<slug>/` already captures everything that *should*
persist (spec, plan, tasks, decisions, evidence, drift, review). This skill captures
what the **chat** is holding that is **not** in the workspace, so a fresh agent (or
the same user after `/clear`) can pick the work up without re-reading the transcript.

Read [`core.md`](../devrites-lib/reference/standards/core.md) first: its "Persistence before stopping" discipline is
exactly what this skill executes. The other rule files load on demand.

Then read the explicit or active workspace's `state.md` directly, and run
`devrites-engine handoff [slug]` — its resume record (cursor, `awaiting_human`,
blocking question gates, the `gates.md` reduction, `decisions.md` dead ends,
in-flight waves, read-next order) is the deterministic spine of the handoff doc's **Resume**,
**Read next**, and **Next action** sections. The chat adds what the workspace
cannot hold; the engine supplies what the workspace already knows.

## Where to write

- **Active feature exists** → `.devrites/work/<slug>/handoff.md` (overwrites the previous
  handoff; the workspace is the canonical home for this slug). Before overwriting, read the
  previous file: its "External references" and "Live assumptions" exist nowhere else. Carry
  each still-valid entry into the new file or list it under "Retired from the previous
  handoff" with a reason; an entry in neither place is a silent drop — fix the draft before
  writing.
- **No active feature** → OS temp dir (`$TMPDIR` / `/tmp` / `%TEMP%`) as
  `rite-handoff-<ISO-timestamp>.md`. Print the absolute path after writing.

## Before you write: sync, don't duplicate

For each of these, write the content into its **canonical home** first, then merely
*note* in the handoff that the sync happened:

- **Open mid-flight question** → append to `questions.md` (with best-guess attached if
  possible).
- **Decision discussed but not yet recorded** → append to `decisions.md` with the *why*,
  not just the *what*.
- **Assumption** about behaviour / API / user intent → append to `assumptions.md`.
- **Drift event raised but not fully resolved** → update `drift.md` with the current
  resolution status (open / asked-user / repaired).
- **Files modified in chat not yet in `touched-files.md`** → no recorded provenance, so
  record them as drift in `drift.md` (or a `questions.md` entry); never append them to
  `touched-files.md`, the candidate manifest Ship stages.

The handoff doc itself then says "synced N entries into decisions.md", not the entries
themselves. The workspace is the canonical store; the handoff is the chat-only delta.

## What to include in the handoff

1. **Suggested next action.** ONE command, not three options. If the active feature is
   mid-phase, name the next `rite-*` command. If a question blocks progress, point at
   it. If the user passed `[what the next session will focus on]`, tailor this section
   to the named focus. Where you were mid-thought, **quote the most recent next-step
   verbatim** from the chat (the exact sentence describing what to do next) so no nuance
   is lost to paraphrase.
2. **What just happened in this chat** (3-5 bullets). Distil: do not transcribe.
3. **External references** that exist only in chat: URLs, Figma links, screenshot paths,
   video timestamps the user pasted. List as references; do not embed.
4. **Live assumptions the agent is acting on** that the workspace doesn't reflect yet
   (after the sync above, this section should be near-empty: flag anything that
   remains).
5. **Tree record.** `HEAD <sha>` (`git rev-parse HEAD`) and the `git status --short` path
   count at write time, so the next session can see edits made after the handoff.
6. **In-flight work.** Every dispatch wave opened or sealed without a return (`devrites-engine
   dispatch <slug> status`), running writer handle, held claim id plus paths (`devrites-engine
   claim list`), and consumptive action started, each `terminal: yes|unknown` (`yes` only with
   an admitted return, release, `dead` claim, or proof of stop). The live handle exists only in chat. Any
   `unknown` row makes item 1 a reconcile step (`dispatch <slug> status`, `parallel status`,
   `claim list`), never a writer command: otherwise the next session dispatches a second writer.
7. **How to resume:** fixed boilerplate (see template below).

## What NOT to include

- Anything already in `spec.md`, `plan.md`, `tasks.md`, `state.md`, `decisions.md`,
  `evidence.md`, `review.md`: link by path instead.
- `git diff` output: the next agent runs `git diff` themselves.
- The full conversation transcript: distil.
- Secrets (API keys, tokens, PII, credentials). Redact aggressively.
- **New ideas the user didn't confirm.** A handoff records what *happened* and what's *next*.
  Leave out fresh suggestions, scope the user didn't agree to, and redesigns you thought of. Capture
  the state, not your opinions about it.

## Output template

Loaded on demand from [`reference/handoff-template.md`](reference/handoff-template.md).
Fill in each section and write to `.devrites/work/<slug>/handoff.md` (or to a temp
file when no active feature). Then use the compact reply contract
([`devrites-lib/reference/reply-contract.md`](../devrites-lib/reference/reply-contract.md)):

```
Done: handoff written for <slug | session>.
Changed: handoff.md plus synced workspace artifacts <n>
Evidence: not applicable; chat-only context persisted
Open: <none | unsynced caveats>
Next: <single resume command>
Record: <absolute path to handoff.md>
↻ Hygiene: /clear
```

Print the absolute path in `Record:` so the user or next agent can open it without searching.

## Session hygiene
Close with the one-line hygiene advisory + the single resume command. This skill *is* the
pre-`/clear` bridge, so it's where the advisory matters most ([`context-hygiene.md`](../devrites-lib/reference/standards/context-hygiene.md)):
```
↻ Hygiene: /clear
```
