---
name: create-skill-to-treat-cancer
description: >-
  Converts NCCN clinical practice guideline PDFs into structured skill packages
  for cancer treatment navigation. Use when given an NCCN PDF to create a clinical
  decision-support skill with progressive disclosure from diagnosis to treatment.
  Handles chunking, parallel Haiku conversion, validation, and assembly.
metadata:
  author: nccn-skill-generator
  version: "1.0"
license: Apache-2.0
compatibility: Requires Python 3.10+ with PyMuPDF (pymupdf). Claude Code with Agent tool for parallel dispatch.
---

# Create Skill to Treat Cancer

Converts an NCCN clinical practice guideline PDF into a Vercel Skills protocol
package with progressive disclosure: disease subtype → stage → treatment line → regimen.

## Prerequisites

- Python 3.10+ with PyMuPDF: `uv pip install pymupdf`
- Claude Code with Agent tool access (for Haiku dispatch)
- A valid NCCN account and cookie for PDF download (or bring your own PDF)
- `fzf` for interactive guideline selection (optional): `brew install fzf`

## Workflow Checklist

Copy and track progress:

```
- [ ] Step 0: Download NCCN guideline PDF
- [ ] Step 1: Extract PDF structure
- [ ] Step 2: Chunk PDF by disease/section
- [ ] Step 3: Convert chunks via parallel Haiku agents
- [ ] Step 4: Assemble output skill package
- [ ] Step 5: Validate (links, citations, format)
- [ ] Step 6: Final review
```

---

## Step 0: Download NCCN Guideline PDF

Download the source PDF using the built-in downloader:

```bash
# Interactive mode (fzf picker from 87 available guidelines)
bash scripts/download_nccn.sh

# Direct download by identifier
bash scripts/download_nccn.sh b-cell
bash scripts/download_nccn.sh nscl
bash scripts/download_nccn.sh breast

# Batch download from a list file
bash scripts/download_nccn.sh --batch nccnlist.txt

# List all available identifiers
bash scripts/download_nccn.sh --list
```

