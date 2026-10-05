---
name: feishu-paper-reading
description: Search, screen, deeply read, synthesize, and publish recent research papers for a user-specified topic, window, count, quality/attention balance, and language. Use for evidence-anchored literature digests, cross-paper comparisons, original-language excerpts, Chinese explanations, guided Feishu setup, or Feishu research reports.
license: MIT
---

# Feishu Paper Reading

Turn a request for recent literature into an evidence-grounded reading artifact,
not a ranked list of titles. Search broadly, select deliberately, read the full
papers, preserve source anchors, synthesize across papers, and publish only after
the report is complete.

## Load The References

Read these files before acting:

- `references/evidence-policy.md` before searching or selecting papers.
- `references/report-schema.md` before extracting evidence or drafting.
- `references/feishu-publishing.md` only when the requested destination is
  Feishu or another connected document surface.
- `references/feishu-onboarding.md` whenever Feishu is requested but a
  verified writable delivery path is not yet available.

Use `scripts/validate_digest.py` on a Markdown report before publishing when a
local runtime is available.
Use `scripts/check_feishu_connection.py --json` for a read-only local
discovery pass when the official Feishu CLI route may be needed; it never
executes a PATH candidate. Execution requires the installer-returned absolute
path and executable SHA-256 plus an explicit named profile and Feishu/Lark
brand, as documented in the onboarding reference.
Use the onboarding reference's installer, isolated
`scripts/run_feishu_config_init.py`, and protected authorization helper only
after consent. A fresh configuration must remain in the helper-returned
dedicated config/data directories; bind those exact directories, profile,
brand, and executable hash through preflight, authorization, publication, and
readback. Use `scripts/publication_checkpoint.py` before the first Feishu create
request. Launch every direct `lark-cli` child with
`scripts/feishu_process_environment.py`'s minimal environment builder so
ambient CLI, workspace, proxy, or custom-CA selectors cannot redirect it.

## Resolve The Brief

Infer harmless defaults and ask only when a missing choice would materially
change the result.

Default to:

- topic: derive it from the request;
- window: previous 30 calendar days;
- count: 5 deeply read papers;
- selection: technical quality first, then observable attention;
- language: Chinese explanation with original paper titles, terminology, and
  short original-language evidence excerpts;
- depth: full paper plus relevant appendix, figures, and tables;
- destination: a new Feishu document, using guided least-privilege onboarding
  when necessary and accepted; otherwise a complete Markdown report.

Accept user overrides for topic boundaries, dates, paper count, venues, source
types, quality/attention balance, desired depth, compute budget, reading goal,
language, output schema, and destination.

Write a one-sentence operational topic boundary before searching. Ask only when
two plausible boundaries would materially change the candidate pool.

Always state an absolute start and end date and timezone. Interpret "previous N
calendar days" as an inclusive interval from `today - (N - 1)` through today in
the user's timezone, or UTC when it is unknown. For arXiv-only or newly posted
work, use the v1 submission date for inclusion. For newly accepted or published
work, use the official decision or publication date. For a general "recent
work" request, accept either route but label it per paper. Read the latest
available version and record both dates when they differ. Do not silently widen
the window to fill a quota.

## Build The Candidate Pool

1. Search at least `max(5 * requested_count, 25)` candidates when coverage
   permits.
2. Search several query families: exact topic terms, adjacent terminology,
   benchmark or dataset names, and key method names.
3. Prefer primary sources: official proceedings or OpenReview, arXiv, DOI or
   publisher metadata, author project pages, and official code repositories.
4. Deduplicate by DOI, arXiv ID, and normalized title. Treat versions of one
   paper as one candidate.
5. Mark publication status precisely as preprint, under review, accepted, or
   published. Never infer acceptance from an arXiv category.
6. Record queries, sources, candidate count, unavailable sources, and coverage
   gaps.

When available, use `$research-evidence` for metadata and claim verification.
Use `$last30days` only for current attention signals and community discovery.
Social posts, aggregators, GitHub activity, and ranking sites never establish a
technical claim.

## Select Deliberately

Assess each candidate on separate evidence-backed dimensions:

