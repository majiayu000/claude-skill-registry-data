---
name: paper-review
description: >-
  Agentic academic paper reviewer modeled on paperreview.ai (by Yixing Jiang and Andrew Ng;
  independent, not affiliated). Produces a grounded,
  ICLR-style referee report for a research paper (local PDF, arXiv ID or URL,
  or LaTeX/Markdown source): retrieves related work from arXiv, critiques it
  with per-claim grounding, scores 7 dimensions and combines them into a 1-10
  overall score. Use when the user asks to review a paper, referee or assess a
  manuscript, get feedback on a draft before submission, check novelty
  against prior work, or estimate a paper's acceptance chances.
argument-hint: "<paper.pdf | arXiv ID | URL> [venue] [cutoff YYYY-MM-DD]"
allowed-tools: Read, Write, Glob, Grep, Agent, Bash(python3 ${CLAUDE_PLUGIN_ROOT}/skills/paper-review/scripts/arxiv_search.py:*), Bash(python3 ${CLAUDE_PLUGIN_ROOT}/skills/paper-review/scripts/pdf_to_text.py:*)
---

<!-- Agentic Research Paper Reviewer, a Claude Code plugin by Tiran Dagan, copyright 2026. MIT licensed. An independent re-implementation of the pipeline described at https://paperreview.ai/tech-overview; not affiliated with or endorsed by its authors. -->

# Paper Review: an agentic referee report

Re-implementation of the paperreview.ai pipeline (Jiang & Ng, Stanford ML
Group; independent, not affiliated). Substitutions vs. the original: LandingAI ADE (PDF→markdown) → Claude
reads the PDF natively, figures and tables included; Tavily web search → the
free arXiv API via `arxiv_search.py`; emailed review link → a review file
written next to the paper. The LLM stages (query generation, relevance
scoring, summarization, review writing, scoring) are you.

Files of this skill (use these exact paths):
- Script: `python3 ${CLAUDE_SKILL_DIR}/scripts/arxiv_search.py`
- Fallback script: `python3 ${CLAUDE_SKILL_DIR}/scripts/pdf_to_text.py`
- [review-template.md](${CLAUDE_SKILL_DIR}/references/review-template.md): exact output format (read before Stage 7)
- [scoring.md](${CLAUDE_SKILL_DIR}/references/scoring.md): 7 dimensions, anchors, weights, rescale, venue rule (read before Stage 9)
- [design-notes.md](${CLAUDE_SKILL_DIR}/references/design-notes.md): provenance and the research behind each rule (read only if the user asks why the pipeline is built this way)

## Inputs

Take them from `$ARGUMENTS` or the user's message; ask only if the paper is missing.

- **paper**: local PDF path, arXiv ID/URL, or LaTeX/Markdown source file.
  For an arXiv ID/URL: `arxiv_search.py ids <ID>` for metadata, then
  `arxiv_search.py fetch <ID> --out <scratch dir>` to download the PDF.
- **venue** (optional): target venue. Default: ICLR (top-tier ML conference).
  See the venue rule in `scoring.md` for how the overall score is reported
  for other venues.
- **literature cutoff** (optional, YYYY-MM-DD): judge novelty only against
  work submitted to arXiv on or before this date. Default: none (all
  literature up to today). Use it when reviewing a paper as of its
  submission date; for an arXiv paper with no cutoff given, use none but
  exclude the paper itself.
- **output** (optional): where to write the review. Default:
  `<paper-stem>-review.md` next to the input paper (or in the current
  directory when the paper came from arXiv).

All intermediate artifacts (downloaded PDFs, search JSON, notes) go in a
scratch directory (the session scratchpad if one exists, else a temp
directory), never next to the user's paper.

## Pipeline

Run the stages in order. Announce stage transitions briefly so the user can
follow. Keep a task list.

### Stage 1: Ingest and sanity-check

Read the paper in full (for PDFs, in page batches; look at every page,
including figures, tables, and appendices). Extract the title. Verify this is
an academic paper (has an abstract/claims/evidence structure). If it is not,
stop and tell the user what the document appears to be instead.

