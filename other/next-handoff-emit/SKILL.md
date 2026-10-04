---
name: next-handoff-emit
description: When and how to emit handoff state (UserAsk / NextSuggestion / SessionReflection) to the graph during work, so the projected NEXT.md and per-user handoff stay current without agent discipline on a tracked file.
compatibility: opencode
metadata:
  audience: any-agent
  purpose: session-handoff
  applies_when: next.projected = true (after `hero next migrate-to-projection`)
---

## What I do

Tell the agent when to fire three small CLI calls during normal work,
so the user-graph nodes that drive `.hero/next/<user>.md` and the
field-grab CLI (`hero next suggest`, `hero next ask`,
`hero next reflection`) stay current — *without* writing to a
markdown file that the next checkpoint will clobber.

This skill replaces the "write the agent half of NEXT.md" pattern in
[skills/next-md.md](next-md.md) when `next.projected` is true. With
projection on, anything you write into NEXT.md gets wiped on the next
Stop hook. Emit structured events instead.

## Why emit, not write

NEXT.md is a graph projection. Every Stop hook regenerates it from:
- Recent commits, AC flips, open features, blockers — derived from
  the project graph (no agent action needed).
- Last user ask, Suggested next prompt, Session reflections —
  attributed user-graph nodes, populated by the three commands below.

If you want something to survive into the next session's NEXT.md, it
has to land as a graph node. The CLI is the one-liner way to do that.

## The three commands

### `hero next ask "<text>"`

Records a `UserAsk` node attributed to the current user. Singleton
per user — the latest supersedes prior. The projection renders this
as the **"Last user ask"** section.

> **Auto-emit:** as of `next-auto-emit-user-ask`, the end-of-turn Stop
> checkpoint (`hero next checkpoint`) automatically records the user's
> **last** transcript message as the `UserAsk` whenever the harness
> supplies a `transcript_path` (Claude Code does). So this command is
> now a **manual override**, not a per-turn requirement — fire it only
> when you want to record something other than the verbatim last
> message (e.g. a one-line paraphrase of a long, wandering prompt).
> Singleton supersession means your override cleanly replaces the
> auto-emitted node, and vice versa, with no duplicates.

When to fire:
- **Every meaningful user prompt.** Right after the user finishes
  asking for something concrete, before you start working on it.
- Quote the user's wording when short and direct. Paraphrase to one
  sentence when the prompt is long, conversational, or wandering.
- Skip when the user is making small talk, asking a clarifying
  question about your previous output, or otherwise not directing
  new work.

Examples:
```bash
hero next ask "Finish phase 4 of next-as-projection — wire UserHandoffMD into checkpoint"
hero next ask "Why does the test fail intermittently on the auth middleware?"
hero next ask "Let's try a different approach — instead of refactoring, just delete the dead branch"
```

### The session goal — emit `<!-- hero:goal: <one-line goal> -->`

The handoff also captures the session's **goal** (the durable intent —
*why* the work is happening) as a separate `SessionGoal` node, distinct
from the volatile last-ask. The goal is captured **automatically** every
checkpoint from the transcript's opening messages — no command required.

You can sharpen it for free: **once you understand the goal, emit it as a
one-line HTML comment in your response —**

```
<!-- hero:goal: add rate limiting to the login endpoint to stop credential-stuffing -->
```

