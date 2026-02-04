---
name: obsidian-vault-manager
description: Manage Obsidian knowledge base - capture ideas, YouTube videos, articles, repositories, create study guides, and publish to GitHub Pages. Use smart AI tagging for automatic organization.
allowed-tools:
  - SlashCommand(*)
  - mcp__obsidian-mcp-tools__*
  - mcp__MCP_DOCKER__create_or_update_file
  - mcp__MCP_DOCKER__push_files
  - mcp__MCP_DOCKER__get_file_contents
  - mcp__MCP_DOCKER__fetch
  - mcp__MCP_DOCKER__gitingest-analyze
  - Bash(uvx youtube_transcript_api:*)
---

# Obsidian Vault Manager

Manage an AI-powered Obsidian knowledge base with automatic organization and GitHub Pages publishing.

## Vault Configuration

- **Vault Path**: `/Users/zorro/Documents/Obsidian/Claudecode`
- **Publishing Folder**: `documents/` (auto-deploys to GitHub Pages)
- **GitHub Repository**: `ZorroCheng-MC/sharehub`

## Tag Taxonomy (STRICT - Use Only These)

### Content Type Tags (choose 1)
- `idea` - Random thoughts, concepts, brainstorms
- `video` - YouTube videos, lectures
- `article` - Web articles, blog posts
- `study-guide` - Learning materials, courses
- `repository` - Code repositories, technical analysis
- `reference` - Documentation, quick lookups
- `project` - Project notes, planning

### Topic Tags (choose 2-4 relevant)
- `AI` - Artificial intelligence, machine learning
- `productivity` - Time management, workflows, GTD
- `knowledge-management` - PKM, note-taking, Obsidian
- `development` - Programming, software engineering
- `learning` - Education, study techniques
- `research` - Academic, scientific papers
- `writing` - Content creation, blogging
- `tools` - Software tools, applications
- `business` - Entrepreneurship, strategy
- `design` - UI/UX, visual design
- `automation` - Workflows, scripts, efficiency
- `data-science` - Analytics, statistics
- `web-development` - Frontend, backend, full-stack
- `personal-growth` - Self-improvement, habits
- `finance` - Money, investing, economics

### Status Tags (choose 1)
- `inbox` - Just captured, needs processing
- `processing` - Currently working on
- `evergreen` - Timeless, permanent knowledge
- `published` - Shared publicly
- `archived` - Done, historical reference
- `needs-review` - Requires attention

### Priority/Metadata Tags (choose 0-2)
- `high-priority` - Important, urgent
- `quick-read` - <5 min to consume
- `deep-dive` - Complex, requires focus
- `technical` - Code-heavy, engineering
- `conceptual` - Theory, ideas, frameworks
- `actionable` - Contains next steps/todos
- `tutorial` - Step-by-step guide
- `inspiration` - Creative, motivational

## Content Routing (Dispatcher)

When invoked from `/capture`, analyze the input and dispatch to the appropriate slash command:

| Content Type | Pattern | Dispatch Command |
|--------------|---------|------------------|
| **YouTube** | `youtube.com`, `youtu.be` | `SlashCommand("/youtube-note $INPUT")` |
| **GitHub** | `github.com` | `SlashCommand("/gitingest $INPUT")` |
| **Web Article** | Other HTTP/HTTPS URL | `SlashCommand("/study-guide $INPUT")` |
| **Plain Text** | No URL pattern | `SlashCommand("/idea $INPUT")` |

**Example dispatches:**
```
Input: https://youtube.com/watch?v=abc123
→ SlashCommand("/youtube-note https://youtube.com/watch?v=abc123")

Input: https://github.com/anthropics/claude-code
→ SlashCommand("/gitingest https://github.com/anthropics/claude-code")

Input: https://medium.com/some-article
→ SlashCommand("/study-guide https://medium.com/some-article")

Input: My new idea about AI agents
→ SlashCommand("/idea My new idea about AI agents")
```

## Core Operations

### 1. Capture Content (Universal Inbox)

Intelligently route content based on type and create properly tagged notes.