- fit to the user's question;
- novelty and conceptual value;
- rigor and strength of evidence;
- reproducibility: code, data, checkpoints, and implementation detail;
- observable attention, including metric, source, and retrieval date.

Do not turn missing evidence into a numeric zero or fabricate precision.
Preserve methodological and research-group diversity when quality is similar.
Exclude abstract-only candidates from the deep-reading set; place promising
ones in a labeled watchlist. If fewer than the requested count pass the quality
bar, return fewer papers and explain why.

When the user supplies quality/attention weights, first apply a minimum
technical-quality gate. Rank the survivors independently by evidence quality
and observed attention, combine normalized rank positions with the requested
weights for ordering, and break ties by relevance then reproducibility. Use the
combined rank only as an internal selection aid, not an objective published
score. If attention coverage is too incomplete for a fair ranking, disclose
that and fall back to quality-first selection.

## Read The Full Evidence

For every selected paper:

1. Read the abstract, introduction, method, main results, limitations, and
   conclusion.
2. Inspect the figures, tables, appendix, proofs, and supplementary material
   that affect the main claims.
3. Record verified metadata, canonical links, version, and publication status.
4. Build an evidence ledger containing the research question, contribution,
   design choices, datasets, baselines, metrics, central results, failure
   cases, assumptions, limitations, and reproducibility assets.
5. Anchor important claims to a page and section, figure, table, theorem,
   equation, or appendix.
6. Separate `source fact`, `author claim`, and `Codex interpretation`.
7. Record uncertainty and contradictory evidence rather than smoothing it
   away.

Never claim a full read when only an abstract, metadata page, or secondary
summary was available.

## Embed Source Figures And Tables

When the brief asks for figures or tables, the final Feishu document must show
the source visual itself. Do not replace a requested figure with a sentence
such as “see Fig. 2 in the paper” or a locator alone.

- Prefer the original PDF figure/table rendered at a readable resolution and
  caption it with the paper, figure/table number, and PDF page.
- Use a DOCX import route when media must survive into Feishu. Markdown and
  plain rich-text routes may preserve the caption while dropping the image.
- Keep one or two decision-relevant source visuals per paper; add a native
  Feishu table only when it improves comparison rather than duplicating the
  source table.
- Before readback, count the expected image/file blocks when the connector
  exposes block inspection. A successful text readback alone is not proof that
  media survived.
- Attribute every embedded source visual. Do not present a newly generated
  diagram as an original paper figure.

## Preserve Original Language

Use original language to let the reader inspect the authors' wording while the
surrounding explanation does the teaching.

- Include 2 to 4 short, high-information fragments per paper when useful.
- Keep all direct quotation from one paper within 25 source-language words by
  default; for Chinese, Japanese, or Korean source text, also keep it within 50
  CJK characters.
- Preserve wording and punctuation exactly.
- Attach a page, section, figure, table, or appendix anchor to every fragment.
- Follow every fragment with an explanation of what it means, why it matters,
  and how strongly the paper supports it. Use Chinese by default or the
  requested output language.
- Prefer claims, definitions, limitation statements, or experimental findings;
  do not reproduce abstracts or long passages.

Retain original titles, method names, dataset names, variable names, and metric
labels. These are not substitutes for evidence anchors. When the user asks for
"more original sentences," explain that the report will use more micro-excerpts
within the per-paper quotation limit rather than reproduce full passages.

## Synthesize, Do Not Stack Summaries

Follow `references/report-schema.md`. The report must include:

1. an executive reading guide;
2. search and selection provenance;
3. a comparison matrix;
4. one deep-reading section per selected paper;
5. agreements, conflicts, trends, and missing evidence across papers;
6. user-specific research opportunities and a recommended reading order;
7. a coverage and confidence statement.

Treat recent preprints as provisional. Distinguish measured results from
author explanations and from your own hypotheses. Prefer a smaller report with
traceable evidence over a larger report built from abstracts.

Describe the final set as the strongest papers within the disclosed candidate
pool. Never imply that a bounded search proves a global "best papers" ranking.

