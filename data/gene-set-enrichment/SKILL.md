---
name: gene-set-enrichment
description: Perform gene set enrichment analysis using AI research providers. Analyzes lists of genes to identify biological themes, pathways, and functional associations.
---

# gene-set-enrichment

Toolkit for performing gene set enrichment analysis on lists of genes using AI research providers. Identifies biological themes, pathways, diseases, and functional relationships within gene sets.

## When to Use

Use this skill when:
- The user provides a list of genes and wants to understand what they have in common
- The user needs pathway or functional enrichment analysis
- The user wants to identify biological themes in differential expression results
- The user needs to understand disease associations for a gene set
- The user has genomic analysis results and wants biological interpretation

## Default Configuration

**This skill uses HEAVYWEIGHT mode by default:**
- **Provider**: Perplexity
- **Model**: `sonar-deep-research` 
- **Rationale**: Extensive research is required to give meaningful results.

Users can override to use comprehensive mode if needed for publication-quality analysis.

## Features

- **Pathway Analysis**: Identifies enriched biological pathways
- **Disease Associations**: Finds disease connections for gene sets
- **Functional Themes**: Discovers common biological functions
- **Tissue Specificity**: Analyzes expression patterns across tissues
- **Drug Targets**: Identifies potential therapeutic connections
- **Template-Based**: Reusable template with space-separated gene lists

## Required Environment Variables

```bash
# At least one is required:
export PERPLEXITY_API_KEY="your-perplexity-key"   # Recommended for speed
export OPENAI_API_KEY="your-openai-key"           # For comprehensive analysis
export FUTUREHOUSE_API_KEY="your-futurehouse-key" # For scientific literature
```

## Basic Usage

### Using the Template (Recommended)

```bash
# Quick enrichment analysis
uv run deep-research-client research \
  --template .claude/skills/gene-set-enrichment/examples/enrichment_template.md \
  --var "geneset=APOH APP COL3A1 VEGFA THBD" \
  --var "organism=human" \
  --provider perplexity \
  --model sonar-deep-research \
  --output enrichment_results.md

# Comprehensive analysis (slower, more detailed)
uv run deep-research-client research \
  --template .claude/skills/gene-set-enrichment/examples/enrichment_template.md \
  --var "geneset=APOH APP COL3A1 VEGFA THBD" \
  --var "organism=human" \
  --provider openai \
  --output enrichment_detailed.md
```

### Direct Query (No Template)

```bash
uv run deep-research-client research \
  "Perform gene set enrichment analysis on: APOH APP COL3A1 VEGFA THBD. Identify common pathways, biological processes, and disease associations." \
  --provider perplexity \
  --model sonar-deep-research \
  --output quick_enrichment.md
```

## Template Variables

The enrichment template accepts:

- `{geneset}` - **Space-separated** list of gene symbols (e.g., "APOH APP VEGFA")
- `{organism}` - Organism name (e.g., "human", "mouse", "rat")
- `{context}` - Optional: Study context (e.g., "upregulated in heart disease", "differentially expressed in cancer")

## Workflow

1. **Prepare gene list**: Convert gene list to space-separated format
2. **Choose analysis mode**:
   - Fast (sonar-pro): Quick exploratory analysis
   - Comprehensive (openai): Publication-quality detailed analysis
3. **Run template**: Use template with geneset variable
4. **Review results**: Check identified pathways, functions, diseases
5. **Iterate**: Refine analysis based on initial results

## Output Format

Results include:

- **Enriched Pathways**: KEGG, Reactome, WikiPathways
- **Biological Processes**: GO terms and functional categories
- **Disease Associations**: OMIM, disease databases
- **Tissue Expression**: Where genes are co-expressed
- **Protein Interactions**: Known interaction networks
- **Drug Connections**: Therapeutic targets and compounds
- **Citations**: Links to relevant databases and publications

## Example Gene Sets