**Cookie setup** (required for NCCN authentication):
1. Log in to [nccn.org](https://www.nccn.org) with a valid professional account
2. Use a browser extension (e.g., [cookie-cook](https://github.com/gaoliang/cookie-cook))
   to export your session cookie as an HTTP Header value
3. Save it to `cookie.txt` in your working directory

The cookie file is gitignored and never committed.

Output: `NCCN-<identifier>-<date>.pdf` in the current directory.

See `assets/nccn_dict.txt` for the full list of 87 guideline identifiers.

## Directory Convention

All paths below use these variables:

- `CANCER` — kebab-case cancer name (e.g., `b-cell-lymphomas`, `breast-cancer`)
- `TMP=tmp/${CANCER}` — intermediate pipeline artifacts (gitignored)
- `OUT=nccn-cancer-skill/${CANCER}` — final skill package (committed)

```
nccn-skill/
├── tmp/<CANCER>/              # Intermediate (gitignored)
│   ├── toc.json
│   ├── chunks/
│   ├── converted/
│   └── merged/
└── nccn-cancer-skill/<CANCER>/ # Final output (committed)
    ├── SKILL.md
    └── references/
```

## Step 1: Extract PDF Structure

```bash
mkdir -p tmp/${CANCER}
python scripts/extract_toc.py <input.pdf> --output tmp/${CANCER}/toc.json
```

This produces `toc.json` containing:
- Hierarchical TOC entries with page ranges
- Algorithm/manuscript boundary detection
- Chunk definitions with IDs, types, and output filenames

**Verify**: Check the summary output. Expect:
- 10-20 disease-algorithm chunks
- 10-20 disease-manuscript chunks
- 5-10 shared chunks (supportive care, response criteria, RT, etc.)

## Step 2: Chunk PDF by Disease/Section

```bash
python scripts/chunk_pdf.py <input.pdf> \
  --toc tmp/${CANCER}/toc.json \
  --output-dir tmp/${CANCER}/chunks \
  --max-chars 50000
```

This extracts text for each chunk with `[PAGE XX]` markers for citation tracing.
Chunks exceeding `--max-chars` are automatically split by page boundaries.

See [references/chunking-strategy.md](references/chunking-strategy.md) for the semantic
boundary rules.

**Verify**: Spot-check 2-3 chunk files in `tmp/${CANCER}/chunks/`. Ensure:
- YAML header has correct metadata
- `[PAGE XX]` markers are present
- Text content is readable (not garbled)

## Step 3: Convert Chunks via Parallel Haiku Agents

This is the core conversion step. Each chunk is processed by a Haiku agent using
the appropriate prompt template.

See [references/haiku-dispatch-protocol.md](references/haiku-dispatch-protocol.md) for
the full orchestration procedure.

See [references/conversion-prompts.md](references/conversion-prompts.md) for the exact
prompt templates.

### Quick Summary

1. For each chunk file in `tmp/${CANCER}/chunks/`:
   - Read the chunk's YAML header to determine type (algorithm or manuscript)
   - Select the appropriate prompt template
   - Fill in placeholders: `{{disease_name}}`, `{{guideline_version}}`, `{{page_range}}`
   - Append the chunk text as source material

2. Dispatch Haiku agents in batches of up to 15:
   ```
   Agent(
     model: "haiku",
     run_in_background: true,
     prompt: <filled template + chunk text>
   )
   ```
   Each agent writes output to `tmp/${CANCER}/converted/{output_file}`.

3. Wait for all agents to complete, then verify each output file exists.

4. Run per-worker quality checks:
   - Output file exists and is non-empty
   - Contains at least one `[p.XX]` citation
   - Starts with a markdown heading
   - No `{{` placeholder text remains

5. Retry failed chunks (up to 2 retries).

6. Merge multi-part files:
   ```bash
   python scripts/merge_parts.py \
     --input-dir tmp/${CANCER}/converted \
     --output-dir tmp/${CANCER}/merged
   ```

**Verify**: Check that `tmp/${CANCER}/merged/` has one `.md` file per original chunk.

## Step 4: Assemble Output Skill Package

```bash
python scripts/assemble_skill.py \
  --chunks-dir tmp/${CANCER}/merged \
  --toc tmp/${CANCER}/toc.json \
  --output-dir nccn-cancer-skill/${CANCER} \
  --template assets/skill-md-template.yaml \
  --guideline-name "<Guideline Name>" \
  --version "<version>"
```

Optionally add `--categories <categories.json>` for cancer-specific grouping.

See [references/output-skill-template.md](references/output-skill-template.md) for the
output structure.

This:
- Creates the skill directory with `SKILL.md` and `references/`
- Generates the navigation SKILL.md from template
- Copies converted files to `references/`
- Detects and fixes cross-disease references (e.g., "See NSCLC-1" → proper markdown links)

**Verify**: Open the generated `SKILL.md` and confirm:
- All disease subtypes are listed
- Links point to actual files in `references/`

## Step 5: Validate

Run all three validators:

```bash
python scripts/validate_links.py nccn-cancer-skill/${CANCER}/
python scripts/validate_citations.py nccn-cancer-skill/${CANCER}/
python scripts/check_format.py nccn-cancer-skill/${CANCER}/
```

See [references/validation-pipeline.md](references/validation-pipeline.md) for details
on each validation stage.

### What each validator checks

**Link integrity** (`validate_links.py`):
- Every markdown link resolves to an existing file
- Every reference file is linked from SKILL.md
- Every evidence file has a matching algorithm file

**Citation coverage** (`validate_citations.py`):
- Every factual paragraph has `[p.XX]` citations
- No citations reference pages outside the declared range
- Citation density is adequate (>0.1 citations per content line)

**Format compliance** (`check_format.py`):
- SKILL.md has valid YAML frontmatter
- SKILL.md body < 500 lines
- Name field is valid (lowercase, hyphens, ≤64 chars)
- Long reference files have a table of contents

**All three must pass with zero errors before proceeding.**

## Step 6: Final Review

Manual review checklist:

```
- [ ] Open SKILL.md — does the disease navigation make clinical sense?
- [ ] Spot-check 3 treatment recommendations against the source PDF
- [ ] Verify category ratings (1, 2A, 2B) match the source
- [ ] Check that no treatment options were missed for a disease
- [ ] Confirm cross-disease references resolve correctly
- [ ] Test loading the skill in a Claude Code session
```

### Testing the Skill

Install the generated skill package in a Claude Code project:

```bash
cp -r nccn-cancer-skill/${CANCER}/ ~/.claude/skills/nccn-${CANCER}/
# or project-level:
cp -r nccn-cancer-skill/${CANCER}/ .claude/skills/nccn-${CANCER}/
```

Then test progressive disclosure:
1. Ask about a disease → should load SKILL.md and identify the right reference file
2. Ask about specific treatment → should load the disease reference file
3. Ask about evidence → should load the evidence file

---

## Troubleshooting

### Garbled text in chunks
NCCN algorithm pages are flowcharts. Text extraction may lose spatial relationships.
The conversion prompts handle this, but if a chunk is severely garbled:
- Re-extract with `page.get_text("blocks")` for block-level layout
- Consider using vision model for that specific page range

### Missing manuscript sections
Some diseases may not have a separate manuscript section (they share with a parent).
The assembler handles this — the algorithm file is still generated, just no evidence file.

### Very long output files
If a reference file exceeds 500 lines, consider splitting it by treatment line
(first-line, second-line, etc.) into separate files. Update SKILL.md links accordingly.

### Cross-disease reference failures
The assembler uses fuzzy matching to convert NCCN page codes to file links.
If a reference isn't resolved, it's left as plain text with `[UNRESOLVED: CODE]` marker.
Fix these manually.
