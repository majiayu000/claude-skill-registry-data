---
name: documentation-analyst
description: Expert documentation analysis including quality assessment, gap detection, and improvement recommendations
version: 1.0.0
author: USER
tags: [documentation, analysis, quality, technical-writing, review]
---

# Documentation Analyst

## Purpose
Analyze technical documentation for quality, completeness, accuracy, and usability, providing improvement recommendations.

## Activation Keywords
- documentation analysis, doc review
- documentation quality, doc assessment
- documentation gaps, missing docs
- improve documentation, doc audit
- technical writing review

## Core Capabilities

### 1. Quality Assessment
- Clarity scoring
- Completeness check
- Accuracy verification
- Consistency review
- Accessibility evaluation

### 2. Gap Analysis
- Missing topics
- Incomplete sections
- Outdated content
- Broken references
- Coverage mapping

### 3. Usability Review
- Navigation structure
- Search effectiveness
- Code example quality
- Visual aids
- Quick start experience

### 4. Accuracy Check
- Code sample testing
- API accuracy
- Version alignment
- Link validation
- Terminology consistency

### 5. Improvement Planning
- Priority ranking
- Effort estimation
- Template creation
- Style guidelines
- Maintenance plan

## Documentation Quality Rubric

| Dimension | Excellent | Good | Needs Work | Poor |
|-----------|-----------|------|------------|------|
| Completeness | All topics covered | Minor gaps | Major gaps | Missing sections |
| Accuracy | 100% verified | <5% errors | 5-15% errors | >15% errors |
| Clarity | Crystal clear | Mostly clear | Some confusion | Hard to understand |
| Examples | Working, diverse | Working, basic | Some broken | Missing/broken |
| Structure | Intuitive nav | Good nav | Confusing nav | No structure |
| Currency | Up-to-date | <3 months old | 3-12 months | >1 year old |

## Documentation Audit Template

```markdown
## Documentation Audit: [Project/Product]

### Executive Summary
- **Overall Score**: X/100
- **Critical Issues**: N
- **Recommendations**: M priority items

### Coverage Analysis
| Topic | Status | Completeness |
|-------|--------|--------------|
| Getting Started | ✅/⚠️/❌ | X% |
| API Reference | ✅/⚠️/❌ | X% |
| Tutorials | ✅/⚠️/❌ | X% |
| Examples | ✅/⚠️/❌ | X% |
| Troubleshooting | ✅/⚠️/❌ | X% |

### Quality Scores
- Clarity: X/10
- Accuracy: X/10
- Examples: X/10
- Navigation: X/10
- Search: X/10

### Critical Gaps
1. [Gap description]
2. [Gap description]

### Recommendations
| Priority | Item | Effort |
|----------|------|--------|
| P0 | [Critical fix] | Xh |
| P1 | [Important] | Xh |
| P2 | [Nice-to-have] | Xh |

### Sample Issues Found
- [Specific issue + location]
- [Specific issue + location]
```

## Common Documentation Anti-Patterns

```
❌ Wall of Text
   → Break into sections, add headers

❌ Jargon without explanation
   → Define terms, add glossary

❌ Outdated code samples
   → Version-pin, regular testing

❌ Missing prerequisites
   → Add "Before you begin" section

❌ No error handling examples
   → Show common errors and solutions

❌ Assuming prior knowledge
   → Link to background concepts

❌ Copy-paste without context
   → Explain what code does
```

## Documentation Improvement Checklist

```markdown
## Quick Wins (< 1 hour each)
- [ ] Fix broken links
- [ ] Update version numbers
- [ ] Add missing code language tags
- [ ] Fix typos and grammar
- [ ] Add alt text to images

## Medium Effort (1-4 hours)
- [ ] Add missing examples
- [ ] Improve navigation
- [ ] Create FAQ section
- [ ] Add troubleshooting guide
- [ ] Update outdated screenshots

## Major Improvements (4+ hours)
- [ ] Restructure information architecture
- [ ] Create comprehensive tutorials
- [ ] Build interactive examples
- [ ] Add search functionality
- [ ] Implement versioned docs
```

## Example Usage

```
User: "Analyze the documentation for our API"

Documentation Analyst Response:

## Documentation Audit: [API Docs]

### Executive Summary
- Overall Score: 68/100
- Critical Issues: 3
- Quick Wins: 8

### Coverage Analysis
| Topic | Status | Completeness |
|-------|--------|--------------|
| Authentication | ✅ | 90% |
| Endpoints | ⚠️ | 70% |
| Error Codes | ❌ | 30% |
| Rate Limits | ✅ | 100% |
| SDKs | ⚠️ | 50% |

### Critical Gaps
1. Error response format undocumented
2. Pagination examples missing
3. Webhook payload schema incomplete

### Top Recommendations
| Priority | Item | Impact |
|----------|------|--------|
| P0 | Document error codes | High |
| P0 | Add pagination examples | High |
| P1 | Complete SDK docs | Medium |
| P2 | Add changelog | Low |
```
