---
name: tech-trend-researcher
description: This skill should be used when users request research on technical topics, technology trends, industry developments, or any subject requiring web search, source analysis, and structured documentation. It provides a systematic workflow for gathering information from multiple web sources, synthesizing findings into a comprehensive summary, and saving results to a local file.
license: Complete terms in LICENSE.txt
---

# Tech Trend Researcher

This skill provides a systematic workflow for researching technical topics, analyzing trends, and documenting findings in a structured format.

## Purpose

Research technical topics or trends by:
1. Conducting targeted web searches
2. Analyzing multiple authoritative sources
3. Synthesizing information into comprehensive summaries
4. Saving structured documentation to local files

This skill solves the problem of ad-hoc research that lacks structure, often resulting in incomplete coverage or poor documentation quality.

## When to Use This Skill

Use this skill when users request:
- Technology trend analysis (e.g., "Research TypeScript trends")
- Industry developments (e.g., "Latest AI advancements")
- Framework/library updates (e.g., "What's new in React 19")
- Technical topic overviews (e.g., "Kubernetes best practices 2025")
- Comparative analyses (e.g., "Python vs Go for microservices")
- Market research on technical products or tools

Trigger phrases include:
- "Research [topic] and save to file"
- "What are the latest trends in [technology]"
- "Summarize recent developments in [field]"
- "Create a report on [topic]"

## Workflow

Follow this systematic four-phase workflow:

### Phase 1: Initial Web Search

Conduct broad web search to identify key themes and authoritative sources.

**Steps:**
1. Formulate search query targeting latest information (include current/recent year when relevant)
2. Use web_search tool with appropriate max_results (typically 8-12)
3. Scan results to identify:
   - Major themes and trends
   - Authoritative sources (official docs, major tech publications, industry leaders)
   - Specific statistics or data points
   - Key terminology and concepts

**Search Query Guidelines:**
- Include temporal indicators: "2024", "2025", "latest", "recent"
- Add context keywords: "trends", "developments", "updates", "new features"
- Be specific but not overly narrow
- Examples:
  - Good: "TypeScript latest trends 2024 2025"
  - Good: "React 19 new features release"
  - Too narrow: "TypeScript 5.3.2 specific bug fixes"
  - Too broad: "programming languages"

### Phase 2: Deep Source Analysis

Fetch and analyze 2-4 most relevant sources for detailed information.

**Steps:**
1. Select sources based on:
   - Recency (prefer 2024-2025 content)
   - Authority (official docs, major publications, recognized experts)
   - Comprehensiveness (detailed articles over brief mentions)
   - Relevance to user's specific question

2. Use fetch tool to retrieve full content:
   - Set appropriate max_length (6000-10000 for detailed articles)
   - Fetch multiple sources in parallel when possible
   - Prioritize sources that provide different perspectives or complementary information

3. Extract key information:
   - Specific features, versions, or capabilities
   - Statistics, adoption rates, or metrics
   - Expert opinions or industry consensus
   - Code examples or technical details
   - Future roadmap or predictions

### Phase 3: Information Synthesis

Organize and synthesize information into a structured summary.

**Structure Guidelines:**

Always include these core sections:
1. **Header**: Title, date, sources
2. **Overview**: 2-3 paragraph executive summary
3. **Main Trends/Topics**: Numbered sections with clear headings
4. **Key Features/Details**: Bullet points or subsections
5. **Market Context**: Adoption rates, industry impact, statistics
6. **Future Outlook**: Predictions, roadmap, or upcoming changes
7. **Conclusion**: Key takeaways and recommendations
8. **References**: Source links or citations

**Formatting Standards:**
- Use clear hierarchy: Headers (===), subheaders (---), bullet points
- Include specific data: percentages, dates, version numbers
- Provide examples: code snippets, use cases, scenarios
- Add visual separation: line breaks, section dividers
- Use symbols for emphasis: checkmarks, bullets, arrows
- Keep paragraphs concise: 3-5 sentences maximum

**Content Quality Standards:**
- Accuracy: Verify claims across multiple sources
- Completeness: Cover all major themes identified in Phase 1
- Balance: Include both benefits and limitations/challenges
- Specificity: Avoid vague statements; provide concrete details
- Actionability: Include practical implications or recommendations

### Phase 4: File Documentation

Save the synthesized summary to the user's specified file path.

