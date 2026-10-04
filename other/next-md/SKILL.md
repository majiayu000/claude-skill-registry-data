---
name: next-md
description: Format and quality bar for the handoff briefing the agent maintains across sessions. Supports solo and team modes. Legacy mode — when next.projected is enabled, see skills/next-handoff-emit.md instead.
compatibility: opencode
metadata:
  audience: any-agent
  purpose: session-handoff
---
## ⚠ Mode check

This skill describes the **legacy** workflow where the agent hand-
writes the agent half of `NEXT.md`. If the project has run
`hero next migrate-to-projection` (config: `next.projected: true` in
`.hero/hero.json`), NEXT.md is now graph-projected — anything you
write to it gets wiped on the next Stop hook. Use the
[next-handoff-emit](next-handoff-emit.md) skill instead.

To check: `hero next` — if the file's `updated:` frontmatter
timestamp moves on every Stop hook, projection is on.

## What I do

Define the shape of NEXT.md — the single living artifact that lets a
fresh session (or one resuming after compaction) pick up exactly where
the last one left off.

NEXT.md is split in two halves:

| Half | Who writes it | When |
|---|---|---|
| **Agent half** — Last user ask, Just finished, Next, Blocked on, Tried and failed, Context | The agent | When the intent shifts, something fails, an approach gets rejected, or you're about to switch tools |
| **Machine half** — Branch, recent commits, working tree, hot files | `hero next checkpoint` (run by a host-tool Stop hook) | Every turn, automatically |

The agent never has to write the machine half. The harness keeps it
fresh on every turn — no agent discipline required. The agent's only
job is the agent half.

### `.hero/next/<user>.local.md` is machine-state-only

The gitignored per-machine state file `.hero/next/<user>.local.md` is
**rebuilt wholesale on every checkpoint** — it contains the marker-
bounded machine block and nothing else. **Never hand-edit it. Never
write scratch into it. Anything outside the marker block is wiped
on the next Stop hook** (the first time a wipe happens, the prior
hand-content is backed up once to `<user>.local.md.bak.<timestamp>`
so an accidental loss is recoverable, then discarded on subsequent
runs).

If you want a preserved per-machine briefing the agent doesn't touch,
write to a separately-named file such as `.hero/notes/<user>.md` —
no Hero tool reads or rewrites that path.

## Modes

Run `hero next path` to get the file path you should write to:

- **Solo mode** (default): writes `.hero/NEXT.md` — one shared briefing.
- **Team mode** (`next.mode: "team"` in `hero.json`): writes
  `.hero/next/<user>.md` — your personal briefing.

In team mode, also update your one-liner in the shared `.hero/NEXT.md`
roster so teammates see what you're working on.

## When to use me

- **At session start:** read your NEXT file (via `hero next path`) before
  doing anything else and surface it to the user.
- **During the session:** the agent overwrites the agent half when the
  triggers below fire. The Stop hook keeps the machine half fresh; you
  do not need to run it manually.

## Format

The agent owns everything *above* the `<!-- BEGIN HERO MACHINE STATE -->`
marker. Always overwrite the entire agent half. Never append. Aim for
15-40 lines in the agent half; hard cap 60.

```markdown
---
updated: 2026-04-22T15:30:00Z
session: <host-tool>/<model>
branch: <git-branch>
---

## Last user ask
<1-3 lines, the user's own words, from their most recent meaningful
turn. The single most expensive thing for a fresh session to recover.>

## Just finished
<What shipped this turn. Commit hash + message if one was made.
Note any uncommitted state.>

## Next
<The concrete next step. One short paragraph plus a runnable pointer.>

→ <runnable pointer: a slash command, spec path, or shell command>

## Blocked on (omit if clear)
<Test failures, build errors, things you got stuck on. Include the
actual error message or file/line.>

## Tried and failed (omit if N/A)
<Approaches that didn't work, so the next session doesn't suggest them
again. One line per rejected idea.>

## Context to carry forward (omit if nothing meaningful)
<Non-obvious decisions, user preferences, open questions. Compaction-
survival kit, not a transcript.>

## Proposed next ask
<One paste-ready sentence the user could say to resume productive
work. Phrased as the user would phrase it, not as instructions to
the agent. The "when in doubt, just look it up" answer for the next
session opener.>

<!-- BEGIN HERO MACHINE STATE -->
[…auto-written, do not touch…]
<!-- END HERO MACHINE STATE -->
```

## Section guidance

- **Last user ask** — quote the user's wording. Don't paraphrase. A fresh
  session reading this should immediately know what the user wants. If
  the last meaningful ask was 3 turns ago and the recent turns have been
  conversational, quote that earlier ask.
- **Just finished** — one bullet per concrete thing. Skip if you only
  read code or had a discussion. The machine half already lists commits
  and dirty files; only mention what's *interesting* (e.g. "shipped X,
  but uncommitted because Y").
