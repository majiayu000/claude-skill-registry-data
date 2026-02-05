---
name: blog-workflow
description: Orchestrate the mycelium blog workflow - scan repos, draft posts, review changes, build graph, and publish
scopes:
  - project
---

# Blog Workflow Skill

## Overview

Manages the complete workflow for your file-based digital garden blog with mycelium links. This skill orchestrates repository scanning, AI-powered draft generation, content review, graph building, and publishing.

**Core principle:** Git-based content workflow. Everything is versioned, reviewable, and transparent.

## Your Role

You are the orchestrator of the mycelium blog system. You help the user:

1. **Scan repositories** for new content opportunities
2. **Generate AI drafts** with proper metadata and privacy filtering
3. **Review and edit** content before publishing
4. **Build knowledge graph** to detect mycelium connections
5. **Publish changes** with descriptive commits

## Workflow Phases

### Phase 1: Scan & Draft

**Command:** User runs `/blog:scan` or asks "scan my repos for blog content"

**Your process:**

1. Run the repository scanner:
```bash
cd ~/Documents/mycelium-blog
npx tsx scripts/scan-repos.ts
```

2. Scanner analyzes repos in `~/Documents/` and generates:
   - Draft markdown files in `content/drafts/`
   - Metadata extraction (commits, patterns, skills)
   - Privacy classification (public vs internal)
   - AI-suggested titles and tags

3. Report findings:
   ```
   ✅ Scanned 15 repositories
   📝 Generated 3 new draft posts:
      - content/drafts/2025-11-02-temporal-workflows.md (internal)
      - content/drafts/2025-11-02-astro-calculator.md (public)
      - content/drafts/2025-11-02-playwright-automation.md (public)

   🤖 NEXT: Run /blog:review to see drafts
   ```

**Privacy enforcement:**
- Check git remote for "dragancloudbizz" + path contains "neo" → internal
- Internal drafts: Technical patterns only, no business context
- Public drafts: Full transparency with examples

### Phase 2: Complete Drafts (NEW)

**Command:** User runs `/blog:complete` or asks "complete the draft posts"

**Your process:**

1. Find all drafts that need completion:
```bash
cd ~/Documents/mycelium-blog
ls content/drafts/*.md
```

2. For each draft, use the **blog-post-writer skill** to complete the story sections:
   - Read the draft completely (frontmatter + commit history)
   - Analyze commit patterns (features, fixes, refactoring)
   - Write Context, Challenge, Solution, Learned sections
   - Use evidence-based narrative (no unverified assumptions)
   - Apply conversational, pedagogical, or contextual style as appropriate
   - **Output must NOT mention "commits", "git history", or similar meta-references**

3. Invoke blog-post-writer:
   ```
   For each draft file:
   - Read content/drafts/[filename].md
   - Invoke blog-post-writer skill
   - Skill writes the four sections based on commit evidence
   - Save updated draft
   ```

4. Report completion:
   ```
   ✅ Completed 3 draft posts:
      - content/drafts/2025-11-02-temporal-workflows.md
      - content/drafts/2025-11-02-astro-calculator.md
      - content/drafts/2025-11-02-playwright-automation.md

   🤖 NEXT: Run /blog:review to review completed drafts
   ```

**blog-post-writer integration:**
- Uses commit history from the draft's "All Commits" section
- Stays grounded in evidence (no business assumptions for internal posts)
- Applies narrative techniques: conversational hooks, self-aware honesty, progressive revelation
- Uses first-person voice: "I built", "I discovered", "I learned"
- Outputs natural narratives without mentioning "commits", "git history", or meta-analysis

### Phase 3: Review & Curate

**Command:** User runs `/blog:review` or asks "show me the draft posts"

**Your process:**

1. List all drafts in `content/drafts/`:
```bash
cd ~/Documents/mycelium-blog
ls -la content/drafts/
```

2. For each draft, show:
   - Title and metadata (tags, privacy level, repos)
   - AI-generated summary (first paragraph)
   - Suggested action (approve/edit/delete)

3. User chooses an action per draft:
   - **Approve:** Move to `content/posts/`
   - **Edit:** Open in editor, assist with improvements
   - **Delete:** Remove from drafts

