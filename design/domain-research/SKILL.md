---
name: domain-research
description: MCP-powered domain research for requirements elicitation. Uses perplexity, context7, firecrawl, and other MCP servers to research domain knowledge, best practices, and industry requirements.
allowed-tools: Read, Glob, Grep, Write, mcp__perplexity__search, mcp__perplexity__reason, mcp__context7__resolve-library-id, mcp__context7__query-docs, mcp__firecrawl__firecrawl_search, mcp__firecrawl__firecrawl_scrape
---

# Domain Research Skill

MCP-powered domain research for enriching requirements elicitation with external knowledge.

## MANDATORY: Documentation-First Approach

Before conducting domain research:

1. **Invoke `docs-management` skill** for requirements elicitation patterns
2. **Use MCP servers as primary research tools** (perplexity, context7, firecrawl)
3. **Base all guidance on official documentation and authoritative sources**

## When to Use This Skill

**Keywords:** domain research, MCP research, industry standards, best practices, competitive analysis, technology research, regulatory requirements

Invoke this skill when:

- Unfamiliar with a domain and need background
- Researching industry standards and best practices
- Investigating regulatory requirements
- Analyzing competitor features
- Exploring technology constraints
- Supplementing stakeholder knowledge

## Available MCP Servers

### Perplexity (General Research)

**Use for:**

- Industry best practices
- Recent developments
- Comparative analysis
- Regulatory overviews

```yaml
mcp_tool: mcp__perplexity__search
example_queries:
  - "e-commerce checkout best practices 2025"
  - "GDPR compliance requirements for SaaS"
  - "authentication patterns for financial applications"
```

### Context7 (Library Documentation)

**Use for:**

- Framework requirements
- API constraints
- Library capabilities
- Technical limitations

```yaml
mcp_tools:
  - mcp__context7__resolve-library-id
  - mcp__context7__query-docs
example_queries:
  - Library: "react" → Query: "state management patterns"
  - Library: "fastapi" → Query: "authentication requirements"
```

### Firecrawl (Web Scraping)

**Use for:**

- Competitor analysis
- Documentation extraction
- Feature comparison
- Market research

```yaml
mcp_tools:
  - mcp__firecrawl__firecrawl_search
  - mcp__firecrawl__firecrawl_scrape
example_queries:
  - Search: "inventory management software features"
  - Scrape: Competitor feature pages
```

## Research Patterns

### Pattern 1: Domain Background

Build foundational domain knowledge:

```yaml
research_pattern: domain_background
steps:
  1. Use perplexity for industry overview
  2. Identify key concepts and terminology
  3. Research common requirements in domain
  4. Note regulatory considerations
output: Domain context document
```

### Pattern 2: Best Practices

Research current best practices:

```yaml
research_pattern: best_practices
steps:
  1. Search for "best practices" in domain
  2. Filter for recent (last 2 years)
  3. Identify common patterns
  4. Note recommended approaches
output: Best practices summary
```

### Pattern 3: Competitive Analysis

Research competitor features:

```yaml
research_pattern: competitive_analysis
steps:
  1. Identify key competitors
  2. Scrape feature pages with firecrawl
  3. Extract capability lists
  4. Compare and contrast
output: Competitive feature matrix
```

### Pattern 4: Regulatory Research

Research compliance requirements:

```yaml
research_pattern: regulatory
steps:
  1. Identify applicable regulations
  2. Research specific requirements
  3. Note mandatory vs recommended
  4. Document compliance criteria
output: Regulatory requirements list
```

### Pattern 5: Technology Constraints

Research technical requirements:

```yaml
research_pattern: technology
steps:
  1. Identify technologies in scope
  2. Use context7 for library docs
  3. Research integration requirements
  4. Document technical constraints
output: Technical requirements document
```

## Research Workflow

### Step 1: Define Research Scope

```yaml
research_scope:
  domain: "{domain name}"
  topic: "{specific focus area}"
  depth: shallow|moderate|deep
  sources: [perplexity, context7, firecrawl]
```

### Step 2: Execute Research Queries

For each research need:

1. Select appropriate MCP server
2. Formulate effective query
3. Process results
4. Extract requirements

### Step 3: Synthesize Findings

Combine research into actionable requirements:

- Identify common patterns
- Note conflicts or options
- Highlight mandatory items
- Suggest priorities

### Step 4: Document Results

Save research findings and derived requirements.

## Output Format

### Research Results

```yaml
research_session:
  id: "RES-{timestamp}"
  domain: "{domain}"
  topic: "{research topic}"
  timestamp: "{ISO-8601}"

  queries_executed:
    - server: perplexity
      query: "{query text}"
      results_count: {number}

    - server: firecrawl
      url: "{scraped URL}"
      content_type: feature_page

  findings:
    domain_context:
      - "{key finding 1}"
      - "{key finding 2}"

    best_practices:
      - "{recommended practice 1}"
      - "{recommended practice 2}"

    regulatory:
      - regulation: "GDPR"
        requirements:
          - "{requirement 1}"
          - "{requirement 2}"

    competitive:
      - competitor: "{name}"
        features:
          - "{feature 1}"
          - "{feature 2}"

  derived_requirements:
    - id: REQ-RES-001
      text: "{requirement statement}"
      source: research
      source_detail: "{where this came from}"
      confidence: low  # Research-derived = low confidence
      needs_validation: true
      category: "{category}"

  recommendations:
    - topic: "{topic}"
      finding: "{what research showed}"
      implication: "{what this means for requirements}"

  gaps_in_research:
    - "{area where more research needed}"
```

## Query Optimization

### Effective Perplexity Queries

```yaml
query_patterns:
  best_practices:
    template: "{domain} {topic} best practices {year}"
    example: "e-commerce checkout best practices 2025"

  requirements:
    template: "{domain} {topic} requirements specifications"
    example: "healthcare application HIPAA requirements"

  comparison:
    template: "{topic A} vs {topic B} for {use case}"
    example: "OAuth 2.0 vs SAML for enterprise SSO"

  regulatory:
    template: "{regulation} requirements for {industry}"
    example: "PCI-DSS requirements for payment processing"
```

### Effective Context7 Queries

```yaml
query_patterns:
  library_features:
    resolve: "{library name}"
    get_docs: topic="{specific feature}"

  integration:
    resolve: "{library name}"
    get_docs: topic="integration authentication"
```

### Effective Firecrawl Queries

```yaml
query_patterns:
  competitor_features:
    search: "{competitor} features {product type}"
    scrape: Feature page URLs

  documentation:
    search: "{technology} documentation requirements"
    scrape: Official docs
```

## Confidence Levels

Research-derived requirements have inherent confidence limits:

```yaml
confidence_levels:
  high:
    sources: [official documentation, regulatory text]
    note: "Verified from authoritative source"

  medium:
    sources: [industry articles, best practice guides]
    note: "Generally accepted but verify with stakeholders"

  low:
    sources: [competitor analysis, general web]
    note: "Use as starting point, requires validation"
```

## Delegation

For follow-up actions:

- **interview-conducting**: Validate research with stakeholders
- **gap-analysis**: Check research fills identified gaps
- **elicitation-methodology**: Return for technique selection

## Output Location

Save research results to:

```text
.requirements/{domain}/research/RES-{timestamp}.yaml
```

## Related

- `elicitation-methodology` - Parent hub skill
- `gap-analysis` - Research to fill gaps
- `interview-conducting` - Validate research findings

---

**Last Updated:** 2025-12-29
