---
name: paraphrase-anything
description: Paraphrase, rewrite, or reword any text in a chosen tone (formal, casual, academic, simple, shorter, longer) or produce several distinct variants, while keeping numbers, names, citations, code, links, and meaning exactly intact, verified by deterministic checks. Use when the user asks to paraphrase, rewrite, reword, rephrase, restate, "say this differently", give alternative versions or variants, viết lại, diễn đạt lại, paraphrase lại, 言い換え, 書き換え, for pasted text or a .txt / .md file. Do not use for pure summarisation, translation into another language, or proofreading-only requests.
---

# Paraphrase Anything

Rewrite text in the requested style while the **original stays the single source of truth**.
You write; the bundled `pe` tool drives the work and verifies it. Never grade your own rewrite
by eye alone.

`pe` is zero-install (Python ≥ 3.9 standard library). Run it as:

```bash
python <skill-dir>/scripts/pe.py <command> ...    # use python3 if python is not Python 3
```

All commands print JSON. Exit code `0` = ok, `1` = issues found, `2` = usage/input error.

## Workflow

Every request runs as a **harness session**: `pe run` keeps the state, gives you one task at a
time, and gates each pass against the original. You never choose the next step yourself.

### 1. Pin the original
Save the user's text **verbatim** to a temp file outside the user's project, e.g.
`<tmp>/pe-<short-id>/input.txt` (keep the extension of a `.md`, `.srt`, or `.vtt` file). Never
edit it: `pe run init` copies it into the session and every gate compares against that copy.

### 2. Resolve the request
| Setting | Default | Notes |
|---------|---------|-------|
| mode | `standard` | `light`, `standard`, `creative`, `shorten`, `expand`; see [modes](references/modes.md) |
| language | same as input | if the user wants another language, that is translation; ask first |
| length | about the same | "shorter / 70%" → `shorten`; give the ratio in pass 1 (`length_ratio`) |
| variants | 1 | "give me 3 versions" → `--variants 3` |
| tone / persona | none | any file in [personas](references/personas/) (list the folder) |
| preset | by route | see below and [presets](references/presets.md) |

Pick the preset by the request:
- `fast`: a sentence or a short paragraph of plain prose.
- `standard`: most rewrites.
- `strict`: the user wants the exact meaning kept, or the text is legal, medical, financial, or
  otherwise high-stakes. Also use it for text over ~150 words with facts that must survive.

### 3. Start the session
```bash
python scripts/pe.py run init <tmp>/input.txt --preset standard --mode standard [--persona name] [--variants N]
```
`init` prints the session directory, the passes and gates, and any `resolutions` it applied. It
detects the route itself: Files for `.md` / `.srt` / `.vtt`, Long above ~3,000 words, Variants
with `--variants`. See [routes](references/routes.md) for the extra task fields of each route.

### 4. Loop: next → write → submit
```bash
python scripts/pe.py run next <session-dir>      # one task as JSON
# write exactly the file named in "output" (plus "review" / entailment files when asked)
python scripts/pe.py run submit <session-dir>    # 0 = passed, 1 = fix needed, 2 = error
```
Repeat until `next` returns `{"step": "done"}` or `{"step": "incomplete"}`. For each task:

- Load **only** the files in `instructions`, and follow `duties`, `ops`, and `plan`.
- Text passes start from `inputs.previous`. Copy every `⟦Pn⟧` placeholder exactly once.
- Never edit `original.txt`, `analysis.json`, or `plan.json` after their gates pass; to change a
  plan, `pe run rewind <session-dir> --to plan`.
- When `issues` come back, fix only what they name. Warnings that are false positives can be
  accepted with a reason in the review file; errors cannot.
- At the last pass, run `pe run pairs <session-dir>` after writing the rewrite and judge every
  pair in both directions, as in [entailment](references/entailment.md). Where your tool supports
  subagents, give the pairs (not the plan) to a fresh subagent and set `"judge": "independent"`.

Pass 1 (analysis) is where you extract key facts: 3–8 short claims with literal anchors that
every later gate re-checks; see [key facts](references/facts.md).

Details: [harness](references/harness.md), [layers](references/layers.md),
[analysis](references/analysis.md), [plan](references/plan.md),
[preservation rules](references/preservation.md), and the language note for the input
language, `references/languages/<code>.md` (any file in [languages](references/languages/)).

### 5. Report
```bash
python scripts/pe.py run report <session-dir>
```
Use the report for the verification line: `gates_run`, `skipped_checks`, `accepted_warnings`,
`open_issues`, fact verdicts, and `entailment.judge`. An `incomplete` session is **not
verified**: say which issues are still open and never present it as checked.

### 6. Respond
Follow [response](references/response.md). In short, answer with:
1. The rewrite (from the report's `output`; each variant labelled with its axis) in a
   plain-text ```text block, so it can be copied as is. Keep the input's formatting inside it.
2. A **What changed** table of verbatim `Original | Rewritten | Change` fragments.
3. One verification line built from the report, e.g. "Checked: numbers, citations, links and
   code unchanged; key facts 4/4 kept; entailment judged by a subagent. Skipped: length target."
   Do not paste the JSON.
4. 2–4 **follow-up suggestions** the user can copy as their next request.

If the input is a file, copy the rebuilt output (e.g. `output.md`) to a new file next to it
(e.g. `name.paraphrased.md`) unless the user asked to overwrite; show the table and follow-ups in
the chat only.

## When the harness cannot run
If your tool cannot keep files between commands, or `pe run init` rejects the input, use the
[manual routes](references/manual.md) and say in the verification line that the checks were run
manually.

## Hard rules
- Never change facts, numbers, dates, names, quotes, citations, code, or links.
- Never add claims, examples, or opinions that are not in the original.
- Keep digits as digits; "3" → "three" is reported as a number error.
- Keep the input language and formatting (Markdown structure, lists, line breaks).
- Do not present the output as a way to evade plagiarism or AI-detection tools.
