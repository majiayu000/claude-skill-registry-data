---
name: eos-bus-sync
description: Sync edited rules and skills into the .agent-bus canonical store and commit them without capturing another session's uncommitted work. Use when you have edited a file under .claude/rules or .claude/skills and are about to commit, or when check_skills.py reports a mirror out of sync. NOT for the reverse direction — regenerating native files from the bus is `eos bus ripple` / `transpile` — and NOT a general commit helper.
---

# EmptyOS Bus Sync

`.claude/rules` and `.claude/skills` are the **authoring** surface. `.agent-bus/`
is the derived canonical store that internal `think()` agents read
(`.claude/rules/agent-bus.md`). Editing a rule therefore leaves the bus stale
until someone imports, and `check_skills.py` will report "mirror out of sync"
until they do.

Importing is one command. Everything else in this skill exists because
**`import` copies the whole native tree** and has no idea which files belong to
a parallel session that is still mid-edit.

## Why this isn't just `eos bus import`

Two failure modes, both observed on 2026-07-31 in a single session.

**1 — You publish someone else's half-written work under your name.** An import
captured a skill while another session was actively rewriting it, plus a rule
pair that had been dirty on two other tracks all day. Nothing errors; the diff
just quietly contains files you never touched.

**2 — Your staged-count intuition is wrong.** `git diff --numstat` counts only
*tracked modifications*. `git add .agent-bus/` also picks up **new** rules and
skills that were never in the bus before. A commit expected to be 31 files
staged 43. The count assertion is what caught it.

## Procedure

```bash
# 1. Stage YOUR native edits FIRST. This is what marks them as yours —
#    see the note below; skipping it makes step 3 delete your own work.
git add .claude/rules/<edited>.md          # and/or .claude/skills/<edited>/

# 2. Import — native (.claude/*) → canonical (.agent-bus/)
python scripts/agent_bus.py import

# 3. Exclude anything derived from another session's uncommitted work.
#    Reverts tracked bus files, removes untracked ones. Native is never touched.
python scripts/bus_sync_guard.py --revert

# 4. Stage the bus side + assert the count, chained so a mismatch
#    prevents the commit entirely.
git add .agent-bus/rules/<edited>.md .agent-bus/manifest.toml \
  && N=$(git diff --cached --name-only | wc -l) \
  && [ "$N" -eq <expected> ] && git commit -F- <<'MSG'
...
MSG
```

**Step 1 is load-bearing and non-obvious.** Your brand-new rule and another
session's brand-new rule are both just "untracked" to git — the index is the
only thing that distinguishes them. Staging declares "this is mine, in this
commit". This skill's own first run got it wrong and the guard cheerfully
deleted the skill being written, which is how the ordering got pinned here.

Run `bus_sync_guard.py` with no flag first if you want to see what it would do.
Exit code is the number of files needing exclusion, so CI or a wrapper can gate
on it; `--json` emits the standard scanner envelope.

## Direction is a human call

`import` is native → canonical. `ripple` / `transpile` is canonical → native.
When **both** sides have changed, do not guess — a blind copy has silently
deleted live content here before (see the docstring of
`scripts/check_skill_vault_sync.py`).

Before importing a rule whose bus copy also moved, check that native is a
strict superset rather than merely newer:

```bash
diff <(tr -d '\r' < .agent-bus/rules/X.md) <(tr -d '\r' < .claude/rules/X.md) | grep '^<'
```

Lines printed are content that exists **only in the bus** and would be
discarded. Read each one. Superseded wording is fine to drop; a section the
native file never had is not — that is the case where the answer is to merge by
hand, not to import.

## When NOT to use this

- **You edited no rule or skill.** Nothing to sync; the bus is already current.
- **You want the reverse direction** — regenerating `CLAUDE.md` / native rule
  files from the canonical store is `eos bus ripple`, a different operation with
  a different blast radius.
- **A normal code commit.** This is only for the native↔canonical mirror. Use
  `/eos-session-wrapup` for ordinary session close-out.
- **The bus reports drift you did not cause.** If `check_skills.py` flags a
  mirror you never touched, that is another track's sync to run, not yours —
  importing it means committing their pending work.

## Cross-references

- `.claude/rules/agent-bus.md` — what the canonical store is for and who reads it
- `scripts/bus_sync_guard.py` — the parallel-session exclusion check
- `scripts/check_skills.py` — the gate that reports "mirror out of sync"
- `.claude/rules/environment.md` § Parallel-session staging — the chained
  add-assert-commit pattern this skill applies to the bus
