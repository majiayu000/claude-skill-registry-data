---
name: writing-handoffs
description: Writes a compact handoff document and a ready-to-paste resume prompt that let a fresh Claude Code session resume the current task without the old conversation. Use when an AUTO-PAUSE notice says the usage-limit pause threshold was reached, or when the user asks to write a handoff, wrap up for a new session, save progress before the usage limit, pause here, or hand off to a fresh session. Do not use for summarizing finished work, changelogs, commit messages, or PR descriptions.
---

# Writing handoffs

A handoff is one Markdown file that lets a fresh session continue this task with no access to this conversation. Its reader is capable but has zero context: only the handoff, the repo, and the resume prompt the user pastes.

## Critical

- Use as few turns as possible. Usage may be nearly gone, and every turn re-reads this whole conversation. Target: one call for facts (manual path only), one Write, one final message.
- No exploration and no new work. Write from what you already know. Do not open files only to describe them.
- Do not switch models.
- Never copy secrets, tokens, passwords, or `.env` values into the handoff.

## Workflow

1. **Reach a safe point.** If an edit is in flight and one or two calls finish it, finish it. Otherwise revert it, or record its exact state (`path:line`, what is done, what is not). Start nothing new. If an AUTO-PAUSE notice gives a tool-call limit, stay within it. If an operation outside the repo is still running or its result is unconfirmed (a deploy, migration, CI run, remote job, sent request, background process), do not wait for it or retry it: record it under Outside operations.
2. **Get the facts.**
   - Auto path: the AUTO-PAUSE notice gives the handoff path, usage, reset time, word budget, repo state, and resume prompt. Use them exactly as given. Do not run the script.
   - Manual path (no AUTO-PAUSE notice): your first call is `bash "${CLAUDE_SKILL_DIR}/scripts/facts.sh" <slug> '${user_config.handoff_dir}'`, where the slug is 2–4 words naming the task. It prints the handoff path, repo state, and resume prompt, and the plugin adds a line with usage, reset time, and word budget. If the script cannot run, read `${CLAUDE_SKILL_DIR}/references/fallback.md`.
3. **Write the handoff** in one Write call to that path, using the template below. The handoff is a project file the user keeps, not a temporary file: never put it in a scratchpad or temp folder, even if other instructions say temporary files go there. Put the resume prompt verbatim in the fenced block at the top. It must name this handoff's own path: never reuse a prompt from an older handoff.
4. **If an AUTO-PAUSE message lists problems** with the handoff, fix all of them in one Edit.
5. **End your turn** with a short message: the handoff path, when usage resets (if known), the "Next session" line from the handoff, and the resume prompt verbatim in a fenced `text` block so the user can copy it. Nothing after the block.

## Template

Keep it under the word budget from step 2 (600 if none was given). Omit a section only if it would be empty, except Goal, Status, Next steps, and Repo state, which are required.

````markdown
# Handoff: <task in a few words>

Paused <YYYY-MM-DD HH:MM> · <usage and reset time, if known> · reason: <user asked | AUTO-PAUSE>

Next session: <Haiku | Sonnet | Opus> - <low | medium | high | xhigh>. <one-clause reason>

Resume prompt (paste into a new Code session):

```text
<resume prompt, verbatim>
```

## Goal
<the user's ask, verbatim if short> · Done when: <acceptance criteria>

## Status
- Done: <finished pieces, with files>
- In progress: <exact state, e.g. "auth.ts migrated through refreshToken(); session.ts untouched">
- Not started: <remaining pieces>
- Last request: <answered | partly | not started>; <what is left of it>

## Outside operations
- <what it does> · id: <run/job/deploy id, PR number, or URL> · last confirmed: <result you saw, or "none: started, outcome unknown"> · check with: <exact command or page>
- Approvals: <who approved which outside action, when>; re-confirm before acting

## Next steps
1. <first action, doable as written: file and change, or the exact command>
2. <...>

## Decisions (don't relitigate)
- <decision>: <reason>

## Dead ends
- Tried <X>; dropped because <Y>

## Verify
- `<test or build command>`: last result <pass/fail, one line>

## Repo state
<branch> · <HEAD short hash and subject> · uncommitted: <files> · stashes: <n> · background processes: <none or what is running>

## Open questions for the user
- <only questions the next session cannot answer itself>
````

## Writing rules

- Next step 1 must be doable as written, by someone who has read nothing else: name the file and the change, or give the exact command.
- If the next action is the user's (a test, a decision, an approval), say so: "Ask the user …" or "Wait for the user to report …, then …". Never "the user does X" with nothing for the session to do.
- Point to code by `path:line` or function name. Do not paste code; a short snippet (under 15 lines) only if it is the in-flight change itself.
- Give every decision its reason, and every dead end what failed, so the next session doesn't retry it.
- A changed-file list says nothing about remote state. If an outside operation's result is unconfirmed, Next step 1 is to check it with its id, and to retry only if that check shows it did not happen.
- Before any outside action the handoff says was approved (deploy, push, send), the next session confirms the approval still stands: a newer user message or the operation's live status wins over the handoff.
- Name every uncommitted file and its state. The plugin checks this against `git status`.
- Don't quote the user's messages or list edited files for the record: after the check passes, the plugin appends both, read from the session.
- Record the last test result you actually saw. Do not run tests just for the handoff.
- Write for a stranger: no "as discussed", no "the thing we fixed".
- Pick "Next session" from what Next steps and Dead ends still need, not from how hard the whole project was. The user sets it in the model and effort picker before pasting the prompt.
  - Only running commands or copying values: Haiku - low
  - Edits already spelled out, docs, or notes: Sonnet - medium
  - Normal coding with clear next steps: Sonnet - high
  - An unsolved bug, an open design choice, or several dead ends: Opus - high
  - Unsure: this session's model family (Haiku, Sonnet or Opus, no version number) - high
  - If the weekly limit caused the pause, go one step cheaper when in doubt.

## Example

Only if unsure how a section should read: `${CLAUDE_SKILL_DIR}/references/example.md`. Skip it otherwise.