Fallback: if native PDF reading fails (e.g., poppler missing), extract text
with `python3 ${CLAUDE_SKILL_DIR}/scripts/pdf_to_text.py <pdf> --out <scratch>/paper.txt`
(uses pypdf if installed, else poppler `pdftotext`) and read that. Figures are invisible
in this mode: skip figure-level checks and state this limitation in the
review's caveat line.

### Stage 2: Paper analysis (private notes)

Before any searching, write structured notes to scratch:
- Claimed contributions, one per line, each with where it is claimed.
- Methods and key design choices.
- Experiments: datasets, baselines, metrics, ablations present.
- **Expected-experiments list**: independently of what the paper contains,
  list the experiments, baselines, and ablations a rigorous version of this
  work *should* have. Diff this against what is present; gaps become
  candidate weaknesses. (This "predict what should be there" step is the
  single most effective known technique for catching missing baselines.)
- Every figure/table and what it shows; note any figure whose content does
  not support the text's claim about it.
- Limitations the authors acknowledge.

### Stage 3: Query generation

Generate 6–10 arXiv search queries at different levels of specificity,
covering three perspectives: (a) relevant benchmarks and baselines, (b) other
papers addressing the same problem, (c) papers using related techniques.
Include at least one broad field-level query and several narrow ones using
the paper's own terminology.

Write each query as 2–5 key terms, most important first. Every term must
match (the search ANDs them, dropping trailing terms if nothing comes back),
so long sentences return little. Put multi-word technical names in double
quotes: `"direct preference optimization" reward hacking`. Spell acronyms
out, or pair them with a domain term: an acronym alone often matches an
unrelated field (e.g. "OSDA" is both "organic structure-directing agent"
and "open-set domain adaptation"). If Stage 5 finds the results are from the
wrong field, rewrite the queries.

### Stage 4: Related-work search

Run all queries in ONE call (it de-duplicates, and it shares a machine-wide
limiter that keeps every arXiv request one at a time and 3 seconds apart,
pausing everything if arXiv answers "429 too many requests"). Do not wrap it
in your own script or split it into one call per query. It can take a few
minutes when other reviews are searching too; let it finish.

```
python3 ${CLAUDE_SKILL_DIR}/scripts/arxiv_search.py search -q "<query 1>" -q "<query 2>" ... --max 15 [--before <cutoff>] [--exclude <the paper's own arXiv ID>]
```

Shell quoting: wrap each query in single quotes so phrase quotes survive,
e.g. `-q '"masked autoencoder" 3D segmentation' -q 'sparse convolution pretraining'`.

Pass `--before` whenever a literature cutoff is set. Always exclude the
reviewed paper itself (by `--exclude` if it has an arXiv ID, otherwise by
dropping any result with the same title).

### Stage 5: Relevance selection

Score every candidate 0–3 for relevance from title + abstract (3 = same
problem or directly competing method; 2 = overlapping technique or benchmark;
1 = same area; 0 = noise). Keep the 8–12 most relevant. If fewer than 5 score
≥2, generate better queries and search again (once).

### Stage 6: Evidence gathering

For each kept paper, decide: **abstract-only** (metadata already tells you
how it relates) or **full summary** (needed to judge novelty or compare
results head-to-head; typically the 3–5 closest works). This balances
coverage against context length, as in the original.

