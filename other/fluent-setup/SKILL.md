---
name: fluent-setup
description: One-time interactive onboarding that creates the learner's personalized language-learning profile — name, target language, native language, current/target CEFR level, timeline, daily minutes, and learning goals. Triggered only when the learner types /fluent-setup. Also handles profile updates and resets for returning users. Must never auto-invoke because re-running can reset progress.
allowed-tools: Read, Write, Bash, AskUserQuestion
disable-model-invocation: true
---

# Language Learning Setup

## Overview

One-time onboarding that seeds all 6 databases in the Fluent data directory. After setup, every other skill reads from those files — this is the bootstrap. Also handles profile updates and progress resets for returning users.

The data directory is resolved at runtime (not hardcoded to `./data/`):

1. `$FLUENT_DATA_DIR` if set
2. `$CLAUDE_PROJECT_DIR/data/` if that path contains `learner-profile.json` (clone mode)
3. `./data/` if `./data/learner-profile.json` exists (clone mode, cwd inside repo)
4. `~/.claude/fluent-data/` otherwise (plugin-install default)

Always resolve it via the helper rather than writing literal `data/` paths:

```bash
FLUENT_DATA="$(python3 "${CLAUDE_PLUGIN_ROOT:-${CLAUDE_PROJECT_DIR:-.}}/.claude/hooks/ensure_data_dir.py")"
```

or from Python:

```python
import sys
sys.path.insert(0, f"{PLUGIN_ROOT}/.claude/hooks")
from fluent_paths import ensure_data_dir
DATA = ensure_data_dir()
```

## When to Use

Trigger this skill only when the learner types `/fluent-setup`. The skill is gated with `disable-model-invocation: true` — re-running can reset a learner's progress, so it must never auto-fire from an ambiguous prompt.

Skip this skill if a profile already exists and the learner did not ask to change anything; route them to `/fluent-learn` or `/fluent-progress` instead.

## Instructions

### 1. Check for existing profile or language registry

Resolve the data directory first, then probe for `languages.json` and
`learner-profile.json`:

```bash
DATA_DIR="$(python3 -c "
import sys; sys.path.insert(0, '${CLAUDE_PLUGIN_ROOT:-${CLAUDE_PROJECT_DIR:-.}}/.claude/hooks')
from fluent_paths import data_dir
print(data_dir())
")"
test -f "$DATA_DIR/languages.json" && echo "multilang" \
  || (test -f "$DATA_DIR/learner-profile.json" && echo "flat-exists" || echo "new")
```

