---
name: memory
description: >
  Use this skill when the user wants to build or update a persistent, fast-lookup
  memory store for a project or directory — split into short-term (active and
  frequently-needed information) and long-term (full project detail) tiers, backed
  by JSON indexes for quick "do we already know this, and where?" checks. Triggers
  include "build memory", "update memory", "remember this project",
  and self-offered check-ins when you estimate your own context usage is approaching
  roughly 25%. Always delegates the actual file reads/writes/categorization to a
  sub-agent so the main conversation's context stays clean.
---

# Memory

Builds and maintains a durable, file-based memory store for a project — so an
agent can quickly answer "do I already know this, and if not, where should I look?"
instead of re-deriving its understanding of the codebase from scratch every session.

The store lives in a `memory/` folder and splits everything it knows into two tiers:

- **`short/`** — information needed for ongoing work, or needed often: open tasks,
  recent decisions, frequently-referenced facts. Small enough to scan in full.
- **`long/`** — the complete picture: architecture, history, rationale, settled
  conventions. The detail behind the short-tier pointers.

Both tiers are backed by small JSON index files, so checking "do we know about X?"
never requires opening and reading entry files one by one.

---

## Activation

Two paths into this skill:

**Explicit invocation, anytime** — the user directly asks for it: "build memory for
this project," "update memory," "remember what we just figured out," or similar. Run
it immediately, regardless of how full your context currently is. By default it
targets the current project's root directory; if the user names a different
directory, target that one instead.

**Self-offered check-in at ~25% context** — periodically gut-check your own context
usage: have you read a lot of large files, had a long back-and-forth, worked through
several rounds of edits? When you estimate you've crossed roughly the 25% mark,
*offer* — in a short, standalone message — to run this skill before that
understanding risks being lost to summarization:

> "We've covered a fair amount of ground — want me to checkpoint what we've learned
> into memory before we go further?"

This is an offer, not a silent auto-run. If the user declines, drop it and don't
re-offer again in the same session unless something changes significantly.

---

## How it works — you delegate, you don't do the work yourself

This skill's entire job, from *your* (the main agent's) side, is to **triage
lightly, then hand off to a sub-agent**. You never read the repo, write memory
files, or build JSON indexes yourself — that all happens inside an isolated
sub-agent so none of it touches your context.

### Step 1 — Assemble a scratch-list (a few bullet points, nothing more)

Jot down what's actually new or noteworthy from this session: decisions made, files
touched, open threads, things you'd want to remember if this conversation ended
right now. This is a handful of bullets, not a transcript — just enough for the
sub-agent to know what's changed since the last pass (or, on a first run, to fold
in alongside what it discovers on its own).

### Step 2 — Dispatch exactly one sub-agent

Give the sub-agent:
- The **target directory** (current project root, or the directory the user named)
- Your **scratch-list**
- The **trigger reason** — `"user-requested"` or `"context-threshold"`

The two modes use that trigger reason differently — seed mode treats it as purely
informational (a first-time build proceeds the same way regardless of why it was
triggered), while maintain mode uses it as context for prioritizing its bounded
re-evaluation pass. You don't need to do anything differently based on which one
it is; just pass it along accurately.

Tell the sub-agent to first check whether `memory/` already exists in the target
directory:
- **If it doesn't exist**, it should follow the full instructions in
  `seed-prompt.md` (in this skill's folder) — a complete first-time build.
- **If it does exist**, it should follow the full instructions in
  `maintain-prompt.md` (in this skill's folder) — an incremental update pass.

Either way, the sub-agent reads `categorization-rules.md` and `index-schema.md`
(also in this skill's folder) before it starts, so its filing decisions and JSON
output are consistent with what the rest of the store already looks like.

### Step 3 — Relay the receipt, nothing more

The sub-agent returns exactly one line — a short status receipt (e.g. "Indexed 3
new facts, promoted 1 entry long→short, memory/ now has 19 short / 43 long
entries"). Pass that line along to the user. Do not read the files the sub-agent
wrote, do not summarize its internal reasoning — you don't have it, and you don't
need it. The receipt is the interface.

If the sub-agent doesn't come back with a clean one-line receipt — it errors out,
stalls, or returns something that isn't a short status line — don't try to inspect
or repair `memory/` yourself from the main context; you can't do that safely
without undermining the whole point of delegating. Just tell the user the memory
update may not have completed cleanly, and that re-running the skill is the right
next step.

---

## Companion files

- **`seed-prompt.md`** — full instructions for the sub-agent's first-time build pass
- **`maintain-prompt.md`** — full instructions for the sub-agent's incremental update pass
- **`categorization-rules.md`** — the three-signal rule (recency, frequency, scope)
  that decides short vs. long placement, and how re-filing works over time
- **`index-schema.md`** — the exact JSON structure for `index.json` and the two
  per-tier `_index.json` files, with worked examples and consistency rules

---

## Scope

**This skill applies to:**
- Any project or directory where an agent would benefit from persisting its
  understanding across sessions or context resets
- Both the initial build of a memory store and its ongoing maintenance

**This skill explicitly does NOT:**
- Do any of the reading, writing, or categorizing itself — that's the sub-agent's
  job, every single time, with no exceptions. This is what keeps your context clean.
- Auto-run silently at the 25% mark — it only ever offers, and only once per
  session unless something changes significantly.
- Rewrite the entire store on every pass — maintenance runs touch only what's
  changed, so `memory/`'s JSON stays small, stable, and easy to diff in git.
