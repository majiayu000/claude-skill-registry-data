---
name: bio-cosmic
description: "This skill should be used when the user needs to query COSMIC Cancer Gene Census to check if genes are known cancer genes. Triggers include requests to annotate genes with cancer information, check if variants are in cancer genes, or retrieve cancer gene properties from COSMIC database."
user_invocable: true
---

# COSMIC Toolkit

Query COSMIC Cancer Gene Census for cancer gene annotation. Check if genes are known cancer genes and retrieve their properties (role, tier, tumor types, etc.).

## Quick Start

### Install

Install Python dependencies:

```bash
uv pip install pandas typer
```

### Setup COSMIC Data

Download Cancer Gene Census from COSMIC and place it in the `data/` directory:

1. Register at https://cancer.sanger.ac.uk/cosmic/register (free for academic use)
2. Download `cancer_gene_census.csv` from https://cancer.sanger.ac.uk/cosmic/download
3. Place the file at: `cosmic-toolkit/data/cancer_gene_census.csv`

See `data/README.md` for detailed instructions.

### Basic Usage

```bash
# Query single gene
python scripts/query_cosmic_genes.py --gene TP53

# Query multiple genes
python scripts/query_cosmic_genes.py --genes TP53 BRCA1 EGFR

# Query from file
python scripts/query_cosmic_genes.py --gene-list genes.txt --output results.json
```

## Scripts

### query_cosmic_genes.py - Cancer Gene Census Query

Query COSMIC Cancer Gene Census to check if genes are known cancer genes and retrieve their properties.

#### Required Arguments

**One of the following**:
- `--gene TEXT` - Single gene symbol to query
- `--genes TEXT [TEXT ...]` - Multiple gene symbols (space-separated)
- `--gene-list PATH` - File containing gene symbols (one per line)

#### Optional Arguments

**Data Source:**
- `--gene-census PATH` - Path to cancer_gene_census.csv (default: `data/cancer_gene_census.csv`)

**Output:**
- `--output PATH` - Output JSON file path (default: stdout)

#### Output Format (JSON)

The script outputs all columns from the Cancer Gene Census CSV as JSON. Common fields include:

```json
{
  "summary": {
    "total_genes": 3,
    "found_in_cancer_census": 2,
    "not_found": 1
  },
  "genes": {
    "TP53": {
      "found": true,
      "Gene Symbol": "TP53",
      "Name": "tumor protein p53",
      "Entrez GeneId": "7157",
      "Genome Location": "17:7661779-7687538",
      "Tier": "1",
      "Hallmark": "Yes",
      "Chr Band": "17p13.1",
      "Somatic": "yes",
      "Germline": "yes",
      "Tumour Types(Somatic)": "lung NS, breast NS, colorectal NS, ...",
      "Tumour Types(Germline)": "Li-Fraumeni syndrome",
      "Cancer Syndrome": "Li-Fraumeni syndrome",
      "Tissue Type": "E",
      "Molecular Genetics": "Dom",
      "Role in Cancer": "TSG",
      "Mutation Types": "Mis, N, F, D"
    },
    "BRCA1": {
      "found": true,
      "Gene Symbol": "BRCA1",
      "Name": "BRCA1 DNA repair associated",
      "Entrez GeneId": "672",
      "Genome Location": "17:43044295-43125483",
      "Tier": "1",
      "Hallmark": "Yes",
      "Role in Cancer": "TSG",
      "Somatic": "yes",
      "Germline": "yes",
      "Tumour Types(Somatic)": "breast, ovary",
      "Cancer Syndrome": "Breast-ovarian cancer, familial, susceptibility to, 1"
    },
    "UNKNOWN_GENE": {
      "found": false
    }
  }
}
```

**Note**: All columns from the Cancer Gene Census CSV are included in the output. The script dynamically adapts to COSMIC format updates.

#### Usage Examples

```bash
# Query single gene
python scripts/query_cosmic_genes.py --gene TP53

# Query multiple genes
python scripts/query_cosmic_genes.py --genes TP53 BRCA1 EGFR KRAS

# Query from gene list file
python scripts/query_cosmic_genes.py --gene-list candidate_genes.txt

# Save output to file
python scripts/query_cosmic_genes.py \
  --genes TP53 BRCA1 EGFR \
  --output cancer_genes.json

# Use custom Cancer Gene Census file
python scripts/query_cosmic_genes.py \
  --gene TP53 \
  --gene-census /path/to/cancer_gene_census.csv
```

