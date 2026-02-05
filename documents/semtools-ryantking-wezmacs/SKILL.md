---
name: semtools
description: High-performance semantic search and document parsing toolkit. Use PROACTIVELY for searching across documentation, YAML manifests, configuration files, or any text where semantic understanding is needed. Particularly effective when exploring unfamiliar codebases, finding conceptually related content, or when exact keywords don't match the desired information.
---

# Semtools - Semantic Search & Document Parsing

## Overview

Semtools is a high-performance CLI toolkit providing semantic search capabilities using AI embeddings and document parsing for unsupported formats. Unlike traditional text search (grep), semtools understands semantic meaning, enabling discovery of conceptually related content even when exact keywords don't match.

## When to Use This Skill

Use semtools PROACTIVELY when:

### Documentation & Configuration Exploration
- Searching across `docs/` for relevant guides, architecture docs, or reference materials
- Finding examples in YAML manifests (ArgoCD applications, Helm values, Crossplane XRDs)
- Locating configuration patterns in `config/`, `terraform/`, or application directories
- Exploring unfamiliar parts of the codebase to understand patterns and conventions

### Semantic Understanding Requirements
- When keyword search (grep) returns too many irrelevant results or misses important content
- When searching for concepts that might be described using different terminology
- When exploring how a feature or pattern is implemented across the codebase
- When the exact wording is unknown but the concept is clear

### Document Analysis
- Parsing and searching PDF documentation, vendor guides, or research papers
- Analyzing large collections of heterogeneous documents
- Extracting information from Office documents (DOCX, PPTX)

### Examples of When to Use
- "Find all examples of Vault authentication configuration" (may be described as "Vault auth", "authentication to Vault", "Vault login", etc.)
- "Search for documentation about Crossplane composition patterns" (semantic understanding of "composition" vs "XRD" vs "managed resources")
- "Locate YAML manifests using external secrets" (finds various ways of referencing external secrets)
- "Find similar error handling patterns" (understands conceptual similarity, not just keyword matches)

## Installation & Setup

Semtools requires Rust and a LlamaCloud API key for parsing operations.

```bash
# Install semtools
cargo install semtools

# Set API key (required for parse command)
export LLAMA_CLOUD_API_KEY=your_api_key

# Add to shell profile for persistence
echo 'export LLAMA_CLOUD_API_KEY=your_api_key' >> ~/.zshrc
```

## Core Workflow: Search Documentation

The primary workflow when searching documentation or configuration files:

### Step 1: Decide on Workspace Usage

Create a workspace for repeated searches or large file collections:

```bash
# Create/activate workspace (recommended for multiple searches)
workspace use cluster-ops-docs
export SEMTOOLS_WORKSPACE=cluster-ops-docs
```

Skip workspace for one-off quick searches.

### Step 2: Execute Semantic Search

Use recommended flags for consistent, high-quality results:

```bash
search "vault OIDC authentication" docs/ \
  --ignore-case \
  --n-lines 30 \
  --max-distance 0.3
```

**Flag explanation:**
- `--ignore-case` (or `-i`): Case-insensitive matching (ALWAYS use this)
- `--n-lines 30` (or `-n 30`): Context lines (default 3 is too small, use 30-50)
- `--max-distance 0.3` (or `-m 0.3`): Similarity threshold (0.3 is good default)

### Step 3: Refine if Needed

Adjust search parameters based on results:

```bash
# Too many results? Tighten similarity threshold
search "query" docs/ -i -n 30 -m 0.2

# Too few results? Loosen similarity threshold
search "query" docs/ -i -n 30 -m 0.4

# Need more context? Increase lines
search "query" docs/ -i -n 50 -m 0.3
```

## Common Search Patterns

### Pattern 1: Quick Documentation Search

For one-off searches without workspace overhead:

```bash
search "crossplane composition patterns" docs/ -i -n 30 -m 0.3
```

### Pattern 2: Research Mode with Workspace

For exploring a topic with multiple related searches:

