---
name: ocean-genomics
category: science
description: >
  Comprehensive bioinformatics and ocean genomics skill for eDNA metabarcoding, metagenomics,
  protein structure prediction, and marine biodiversity analysis. Use when: (1) Working with DNA/RNA
  sequences (FASTQ, FASTA, SAM/BAM, VCF files), (2) Running BLAST, QIIME2, Kraken2, or Nextflow
  pipelines, (3) Predicting protein structures via ESMFold2, AlphaFold, or ColabFold, (4) Analyzing
  environmental DNA (eDNA) from marine samples, (5) Querying marine databases (OBIS, BOLD, DOO,
  GenBank, UniProt), (6) Using biological foundation models (Evo 2, ESMC/ESMFold2, ProGen3), (7) Setting up
  MCP servers for bioinformatics (gget-mcp, bio-mcp), (8) Building agentic bioinformatics workflows,
  (9) Ocean biodiversity research, deep-sea species discovery, extremophile enzyme characterization,
  (10) Any task involving genomics, proteomics, transcriptomics, or computational biology.
---

# Ocean Genomics

Agentic bioinformatics skill for ocean genomics — from eDNA water sampling to species identification, protein structure prediction, and scientific insight publication.

## Quick Start

### 1. Set Up MCP Integration

Install gget-MCP for immediate access to BLAST, AlphaFold, sequence retrieval, and 9 other genomics tools:

```json
// Add to .claude/settings.json → mcpServers
{
  "gget-mcp": {
    "command": "uvx",
    "args": ["--from", "gget-mcp@latest", "stdio"]
  }
}
```

### 2. Install CLI Tools

```bash
# Core tools
brew install blast mmseqs2 samtools minimap2 nextflow
pip install biopython biotite gget

# Nanopore basecalling (runs on Apple Silicon)
brew install nanoporetech/dorado/dorado

# eDNA pipeline (conda recommended)
conda create -n edna -c bioconda -c conda-forge qiime2 kraken2 fastp fastqc
```

### 3. Install Companion Skills

```bash
npx skills add adaptyvbio/protein-design-skills@alphafold -g -y
npx skills add anthropics/life-sciences@nextflow-development -g -y
npx skills add gptomics/bioskills@bioskills -g -y
npx skills add davila7/claude-code-templates@gget -g -y
```

## Core Workflows

### Workflow A: eDNA Species Inventory

**Trigger**: User has sequencing data from marine water samples and needs species identification.

```
Input: FASTQ files (amplicon sequencing of CO1/16S/18S marker gene)

1. Quality control
   → fastp: trim adapters, filter low-quality reads
   → FastQC + MultiQC: generate QC reports

2. Denoise and classify
   → QIIME2 import → DADA2 denoise → ASV table
   → Taxonomy: classify-sklearn against BOLD (CO1) or SILVA (16S/18S)

3. Diversity analysis
   → Alpha diversity: Shannon, Simpson, Chao1
   → Beta diversity: Bray-Curtis, PCoA ordination
   → Rarefaction curves

4. Species report
   → Taxa count table (species × samples)
   → Novel species flags (CO1 divergence >3% from nearest reference)
   → Upload-ready format for OBIS

Output: Species inventory, diversity metrics, novel species candidates
```

**Nextflow shortcut**: `nextflow run nf-core/ampliseq --input samplesheet.csv --FW_primer <fwd> --RV_primer <rev>`

### Workflow B: Metagenomic Community Profiling

**Trigger**: User has shotgun metagenomic data and needs taxonomic + functional profiles.

```
Input: FASTQ files (shotgun whole-metagenome sequencing)

1. QC → fastp
2. Taxonomic classification → Kraken2 + Bracken (abundance estimation)
3. Functional profiling → HUMAnN3 (metabolic pathways)
4. Assembly (optional) → SPAdes/MEGAHIT → QUAST quality check
5. Binning (optional) → MetaBAT2 → CheckM quality → MAG annotation

Output: Taxonomic profiles, functional pathways, metagenome-assembled genomes (MAGs)
```

**Nextflow shortcut**: `nextflow run nf-core/mag --input samplesheet.csv --assembly_type megahit`

### Workflow C: Novel Protein Characterization

**Trigger**: User has protein sequences (from metagenomics or genome annotation) and needs structure/function prediction.

