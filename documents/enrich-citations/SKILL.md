---
name: enrich-citations
description: Find and add authoritative source links for all facts, citations, and references in markdown documents
---

# Enrich Citations

This skill enhances markdown documents by finding and adding authoritative source links for all mentioned facts, citations, tools, products, research, and references.

## Key Principles

- **Find authoritative sources**: Search for the original, most credible source for each reference
- **Verify accuracy**: Ensure links point to the correct, current information
- **Preserve content**: Only add hyperlinks, don't change the document's text or meaning
- **Proper formatting**: Use markdown hyperlink syntax with spaces for proper rendering

## When to Use This Skill

Use this skill when the user asks to:
- Add citations to a document
- Find sources for mentioned references
- Add hyperlinks to external resources
- Verify and link fact sources
- Enrich a document with authoritative links

## Processing Instructions

### Step 1: Identify References

Read through the entire markdown document and identify all mentions of:

1. **External sources and research**:
   - Academic papers, studies, reports
   - Books, articles, blog posts
   - Research findings or statistics

2. **Tools and software**:
   - Applications, frameworks, libraries
   - Programming languages, platforms
   - Development tools, services

3. **Products and services**:
   - Commercial products
   - SaaS platforms
   - Hardware or software products

4. **Organizations and institutions**:
   - Companies, universities
   - Standards bodies, foundations
   - Government agencies

5. **Technical concepts and standards**:
   - Specifications (RFC, W3C, etc.)
   - APIs, protocols
   - Industry standards

6. **People and experts**:
   - Authors, researchers
   - Industry leaders
   - Subject matter experts

### Step 2: Web Search for Sources

For **each identified reference**:

1. **Search for the authoritative source**:
   - Use web search to find the official or most credible source
   - Prioritize: official websites > documentation > reputable publications
   - For academic references: search for DOI, arXiv, official publication

2. **Verify the source**:
   - Ensure the URL is current and accessible
   - Check that content matches the reference
   - Confirm it's the most authoritative source available

3. **Select the best link**:
   - Official documentation or homepage for tools/products
   - Original publication for research/articles
   - Wikipedia for general concepts (if no better source exists)
   - GitHub repository for open source projects

### Step 3: Add Hyperlinks

Replace plain text references with markdown hyperlinks:

**Format:** `[Reference Text](URL)`

**Critical formatting requirements:**
- **Add spaces around hyperlinks**: `text [link](url) text` (not `text[link](url)text`)
- Use descriptive link text (the actual reference name, not "click here")
- Maintain the original sentence structure
- Preserve all other content unchanged

**Examples:**

Before:
```
According to the 2023 Stack Overflow Survey, JavaScript is the most popular language.
```

After:
```
According to the [2023 Stack Overflow Survey](https://survey.stackoverflow.co/2023/) , JavaScript is the most popular language.
```

Before (Chinese):
```
文章提到了GPT-4的能力提升
```

After (Chinese):
```
文章提到了 [GPT-4](https://openai.com/gpt-4) 的能力提升
```

### Step 4: Quality Assurance

Before finalizing:

1. **Verify all links**:
   - Test that URLs are valid and accessible
   - Check for broken links or redirects
   - Ensure HTTPS when available

2. **Check formatting**:
   - Confirm spaces around hyperlinks
   - Verify markdown syntax is correct
   - Ensure links render properly

3. **Review accuracy**:
   - Links point to correct resources
   - No duplicate or conflicting sources
   - All identified references are addressed

## Important Constraints

- **NEVER change the document content**: Only add hyperlinks to existing text
- **NEVER add new information**: Don't insert citations not mentioned in the original
- **NEVER remove existing content**: Preserve all original text
- **NEVER summarize or paraphrase**: Keep exact wording
- **DO add spaces around hyperlinks**: Essential for proper rendering
- **DO verify all sources**: Ensure accuracy and accessibility

## Output Format

Return the enhanced markdown document with:
- All appropriate references converted to hyperlinks
- Proper spacing around all links
- Original content and structure preserved
- All links verified and working

## Source Priority Guidelines

When multiple sources exist, prioritize in this order:

1. **Official sources**: Project homepages, official documentation
2. **Primary sources**: Original research papers, first publications
3. **Authoritative organizations**: Standards bodies, academic institutions
4. **Reputable publications**: Well-known tech blogs, news sites
5. **Community resources**: GitHub, Stack Overflow (for code/tools)
6. **General references**: Wikipedia, encyclopedias (as last resort)

## Language Support

This skill works with documents in any language:
- Respect the document's primary language
- Use appropriate sources for the language/region
- Maintain original text while adding hyperlinks
- For multilingual documents, find sources matching each language section when appropriate