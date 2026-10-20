---
name: capture-docs
description: At the end of a session, capture what was learned into the repo's documentation so it isn't lost and future sessions start cheaper. Use when the user says "capture docs", "save what we learned", "update docs", "sync docs", or runs "/capture-docs", typically when wrapping up. Relies on the conversation already in context plus cheap git signals — it does NOT re-research the codebase. Updates human-facing docs (READMEs, docs/) and AI-facing docs (CLAUDE.md, AGENTS.md), keeping AI docs as pointers to human docs, and ensures what it writes is discoverable from the nearest CLAUDE.md/AGENTS.md.
---

# Capture Docs

Capture the knowledge produced in this session into the repo's documentation, so it
survives the session and lowers the token cost of every future one.

Two goals drive every decision here:

1. **Avoid doc drift** — docs should match what the code and the team actually do now.
2. **Make future sessions cheaper** — up-to-date docs that are _referenced_ from
   CLAUDE.md/AGENTS.md mean the next agent reads less to get oriented.

## Core principle: spend no tokens re-researching

The session you just had is the asset. Re-reading the codebase to write docs throws
that away. So:

- **Draw from the conversation already in context** — decisions, gotchas, root causes,
  new patterns, "you must do X before Y" insights. This is the primary source.
- **Use only cheap, deterministic git signals** to find _what_ changed (file names,
  not contents). Never run a broad search or open files just to write a doc.
- **If a doc claim genuinely needs verification against a file you have NOT read this
  session, STOP and ask the user.** Name the exact file and explain why the dig is
  worth the tokens. Only proceed if they agree. Never silently burn tokens digging.

## Workflow

### Step 1 — Gather what changed (cheap signals only)

```bash
# Uncommitted (unstaged + staged + untracked)
git diff --name-only HEAD
git diff --name-only --cached
git ls-files --others --exclude-standard

# Committed during this session (heuristic; widen if the session was longer)
git log --since="3 hours ago" --name-only --pretty=format:""
```

These list filenames only — essentially free. Do not read the diffs' contents unless
the conversation didn't already explain a change and you genuinely can't document it
without looking (in which case, ask first per the core principle).

Then mine the **conversation** for doc-worthy knowledge that may not appear in any
diff at all:

- Architectural decisions and the _why_ ("chose X over Y because…")
- Gotchas / bugs discovered and their root cause
- New patterns or conventions established
- Workflow ordering ("run X before Y", "Z must be regenerated after…")
- Clarifications of non-obvious existing behavior

The user may have already committed and pushed — the diff can be empty while the
session still produced real knowledge.

If **both** sources are empty (no changed files, no doc-worthy insight), report
"Nothing new to capture" and **stop**.

### Step 2 — Locate the docs to update (auto-discover, no hardcoded map)

For each changed file (or, for a context-only insight, the directory it relates to),
walk **up** the tree to the repo root and collect the nearest of each:

- AI docs: `CLAUDE.md`, `AGENTS.md`, `AGENT.md`
- Human docs: `README.md`, and any `docs/` directory along the way

Cross-cutting insights with no natural home map to the **root** CLAUDE.md/AGENTS.md or
root README. Prefer the **most specific** doc that fits; only fall back to the root.

Only touch docs tied to something that actually changed or was learned. Skip the rest.

### Step 3 — Update the docs

For each affected location, in order:

**a) Human docs (source of truth).** Update READMEs / `docs/*.md` where they're now
stale or missing the new knowledge. Be surgical — small targeted edits, existing
heading structure preserved.

**b) AI docs (pointers, not copies).** Update CLAUDE.md/AGENTS.md. When the AI doc
would restate something a human doc already covers, replace it with a reference:

```markdown
See `docs/foo.md` for the full workflow and conventions.
```

Put session-context insights (decisions, gotchas, patterns) in the most specific
applicable CLAUDE.md/AGENTS.md.

**c) Deduplicate.** If the same content lives in both a human and an AI doc, keep the
human doc as the source of truth and make the AI doc point to it.

### Step 4 — Make it discoverable (the payoff for future sessions)

A doc nothing can reach is dead weight and won't save anyone tokens. For every human
doc you created or meaningfully changed, check that it is **reachable from a
CLAUDE.md/AGENTS.md** — directly _or transitively_. A chain is fine:
`CLAUDE.md → docs/overview.md → docs/foo.md` makes `foo.md` discoverable; don't add a
redundant direct link in that case. Only when a doc is **orphaned** (no reference
chain leads to it from any CLAUDE.md/AGENTS.md) add a single pointer, at the most
natural point in an existing chain rather than always at the root. This is what turns
"the doc exists" into "the next session finds it without searching."

### Step 5 — Format

If the repo has a markdown formatter configured (e.g. a prettier setup), run it on the
files you touched. If not, leave formatting as-is — don't introduce tooling.

### Step 6 — Report

A few bullets, no prose: which docs changed and why, which insights were captured,
what was already in sync, any duplication resolved, and any pointer you added in
Step 4. If you stopped to ask about a dig, note its outcome.

## Rules

- **Don't re-research.** Conversation + cheap git signals only. Digging requires the
  user's OK, with the file and reason named.
- **AI docs are pointers, not copies.** Reference human docs instead of restating them.
- **Don't document unchanged code.** Only what changed or what was learned.
- **Be surgical.** Small edits over rewrites; preserve existing structure.
- **Don't create files unless there's a real gap.** Prefer updating what exists.
- **Discoverability is part of the job** — an unreferenced doc isn't done (Step 4).
- **Empty diff ≠ nothing to do** — session knowledge counts even with no file changes.
