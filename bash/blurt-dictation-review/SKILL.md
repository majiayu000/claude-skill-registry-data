---
name: blurt-dictation-review
description: Review the user's own recent Blurt dictations (kept audio + what was typed) to find recognition, polish, punctuation and formatting errors, judge each one, save the real ones as Dictation Lab cases, and turn them into fixes measured on the growing case set. Use when the user says "看一下今天的听写", "review my dictations", "复查一下识别问题", or reports a misrecognition they just had.
---

# Review the user's dictations

The user dictates with Blurt all day. Their takes are the best test data there is: real voice, real pauses, real
vocabulary. This skill turns them into fixes.

## Prerequisites
- Settings → 听写 → 「保留录音」 (`record.dictation.keep_audio`) on. Then each take keeps its audio
  (`$BLURT_HOME/dictation/audio/<id>.wav`) and its streamed pieces (cuts, pauses, every polish window's input and
  output) until the history retention (30 days). Without it only the text is there: say so and review the text alone.
- Never write `~/.blurt` except through `dictation_lab.py` (cases) — no hand edits of the history or config.
- The audio is the user's voice. Allowed off this Mac (user, 2026-10-28): **disputed clips only**, to OpenAI's speech
  models through OpenRouter, **at most $10 in total** — `cloud_ref.py` next to this file enforces the cap (ledger
  `spend.json`, clips ≤ 120 s). Nothing else leaves the Mac.

## Cloud second opinion (disputed clips)
```bash
OPENROUTER_API_KEY=$(grep '^OPENROUTER_API_KEY=' /Users/john/workspace/ordo_projects/ordo_ai/ordo-backend/.env.prod | head -1 | cut -d= -f2- | tr -d "\"'") \
  python3 -I .claude/skills/blurt-dictation-review/cloud_ref.py CLIP.wav [--language zh]
```
Default models: `openai/whisper-large-v3` (≈ $0.03 / audio hour) and `openai/gpt-transcribe` (≈ $0.27 / hour). Never
print the key. On Chinese, Whisper is weaker than the local Qwen3-ASR (rare names 12 % vs 4.5 % errors), so read it as
a vote: two cloud models agreeing against Blurt is strong evidence of a recognition error; one alone is not. Cut the
disputed span out of a long take (ffmpeg `-ss/-to`) rather than sending it all.

## Steps
1. `uv run skills/blurt/scripts/dictation_lab.py review --since <ISO date>` (or `--last N`). Each kept take comes back
   with `typed`, `raw` (streamed ASR), `heard_once` (the whole take re-heard in one pass by the installed model, no
   cuts), `heard_diff`, the `pieces` with `pause_after` and each window's `polish_in` / `text`, and `flags`:
   `fell_back:<reason>`, `heard_differently`, `seam_marks`, `spelled_letters`, `numeral_format`.
   For a take without audio, read `~/.blurt/dictation/history.jsonl` (raw / polished / text / fell_back / reason).
2. Read every take, flagged or not, as a careful human editor would: what did the user most likely say?
   Classify each problem:
   - **heard wrong** (ASR): homophone (买点/埋点), term (空中云会/空中云汇), dropped or invented words. If `heard_once`
     has it right, the streaming (cuts, prior) caused it; if not, the model.
   - **pause punctuation**: a mark where the user only paused to think (look at `pause_after` ≥ 0.6 s and the window
     that wrote it); or missing marks in dense speech.
   - **formatting**: 三D → 3D, 四十八小时 → 48 小时, C L I → CLI, V 二 → V2, spaces.
   - **polish**: fell back (why — the guard's reason), dropped / changed / translated words, copied the text before
     the cursor.
   - **user**: they misspoke — not a bug.
   When unsure whether the user or the model is wrong, re-run the take through other configurations
   (`dictation_lab.py from-history ID` then `rerun CASE --config asr=qwen3-asr-1.7b-mlx,mode=whole` …) and the
   cloud second opinion below.
3. Save each real error as a case with its ground truth:
   `dictation_lab.py from-history ID --corrected "<what they meant>" --tags term,punctuation --note "<why>"`.
   Tags: term, code_switch, punctuation, filler, dropped, made_up, segmentation, clipped, slow (+ format, homophone).
4. Report to the user in a short table: take, what was typed, what was meant, class, cause. Then group by cause and
   propose fixes — model choices, prompt, guard, seams, vocabulary — never word lists or regex rules for language
   (docs/design/dictation.md §Rules vs model).
5. When fixing: measure before / after on all saved cases (`dictation_lab.py run --config mode=windows --json`) plus
   the eval sets (`polish.py eval`, `tests/fixtures/polish_overdelete.jsonl`), and the real-take replay of the
   history text. Ship only what improves the cases without regressions; say the numbers.
