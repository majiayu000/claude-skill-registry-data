---
name: fluent-speaking-export
description: Generate a voice speaking session card (default 10 questions, configurable via preferences.speaking_export_question_count) and hand it off to the Claude app's voice mode — via a Slack channel when the claude.ai Slack connector is available, Google Drive as fallback, otherwise as a local file to paste. Triggered only when the learner types /fluent-speaking-export. Questions mix level topics, the learner's top mistake patterns, due review vocabulary, and one role-play. After the voice session, /fluent-speaking-import brings the results back.
allowed-tools: Read, Write, Bash, ToolSearch, mcp__claude_ai_Slack__slack_send_message, mcp__claude_ai_Slack__slack_search_channels, mcp__claude_ai_Google_Drive__create_file, mcp__claude_ai_Google_Drive__search_files
disable-model-invocation: true
---

# Speaking Practice Export (Voice Round-Trip, Step 1 of 2)

## Overview

Claude Code has no microphone — real spoken practice happens in the Claude
app's voice mode. This skill packages a personalized speaking session for that
environment: a **session card** with `N` questions (default 10, from
`preferences.speaking_export_question_count` if the learner set one during
`/fluent-setup` or has changed it since) built from the learner's level,
mistake patterns, and due reviews. A one-time claude.ai Project
("Fluent Speaking", instructions in
`.claude/references/voice-project-instructions.md`) knows how to run the card
and emit a results JSON that `/fluent-speaking-import` ingests.

