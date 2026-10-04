---
name: ask
description: >-
  Ask another project's agent a question and get its answer back — an agent
  already running in its Herdr workspace when one is open, otherwise a known
  project resolved from the herdr-workbench registry or zoxide, spun up on
  demand.
when_to_use: >-
  Use when you need an ANSWER from a different project, not just to hand it
  work — "what version of X does <project> use", "ask the api-service agent
  what port it runs on", "check with <project> whether Y is done". If you just
  want to hand off work and move on with no answer needed, use `tell` instead.
argument-hint: <project-or-fragment> <question>
version: 1
---

# Ask another project's agent

`ask` is `tell`'s round-trip sibling: same addressing, same fallback chain, but it waits for the target to actually answer and hands you back clean text instead of firing and forgetting.

## Do it

**Always run this through Bash with `run_in_background: true`** — `ask` blocks up to 10 minutes. Wait for the completion notification; do not add a sleep loop.

```bash
HERD="$SKILL_DIR/../herdr/scripts/herd.ts"

bun "$HERD" ask api-service "what port does the dev server run on?"
bun "$HERD" ask web-app/dashboard "is the migration finished?"

# --agent / --timeout / --keep-pane go BEFORE the fragment, never after
bun "$HERD" ask --keep-pane --timeout 120000 api-service "what port does the dev server run on?"
```

Resolve `$SKILL_DIR` as the `tell` skill describes.

Need a flag's exact spelling, default, or accepted values? Run `bun "$HERD" ask --help`. Never read `herd.ts` to answer that — every verb prints its own block, and `bun "$HERD" --help` lists them all.

**Flag placement is not optional.** Everything from `<fragment>` onward is the question, verbatim — this is what lets a question contain a literal `--` without being misparsed as a flag. A flag placed AFTER the fragment is not an error; it is silently swallowed into the question text, `--keep-pane` included. That means a `--keep-pane` typed at the end does nothing and the spawned pane still closes on success with no warning. Put every flag before the fragment, always.

## Addressing and fallback

Identical to the `tell` skill — read it first. Every rule in its `## Rules` applies unchanged, including the destructive-action bar when the question itself would make the target act.

The one difference in fallback behavior: a pane `ask` spawns itself gets **closed** once the answer is collected, unless the caller passed `--keep-pane`. An agent that was already running before you asked it anything is never closed, no matter what.

## How the answer comes back

`ask` does not read the target's pane — pane text can't prove an answer is complete versus a mid-turn snapshot. Instead it writes the question to a file with instructions to write the final answer to a second file ending in a fixed sentinel, sends the target a one-line pointer to that file, and polls until the agent settles (`idle`/`done`) **and** the sentinel has landed.

## Rules

**Timeout is not failure.** Default wait is 10 minutes. If it's not answered by then, the result carries `{pending: true}` plus a ready-to-run `collect` command (target + result-file path) in the `report` field. Run that verbatim to redeem the answer later — **do not call `ask` again** with the same question, since the target may still be working on the first one.

**A settled agent with no file is a real failure, not a timeout.** If the target's status goes idle/done but it never wrote a valid result, `ask` throws instead of returning pending — waiting longer will not produce an answer the target never intended to write. Report this to the user; it usually means the target ignored the file-contract instructions or hit an error before finishing.

**`collect` never closes anything.** It cannot tell a spawned pane from a pre-existing one. Only `ask` itself ever closes a pane, and only the one it spawned.

For the rest of the wrapper (`spawn`, `send`, `keys`, `wait`, `read`, `close`), see the `herdr` skill.
