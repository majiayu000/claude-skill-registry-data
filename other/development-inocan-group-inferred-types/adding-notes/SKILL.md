---
name: adding-notes
description: Add new notes to the Second Brain knowledge base. Use when the user provides a resource (URL, book, podcast, article, GitHub repo, Reddit thread) and asks to "add a note", "create a note", "save this", "add to my notes", "take notes on", or "capture this".
allowed-tools: Read, Write, Bash, WebFetch, Glob, Grep, Task, TaskOutput, WebSearch, AskUserQuestion
---

# Adding Notes to Second Brain

Add content to the knowledge base with proper frontmatter, tags, summaries, and wiki-links.

## Content Type Routing

Detect type from URL, then load the appropriate reference file.

| URL Pattern | Type | Reference |
|-------------|------|-----------|
| youtube.com | See [YouTube Classification](#youtube-classification) | `references/content-types/youtube.md` or `talk.md` or `podcast.md` |
| reddit.com | reddit | `references/content-types/reddit.md` |
| github.com | github | `references/content-types/github.md` |
| goodreads.com/series/ | manga | `references/content-types/manga.md` |
| goodreads.com, amazon.com (books) | book | `references/content-types/book.md` |
| spotify.com/episode, podcasts.apple.com | podcast | `references/content-types/podcast.md` |
| udemy.com, coursera.org, skillshare.com | course | `references/content-types/course.md` |
| *.substack.com/p/*, *.beehiiv.com/p/*, buttondown.email/* | newsletter | `references/content-types/newsletter.md` |
| Other URLs | article | `references/content-types/article.md` |
| No URL | note | `references/content-types/note.md` |
| Manual: `quote` | quote | `references/content-types/quote.md` |
| Manual: `evergreen` | evergreen | `references/content-types/evergreen.md` |
| Manual: `map` | map | `references/content-types/map.md` |

### YouTube Classification

YouTube URLs require sub-classification before processing:

1. **Known podcast channel?** → `references/content-types/podcast.md`
2. **Known talk channel OR conference title?** → `references/content-types/talk.md`
3. **Tutorial signals?** → `references/content-types/youtube.md` with `isTechnical: true`
4. **Default** → `references/content-types/youtube.md`

See `references/content-types/youtube.md` for full classification logic and channel lists.

---

## Scripts Reference

Only use scripts that fetch external data or perform complex processing:

| Script | Purpose |
|--------|---------|
| `get-youtube-metadata.sh URL` | Fetch video title, channel |
| `get-youtube-transcript.py URL` | Fetch video transcript |
| `get-podcast-transcript.py [opts]` | Multi-source podcast transcript |
| `get-reddit-thread.py URL --comments N` | Fetch thread and top comments |
| `get-goodreads-metadata.sh URL` | Fetch book title, author, cover |
| `get-manga-metadata.sh URL` | Fetch series metadata |
| `get-github-metadata.sh URL` | Fetch repo name, stars, language |
| `find-related-notes.py FILE --limit N` | Find semantically related notes |

**Do NOT use scripts for these trivial operations — do them inline:**
- Slug generation: `"My Title Here"` → `my-title-here` (lowercase, spaces to hyphens)
- Author check: Use `Glob` tool with `content/authors/*{lastname}*.md`
- Frontmatter templates: Write YAML directly
- Tag lookup: Use `Grep` tool or rely on knowledge from prior notes

---

## Workflow Phases

```text
Phase 1: Type Detection → Route to content-type file
Phase 2: Parallel Metadata Collection → Per-type agents
Phase 3: Author Creation → See references/author-creation.md
Phase 4: Content Generation → Apply writing-style, generate body
Phase 4.5: Connection Discovery → Find genuine wiki-link candidates (if any exist)
Phase 5: Quality Validation → Parallel validators
Phase 6: Save Note → Write to content/{slug}.md with link density report
Phase 7: MOC Placement → Suggest placements + check MOC threshold
Phase 8: Quality Check → Run pnpm lint:fix && pnpm typecheck
```

### Phase 1: Type Detection & Dispatch

1. **Detect type from URL** using the Content Type Routing table above (no script needed)
2. **Load the content-type reference file** for detailed handling
3. Detect `isTechnical` flag (see content-type file for criteria)

### Phase 2: Metadata Collection

Spawn parallel agents as specified in the content-type file. Each file lists:
- Required scripts to run
- Agent configuration
- Special handling notes

**If `isTechnical: true`:** Also spawn code extraction agent (see `references/code-extraction.md`).

### Phase 3: Author Creation

For external content types, authors are **required**. Check existence with Glob (no script needed):

```text
Glob: content/authors/*{lastname}*.md
```

**Handle by result:**

| Result | Action |
|--------|--------|
| Exact match found | Use the existing author's slug |
| Partial match | Read matched files, use `AskUserQuestion` to verify |
| No matches | Create new author (see below) |

**For partial matches**, use the `AskUserQuestion` tool:

```yaml
question: "Is [Author Name] the same person as this existing author?"
header: "Author Match"
multiSelect: false
options:
  - label: "Yes, use existing"
    description: "Use the existing author profile"
  - label: "No, create new"
    description: "Create a new author profile"
```

**Quick creation flow:**
1. WebSearch: `[Author Name] official site bio`
2. Extract: bio, avatar, website, socials
3. Write author file directly (no script):

```yaml
---
name: "Author Name"
slug: "author-name"
bio: "1-2 sentence description"
avatar: ""
website: ""
socials:
  twitter: ""
  github: ""
  linkedin: ""
  youtube: ""
---
```

4. Save to `content/authors/{slug}.md` (slug = lowercase name, spaces to hyphens)

**Tip:** Add `aliases` field to authors who go by multiple names (e.g., "DHH" → aliases: ["David Heinemeier Hansson"]).

### Phase 4: Content Generation

1. **Load writing-style skill** (REQUIRED): `Read .claude/skills/writing-style/SKILL.md`
2. **Load linking philosophy** (REQUIRED): `Read .claude/skills/adding-notes/references/linking-philosophy.md`
3. If `isTechnical`: collect code snippets from Phase 2
4. **Compile frontmatter** using template from content-type file
5. **Generate body** with wiki-links (see Phase 4.5 for connection discovery)
6. Add diagrams if applicable (see `references/diagrams-guide.md`)

**Tags:** 3-5 relevant tags. Use tags you've seen in prior notes or `Grep` for similar content to find existing tags.

**Summary:** Frame as a core argument, not a description. What claim does this content make?

### Phase 4.5: Connection Discovery

Before finalizing content, search for genuinely related notes. **Only add connections that organically make sense.**

1. **Same author check** (highest priority): If author exists, find their other works:
   ```text
   Grep pattern: "authors:.*{author-slug}" glob: "content/*.md"
   ```

2. **Tag-based discovery:** For each tag, find notes with that tag:
   ```text
   Grep pattern: "tags:.*{tag}" glob: "content/*.md" limit: 5
   ```

3. **Evaluate candidates:** For each potential connection, ask: "Would I naturally reference this when discussing the topic?" If the answer is no, don't force the link.

**Connection quality over quantity:**
- Add links only when the relationship is genuine and useful
- If no notes genuinely relate, save as an orphan—that's fine
- Forced connections create noise and reduce trust in the link graph
- A well-explained single link beats two tenuous ones

**When adding links**, explain the relationship:
- `[[note]] - Same author explores this from a different angle`
- `[[note]] - Provides the theoretical foundation for these ideas`

### Phase 5: Quality Validation

Spawn parallel validators:

| Validator | Checks |
|-----------|--------|
| Wiki-link exists | Each `[[link]]` exists in `content/` (excluding Readwise) |
| Link context | Each link has adjacent explanation (not bare "See also") |
| Duplicate | Title/URL doesn't already exist |
| Tag | Tags match or similar to existing |
| Type-specific | E.g., podcast: profile exists, guest not in hosts |

**Wiki-link note:** Readwise highlights (`content/readwise/`) are excluded from Nuxt Content and won't resolve as valid wiki-links. Use plain text or italics for books/articles that only exist in Readwise.

**IF issues found:** Use the `AskUserQuestion` tool:

```yaml
question: "Validation found issues. How should I proceed?"
header: "Validation"
multiSelect: false
options:
  - label: "Fix issues"
    description: "Let me fix the issues before saving"
  - label: "Save anyway"
    description: "Proceed despite validation warnings"
  - label: "Cancel"
    description: "Don't save the note"
```

**IF no issues:** Log "✓ Validation passed" and proceed.

### Phase 6: Save Note

Generate slug inline: lowercase title, replace spaces with hyphens, remove special characters.
Example: `"Superhuman Is Built for Speed"` → `superhuman-is-built-for-speed`

Save to `content/{slug}.md`. Confirm with link density status:

```text
✓ Note saved: content/{slug}.md
  - Type: {type}
  - Authors: {author-slugs}
  - Tags: {tag-count} tags
  - Wiki-links: {link-count} connections ({status})
    - [[link-1]] (why: {context})
    - [[link-2]] (why: {context})
```

**Link density status:**
- `{link-count} >= 3`: "well-connected"
- `{link-count} = 1-2`: "connected"
- `{link-count} = 0`: "standalone" (fine when no genuine connections exist)

### Phase 7: MOC Placement (Non-blocking)

#### 7.1 Suggest Existing MOC Placement

```bash
python3 .claude/skills/moc-curator/scripts/cluster-notes.py --mode=for-note --note={slug}
```

If suggestions score >= 0.7, present to user. Apply selections to MOC's `## Suggested` section.

#### 7.2 Check MOC Creation Threshold

After saving, check if any of the note's tags exceed the threshold:

```bash
# For each tag on the new note, count notes with that tag
Grep pattern: "tags:.*{tag}" glob: "content/*.md" output_mode: "count"
```

**IF tag count >= 15 AND no existing MOC for that tag:**

```yaml
question: "The tag '{tag}' now has {count} notes. Would you like to create a MOC?"
header: "MOC Opportunity"
multiSelect: false
options:
  - label: "Create MOC"
    description: "Generate a '{tag}' guide/roadmap to organize these notes"
  - label: "Skip for now"
    description: "Don't create a MOC yet"
```

If "Create MOC" selected: Invoke moc-curator skill with `--mode=new-clusters --tag={tag}`.

### Phase 8: Quality Check

Run linter and type check to catch any issues:

```bash
pnpm lint:fix && pnpm typecheck
```

If errors are found, fix them before completing the task.

---

## Error Handling

| Error | Recovery |
|-------|----------|
| Metadata agent fails | Prompt for manual entry or WebFetch fallback |
| Transcript unavailable | Note "No transcript available" in body |
| Author not found online | Create minimal profile (name only) |
| Reddit 429 | Wait 60s and retry |
| Semantic analysis timeout | Proceed without wiki-link suggestions |
| Validation crash | Warn user, recommend manual check |

---

## Reference Files

| File | Purpose |
|------|---------|
| `references/author-creation.md` | Author profile workflow |
| `references/diagrams-guide.md` | When/how to add mermaid diagrams |
| `references/code-extraction.md` | Technical content code snippets |
| `references/podcast-profile-creation.md` | Creating podcast show profiles |
| `references/newsletter-profile-creation.md` | Creating newsletter publication profiles |
| `references/content-types/*.md` | Type-specific templates and handling |
