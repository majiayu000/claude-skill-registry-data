---
name: gi-splice
description: Detect splice donor and acceptor sites in DNA sequences using the Genomic Intelligence G0 BigBird transformer, via the hosted /v1/tasks/splice/predict API. Returns per-position site probabilities
  and called sites.
license: MIT
metadata:
  openclaw:
    requires:
      bins:
      - python3
      env: null
      config: null
    always: false
    emoji: ✂️
    homepage: https://docs.genomicintelligence.ai
    os:
    - darwin
    - linux
    install:
    - kind: pip
      package: requests
      bins: null
    trigger_keywords:
    - splice
    - splice site
    - splice donor
    - splice acceptor
    - splicing prediction
    - intron exon boundary
    - cryptic splice site
    - GT-AG site
    - gi splice
    - G0 splice
    - genomic intelligence splice
  author: ClawBio + Genomic Intelligence
  demo_data:
  - path: example_data/splice_hbb.fa
    description: HBB gene body (chr11, GRCh38; reverse-complemented to gene-sense) — bundled real reference sequence.
  dependencies:
    python: '>=3.10'
    packages:
    - requests>=2.31
  domain: genomics
  endpoints:
    cli: python skills/gi-splice/gi_splice.py --input {input_file} --output {output_dir}
  inputs:
  - name: input_file
    type: file
    format:
    - fa
    - fasta
    - fna
    description: Single-record FASTA, typically a gene body (5'UTR → 3'UTR including introns).
    required: false
  outputs:
  - name: report
    type: file
    format: md
    description: Markdown report — sequence + model metadata, called splice sites (position, kind, strand, probability).
  - name: result
    type: file
    format: json
    description: Full `{data, meta}` response from the GI API plus a flattened summary.
  - name: reproducibility
    type: directory
    description: command.sh + environment.json for exact-rerun reproducibility.
  tags:
  - genomics
  - splice
  - splice-site
  - splicing
  - intron-exon
  - dna-lm
  - transformer
  - gi-api
  version: 0.1.0
---

# ✂️ gi-splice

You are **gi-splice**, a ClawBio agent that calls the **Genomic Intelligence** splice-site model. Given a gene-body sequence, it returns called donor/acceptor sites and per-position probabilities via the hosted API.

> ⚠️ **Remote inference — opt-in required.** Unlike most ClawBio skills, this skill uploads your FASTA sequence to the hosted Genomic Intelligence API at `https://api.genomicintelligence.ai`. Prefer a browser? The same models run interactively at <https://genomicintelligence.ai>. **Do not submit identifiable patient data** without an appropriate data-use agreement. Key setup: see [Authentication](#authentication) below.

## Trigger

**Fire this skill when the user says any of:**
- "predict splice sites in this gene"
- "find splice donors/acceptors"
- "score this for cryptic splice sites"
- "splice site prediction"
- "gi-splice", "G0 splice"
- "where does this transcript splice?"

**Do NOT fire when:**
- The user asks for full transcript structure (multi-exon annotation) → `gi-annotation`
- The user asks about variant effect on splicing → use `variant-annotation` (VEP) or chain `gi-splice` ref/alt comparisons

## Why This Exists

- **Without it**: SpliceAI / similar require local GPU + weights + careful preprocessing.
- **With it**: One CLI call → ranked site list with positions and probabilities, in ~1 s.
- **Why ClawBio**: Hosted G0 BigBird inference plus ClawBio's reproducibility bundle and chaining (`gi-splice` → `gi-annotation` → variant interpretation).

## API Backed

`POST https://api.genomicintelligence.ai/v1/tasks/splice/predict` — default model `g0-splice-bigbird` (G0 BigBird transformer; long-context handling for full gene bodies).

## Workflow

1. **Parse**: single-record FASTA via `clawbio.gi.gi_client.read_fasta`.
2. **POST** the full gene body to `/v1/tasks/splice/predict`.
3. **Render**: `report.md` + `result.json` + `reproducibility/`.

## CLI Reference

```bash
# Demo — bundled HBB gene body
python skills/gi-splice/gi_splice.py --demo --output /tmp/gi-splice-demo

# Your own FASTA
python skills/gi-splice/gi_splice.py --input my_gene.fa --output report_dir

# Via ClawBio runner
python clawbio.py run gi-splice --demo
```

## Demo

```bash
python clawbio.py run gi-splice --demo
```

Bundled fixture is HBB (β-globin) gene body, reverse-complemented to gene-sense. HBB has 3 exons / 2 introns; on the coding strand the model calls ~8 sites (≈4 donor + 4 acceptor, including lower-confidence alternates).

## Authentication

The skill requires a Genomic Intelligence partner key in `GI_API_KEY`. Resolution order:

1. `--api-key <value>` CLI flag (explicit override).
2. `GI_API_KEY` environment variable.
3. Otherwise: the skill raises a `RuntimeError` pointing here.

### Quick start — ClawBio hackathon key

A shared hackathon-tier key ships in `.env.example` at the repo root (50 concurrent / 120 rpm, opt-in only). From wherever the ClawBio files live on your machine:

```bash
# Repo root (git clone) — or ~/.claude/plugins/cache/clawbio/clawbio/<version>/ for plugin installs
cp .env.example .env
set -a && source .env && set +a
```

### Production / heavier use

Request an individual key at **contact@genomicintelligence.ai**, then:

```bash
export GI_API_KEY=gi_yourkeyhere
```

## Gotchas

- **Submit gene-sense, not genomic-sense.** Minus-strand genes need RC'd input. The bundled HBB fixture demonstrates this — its FASTA header notes `strand:-1` (gene-sense for the minus-strand HBB gene).
- **Full gene body, not just an exon.** The model uses long context to disambiguate; truncated input degrades accuracy.
- **Donor/acceptor pairs.** The model emits independent site calls. Pair them downstream by ordering + strand consistency if you need intron boundaries.
- **Hackathon key is shared** — `GI_API_KEY` for serious work.

## Output Structure

```
output_dir/
├── report.md              # Site table (position, kind, strand, probability)
├── result.json            # Full {data, meta} envelope
└── reproducibility/
    ├── command.sh
    └── environment.json
```

## Integration with Bio Orchestrator

Routes here on: "splice site", "splice donor", "splice acceptor", "predict splicing".

Chains with: `variant-annotation` (intersect calls with VEP splice consequences), `gi-annotation` (cross-check against predicted exon boundaries).

## Safety

Research tool. Not a clinical assay.
