---
name: regulatory-document-parser
description: |
  Parse regulatory document templates (PDF/DOCX) into structured markdown and extract section hierarchies 
  using semtools. Use when tasks involve: analyzing regulatory templates, extracting document structure, 
  parsing ICH/eCTD documents, identifying section hierarchies, preparing documents for content generation,
  or working with bulk PDF/DOCX processing.
  
  Keywords: parse template, extract sections, regulatory document, ICH template, eCTD, document structure,
  section headings, PDF parsing, DOCX parsing, bulk document processing, semtools
---

# Regulatory Document Parser Skill

Specialized capability to parse regulatory documents (PDF, DOCX) using semtools and extract structured 
section hierarchies for pharmaceutical/biotech dossiers.

## When to Use This Skill

Invoke this skill when:
- Analyzing regulatory document templates (ICH modules, eCTD sections)
- Extracting table of contents or section hierarchies
- Parsing PDF/DOCX files to structured markdown
- Identifying numbered sections (1.1, 2.6.2, A.3.1)
- Processing multiple documents in bulk
- Preparing templates for content generation workflows

## Tool Usage Philosophy

**Primary Tool: Semantic Search (`search`)**

Semantic search is your PRIMARY discovery tool:
- Finds relevant content even with different wording
- Discovers sections without knowing exact patterns
- Allows iterative refinement (broad → specific queries)
- Essential for exploring unfamiliar document structures

**Secondary Tool: Exact Matching (`grep`)**

Grep is SECONDARY, used AFTER semantic search:
- Validates findings from search results
- Extracts precise numbering patterns
- Ensures formatting accuracy
- Only use directly if you already know exact patterns

**Recommended Pattern: Search → Grep**

```bash
# Step 1: Semantic discovery (PRIMARY)
search "table of contents sections" ~/.parse/template.md --n-lines 20 --top-k 10
search "module 2 clinical nonclinical" ~/.parse/template.md --n-lines 15 --top-k 15

# Step 2: Exact extraction (SECONDARY)
grep -E '^\s*[0-9]+\.[0-9]+' ~/.parse/template.md

# Step 3: Combine results
# Use search context + grep precision for complete picture
```

**Decision Tree:**
- Need to find sections? → Start with `search`
- Found relevant areas? → Use `grep` to extract exact patterns
- Already know exact format? → Can use `grep` directly (rare)

## Core Commands

### parse - Document to Markdown Conversion

**Syntax:**
```bash
parse "<file-path>"
```

**Behavior:**
- Converts PDF/DOCX to clean markdown
- Output cached at `~/.parse/<filename>.md`
- Handles tables, hierarchies, multi-column layouts
- First parse is slow (1-10s), subsequent access instant

**Examples:**
```bash
# Single file
parse "template_abc/document.pdf"

# Bulk processing
find . -name "*.pdf" | xargs parse
```

### search - Semantic Discovery (PRIMARY TOOL)

**Syntax:**
```bash
search "query" <files> --n-lines N --top-k K --max-distance D
```

**Key Options:**
- `--n-lines N`: Context lines (10-20 recommended)
- `--top-k K`: Number of results (3-15 typical)
- `--max-distance D`: Similarity threshold (0.0=perfect, 0.3=good)

**When to Use:** ALWAYS start with search for section discovery

**Iterative Pattern:**
```bash
# 1. Broad discovery
search "table of contents sections" ~/.parse/template.md --n-lines 20 --top-k 10

# 2. Refine
search "module 2 clinical nonclinical" ~/.parse/template.md --n-lines 15 --top-k 15

# 3. Target specifics
search "pharmacology toxicology" ~/.parse/template.md --n-lines 12 --top-k 10
```

### grep - Exact Pattern Extraction (SECONDARY TOOL)

**When to Use:** AFTER semantic search, to extract precise patterns

**Common Patterns:**
```bash
# Numbered sections
grep -E '^\s*[0-9]+\.[0-9]+' ~/.parse/template.md

# Deep hierarchies
grep -E '^\s*[0-9]+\.[0-9]+\.[0-9]+' ~/.parse/template.md

# ICH modules
grep -E '^Module\s+[0-9]' ~/.parse/template.md
```

### workspace - Performance Optimization

**Commands:**
```bash
export SEMTOOLS_WORKSPACE=dossierflow-templates
workspace use dossierflow-templates  # 10x faster subsequent searches
workspace status                      # Check stats
workspace prune                       # Clean stale files
```

**When to Use:** Repeated searches on same document set



## Section Numbering Patterns

**Common Patterns to Recognize:**

```regex
# Numbered sections: 1.1, 2.5, 3.2.1
^\s*\d+\.\d+

# Deep hierarchies: 2.6.2.4.1
^\s*\d+\.\d+\.\d+\.\d+

# Lettered sections: A.1, B.2.3
^\s*[A-Z]\.\d+

# ICH modules: Module 2.5, 3.2.S.1
^Module\s+\d+|^3\.2\.[SP]
```

## Output Format

For each extracted section, provide structured metadata:

```json
{
  "sections": [
    {
      "title": "2.5 Clinical Overview",
      "summary": "Provides integrated analysis of clinical data including study design, patient populations, efficacy results, and safety profiles. Synthesizes findings across all clinical studies.",
      "originalHeading": "2.5 Clinical Overview"
    },
    {
      "title": "2.6.2 Pharmacodynamics",
      "summary": "Describes pharmacodynamic properties including mechanism of action, dose-response relationships, and therapeutic effects. References nonclinical and clinical PD studies.",
      "originalHeading": "2.6.2 Pharmacodynamics"
    }
  ]
}
```

**Summary Guidelines:**
- 2-3 sentences describing expected section content
- Reference typical evidence requirements (studies, data, analyses)
- Use regulatory terminology (ICH, FDA, EMA)
- Note cross-references to other modules when relevant

## Error Handling

**Parse Failures:**
```bash
ls -la template.pdf        # Verify file exists
find . -name "*.pdf"       # Find available PDFs
ls -la ~/.parse/           # Check cache
```

**Search No Results:**
```bash
cat ~/.parse/template.md | head -100  # Verify parsed
search "section" ~/.parse/template.md --top-k 20 --max-distance 0.5  # Broaden
grep -i "keyword" ~/.parse/template.md  # Fallback to exact match
```

**JSON Validation:**
- All sections must have: `title`, `summary`, `originalHeading`
- No trailing commas, use double quotes
- Preserve section order from template





## Best Practices

1. **Search first, grep second** - Always start with semantic search
2. **Iterate queries** - Broad → specific → targeted
3. **Parse once** - Parsed files cached at `~/.parse/`
4. **Use workspaces** - 10x faster for repeated searches
5. **Validate JSON** - Check structure before returning
6. **Preserve hierarchy** - Maintain exact numbering from template

## Complete Workflow Examples

For detailed end-to-end workflows with real examples, see `semtools-examples.md`:
- Conference paper analysis (900+ PDFs with iterative search)
- Regulatory template processing (search → grep pattern)
- Multi-template comparison
- Workspace optimization strategies

---

**Note:** This Skill synthesizes semtools best practices. See `semtools-examples.md` for complete workflows.
