---
name: audit-references
description: >-
  Verify citations in a paper or document. Reads a markdown document, extracts
  every [@citation-id] pandoc citation, resolves each against references.yaml
  (CSL-YAML), fetches the cited papers (arXiv or Google Scholar), reads them,
  and checks whether the claims made in the citing text are supported by the
  sources. Produces an audit report with per-citation verdicts. Triggers:
  audit references, verify citations, check references, citation audit,
  verify bibliography, check my citations, are my references correct,
  fact-check citations, validate sources.
---

# Audit references (citation verification)

This skill verifies that the citations in a document actually say what the
author claims they say. It complements `update-references` (which discovers
new papers) by auditing existing citations for correctness.

The output is an audit report: one entry per citation, with a verdict
(supported, unsupported, misattributed, not-found) and the evidence from the
source paper.

## Where things live

- **Document:** The markdown file the user points you at, or the most obvious
  draft in the working directory. Look for `.md` files that contain `[@`
  citations.
- **Database:** `references.yaml` in the working directory (or at the nearest
  ancestor that has one). This is the Citation Style Language (CSL) YAML bibliography that pandoc and
  `update-references` both use.
- **PDFs/papers:** `<db-dir>/pdfs/` and `<db-dir>/papers/` — the same locations
  `update-references` uses. If a paper was already fetched, reuse its markdown.
- **Audit report:** `<db-dir>/audits/<document-stem>-audit.md`, using the
  template in `<skill>/references/audit-template.md`.

## Prerequisites

The document must use pandoc citation syntax: `[@citation-id]`, `[@id1; @id2]`,
or `@citation-id` inline. The citation ids must match entries in
`references.yaml`.

If `references.yaml` does not exist in the paper directory, stop and tell the
user. They need to create it first (using `update-references` or manually).

## Running the scripts

This skill and the `update-references` scripts it calls run in the pixi-managed
environment that ships beside the skills. The agent provisions it on repo open
via `<agent-dir>/scripts/ensure-env.sh`; the commands below use `$RUN`:

```bash
RUN="pixi run --manifest-path <skill>/../../pixi.toml python"
```

No `pip install` is needed — the environment supplies PyYAML and the PDF
libraries.

## The workflow

### 1. Extract citations

Run the extraction script to get every citation and its surrounding context:

```bash
$RUN <skill>/scripts/extract_citations.py <document-path>
```

This outputs a JSON array of objects, each with:
- `citation_id`: the pandoc citation key
- `context`: the sentence or paragraph surrounding the citation
- `line`: the line number in the source document
- `claim`: a best-effort extraction of the claim being made (the sentence
  containing the citation)

Review the output. If the document has no citations, report that and stop.

### 2. Resolve against references.yaml

Load `references.yaml` and match each `citation_id` to an entry. Classify each
citation:

- **resolved**: the id matches an entry in `references.yaml`
- **unresolved**: no matching entry — flag this immediately in the report

For resolved citations, note the entry's `arxiv_id` (if present), `URL`,
`title`, and `author` fields. These are needed to fetch the paper.

### 3. Fetch and read cited papers

For each resolved citation, get the paper text:

1. **Already fetched?** Check if `md_path` (or legacy `text_path`) or `pdf_path`
   exists in the database entry and the file is on disk. If so, read the
   markdown file directly. If only a PDF exists without markdown, run `repair`
   first to generate it.

2. **Has arxiv_id?** Fetch via the sibling skill's script:
   ```bash
   $RUN .agents/skills/update-references/scripts/arxiv.py \
     --db <db-path> fetch --id <arxiv_id>
   ```
   Then read the markdown conversion it produces.

3. **No arxiv_id?** Search Google Scholar for the title:
   ```bash
   $RUN .agents/skills/update-references/scripts/scholar.py \
     --db <db-path> search --query "<paper title>" --max 3
   ```
   If a match is found with a PDF link, fetch it:
   ```bash
   $RUN .agents/skills/update-references/scripts/scholar.py \
     --db <db-path> fetch --title "<title>" --url "<pdf_url>" \
     --authors "Given Family" --year YYYY
   ```

4. **Cannot fetch?** Mark the citation as `not-found` in the report and move on.

### 4. Verify claims

For each citation where you have the paper text, read the relevant sections and
evaluate the claim made in the citing document:

- **supported**: the source paper contains evidence that backs the claim.
  Quote the relevant passage (one or two sentences).
- **unsupported**: the source paper does not contain evidence for the claim.
  Explain what the paper actually says about the topic.
- **misattributed**: the claim is true but attributed to the wrong source, or
  the source says something different from what is claimed. Explain the
  discrepancy.
- **not-found**: the paper could not be located or accessed.

Be precise. A claim like "Smith et al. show 30% improvement" requires finding
that specific number in the source. A paraphrase like "Smith et al. demonstrate
significant gains" needs the source to actually demonstrate gains in the claimed
domain.

### 5. Write the audit report

Use the template at `<skill>/references/audit-template.md`. Write the report to
`<db-dir>/audits/<document-stem>-audit.md`.

### 6. Report back

Summarize the results:
- Total citations found
- How many resolved vs. unresolved
- Verdicts: N supported, N unsupported, N misattributed, N not-found
- Call out any unsupported or misattributed citations explicitly — these need
  the author's attention

## Dependencies

Same as `update-references`: the shared pixi environment supplies PyYAML and
`pymupdf4llm` for PDF-to-markdown conversion, provisioned by `ensure-env.sh`
with no `pip install`. The extraction script is pure Python stdlib. arXiv and
Scholar access use the sibling skill's scripts, run through the same `$RUN`
wrapper.