#### YouTube Videos

**Bundled Resources:**
- **Script**: `scripts/core/fetch-youtube-transcript.sh` - Fetches transcript via uvx
- **Template**: `templates/youtube-note-template.md` - Note structure
- **Validation**: `scripts/validation/validate-frontmatter.py` - Quality check

When user provides a YouTube URL:

**Step 1: Extract Video ID and Fetch Transcript**
1. Extract VIDEO_ID from URL (e.g., `https://youtu.be/VIDEO_ID` or `https://www.youtube.com/watch?v=VIDEO_ID`)
2. Run bundled script to fetch transcript:
   ```bash
   SKILL_DIR="$HOME/.claude/skills/obsidian-vault-manager"
   TRANSCRIPT=$("$SKILL_DIR/scripts/core/fetch-youtube-transcript.sh" "$VIDEO_ID")
   ```
3. Use `get_transcript` to get video transcript and `fetch` to get YouTube page for metadata (title, channel, description)

**Step 2: Analyze Content for Smart Tags**
Determine:
- Main topics (choose 2-4 from taxonomy)
- Complexity level:
  - `quick-read` = under 10 minutes
  - `tutorial` = step-by-step instructional
  - `deep-dive` = 30+ minutes, complex
- Content characteristics:
  - `technical` = code-heavy, engineering
  - `conceptual` = theory, frameworks
  - `actionable` = practical steps
  - `inspiration` = motivational
- Priority (high/medium/low based on relevance)

**Step 3: Generate Filename**
Format: `[date]-[creator-or-channel]-[descriptive-title].md`
Example: `2025-10-24-ai-labs-context-engineering-claude-code.md`

**Step 4: Load Template and Substitute Variables**

⚠️ **CRITICAL: You MUST literally read and substitute the template file. DO NOT generate your own structure.**

1. **Read the actual template file** - Execute this command FIRST:
   ```bash
   cat ~/.claude/skills/obsidian-vault-manager/templates/youtube-note-template.md
   ```

2. **Take the raw template content** and perform literal `{{PLACEHOLDER}}` text substitution:
   - DO NOT paraphrase or summarize the template structure
   - DO NOT reorganize or reorder sections
   - DO NOT omit any fields, sections, or elements
   - DO NOT change field names (use `channel:` not `creator:`, use `url:` not `source:`)
   - PRESERVE all emojis in section headers (📖 🎯 📋 📝 ⭐ 🏷️ 🔗)
   - PRESERVE the clickable thumbnail image markdown after the H1 title

3. **Required placeholder substitutions** (ALL must be present in final output):

   | Placeholder | Required | Description |
   |-------------|----------|-------------|
   | `{{VIDEO_ID}}` | **YES** | Must appear in `url:`, `cover:`, AND thumbnail image link |
   | `{{TITLE}}` | **YES** | Video title |
   | `{{CHANNEL}}` | **YES** | Channel name (field must be named `channel:`) |
   | `{{DATE}}` | **YES** | Today's capture date (YYYY-MM-DD) |
   | `{{VIDEO_DATE}}` | **YES** | Video publish date from metadata |
   | `{{TOPIC_TAGS}}` | **YES** | 2-4 topic tags, comma-separated |
   | `{{METADATA_TAGS}}` | **YES** | 1-2 metadata tags |
   | `{{PRIORITY}}` | **YES** | high/medium/low |
   | `{{DURATION}}` | **YES** | Estimated duration (~X minutes) |
   | `{{DESCRIPTION}}` | **YES** | 2-3 sentence summary |
   | `{{LEARNING_OBJECTIVES}}` | **YES** | Bullet list of outcomes |
   | `{{CURRICULUM}}` | **YES** | Structured outline with timestamps |
   | `{{MAIN_INSIGHTS}}` | **YES** | 3-5 key insights |
   | `{{ACTIONABLE_POINTS}}` | **YES** | Practical takeaways |
   | `{{TARGET_AUDIENCE}}` | **YES** | Who should watch |
   | `{{TOPIC_ANALYSIS}}` | **YES** | Explanation of topics |
   | `{{COMPLEXITY_LEVEL}}` | **YES** | quick-read/tutorial/deep-dive |
   | `{{PRIORITY_REASONING}}` | **YES** | Why this priority |
   | `{{TAG_REASONING}}` | **YES** | Tag selection explanation |
   | `{{PRIMARY_TOPIC}}` | **YES** | Main topic for filtering |
   | `{{RELATED_SEARCHES}}` | **YES** | Suggested searches |
   | `{{CONNECTIONS}}` | **YES** | Links to related notes |

