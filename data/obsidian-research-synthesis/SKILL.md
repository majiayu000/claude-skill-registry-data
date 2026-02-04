---
name: obsidian-research-synthesis
description: Searches across Obsidian vault, synthesizes findings from multiple notes, and creates comprehensive research documentation. Gathers scattered information using filesystem search and dataview queries, analyzes content, and produces structured research reports with proper citations and wiki-links.
---

# Research & Synthesis

Enables comprehensive research workflows within Obsidian: search for information across your vault, analyze and synthesize findings from multiple notes, and create well-structured research documentation with proper citations.

## Quick Start

When asked to research and document a topic:

1. **Search vault**: Use filesystem search, grep, and dataview to find relevant notes
2. **Read notes**: Parse markdown files and extract relevant information
3. **Synthesize findings**: Analyze and combine information from multiple sources
4. **Create research note**: Generate structured documentation with citations

## Research Workflow

### Step 1: Search for relevant information

**Filesystem search:**
```bash
# Search by filename
find /path/to/vault -name "*keyword*"

# Search file content
grep -r "search term" /path/to/vault/ --include="*.md"

# Search with context
grep -r -C 3 "search term" /path/to/vault/

# Case-insensitive search
grep -ri "keyword" /path/to/vault/
```

**Search by frontmatter:**
```bash
# Find notes with specific tag
grep -l "tags:.*keyword" /path/to/vault/**/*.md

# Find notes of specific type
grep -l "type: research" /path/to/vault/**/*.md
```

**Dataview queries** (if using Dataview plugin):
```dataview
TABLE file.ctime, tags
FROM "research" OR "projects"
WHERE contains(file.name, "keyword")
   OR contains(tags, "#topic")
SORT file.mtime DESC
```

**Search strategies:**
- Topic-based: Search for concept or domain keywords
- Tag-based: Filter by relevant tags
- Date-based: Recent notes using mtime
- Author-based: Notes created by specific person
- Link-based: Notes linking to specific concept

### Step 2: Read and extract information

For each relevant note:

```bash
# Read full note
cat /path/to/vault/note-name.md

# Read just frontmatter
head -20 /path/to/vault/note-name.md | sed -n '/^---$/,/^---$/p'

# Extract specific sections
sed -n '/## Section Name/,/^## /p' /path/to/vault/note-name.md
```

Extract and organize:
- Key concepts and definitions
- Data points and metrics
- Insights and analysis
- Quotes and specific claims
- Relationships between concepts
- Gaps in knowledge

### Step 3: Analyze and synthesize

**Identify patterns:**
- Common themes across notes
- Contradictions or conflicts
- Knowledge gaps
- Complementary information
- Chronological developments

**Connect concepts:**
- How topics relate to each other
- Dependencies and prerequisites
- Cause and effect relationships
- Examples and counter-examples

**Note limitations:**
- Missing information
- Uncertain claims
- Areas needing more research
- Conflicting viewpoints

### Step 4: Create research documentation

**Choose output format:**

- **Research Summary**: Quick overview with key findings (see [reference/research-summary-template.md](reference/research-summary-template.md))
- **Comprehensive Report**: Detailed analysis with full citations (see [reference/comprehensive-report-template.md](reference/comprehensive-report-template.md))
- **Literature Review**: Academic-style review (see [reference/literature-review-template.md](reference/literature-review-template.md))
- **Synthesis Note**: Integration of multiple sources (see [reference/synthesis-note-template.md](reference/synthesis-note-template.md))

**Create research note:**
```bash
touch /path/to/vault/research/topic-research.md
```

See [reference/format-selection-guide.md](reference/format-selection-guide.md) for choosing the right format.

## Research Output Formats

### Research Summary

Brief overview synthesizing key findings:

```markdown
---
type: research-summary
topic: [Topic]
created: YYYY-MM-DD
tags:
  - research
  - TOPIC
sources: X notes
---

# Research Summary: [Topic]

## Executive Summary
One paragraph capturing the main findings.

## Key Findings
1. Finding 1 [[source-note-1]]
2. Finding 2 [[source-note-2]]
3. Finding 3 [[source-note-3]]

## Main Themes
- Theme 1: Description
- Theme 2: Description

## Conclusions
Summary of insights and implications.

## Further Research
- Question 1
- Question 2

## Sources
- [[note-1]]
- [[note-2]]
- [[note-3]]
```

### Comprehensive Report

Detailed analysis with full exploration:

```markdown
---
type: research-report
topic: [Topic]
created: YYYY-MM-DD
tags:
  - research
  - report
  - TOPIC
---

# Research Report: [Topic]

## Executive Summary
Comprehensive overview of research and conclusions.

## Background
Context and motivation for research.

## Methodology
How information was gathered and analyzed.

## Findings

### Theme 1: [Name]
Detailed discussion with evidence.

**Evidence from sources:**
- [[source-1]]: Specific claim or data
- [[source-2]]: Supporting information
- [[source-3]]: Additional context

### Theme 2: [Name]
Continue analysis...

## Analysis
Synthesis and interpretation of findings.

## Limitations
Gaps in current research and uncertainties.

## Conclusions
Key takeaways and implications.

## Recommendations
Actionable suggestions based on research.

## Further Research
Areas needing additional investigation.

## References
Complete list of source notes with brief descriptions.
```

