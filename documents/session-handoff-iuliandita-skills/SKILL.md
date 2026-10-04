---
name: session-handoff
description: >
  Write an agent session handoff with current state, decisions, unfinished work, verification, and next steps.
license: MIT
compatibility: "None - writes a markdown file. Optional: git for gitignoring the .handoff/ directory"
metadata:
  source: iuliandita/skills
  date_added: "2026-06-13"
  effort: medium
  argument_hint: "[purpose of next session] | resume <path>"
---

# Session Handoff: Move Context Between Agent Sessions

Compress the current session into a small markdown document another agent session can continue
from. A handoff is a one-way, lossy carry: whatever the next session needs has to be written
down explicitly, because everything else is gone.

The point is to keep each session focused and inside its high-attention context window
instead of dragging one bloated thread forward.

Inspired by Matt Pocock's `/handoff` skill. The failure mode it exists to prevent is
**relitigation**: the next session reopens a decision the current one had already settled,
because the doc recorded *what* was decided but not *why*. Every locked decision carries its
rationale for this reason.

## When to use

- Switching roles across sessions: planner -> implementer, implementer -> reviewer
- Kicking off an AFK or unattended run from a clean context
- Fanning out to parallel sessions that each own one slice of the work
- Prototyping or spiking in a throwaway session without polluting the current one
- The current context window is full or degrading and you want a fresh start with only essentials
- User says "hand this off", "write a handoff", "continue this in a fresh session"

## When NOT to use

- Capturing feature ideas or backlog items - use **roadmap**
- Running the full branch -> implement -> test -> PR -> merge workflow - use **dev-cycle**
- Choosing a skill for the current request - use the host's normal skill selection.
- Writing durable project documentation, READMEs, or changelogs - use **update-docs**
- Composing commit, PR, or MR text - use **git**
- A heavyweight, phase-coupled pause inside a GSD planning workflow - use GSD's `pause-work`.
  This skill is the lightweight, plugin-agnostic version: one disposable doc, no phase state

---

## AI Self-Check

Before writing or returning a handoff doc, verify:

- [ ] **Purpose stated**: the next session's job is one or two clear sentences at the top
- [ ] **Decisions carry rationale**: every locked decision says *why*, not just *what*, so the
      next session does not relitigate it
- [ ] **State is tagged**: each current-state item is marked `verified`, `assumed`, or `blocked`
      so the next session knows what it can trust without rechecking
- [ ] **Pointers, not paste**: artifacts are referenced by path, `file:line`, PR, or branch -
      not copied in, which would bloat the carry and drift from the source
- [ ] **No secrets**: API keys, passwords, tokens, PII, credential-bearing URLs, and sensitive topology are redacted
- [ ] **Suggested skills listed**: the next session is told which skills to invoke for its task
- [ ] **Small enough to fit**: the doc is short enough to sit in the next session's
      high-attention zone - if it is long, cut detail and lean harder on pointers
- [ ] **Gitignored**: `.handoff/` is in .gitignore unless the user asked to commit the doc
- [ ] **Spec claims verified**: pointers (paths, line numbers, PR numbers, branches) are confirmed to exist at write time, not assumed
- [ ] Cross-cutting agent hygiene applied - see `references/agent-hygiene.md`

---

## The handoff document

One purpose-driven markdown file. Sections in this order; omit a section only when it is
genuinely empty.

```markdown
# Handoff: {one-line purpose}

> Written: {date} | {Disposable working doc | Committed for review} | From: {short note on the source session}

## Purpose

{What the next session is for. One or two sentences. The single most important field -
if the next agent reads only this, it should still know what to do.}

## Locked decisions

Settled. Do NOT reopen these.

- {Decision} - because {rationale}
- {Decision} - because {rationale}

## Deferred

Deliberately not doing now. Recorded so the next session does not relitigate them. Omit if empty.

- {Ruled out for now} - because {rationale}; revisit when {trigger}

## Current state

- [verified] {Done and confirmed} - confirmed by {test, command, or observation}
- [assumed] {Believed true but unchecked} - verify by {command or check} before relying on it
- [blocked] {Stuck} - waiting on {what}

## Next steps

1. {Concrete action}
2. {Concrete action}

## Pointers

References, not copied content.

- `{file:line}` - {what is there}
- PR #{n} / branch `{name}` - {status}
- `{spec or doc path}` - {what it covers}

## Suggested skills

- **{skill}** - {why the next session needs it}
```

Keep it lossy on purpose. A handoff is not a transcript; it is the minimum the next session
needs to act without re-deriving context. When in doubt, point at the artifact rather than
pasting it.

---

## Performance

- Write one handoff per next-session purpose. Fanning out to three parallel sessions means
  three focused handoffs, not one doc the readers must filter.

## Workflow

### Mode 1: Author a handoff (default)

Copy this checklist and track progress:
- [ ] Step 1: Next session's purpose named
- [ ] Step 2: Decisions recorded with rationale
- [ ] Step 3: State tagged `verified`, `assumed`, or `blocked`
- [ ] Step 4: Pointers confirmed and secrets redacted
- [ ] Step 5: Next steps and skills listed
- [ ] Step 6: Self-Check passes (fix the failing item in its step and re-check), file written

#### Step 1: Name the next session's purpose

State, in one or two sentences, what the next session is for. If the user gave a purpose as the
argument, use it. If not, infer it from the current work and confirm in the doc's Purpose
section. Everything downstream is selected to serve this purpose - context irrelevant to it is
dropped.

#### Step 2: Extract decisions and their rationale