## Workflow Examples

### Example 1: Annotate WGS Candidate Genes

Filter WGS results to known cancer genes:

```bash
# Step 1: Extract gene names from VCF (using bcftools or grep)
bcftools query -f '%INFO/GENE\n' variants.vcf | sort -u > candidate_genes.txt

# Step 2: Check which genes are in Cancer Gene Census
python scripts/query_cosmic_genes.py \
  --gene-list candidate_genes.txt \
  --output cancer_gene_annotation.json

# Step 3: Parse results to filter cancer genes only
jq '.genes | to_entries | map(select(.value.found == true)) | from_entries' cancer_gene_annotation.json
```

### Example 2: Identify Tier 1 Cancer Genes

Filter results to only Tier 1 cancer genes (highest confidence):

```bash
# Query genes
python scripts/query_cosmic_genes.py \
  --gene-list genes.txt \
  --output results.json

# Filter to Tier 1 genes only
jq '.genes | to_entries | map(select(.value.Tier == "1")) | from_entries' results.json
```

### Example 3: Separate Oncogenes and Tumor Suppressors

Classify cancer genes by their role:

```bash
# Query genes
python scripts/query_cosmic_genes.py \
  --genes TP53 BRCA1 EGFR KRAS MYC \
  --output cancer_genes.json

# Extract tumor suppressor genes (TSG)
jq '.genes | to_entries | map(select(.value."Role in Cancer" | contains("TSG"))) | from_entries' cancer_genes.json

# Extract oncogenes
jq '.genes | to_entries | map(select(.value."Role in Cancer" | contains("oncogene"))) | from_entries' cancer_genes.json
```

### Example 4: Check Germline vs Somatic Cancer Genes

Identify genes involved in germline or somatic cancer:

```bash
# Query genes
python scripts/query_cosmic_genes.py \
  --gene-list genes.txt \
  --output results.json

# Filter germline cancer genes
jq '.genes | to_entries | map(select(.value.Germline == "yes")) | from_entries' results.json

# Filter somatic cancer genes
jq '.genes | to_entries | map(select(.value.Somatic == "yes")) | from_entries' results.json
```

## Cancer Gene Census Fields

Common fields in the output (exact fields depend on COSMIC version):

- **Gene Symbol** - Official gene symbol
- **Name** - Full gene name
- **Entrez GeneId** - NCBI Entrez Gene ID
- **Genome Location** - Chromosomal location (GRCh38)
- **Tier** - 1 (high confidence) or 2 (lower confidence)
- **Hallmark** - Hallmark cancer gene (Yes/No)
- **Chr Band** - Cytogenetic band
- **Somatic** - Involved in somatic cancer (yes/no)
- **Germline** - Involved in germline cancer (yes/no)
- **Tumour Types(Somatic)** - Cancer types (somatic)
- **Tumour Types(Germline)** - Cancer syndromes (germline)
- **Cancer Syndrome** - Associated cancer syndrome
- **Tissue Type** - Tissue type (E=epithelial, M=mesenchymal, L=leukemia/lymphoma, etc.)
- **Molecular Genetics** - Inheritance pattern (Dom, Rec)
- **Role in Cancer** - TSG (tumor suppressor), oncogene, or fusion
- **Mutation Types** - Types of mutations (Mis=missense, N=nonsense, F=frameshift, etc.)

## Error Handling

### Cancer Gene Census File Not Found

```bash
$ python scripts/query_cosmic_genes.py --gene TP53

Error: Cancer Gene Census file not found at: data/cancer_gene_census.csv

To use this tool, please download COSMIC data:

1. Register for free academic access:
   https://cancer.sanger.ac.uk/cosmic/register

2. Download Cancer Gene Census:
   https://cancer.sanger.ac.uk/cosmic/download
   File: cancer_gene_census.csv (GRCh38)

3. Place the file at:
   cosmic-toolkit/data/cancer_gene_census.csv

For more information, see: cosmic-toolkit/data/README.md
```

**Solution:** Follow the instructions in `data/README.md` to download and place the Cancer Gene Census file.

### No Input Specified

```bash
$ python scripts/query_cosmic_genes.py

Error: Must specify --gene, --genes, or --gene-list
```

**Solution:** Provide at least one gene to query:

```bash
python scripts/query_cosmic_genes.py --gene TP53
```