- **Next** — concrete next step plus the `→ <pointer>` line. The pointer
  must be runnable.
- **Blocked on** — only if actually stuck. Copy the real error.
- **Tried and failed** — gold. One line per rejected approach.
- **Context to carry forward** — only what isn't derivable from `git log`,
  the spec corpus, or the codebase. Skip the heading entirely if empty.
- **Proposed next ask** — the user's perspective, paste-ready. One
  sentence, no command names, no file paths unless the user would
  naturally name them. The bar: a fresh session that pastes this
  verbatim should kick off productive work without needing to read
  the rest of the file. Think *"continue with the e2e suite for
  discovery, same shape as onboarding"*, not *"run scripts/e2e/
  discovery.sh"*. Skip if the next move genuinely depends on the
  user's state (e.g. they're about to make a strategic decision
  only they can make).

## When to update the agent half

The Stop hook handles the machine half every turn — the auto-half also
auto-summarizes commits + AC status flips since the prior checkpoint,
so most "what just happened" is captured for free.

The single rule for the agent half:

> **Read the file as it stands. Could a fresh session pick up correctly
> from this right now? If no, update it. If yes, leave it.**

Apply this rule before handing back to the user, before invoking another
agent or skill, and any time you're about to claim a piece of work is
done. The bar is *correctness of the handoff*, not "did anything change."

Concrete failure modes that flip the answer to **no**:

- The "Last user ask" no longer reflects what the user actually wants
  (intent shifted, or the user gave new instructions).
- "Just finished" omits a meaningful commit or spec status change a
  fresh session would need to know about.
- "Next" points at work that's already done, or doesn't exist anymore.
- "Blocked on" is silent about a real blocker, or claims one that's
  been resolved.
- "Tried and failed" is missing an approach you just rejected — the
  next session would re-suggest it.

If none of those apply, leave the file alone. Conversational turns
(*"explain this", "what would you suggest"*) almost never flip the rule.

Don't write a fresh agent half just because commits landed — the
machine half lists those automatically. Update the agent half when the
**narrative** would mislead a fresh session, not when the activity log
grew.

## Quality bar

A good NEXT.md is one a fresh session can read and immediately be
productive without asking "what were we doing?"

The new session should know:

1. **What the user actually wants** — last user ask, in their words
2. **What just shipped** — agent half + machine commits
3. **What's blocked** — actual error messages
4. **What to do next** — a runnable pointer
5. **What NOT to try** — approaches already rejected

If you can't picture a fresh session being productive after reading it,
add detail. If it's becoming a transcript, cut detail.

**Hard cap on agent half: 60 lines. Target: 15-40.** If you need more,
move detail to `.hero/knowledge/notes/` and link it.

## Shared file (team mode only)

In team mode, `.hero/NEXT.md` is the team's shared file with two roles:

### 1. Roster — always update your line

```markdown
## Working on

- **chet-bellows**: delivering challenge-diagnosis spec (Apr 23 14:30)
- **alice**: fixing auth timeout bug #142 (Apr 23 11:15)
```

### 2. Updates — only when something affects others

```markdown
## Updates

### Apr 23 — chet-bellows
Shipped drift detection — `hero drift` is live, affects all spec workflows.
```

Most turns don't warrant a team update. If unsure, skip it.

## What not to do

- Don't append history — overwrite the agent half every time.
- Don't touch the `<!-- BEGIN HERO MACHINE STATE -->` … `<!-- END … -->`
  block. The Stop hook owns it.
- Don't write a fresh agent half after every prompt. Only when something
  in the trigger list above fired.
- Don't include large diffs, code snippets, or full spec contents — point
  at the artifact instead.
- Don't paraphrase what's already in the spec corpus or the codebase.
  The handoff is the *delta* not visible elsewhere.
- **Don't hand-edit `.hero/next/<user>.local.md`.** It is rebuilt
  every checkpoint and any content you write outside the marker
  block will be discarded. Use `.hero/notes/<user>.md` (or any
  path not under `.hero/next/`) for preserved per-machine notes.

## CLI commands

| Command | What it does |
|---|---|
| `hero next` | Show your briefing |
| `hero next path` | Print the file path the agent should write to |
| `hero next checkpoint` | Refresh the machine half (the Stop hook does this automatically; `/handoff` does it manually) |
| `hero next team` | Show all team members' recent handoffs |
| `hero next shared` | Show the project-level shared NEXT.md |
| `hero next migrate` | Move existing .hero/NEXT.md into .hero/next/<user>.md |

## Configuration

In `hero.json`:

```json
{
  "next": {
    "mode": "team"
  }
}
```

Omit entirely or set to `"solo"` for the default single-file behavior.
