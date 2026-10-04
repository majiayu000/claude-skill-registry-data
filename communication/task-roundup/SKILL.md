---
name: task-roundup
description: Collects every open action item you own from across the vault (meetings, decisions, daily notes, people 1-1s, braindumps) into a single TODO.md at the vault root, and keeps checkboxes synced both ways via stable block-IDs. Use when the user says "task roundup", "my todo", "todo list", "what do I have to do", "consolidate my actions", "sync tasks", or as a phase invoked by daily-brief.
---

# Skill: Task Roundup

The missing piece of the system: actions are born scattered across notes (meeting
action items, decision execution plans, daily follow-ups, 1-1 follow-ups, braindump
next-steps). This skill consolidates the ones **you own** into a single `TODO.md` at
the vault root and keeps the checkboxes in sync **both ways**.

## Core principle

**The source notes are the source of truth. `TODO.md` is a generated, reconcilable
view.** You never lose context: every consolidated line links back to the exact line
it came from. The link that makes two-way sync reliable is a **stable block-ID** on
each action line.

## When to activate

- The user says: "task roundup", "my todo", "todo list", "what do I have to do",
  "consolidate my actions", "sync tasks", "what's on my plate".
- As a phase invoked by `daily-brief` (collect new actions from the day + reconcile).
- After a `meeting-ingest` or `challenge-decision` that produced new action items, if
  the user wants the TODO refreshed.

**Do NOT activate when:**
- The user is capturing a single new task into a note → that's `braindump` or a direct edit.
- The user wants a plan for one project only → answer directly from that project note.

## Preflight

1. **Read `_CLAUDE.md`** (rules, the task-line convention, append-only rules).
2. **Read `00-inbox/MY-PROFILE.md`** (who "me" is, name variants, owner aliases).
3. **Get the real timestamp** (needed to bucket by due date and to stamp completions).
4. **Locate `TODO.md`** at the vault root (create it from the template below if missing).

## Concepts

### Action line convention
An action line, anywhere in the vault, looks like:

```
- [ ] <action text> — owner: me — due: 2026-05-25 — #from/meeting ^t-ab12cd
```

- `- [ ]` / `- [x]` — open / done checkbox.
- `owner:` — `me` (or your name/alias from MY-PROFILE) = yours; another `[[02-people/...]]`
  = someone else's; missing = treat as yours if it sits in a note you own.
- `due:` — `YYYY-MM-DD` or absent.
- `#from/<source>` — origin tag: `meeting | decision | daily | 1-1 | braindump | email | chat`.
- `^t-xxxxxx` — the **block-ID anchor**: `^t-` + 6 lowercase alphanumerics. Assigned once,
  **never changed**, never reused. This is what links the source line to its `TODO.md` entry.

### Ownership: "my actions" vs "waiting on others"
- **Mine** → goes in the main buckets of `TODO.md`.
- **Owner is someone else AND you're blocked / awaiting it** → goes under
  `## ⏳ Waiting on others` (tracked, but separate — it's not your action, it's a follow-up).
- Owner is someone else and it doesn't block you → ignore.

### Where actions live
Scan these for checkboxes (only `- [ ]` / `- [x]` lines count as actions):
- `04-meetings/` → `## Action items`
- `05-decisions/` → `## Execution plan`
- `01-daily/` → `## Pending follow-ups`
- `02-people/` → checkbox `- [ ] Follow-up:` lines in timeline entries / `## Open threads`
  (a plain `- Follow-up:` bullet without a checkbox is FYI-only and is not collected)
- `03-projects/` → any action line you own (e.g. in `## Timeline` or next steps)
- `00-inbox/` → braindump `## Suggested follow-up`

## Process

### Step 1 — Collect
Scan the locations above. For each `- [ ]` / `- [x]` line, determine ownership. Keep
yours and "waiting on" items; drop others'.

### Step 2 — Assign block-IDs (additive, safe)
For every kept action line **without** a `^t-` anchor, append one: `… ^t-ab12cd`.
- This is an in-place line edit — additive, and it does **not** trip the pre-commit hook
  (it removes no dated timeline header and no `(auto-logged)`/`(Backfilled)` marker).
- Generate IDs randomly; verify uniqueness across the vault before writing.
- **Never** modify or remove an existing `^t-` anchor.
- **Never assign a new anchor to a mirror line** — a line that already references an
  anchor via a wikilink (`[[…#^t-…]]`), e.g. the entries daily-brief mirrors into the
  daily `## Pending follow-ups`. Those are views of an existing task: reconcile through
  the referenced anchor; creating a second anchor would duplicate the task in TODO.md.

### Step 3 — Build / refresh TODO.md
Regenerate the body of `TODO.md` (vault root) from the collected actions, grouped by
due date relative to today. Each line **links back** via the anchor:

```
- [ ] <action text> — [[<source-note-path>#^t-ab12cd]] — due 2026-05-25 — #from/meeting
```

Do not invent or rewrite action text in `TODO.md` — mirror the source. The source is canonical.

### Step 4 — Reconcile checkboxes (the heart — both directions)
Match each `TODO.md` line to its source line by `^t-id`. Then:

