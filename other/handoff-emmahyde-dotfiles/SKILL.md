---
name: handoff
description: Writes a self-contained continuity document that lets a fresh session resume your active task after a context wipe — mission, verbatim rules still in force, verified-vs-unverified ledger, wrong turns already taken, and literal TaskCreate calls that rebuild the cleared TaskList. Use when the user types /handoff, says "hand this off", "handoff", "write a handoff", "I'm about to /clear, keep going after", "resume this in a new session", or before a compaction, model swap, or overnight break where the next agent is future-you continuing the same work. For a compact state snapshot with no behavioral carry, use passoff; for a side branch that needs only its own topic, use /spinoff.
---

# Handoff — Continuity Across a Context Wipe

The next session inherits **artifacts, not context**. Everything that lives only in the conversation — the rules the user set, the corrections they made, the approaches already proven wrong — evaporates unless this document carries it.

That is the whole difference from **passoff**. Passoff answers *what is the state*. Handoff answers *what is the state, what am I still bound by, and what have I already learned the hard way*. Write a handoff when future-you continues this same work; write a passoff when someone else just needs the snapshot.

## Procedure

1. **Audit the live conversation for non-default rules.** Sweep for: constraints the user stated ("don't", "only", "keep", "stop"), corrections they made to your approach, mode flags active (register, verbosity, autonomy level, skills invoked), and division-of-labor decisions. These are the first thing lost and the most expensive to recover. Quote them verbatim — paraphrase drifts, and a drifted constraint is a broken one.
2. **Separate proven from asserted.** Every claim of done goes in the ledger with the command that proved it, or it goes in as unverified with the command that *would*.
3. **Collect the wrong turns.** Every approach tried and abandoned, with the reason. Without this the next session re-derives it at full cost.
4. **Write the document** to `~/.claude/handoffs/<name>.md` — never chat-only. A handoff that lives in the transcript dies with it.
5. **Save the task list** with `bash ~/.claude/skills/handoff/scripts/handoff-save.sh <name> --anchor "<exact fragment of a subject in your task list>"`. Task state lives in `~/.claude/tasks/<session-dir>/` and is per-session: a new session reads a different directory, so nothing migrates across `/clear`. The directory name cannot be computed, so the anchor identifies it by lookup — the one directory containing that text is yours. Ambiguous or missing anchor is a hard failure, never a guess. The script snapshots to `~/.claude/handoffs/<name>.tasks.json` beside the document; check the printed subjects against the list you can see.
6. **State the name and both paths** to the user when done.

## Picking it up

In the fresh session, create one task first — `TaskCreate` with subject `picking up handoff <name>` is enough — then:

`bash ~/.claude/skills/handoff/scripts/handoff-load.sh <name> --anchor "picking up handoff <name>"`

Then read the document it points at before acting. The task exists to make the directory findable: nothing in the environment names it, so the script locates the directory by finding the one that holds that subject.

Load merges the saved tasks straight into that directory, which the running session reads back — so the list is restored, not retyped. Ids are rewritten from `max(existing)+1` and `blocks`/`blockedBy` are remapped through the same table, so a saved task never clobbers one already in the list and dependencies survive. Only `pending` and `in_progress` tasks come across by default; the document's LEDGER already records what finished. Pass `--all` to include completed ones, `--into <dir>` for an explicit path, `--newest` to accept a recency guess instead.

The TASKS section of the document is the fallback, not the primary path — use it when the load script is unavailable or the save was never made.

## Format

Section order is fixed; empty sections are omitted. Use passoff's compressed notation for STATE and TASKS (see the passoff skill). Write MISSION, RULES, LESSONS, and MODEL in normal prose — compression that loses nuance is a defect here, not a saving.

```
# HANDOFF · <slug> · <YYYY-MM-DD HH:MM>

## MISSION
<What you are doing and why, in the user's own vocabulary. Two or three sentences. The goal, not the current step.>

## RULES IN FORCE
- "<verbatim user constraint>" — <when it applies>
- mode: <register / autonomy / skill> — <what it changes about how you work>
- correction: "<what the user pushed back on>" — <the generalized rule you took from it>

## STATE
now     <task> @file:line — <one-line state>
blocked <issue> > need <resolution>
?       <open question> — <where it surfaced>

## LEDGER
verified   <claim> — $ <command that proved it> > <result line>
unverified <claim> — $ <command that would prove it>

## LESSONS
- tried <approach> > failed because <reason>. Do not retry without <what would change>.
- assumed <belief> > wrong: <what is actually true> @file:line

## MODEL
<The working theory the next session needs to make judgment calls rather than only follow steps: architecture facts, invariants, which state the system is in when the changed code runs. Anchor every claim with @file:line.>

## RESUME
$ <first command to run>
<first action to take, in one sentence>

## TASKS
Each line is one TaskCreate call: `[priority] subject || activeForm || description`
- [H] <imperative subject> || <present-continuous> || <what and why, plus the acceptance check>
```

A filled example: `references/example.md`.

## Rules

1. **Verbatim, not paraphrased,** for every user constraint and correction. Quote marks earn their tokens here.
2. **Behavioral state is not optional.** A handoff with no RULES section is a handoff that silently reset the session's working agreement. If the sweep genuinely found none, write `RULES IN FORCE: none beyond the project defaults` — the assertion is the evidence that you looked.
3. **Every done claim carries its command.** No bare "fixed" or "works" in a handoff. Unverified is a legitimate state; unverified-and-unlabelled is not.
4. **Lessons are load-bearing.** The abandoned approaches are what keep the next session from spending its first hour re-discovering them. Include the *generalized* rule, not only the specific case.
5. **TASKS rebuild the TaskList.** Include the description and the acceptance check on each line, not just a title — the next session cannot see what you meant. Write this section even when `handoff-save.sh` ran: the JSON restores the list mechanically, the document is what survives a lost or stale snapshot.
6. **Do not invent state.** Unknown is written `? unknown`, never guessed. A confidently wrong handoff is worse than a thin one.
7. **Write it to a file** — `~/.claude/handoffs/<name>.md`, so the document and its task snapshot share a name and live together. Project-scoped work may also keep a copy under `docs/`. Chat-only handoffs do not survive the wipe they exist to survive.