4. Example interaction:
   ```
   📄 Draft: "Temporal.io Workflow Patterns with Event Sourcing"
   🏷️  Tags: temporal, event-sourcing, orchestration
   🔒 Privacy: internal (client work)
   📦 Repos: neo-provisioning

   Summary: Explores saga patterns and compensation logic
   in Temporal workflows for distributed systems...

   Options:
   - Approve → Move to posts/
   - Edit → Open for review
   - Skip → Keep in drafts
   ```

**Editing assistance:**
- Suggest improvements to clarity
- Check technical accuracy
- Ensure privacy compliance (no business leaks in internal posts)
- Enhance SEO (title, meta description suggestions)

### Phase 4: Graph Building

**Command:** User runs `/blog:graph` or asks "rebuild the knowledge graph"

**Your process:**

1. Run graph builder:
```bash
cd ~/Documents/mycelium-blog
npx tsx scripts/build-graph.ts
```

2. Graph builder:
   - Scans all published posts, skills, patterns
   - Detects connections via:
     - Shared tags (overlap strength)
     - Explicit cross-references in content
     - Shared repos
     - Tech stack overlap
     - Temporal proximity
   - Generates `public/graph.json`
   - Updates `relatedTo` frontmatter in posts

3. Report new connections:
   ```
   🕸️  Graph rebuilt successfully

   📊 Stats:
      - 24 nodes (18 posts, 4 skills, 2 patterns)
      - 47 edges (connections)

   🆕 New mycelium links:
      - "Temporal Workflows" ←→ "Event Sourcing Patterns" (0.9 strength)
      - "Browser Automation" ←→ "META Script Manager" (1.0 strength)
      - "Astro Calculator" ←→ "Static Site Generation" (0.8 strength)

   🤖 NEXT: Review updated posts or run /blog:publish
   ```

**Edge strength calculation:**
- 1.0 = Explicit reference in content
- 0.8-0.9 = High tag overlap (>60%)
- 0.6-0.7 = Shared repos or tech stack
- 0.3-0.5 = Moderate tag overlap or temporal proximity

### Phase 5: Publish

**Command:** User runs `/blog:publish` or asks "publish the blog changes"

**Your process:**

1. Show what will be committed:
```bash
cd ~/Documents/mycelium-blog
git status
git diff --stat
```

2. Review changes summary:
   ```
   📦 Ready to publish:

   New posts:
   - content/posts/2025-11-02-astro-calculator.md
   - content/posts/2025-11-02-playwright-automation.md

   Updated:
   - public/graph.json (2 new connections)
   - content/posts/2025-10-28-event-sourcing.md (backlinks updated)

   Total: 4 files changed, 312 insertions(+), 8 deletions(-)
   ```

3. Generate descriptive commit message:
   ```
   feat: add 2 new posts (Astro calculator, Playwright automation)

   - Add post on Belgian real estate calculator using Astro + pure functions
   - Add post on browser automation with META pattern and Playwright
   - Update knowledge graph with 2 new mycelium connections
   - Add backlinks to existing event sourcing post

   🤖 Generated with Claude Code

   Co-Authored-By: Claude <noreply@anthropic.com>
   ```

4. Commit and push:
```bash
cd ~/Documents/mycelium-blog
git add .
git commit -m "[generated message]"
git push origin main
```

5. Verify deployment:
   ```
   ✅ Changes committed and pushed
   🚀 Deployment triggered (GitHub Actions / Netlify)
   🌐 Site will be live in ~2 minutes

   🤖 NEXT: Verify at [your-blog-url] in a few minutes
   ```

## Commands Reference

| Command | Alias | Description |
|---------|-------|-------------|
| `/blog:scan` | "scan repos" | Analyze git repos and generate drafts |
| `/blog:complete` | "complete drafts" | Use blog-post-writer to complete story sections |
| `/blog:review` | "review drafts" | Show pending drafts with metadata |
| `/blog:graph` | "rebuild graph" | Detect mycelium connections |
| `/blog:publish` | "publish blog" | Commit and deploy changes |
| `/blog:status` | "blog status" | Show overall blog state |

## File Locations