### Cardiovascular/ECM Example (36 genes)
```
APOH APP CND2 COL3A1 COL5A2 CXCL6 FGFR1 FSTL1 ITGAV JAG1 JAG2 KCNJ8 LPL LRPAP1 LUM MSX1 NRP1 OLR1 PDGFA PF4 PGLYRP1 POSTN PRG2 PTK2 S100A4 SERPINA5 SLCO2A1 SPP1 STC1 THBD TIMP1 TNFRSF21 VAV2 VCAN VEGFA VTN
```

This set appears enriched for:
- Extracellular matrix organization
- Cardiovascular development
- Angiogenesis and vascular remodeling
- Cell adhesion and migration

### Small Test Set
```
TP53 BRCA1 BRCA2 PTEN RB1
```

Cancer-related tumor suppressors for testing.

## Common Patterns

### Quick exploratory enrichment
```bash
uv run deep-research-client research \
  --template .claude/skills/gene-set-enrichment/examples/enrichment_template.md \
  --var "geneset=GENE1 GENE2 GENE3" \
  --var "organism=human" \
  --provider perplexity \
  --model sonar-pro
```

### Context-specific enrichment
```bash
uv run deep-research-client research \
  --template .claude/skills/gene-set-enrichment/examples/enrichment_template.md \
  --var "geneset=GENE1 GENE2 GENE3" \
  --var "organism=human" \
  --var "context=upregulated in diabetic cardiomyopathy" \
  --var "focus=cardiac remodeling pathways"
```

### Comprehensive publication-quality
```bash
uv run deep-research-client research \
  --template .claude/skills/gene-set-enrichment/examples/enrichment_template.md \
  --var "geneset=GENE1 GENE2 GENE3" \
  --var "organism=human" \
  --provider openai
```

## Tips for Best Results

1. **Gene Symbol Format**: Use official gene symbols (HUGO for human, MGI for mouse)
2. **List Size**: Works best with 10-500 genes
   - Too few (<5): Limited statistical power
   - Too many (>1000): May be too broad
3. **Organism**: Specify organism to avoid ambiguity
4. **Context**: Add experimental context for more relevant results
5. **Iteration**: Start with fast mode, then use comprehensive for final analysis
6. **Caching**: Results are cached - use `--no-cache` to force re-analysis with updated databases

## Integration with Analysis Pipelines

### From differential expression results
```python
# Python example: extract top genes
import pandas as pd

# Load DEG results
degs = pd.read_csv("deg_results.csv")
top_genes = degs[degs['padj'] < 0.05].head(50)['gene_symbol'].tolist()
geneset = " ".join(top_genes)

# Use with template
print(f"--var \"geneset={geneset}\"")
```

### From genomic analysis
```bash
# Extract gene symbols from analysis output
cut -f1 significant_genes.txt | tr '\n' ' ' > geneset.txt

# Use in template
uv run deep-research-client research \
  --template .claude/skills/gene-set-enrichment/examples/enrichment_template.md \
  --var "geneset=$(cat geneset.txt)" \
  --var "organism=human"
```

## Comparison with Traditional Tools

This AI-based approach complements traditional enrichment tools (DAVID, Enrichr, g:Profiler):

**Advantages:**
- Natural language interpretation
- Integrated cross-database search
- Literature context and recent discoveries
- Flexible, conversational analysis

**Traditional Tools Still Better For:**
- Precise statistical p-values
- Large-scale batch processing
- Specific database versions
- Reproducible computational workflows

**Best Practice**: Use both approaches:
1. Run traditional enrichment for statistics
2. Use this skill for biological interpretation and context

## Important Notes

- **Default is fast mode**: Uses sonar-pro for quick results
- **Gene symbols**: Use standard nomenclature (HGNC for human)
- **List format**: Space-separated gene symbols in the template variable
- **Caching**: Results cached by gene set and provider
- **Updates**: AI models have knowledge cutoff - very recent discoveries may not be included
- **Validation**: Cross-reference with traditional enrichment tools for important findings

## Related Skills

- **run-deep-research**: For individual gene deep-dive analysis
- Custom analysis workflows can combine both skills
