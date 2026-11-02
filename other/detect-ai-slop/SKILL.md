---
name: detect-ai-slop
description: Use when the user wants to SEE which AI tells are in a piece of text without rewriting it. Triggers include "flag the AI slop", "where are the tells", "show me what to fix", "detect AI-generated writing", "check this for slop but don't change it", "what would you flag here", or any editorial / pre-publish review that lists issues by location. This is the report lens; it returns located findings (category, severity, the offending text), never a rewrite and never a single 0-10 score. To rewrite instead, use remove-ai-slop.
---

# Detect AI Slop

Report where the AI tells are. Return located findings, grouped by category, so the
author knows exactly what to fix. This lens never rewrites and never emits a single
headline score — a number invites gaming, a located finding invites editing.

Rules, categories, severity, and the override-merge order are defined once in
[`../../shared/spec.md`](../../shared/spec.md). Read it before reporting. The countable
tells are scored by a deterministic script; the meaning-dependent ones are yours to judge.

## Two tiers

**Deterministic tier (preferred).** Run the bundled script. It counts the countable
tells (vocabulary-table hits, em-dash density, fixed templates, bold/bullet soup, fixed
scaffolding phrases) and returns stable JSON.

```bash
python3 shared/slop_count.py --file <path> \
  [--allow-list ~/.claude/config/remove-ai-slop/user-allow-list.md] \
  [--allow-list .claude/skills/remove-ai-slop/overrides/user-allow-list.md] \
  [--extra-vocab ~/.claude/config/remove-ai-slop/user-vocabulary.md] \
  [--extra-vocab .claude/skills/remove-ai-slop/overrides/user-vocabulary.md]
```

Pipe text on stdin instead of `--file` when the user pasted it. Pass whichever
override files exist (skip silently if absent). The script is the **sole parser** of
the override files: consume its `findings` and `summary`, do not re-parse the override
tables yourself.

**Judged tier (you).** The script cannot see meaning. After the script runs, add
findings for the meaning-dependent categories from the spec — `padding-and-filler`,
`elegant-variation`, and contextual cases (is `robust` actually wrong *here*? is this
copula avoidance or a legitimate verb?). Mark these `tier: judged`.

## Fallback — when `python3` is absent

A Claude Code plugin has no guaranteed runtime. If `python3` is not available (the run
fails or `command -v python3` is empty), do the whole detection yourself from the spec
and references, read the allow-list files directly (the same files the script would
have read), and tag the result **unstable** — say plainly: "No python3 found; this is
an LLM-only pass and the counts are not byte-stable." Do not run two parsers at once.

## Output

Group findings by category, most severe first (severity is in the spec). For each:

```
[high] formulaic-constructions — para 3
  "It's not just a tool, it's a way of life."
[low] overused-vocabulary — para 1
  "delve", "leverage", "tapestry"
```

Rules:
- No single 0-10 number. A per-category tally (from the script `summary`) is fine.
- Quote the offending text and give the paragraph index. That is the anchor.
- If the script ran, say so and note the result is stable. On fallback, tag it unstable.
- If there are no findings, say: `*No AI tells detected.*` Do not invent problems.
- Respect the allow-list. A word the user allow-listed is never a finding.

## Scope

Report only. To rewrite the text, that is `remove-ai-slop`. To get a per-category
breakdown framed as a quality pass, that is `score-ai-slop` (ships next). Do not expand
beyond reporting what is there.