4. **Verification checklist** - Before creating file, confirm:
   - [ ] Frontmatter has `cover:` with `https://i.ytimg.com/vi/{{VIDEO_ID}}/maxresdefault.jpg`
   - [ ] Frontmatter has `url:` (not `source:`)
   - [ ] Frontmatter has `channel:` (not `creator:`)
   - [ ] Frontmatter has `video_date:` field
   - [ ] Clickable thumbnail image `[![Watch on YouTube](...)]` appears after H1 title
   - [ ] All section headers have emojis: 📖 🎯 📋 📝 ⭐ 🏷️ 🔗
   - [ ] Rating section with Quality/Relevance/Recommend fields is present
   - [ ] Footer has "Captured:", "Source:", "Channel:" lines

**Step 5: Create Enhanced Video Entry**

Use `mcp__obsidian-mcp-tools__create_vault_file` with the substituted template content.

**Tag Count:** 6-8 tags total
**Always include:** `video`, `inbox`, 2-4 topic tags, 1-2 metadata tags, optional content-specific tags

#### Ideas & Quick Thoughts

**Bundled Resources:**
- **Template**: `templates/idea-template.md` - Idea note structure

When user provides plain text (no URL):

**Step 1: Analyze the Idea**
Extract:
1. Main concept (for title)
2. Related topics (choose 2-4 from taxonomy)
3. Idea type:
   - `actionable` = has concrete next steps
   - `conceptual` = theoretical, framework-based
   - `inspiration` = creative, motivational
   - `high-priority` = urgent or important
4. Brief description (1-2 sentences explaining the idea clearly)

**Step 2: Generate Smart Filename**
Format: `{date}-{3-5-word-idea-name}.md`

Examples:
- "Use AI to automatically categorize notes" → `2025-10-23-ai-note-categorization.md`
- "Knowledge compounds when connected" → `2025-10-23-knowledge-compound-connections.md`

**Step 3: Load Template and Substitute Variables**

⚠️ **CRITICAL: You MUST literally read and substitute the template file. DO NOT generate your own structure.**

1. **Read the actual template file** - Execute this command FIRST:
   ```bash
   cat ~/.claude/skills/obsidian-vault-manager/templates/idea-template.md
   ```

2. **Take the raw template content** and perform literal `{{PLACEHOLDER}}` text substitution:
   - DO NOT paraphrase or summarize the template structure
   - DO NOT reorganize or reorder sections
   - PRESERVE all emojis in section headers (💡 🎯 🔗 📝 🏷️ 🔍)

3. **Required placeholder substitutions:**
   - `{{TITLE}}` - Concise idea title
   - `{{TOPIC_TAGS}}` - 2-4 topic tags from taxonomy (comma-separated)
   - `{{METADATA_TAGS}}` - 1-2 metadata tags (actionable, conceptual, inspiration, etc.)
   - `{{DATE}}` - Current date (YYYY-MM-DD)
   - `{{PRIORITY}}` - high/medium/low
   - `{{CORE_IDEA}}` - Cleaned idea description (1-2 paragraphs)
   - `{{WHY_MATTERS}}` - 1-2 sentences on potential impact or value
   - `{{RELATED_CONCEPTS}}` - Bullet list of related concepts
   - `{{NEXT_STEPS}}` - If actionable: 2-3 next steps. Otherwise: "Further research needed"
   - `{{TOPICS_EXPLANATION}}` - Explanation of why these topics were chosen
   - `{{CHARACTERISTICS_EXPLANATION}}` - Why it's actionable/conceptual/inspiration
   - `{{PRIORITY_EXPLANATION}}` - Reasoning for priority level
   - `{{TAG_REASONING}}` - Overall tag selection explanation
   - `{{PRIMARY_TOPIC}}` - Main topic for filtering
   - `{{SECONDARY_TOPIC}}` - Secondary topic for filtering
   - `{{RELATED_CONCEPT}}` - For semantic search suggestions