```
Input: Protein sequences (FASTA)

1. Homology search
   → BLAST/MMseqs2 against UniProt, GenBank nr
   → If match found: annotate function from homolog

2. Structure prediction (if novel / no homolog)
   → Fast screening: ESMFold2 single-sequence mode (no MSA) — legacy: ESMFold
   → With ligands / DNA / RNA / modified AA: AlphaFold 3 (leads both subsets); ESMFold2 if MIT required
   → High accuracy: benchmark ESMFold2 vs AlphaFold 3 / ColabFold on your targets
   → Check confidence: pLDDT >70 = reliable fold

3. Structural search
   → Foldseek against AlphaFold DB + PDB
   → Find structural homologs even without sequence similarity

4. Functional annotation
   → Domain analysis: InterPro scan
   → Pathway mapping: gget enrichr
   → Interaction networks: STRING database

5. Report
   → Structure visualization (PDB files)
   → Functional predictions with confidence scores
   → Comparison to known extremophile enzymes

Output: 3D structures, functional annotations, drug/enzyme candidates
```

### Workflow D: Variant Effect Analysis

**Trigger**: User wants to understand impact of mutations in marine organism genomes.

```
Input: DNA sequences + variants of interest

1. Score variants with Evo 2
   → Zero-shot pathogenicity prediction
   → No fine-tuning needed — works across all species

2. Structural impact (if protein-coding)
   → Translate → AlphaFold → compare wild-type vs mutant structure
   → Stability prediction (ΔΔG estimation)

3. Conservation analysis
   → Multiple sequence alignment (MUSCLE/MAFFT)
   → Conservation scores across species

Output: Variant effect scores, structural impact, conservation context
```

## Tool Reference

### Sequence Analysis

| Task | Tool | Command |
|------|------|---------|
| Nucleotide BLAST | BLAST+ | `blastn -query input.fasta -db nt -evalue 1e-6 -outfmt 6` |
| Protein BLAST | BLAST+ | `blastp -query proteins.fasta -db nr -evalue 1e-10` |
| Fast homology search | MMseqs2 | `mmseqs search queryDB targetDB resultDB tmp` |
| Short read alignment | BWA | `bwa mem ref.fa reads.fq \| samtools sort -o out.bam` |
| Long read alignment | Minimap2 | `minimap2 -ax map-ont ref.fa reads.fq \| samtools sort -o out.bam` |
| BAM statistics | SAMtools | `samtools flagstat aligned.bam` |
| Variant calling | bcftools | `bcftools mpileup -f ref.fa in.bam \| bcftools call -mv` |

### eDNA & Taxonomy

| Task | Tool | Command |
|------|------|---------|
| Amplicon denoising | QIIME2/DADA2 | `qiime dada2 denoise-paired ...` |
| Taxonomic classification | Kraken2 | `kraken2 --db standard --paired R1.fq R2.fq --report report.txt` |
| Abundance estimation | Bracken | `bracken -d db -i report.txt -o output.txt -r 150 -l S` |
| Basecalling (Nanopore) | Dorado | `dorado basecaller sup pod5_dir/ > calls.bam` |

### Structure Prediction

| Task | Tool | Command/API |
|------|------|-------------|
| Fast structure (no MSA) | ESMFold2 / ESMFold2-Fast | `ESMFold2InputBuilder().fold(model, spi, ...)` |
| Fast structure (legacy) | ESMFold | `model.infer_pdb(sequence)` |
| High-accuracy structure | ColabFold | `colabfold_batch input.fasta output/` |
| Complex w/ ligand/DNA/RNA | AlphaFold 3 (ESMFold2 if MIT req.) | `StructurePredictionInput(sequences=[ProteinInput(...), LigandInput(...)])` |
| Complex prediction | AlphaFold 3 | `python run_alphafold.py --input_dir inputs/` |
| Structural search | Foldseek | `foldseek easy-search query.pdb afdb result.m8 tmp` |

### Database Queries (via gget)

```python
import gget

gget.blast("ATCGATCG...")          # BLAST search
gget.alphafold("MVLSPADKTNVK...")  # Structure prediction
gget.seq("ENSG00000012048")        # Fetch sequence
gget.info("BRCA1")                 # Gene metadata
gget.enrichr(["BRCA1", "TP53"])    # Pathway enrichment
gget.pdb("1BNA")                   # PDB structure
```

## File Format Reference

