---
name: fluent-speaking-import
description: Import the results of a Claude app voice speaking session back into Fluent — fetch the results JSON from a Slack channel, Google Drive, pasted text, or a raw transcript, validate and re-score it, convert it to an update-db.py payload, write the standard session results markdown, and update all 6 databases. Fires on /fluent-speaking-import, or on natural-language cues that the learner just finished a voice session (e.g. "I finished my voice practice", "pull in my speaking results", "import my Fluent Speaking session"), after a voice session created by /fluent-speaking-export.
allowed-tools: Read, Write, Bash, ToolSearch, mcp__claude_ai_Slack__slack_search_channels, mcp__claude_ai_Slack__slack_read_channel, mcp__claude_ai_Slack__slack_read_thread, mcp__claude_ai_Google_Drive__search_files, mcp__claude_ai_Google_Drive__read_file_content
---

# Speaking Practice Import (Voice Round-Trip, Step 2 of 2)

## Overview

Closes the loop opened by `/fluent-speaking-export`: takes the results JSON
produced by the claude.ai "Fluent Speaking" Project (schema defined in
`.claude/references/voice-project-instructions.md`), validates it, converts it
into one `update-db.py` payload, and records the session exactly like a native
`/fluent-speaking` session — results markdown, mistakes, SM-2 reviews, streak.

**This skill is the authoritative scorer.** The external chat's output is
evidence, not truth: validate every field, re-derive what doesn't add up.

## When to Use

Trigger on `/fluent-speaking-import`, or when the learner's message indicates
they just finished (or want to pull in) a voice session — e.g. "I'm done with
voice practice", "pull in my results", "import my speaking session". Don't
fire on vague mentions of speaking practice with no completion/import intent
(e.g. a question about how voice mode works).

## Instructions

### 1. Load context

```bash
python3 "${CLAUDE_PLUGIN_ROOT:-${CLAUDE_PROJECT_DIR:-.}}/.claude/hooks/read-db.py"
```

Need: `computed.next_session_id`, `computed.today`, `mistakes_db` (existing
`pattern_id`s), `spaced_repetition` (item ids), learner profile
(`preferences.voice_slack_channel`, `preferences.voice_slack_channel_id`).

### 2. Locate the results

In order:

1. **Pasted by learner** — if the message invoking the skill (or the next
   one) contains a `fluent_voice_results` JSON block, use it.
2. **Slack** — if `preferences.voice_slack_channel` is set: load
   `mcp__claude_ai_Slack__slack_read_channel` via ToolSearch (and
   `mcp__claude_ai_Slack__slack_search_channels` only as a fallback — see
   below). Prefer `preferences.voice_slack_channel_id` if already saved on
   the profile — skip the channel-name search entirely and call
   `slack_read_channel(channel_id, limit=5)` directly. If no
   `voice_slack_channel_id` is saved yet, resolve it once via
   `slack_search_channels(voice_slack_channel)` and save the resulting ID to
   that preference field (a normal profile edit) so future imports skip the
   lookup.
   Scan the 5 newest messages (returned newest-first) for one containing
   `fluent_voice_results`. **If none of the 5 match, fetch one more page of 5
   older messages (10 total) and stop — do not paginate further.** If still
   not found after those 10, fall through to Google Drive / ask the learner.
   If the JSON was split across a parent message and a threaded reply (the
   export skill does this for long cards, but results are always small —
   check anyway), use `slack_read_thread` to pull the reply and concatenate.
3. **Google Drive** — load
   `mcp__claude_ai_Google_Drive__search_files` via ToolSearch; query
   `title contains 'fluent-voice-results'`, take the newest match, read it
   with `read_file_content`. (The file may have been converted to a Google
   Doc — extract the JSON from the text representation.)
4. **Raw transcript fallback** — if the learner pastes a chat transcript with
   no JSON block, reconstruct the data yourself: identify each
   question/answer exchange and score it with the `fluent-speaking` /
   `voice-project-instructions.md` rubric (Communication /5, Grammar /3,
   Vocabulary /2). Tell the learner you're re-scoring from the transcript.

If nothing is found, ask the learner to paste the JSON block from the chat.

### 3. Validate (authoritative-scorer pass)

- `fluent_voice_results` must be `true`; `session_ref` must match an existing
  `/results/fluent-voice-card-{session_ref}.md` (warn and continue if the
  card is missing; abort if `session_ref` is absent entirely).
- **Multi-language guard:** if `<data_dir>/languages.json` exists (multi-language
  mode active) and the results JSON has a `language` field, compare it
  (case-insensitive) against the *active* language's label. On a mismatch —
  e.g. the learner practiced Swedish by voice but English is currently
  active — stop and ask: "This session was in {results_language}, but
  {active_language} is your active language. Run `/fluent-language switch
  {results_language}` first, then re-import?" Importing into the wrong
  language's databases silently corrupts that language's streak/mastery, so
  never import across a mismatch without confirmation.