4. **Verification checklist** - Before creating file, confirm:
   - [ ] All section headers have emojis
   - [ ] Tags Analysis section is present
   - [ ] Suggested Bases Filters section is present
   - [ ] Footer has "Captured:", "Status:", "Next Action:" lines

**Step 4: Create Enhanced Idea File**

Use `mcp__obsidian-mcp-tools__create_vault_file` with the substituted template content.

**Tag Count:** 5-8 tags total
**Always include:** `idea`, `inbox`, 2-4 topic tags, 1-2 metadata tags

#### GitHub Repositories

When user provides a GitHub URL:

**Step 1: Analyze Repository**
Use `gitingest-analyze` with:
- `source`: GitHub URL
- `include_patterns`: `["*.md", "*.py", "*.js", "*.ts"]` (adapt to repo language)
- `max_file_size`: 10485760 (10MB)

**Step 2: Create Repository Analysis Note**

Use `mcp__obsidian-mcp-tools__create_vault_file`:

```yaml
---
title: "[Repo Name] - Repository Analysis"
tags: [repository, {language}, {topic}, inbox, technical, reference]
url: [github_url]
date: YYYY-MM-DD
type: repository
status: inbox
priority: medium
---

## 📦 Repository Overview
[Repository description from README]

## 🏗️ Architecture
[Key components and structure from gitingest analysis]

## 📁 Key Files & Components
[Important files identified in analysis]

## 📝 Documentation Summary
[Main docs and README content]

## 💡 Key Patterns & Insights
[Notable patterns, technologies, approaches]

## 🏷️ Tags Analysis
- **Topics:** {why these topics}
- **Language:** {primary programming language}
- **Bases Filtering:** `type = repository AND tags contains "{topic}"`

---
*Captured: {date}*
*Source: {repo_url}*
```

**Tag Count:** 6-8 tags

#### Web Articles

When user provides web article URL:

**Step 1: Fetch Content**
Use `mcp__MCP_DOCKER__fetch` to get article content

**Step 2: Create Article Note**

Use `mcp__obsidian-mcp-tools__create_vault_file`:

```yaml
---
title: "[Article Title]"
tags: [article, {topic1}, {topic2}, {topic3}, inbox, quick-read]
url: [article_url]
date: YYYY-MM-DD
type: article
status: inbox
priority: medium
---

## 📄 Summary
[AI-generated summary of key points]

## 🔑 Key Takeaways
- [Point 1]
- [Point 2]
- [Point 3]

## 💭 Personal Notes
[Space for user's thoughts]

## 🔗 Related Resources
[Links mentioned in article]

## 🏷️ Tags Analysis
- **Topics:** {explanation}
- **Bases Filtering:** `type = article AND tags contains "{topic}"`

---
*Captured: {date}*
```

**Tag Count:** 6-8 tags

### 2. Create Study Guides

**Bundled Resources:**
- **Template**: `templates/study-guide-template.md` - Study guide structure

When user requests study guide from URL or content:

**Step 1: Fetch Content**
- If URL: use `mcp__MCP_DOCKER__fetch`
- If file: use `mcp__obsidian-mcp-tools__get_vault_file`
- If direct text: use provided content

**Step 2: Analyze for Smart Tagging**
Identify:
- Main topics and themes → Choose 2-4 topic tags from taxonomy
- Complexity level → `deep-dive` (multi-hour), `technical` (code/math), `conceptual` (theory)
- Practical application → `actionable` (exercises) or `tutorial` (step-by-step)
- Learning prerequisites → Determines difficulty level
- Estimated study time → Hours required
- Priority (high/medium/low based on goals)