- **`multilang`** — this learner already has the language registry (either
  from a prior `/fluent-setup` on a newer version, or from
  `/fluent-language`'s migration). `/fluent-setup` is for the *first*
  language only; adding or switching languages afterward is
  `/fluent-language`'s job. Tell the learner: "You already have language(s)
  set up. Use `/fluent-language add` to add another, `/fluent-language
  switch` to change the active one, or `/fluent-language` to see your list."
  Stop here — do not run the rest of this skill.
- **`flat-exists`** — a pre-multi-language single flat profile. Jump to
  **Profile updates** below (same as always; this skill still supports the
  legacy layout for existing learners who haven't migrated).
- **`new`** — continue to Step 2. New installs are born multi-language (see
  Step 5) — there is no separate migration step for a fresh install.

### 2. Welcome

```markdown
# 🌍 Welcome to Your Personal Language Learning System!

This AI-powered system will help you learn any language through:
- 📊 Systematic progress tracking
- 🧠 Spaced repetition (scientifically proven)
- 🎮 Gamification (streaks, achievements)
- 📈 Adaptive difficulty
- 🎯 Personalized to YOUR goals

**Let's get you set up!** (~5 minutes)
```

### 3. Collect info

Use the `AskUserQuestion` tool to gather questions in batches when possible. Required fields:

1. **Name** — personalizes greetings.
2. **Target language** — the language being learned (e.g. Spanish, French, German, Japanese, Korean, Arabic, Dutch).
3. **Native language** — the learner's first language. Used for cross-language notes (e.g. "close to your native X") — NOT assumed to be the explanation language; ask that separately next.
4. **Explanation language** — which language Claude should use when explaining grammar, vocabulary, and corrections. Default suggestion: same as native language. But always offer these alternatives explicitly, since native language is often the wrong default:
   - Same as native language (default for true beginners)
   - Target language only (immersion — for learners who already understand the target language well enough to follow explanations in it, e.g. B2+ polishing toward C1/C2, or anyone learning a language where the target *is* their explanation language, like this profile: native Vietnamese, learning English, explanations in English)
   - Another language they speak fluently (e.g. explain Russian using English, not Vietnamese)
   Store as `preferences.explanation_language`. Never assume it equals native language — ask.
5. **Other languages spoken** — optional, used to offer cross-language connections and as candidate explanation languages.
6. **Current level** — A1 / A2 / B1 / B2 / C1 / C2 / "not sure".
7. **Target level** — where they want to get to.
8. **Timeline** — 3 months / 6 months / 12 months / 2+ years / custom.
9. **Daily study minutes** — 10 / 15 / 30 / 60 / custom.
10. **Learning goal** — travel / work / exam (specify) / living in country / academic / family / interest.
11. **Learning style** — conversational / academic / immersive / balanced (default).
12. **Gamification on/off** — default on.

Optional voice-practice preferences — only matter if the learner ever runs
`/fluent-speaking-export`, so frame them as skippable:

13. **Speaking export question count** — how many questions per
    `/fluent-speaking-export` voice session card. Offer 5 (quick) / 10
    (recommended, default) / 15 / 20 via `AskUserQuestion`, with a "not sure,
    use the default" option. Store as `preferences.speaking_export_question_count`
    — omit the key entirely if skipped or left at default (the export skill
    already falls back to 10 when unset).
14. **Voice session Slack channel** — which Slack channel
    `/fluent-speaking-export` should post session cards to. Suggest a default
    of `<name-slug>-language` (lowercase, hyphenated first name — e.g. name
    "Tuan" → `tuan-language`), but let the learner type their own, or pick
    "Skip — I'll set this up later" (the export skill asks again on its own
    first run if this is left unset). Store as `preferences.voice_slack_channel`
    — omit the key if skipped.

If the learner picks "not sure" for current level, run a quick 5-question assessment:

1. Basic vocabulary recognition → A1
2. Simple sentence construction → A2
3. Past tense usage → B1
4. Complex subordinate clauses → B2
5. Idiomatic expression → C1

Map score to level: 0-1 correct = A1, 2 = A2, 3 = B1, 4 = B2, 5 = C1.

### 4. Generate the learning plan

Compute expected months to target level:

```
A1 → A2: ~100 hours
A2 → B1: ~150 hours
B1 → B2: ~200 hours
B2 → C1: ~300 hours
C1 → C2: ~400 hours

months = hours_needed / (daily_minutes / 60) / 30
```

Adjust:

- `-10%` time if learner's native language is typologically close to the target (e.g. Dutch ↔ English, Spanish ↔ Italian).
- `-10%` per additional language already known (cap at 30% total).

Present:

```markdown
## 🎉 Setup Complete!

**Your Learning Profile:**
- 👤 Name: {name}
- 🌍 Learning: {target_language}
- 📚 Native: {native_language}
- 📖 Explanations in: {explanation_language}
- 📊 Level: {current} → {target}
- 📅 Timeline: {timeline}
- ⏱️ Daily time: {minutes} min
- 💡 Goal: {goal}

## 📋 Personalized Plan

**Estimated time:** {months} months
**Total study hours:** ~{hours} hours

### Weekly Schedule
**Daily:**
- 🔄 `/fluent-review` — spaced repetition ({X} min)
- 📚 `/fluent-vocab` — new vocabulary ({Y} min)

**Alternating:**
- 📝 `/fluent-writing` (Mon/Wed/Fri)
- 🗣️ `/fluent-speaking` (Tue/Thu/Sat)
- 📖 `/fluent-reading` (Sun)

**Weekly:**
- 📊 `/fluent-progress` — check stats (5 min)

### Milestones
- Month 1: {reasonable short-term}
- Month 3: {quarter-way}
- Month 6: {half-way}
- Target date: {target_level}!

### Next Steps
1. Start now — type `/fluent-learn`
2. Daily habit — `/fluent-review` every day
3. Weekly — `/fluent-progress` to see stats
4. Stay consistent — even 10 min daily beats 2 hours weekly

**Your journey to {target_language} fluency starts now!** 🚀
```

### 5. Write databases (born multi-language)

New installs are always created in the per-language layout — never as a
flat `data/*.json` install — so `/fluent-language add` works immediately
without a migration step later.

1. Derive a language slug from `target_language`: lowercase, collapse
   non-alphanumeric runs to `_`, strip leading/trailing `_` (same rule
   `migrate-multilang.py` uses — e.g. "Brazilian Portuguese" →
   `brazilian_portuguese`).
2. Resolve the data root via `fluent_paths.ensure_data_dir()`, then create
   `<data_dir>/<slug>/` (this is the language directory — `fluent_paths.
   language_dir()` resolves here automatically once `languages.json` names
   it active).
3. Start from the templates in `data-examples/`. Create these 6 files inside
   `<data_dir>/<slug>/`:
   - `learner-profile.json` — fill all fields from the interview, including
     `preferences.explanation_language` (do not default this silently — it
     must come from the learner's answer in step 3). Also set
     `preferences.speaking_export_question_count` and
     `preferences.voice_slack_channel` if the learner answered items 13-14
     with anything other than "skip"/"default" — otherwise omit both keys.
   - `progress-db.json` — empty stats.
   - `mistakes-db.json` — empty `error_patterns`.
   - `mastery-db.json` — `skills` entries with `mastery_level: 0` for each skill.
   - `spaced-repetition.json` — empty queues, `daily_limits.review_items_per_day: 20`.
   - `session-log.json` — empty `sessions` array, `total_sessions: 0`.
4. Create `<data_dir>/languages.json`:
   ```json
   {
     "schema_version": 1,
     "active": "{slug}",
     "learner_name": "{name}",
     "native_language": "{native_language}",
     "languages": {
       "{slug}": {
         "label": "{target_language}",
         "added": "{today, YYYY-MM-DD}",
         "level": "{current_level}",
         "target": "{target_level}"
       }
     }
   }
   ```

Use the Write tool for each. Do not call `update-db.py` — that script is for session updates, not bootstrapping.

### 6. Optional first lesson

```markdown
## 🎓 Want to start your first lesson now?

A quick 5-10 min intro session to learn your first 10 words and get familiar with the system.

Type "yes" to start, "later" to begin on your own.
```

If yes, hand off to the `fluent-learn` skill.

## Profile Updates (existing profile)

```markdown
# 👋 Welcome back, {name}!

You already have a learning profile.

What would you like to do?

1. **Update profile** — change goals, timeline, or preferences
2. **View current plan** — see your learning schedule
3. **Reset progress** — start fresh (⚠️ erases all progress!)
4. **Cancel** — keep everything as is

**Type 1, 2, 3, or 4:**
```

- **1** — ask which field, update only that field, preserve the rest.
- **2** — render the plan section from current data. Read-only.
- **3** — confirm twice. This deletes every file in the resolved data directory. Back up first:

  ```bash
  DATA_DIR="$(python3 -c "
  import sys; sys.path.insert(0, '${CLAUDE_PLUGIN_ROOT:-${CLAUDE_PROJECT_DIR:-.}}/.claude/hooks')
  from fluent_paths import data_dir
  print(data_dir())
  ")"
  TS="$(date +%Y%m%d-%H%M%S)"
  mkdir -p "$DATA_DIR/.backups/pre-reset-$TS"
  cp "$DATA_DIR"/*.json "$DATA_DIR/.backups/pre-reset-$TS/"
  ```

  Then restart setup from Step 2.
- **4** — exit cleanly.

## Examples

### Example 1 — first-time setup flow

Learner runs `/fluent-setup`. After collecting all 11 answers, compute months, generate plan, write 6 JSON files, offer first lesson.

### Example 2 — returning-user profile reset

Learner: "reset my progress, I want to start over"

> You're about to delete:
> - 42 sessions
> - 6-day streak
> - 287 vocabulary items
> - 12 mastered patterns
>
> This is irreversible. Type `RESET` (all caps) to confirm, or anything else to cancel.

## Critical Rules

- **Never auto-invoke.** Re-running this can reset a learner's progress. Must be an explicit `/fluent-setup`.
- **Confirm twice before reset.** "This will erase X days of progress, Y sessions, and Z mastered words. Proceed? (yes/no)".
- **Always seed all 6 files** — every other skill assumes they exist.
- **Back up before reset.** Hooks may not fire here; back up manually to `.backups/pre-reset-<timestamp>/`.
- **Don't invent data.** Start every file empty — progress, mistakes, mastery all start at zero. The system builds up from real sessions.
