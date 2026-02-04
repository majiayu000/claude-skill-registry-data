---
name: docs-create
description: |
  Create epic-specific documentation skill with external reference docs. MUST BE USED for caching external docs.
  Fetches URLs, caches full content, uses documentation-engineer to generate cohesive summaries, and creates auto-activating skill.
  Use when starting work on epic that requires external documentation context (API docs, tool guides, reference materials),
  or when user mentions "cache docs", "external docs", "API documentation", URLs for docs,
  documentation needs, reference materials, knowledge caching, or epic context documentation.
tags: [meta, documentation, skill-creation, caching]
allowed-tools:
  - Bash
  - Read
  - Write
  - WebFetch
  - Task
  - mcp__serena__write_memory
  - mcp__serena__read_memory
  - mcp__serena__list_dir
---

# docs-create: External Docs Skill Generator

Creates epic-specific skill for loading external documentation into session context.

## Problem Solved

When working on epics that require external docs (Beads, Claude Code, Railway, etc.), you need:
- Same 10-20 docs available across multiple sessions
- Auto-activation when relevant topics come up
- No re-pasting URLs every session
- Easy to add/remove/refresh docs

## Solution

Creates `.claude/skills/docs-{epic-id}/SKILL.md` with:
- 3-6 line summaries per doc (in skill description)
- Full docs cached to Serena
- Auto-activation on relevant topics
- Commands: list, show, add, remove, refresh, archive

## Usage

```bash
/docs-create bd-xyz https://url1 https://url2 https://url3 ...
```

**Arguments:**
- `epic-id`: Beads issue ID (e.g., bd-xyz)
- `urls`: Space-separated list of URLs to cache

**Example:**
```bash
/docs-create bd-abc \
  https://github.com/steveyegge/beads/blob/main/AGENTS.md \
  https://docs.claude.com/claude-code/skills \
  https://docs.railway.app/reference/variables
```

## Workflow

### Phase 1: Fetch & Cache

For each URL:
1. Download content (WebFetch for web, raw GitHub URLs for .md)
2. Extract meaningful slug from URL
3. Cache to `.serena/memories/external_{epic}/doc{N}_{slug}.md`
4. Track URL → doc mapping

**Storage structure:**
```
.serena/memories/external_bd-xyz/
  ├── doc1_beads_agents.md
  ├── doc2_claude_skills.md
  ├── doc3_railway_variables.md
  └── manifest.json  # URL → doc mapping
```

### Phase 2: Batch Summarization (Built-in)

Read all cached docs together and generate summaries.

**Process:**
1. Read all N docs from `.serena/memories/external_{epic}/`
2. Analyze together to identify:
   - Key concepts per doc
   - Overlapping topics (reduce redundancy)
   - Cross-references between docs
   - Trigger keywords for auto-activation
3. Generate 3-6 line summary per doc
4. Extract combined topic keywords

**Example output:**
```
Doc 1: Beads AGENTS.md
Summary: Beads workflow for AI agents: Issue-First development pattern, epic→feature→task hierarchy, dependency types (blocks, parent-child, discovered-from). Core commands: bd create/update/close, bd ready, bd sync. Multi-developer git integration via .beads/issues.jsonl.
Topics: beads, workflow, issue-first, dependencies

Doc 2: Claude Code Skills
Summary: Skill structure: SKILL.md frontmatter (name, description, allowed-tools), auto-activation via semantic description matching. Tool restrictions, skill chaining, error handling patterns. Integrates with Beads workflow (see Doc 1).
Topics: claude-code, skills, auto-activation, tools

Doc 3: Railway Variables
Summary: Environment variable management: service-level vs shared variables, reference syntax ${{SERVICE.VAR}}, Railway CLI commands, secrets handling. Auto-redeploy on variable changes. Used for deployment config (complements Claude Code in Doc 2).
Topics: railway, environment, deployment, config

Combined topics: beads, workflow, issue-first, claude-code, skills, railway, deployment, environment
```

**Why batch processing:**
- See all docs together (identify overlaps)
- Reduce redundant summaries (cross-reference instead)
- Create cohesive set that works together