See [reference/comprehensive-report-template.md](reference/comprehensive-report-template.md) for full template.

## Citation Patterns

### Basic Citation
```markdown
According to [[note-name]], the primary factor is X.
```

### Citation with Context
```markdown
The implementation pattern [[patterns/circuit-breaker]] suggests using exponential backoff.
```

### Multiple Sources
```markdown
Multiple sources ([[source-1]], [[source-2]], [[source-3]]) indicate that X is common.
```

### Direct Quote Attribution
```markdown
> "Key insight here"
> — [[person-name]] in [[meeting-notes-2025-10-15]]
```

### Conflicting Sources
```markdown
While [[source-1]] suggests X, [[source-2]] presents evidence for Y, indicating further investigation is needed.
```

## Search Techniques

### Content-Based Search

**Exact phrase:**
```bash
grep -r "exact phrase here" /path/to/vault/
```

**Multiple keywords:**
```bash
grep -r "keyword1" /path/to/vault/ | grep "keyword2"
```

**Exclude certain directories:**
```bash
grep -r "keyword" /path/to/vault/ --exclude-dir=".obsidian"
```

### Metadata-Based Search

**Find by tag:**
```bash
grep -l "tags:.*#specific-tag" /path/to/vault/**/*.md
```

**Find by type:**
```bash
grep -l "type: research" /path/to/vault/**/*.md
```

**Find by date range:**
```bash
find /path/to/vault -name "*.md" -newermt "2025-01-01" -not -newermt "2025-12-31"
```

### Link-Based Analysis

**Find all notes linking to specific note:**
```bash
grep -r "\[\[target-note\]\]" /path/to/vault/
```

**Find orphan notes (no incoming links):**
```bash
# Requires custom script
python scripts/find_orphans.py /path/to/vault
```

**Find highly connected notes:**
```bash
# Count outgoing links per note
for file in /path/to/vault/**/*.md; do
  count=$(grep -o "\[\[" "$file" | wc -l)
  echo "$count $file"
done | sort -rn | head -10
```

## Synthesis Strategies

### Thematic Synthesis
Group findings by common themes across sources.

### Chronological Synthesis
Trace development of ideas over time.

### Comparative Synthesis
Compare and contrast different perspectives.

### Integrative Synthesis
Build unified understanding from diverse sources.

## Quality Checks

Before finalizing research:

- [ ] All claims cited to source notes
- [ ] Contradictions noted and explained
- [ ] Knowledge gaps identified
- [ ] Key themes clearly articulated
- [ ] Executive summary captures essence
- [ ] Recommendations are actionable
- [ ] Further research questions listed
- [ ] All source links valid

## Best Practices

1. **Search broadly first**: Cast wide net initially
2. **Read critically**: Evaluate quality and relevance of sources
3. **Take structured notes**: Extract key points during reading
4. **Cite consistently**: Always link to source notes
5. **Note conflicts**: Document disagreements between sources
6. **Identify gaps**: What's missing from current knowledge
7. **Synthesize, don't summarize**: Create new understanding
8. **Write for audience**: Tailor depth and tone appropriately

## Advanced Techniques

### Network Analysis
Examine connection patterns between notes to identify central concepts and knowledge clusters.

### Temporal Analysis
Track how understanding of topic evolved over time based on note creation/modification dates.

### Gap Analysis
Systematically identify what's not documented in vault.

### Source Quality Assessment
Evaluate reliability and depth of different source notes.

## Dataview Research Queries

**Find all research on topic:**
```dataview
LIST
FROM #research
WHERE contains(file.name, "topic")
   OR contains(tags, "#specific-tag")
SORT file.mtime DESC
```

**Research by recency:**
```dataview
TABLE file.ctime as "Created", tags
FROM "research"
SORT file.ctime DESC
LIMIT 20
```

**Find related research:**
```dataview
TABLE file.outlinks as "References"
FROM "research"
WHERE file.name = this.file.name
FLATTEN file.outlinks
```

## Common Issues

**"Too many results"**: 
- Add more specific keywords
- Filter by date range
- Search within specific folders
- Use tag combinations

**"Results not relevant"**:
- Try different search terms
- Check synonyms and related concepts
- Search by links rather than content

**"Missing key information"**:
- Note gaps in research note
- Create follow-up research tasks
- Ask for clarification from original authors

**"Conflicting information"**:
- Document both perspectives
- Note level of confidence
- Suggest resolution approach

## Scripts

`scripts/vault_search.py`: Advanced vault searching
`scripts/extract_citations.py`: Extract all citations from note
`scripts/validate_links.py`: Check for broken links
`scripts/find_related.py`: Find notes related to topic
`scripts/generate_bibliography.py`: Create formatted source list

## Examples

See [examples/](examples/) for complete workflows:
- [examples/topic-research.md](examples/topic-research.md) - Comprehensive topic research
- [examples/quick-synthesis.md](examples/quick-synthesis.md) - Rapid synthesis
- [examples/literature-review.md](examples/literature-review.md) - Academic-style review
