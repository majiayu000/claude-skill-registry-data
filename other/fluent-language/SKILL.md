---
name: fluent-language
description: List, switch, and add languages for multi-language learners — each language gets its own isolated set of the 6 databases under data/<slug>/, tracked in data/languages.json. Triggered only when the learner types /fluent-language (list / switch <language> / add). Never auto-invoke — switching or adding changes which database directory every other skill reads from next.
allowed-tools: Read, Write, Bash, AskUserQuestion
disable-model-invocation: true
---

# Language Switcher

## Overview

Lets one learner study several target languages without any language's
progress overwriting another's. Each language lives in its own
`data/<slug>/` directory holding the same 6 databases every other skill
already knows how to read and write; `data/languages.json` is a small
registry that tracks which language is active and shared learner identity
(name, native language) so adding a language never re-asks those.

See `docs/plans/2026-07-10-multi-language-support.md` for the full design.
This skill implements steps 3-4 of that plan (list/switch/add + first-run
migration trigger); `fluent-setup` implements the rest (new-install bootstrap,
per-language onboarding questions this skill reuses).

## When to Use

Trigger only when the learner types `/fluent-language`, `/fluent-language
list`, `/fluent-language switch <language>`, or `/fluent-language add`.
Gated with `disable-model-invocation: true` — switching changes which
database directory every other skill reads from on the next command; it
must never happen from an ambiguous chat message.

## Instructions

### 0. Resolve the data root and check for the registry

```bash
python3 -c "
import sys; sys.path.insert(0, '${CLAUDE_PLUGIN_ROOT:-${CLAUDE_PROJECT_DIR:-.}}/.claude/hooks')
from fluent_paths import data_dir
print(data_dir())
"
```

Then check for `<data_dir>/languages.json`:

- **Missing, but `<data_dir>/learner-profile.json` exists** (flat single-language
  layout, never migrated): run the migration first —
  `python3 "${CLAUDE_PLUGIN_ROOT:-${CLAUDE_PROJECT_DIR:-.}}/.claude/hooks/migrate-multilang.py"`.
  It derives a slug from `learner.target_language`, moves the six databases
  and `.backups/` into `<data_dir>/<slug>/`, and writes `languages.json`.
  Confirm success (exit 0) before continuing — tell the learner what
  happened ("Your English progress now lives under its own language slot").
- **Missing, and no `learner-profile.json` either** (brand-new install): tell
  the learner to run `/fluent-setup` first — there's no language to list yet.
- **Exists:** continue below with no migration needed.

### 1. `/fluent-language` or `/fluent-language list` — show all languages

Read `<data_dir>/languages.json` for the registry, then `read-db.py` with
`FLUENT_LANGUAGE=<slug>` set per language (or just read each
`<data_dir>/<slug>/learner-profile.json` + `spaced-repetition.json` directly)
to get level, streak, and due-review count for each.

```markdown
## 🌍 Your Languages

| | Language | Level | Streak | Due Today |
|---|----------|-------|--------|-----------|
| ▶ | **English** (active) | B2 → C1 | 🔥 6 days | 3 items |
|   | Swedish | A0 → B1 | — | 0 items |

**Switch:** `/fluent-language switch swedish`
**Add another:** `/fluent-language add`
```

If there's only one language, still show the table (so the learner discovers
`add`), but skip the switch hint.

### 2. `/fluent-language switch <language>` — change the active language

1. Match `<language>` against `languages.json.languages` keys/labels
   (case-insensitive, partial match ok if unambiguous). If no match, list
   available languages and ask again.
2. If the **current** active language has due reviews (check its
   `spaced-repetition.json` review_queue.today), warn once: "You have {N}
   items due in {current_language} today — they'll wait for you. Switch
   anyway?" Proceed on confirmation.
3. Update `languages.json`: set `"active"` to the matched slug. This is a
   normal JSON edit (small registry file, not one of the six databases —
   `update-db.py` doesn't touch it).
4. Confirm: "Switched to {language}. Level {current} → {target}, streak {N}
   days." Every skill's next `read-db.py`/`update-db.py` call now resolves
   to this language's directory automatically — nothing else to do.

### 3. `/fluent-language add` — onboard a new language

1. Ask the learner which language, current level, target level, timeline,
   and daily goal minutes — the same fields `fluent-setup` Step 3 collects,
   **except** name, native language, and explanation-language default
   (pulled from `languages.json.learner_name` / `native_language` instead of
   re-asking). Still ask for **this language's** explanation-language
   preference explicitly — it can differ per language (e.g. immersion for a
   near-fluent language, native-language explanations for a brand-new one).
2. Derive the slug the same way `migrate-multilang.py` does: lowercase,
   non-alphanumeric runs collapsed to `_`. Refuse if `<data_dir>/<slug>/`
   already exists and is non-empty — that language is already set up; route
   to `/fluent-language switch` instead.
3. Create `<data_dir>/<slug>/` and seed all 6 files from `data-examples/`
   templates, exactly like `fluent-setup` Step 5 — empty progress, empty
   mistakes, empty mastery, empty spaced-repetition queues, empty session
   log. Fill `learner-profile.json`'s `learner.name` / `native_language` from
   the registry, `target_language` / levels / timeline / daily_goal_minutes
   from this interview, and `preferences.explanation_language` from step 1.
4. Add an entry to `languages.json.languages.<slug>` (label, added date,
   level, target) but **do not** change `active` — let the learner decide
   whether to switch now:

   ```markdown
   ## 🎉 {language} added!

   Your English progress is untouched. Ready to start {language} now?

   1. **Switch to {language} now**
   2. **Stay on {current_language}, switch later** — `/fluent-language switch {language}`
   ```
5. Never touch any other language's directory or files during this flow.

## Critical Rules

- **Never auto-invoke.** Switching changes which data every other skill
  reads/writes next — must be an explicit `/fluent-language` command.
- **Migration is offered, never silent, and happens at most once.** If
  `languages.json` already exists, never re-run `migrate-multilang.py`.
- **`languages.json` is not one of the 6 databases.** Edit it directly
  (Read + Write) — `update-db.py` and `read-db.py` don't touch it.
- **Adding a language never touches another language's directory.** Only
  create files under the new slug's own directory.
- **Ask this language's `explanation_language` explicitly** — never copy it
  from another language in the registry; immersion-appropriateness is
  language-specific (e.g. immersion for a near-fluent language, but
  native-language explanations for a brand-new one).
- **Don't force a switch after `add`.** The learner may want to finish
  today's session in the current language first.