| TODO state | Source state | Action |
|---|---|---|
| `[x]` | `[ ]` | User completed it here → set source to `[x]`, append ` ✅ <today>` to the source line, move the TODO item to `## ✅ Done`. |
| `[ ]` | `[x]` | Completed in the source → set TODO to `[x]`, move to `## ✅ Done`. |
| `[x]` | `[x]` | Already done → ensure it's under `## ✅ Done`. |
| `[ ]` | `[ ]` | Still open → bucket it by due date. |

Other cases:
- **New source action** (anchor not yet in TODO) → add it to the right bucket.
- **Source text changed** → source wins; refresh the TODO line text.
- **Source line deleted** (anchor gone from the vault) → don't silently drop it; mark the
  TODO item `⚠️ (source removed — confirm)` so the user notices, and ask before deleting.
- **Conflict** (can't tell which side changed) → leave both, flag `⚠️ (conflict)`, ask.

Never edit the `Compiled truth` of a people note here. Completing a task in `02-people/`
or `05-decisions/` means **only** toggling its checkbox + adding the `✅ <date>` stamp on
that line — both are allowed under append-only.

### Step 5 — Archive completed
Keep `## ✅ Done` to completions from the **last 14 days**. Older done items are pruned
from `TODO.md` (their record lives on in the source note + Git history).

### Step 6 — Report
```
✓ TODO.md refreshed (vault root)
✓ Scanned: 04-meetings (12), 05-decisions (3), 01-daily (7), 02-people (9), 00-inbox (2)
✓ 4 new actions picked up (block-IDs assigned)
✓ Reconciled: 2 completed here → marked done in source; 1 completed in source → checked here
→ ⏰ 2 overdue · 📅 3 due today · ⏳ 5 waiting on others
⚠️ 1 item flagged: source line for "send the QA plan" was removed — delete from TODO? (y/n)
```

## TODO.md format

```markdown
---
type: todo-dashboard
updated: YYYY-MM-DD
ai-first: true
---

## For future Claude

Consolidated, auto-generated action list. The source of truth is the linked notes;
this file is a reconcilable view. Checking a box here flips it in the source note
(matched by `^t-id`). Refreshed by task-roundup and daily-brief. Do NOT hand-edit the
action text here — edit it in the source note. You MAY check/uncheck boxes here.

## ⏰ Overdue

- [ ] <action> — [[04-meetings/2026-05-18-...#^t-ab12cd]] — due 2026-05-20 — #from/meeting

## 📅 Today

- [ ] <action> — [[05-decisions/2026-05-22-...#^t-cd34ef]] — due 2026-05-22 — #from/decision

## 🔜 Upcoming (next 7 days)

- [ ] <action> — [[01-daily/2026-05-22#^t-gh56ij]] — due 2026-05-27 — #from/daily

## 🗓 Scheduled (later)

- [ ] <action> — [[03-projects/...#^t-kl78mn]] — due 2026-06-15

## 🧭 No date

- [ ] <action> — [[00-inbox/2026-05-21-...#^t-op90qr]] — #from/braindump

## ⏳ Waiting on others

- [ ] (owner: [[02-people/Alex Rivera]]) <what you're waiting for> — [[04-meetings/...#^t-st12uv]] — since 2026-05-19

## ✅ Done (last 14 days)

- [x] <action> — [[04-meetings/...#^t-wx34yz]] — done 2026-05-22
```

## Priority (optional booster)
Prefix high-priority items with `🔴` and medium with `🟡` in `TODO.md`. Infer priority:
- 🔴 high: actions from a `one-way` / `hard-to-reverse` decision, a request from your
  manager, or anything overdue.
- 🟡 medium: actions tied to a `status: active` project.
- otherwise unmarked.

## Task staleness (optional booster)
Flag `⏳ stale` on any open action with no due date that has sat untouched for > 21 days
(by the source note's age). Surfaces zombie tasks the same way `people-update` flags
stale relationships.

## Anti-patterns to avoid
❌ **Editing action text in TODO.md** — the source note is canonical; edit there.
❌ **Reusing or rewriting a `^t-` anchor** — anchors are permanent identities.
❌ **Silently deleting a TODO item** when its source vanished — flag and ask.
❌ **Pulling in others' actions** — only yours + things you're waiting on.
❌ **Touching Compiled truth** while completing a people-note task — toggle the box only.
❌ **Duplicating a task** — match by anchor first; one anchor = one task.

## Special cases

### Email / chat actions with no note
If the user says "I need to reply to X" with no source note, create a one-line capture
in today's daily note under `## Pending follow-ups` (with an anchor), then it flows into
TODO.md like everything else. Don't put orphan tasks only in TODO.md — every task needs a home note.

### Recurring tasks
If an action recurs (e.g. "weekly status update"), keep one anchored line in its home
note and, on completion, append a fresh dated line rather than un-checking the old one
(preserves the completion history).

### Project rollup
If asked "what's open on [project]?", filter the collected actions by the project
wikilink instead of regenerating the whole TODO.md.