**Steps:**
1. Confirm file path from user request (use absolute paths)
2. Use write_file tool with mode='rewrite'
3. Include the complete structured summary from Phase 3
4. For files over 50 lines, consider chunking (write first chunk, then append)

**File Naming Conventions:**
- Use descriptive names: typescript_trends.txt, react_19_features.md
- Include date if relevant: ai_trends_2025.txt
- Use underscores for spaces: kubernetes_best_practices.txt
- Prefer .txt or .md extensions for readability

## Best Practices

### Search Strategy

- **Cast wide net first**: Initial search should be broad to capture ecosystem
- **Then go deep**: Follow up with targeted searches if gaps remain
- **Multiple queries**: Consider 2-3 different search angles for comprehensive coverage
- **Validate recency**: Prioritize sources from past 6-12 months for trend analysis

### Source Selection

- **Official over community**: Official docs and announcements trump blog posts
- **Data over opinion**: Sources with statistics or benchmarks are more valuable
- **Multiple perspectives**: Do not rely on single source; cross-reference
- **Original over secondary**: Link to primary sources when available

### Synthesis Quality

- **Structure matters**: Well-organized content is more valuable than comprehensive but chaotic information
- **Context is key**: Explain why trends matter, not just what they are
- **Be critical**: Note limitations, controversies, or competing viewpoints
- **Stay objective**: Present balanced view even if sources are biased

### Common Pitfalls to Avoid

- **Over-reliance on first search**: Do not stop after initial search if coverage is incomplete
- **Ignoring dates**: Outdated information can mislead users about current trends
- **Too much detail**: Focus on signal over noise; summarize rather than transcribe
- **Poor structure**: Wall of text reduces value; use hierarchy and formatting
- **Missing context**: Statistics without context are meaningless
- **No conclusion**: Always provide synthesis and takeaways

## Output Quality Checklist

Before saving the file, verify:
- All major themes from initial search are covered
- At least 2-3 authoritative sources are cited
- Specific data points (dates, versions, percentages) are included
- Structure follows standard format with clear sections
- Content is well-formatted with headers and bullets
- Conclusion provides actionable insights
- File path is correct and absolute
- No placeholder text or TODOs remain

## Examples

### Example 1: Technology Trend Research
**User Request**: "Research TypeScript trends and save to /Users/user/Desktop/typescript_trends.txt"

**Workflow Execution**:
1. Search: "TypeScript latest trends 2024 2025" with 10 results
2. Fetch: 2 detailed articles from authoritative sources
3. Synthesize: 10-section structured summary covering adoption rates, new features, ecosystem changes
4. Save: Complete formatted document to specified path

**Key Success Factors**:
- Included specific statistics (12% to 35% adoption growth)
- Covered multiple dimensions (features, tooling, ecosystem)
- Provided actionable conclusion
- Well-structured with clear hierarchy

### Example 2: Framework Update Research
**User Request**: "What's new in React 19? Save summary to ~/Documents/react19.md"

**Workflow Execution**:
1. Search: "React 19 new features release 2024"
2. Fetch: Official React blog post plus community analysis
3. Synthesize: Feature-by-feature breakdown with code examples
4. Save: Markdown format with syntax highlighting

### Example 3: Comparative Analysis
**User Request**: "Compare Rust vs Go for web services and document findings"

**Workflow Execution**:
1. Search: "Rust vs Go web services 2024 comparison"
2. Fetch: Multiple benchmark articles and developer surveys
3. Synthesize: Side-by-side comparison with use case recommendations
4. Save: Structured comparison table with detailed sections

## Adaptation for Different Domains

This workflow can be adapted for non-technical research:

**Business/Market Research**:
- Search industry reports and market analyses
- Focus on market size, growth rates, key players
- Include competitive landscape and trends

**Policy/Regulatory Research**:
- Search official government or regulatory sources
- Focus on timeline, requirements, implications
- Include compliance considerations

**Scientific/Academic Research**:
- Search academic publications and research papers
- Focus on methodologies, findings, citations
- Include limitations and future research directions

## Notes

- **Objectivity**: Present balanced view; avoid promotional language
- **Timeliness**: Always check publication dates; trends evolve quickly
- **User's Language**: If user requests in non-English, consider translating summary
- **File Permissions**: Verify user has write access to specified path
- **Follow-up**: If user requests clarification, be prepared to expand specific sections