**Step 3: Generate Filename**
Format: `[date]-[topic-name]-study-guide.md`

Examples:
- Machine learning basics → `2025-10-28-machine-learning-study-guide.md`
- React advanced patterns → `2025-10-28-react-advanced-study-guide.md`

**Step 4: Load Template and Substitute Variables**

⚠️ **CRITICAL: You MUST literally read and substitute the template file. DO NOT generate your own structure.**

1. **Read the actual template file** - Execute this command FIRST:
   ```bash
   cat ~/.claude/skills/obsidian-vault-manager/templates/study-guide-template.md
   ```

2. **Take the raw template content** and perform literal `{{PLACEHOLDER}}` text substitution:
   - DO NOT paraphrase or summarize the template structure
   - DO NOT reorganize or reorder sections
   - PRESERVE all emojis in section headers (📚 🎯 ⏱️ 📋 💡 🧠 📊 🔗 🏷️ 🔍)

3. **Required placeholder substitutions:**
   - `{{TITLE}}` - Study subject/topic name
   - `{{TOPIC_TAGS}}` - 2-4 topic tags from taxonomy (comma-separated)
   - `{{METADATA_TAGS}}` - 1-2 metadata tags (deep-dive, technical, tutorial, etc.)
   - `{{SOURCE}}` - Source URL or file reference
   - `{{DATE}}` - Current date (YYYY-MM-DD)
   - `{{DIFFICULTY}}` - beginner/intermediate/advanced
   - `{{ESTIMATED_TIME}}` - Study time (e.g., "40 hours", "2 weeks")
   - `{{PRIORITY}}` - high/medium/low
   - `{{LEARNING_OBJECTIVES}}` - Bulleted checklist of objectives
   - `{{PREREQUISITES}}` - Required background knowledge
   - `{{STUDY_METHOD}}` - Recommended approach (active reading, practice-based, mixed)
   - `{{CONTENT_STRUCTURE}}` - Weekly breakdown with concepts/activities/assessments
   - `{{MATERIAL_STRATEGIES}}` - Content-specific study strategies
   - `{{PRACTICE_EXERCISES}}` - Practical exercises or projects
   - `{{TEACHING_TECHNIQUES}}` - How to teach/explain concepts
   - `{{WEEK1_ASSESSMENT}}` - Early knowledge check questions
   - `{{FINAL_ASSESSMENT}}` - Comprehensive assessment questions
   - `{{PROGRESS_STATUS}}` - Weekly completion tracking checklist
   - `{{NEXT_MILESTONE}}` - Specific next goal
   - `{{RELATED_NOTES}}` - Wiki-style links to related content
   - `{{TOPICS_EXPLANATION}}` - Why these topics were chosen
   - `{{DIFFICULTY_EXPLANATION}}` - Difficulty level reasoning
   - `{{CHARACTERISTICS_EXPLANATION}}` - Content characteristics (technical, deep-dive, etc.)
   - `{{PRIORITY_EXPLANATION}}` - Priority reasoning
   - `{{TAG_REASONING}}` - Overall tag selection explanation
   - `{{PRIMARY_TOPIC}}` - Main topic for filtering
   - `{{SECONDARY_TOPIC}}` - Secondary topic for filtering
   - `{{RELATED_CONCEPT}}` - For semantic searches
   - `{{FOUNDATIONAL_TOPIC}}` - Base knowledge topic
   - `{{NEXT_ACTION}}` - Specific next step in study plan

4. **Verification checklist** - Before creating file, confirm:
   - [ ] Frontmatter has `difficulty:` and `estimated-time:` fields
   - [ ] All section headers have emojis
   - [ ] Self-Assessment section with Knowledge Checks is present
   - [ ] Progress Tracking section is present
   - [ ] Footer has "Created:", "Status:", "Next Action:" lines

**Step 5: Create Enhanced Study Guide**

Use `mcp__obsidian-mcp-tools__create_vault_file` with the substituted template content.