- **Duplicate guard:** `grep -l "{session_ref}" results/fluent-speaking-session-*.md`
  — if any hit, this session was already imported. Stop and tell the learner
  (re-import would double-count streak/session stats).
- Per question: each of communication (0-5), grammar (0-3), vocabulary (0-2)
  clamped to range; recompute `score` as their sum (ignore the reported
  `score` if it disagrees).
- Per error: `category` must be one of `grammar`, `formal_informal`,
  `vocabulary`, `spelling`, `prepositions`, `articles`, `missing` — relabel
  to the closest canonical category if not; `severity` must be
  `critical`/`moderate`/`minor` (default `moderate`).
- `date`: valid `YYYY-MM-DD`, not in the future — else use `computed.today`.
- `duration_minutes`: integer 1-120 — else estimate 2 min per question.

### 4. Convert to the update-db payload

| Payload field | Derivation |
|---|---|
| `session_id` | `computed.next_session_id` (NEVER from the JSON) |
| `date` | validated results `date` |
| `duration_minutes` | validated duration |
| `command_used` | `"/fluent-speaking-import"` |
| `skills_practiced` | `["speaking"]` |
| `skill_scores.speaking` | `{exercises: len(questions), correct: count(communication >= 4), time_minutes: duration_minutes}` |
| `errors[]` | flatten `questions[].errors`; collapse duplicates by pattern; `pattern_id` = existing `mistakes_db` id when category+context match one, else `{category}_{context_in_snake_case}`; carry `category`, `severity`, `your_answer`, `correct_answer`, `context` |
| `review_results[]` | for each card "Tutor focus" line whose `pattern_id` exists in `spaced_repetition` items: `{item_id: pattern_id, quality: floor(score_of_probing_question / 2)}` |
| `new_vocabulary[]` | one entry per `new_words[]` item: `item_id` = snake_case content (article stripped), `item_type: "vocabulary"`, `content`/`answer` from the entry, `category: "voice_session"`, `difficulty` = learner CEFR level, `initial_quality: 3`, `priority: "medium"` |
| `topics_covered`, `breakthroughs`, `focus_next_session` | pass through |
| `session_notes` | `"Voice session via Claude app ({session_ref}). "` + results `session_notes` |

### 5. Write the session results markdown

`/results/fluent-speaking-session-{NNN}.md` (NNN from `session_id`),
following `.claude/references/session-file-template.md` exactly — same
headings and parsing markers (`❌`, `✅`, `**Score:** X/10`,
`**Accuracy:** N%`, `**Focus Areas:**`). Set:

- `**Skill:** speaking`
- `**Command:** /fluent-speaking-import`
- Add one line under the header: `**Modality:** voice (Claude app) — {session_ref}`
- One `### Question N` block per results question, with the learner's spoken
  answer, corrections, and the recomputed score.

### 6. Update all databases

Use the `fluent-db-updater` skill: pipe the Step-4 payload to

```bash
python3 "${CLAUDE_PLUGIN_ROOT:-${CLAUDE_PROJECT_DIR:-.}}/.claude/hooks/update-db.py"
```

Exit `1` = fix payload and retry; exit `2` = report I/O error, nothing written.

### 7. Show the summary

Normal Fluent session summary: questions answered, accuracy, streak status,
new words added to the review queue, focus for next session. Celebrate — this
was REAL speaking practice. 🎉

## Example — score recomputation

Results JSON says `{"communication": 4, "grammar": 2, "vocabulary": 2,
"score": 9}`. 4+2+2 = 8 ≠ 9 → use 8. Review quality for a pattern probed by
this question: `floor(8/2) = 4`.

## Critical Rules

- **Never trust external data blindly.** Clamp, recompute, relabel — the
  canonical rules live in this repo, not in the chat.
- **`session_id` comes from `read-db.py` at import time.** The voice chat
  must never pick it — another session may have happened in between.
- **One `update-db.py` call, at the end** — same rule as every other session.
- **Duplicate imports are blocked**, not merged. `update-db.py` rejects a
  reused `session_id` outright (exit 1, nothing written); the Step-3
  `session_ref` duplicate guard exists to catch it *before* that — re-running
  this skill on an already-imported session must not look like new progress.
- **Transcript fallback always exists.** A voice session without a JSON block
  is still importable — you re-score it yourself.
- **Slack is read-only here.** This skill only reads from the channel; it
  never posts. `/fluent-speaking-export` owns the one-time
  `voice_slack_channel` preference (this skill may still cache
  `voice_slack_channel_id` as a read-side optimization if export hasn't yet).
- **Auto-invocable, but only on clear completion/import intent** — the
  duplicate-guard in Step 3 makes accidental re-firing harmless (it stops and
  tells the learner rather than double-importing), so err toward firing when
  the learner sounds done, not toward re-asking `/fluent-speaking-import`.