**Scripts:**
- `scripts/scan-repos.ts` - Repository scanner
- `scripts/build-graph.ts` - Knowledge graph builder
- `scripts/privacy-filter.ts` - Git config privacy checker

**Content:**
- `content/drafts/` - AI-generated drafts awaiting review
- `content/posts/` - Published blog posts
- `content/skills/` - Claude skills documentation
- `content/patterns/` - Technical patterns library

**Generated:**
- `public/graph.json` - Knowledge graph data

## Privacy Guidelines

**Public posts (personal repos):**
- Full project details and business context
- Real domain names and URLs
- Client testimonials (with permission)
- Complete code examples

**Internal posts (dragancloudbizz/neo-* repos):**
- Generic titles: "Temporal Workflow Patterns" ✅ not "Neo Provisioning Architecture" ❌
- Abstract descriptions: "orchestration platform" ✅ not "client X deployment system" ❌
- Sanitized examples: Remove client names, domains, business logic
- Focus: Technical patterns, architectural decisions, code quality

**Always verify:**
```typescript
// Check before publishing
if (post.privacy === 'internal') {
  // Ensure no mentions of:
  - Client names or brands
  - Business domain specifics
  - Proprietary logic or data
  - Financial/operational details
}
```

## Integration with Existing Skills

**Core skill integration:**

1. **blog-post-writer (PRIMARY):** Completes story sections with evidence-based narratives
2. **divergent-ideation:** Generate diverse post angles from repo analysis
3. **gestalt-information-architecture:** Optimize graph visualization layout
4. **ai-slop-detector:** Ensure AI drafts are high quality, not verbose

**Updated workflow synergy:**
```
blog-workflow:scan (repo analysis + draft generation)
    ↓
blog-post-writer (complete story sections) ← NEW!
    ↓
blog-workflow:review (approve/edit/delete)
    ↓
blog-workflow:graph (build connections)
    ↓
blog-workflow:publish (commit + deploy)
```

**Key improvement:** The blog-post-writer skill is now integrated directly into the workflow, transforming commit lists into engaging narratives automatically.

## Error Handling

**Common issues:**

1. **No new content found:**
   ```
   ℹ️  No new activity since last scan

   Last scan: 2025-10-28 (5 days ago)
   Commits since: 0

   🤖 NEXT: Try again after making some commits, or scan older repos
   ```

2. **Privacy violation detected:**
   ```
   ⚠️  Privacy check failed for draft:

   File: content/drafts/2025-11-02-client-deployment.md
   Issue: Contains client name "CloudBizz" in title

   🤖 NEXT: Edit draft to use generic terminology
   ```

3. **Git conflicts:**
   ```
   ❌ Cannot publish: Git conflicts detected

   Conflicted files:
   - public/graph.json

   🤖 NEXT: Pull latest changes and rebuild graph
   ```

## Best Practices

1. **Scan weekly** - Run `/blog:scan` every week to capture recent work
2. **Auto-complete drafts** - Run `/blog:complete` after scanning to generate story sections
3. **Batch reviews** - Review all completed drafts at once for consistency
4. **Rebuild graph after edits** - Connections may change with content updates
5. **Descriptive commits** - Use conventional commit format (feat/fix/docs)
6. **Verify privacy** - Double-check internal posts before publishing

**Recommended workflow cadence:**
- Weekly: scan + complete drafts
- Weekly: review and approve drafts
- Before publishing: rebuild graph
- Regular: publish approved posts

## Workflow Synergy

The updated workflow creates a seamless pipeline:

```
1. /blog:scan
   → Analyzes repos
   → Generates drafts with commit history
   → Creates story prompts

2. /blog:complete (NEW)
   → Invokes blog-post-writer skill
   → Completes Context/Challenge/Solution/Learned sections
   → Uses evidence-based narrative (no commits/git mentioned in output)

3. /blog:review
   → Shows completed drafts
   → Approve/Edit/Delete

4. /blog:graph
   → Detects mycelium connections
   → Updates backlinks

5. /blog:publish
   → Commits and deploys
```

**Key improvement:** The blog-post-writer skill transforms basic drafts with commit lists into engaging, story-driven blog posts automatically. No more manual section writing!

## Example Session

```
User: Scan my repos for new blog content