The report is an article-reading artifact, not a chat transcript. Do not write
direct-to-reader asides such as “this is only a reference,” “you should decide
for yourself,” or “you need to judge.” Put uncertainty, scope, and limitations
inside the paper analysis itself. Use a fixed semantic palette across runs:
blue for conclusions/headings, green for transferable strengths, purple for
original-language evidence, orange for attention/public resources, red for
limitations/failure modes, and gray for metadata/verification.

## Validate

Before publishing:

1. Check canonical links and bibliographic metadata against primary sources.
2. Confirm that every selected paper has full-text evidence and locators.
3. Check paper count, duplicate IDs, unresolved placeholders, required report
   sections, quote anchors, and conservative quote limits.
4. Run:

   ```bash
   python "<skill-directory>/scripts/validate_digest.py" report.md \
     --expected-count <actual-selected-count>
   ```

5. Resolve failures or disclose intentional deviations. Do not weaken the
   validator merely to make a report pass.

## Establish Feishu Delivery

When Feishu is requested, preserve the validated report locally before
changing connection state. Research and onboarding are independent: a failed
installation or authorization must never erase or shorten the reading result.

Probe available tools and local delivery routes before installing anything:

1. Prefer an already authorized connector that can create a document and read
   it back.
2. Otherwise inspect an existing official Feishu CLI installation.
3. Follow `references/feishu-onboarding.md` when the route is absent,
   disabled, unconfigured, expired, partially authorized, not visible in the
   current task, or fails a real operation.

Treat status metadata and configuration readback as discovery, not proof of a
working connection. A route is verified only after the intended report has
been written and its title and representative content have been read back.

Before installing software, creating or updating a Feishu application,
publishing/submitting it in a tenant, starting user authorization, expanding
scopes, changing PATH/Codex/MCP configuration, or restarting a client, ask one
blocking consent question. Name the account/tenant, remote and local changes,
official package or service, requested permission profile, and possible admin
approval. Reuse that consent for the disclosed sequence; ask again when the
route, identity, remote tenant action, local change, or permission scope expands.

After consent, complete non-sensitive setup steps autonomously. Open only
official Feishu or Lark authorization pages and pause only for confirmations
that the user must perform there. Never ask the user to paste a password,
cookie, App Secret, access token, refresh token, authorization code, or device
code into chat. Never print, checkpoint, or add credentials to command
arguments, reports, repositories, or skill directories.

For onboarding that spans tasks, keep a credential-free checkpoint containing
the operational brief, absolute date window, selected count, validated report
path and digest, intended destination, and last completed setup stage. Before
publishing, use `scripts/publication_checkpoint.py` to assign a durable run ID,
generate the exact publication payload, and atomically record any returned
document ID before readback. Run its `begin-create` write-ahead transition
immediately before the remote create, repeating the same verified CLI or
connector identity binding used at `prepare`; this also re-hashes the payload.
Do not store authorization URLs or device codes in the research or publication checkpoint. Resume from recorded state
instead of repeating the search or creating duplicate documents; an in-flight
or ambiguous create forbids automatic retry and requires the documented audited
recovery transition.

If the user declines setup, the platform is unsupported, or verification still
fails after bounded diagnosis, stop changing connection state and return the
complete local report with the precise publication blocker.

## Publish And Read Back

Create one new document per run unless the user explicitly asks to update a
specific existing document. Follow `references/feishu-publishing.md`.

After publication, read the document back and verify:

- exact title, date window, and requested paper count;
- canonical paper and code links;
- comparison, per-paper, synthesis, and confidence sections;
- original fragments and their source anchors;
- no placeholders, truncation, duplicated sections, or missing media;
- expected source-figure/table media blocks, not only image captions.

Return the document link and disclose any formatting downgrade. If no
verified delivery path can be established, return the same complete report as
Markdown; publication failure must not erase the research result.

## Report Completion

Report the selected count, candidate-pool size, absolute time window, sources
searched, important coverage gaps, destination link or fallback artifact,
readback result, and any papers treated as abstract-only or provisional.

Do not save credentials, request broad drive permissions, overwrite unrelated
documents, or delete existing documents or local sources.
