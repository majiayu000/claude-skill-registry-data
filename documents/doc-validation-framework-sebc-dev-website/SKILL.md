---
name: doc-validation-framework
description: >
  Expert methodology for systematically validating the quality, accuracy, and freshness of any
  technical document. Use when user requests document validation, checklist generation, documentation
  quality assurance, or needs to verify claims in technical documentation. Generates comprehensive
  validation checklists with 80-150 items organized by domain and criticality.
version: '1.0'
tags:
  - documentation
  - validation
  - qa
  - checklists
---

# Document Validation Framework - Expert Methodology

## Overview

This skill encapsulates a comprehensive, systematic methodology for validating technical documentation. It enables the generation of detailed validation checklists that can be used by AI agents (Gemini, ChatGPT) to perform automated research and produce validation reports.

## Four Fundamental Principles

### 1. Hierarchical Exhaustiveness

Structure validation by **depth levels**:

- **Level 1**: General concepts & architecture
- **Level 2**: Components & specific technologies
- **Level 3**: Versions, configurations, edge cases

### 2. Source Traceability

Every claim must point to:

- Official documentation
- GitHub repositories
- Official blog posts / announcements
- Community resources (with caution)

### 3. Freshness Detection

Identify information prone to obsolescence:

- Software versions
- APIs & patterns
- Breaking changes
- Recommendations & best practices

### 4. Bidirectional Validation

- **Positive**: Verify that X is supported/recommended
- **Negative**: Verify that Y is obsolete/deprecated

## Eight Property Types

When analyzing documents, extract properties falling into these 8 categories:

### Type 1: Version

Claims about specific versions of technologies

- **Example**: "Next.js 15.0+"
- **Questions**: Is this version current? Has a newer version been released?

### Type 2: Availability/Status

Claims about feature availability (GA, Beta, Alpha)

- **Example**: "Feature is Generally Available"
- **Questions**: What's the current status? Any breaking changes?

### Type 3: Support/Compatibility

Claims about what components support what

- **Example**: "Next.js supports WebAssembly"
- **Questions**: Is this still supported? Any limitations?

### Type 4: Recommendations/Best Practices

Claims about what is recommended

- **Example**: "Server Components are the recommended approach"
- **Questions**: Is this still best practice? Any caveats?

### Type 5: Deprecation/Obsolescence

Claims about deprecated or outdated approaches

- **Example**: "Class components are being phased out"
- **Questions**: When will they be removed? Migration path?

### Type 6: Limitations/Constraints

Claims about limits or constraints

- **Example**: "Maximum 2MB bundle size"
- **Questions**: What are the exact current limits?

### Type 7: Patterns/Approaches

Claims about architectural patterns

- **Example**: "Server-first rendering approach"
- **Questions**: Is this pattern still recommended? Alternatives?

### Type 8: Integration/Chains

Claims about multi-component interactions

- **Example**: "Next.js → Cloudflare Workers → D1 Database"
- **Questions**: Does this integration still work? Are there breaking changes?

## Three Criticality Levels

When extracting properties, assign criticality:

### Fundamental (15-20% of items)

Core architecture that affects everything

- Framework choice (Next.js, React, etc.)
- Database strategy
- Authentication approach
- Deployment platform

### Major (30-40% of items)

Important components with significant impact

- Specific libraries/ORM choices
- Styling approach
- Testing framework
- CI/CD pipeline

### Secondary (40-55% of items)

Optimizations and nice-to-haves

- Performance tuning
- Optional libraries
- Development tools
- Optional integrations

## Standard Domains

Technical architecture documents typically contain these 12 domains:

1. **Framework & Runtime**: Framework versions, runtimes, adapters
2. **Database & ORM**: Database choices, ORM libraries, migrations
3. **Storage & Media**: File storage, CDN, image handling
4. **Authentication & Security**: Auth methods, security practices
5. **Internationalization**: i18n library, localization strategy
6. **Content & Rendering**: Rendering strategies, content sources
7. **UI & Styling**: CSS approach, component libraries
8. **Testing**: Test frameworks, testing strategy
9. **Deployment & CI/CD**: Deployment platforms, CI/CD tools
10. **Infrastructure & Monitoring**: Hosting, monitoring, logging
11. **Performance & Web Vitals**: Performance targets, optimization
12. **Architecture Patterns**: Design patterns, architectural decisions

