---
name: skill-recall
description: "Find local skills for the current task and log gaps. Use when checking which local skill matches a task or whether a suitable skill exists."
---

# /skill-recall — Find local skills for current task

When invoked, match the current task against the installed skill taxonomy. Return ranked suggestions or log a gap.

## Trigger

`/skill-recall` or `/skill-recall <task description>`

## Flow

1. **Parse intent** — extract key action words and domain from the task description or current conversation context
2. **Read taxonomy** — load `$AIGENT_VAULT/memory/SKILL_LEDGER.md`
3. **Prefix match** — match intent keywords against taxonomy paths:
   - Direct path match: `research.deep` matches all `research.deep.*` skills
   - Keyword match: "browser" matches `automation.browser.*`, "lyrics" matches `music.lyrics.*`
   - Fuzzy domain match: "investigate a bug" matches `research.deep.investigate` + `strategy.debug.investigate`
4. **Check chains** — read `$AIGENT_VAULT/memory/SKILL_CHAINS.md` for prior successful multi-skill sequences with similar objectives
5. **Rank results** — prioritize by:
   - Exact taxonomy path match (highest)
   - Prior chain match (high — proven to work)
   - Keyword overlap (medium)
   - Domain proximity (lower)
6. **Output**:
   - If matches found: return ranked list with skill name, taxonomy path, one-line description, and invocation hint
   - If chain match found: suggest the full chain with `→` notation
   - If NO match found: log to `memory/SKILL_GAPS.md` and suggest `/skill-hunt`

## Gap Logging

When no match is found, append a row to `memory/SKILL_GAPS.md`:

```
| {today's date} | {task context, 1 line} | {what capability is missing} | — | open |
```

Then output: "No matching skill found. Gap logged. Run `/skill-hunt {gap description}` to search externally."

## Example

```
User: /skill-recall transcribe this meeting recording
aigent: 
  Match: `research.audio.transcriber` — /audio-transcriber
  "Transcribe audio files to structured markdown with speaker labels via Whisper"
  Invoke: /audio-transcriber <path-to-audio>
```

## Related

- [[memory/SKILL_LEDGER]] — the taxonomy this skill searches
- [[memory/SKILL_GAPS]] — where misses are logged
- [[memory/SKILL_CHAINS]] — prior successful sequences
- [[concepts/Capability Expansion Doctrine]] — the doctrine governing recall + hunt