### Phase 3: Generate Epic-Specific Skill

Create `.claude/skills/docs-{epic}/SKILL.md`:

```markdown
---
name: docs-{epic}
description: |
  Documentation context for {epic}: {title}

  Auto-activates when discussing: {combined_topics}

  Summaries ({N} docs):

  1. **{doc1_name}** - {doc1_summary}

  2. **{doc2_name}** - {doc2_summary}

  ... [{N} total]

allowed-tools:
  - Read
  - mcp__serena__read_memory
  - Bash
  - Write
  - WebFetch
  - Task
---

# Documentation Context: {epic}

This skill provides quick access to {N} external docs.

## Cached Docs

{manifest.json content - URL → doc mapping}

## Commands

Run `/docs-{epic} <command>` where command is:

- `list` - Show all doc summaries
- `show <N>` - Read full doc (e.g., `/docs-{epic} show 3`)
- `add <url>` - Add new doc to collection
- `remove <N>` - Remove doc from collection
- `refresh` - Re-download all URLs (get latest)
- `archive` - Move skill to archive (cleanup)

[Command implementations...]
```

### Phase 4: Confirmation

```
✅ Created .claude/skills/docs-{epic}/
✅ Cached {N} docs to .serena/memories/external_{epic}/
✅ Generated summaries via documentation-engineer
✅ Skill auto-activates on: {topics}

Next:
- Skill is active (will auto-trigger on relevant topics)
- Manage with: /docs-{epic} list|show|add|remove|refresh
- When done: /docs-{epic} archive
```

## Agent Implementation (When Invoked)

When user runs `/docs-create bd-xyz <url1> <url2> ...`, follow these steps:

### Step 1: Parse & Validate

```
Input: epic_id, urls[]
Validate: epic exists in Beads (bd show {epic_id})
Get: epic title for context
```

### Step 2: Fetch & Cache All Docs

For each URL:
1. Use WebFetch to get content (handles both .md and HTML)
2. Extract slug from URL for filename
3. Write to `.serena/memories/external_{epic}/doc{N}_{slug}.md`
4. Track in manifest.json

```json
// .serena/memories/external_{epic}/manifest.json
{
  "epic_id": "bd-xyz",
  "epic_title": "Authentication Epic",
  "created": "2025-01-15T14:30:00Z",
  "docs": [
    {"num": 1, "url": "https://...", "file": "doc1_beads_agents.md", "slug": "beads_agents"},
    {"num": 2, "url": "https://...", "file": "doc2_claude_skills.md", "slug": "claude_skills"}
  ]
}
```

### Step 3: Read All Docs & Generate Summaries

Read all cached docs together:

```
For doc in .serena/memories/external_{epic}/*.md:
  Read full content
  Note key concepts
  Identify overlap with other docs
```

Generate summaries (3-6 lines each):
- Focus on unique value of each doc
- Cross-reference related docs (e.g., "see Doc 1 for...")
- Extract topic keywords
- Ensure non-redundant (if two docs cover same topic, divide clearly)

Output format:
```
summaries = [
  {
    num: 1,
    name: "Beads AGENTS.md",
    summary: "...",
    topics: ["beads", "workflow", ...]
  },
  ...
]
combined_topics = [all unique topics]
```

### Step 4: Generate docs-{epic} Skill

Create `.claude/skills/docs-{epic}/SKILL.md` with:

- **Frontmatter:** name, description (with summaries), allowed-tools
- **Commands:** list, show, add, remove, refresh, archive
- **Manifest reference:** Link to cached docs

See "Generated Skill Template" section below for full template.

### Step 5: Confirm

```
✅ Created .claude/skills/docs-{epic}/
✅ Cached {N} docs to .serena/memories/external_{epic}/
✅ Generated {N} summaries
✅ Skill active - auto-activates on: {topics}

Test: Try asking about one of the topics to verify auto-activation
Manage: /docs-{epic} list|show|add|remove|refresh|archive
```

## Generated Skill Commands

Each generated `docs-{epic}` skill includes these commands:

