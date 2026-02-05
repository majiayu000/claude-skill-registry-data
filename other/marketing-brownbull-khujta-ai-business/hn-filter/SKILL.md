---
name: hn-filter
description: Filter and analyze Hacker News top stories based on user interests. Use when the user wants to browse, filter, or get personalized Hacker News content, find interesting tech articles, or get a curated digest of HN posts.
---

# Hacker News Filter

Filter top 100 Hacker News posts based on user interests with AI-powered semantic matching.

## When to Use This Skill

Use this skill when the user:
- Wants to see filtered/personalized Hacker News content
- Asks about interesting tech news or articles
- Wants a curated HN digest
- Mentions "hacker news", "HN", or tech news filtering

## Workflow

### Step 1: Get User Interests (Interactive)

Ask the user what topics they're interested in and what they want to exclude:

```
What topics interest you today? (Press Enter to use saved defaults)

Examples:
- Interested in: AI, systems programming, developer tools, startups
- Exclude: crypto, blockchain, politics
```

If user presses Enter or says "use defaults", load from config file.

### Step 2: Load/Save Config

Config file location: `~/.claude/hacknews-interest.json`

Expected format:
```json
{
  "interests": ["AI", "machine learning", "systems programming", "developer tools", "open source"],
  "blacklist": ["crypto", "blockchain", "NFT", "web3", "politics"]
}
```

If config doesn't exist, create it with user's input.
If user provides interests interactively, optionally ask if they want to save as new defaults.

### Step 3: Fetch Top 100 HN Stories

Use the Hacker News API:

```bash
# Fetch top story IDs
curl -s "https://hacker-news.firebaseio.com/v0/topstories.json" | jq '.[0:100]'

# Fetch individual story details
curl -s "https://hacker-news.firebaseio.com/v0/item/{id}.json"
```

For each story, extract:
- `id`: Story ID
- `title`: Story title
- `url`: Link to article (may be missing for Ask HN, Show HN)
- `score`: Upvotes
- `descendants`: Comment count
- `by`: Author username

### Step 4: Fetch Article Content (with Caching)

For each story with a URL:

1. **Check cache first**: Look in `~/.cache/hn-filter/articles/{story_id}.txt`
2. **If not cached, fetch article**:
   - Use `curl` or web fetch to get the article content
   - Extract main text content (strip HTML, ads, navigation)
   - Cache the result for future runs
3. **Fallback**: If fetching fails (paywall, blocked, etc.), use title + URL domain for analysis

Cache structure:
```
~/.cache/hn-filter/
â”œâ”€â”€ articles/
â”‚   â”œâ”€â”€ 12345.txt
â”‚   â”œâ”€â”€ 12346.txt
â”‚   â””â”€â”€ ...
â””â”€â”€ comments/
    â”œâ”€â”€ 12345.json
    â””â”€â”€ ...
```

### Step 5: Fetch and Summarize Comments

For each story:

1. Fetch top-level comments (limit to first 10-20 for performance)
2. For each comment, fetch its content
3. Look for substantive discussion points, not meta-commentary

```bash
# Story item includes 'kids' array of comment IDs
curl -s "https://hacker-news.firebaseio.com/v0/item/{comment_id}.json"
```

### Step 6: Semantic Filtering

For each story, analyze:
1. **Title** - Quick keyword + semantic match
2. **Article content** - Deep semantic analysis of full text
3. **URL domain** - Source credibility/relevance (github.com, arxiv.org, etc.)

**Filtering Logic:**
1. First, check blacklist - if ANY blacklist term matches semantically, EXCLUDE the story
2. Then, check interests - if ANY interest matches semantically, INCLUDE the story
3. Blacklist takes priority over interests

**Semantic matching means:**
- Not just exact keyword match
- Understanding context (e.g., "LLM" matches "AI" interest)
- Understanding negation (article criticizing crypto still matches crypto blacklist)
- Understanding related concepts (e.g., "Rust compiler" matches "systems programming")

### Step 7: Generate Output

For each matching story, output:

```
## [Story Title](URL)
Score: X | Comments: Y

**Why this matched:** [1-line AI explanation of why this matches user interests]

**Key discussion points:**
- [Balanced point 1 - present both perspectives if debated]
- [Balanced point 2]
- [Balanced point 3]

---
```

**Discussion point guidelines:**
- Extract substantive insights, not meta-commentary ("great article!")
- When there's debate, present BOTH sides neutrally
- Focus on technical insights, lessons learned, contrarian views
- Ignore flame wars, personal attacks, off-topic tangents
- Limit to 3-5 key points per story

### Output Example

```
# Hacker News Digest - Filtered for: AI, systems programming
Excluding: crypto, blockchain

Found 12 matching stories from top 100

---

## [Anthropic releases Claude 3.5 with improved reasoning](https://example.com/article)
Score: 542 | Comments: 231

**Why this matched:** Directly relevant to AI/ML interests - covers new LLM capabilities and benchmarks.

**Key discussion points:**
- Performance comparison shows 2x improvement on coding tasks vs previous version
- Debate on benchmark validity: some argue real-world performance differs from synthetic tests
- Several commenters report success using it for complex refactoring tasks
- Discussion of API pricing changes and impact on indie developers

---

## [Building a Modern Text Editor in Rust](https://example.com/rust-editor)
Score: 312 | Comments: 89

**Why this matched:** Combines systems programming (Rust) with developer tools (text editor).

**Key discussion points:**
- Author shares performance metrics: <5ms latency for 100k line files
- Debate on using GPU rendering: proponents cite smoothness, critics cite battery drain
- Several suggestions for async architecture patterns for plugin systems

---
```

## Error Handling

- **No config file**: Create default with empty interests/blacklist, ask user to configure
- **API rate limiting**: Add delays between requests, inform user of progress
- **Article fetch failures**: Log which articles couldn't be fetched, continue with title-only analysis
- **No matches found**: Report this to user, suggest broadening interests or narrowing blacklist

## Performance Tips

- Fetch stories in parallel (batch of 10-20 at a time)
- Cache aggressively - articles don't change
- For repeat runs on same day, skip re-fetching if cache is <24 hours old
- Show progress to user: "Fetching stories... 50/100"