Transport priority: **Slack channel** (two-way, conversational, the default)
→ **Google Drive** (fallback if Slack isn't connected) → **local file +
copy/paste** (always works).

## When to Use

Trigger only when the learner types `/fluent-speaking-export`. Gated with
`disable-model-invocation: true`.

Skip below A1 mastery 2 — same threshold as `/fluent-speaking` (the learner
needs a basic word bank first; suggest `/fluent-vocab`).

## Instructions

### 1. Load context

```bash
python3 "${CLAUDE_PLUGIN_ROOT:-${CLAUDE_PROJECT_DIR:-.}}/.claude/hooks/read-db.py"
```

Need: `learner_profile` (name, target/native language, level,
`preferences.explanation_language`, `preferences.voice_slack_channel` if set,
`preferences.speaking_export_question_count` if set), `mastery_db.skills.speaking`,
`mistakes_db` (top patterns), `session_log` (recent `topics_covered`),
`computed.due_review_items`, `computed.today`.

Set `N = preferences.speaking_export_question_count` if present and a sane
integer (5-20), otherwise `N = 10`.

**Use `preferences.explanation_language`, never `native_language`, for every
gloss/scenario field below.** They're often different — e.g. a B2 learner
targeting English with `native_language: Vietnamese` may set
`explanation_language: English` for immersion. If `explanation_language`
equals `target_language`, this is a pure-immersion learner: skip glosses
entirely rather than translating a language into itself (rule in step 3).

### 2. Build the session ref

`session_ref = voice-YYYYMMDD` from `computed.today` (e.g. `voice-20260709`).
If `/results/fluent-voice-card-{session_ref}.md` already exists, append `-2`,
`-3`, ... until unique.

### 3. Compose N questions

All questions in the target language with an `explanation_language` gloss and
2-3 helper vocabulary words. Difficulty: i+1 relative to the learner's CEFR
level. Use the topic lists from the `fluent-speaking` skill (A2: routines,
hobbies, shopping, appointments, directions, food, weather, plans, work; B1+:
opinions, comparisons, hypotheticals, complaints, narratives).

If `explanation_language == target_language` (immersion), drop the gloss line
entirely — give a one-line target-language context/definition instead of a
translation.

The card always ends with role-play and due-review vocabulary, and always
opens with warm-up — everything else scales with `N`. Compute the slot counts
in this order:

| Slot | Count | Position |
|------|-------|----------|
| Role-play | 1 | always question `N` (last) |
| Due review vocabulary | 1 | always question `N-1` |
| Mistake-pattern probes | 2 if `N >= 8`, else 1 if `N >= 6`, else 0 | immediately before the vocabulary question |
| Warm-up | 2 if `N >= 8`, else 1 | always questions 1 (and 2, if warm-up count is 2) |
| Level topics NOT in `topics_covered` of the last 3 sessions | everything left over (`N` minus the four slots above) | fills the middle |

At the default `N = 10` this reproduces the original fixed layout exactly:
2 warm-up, 4 level topics, 2 mistake probes, 1 vocabulary, 1 role-play.

Design each mistake-pattern question so a correct answer must use the
pattern, WITHOUT naming the pattern in the question — pick the
highest-frequency unresolved `mistakes_db` patterns first. For the due-review
question, also list up to 5 due words in the card's review-vocabulary line.
If `N` is large enough that level topics run out, cycle back to earlier-level
topics rather than repeating a topic already used earlier in the same card.

If the mistakes DB or review queue is empty (new learner), backfill from level
topics.

### 4. Write the card

Save to `/results/fluent-voice-card-{session_ref}.md`:

```markdown
# Fluent Voice Session Card — {session_ref}

**Learner:** {name} · **Language:** {target_language} · **Level:** {CEFR}
**Explain in:** {explanation_language} ← the tutor MUST use this language for
all explanations, glosses, and small talk — never assume it equals the
learner's native language
**Date:** {YYYY-MM-DD} · **session_ref:** `{session_ref}`
**Results channel:** `#{slack_channel}` (post your results JSON here when done)
**Review vocabulary to weave in:** {word1}, {word2}, ...

## Questions

### 1. {Topic}
**{Question in target language}**
({gloss in explanation_language — omit this line entirely if
explanation_language equals target_language})
Helper vocab: {word — meaning}, {word — meaning}

[... questions 2 through N-1 in the same format ...]

### N. Role-play: {Scenario title}
**Scenario:** {description in explanation_language}
**Your role:** {learner role} · **Tutor plays:** {tutor role}
**Opener:** "{first line in target language}"

## Tutor focus (watch for these)
- {pattern description} ({category}) — probed by Q{n} — pattern_id: `{pattern_id}`
- {pattern description} ({category}) — probed by Q{n} — pattern_id: `{pattern_id}`
```

The `pattern_id` lines let `/fluent-speaking-import` map question scores back
to spaced-repetition items. Use the exact `pattern_id` from `mistakes_db`.

### 5. Deliver the card (Slack first, then Drive, then local)

**Resolve the Slack channel** (once per learner): `/fluent-setup` already asks
for this, so `learner_profile.preferences.voice_slack_channel` is normally
set by the time this skill runs. If it's still unset (learner skipped it
during setup), ask now — default suggestion: `<name-slug>-language` from the
learner's first name (e.g. name "Tuan" → `tuan-language`) — then save it to
that preference field via a normal profile edit so it's never asked again.

Load `mcp__claude_ai_Slack__slack_search_channels` via ToolSearch
(`select:mcp__claude_ai_Slack__slack_search_channels,mcp__claude_ai_Slack__slack_send_message`).

- **Slack available** → if `preferences.voice_slack_channel_id` is already
  saved, use it directly and skip the search. Otherwise
  `slack_search_channels(query=voice_slack_channel)` to resolve the channel
  ID, save it to `preferences.voice_slack_channel_id` (normal profile edit,
  once), then `slack_send_message(channel_id, message=card)`.
  **5000-char limit per message:** if the card markdown exceeds ~4500 chars,
  post the header + the first `ceil(N/2)` questions as the parent message,
  then post the remaining questions + Tutor focus as a `thread_ts` reply to
  it (at `N=10` this is the original 1-5 / 6-10 split). Tell the learner the
  card is in `#{voice_slack_channel}`.
- **Slack unavailable or channel not found** → fall back to Google Drive: load
  `mcp__claude_ai_Google_Drive__create_file` via ToolSearch, create a file
  titled `fluent-voice-card-{session_ref}`, `textContent` = the card markdown,
  `contentMimeType` = `text/plain`. Report the Drive file name to the learner.
- **Both unavailable** → no problem: tell the learner to copy the local card
  file into the chat instead. Never block on either connector.

### 6. First-run Project setup

If this is the first voice card (no other `/results/fluent-voice-card-*.md`
exists), also:

1. Tell the learner to create a claude.ai Project named **Fluent Speaking**.
2. Print the contents of
   `.claude/references/voice-project-instructions.md` (everything below its
   `---` separator) for them to paste into the Project instructions — and if
   Slack or Drive is available, post/upload it too (Slack: post to
   `#{voice_slack_channel}` as `Fluent Speaking — Project instructions`;
   Drive: upload as `fluent-voice-project-instructions`).

### 7. Handoff message

```markdown
## 🎙️ Voice Session Ready — {session_ref}

**Card:** {posted to #{voice_slack_channel} on Slack, or Drive file name, or local path}

**Next steps:**
1. Open the **Fluent Speaking** Project in the Claude app
2. Start a new chat → open the card (say "open my Fluent voice card from
   #{voice_slack_channel}" / "...from Drive", or attach/paste it)
3. Start **voice mode** and follow the tutor
4. When done, make sure the session JSON is posted to Slack (or saved/shown)
5. Back here, run `/fluent-speaking-import`

Veel succes! 🎧
```

(Adapt the sign-off to the target language.)

## Example — question probing a mistake pattern

`mistakes_db` has `grammar_omdat_word_order` (frequency 4, unresolved). Card
question (at the default `N=10`, mistake probes land around Q7-Q8):

> ### 7. Reasons
> **Waarom leer je Nederlands? Begin je antwoord met "Ik leer Nederlands omdat..."**
> (Why are you learning Dutch? Start your answer with "I'm learning Dutch because...")
> Helper vocab: de reden — the reason, verhuizen — to move

Forces a subordinate clause — the pattern — without mentioning word order.

## Critical Rules

- **Never reveal the tested pattern in a question.** Probe it, don't name it.
- **Use `explanation_language`, never `native_language`, for glosses and
  scenarios.** They diverge often — e.g. Vietnamese-native learners targeting
  C1 English typically want explanations in English, not Vietnamese.
- **Slack and Drive are both optional.** Local card + copy/paste must always
  work regardless of which connectors are available.
- **Respect the Slack 5000-char message limit.** Split into a threaded reply
  rather than truncating or erroring.
- **Card ≠ session result.** Name is `fluent-voice-card-*` — never
  `fluent-*-session-NNN.md` (the session analyzer must not parse cards).
- **No DB writes here.** Export is read-only apart from the card file and the
  `voice_slack_channel` / `voice_slack_channel_id` preferences (the channel
  name is asked once; the ID is cached lazily by whichever skill resolves it
  first — export or import); all other database updates happen in
  `/fluent-speaking-import`.
- **Never auto-invoke.** Gated; fires only on explicit `/fluent-speaking-export`.