### list
Shows all cached doc summaries.

### show <N>
Reads full doc from Serena cache.

```bash
DOC_NUM=$1
EPIC_ID=$(basename $(dirname "$0") | sed 's/docs-//')
mcp__serena__read_memory(
  memory_file_name="external_${EPIC_ID}/doc${DOC_NUM}_*.md"
)
```

### add <url>
Adds new doc to collection, regenerates summaries.

### remove <N>
Removes doc from collection, regenerates summaries.

### refresh
Re-downloads all URLs (gets latest versions).

### archive
Moves skill to `.claude/skills/archive/` for cleanup.

## Best Practices

**When to use:**
- Starting work on epic with 5+ external docs
- Docs needed across multiple sessions
- Want auto-activation on relevant topics

**When NOT to use:**
- One-off doc reference (just use WebFetch)
- Docs change frequently (manual refresh overhead)
- Simple features (<5 docs, 1-2 sessions)

**Maintenance:**
- Run `/docs-{epic} refresh` weekly if docs update frequently
- Remove unused docs with `/docs-{epic} remove N`
- Archive when epic complete: `/docs-{epic} archive`

## Example Workflow

```bash
# Day 1: Start authentication epic
User: "work on authentication"
Agent: Creates bd-abc

# Day 1: Load external docs
User: "/docs-create bd-abc https://beads.md https://railway.md https://clerk.md"
Agent: [Fetches, summarizes, creates skill]
       ✅ docs-bd-abc active

# Day 2: Work on spec (docs auto-activate)
User: "how do I create epic dependencies in Beads?"
Agent: [docs-bd-abc auto-activates]
       [Reads Beads summary, decides to show full doc]
       /docs-bd-abc show 1
       [Answers with full context]

# Day 10: Need more docs
User: "/docs-bd-abc add https://supabase.com/docs/auth/rls"
Agent: [Fetches, regenerates summaries]
       ✅ Now 4 docs

# Week 4: Complete epic
User: "finish bd-abc"
Agent: [finish-feature skill]
       "/docs-bd-abc archive"
       ✅ Archived
```

## Storage & Cleanup

**Active:**
```
.claude/skills/docs-bd-xyz/SKILL.md
.serena/memories/external_bd-xyz/
  ├── manifest.json
  ├── doc1_beads_agents.md
  └── doc2_claude_skills.md
```

**Archived:**
```
.claude/skills/archive/docs-bd-xyz/SKILL.md
.serena/memories/archive/external_bd-xyz/
```

**Restore:**
```bash
mv .claude/skills/archive/docs-bd-xyz .claude/skills/
mv .serena/memories/archive/external_bd-xyz .serena/memories/
/docs-bd-xyz refresh  # Get latest versions
```

## Generated Skill Template

Template for `.claude/skills/docs-{epic}/SKILL.md`:

```markdown
---
name: docs-{epic}
description: |
  Documentation context for {epic}: {epic_title}

  Auto-activates when discussing: {combined_topics}

  Summaries ({N} docs):

  1. **{doc1_name}** - {doc1_summary}

  2. **{doc2_name}** - {doc2_summary}

  ... [{N} total]

allowed-tools:
  - Read
  - mcp__serena__read_memory
  - Write
  - WebFetch
---

# Documentation Context: {epic}

{epic_title}

**Cached docs:** {N}
**Last updated:** {date}
**Location:** `.serena/memories/external_{epic}/`

## Quick Reference

{summary_list}

## Commands

Run `/docs-{epic} <command>`:

- `list` - Show all summaries
- `show <N>` - Read full doc
- `add <url>` - Add new doc
- `remove <N>` - Remove doc
- `refresh` - Re-download all
- `archive` - Move to archive

## Cached Docs

{manifest_content}

---

When invoked with command:
- Parse command (list/show/add/remove/refresh/archive)
- Execute appropriate action
- Use mcp__serena__read_memory for showing full docs
- Use WebFetch for adding/refreshing
```

## Related

- **issue-first skill**: Suggests `/docs-create` for epics
- **finish-feature skill**: Auto-archives docs when epic complete
