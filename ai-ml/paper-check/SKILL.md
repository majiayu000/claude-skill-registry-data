---
name: paper-check
description: >
  Check a paper against its code, results and citations before submission
  (numbers, terms, code vs paper, formulas vs code, BibTeX and cited claims
  via DBLP and Crossref, eval integrity), and prepare its code for
  open-source release. Use when the user says "verify claims" / "verify
  paper against code", "check numbers" / "do the numbers match" / "are my
  numbers right", "formula vs code", "audit my paper", "cross-check claims
  or results", "paper consistency check", "check citations", "verify
  BibTeX", "publish code" / "open source release" / "code release",
  "structure a research repository for publication", "create reproducible
  research artifacts", "reproducibility checklist for a code release", or
  "prepare for publication".
---

# Paper Check

Every number, method claim and citation in the paper must trace to code, data, results or a cited source. Output a prioritized list of issues with specific fixes.

For a code release request, follow [references/code-release.md](references/code-release.md) and skip Steps 1-4.

## Step 1: Discover Files

1. Find the paper's .tex files (Glob for `**/*.tex`)
2. Identify the main .tex file (usually imports other sections) and the document structure
3. Find .bib files for citation checking
4. Locate result files (JSON, CSV, logs), configs, evaluation scripts and training logs
5. Identify the key code modules referenced by the paper's methods

When you run the checks yourself, read the full paper, or the sections the user names. When you hand checks to subagents, pass them the file paths from items 1-5 instead.

## Step 2: Run the Six Checks

Run all six checks by default. When the user names specific checks (for example only citations or BibTeX), run only those, and only the Step 1 items they need (check 5 needs just the .bib files and the `\cite` sites).

The checks are independent. If the harness supports subagents, they can run in parallel, one check each. Each check returns a structured list of findings.

### 1. Numbers

For every number in the paper (dataset sizes, metric values, percentages, counts):

1. **Extract** the number and its context (section, sentence) from the .tex file
2. **Trace** it to its source: result file, code output, config, log, or tracking system
3. **Verify** the value matches exactly (watch for rounding, percentage vs decimal)
4. **Note** rounding conventions and check they are consistent
5. **Flag** any number that does not match its source or cannot be traced

Record each number as a row of the Numerical Audit table in Output Format.

Common numerical errors:
- Rounding inconsistencies (3.14 in text, 3.1415 in table)
- Stale numbers from earlier experiments not updated after re-runs
- Percentage vs absolute confusion
- Off-by-one in dataset counts (headers counted, or not)

### 2. Terms

1. **Extract** all defined terms from the methods section
2. **Search** for each term across ALL sections
3. **Flag** any inconsistent usage:
   - Same concept, different names (e.g., "tag head" vs "classification head")
   - Same name, different meanings across sections
   - Defined but never used, or used but never defined

### 3. Code vs Paper

For each method or algorithm described in the paper:

1. **Find** the corresponding code (function, class, module)
2. **Compare** the paper's description with the actual implementation
3. **Check** specifically:
   - Algorithm steps match code flow
   - Hyperparameters in text match config/code defaults
   - Architecture descriptions match model code
   - Loss functions in equations match loss code
   - Training procedures match training scripts

Common mismatches:
- Paper describes an idealized version, code has edge cases not mentioned
- Hyperparameters changed during development but paper not updated
- Paper describes a method that was later modified or removed from code

### 4. Formulas vs Code

For each equation in the paper:

1. **Identify** the equation and its variables
2. **Find** the code that implements it
3. **Map** each mathematical operation to its code equivalent
4. **Verify**:
   - Summation bounds match loop bounds
   - Division operations handle edge cases
   - Normalization factors match
   - Gradient flow matches (detach, no_grad)
   - Reduction operations (mean vs sum) match

### 5. Citations

Read the .bib file(s). Search the .tex files for citation patterns (`\cite{...}`, `\citep{...}`, `\citet{...}`) to find where each entry is used. Check every entry. For a quick pass, spot-check the 5 most important citations.

1. Extract the claim and the cited paper key.

   Use `paper-search tool get_crossref_paper_by_doi <doi>` to retrieve the cited record. For an arXiv paper, use `paper-search download arxiv <id>` and `paper-search read arxiv <id>`. Follow [paper search setup](../literature-research/references/paper-search.md) if the CLI is missing. Inspect the PDF itself when text extraction loses table or equation layout.

2. Verify BibTeX metadata against DBLP. Search DBLP for the paper title via web search (query: `site:dblp.org "paper title"`) and check:
   - Author names (exact spelling, correct order, completeness)
   - Paper title (exact, from the published version, not the preprint title), and cite the published version when one exists
   - Venue (conference or journal name) and year (publication year, not submission or preprint year), confirmed against the actual publication

   Flag any discrepancy with the corrected value.

3. For cited claims with specific numbers:
   - Locate the exact table, figure or text in the cited paper
   - Verify the number matches what the citing paper states
   - If the claim cannot be verified, or the cited paper does not make the claim at all, suggest qualitative language instead

### 6. Eval Integrity

Read the evaluation scripts and result files. Check for:
- Data leakage between train/val/test splits
- Off-by-one errors in metric computation
- Wrong aggregation methods (micro vs macro)
- Mismatched ground-truth and prediction alignment
- Zero-division edge cases
- Results that don't reproduce from the evaluation scripts

Run the evaluation if possible and compare its output to the paper's values.

## Step 3: Merge Findings

Merge all findings into one prioritized list:
- **HIGH** (must fix before submission): incorrect numbers, wrong claims, missing citations
- **MEDIUM** (should address): terminology inconsistencies, stale but close numbers
- **LOW** (nice to have): minor formatting, optional improvements

Before reporting, check the findings:
1. Every flagged issue is backed by specific evidence (file path, line number, exact value)
2. Numerical comparisons are exact, not approximate
3. Verified issues are kept apart from suspected issues
4. Each suggested fix is specific enough to act on

Refine any finding that fails these checks.

## Output Format

```
## Paper Check Report

### Summary
- Files checked: N .tex files, M code files, K result files
- Issues found: X HIGH, Y MEDIUM, Z LOW

### HIGH
1. [Check] Description
   - Paper says: "..." (file:line)
   - Code/data shows: "..." (file:line)
   - Suggested fix: specific replacement text

### MEDIUM
[Same format]

### LOW
[Same format]

### Numerical Audit
| Paper claim | Location (.tex) | Source file/code | Source value | Match? |
|-------------|-----------------|-----------------|-------------|--------|

### Unverified Claims
| .tex location | Claim | Cited paper | Status | Suggestion |
|--------------|-------|------------|--------|------------|

### Corrected BibTeX Entries
(Ready-to-paste corrected entries for any that need fixing, each with a comment naming its DBLP or Crossref source)

### Verified Claims
(Claims checked and correct)
```

Tag each issue with its check name.

## Step 4: Auto-Fix Offer

For HIGH priority issues that have clear fixes (wrong numbers, typos, stale values):
- Show the exact .tex location and current text
- Show the verified correct value from the source
- Ask the user for confirmation before applying fixes
