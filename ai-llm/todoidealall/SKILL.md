---
name: todoIdealAll
description: "Sweep the user's todo file (TODO.<git user.name>.md, resolved as in the todo rules) at the end of a session: replace the text of every done ([x]) item that was worked in THIS conversation with its distilled ideal prompt (same distillation rules as /todoIdealPrompt). Done items with no dialog in this session are left untouched and listed as skipped — no honest ideal prompt can be distilled without their dialog. Ids are never assigned, renumbered, or reused. Use when the user wants to batch-update the todo file after a work session — phrases like '/todoIdealAll', 'ideal prompts for all done items', 'update prompts for done issues', 'go through the todo and update prompts'. This skill IS allowed to edit the user's todo file; that is its purpose."
argument-hint: ""
allowed-tools: Read, Edit, Glob, Grep, Bash(git config:*)
---

# /todoIdealAll

The batch counterpart of `/todoIdealPrompt --replace`: one pass over the user's todo file that
turns the session's finished work into prompt-history the user can learn from.

## What Claude does

1. **Resolve and read the user's todo file** — `TODO.<name>.md` at the repo root, `<name>`
   from `git config user.name` (the rule in `.claude/prompt-todo/RULES.md`). Never another
   user's file. Run the Autoincrement rule first, as on any touch. Edit it with the Edit tool
   only.

2. **Partition the `[x]` items**:
   - *Worked this session* — the item's dialog (prompting, corrections, confirmation) happened
     in the current conversation.
   - *Not from this session* — done earlier or elsewhere; there is no dialog to distill, so
     these are **left untouched** and listed as skipped with that reason.
   - *Ignore rows* — the user's personal tasks (the ignore tags in the todo rules, `QA:` /
     `Admin:` by default): skipped entirely, whatever their state, and not listed as
     candidates.

3. **For each session-worked done item**, distill the ideal prompt following the rules in the
   sibling skill `../todoIdealPrompt/SKILL.md` (relative to this file; read it if it is not
   already in context): a few typeable lines, imperative, every iteration-discovered constraint
   folded in, nothing the codebase or the project's rules already carry. Then replace the
   item's text in the todo file: keep the `- [x] #N KEY TAG: ` prefix exactly — ticket key and
   tag included when the item has them — first line of the prompt on the item line, overflow
   as indented `  - ` sub-bullets, every line within the **Line width** rule's limit while it
   is on (prefix and score included, split at a clause boundary). While the **Prompt scores** rule in `.claude/prompt-todo/RULES.md` is on, the
   item line ends with the original prompt's ` (N/5)` score, replacing an existing one. Open
   (`[ ]`) items are never rewritten.

4. **Reply with a summary**: per rewritten item a compact `#N: old text → new first line (N/5)`
   (the score only while it is on), and the skipped list with reasons.

## Notes

- This skill edits the user's todo file by design — the per-skill restriction that
  `/todoIdealPrompt` may only change an item's text with `--replace` does not apply here.
- Feedback bullets (what the original prompt lacked) are printed only if the user asks; the
  batch pass keeps the reply to the summary, unlike single-item `/todoIdealPrompt`.
- If nothing qualifies (no session-worked done items), say so and change nothing.
