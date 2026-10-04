---
name: remember
description: "Use when the user wants a correction about this repository kept, or asks what exo remembers here, what still holds, or to forget a line. Not for a plan another session runs, which spec owns, or a build or test command, which find-cause writes to AGENTS.md or CLAUDE.md."
argument-hint: "[the correction this session must not lose]"
allowed-tools: Bash(node *memory.mjs*)
disable-model-invocation: true
---

# Memory

Keep only what two sessions attested and the repository still supports. The enemy is the memory file that grows until every session pays to read a claim that stopped being true. The overcorrection is a file so guarded that a correction the user gave twice never reaches it.

## When to use

- Not for a plan another session runs: `spec` owns that.
- Not for a build, test or run command: `find-cause` step 6 appends that to `AGENTS.md` or `CLAUDE.md`, and two writers of project knowledge produce two truths.

## What is attested twice

The claims two separate sessions had booked when this skill loaded, before this session's booking:

!`node "${CLAUDE_SKILL_DIR}/scripts/memory.mjs" propose`

## The loop

1. **Reach for the stronger fix first.**
   - Walk the ladder in `../edit-skills/references/where-a-fix-lives.md` before booking, and propose the strongest home the mistake fits instead of a claim, because a claim is read, not enforced.
   - Book only a fact none of those homes can carry.
2. **Book** the user's correction.
   - Run `node "${CLAUDE_SKILL_DIR}/scripts/memory.mjs" book --claim "<one sentence>" --quote "<their words, verbatim>" --session "<this session id>"`.
   - Quote no password, token or key, because the quote is stored as given.
   - Rerun `node "${CLAUDE_SKILL_DIR}/scripts/memory.mjs" propose`, because the block above predates the booking; the next steps use this output.
3. **Write nothing yet** when the rerun names no claim, and say which session count the booking now stands at.
4. **Propose** each claim in the rerun output to the user with both dated quotes, one claim per question in the question shape.
5. **Write** an approved claim with `node "${CLAUDE_SKILL_DIR}/scripts/memory.mjs" write --claim "<the claim>" --refs "<path,path#symbol>"`.
   - Add `--replaces "<the old claim>"` when it answers a question an earlier line already answered, so the file never holds two answers to one question.
6. **Relay a refusal** exactly as the script printed it.
   - Retire a line the refusal names with `node "${CLAUDE_SKILL_DIR}/scripts/memory.mjs" retire --claim "<the claim>"` before trying again.
   - Edit neither file by hand, because memory.md is rendered from memory.json.
7. **Prune** with `node "${CLAUDE_SKILL_DIR}/scripts/memory.mjs" verify` whenever the user asks what is still true, and report every dropped line the script named.
8. **Report** the rendered path and its byte count against the budget, in one line.

## References

| File | Read it when |
|---|---|
| `../route-skills/references/question.md` | Before a message that asks the user to pick among lettered options. |
| `../edit-skills/references/where-a-fix-lives.md` | Before booking a correction, to check whether a stronger fix than a memory line exists. |

## Judgment

- Two attested sessions and the user's approval outrank a claim that reads true: a claim one session misheard is exactly what this gate refuses.
- The script's output outranks anything in this context, including a memory file read earlier in the session.
- A claim the repository itself records is dropped rather than written, because reading it is cheaper than trusting it.