**Tag Count:** 6-8 tags total
**Status:** Always use `processing` for study guides (not `inbox`)
**Always include:** `study-guide`, `processing`, 2-4 topic tags, 1-2 metadata tags

### 3. Search Vault (Semantic Search)

When user asks to search vault:

**Use Semantic Search:**

Since Smart Connections is configured, use `mcp__obsidian-mcp-tools__search_vault_smart` with the query:

```
mcp__obsidian-mcp-tools__search_vault_smart({
  query: "[user's search query]",
  filter: {
    limit: 5
  }
})
```

**Present results showing:**
- Note titles
- Relevant excerpts
- Tags and metadata
- Connections to other notes

**Example queries:**
- "Search for notes about productivity and AI"
- "Find everything related to learning workflows"
- "Show me all high-priority technical content"

### 4. Bulk Tag Existing Notes

When user asks to tag untagged notes:

**Step 1: Discover Files**
Use `mcp__obsidian-mcp-tools__list_vault_files` to find markdown files

**Step 2: Process Each File**
For each file:

1. Use `mcp__obsidian-mcp-tools__get_vault_file` to read content
2. Analyze existing frontmatter:
   - Check if `tags:` field exists
   - Check if tags are comprehensive (5+ taxonomy tags)
3. Skip if already well-tagged (has 5+ taxonomy-compliant tags)
4. Analyze content to determine:
   - Content type (from filename, existing tags, content)
   - Main topics (2-4 from content analysis)
   - Status (infer from content or default to `evergreen` for old notes)
   - Metadata characteristics
5. Generate enhanced tag array (5-8 tags total)
6. Use `mcp__obsidian-mcp-tools__patch_vault_file` to update frontmatter:

```
mcp__obsidian-mcp-tools__patch_vault_file({
  filename: "[note-name].md",
  targetType: "frontmatter",
  target: "tags",
  operation: "replace",
  contentType: "application/json",
  content: "[{content-type}, {topic1}, {topic2}, {status}, {metadata}]"
})
```

**Important Rules:**
1. Preserve existing data - merge AI tags with existing tags
2. Be conservative - if uncertain, default to `reference`
3. Handle errors gracefully - skip invalid files
4. Respect user intent - enhance rather than replace

**Step 3: Report Progress**
After every 5-10 files:
```
✅ Tagged 10 files:
   - 3 ideas tagged with [idea, productivity, ...]
   - 2 videos tagged with [video, AI, learning, ...]
   - 5 articles tagged with [article, development, ...]

📊 Progress: 10/47 files processed
🏷️  Total tags added: 73 tags
```

**Step 4: Final Summary**
```markdown
# Bulk Tagging Report

## Summary
- **Files processed:** 47
- **Files updated:** 43
- **Files skipped:** 4 (already well-tagged)
- **Total tags added:** 312
- **Average tags per note:** 7.3

## Tag Distribution

### By Content Type
- idea: 15 notes
- video: 8 notes
- article: 12 notes

### By Topic
- AI: 23 notes
- productivity: 18 notes
- knowledge-management: 15 notes

### By Status
- inbox: 12 notes
- evergreen: 28 notes
- published: 7 notes

## Bases Filtering Suggestions

You can now create Bases views like:
1. **AI Learning Pipeline**: `type = video AND tags contains "AI" AND status = inbox`
2. **Quick Wins**: `tags contains "quick-read" AND tags contains "high-priority"`
3. **Technical Deep Dives**: `tags contains "technical" AND tags contains "deep-dive"`
4. **Actionable Items**: `tags contains "actionable" AND status != archived`
```

### 5. Publish to GitHub Pages

**Bundled Resources:**
- **Script**: `scripts/core/publish.sh` - Complete publish workflow

When user asks to publish a note:

**Step 1: Validate Input**

Add `.md` extension if not provided and verify file exists in vault.

**Step 2: Run Bundled Publish Script**

```bash
SKILL_DIR="$HOME/.claude/skills/obsidian-vault-manager"
"$SKILL_DIR/scripts/core/publish.sh" "$NOTE_FILE"
```