The Stop-hook checkpoint greps your assistant messages for the **last**
such marker and records it as the session goal (priority `marker`, which
overrides the auto-derived opening-window goal but not a manual override).
It is invisible in rendered markdown, costs no extra call (it rides the
response you're already writing), and gives the next session model-quality
intent. Emit it once when the goal crystallizes, and again only if the
goal genuinely changes mid-session.

The marker is **optional upside** on top of the always-on window goal — if
you never emit one, the floor still captures a reasonable goal from the
opening exchange. Use it when the real intent isn't obvious from the first
few messages (a session that opened with throat-clearing, or pivoted).

#### `hero next goal "<text>"` — the manual override

For the rare case where even the marker is wrong, `hero next goal "<text>"`
records a **manual** goal that supersedes every auto/marker goal. With no
argument it prints the current goal. This is a quality ceiling, not a
requirement — fire it only to correct a wrong auto-derived opener.

```bash
hero next goal                                              # print current goal
hero next goal "stop credential-stuffing on the login endpoint"
```

Do **not** use `hero next goal` for the latest prompt — that is what
`hero next ask` owns. The goal is the session's durable WHY; the ask is
the most recent refinement.

### `hero next suggest "<text>"`

Records a `NextSuggestion` node. Singleton per user. The projection
renders this as **"Suggested next prompt"** in the per-user handoff.

When to fire:
- **At the end of a meaningful work unit** (commit landed, phase
  shipped, blocker hit and parked). Phrase it as *the user's next
  prompt*, not as instructions to yourself.
- The bar: a fresh session pasting this verbatim should know
  immediately what to do.

Crucial framing — write in the user's voice:

| ❌ Wrong (agent-instructions voice) | ✅ Right (user-voice prompt) |
|---|---|
| `"Run hero next migrate-to-projection then ship phase 8"` | `"run the migration and then we gotta do phase 8 right..."` |
| `"Implement Phase 5 round-trip ingest with idempotency"` | `"let's tackle phase 5 of next-as-projection, the round-trip"` |
| `"Fix the auth middleware test"` | `"why does the auth middleware test fail intermittently?"` |

If genuinely no good next prompt exists (e.g. the user is about to
make a strategic decision only they can make), don't emit — leave
the field blank rather than fill it with noise.

### `hero next reflection "<text>"`

Records a `SessionReflection` node. Multiple co-exist; the projection
shows the most recent N. The projection renders these as
**"Recent reflections"**.

When to fire:
- **When a non-obvious lesson surfaces** — a constraint nobody told
  you, a gotcha you discovered, a surprising data point worth
  carrying into the next session.
- One sentence. Like a sticky note. The lesson, not the action.
- Skip mechanical observations — those land in commit messages or
  the project graph automatically.

Examples:
```bash
hero next reflection "config.Load reads from .hero/hero.json, not project root — silent no-op if you write to the wrong place"
hero next reflection "merge=ours plus stop-hook regen is cleaner than a custom merge driver for v1"
hero next reflection "MCP tool count is 35; README still says 25+"
```

## Cadence

A normal session looks like:

| Event | Action |
|---|---|
| User sends a prompt that directs new work | `hero next ask "..."` |
| The session's real goal crystallizes | emit `<!-- hero:goal: ... -->` (once) |
| Phase / commit / meaningful unit lands | `hero next suggest "..."` |
| Surprise / lesson / gotcha surfaces | `hero next reflection "..."` |
| Conversation, clarification, or small question | nothing — let it pass |
| End of turn | the Stop hook handles the rest |

Aim for **1-2 emits per meaningful turn**. Quality over quantity. A
single high-signal `hero next ask` and `hero next suggest` is better
than five vague ones.

## What NOT to emit

- Don't fire `hero next ask` for every user message — only when the
  intent actually shifts or a new ask arrives.
- Don't `hero next suggest` if the next move depends on the user
  making a decision only they can make. Leave it empty.
- Don't reflect on mechanical observations the graph already
  captures (commits, AC status, blockers).
- Don't write to `.hero/NEXT.md` directly when projection is on —
  it'll be wiped next turn. Use the commands.
- **Don't write scratch into `.hero/next/<user>.local.md`.** That
  file is machine-state-only and rebuilt wholesale on every
  checkpoint — anything outside the marker block is discarded (with
  a one-time backup to `.local.md.bak.<timestamp>` the first time
  hand-content is detected). For preserved per-machine notes the
  agent doesn't touch, use a path like `.hero/notes/<user>.md`.

## Reading state

To check what's currently recorded:

```bash
hero next suggest                   # print suggested next prompt
hero next ask                       # print last user ask
hero next goal                      # print the session goal (durable intent)
hero next reflection                # print recent reflections
hero next                           # full handoff (project + user + machine)
```

Add `--json` to any read for scripting; `--copy` to also copy to
clipboard; `--user <slug>` to read someone else's (in team mode).

## Cross-machine continuity

The `.hero/next/<user>.md` file is the load-bearing artifact for
solo-no-Cloud cross-machine handoff. When you push from one machine
and pull on another, the next `hero scan` (or session-start) ingests
the file's content back into the local graph automatically.

This means the cadence above also gets you cross-machine continuity
for free — emits on home laptop become readable on office desktop
after a git pull, even with no Cloud configured.
