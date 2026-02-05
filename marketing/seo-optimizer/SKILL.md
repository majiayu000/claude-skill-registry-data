---
name: seo-optimizer
description: Analyze and optimize text for search engines. Execute Python script for detailed SEO analysis. Use when optimizing for keywords, search visibility, or content structure.
---

# SEO Optimizer

I analyze text for search engine optimization and provide actionable recommendations.

## How to Use This Skill

When analyzing SEO performance, execute the SEO optimizer script:

```bash
python /home/ywatanabe/dev/agent-patterns/.claude/skills/seo-optimizer/run.py "text to analyze"
```

The script returns JSON results with keyword analysis, SEO score, and optimization recommendations.

## What I Analyze

### Keyword Optimization
- Primary keyword identification and density
- Secondary keyword usage
- Keyword placement (title, headers, first paragraph)
- Long-tail keyword opportunities
- Keyword stuffing detection

### Content Structure
- Heading hierarchy (H1, H2, H3)
- Paragraph length and scanability
- Use of lists and bullet points
- Internal linking opportunities
- Content length and depth

### On-Page SEO Elements
- Title tag optimization
- Meta description suggestions
- URL structure recommendations
- Image alt text (if applicable)
- Schema markup opportunities

### Content Quality
- Topic coverage and depth
- Search intent alignment
- Unique value proposition
- Content freshness indicators
- E-A-T signals (Expertise, Authoritativeness, Trustworthiness)

## When This Skill Activates

Activate when user requests:
- "Optimize for SEO" or "improve search ranking"
- "Check keywords" or "keyword density"
- "SEO review" or "search optimization"
- "Make this more discoverable"
- Any request about search visibility

## Analysis Process

1. **Identify Target Keywords**: Determine primary/secondary keywords
2. **Analyze Current Optimization**: Assess keyword usage and placement
3. **Evaluate Structure**: Check heading hierarchy and organization
4. **Assess Content Quality**: Evaluate depth, uniqueness, and value
5. **Generate Recommendations**: Provide specific, actionable improvements

## Output Format

Provide structured SEO report:

**Keyword Analysis**:
- Primary keyword: [Identified keyword]
- Keyword density: [X%] ([Too low/Good/Too high])
- Keyword placement: [Assessment]
- Secondary keywords: [List]
- Opportunities: [Suggested keywords]

**Content Structure**:
- Heading hierarchy: [Assessment]
- Content length: [X words] ([Assessment])
- Paragraph structure: [Assessment]
- Scanability: [Good/Needs improvement]

**On-Page SEO**:
- Suggested title tag (50-60 chars)
- Suggested meta description (150-160 chars)
- URL recommendation
- Internal linking opportunities

**Content Quality**:
- Topic depth: [Shallow/Moderate/Comprehensive]
- Search intent: [Informational/Transactional/Navigational]
- Unique value: [Assessment]
- E-A-T signals: [Present/Weak/Missing]

**Recommendations** (prioritized):
1. [High priority item]
2. [Medium priority item]
3. [Low priority item]

## Example Analysis

**Input**: "Machine Learning Guide

Machine learning is cool. It uses computers to learn stuff. There are different types. Supervised learning is one type. Unsupervised is another."

**Output**:
```
Keyword Analysis:
- Primary keyword: "machine learning" (detected)
- Keyword density: 2.8% (Too low for competitive term)
- Keyword placement: ✅ In title, ❌ Not in first paragraph
- Secondary keywords: Missing ("AI", "algorithms", "training data", "neural networks")
- Opportunities: Add "machine learning guide", "ML tutorial", "beginner machine learning"

Content Structure:
- Heading hierarchy: ❌ Missing H2/H3 subheadings
- Content length: 28 words (❌ Far too short - aim for 800+ words)
- Paragraph structure: ❌ Single paragraph, no organization
- Scanability: ❌ Poor - no lists, bullets, or sections

On-Page SEO:
- Title: "Machine Learning Guide" (Too generic)
  Suggested: "Machine Learning for Beginners: Complete Guide 2024"

- Meta description: (Missing)
  Suggested: "Learn machine learning basics with our beginner-friendly guide. Understand supervised vs unsupervised learning, algorithms, and real-world applications."

- URL: Suggest "/machine-learning-guide-beginners"
- Internal links: Add links to related ML topics

Content Quality:
- Topic depth: ❌ Very shallow - needs comprehensive coverage
- Search intent: Informational, but underdeveloped
- Unique value: ❌ Generic information, no unique insights
- E-A-T signals: ❌ Missing (no author credentials, sources, or depth)

High Priority Recommendations:
1. **Expand content to 1000+ words**
   - Add sections: "What is Machine Learning?", "Types of ML", "How It Works", "Applications", "Getting Started"

2. **Improve keyword usage**
   - Use "machine learning" 10-15 times naturally
   - Add related terms: "AI", "algorithms", "training", "models"
   - Include in first paragraph: "Machine learning is a..."

3. **Add proper structure**
   - Create H2 sections for main topics
   - Use H3 for subsections
   - Add bullet points for key concepts
   - Include examples and use cases

4. **Enhance E-A-T**
   - Add author bio with credentials
   - Cite authoritative sources
   - Include case studies or research
   - Add "Last updated: [date]"

5. **Optimize technical elements**
   - Title tag with primary keyword + year
   - Meta description highlighting unique value
   - Add schema markup (Article or HowTo)
```

## Tone

- Strategic and results-focused
- Data-informed recommendations
- Prioritized action items
- Balance SEO with user experience
