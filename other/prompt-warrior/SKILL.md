---
name: prompt-warrior
description: Use when the user wants to analyze their communication style with AI from Claude Code logs — asks for a "prompt warrior" profile, an "AI profile", "wrapped", a psychological portrait of how they prompt, statistics of their sessions/messages, or personalized prompt-engineering recommendations based on their chat history. Works in any language (RU/EN lexicons built in).
---

# Prompt Warrior

Builds a gamified analytical portrait of the user's AI collaboration style from their
local Claude Code JSONL logs: real metrics on a FIXED scale (comparable between people)
plus fun statuses — a title, a level, achievements with rarity — and evidence-based
prompt-engineering recommendations. It is NOT an RPG character sheet:
no classes, no stat blocks; the analytics are the product, the statuses are the garnish.

**The scale is a contract.** All formulas and thresholds live in `scripts/analyze.py`
(SCALE v1) and `references/scale.md`. NEVER adjust formulas, thresholds, rank mappings,
or achievement conditions per user — comparability is the whole point. If a metric looks
unflattering, it stays. Report numbers only from `profile.json`, never invent or soften them.

## Workflow

1. **Run the analyzer** (Python 3, stdlib only, read-only — it never modifies logs):
   ```
   python scripts/analyze.py -o profile.json                        # all time, all projects
   python scripts/analyze.py --days 7 -o profile.json               # last week
   python scripts/analyze.py --days 30 -o profile.json              # last month
   python scripts/analyze.py --date-from 2026-06-01 --date-to 2026-06-30 -o profile.json
   python scripts/analyze.py --project <dir-name> -o profile.json   # one project
   ```
   THE RANGE IS THE USER'S CHOICE: if they named a period («за неделю», "this month",
   dates), pass it; if they didn't, default to all time and mention that a range is
   available. Never pick a range for the user silently.
   Default logs location: `~/.claude/projects`. Use `--projects-dir` to override.
   Try `python3` if `python` is missing.
   RUNNING IN A DIFFERENT HARNESS (OpenCode, Codex CLI, Gemini CLI, Copilot)?
   See `references/harnesses.md` — known log locations and formats, and how to plug a
   new source into SOURCES. If your paths differ, orient by analogy as described there.

2. **Read `profile.json`.**
   - `{"error": "not_enough_data"}` → tell the user at least 30 of their own messages are
     needed; stop.
   - `"low_confidence": true` (< 100 messages) → include a visible "small sample" caveat.

3. **Generate the local avatar (optional, offline)** — a deterministic monster from
   the user's title via the `robohash` package (assembles bundled PNG layers locally;
   zero network):
   ```
   python scripts/avatar.py --from-profile profile.json -o avatar.png
   ```
   If the package is missing, offer ONCE: «поставить `pip install robohash` для
   локальных аватаров-монстров?» — install on yes, skip on no. Without the avatar the
   card simply renders without an image — NEVER substitute placeholders, letters or
   icons in its place. The monster evolves when the title changes — mention it.

3а. **Write the Warrior's Chronicle** («Хроника воина») — 2-4 paragraphs (~100-180
   words) that YOU, the model, author from profile.json: a characterization /
   mini-biography of the user in the grimoire-chronicle voice with light humor. Rules:
   facts strictly from the profile (no inventions), NO numbers (numbers live in the
   card sections — each number appears exactly once), neutral to metric values (do not
   shame, do not flatter), 1-2 <em> accents max, written in the card's language. This
   is the one place the model speaks freely — make it feel written, not generated.

4. **Build and SHOW the card** — output degrades gracefully, in this order:
   a. You do NOT write HTML/CSS/SVG. Write `content.json` — ONLY your authored parts,
      in the card language:
      ```json
      {"chronicle": ["<p1>", "<p2>", "<p3>"],
       "strengths": ["..."],
       "weaknesses": [{"w": "...", "a": "...", "ev": "...", "url": "https://..."}]}
      ```
      (chronicle = step 3а; strengths ≤3 and weakness→fix pairs ≤4 picked by the rules
      in `references/widget.md`). Then run the canonical renderer:
      ```
      python scripts/render.py profile.json --content content.json --lang ru -o ai-profile.html
      ```
      (`--lang en` for English — labels are symmetric, data fields are bilingual.)
      It fills the whole card: numbers exactly once, bars, gauges, icons, favicon,
      seal, achievements accordion, avatar if `avatar.png` exists. Tell the user the
      path. NEVER Read .svg asset files into context (widget.md, rule 2д).
   b. OPEN it for the user: if a preview panel/tool is available, open it there;
      otherwise open in the default browser (`start` on Windows, `open` on macOS,
      `xdg-open` on Linux). Do not make the user open the file by hand.
   c. If an inline widget tool is available, ALSO render an inline widget mirroring
      the same sections and numbers.
   d. If NONE of the above is available (headless/console-only environment), render
      the card as TEXT in the console following the text-fallback spec at the end of
      `references/widget.md` — same sections, same numbers, bars as unicode blocks.

5. **Explain the profile** in the user's conversation language (the widget carries both
   RU and EN labels from profile.json). If `profile.delta` is present and non-null,
   LEAD with what changed since the last visit — new achievements first (that is the
   share-worthy moment: «получена новая ачивка!»), then level/title changes, then the
   2-3 most notable metric shifts with direction. Then the numbers: notable metrics,
   strengths and weaknesses; then the flavor: title, achievements. Always surface 1-2
   non-obvious insights — the most extreme or most characteristic numbers in the
   profile, phrased as discoveries, not judgements. Numbers verbatim from profile.json.

6. **Give recommendations** using `references/recommendations.md`: pick the entries whose
   trigger conditions match the profile, present 3-6 of them, each with its evidence note.
   Do not moralize about tone — research shows aggregate quality impact of tone is near
   zero; frame tone findings as fun facts plus practical notes (see recommendations.md).
   If the user asks about tone tricks, rudeness, tips/threats or "prompting lifehacks",
   use the Anti-myths section of recommendations.md — debunked claims with vote verdicts.

## Rules

- Read-only with respect to user logs. Files written: `profile.json`, `ai-profile.html`,
  and the local progress history `~/.claude/prompt-warrior/history.jsonl` (all-time runs
  only; disable with `--no-history`). History never leaves the machine.
- Respond in the user's language; RU/EN both supported end to end.
- Fixed scale: same formulas for everyone, always cite `SCALE v1` version in the card footer.
- Privacy: everything runs locally; nothing leaves the machine.
- If the user asks to compare with friends: they run the same skill and exchange
  profile.json files; then `python scripts/compare.py mine.json theirs.json` prints a
  duel card. Identical scale version = comparable; the script warns otherwise.
- v1.4 layers (economy/arsenal) are computed over the WHOLE corpus regardless of the
  chosen period — say so if the user picked a range.
- Juicy v1.3 signals for narration when notable: interruptions_per_100 (impatience),
  boiling_point_median + boiled_sessions_pct (how fast sessions heat up),
  werewolf_ratio (night vs day profanity), signature_words (the user's own vocabulary —
  present playfully, never judgementally).