**What the script does:**
1. Finds all image references in the note (supports jpg, jpeg, png, gif, svg, webp)
2. Copies images from Claudecode vault to sharehub repository (preserves directory structure)
3. Converts relative image paths to absolute GitHub Pages URLs:
   - `./images/file.jpg` → `/sharehub/images/file.jpg`
   - `images/file.jpg` → `/sharehub/images/file.jpg`
4. Copies the note with converted paths to `sharehub/documents/`
5. Creates git commit with proper message format
6. Pushes to GitHub (triggers GitHub Pages deployment)

**Step 3: Wait for Deployment**

```bash
# Wait for GitHub Actions to start
sleep 3

# Show recent workflow runs
gh run list --limit 3 --repo ZorroCheng-MC/sharehub 2>/dev/null || echo "Install GitHub CLI with: brew install gh"

echo ""
echo "⏳ Waiting 60 seconds for GitHub Pages to deploy..."
sleep 60
```

**Step 4: Verify Published Page**

Use `mcp__MCP_DOCKER__fetch` to verify the page is live:
```
url: https://zorrocheng-mc.github.io/sharehub/documents/${NOTE_FILE%.md}.html
max_length: 2000
```

Check the fetched content for:
- Page title matches the note title
- Main heading is present
- No 404 or error messages
- Images are referenced correctly

**Publishing Paths:**
- **Vault**: `/Users/zorro/Documents/Obsidian/Claudecode`
- **Sharehub**: `/Users/zorro/Dev/sharehub`
- **Repository**: `ZorroCheng-MC/sharehub`
- **GitHub Pages**: `https://zorrocheng-mc.github.io/sharehub`

**Notes:**
- This workflow requires filesystem access (works in Claude Code CLI)
- For Claude Desktop: Consider using MCP GitHub tools as alternative
- Script handles all image copying and path conversion automatically
- Git commit includes Claude Code attribution

## MCP Tools Reference

### Primary Tools
- `mcp__obsidian-mcp-tools__create_vault_file` - Create new notes
- `mcp__obsidian-mcp-tools__get_vault_file` - Read note content
- `mcp__obsidian-mcp-tools__patch_vault_file` - Update frontmatter/sections
- `mcp__obsidian-mcp-tools__search_vault_smart` - Semantic search
- `mcp__obsidian-mcp-tools__list_vault_files` - List files
- `mcp__MCP_DOCKER__fetch` - Get web content
- `mcp__MCP_DOCKER__gitingest-analyze` - Analyze repositories
- `mcp__MCP_DOCKER__create_or_update_file` - Create/update single file on GitHub
- `mcp__MCP_DOCKER__push_files` - Push multiple files to GitHub in one commit
- `mcp__MCP_DOCKER__get_file_contents` - Read files from GitHub
- YouTube transcript via bash script (`uvx youtube_transcript_api`)

## Response Format

When completing operations:
1. **Confirm action**: "✅ Created video note: [title]"
2. **Show frontmatter**: Display YAML tags and metadata
3. **Provide path**: Show filename and location
4. **For publishing**: Include GitHub Pages URL
5. **Be concise**: Action-oriented responses

## Quality Standards

- **Consistent tagging**: Use ONLY the defined taxonomy
- **Correct tag counts**: 5-8 for ideas, 6-8 for videos/study-guides
- **Complete frontmatter**: All required YAML fields
- **Clean formatting**: Proper markdown structure
- **Meaningful titles**: Descriptive, searchable
- **Actionable content**: Include next steps where relevant
- **Smart defaults**: Medium priority, inbox status for new captures (except study-guides use processing)
- **Date stamps**: Always include capture date (YYYY-MM-DD)
- **Filename rules**: Follow format for each content type

## Integration with Bases

These tags enable powerful Bases filtering queries like:

- "Show all `inbox` items with `high-priority`"
- "Show `video` content about `AI` and `productivity`"
- "Show `actionable` items in `processing` status"
- "Show `technical` `tutorial` content for learning"

**Always create tags with filtering in mind.**