| Format | Extension | Content | When You See It |
|--------|-----------|---------|-----------------|
| **FASTQ** | `.fq`, `.fastq` | Raw reads + quality | Fresh from sequencer |
| **FASTA** | `.fa`, `.fasta`, `.fna` | Sequences (no quality) | References, assemblies |
| **SAM/BAM** | `.sam`, `.bam` | Aligned reads | After alignment |
| **VCF** | `.vcf`, `.vcf.gz` | Variant calls | After variant calling |
| **BED** | `.bed` | Genomic intervals | Feature coordinates |
| **GFF/GTF** | `.gff`, `.gtf` | Gene annotations | Gene models |
| **PDB/mmCIF** | `.pdb`, `.cif` | 3D protein structures | From AlphaFold/PDB |
| **BIOM** | `.biom` | Taxa count tables | From QIIME2 |

## Marine Databases

| Database | URL | Best For |
|----------|-----|----------|
| **OBIS** | obis.org | Marine species occurrence (100M+ records) |
| **BOLD** | boldsystems.org | CO1 barcode species ID |
| **DOO** | deepoceanomics.org | Deep-sea multi-omics (72 genomes, 1112 metagenomes) |
| **GenBank** | ncbi.nlm.nih.gov/genbank | All nucleotide sequences |
| **UniProt** | uniprot.org | Protein sequences + function |
| **AlphaFold DB** | alphafold.ebi.ac.uk | 200M+ predicted structures |
| **ESM Metagenomic Atlas** | esmatlas.com | 617M metagenomic protein structures (Meta FAIR, still live) |
| **ESM Atlas** | biohub.ai/esm/protein/atlas | 6.8B proteins, >1B structures, SAE-feature organized |
| **Tara Oceans** | fondationtaraocean.org | Global ocean microbiome |
| **WoRMS** | marinespecies.org | Marine species taxonomy |

## Foundation Models

| Model | Scale | Input | Best For | Install |
|-------|-------|-------|----------|---------|
| **Evo 2** | 40B params | DNA | Variant effects, genome design | `pip install evo2` |
| **ESMC** | 300M/600M/6B | Protein | Embeddings, SAE features (current gen) | `pip install esm@git+https://github.com/Biohub/esm.git@main` |
| **ESMFold2** | On frozen ESMC 6B | Protein+DNA+RNA+ligand+modified AA | All-atom structure, binder design | same as ESMC · HF `biohub/ESMFold2` |
| **ESM-2** *(legacy)* | 15B params | Protein | Embeddings, contacts | `pip install fair-esm` |
| **ESMFold** *(legacy)* | Based on ESM-2 | Protein | Fast structure prediction | `pip install fair-esm` |
| **AlphaFold 3** | N/A | Protein+DNA+RNA+ligand | High-accuracy complexes | Docker + weights request |
| **ColabFold** | AF2+ESMFold | Protein | Batch structure prediction | `pip install colabfold` |
| **ProGen3** | Billions | Conditioning | Novel protein generation | Proprietary |

> ESM stewardship: Meta FAIR → EvolutionaryScale → **Chan Zuckerberg Biohub**. Repo moved to
> `github.com/Biohub/esm` and relicensed to **MIT** (2026-05-27); `facebookresearch/esm` is
> archived.
>
> Accuracy is **task-dependent**, vendor-self-reported, and not independently replicated as of
> 2026-07-21: ESMFold2 beats AlphaFold 3 head-to-head on protein-protein (76 vs 73) and
> antibody-antigen (53 vs 47), but AF3 leads protein-ligand and protein-DNA. Benchmark your own
> targets.
>
> ⚠️ Local ESMFold2 needs the **Biohub `transformers` fork** (stock transformers has no
> `esmfold2` module) and **Python 3.12 only** — install via
> `pip install esm@git+https://github.com/Biohub/esm.git@main`. **ESMC context window: 2048
> tokens** — chunk longer metagenomic ORFs.

For detailed specifications on each model, see [references/foundation-models.md](references/foundation-models.md).

## Detailed References

- **[references/tools-inventory.md](references/tools-inventory.md)** — Full CLI commands, install instructions, and usage examples for all 30+ tools
- **[references/marine-databases.md](references/marine-databases.md)** — Database catalog with API access patterns
- **[references/foundation-models.md](references/foundation-models.md)** — Technical specs, hardware requirements, and code examples for each model
- **[references/mcp-integration.md](references/mcp-integration.md)** — MCP server setup, agent workflow architecture, and skill companion catalog
