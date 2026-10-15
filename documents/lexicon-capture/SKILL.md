---
name: lexicon-capture
description: >-
  Find recurring mis-transcriptions in the newest unacknowledged voice-dictated prompts, submit each as a candidate correction to the workstation Lexique, then ALWAYS log the pass. Only when the Stop hook lexicon-capture-stop.mjs blocks a turn after new dictation. Never speculatively.
---

# Lexicon Capture

The workstation Lexique corrects voice-dictated prompts (the global
`transcription-clean.mjs` hook applies it on every dictated prompt). Source
of truth: `~/Desktop/my-projets/workstation/data/lexicon/lexicon.json`. This
skill closes the loop after each turn that added dictation: propose
mis-transcriptions the current lexicon did NOT yet catch, for human approval in the workstation
"Lexique" tab. Full doctrine (marker list, ambiguity bar, confidence
guidance): `/Users/elmabi/Desktop/my-projets/workstation/docs/lexique.md`.

## Step 1 — Read the hook's progress values

The hook reason provides three mandatory values: `pending`, `observed`, and
`session`. Analyze only the newest `pending` dictated prompts in the current
context. Do not re-read the transcript and do not re-analyze older acknowledged
dictations. Dictated prompts started with a marker (`tt`, `transcrit`, `transcrite`,
`transcription`, `transcribed`, `transcript`, `dictee`/`dictée`,
`dicte`/`dicté`, `voix`, `voice`) and/or arrived with a "🎙️ transcription
cleaned" system notice. Ignore typed prompts entirely.

## Step 2 — Spot recurring mis-transcriptions (0-N candidates)

Bar for inclusion, ALL must hold: recurring/reusable (not a one-off slip);
not already caught (`cd ~/Desktop/my-projets/workstation && bun run lexicon
entries` first); not already open as the exact same pair (`bun run lexicon
list --status pending,changes_requested`); a real correction (`from`/`to`
differ, both non-empty);
unambiguous source term — THINK, don't map word-for-word: simulate 2-3 other
sentences that could plausibly contain `from` — if any is legitimate as-is,
a bare mapping would corrupt it. A real French/English word or natural
phrase is NEVER acceptable as a bare `from` (see the canonical
« gold »/« goal » counter-example in the doc above); anchor ambiguous
corrections in a multi-word disambiguating phrase, or skip and rely on
in-session contextual self-correction. **0 candidates is normal — never pad
the count.**

## Step 3 — Submit each candidate via the CLI

```
cd ~/Desktop/my-projets/workstation && bun run lexicon propose "<from>" "<to>" \
  --confidence <0..1> [--context "<phrase or rationale>"] [--source-session <id>]
```

`--confidence`: clear proper noun ≈ 0.9, plausible-but-uncertain ≈ 0.4, a
contextualized ambiguous-word entry caps at ≈ 0.6 (and its `--context` MUST
name the ambiguity). Never resolve/approve proposals yourself — that's the
human's job in the "Lexique" tab. Don't retry a failed `propose` more than
once; count it as not-submitted and move on.

## Step 4 — Log the run (mandatory, even at 0 candidates)

```
cd ~/Desktop/my-projets/workstation && bun run lexicon capture-log \
  --candidates <N> --submitted <M> --source-session "<session>" \
  --dictations-seen <observed>
```

Use the exact cumulative `observed` value from the hook, not `pending`. This
log entry acknowledges every dictation through that count. If it fails, report
the failure. Do not write a sentinel and do not claim the pass completed.

## Step 5 — Stop normally

Capture pass complete. End your turn as usual. The Stop hook sees that
`dictationsSeen >= observed` and allows the turn to finish. A new dictation
increments `observed` and triggers a new pass immediately, including within
the hook's short re-entry lease.
