---
name: tech-ecosystem-analyzer
description: This skill should be used when users request comprehensive analysis of technology ecosystems, comparing multiple libraries/frameworks/tools with quantitative metrics from GitHub and web research. Trigger words include "ecosystem analysis", "compare libraries", "analyze React/Vue/Python ecosystem", "trending libraries", "technology stack comparison", or requests to evaluate multiple technical tools with data-driven insights.
---

# Tech Ecosystem Analyzer

## Overview

This skill enables systematic, data-driven analysis of technology ecosystems through a combination of web research, GitHub API data collection, quantitative scoring, and comprehensive documentation. It transforms subjective technology selection into objective, metrics-based decision-making.

Unlike simple web research, this skill produces:
- Quantitative rankings based on GitHub metrics (stars, forks, growth rates)
- Automated data collection via custom Python scripts
- Dual output: raw data (JSON) + analysis report (Markdown)
- Comparative analysis with scoring algorithms
- Trend predictions and actionable recommendations

## When to Use This Skill

Use this skill when users request any of the following:

- **Technology stack evaluation**: "Compare React state management libraries"
- **Ecosystem trend analysis**: "What are the latest trends in the Python data science ecosystem?"
- **Library/framework comparison**: "Analyze Vue.js vs React vs Svelte with data"
- **Tool selection research**: "Which GraphQL client should we use?"
- **Open source project evaluation**: "Compare testing frameworks for JavaScript"
- **Technology adoption decisions**: "Should we migrate from Redux to Zustand?"
- **Competitive technical analysis**: "Compare popular CI/CD tools"

**Key indicators:**
- User requests comparison of **multiple** (3+) libraries/tools
- Request implies need for **quantitative data** (GitHub stats, growth rates)
- User wants **trend analysis** or future predictions
- Decision-making context (choosing between options)
- Request mentions "latest", "trending", "popular", "best"

**Do NOT use this skill when:**
- Analyzing a single library/tool (use web-research-documenter instead)
- No quantitative comparison needed
- Focus is purely qualitative (best practices, tutorials)

## Workflow

Follow this systematic five-step workflow for ecosystem analysis:

### Step 1: Clarify Scope and Output Requirements

Before starting analysis, confirm with the user:
1. Which libraries/frameworks/tools to analyze (minimum 3 recommended)
2. Output directory location for results
3. Any specific metrics of interest (performance, bundle size, etc.)

**Example interaction:**
```
User: "Analyze React state management trends"
Claude: "I'll analyze the React state management ecosystem. I recommend including:
- Redux (traditional standard)
- Zustand (modern lightweight)
- Jotai (atomic pattern)
- TanStack Query (server state)
- Recoil (if desired)

Where would you like me to save the analysis results?"
```

### Step 2: Conduct Multi-Angle Web Research

Execute 2-3 complementary web searches to gather comprehensive context about the ecosystem:

**Search strategy:**
- **Search 1 (Broad)**: Overall ecosystem trends and library names
  - Example: "React state management 2024 2025 Redux Zustand Jotai"
- **Search 2 (Comparative)**: Direct comparisons and decision guides
  - Example: "Redux vs Zustand vs Jotai comparison 2024"
- **Search 3 (Version-specific)**: Latest updates and features
  - Example: "Redux Toolkit Zustand latest version features 2024"

**Tool usage:**
```javascript
// Execute searches in parallel
mcp-server-search__web_search(query="[broad ecosystem query]", max_results=10)
mcp-server-search__web_search(query="[comparison query]", max_results=10)
mcp-server-search__web_search(query="[version-specific query]", max_results=10)
```

**What to extract from search results:**
- Current version numbers and release dates
- Key features and differentiators
- Community sentiment and adoption trends
- Migration patterns (what people are moving from/to)
- Integration patterns with other tools

### Step 3: Generate GitHub Data Collection Script

Create a Python script to automate GitHub API data collection and analysis. Use the template in `scripts/collect_github_data.py` as a foundation.

**Script must include:**
1. Library definitions with GitHub repo paths
2. GitHub API fetching function
3. Popularity score calculation (weighted algorithm)
4. Growth rate estimation
5. JSON data export
6. Console output with rankings

**Key metrics to collect:**
- Stars (primary popularity indicator)
- Forks (community contribution level)
- Open issues (maintenance health)
- Last update timestamp (activity level)
- Watchers
- Creation date (project age)
- License, language, description

**Popularity scoring algorithm:**
Use weighted scoring to normalize and compare different-sized projects:

