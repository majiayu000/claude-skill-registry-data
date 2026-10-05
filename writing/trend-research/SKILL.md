---
name: trend-research
description: Research any topic across Reddit, X (Twitter), and the web to identify recent trends (last 30 days) and generate production-ready prompts or recommendations
---

# Trend Research & Prompt Generation

This skill enables you to research any topic to find the latest trends, best practices, and community consensus from the last 30 days, and then turn that research into high-quality, copy-paste-ready prompts or recommendations.

## 1. Parse User Intent
Before researching, identify these three variables from the user's request:
1.  **TOPIC**: What they want to learn about (e.g., "Claude Code workflows", "shadcn/ui templates").
2.  **TARGET_TOOL** (Optional): Where they will use the output (e.g., "Cursor", "Midjourney", "ChatGPT").
3.  **QUERY_TYPE**:
    *   **PROMPTING**: "prompts for X", "how to prompt X" (Goal: Create a prompt)
    *   **RECOMMENDATIONS**: "best X", "top tools for Y" (Goal: List of items)
    *   **NEWS**: "latest on X", "what's new with Y" (Goal: Summary of events)
    *   **GENERAL**: Everything else (Goal: Broad understanding)

## 2. Execute Research (Native)
Perform a targeted search using your `Search` tool. Do NOT use Python scripts or external APIs. Use your internal browsing capabilities.

### Search Strategy
Run these specific search queries in order:

**Query 1: Community Discussions (Reddit/Forums)**
*   Search for: `site:reddit.com "{TOPIC}" after:2025-12-01` (Adjust date to ~30 days ago)
*   *Goal*: Find what real users are discussing, debating, and upvoting.

**Query 2: Current Trends (General Web)**
*   Search for: `"{TOPIC}" latest trends 2026` OR `"{TOPIC}" best practices 2026`
*   *Goal*: Find articles, blog posts, and news from the last month.

**Query 3: Prompt Specifics (If QUERY_TYPE is PROMPTING)**
*   Search for: `"{TOPIC}" prompt examples` OR `"{TOPIC}" system prompt template`
*   *Goal*: Find the specific JSON/XML/Markdown formats that work best for this topic.

## 3. Synthesize Findings (The Judge Agent)
Analyze the search results. apply these "Judge" rules:
1.  **Weight Community Higher**: Trust repeated mentions in Reddit threads/X posts over generic SEO blog posts.
2.  **Look for Formats**: If multiple sources say "Use JSON for this tool" or "Include rigid constraints", NOTE THAT. This is critical for the final output.
3.  **Identify Consensus**: What are the top 3-5 things everyone agrees on?
4.  **Ignore Noise**: Discard generic advice that applies to everything (e.g., "be specific"). Focus on topic-unique advice.

## 4. Generate Output
Based on the `QUERY_TYPE`, generate the final response.

### If QUERY_TYPE is PROMPTING
Write **ONE** perfect, massive, copy-paste-ready prompt.

**CRITICAL**: The prompt format **MUST** match your research findings.
*   If research says "Use XML tags", ANY prompt you write MUST use XML tags.
*   If research says "Use JSON", use JSON.
*   *Do not use your default style if the research suggests a different specific format is better for this tool.*

**Output Structure**:
```markdown
# Trend Research: {TOPIC}

Based on analysis of community discussions from the last 30 days:
*   **Key Insight 1**: [Insight]
*   **Key Insight 2**: [Insight]
*   **Format Consensus**: The community recommends using [Format, e.g., JSON/XML] for best results.

---

## Generated Prompt for {TARGET_TOOL}

```text
[THE ACTUAL PROMPT CONTENT GOES HERE]
[Ensure it follows the constraints finding in your research]
```
```

### If QUERY_TYPE is RECOMMENDATIONS
Provide a ranked list based on **community sentiment**, not just popularity.

**Output Structure**:
```markdown
# Top Recommendations for {TOPIC}

1.  **[Item Name]**
    *   *Why it's trending*: [Specific reason from research, e.g., "Released v2.0 last week"]
    *   *Community Consensus*: [Positive/Negative sentiment]
    
2.  **[Item Name]** ...
```

### If QUERY_TYPE is NEWS/GENERAL
Provide a "State of the Union" summary.

**Output Structure**:
```markdown
# State of {TOPIC}: Last 30 Days

## 🚨 Headlines
*   [Major Event 1]
*   [Major Event 2]

## 📈 Trending Discussions
*   [What are people arguing about?]
*   [What are people excited about?]

## 💡 Takeaway
[One sentence summary of the current vibe]
```


### Iterative Refinement Strategy
This skill is optimized for an iterative approach:
1. **Execute**: Perform the core steps defined above.
2. **Review**: Critically analyze the output (coverage, quality, completeness).
3. **Refine**: If targets aren't met, repeat the specific implementation steps with improved context.
4. **Loop**: Continue until the definition of done is satisfied.
