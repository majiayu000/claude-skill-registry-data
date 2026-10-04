---
name: passoff
description: Emits a token-conservative symbolic-notation snapshot of session state — in-progress and completed work, remaining tasks, references, and literal TaskCreate seeds for rehydrating a cleared TaskList. Use when the user types /passoff, says "pass off", "prep for /clear", "summarize state for next session", or wants current state transferred compactly to a teammate, a spinoff split, or future-self. For a full-continuity resume of your own active task after a context wipe — behavioral rules and lessons included — use the handoff skill instead.
---

# Passoff — Compressed Session Snapshot

Goal: hand the reader the state of play in the fewest tokens that preserve intent. Optimize fidelity-per-token, not prose.

## When to invoke

User types `/passoff` or asks for a state dump; before `/clear`, compaction, or a model swap; end of a working session.

Sibling skills: **handoff** — this session's work resumed by a fresh you, carrying behavioral state and lessons, not just task state. **`/spinoff`** — a side branch needing only enough context for its own topic. Pass a passoff as the 3rd argument to `bash ~/.claude/scripts/spinoff-session.sh <task-file> [model] <passoff-file>`, or pipe the text on stdin when no file exists.

## Core principle: legend defines meaning

Any single-token word or symbol can mark any concept — provided the legend binds it. The notation is not sacred; the legend is. Bind `now` to in-progress and `now` means in-progress for that document; bind `>>>` or `xyz` and the same holds.

So: pick whatever reads best for the audience, reuse short tokens across roles when the legend stays unambiguous within the document, and never list a marker you did not use.

Default to English words. Reach for a symbol only when the English equivalent costs two or more tokens. Rationale, the full cheap-token list, and the avoid-list: `references/token-economy.md`.

One caveat that bites at emit time: `>` at the start of a line is a markdown blockquote. Keep `>` inline; start lines with `-` or a header.

## Default output format

Fixed order. Empty sections are omitted, not left blank. Apply the compression rules to every line.

```
# PASSOFF · <slug> · <YYYY-MM-DD HH:MM>

## LEGEND
now in-progress   done completed   next upcoming   blocked stuck   drop abandoned ?  open question   ref pointer   note decision
>  causes    =>  implies    <-  depends on    @path:line   #branch   $cmd
[H/M/L] priority   {S|M|L} effort   ~approx

## NOW
- <task> @file:line — <one-line state>  blocked:<blocker>

## DONE
- <task>  > <outcome>  ref:<commit|file>

## NEXT
- [H] <task>  because <reason>  {S|M|L}
- [M] <task>  > unblocks <thing>

## BLOCKED / OPEN ?
- blocked: <issue>  > need <resolution>
- ? <question>  note:<where surfaced>

## NOTES
- <decision>  because <reason>  ref:<file/commit>

## REFS
- code: @path:line — <why matters>
- docs: <path/url> — <contents>
- prior: <sha|PR#|session-id> — <topic>
- skills: /<skill> — <when to invoke>

## RESUME
$ <exact command(s) to pick up>
#branch · uncommitted: <count> · tests: <pass/fail/unrun>

## REHYDRATE TASKS
Next agent: each line = one TaskCreate. Format: `[priority] title || activeForm`.
- [H] <imperative title> || <present-continuous active form>
```

Worked examples at two densities: `references/examples.md`.

## Compression rules

Full caveman register on every prose-bearing line — the complete ruleset, intensity calibration, and per-line self-check are in `references/caveman-style.md` (vendored; the upstream plugin is not required).

1. **Legend governs.** Pick markers, bind them, use them consistently. Different documents may bind differently.
2. **Trim the legend.** Only entries the body actually uses.
3. **Caveman prose, full intensity.** Drop articles, copulas where the subject is obvious, filler, pleasantries, hedging. Fragments fine. Pattern: `[thing] [action] [reason]`. `Bug @auth/mw.py:84 — token expiry uses < not <=`, never a sentence explaining it.
4. **One line per item.** Wrap only when a thought genuinely does not fit.
5. **Cite, do not summarize.** Findings over one line become gist plus `ref:<location>`.
6. **Tag NEXT with priority and effort** so the reader sequences without re-deriving.
7. **RESUME is literal.** Exact command, exact branch, copy-paste-runnable. <MANDATORY>Never omit it.</MANDATORY>
8. <REQUIREMENTS>**Preserve exact strings** for errors, paths, shas, env vars, commands. Compression applies to prose, never identifiers.</REQUIREMENTS>
9. **REHYDRATE TASKS mirrors NEXT.** Same items recast for direct `TaskCreate` consumption — the TaskList clears across `/clear` and session boundaries, so the next agent rebuilds it. Format `[priority] imperative title || activeForm`; no markers in the title, no commentary.
10. **Auto-clarity escape hatch.** Drop the register for security warnings, irreversible-action warnings, and any fragment ordering that could be misread. A destructive RESUME command gets a normal-prose warning line above it, then the register resumes.

## Sourcing state

Pull in this order: the current conversation (what was just worked on, decided, or left half-finished); `git status` and `git log -5`; the active TaskList; branch and worktree state; and open questions the user raised — those are the most expensive context to recover, so they are never dropped.

<MANDATORY>
Do not invent state. Unknown → omit the section or mark `? unknown`.
</MANDATORY>

## Anti-patterns

<ALERT>
- ✗ Prose paragraphs. Compress them.
- ✗ Restating file contents. Point with `@path:line`.
- ✗ Vague NEXT items (`improve performance`). Use concrete predicates: `batch X chunks of N`.
- ✗ Dropping RESUME. Highest-leverage line in the document.
- ✗ Legend entries the body never uses.
- ✗ Bracketed markers (`[done]`, `[x]`). Two extra tokens each; use bare.
- ✗ Color emoji. Two tokens each plus variation selectors.
- ✗ Inventing state. Mark `? unknown` or omit.
</ALERT>