For full-summary papers: download with
`python3 ${CLAUDE_SKILL_DIR}/scripts/arxiv_search.py fetch <ID> [<ID> ...] --out <scratch>/related [--before <cutoff>]`
(with a cutoff it downloads each paper's v1, so later revisions cannot leak in).
Then, if the Agent tool is available, spawn one
`agentic-paper-reviewer:related-paper-summarizer` subagent per paper, all in
one message so they run in parallel. Give each the PDF path, the reviewed
paper's title and one-paragraph summary, and the salient focus areas you
named when selecting it (e.g., "their benchmark numbers on X", "exact
mechanism of their Y"). Each returns its summary as its reply; save each one
to `<scratch>/related/<ID>-summary.md` yourself. Without the Agent tool, read
each PDF yourself and write the same focused summary sequentially.

### Stage 7: Draft the review

Read `review-template.md` and follow it exactly. Rules that override any
instinct to be agreeable:

- **Grounding gate**: every weakness, factual claim about the paper, and
  novelty judgment must cite either a specific location in the paper
  (section/page + a short quoted phrase) or a specific related work by arXiv
  ID. A point you cannot ground gets cut or explicitly marked "Unverified
  impression". Never invent citations, numbers, or quotes.
- **Novelty is judged against the retrieved related work, by name**, never
  from general impressions. Name the 2–4 closest papers and state the delta
  (what this paper adds over each). LLM reviewers' best-documented blind spot
  is skipping novelty/prior-work critique while over-weighting
  validity/experiments; cover every facet: novelty, prior-work positioning,
  method soundness, experimental validity, claims-vs-evidence, clarity,
  impact.
- **Major over minor**: prioritize comments that could change the paper's
  conclusions or acceptance. Typos and style nits go in one short line at
  the end of Detailed Comments, if at all.
- Weaknesses are actionable: name the missing thing and why it matters, not
  "add more details".
- Separate "appears novel/exciting" from "likely to hold up": feasibility
  and effectiveness judgments made from text alone are unreliable; flag
  them as such rather than asserting them.

### Stage 8: Critic pass (mandatory, one round)

Re-read your draft as a hostile editor. For each comment, check: (1)
specific to *this* paper: if the comment would apply to any paper in the
area, delete it or sharpen it; (2) valid: re-check the paper; if the paper
already addresses it, delete it (this is the most common LLM-review failure);
(3) grounded: the quote exists, the section number is right, the arXiv ID is
real and relevant; (4) non-duplicate; (5) major, not a nitpick. Then check
coverage: is there a real novelty assessment naming related work? Are
strengths genuine (no bare praise)? Fix everything found; do not mention the
critic pass in the output.

### Stage 9: Score

Read `scoring.md`. Score the 7 dimensions with the anchors given there,
compute the raw weighted score, and sanity-check it against the calibration
guidance in both directions (a long weakness list is not by itself a low
score; the median ICLR submission sits near 5, and papers whose core claims
hold up belong at 6 or above). Then apply the fixed rescale to get the
overall score, and apply the venue rule. Never adjust dimension scores to
reach a target overall.

### Stage 10: Deliver

Write the review file (template format). Next to it, write
`<review-stem>.scores.json`:

```json
{"title": "...", "venue": "ICLR", "literature_cutoff": "2024-10-01 or null",
 "dimensions": {"originality": 0, "importance": 0, "claims_supported": 0,
   "soundness": 0, "clarity": 0, "value": 0, "contextualization": 0},
 "overall_raw": 0.0, "overall": 0.0, "related_work_ids": ["2401.00001", "..."]}
```

`overall_raw` is the weighted sum; `overall` is the rescaled score reported in
the review.

In chat, give a short summary: the overall score, the 2–3 most important
weaknesses, and the file path. Include the standard caveat: the review is
AI-generated and may contain errors; grounding comes from arXiv, so coverage
is strongest in fields that post there; use it as guidance alongside your own
judgment.

## Hard rules

- Never fabricate related work, quotes, page numbers, or results.
- If the PDF is unreadable or not an academic paper, stop and say so.
- If arXiv search fails repeatedly, write the review anyway but downgrade
  confidence and say the novelty assessment is not literature-grounded.
- The review file is the deliverable; keep chat output short.
- This plugin never uploads the paper anywhere: Claude reads it in this
  session, and only search queries and arXiv IDs are sent to arXiv.
- This tool is for authors seeking feedback on their own work. If the user
  appears to be a conference reviewer outsourcing an assigned review, note
  that most venues prohibit this and let them decide.