Walk the current session for decisions that are settled: choices of approach, tradeoffs
resolved, things ruled out. For each, record the decision and the reason it was made. The
rationale is not optional - it is the specific thing that stops the next session relitigating.

#### Step 3: Capture state, tagged by confidence

Summarize where things stand. Tag each item:

- `verified` - done and confirmed, with how it was confirmed
- `assumed` - believed true but not checked; name the command or check that would verify it, so
  the next session can confirm before relying on it
- `blocked` - stuck, and on what

Do not present assumptions as facts. A mistagged assumption is how the next session inherits a
bug as a foundation.

#### Step 4: Collect pointers, redact secrets

Reference the artifacts the next session needs: `file:line`, spec and doc paths, PR numbers,
branch names. Confirm each pointer resolves at write time - check that the file and line exist
rather than trusting a remembered location, because a stale line number sends the next session
to the wrong place. Do not paste file contents.

While collecting, strip secrets: API keys, passwords, tokens, PII, credential-bearing
connection strings, and sensitive topology. For a private handoff, preserve authorized
non-secret operational endpoints when needed to resume, or point to their durable config
entry. Public or committed handoffs must follow the repository's publication rules. This includes secrets that surfaced in the session itself - a value the user
pasted into the chat or that printed to a log is just as sensitive as one read from a file.
Redact by reference, not by partial value - point at where the secret lives so the next session
can resolve it, and never write a fragment that is itself sensitive (part of a token or protected
network topology):

- `REDIS_URL` env var
- credentials loaded from `.env.local`
- `{REDACTED}` when there is nowhere to point

If the secret's only source is volatile - shell history, a pasted chat message, console output -
there is no durable place to point at. Tell the next session to re-provision it from the real
secret store, not to recover the leaked value.

#### Step 5: Suggest skills and next steps

List the concrete next actions, and the skills the next session should invoke for its task -
pick the smallest installed set that covers the work (e.g., an "implement
and test a Redis denylist" next step suggests **testing** for the tests, plus whichever domain
skill fits the implementation). This primes the fresh session to start with the right tool
instead of rediscovering it.

#### Step 6: Write the file

Check the draft against the AI Self-Check first. Fix any failed item and re-check until all pass.

**Disposable (default).** Write to `.handoff/YYYY-MM-DD-{slug}.md` in the working directory and
keep it out of version control:

1. Ensure `.handoff/` is gitignored. If `.handoff/` (or a covering entry) is not in
   `.gitignore`, add it:
   ```
   # Disposable agent handoff docs
   .handoff/
   ```
   Inform the user: "Added .handoff/ to .gitignore. Tell me if you want this handoff committed
   instead."
2. Set the header's middle field to `Disposable working doc`.
3. Write the doc and report the path so the user can pass it to the next session.

**Committed (when the user wants it tracked - e.g. visible in a PR).** Do not write into the
gitignored `.handoff/`; that only forces a `git add -f` fight. Instead:

1. Write to a tracked path. Default to `docs/handoffs/YYYY-MM-DD-{slug}.md`; use the location
   the user named if they gave one, or follow an existing repo handoff convention if there is one.
2. Set the header's middle field to `Committed for review`.
3. Write the doc, then commit it via **git**. Report the path.

### Mode 2: Resume from a handoff

Trigger: user points at an existing handoff doc ("resume <path>", "continue from this handoff").

1. Read the handoff doc.
2. Treat **Locked decisions** as settled - do not reopen them. If one looks wrong, flag it to
   the user rather than silently relitigating.
3. Verify pointers still resolve (files, line numbers, branches, PRs). Note any that have moved
   or gone stale before relying on them.
4. Re-check anything tagged `assumed` before building on it.
5. Invoke the suggested skills and start on the next steps.

A disposable handoff has served its purpose once the next session is underway and can be
deleted; a committed one stays in the repo as a record of the PR it shipped with.

## Output Contract

See `references/output-contract.md` for the full contract.

- **Skill name:** SESSION-HANDOFF
- **Deliverable bucket:** `deliverables`
- **Mode:** conditional. When invoked to **author or resume a handoff** (its primary mode),
  respond freely without the contract; the handoff doc is written to `.handoff/` in the working
  directory, not to `docs/local/`. When invoked to **review or audit** existing handoff docs
  (e.g., "check whether these handoffs are leaking secrets or relitigating"), apply the reporting size and evidence rules in `references/output-contract.md` and write the deliverable to
  `docs/local/deliverables/session-handoff/<YYYY-MM-DD>-<slug>.md`.
- **Severity scale:** `P0 | P1 | P2 | P3 | info` (see shared contract; only used in audit/review mode).

## Related Skills

- For Suggested skills, compare installed descriptions and boundaries against the next session's task.
- **dev-cycle** - runs the full development workflow in one session; handoff carries context
  *between* sessions when that workflow spans more than one.
- **roadmap** - captures what to build over time; handoff carries the live state of one piece
  of work to the next session. Ideas there, in-flight context here.
- **git** - use it to commit a handoff when the user wants it durable instead of disposable, or
  to resolve branch and PR pointers when authoring one.
- **update-docs** - writes durable project documentation; a handoff is a throwaway working doc,
  not documentation.

## Rules

1. **Every decision carries its why.** A locked decision without a rationale invites
   relitigation. Record the reason or do not lock it.
2. **Headless mode.** In non-interactive contexts (`--bare`, Cursor Automations, Codex `exec`):
   write to `.handoff/`, add the gitignore entry without prompting, and report the path.