```python
weights = {
    "stars": 0.4,        # Primary popularity indicator
    "forks": 0.2,        # Community engagement
    "watchers": 0.1,     # Active interest
    "recent_activity": 0.3  # Maintenance health
}

# Normalize against realistic maximums for the ecosystem
star_score = min(stars / max_stars, 1.0) * weights["stars"]
# ... similar for other metrics

total_score = sum(all_scores) * 100  # Scale to 0-100
```

**Growth rate calculation:**
```python
age_days = (now - created_date).days
avg_stars_per_day = stars / max(age_days, 1)

if avg_stars_per_day > 50: return "Very High"
elif avg_stars_per_day > 20: return "High"
elif avg_stars_per_day > 5: return "Medium"
else: return "Low"
```

**File location:**
Save script to: `{output_directory}/collect_github_data.py`

### Step 4: Execute Data Collection

Run the Python script using desktop-commander process execution:

```python
desktop-commander__start_process(
    command=f"cd {output_directory} && python3 collect_github_data.py",
    timeout_ms=30000
)
```

**Expected outputs:**
1. Console summary with rankings
2. JSON file: `{output_directory}/[ecosystem]_data.json`

**Verify data quality:**
- All libraries successfully fetched
- No API rate limit errors
- Popularity scores calculated
- JSON properly formatted

### Step 5: Synthesize Comprehensive Analysis Report

Create a detailed Markdown report using the template structure below. Write in chunks (25-30 lines per write_file call) using desktop-commander.

**Report structure (see `references/report_template.md` for full template):**

```markdown
=============================================================================
[ECOSYSTEM] ECOSYSTEM ANALYSIS REPORT
=============================================================================
Generated: [Date]
Analysis: [List of libraries]
Data Sources: GitHub API, Web Research
=============================================================================

## 1. Executive Summary
- Key findings (3-5 bullet points)
- Top recommendations
- Critical trends

## 2. GitHub Metrics Analysis
- Comprehensive ranking table
- Detailed statistics per library
- Growth rate comparison

## 3. Detailed Library Profiles
For each library:
- Description and use cases
- Latest version and updates
- Strengths and weaknesses
- Community health indicators

## 4. Comparative Analysis
- Side-by-side comparison table
- When to use each option
- Migration considerations

## 5. Top 3 Recommendations
Ranked recommendations with:
- Selection rationale
- Core value proposition
- Ideal use cases
- Code examples (if applicable)

## 6. Trend Predictions
- Growth trajectory analysis
- Future scenarios (with probability estimates)
- Monitoring indicators

## 7. Actionable Recommendations
- Decision framework by project type
- Migration strategies
- Team education priorities
- Implementation checklists

## 8. Learning Resources
- Official documentation links
- Community resources
- Tutorial recommendations

## 9. Data Sources & Methodology
- GitHub repositories
- Web sources cited
- Scoring methodology explained
```