## Validation Checklist Structure

A generated validation checklist should include:

### 1. Quick Reference Table

Summary of criticality distribution

```
| Criticality | Count | % |
|---|---|---|
| Fundamental | 23 | 18% |
| Major | 45 | 35% |
| Secondary | 59 | 47% |
| **Total** | **127** | **100%** |
```

### 2. Domain-Organized Checklist

For each domain, list validation items with:

- [ ] Checkbox for completion
- Clear, specific question
- Domain tag
- Criticality level

Example:

```markdown
### Framework & Runtime (15 items)

- [ ] **Fundamental**: Is Next.js version 15.0+ confirmed as current? Check official Next.js releases
- [ ] **Fundamental**: Are React Server Components the recommended approach in 2024/2025?
- [ ] **Major**: Is the OpenNext adapter still actively maintained?
```

### 3. Research Sources Section

List all 15-30 external sources with:

- Technology name
- Type (official docs, GitHub, blog)
- URL
- Verification status

Example:

```markdown
## Research Sources

### Next.js

- **Official Docs**: https://nextjs.org/docs
- **GitHub**: https://github.com/vercel/next.js
- **Blog**: https://vercel.com/blog

### Cloudflare Workers

- **Official Docs**: https://developers.cloudflare.com/workers/
- **Status Page**: https://www.cloudflarestatus.com/
```

### 4. Notes Section

Space for documenting findings, conflicts, and resolution notes

## Documentation Analysis Process

### Step 1: Document Scanning (5-10 min)

- Read through entire document
- Extract 30-50 technical concepts
- Identify mention locations
- Initial categorization

### Step 2: Property Extraction (20-30 min)

- For each concept, identify 2-3 factual properties
- Classify into one of 8 property types
- Assign to appropriate domain
- Estimate criticality level
- Total: 80-150 properties

### Step 3: Question Generation (10-15 min)

- Convert each property to a specific validation question
- Frame questions to be researchable
- Ensure questions are actionable
- Add source hints when relevant

### Step 4: Checklist Organization (5-10 min)

- Group by domain
- Sort by criticality within domain
- Create Quick Reference table
- Compile Research Sources list
- Add standard sections

## Usage Instructions

When generating a validation checklist for a document:

1. **Read the full document** to understand context
2. **Extract all technical concepts** mentioned
3. **Classify each concept** into appropriate domain(s)
4. **Identify factual properties** for each concept
5. **Assign criticality** based on architectural impact
6. **Generate validation questions** that are specific and researchable
7. **Organize** by domain and criticality
8. **Create Quick Reference** table with statistics
9. **List all sources** that could validate the claims
10. **Export as Markdown** ready for external agents

## Expected Output Characteristics

A well-generated checklist should have:

- ✅ 80-150 validation items (minimum for meaningful validation)
- ✅ Organized into 8-15 domains
- ✅ Distributed across three criticality levels
- ✅ 15-30 research sources identified
- ✅ Clear, specific validation questions
- ✅ Exportable in plain Markdown format
- ✅ No tool-specific proprietary formats
- ✅ Ready for use by any external AI agent

## Integration with Claude Code

This skill is designed to work within Claude Code's architecture:

- **Autonomously invoked** when document validation is requested
- **Works with Subagent** `checklist-generator` for complex analysis
- **Triggered by Command** `/generate-checklist` for user control
- **Produces exportable Markdown** for downstream agents
- **Reusable** across any technical document type

## Next Steps

After generating a validation checklist:

1. **Export the Markdown** to a file
2. **Share with external agents** (Gemini, ChatGPT)
3. **Let external agents** research items and collect findings
4. **Review and consolidate** findings into validation report
5. **Update documentation** based on findings
6. **Re-validate** updated documentation
