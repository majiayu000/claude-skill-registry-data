---
description: Deep competitive analysis - research, compare, strategise
argument-hint: "[your product or market]"
allowed-tools:
  - Read
  - Write
  - Edit
  - Agent
  - Glob
  - WebSearch
  - WebFetch
  - Bash(date:*)
---

Deep competitive intelligence. Research competitors, extract positioning and pricing, generate strategic comparison and recommendations.

## Steps

### Step 1: Define the competitive frame

Clarify:
- **Your product/service:** What are you competing with?
- **Market category:** What space are you in?
- **Known competitors:** Any the user already knows about?

### Step 2: Research competitors (parallel agents)

Spawn 2-3 agents to research in parallel:

**Agent 1 — Direct competitors:**
- Search for products/services in the same category
- For each: name, URL, pricing, key features, target customer, funding/size
- Look at their landing pages, pricing pages, feature pages

**Agent 2 — Adjacent competitors:**
- Search for alternative approaches to the same problem
- Products in adjacent categories that could expand into this space
- Open-source alternatives

**Agent 3 — Market context:**
- Recent news, launches, shutdowns in this space
- Analyst reports or market sizing data
- Customer sentiment (reviews, Reddit, Twitter)

### Step 3: Build the comparison matrix

Create a structured comparison:

| Dimension | Your Product | Competitor A | Competitor B | Competitor C |
|-----------|-------------|-------------|-------------|-------------|
| **Price** | | | | |
| **Target customer** | | | | |
| **Key differentiator** | | | | |
| **Strengths** | | | | |
| **Weaknesses** | | | | |
| **Feature 1** | | | | |
| **Feature 2** | | | | |

### Step 4: Identify strategic insights

Analyse the comparison for:

**Gaps you can exploit:**
- Features competitors lack that customers want
- Price points nobody serves
- Customer segments being ignored
- Positioning angles nobody owns

**Threats to watch:**
- Well-funded competitors making moves
- Feature convergence (everyone building the same thing)
- Platform risk (dependency on a platform that could compete)

**Your unfair advantages:**
- What do you have that's hard to replicate?
- Speed, expertise, network, data, positioning?

### Step 5: Strategic recommendations

Based on the analysis:
1. **Positioning recommendation:** How to position against the field
2. **Pricing recommendation:** Where to price and why
3. **Feature priority:** What to build (and not build) based on competitive gaps
4. **Messaging:** Key claims that differentiate you
5. **Watch list:** Competitors to monitor closely and triggers for action

### Step 6: Write the intel report

Save to `competitive-intel-[market].md`:

```markdown
# Competitive Intelligence — [Market/Product]

**Date:** [date]

## Market Overview
[2-3 sentences on the competitive landscape]

## Competitor Profiles

### [Competitor 1]
- **URL:** [url]
- **Pricing:** [pricing model and range]
- **Target:** [who they serve]
- **Strengths:** [bullets]
- **Weaknesses:** [bullets]

[Repeat for each competitor]

## Comparison Matrix
[Table from Step 3]

## Strategic Insights

### Gaps to Exploit
[bullets]

### Threats to Watch
[bullets]

### Your Advantages
[bullets]

## Recommendations
1. [Specific, actionable recommendation]
2. [Specific, actionable recommendation]
3. [Specific, actionable recommendation]

---
Sources: [list all URLs and sources used]
```

Output a summary of key findings and top recommendation.