**Writing guidelines:**
- Use visual elements: tables, ASCII art headers, emoji for emphasis
- Include specific numbers: stars, dates, versions
- Provide actionable insights, not just data
- Compare and contrast (don't just list)
- Add code examples for technical concepts
- Use tables for structured comparisons
- Bold key findings and recommendations
- Structure with clear hierarchy (===, ---, •)

**File outputs:**
1. `{output_directory}/[ecosystem]_analysis.md` - Full report
2. `{output_directory}/[ecosystem]_data.json` - Raw data (already created in Step 4)
3. `{output_directory}/collect_github_data.py` - Collection script (already created in Step 3)

### Step 6: Deliver Summary and Next Steps

After completing analysis, provide the user with:

1. **File confirmation**: List all generated files with sizes
2. **Key findings summary**: Top 3-5 insights
3. **Visual ranking**: Quick table/chart of results
4. **Recommended action**: Immediate next step for decision-making

**Example summary:**
```
✅ Analysis Complete! Generated 3 files in results/20250114/:

1. react_ecosystem_analysis.md (28 KB, 715 lines)
   - Comprehensive analysis of 5 libraries
   - Trend predictions through 2026
   - Project-specific recommendations

2. react_data.json (4 KB)
   - Raw GitHub metrics for all libraries

3. collect_github_data.py (3 KB)
   - Reusable data collection script

🏆 Top 3 Recommendations:
1. TanStack Query (47K stars, High Growth) - Server state standard
2. Zustand (56K stars, High Growth) - Simplest client state
3. Redux Toolkit (61K stars, Medium Growth) - Enterprise choice

📊 Key Finding: "Zustand projected to overtake Redux by mid-2026"

💡 Recommended Next Step: [Specific action based on user's context]
```

## Quality Standards

Ensure analysis meets these criteria:

### Comprehensiveness
- ✅ Minimum 3 libraries analyzed
- ✅ Both GitHub metrics AND web research insights
- ✅ Quantitative (scores, stars) AND qualitative (use cases, trends)
- ✅ Historical context and future predictions

### Data Quality
- ✅ Recent data (collected within analysis session)
- ✅ Consistent methodology across all libraries
- ✅ Transparent scoring algorithms
- ✅ Raw data preserved in JSON

### Actionability
- ✅ Clear recommendations (ranked top 3)
- ✅ Decision frameworks by project type
- ✅ Specific migration strategies
- ✅ Immediate action items

### Readability
- ✅ Visual structure (tables, headers, emoji)
- ✅ Scannable format (bullets, bold, sections)
- ✅ Progressive disclosure (summary → details)
- ✅ Examples and code snippets

## Advanced Techniques

### Handling Large Ecosystems (10+ libraries)

For ecosystems with many options:
1. **Phase 1**: Analyze top 5-7 by popularity
2. **Phase 2**: Deep-dive into top 3 based on Phase 1
3. **Optional Phase 3**: Niche/emerging options

### Custom Scoring Algorithms

Adjust weights based on ecosystem characteristics:
- **Mature ecosystems** (e.g., React): Weight recent activity higher
- **Emerging ecosystems** (e.g., Deno): Weight growth rate higher
- **Enterprise contexts**: Weight fork count and open issues higher

### Multi-Dimensional Analysis

Beyond GitHub metrics, consider:
- **Bundle size**: For frontend libraries
- **Performance benchmarks**: For frameworks
- **TypeScript support**: For modern projects
- **Framework integrations**: For specific contexts
- **Learning curve**: For team adoption

Include these in report if relevant to user's context.

### Trend Prediction Methodology

Base predictions on:
1. **Growth rates**: Extrapolate current trajectories
2. **Community signals**: Reddit/Twitter/HN mentions
3. **Corporate backing**: Company sponsorships
4. **Ecosystem momentum**: Integration with popular tools
5. **Developer sentiment**: Issue discussions, migrations

Assign probability estimates to scenarios:
- 90%+ = Highly confident
- 70-90% = Likely
- 50-70% = Moderate confidence
- <50% = Speculative

## Common Pitfalls to Avoid

❌ **Analyzing outdated data**: Always collect fresh GitHub stats
❌ **Ignoring context**: Same library isn't best for all projects
❌ **Pure metrics bias**: High stars ≠ best choice for every case
❌ **Missing the "why"**: Explain rationale, don't just rank
❌ **Incomplete web research**: Multiple search angles required
❌ **Generic recommendations**: Tailor to project size/type
❌ **No actionable steps**: Analysis must guide decisions

## Example Usage Patterns

### Pattern 1: New Project Technology Selection
```
User: "We're starting a new React project. Help us choose state management."
→ Analyze: Redux, Zustand, Jotai, TanStack Query, Recoil
→ Emphasize: Learning curve, bundle size, team onboarding
→ Recommendation: Project size-based decision framework
```

### Pattern 2: Migration Evaluation
```
User: "Should we migrate from Redux to Zustand?"
→ Analyze: Redux, Redux Toolkit, Zustand (focused comparison)
→ Emphasize: Migration effort, breaking changes, ROI
→ Recommendation: Go/no-go decision with migration strategy
```

### Pattern 3: Ecosystem Monitoring
```
User: "What are the latest Python ML library trends?"
→ Analyze: TensorFlow, PyTorch, JAX, scikit-learn, etc.
→ Emphasize: Recent updates, community shifts, future direction
→ Recommendation: When to adopt new tools vs. stay current
```

### Pattern 4: Competitive Analysis
```
User: "Compare GraphQL clients for React"
→ Analyze: Apollo, urql, Relay, graphql-request, etc.
→ Emphasize: Feature comparison, performance, bundle size
→ Recommendation: Use-case specific (simple vs. complex apps)
```

## Integration with Other Skills

This skill complements:
- **web-research-documenter**: Use for single-library deep dives
- **skill-creator**: Create ecosystem-specific skills based on findings
- Can feed into architecture decision records (ADRs)
- Can inform technical roadmap planning

## Maintenance Notes

Keep scoring algorithms updated:
- Adjust max_stars/max_forks based on ecosystem growth
- Update growth rate thresholds as ecosystems mature
- Refine weights based on what correlates with actual adoption

Monitor for GitHub API changes:
- Rate limiting adjustments
- New metrics availability
- Authentication requirements