```bash
# Setup workspace once
workspace use architecture-research
export SEMTOOLS_WORKSPACE=architecture-research

# Multiple searches (fast after first one)
search "service mesh networking" docs/ -i -n 30 -m 0.3
search "cilium cluster mesh" docs/ -i -n 30 -m 0.3
search "BGP configuration" docs/ -i -n 30 -m 0.3
```

### Pattern 3: Multi-Directory Configuration Search

Search across multiple directories for configuration patterns:

```bash
search "external secrets configuration" apps/ argocd/ crossplane/ \
  -i -n 40 -m 0.3
```

### Pattern 4: YAML Manifest Search

Find specific patterns in Kubernetes/Helm manifests:

```bash
# Find ingress configurations with authentication
search "ingress with oauth2 proxy" apps/ -i -n 30 -m 0.3

# Find Crossplane resource examples
search "vault kubernetes role composition" crossplane/ -i -n 30 -m 0.3

# Find ArgoCD sync configurations
search "sync waves and hooks" argocd/ -i -n 25 -m 0.3
```

### Pattern 5: Pre-filter with grep

Combine exact-match filtering with semantic search:

```bash
# Find files mentioning "vault", then semantic search within
grep -l "vault" apps/*/values.yaml | \
  xargs search "authentication configuration" -i -n 30 -m 0.3

# Pre-filter by section, then semantic search
cat docs/reference/*.md | grep -A 50 "## Authentication" | \
  search "OIDC provider setup" -i -n 20 -m 0.3
```

## Document Parsing Workflow

Parse unsupported file formats (PDF, DOCX, PPTX) into searchable markdown.

### Step 1: Create Workspace for PDFs

```bash
workspace use vendor-docs
export SEMTOOLS_WORKSPACE=vendor-docs
```

### Step 2: Parse Documents

```bash
# Parse PDFs (results cached to ~/.parse/)
parse docs/vendor/*.pdf

# Parse multiple formats
parse whitepaper.pdf guide.docx presentation.pptx
```

### Step 3: Search Parsed Content

```bash
# Search cached parsed files
search "API authentication" ~/.parse/*.pdf.md -i -n 30 -m 0.3

# Or parse and search in pipeline
parse document.pdf | xargs cat | search "security model" -i -n 40 -m 0.3
```

### Step 4: Repeated Searches

Subsequent searches use cached embeddings (very fast):

```bash
search "rate limiting" ~/.parse/ -i -n 30 -m 0.3
search "error handling" ~/.parse/ -i -n 30 -m 0.3
```

## Advanced Workflows

### Workflow: Complex Research Pipeline

Chain Unix tools for powerful document processing:

```bash
# Find YAML files, pre-filter with grep, then semantic search
find apps/ argocd/ -name "*.yaml" | \
  xargs cat | \
  grep -i "ingress" | \
  search "TLS certificate management" -i -n 30 -m 0.3
```

### Workflow: PDF Document Analysis

Analyze large PDF collections efficiently:

```bash
# Setup dedicated workspace
workspace use research-papers
export SEMTOOLS_WORKSPACE=research-papers

# Parse all PDFs once (cached)
parse papers/*.pdf

# Run multiple semantic queries (fast)
search "kubernetes security" ~/.parse/ -i -n 50 -m 0.2
search "container isolation" ~/.parse/ -i -n 50 -m 0.3
search "network policies" ~/.parse/ -i -n 50 -m 0.3

# Clean up when done
workspace prune
```

### Workflow: Codebase Pattern Discovery

Discover how patterns are implemented across the codebase:

```bash
# Find authentication implementations
search "authentication middleware" src/ -i -n 40 -m 0.3

# Find error handling patterns
search "error propagation patterns" src/ lib/ -i -n 30 -m 0.3

# Find similar API endpoint structures
search "REST endpoint with validation" src/api/ -i -n 35 -m 0.3
```

## Understanding Distance Thresholds

The `--max-distance` parameter controls semantic similarity (cosine distance):