### Gene Not Found

Genes not in the Cancer Gene Census will have `"found": false`:

```json
{
  "UNKNOWN_GENE": {
    "found": false
  }
}
```

This is normal and indicates the gene is not in the expert-curated cancer gene list.

## Best Practices

### 1. Keep Cancer Gene Census Updated

COSMIC is updated quarterly. Periodically download the latest version:

```bash
# Download new version and replace existing file
mv ~/Downloads/cancer_gene_census.csv cosmic-toolkit/data/
```

### 2. Use Gene List Files for Batch Queries

For multiple genes, use a gene list file instead of command-line arguments:

```bash
# ✅ Good: Use file for many genes
python scripts/query_cosmic_genes.py --gene-list genes.txt

# ❌ Bad: Long command line
python scripts/query_cosmic_genes.py --genes GENE1 GENE2 GENE3 ... GENE100
```

### 3. Filter Results with jq

Use `jq` to post-process JSON output:

```bash
# Extract only Tier 1 genes
python scripts/query_cosmic_genes.py --gene-list genes.txt | \
  jq '.genes | to_entries | map(select(.value.Tier == "1"))'

# Count tumor suppressor genes
python scripts/query_cosmic_genes.py --gene-list genes.txt | \
  jq '[.genes[] | select(."Role in Cancer" | contains("TSG"))] | length'
```

### 4. Combine with Other Tools

Integrate with WGS analysis workflow:

```bash
# Extract genes from VCF
bcftools query -f '%INFO/GENE\n' variants.vcf | sort -u > genes.txt

# Annotate with COSMIC
python scripts/query_cosmic_genes.py --gene-list genes.txt --output cosmic_annotation.json

# Filter VCF to cancer genes only (using cancer gene list)
jq -r '.genes | to_entries | map(select(.value.found == true)) | .[].key' cosmic_annotation.json > cancer_genes.txt
bcftools view -i "GENE=@cancer_genes.txt" variants.vcf > cancer_variants.vcf
```

## Integration with WGS Pipeline

### Typical WGS Workflow

1. **Variant Calling** → VCF file
2. **Gene Extraction** → Gene list
3. **COSMIC Annotation** → Identify cancer genes
4. **Filtering** → Focus on cancer-relevant variants

### Example Pipeline

```bash
# 1. Extract genes from VCF
bcftools query -f '%INFO/GENE\n' variants.vcf | sort -u > all_genes.txt

# 2. Query COSMIC
python scripts/query_cosmic_genes.py \
  --gene-list all_genes.txt \
  --output cosmic_results.json

# 3. Extract cancer gene names
jq -r '.genes | to_entries | map(select(.value.found == true and .value.Tier == "1")) | .[].key' \
  cosmic_results.json > tier1_cancer_genes.txt

# 4. Filter VCF to Tier 1 cancer genes
grep -f tier1_cancer_genes.txt all_genes.txt | \
  bcftools view -i "GENE=@-" variants.vcf > cancer_variants.vcf
```

## Related Skills

- **vcf-toolkit** - VCF variant analysis and filtering
- **bam-toolkit** - BAM alignment file operations
- **sequence-io** - FASTA/GenBank sequence operations

## Troubleshooting

### CSV Format Changes

The script dynamically reads all columns, so it should adapt to COSMIC format updates. If issues occur:

1. Check the CSV file has a "Gene Symbol" column
2. Verify the file is properly formatted (no corruption)
3. Try re-downloading the file

### Memory Issues with Large Gene Lists

For very large gene lists (>10,000 genes), consider splitting:

```bash
# Split gene list
split -l 1000 large_gene_list.txt genes_part_

# Process each part
for file in genes_part_*; do
  python scripts/query_cosmic_genes.py --gene-list $file --output ${file}.json
done

# Merge results
jq -s 'reduce .[] as $item ({}; . * $item)' genes_part_*.json > merged_results.json
```

## Citation

When using COSMIC data, please cite:

Tate JG, Bamford S, Jubb HC, et al. COSMIC: the Catalogue Of Somatic Mutations In Cancer. Nucleic Acids Research. 2019;47(D1):D941-D947.

## Additional Resources

- **COSMIC Website**: https://cancer.sanger.ac.uk/cosmic
- **Cancer Gene Census**: https://cancer.sanger.ac.uk/census
- **Documentation**: https://cancer.sanger.ac.uk/cosmic/help