| Threshold | Precision | Recall | Use When |
|-----------|-----------|--------|----------|
| **0.2** | Very High | Low | Need only highly relevant, precise matches |
| **0.3** | High | Medium | **Recommended default**, good balance |
| **0.4** | Medium | High | Exploratory search, broader results |
| **0.5+** | Low | Very High | Very broad search, discovery mode |

**General guidance:**
- Start with **0.3** (good default)
- If too many irrelevant results → decrease to 0.2
- If missing relevant results → increase to 0.4
- For discovery/exploration → use 0.4-0.5

## Best Practices

### 1. Always Use These Three Flags

For consistent, high-quality results, always use:

```bash
search "query" path/ -i -n 30 -m 0.3
```

**Why:**
- `-i`: Don't know how terms are capitalized in files
- `-n 30`: Default 3 is rarely sufficient context (use 30-50)
- `-m 0.3`: Good precision/recall balance

### 2. Use Workspaces for Large Operations

Create workspace before searching large file collections or running multiple related searches:

```bash
workspace use project-name
export SEMTOOLS_WORKSPACE=project-name
# First search generates embeddings (slower)
# Subsequent searches use cache (much faster)
```

**Benefits:**
- Dramatically faster repeated searches
- Cost-effective (avoids re-embedding)
- Automatic cache invalidation when files change

### 3. Pre-parse PDFs Once

Parse PDFs as a one-time operation, then search cached markdown:

```bash
# Parse once
parse documents/*.pdf

# Search many times (fast)
search "topic 1" ~/.parse/ -i -n 30 -m 0.3
search "topic 2" ~/.parse/ -i -n 30 -m 0.3
```

### 4. Chain with grep for Exact Pre-filtering

Combine exact-match filtering with semantic understanding:

```bash
# Find files with exact keyword, then semantic search
grep -l "kubernetes" docs/*.md | \
  xargs search "authentication patterns" -i -n 30 -m 0.3
```

### 5. Adjust Context Lines Based on Content Type

Different content types need different context amounts:

```bash
# Code/configs: 30-40 lines
search "query" src/ -i -n 35 -m 0.3

# Documentation: 40-50 lines
search "query" docs/ -i -n 45 -m 0.3

# Dense technical docs: 50+ lines
search "query" papers/ -i -n 60 -m 0.3
```

## When NOT to Use Semtools

Don't use semtools when:

### 1. Simple Exact-Match Search
Use `grep` or `Grep tool` for literal string matching:
```bash
# Use grep, not semtools
grep -r "function_name" src/
grep "exact error message" logs/*.txt
```

### 2. Code Structure Search
Use `ast-grep` for AST-based code pattern matching:
```bash
# Use ast-grep, not semtools
ast-grep --pattern 'async function $NAME($$$)'
```

### 3. File Name Search
Use `find` or `Glob tool` for file path patterns:
```bash
# Use find/glob, not semtools
find . -name "*.yaml"
glob "apps/**/*.values.yaml"
```

### 4. Real-time Operations
Semtools requires embedding time; use grep for instant results:
```bash
# For instant results, use grep
grep "ERROR" logs/current.log
```

### 5. Very Small or Single-File Searches
Use native tools for focused, single-file operations:
```bash
# Use grep for single files
grep "keyword" single_file.txt
```

## Tool Selection Guide

| Need | Tool | Reason |
|------|------|--------|
| Exact string match | `grep` | Fast, instant, literal matching |
| Code structure/AST | `ast-grep` | Understands syntax, structural patterns |
| File name patterns | `find`/`Glob` | Fast directory traversal |
| Semantic/concept search | **semtools** | Understands meaning, finds related content |
| Exploring unfamiliar code | **semtools** | Discovers patterns via semantic similarity |
| Multi-format docs | **semtools** | Parses PDFs, DOCX, searches semantically |

## Troubleshooting

### Search Returns No Results

1. **Increase distance threshold:**
   ```bash
   search "query" files/ -i -n 30 -m 0.4  # or 0.5
   ```

2. **Rephrase query** using different terminology

3. **Check file paths** exist and are readable:
   ```bash
   ls docs/  # verify path
   ```

4. **Verify workspace status:**
   ```bash
   workspace status
   ```

### Search is Slow

1. **Use workspace** for repeated searches:
   ```bash
   workspace use project
   export SEMTOOLS_WORKSPACE=project
   ```

2. **Pre-parse PDFs** to avoid parsing repeatedly

3. **Reduce scope** - search specific directories, not entire repo

### Parse Fails

1. **Check API key:**
   ```bash
   echo $LLAMA_CLOUD_API_KEY  # should output your key
   ```

2. **Verify network connection** (LlamaParse requires internet)

3. **Check file format** (PDF, DOCX, PPTX supported)

### Embeddings Seem Stale

```bash
# Remove stale cache entries
workspace prune

# Or create fresh workspace
workspace use new-workspace
export SEMTOOLS_WORKSPACE=new-workspace
```

### Too Many Irrelevant Results

1. **Tighten distance threshold:**
   ```bash
   search "query" files/ -i -n 30 -m 0.2
   ```

2. **Use more specific query terms**

3. **Pre-filter with grep:**
   ```bash
   grep -l "exact_term" *.yaml | xargs search "broader query" -i -n 30 -m 0.3
   ```

## Cost Considerations

Semtools uses LlamaCloud API for:
- Document parsing (PDF, DOCX, etc.)
- Embedding generation for semantic search

**Cost optimization strategies:**
- Use workspaces to cache embeddings (avoids re-embedding)
- Pre-parse documents once, search multiple times
- Parse → cache → search workflow minimizes API calls

**Example costs:**
- 910 ACL research papers analyzed for ~$0.68 (from docs)

## Workspace Management

### Create and Activate Workspace

```bash
workspace use my-project
export SEMTOOLS_WORKSPACE=my-project
```

Add to shell profile for persistence:
```bash
echo 'export SEMTOOLS_WORKSPACE=my-project' >> ~/.zshrc
```

### Check Workspace Status

```bash
workspace status
# Shows: active workspace, cached files, size, last modified
```

### Clean Up Workspace

```bash
# Remove stale/missing files from cache
workspace prune
```

### Workspace Directory

Workspaces stored at: `~/.semtools/workspaces/<workspace-name>/`

## Examples for This Codebase

### Search Architecture Documentation

```bash
search "service mesh design" docs/architecture/ -i -n 40 -m 0.3
```

### Find Crossplane XRD Patterns

```bash
search "composition with managed resources" crossplane/ -i -n 30 -m 0.3
```

### Locate Vault Configuration Examples

```bash
search "vault kubernetes authentication role" apps/ crossplane/ terraform/ \
  -i -n 30 -m 0.3
```

### Search Terraform Modules

```bash
search "authentik group provisioning" terraform/modules/ -i -n 30 -m 0.3
```

### Find ArgoCD Application Patterns

```bash
search "argocd sync waves and hooks" argocd/ -i -n 30 -m 0.3
```

### Explore Helm Values

```bash
search "ingress configuration with TLS" apps/*/values.yaml -i -n 35 -m 0.3
```

### Search Across Documentation Types

```bash
# Search guides, reference docs, and architecture docs
search "secret management patterns" docs/ -i -n 40 -m 0.3
```

## Quick Reference Card

### Essential Pattern

```bash
# Standard search command
search "<query>" <path> -i -n 30 -m 0.3
```

### Create Workspace

```bash
workspace use <name>
export SEMTOOLS_WORKSPACE=<name>
```

### Parse Documents

```bash
parse *.pdf
search "query" ~/.parse/ -i -n 30 -m 0.3
```

### Adjust Precision/Recall

```bash
-m 0.2  # High precision (strict)
-m 0.3  # Balanced (default)
-m 0.4  # High recall (broad)
```

## Resources

For detailed CLI documentation, see `references/cli_reference.md`.

**External resources:**
- GitHub: https://github.com/run-llama/semtools
- Documentation: https://github.com/run-llama/semtools/blob/main/README.md
- Examples: https://github.com/run-llama/semtools/tree/main/examples
