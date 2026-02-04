---
name: learning-system
description: Process learning resources from markdown files, extract content, identify clusters, and create Ship-Learn-Next learning paths
triggers:
  - "process learning inbox"
  - "process learning from"
  - "create learning paths"
---

# Learning System

## Purpose
Transform collected learning resources (URLs + notes) into structured Ship-Learn-Next learning paths.

## Usage

Call this skill with a markdown file containing learning resources:
```
process learning from AI/Inbox.md
```

The file can contain:
- YouTube URLs
- Web article URLs
- PDF file paths
- Your own notes and thoughts about topics
- Any mix of the above

## Workflow

### Phase 1: Parse & Extract

1. **Read the inbox file**
   - Parse markdown content
   - Identify URLs (YouTube, web articles)
   - Extract user notes (text content, bullet points)
   - Report summary: "Found X YouTube videos, Y articles, Z paragraphs of notes"

2. **Extract content from URLs**
   - For YouTube URLs: Call `youtube-transcript` skill
   - For web article URLs: Call `article-extractor` skill
   - For PDF paths: Read and extract text directly
   - Process in parallel where possible
   - Report failures gracefully: "Extracted X/Y sources (Z failed)"
   - Continue processing even if some extractions fail

### Phase 2: Analyze & Cluster

3. **Unified analysis**
   - Analyze ALL content together:
     * Extracted transcripts and articles
     * User's original notes
     * Context from markdown structure (headings, sections)

4. **Identify learning clusters**
   - Look for topic patterns and themes
   - Group related sources together
   - Consider user's notes as strong signals for clustering
   - Create proposed clusters with:
     * Suggested cluster name
     * List of URLs belonging to cluster
     * List of user notes related to cluster
     * Rationale for grouping

### Phase 3: Interactive Approval

5. **Present clusters one by one**
   - For each cluster, show:
     ```
     Cluster: "[Suggested Name]"

     Sources:
     - YouTube: "[Title]" (transcript available)
     - Article: "[Title]" (from [domain])
     - Your note: "[first 100 chars...]"

     Rationale: [Why these are grouped together]

     Options:
     1. Approve as-is
     2. Rename cluster
     3. Split into multiple topics
     4. Merge with another cluster
     5. Exclude some sources
     ```

6. **Handle user feedback**
   - Listen for natural language responses:
     * "Approve" / "looks good" → Accept cluster
     * "Rename to [X]" → Change cluster name
     * "Split - [reason]" → Divide cluster
     * "Merge with cluster N" → Combine clusters
     * "Remove [source]" → Exclude specific item

   - Apply changes immediately and confirm
   - Continue to next cluster
   - Keep track of all decisions

7. **Final confirmation**
   - Show summary of all approved clusters
   - Confirm: "Ready to create N learning paths in 3_Resources/?"
   - Wait for explicit approval

### Phase 4: Create Learning Paths

8. **Check for existing paths**
   - For each cluster, check if `3_Resources/[topic-name]/` exists
   - If exists: This is a MERGE operation (add to existing path)
   - If new: This is a CREATE operation

9. **Create folder structure**
   - For NEW paths:
     ```
     3_Resources/[topic-name]/
     ├── README.md              # Ship-Learn-Next plan
     ├── sources/               # Extracted content
     │   ├── [source-1].md
     │   └── [source-2].md
     └── notes/                 # User's notes
         └── [note].md
     ```

   - For MERGE operations:
     * Add new source files to `sources/`
     * Add new notes to `notes/`
     * Update README.md with new content

10. **Generate Ship-Learn-Next plan**
    - Use the template from `ship-learn-next-template.md`
    - Fill in:
      * Title: Cluster name
      * Overview: Brief description of learning path
      * Ship section: 3-5 practical projects to build
      * Learn section: Links to all sources and notes
      * Next section: Advanced topics and next steps
      * Topics tags: Extracted keywords
      * Status: "seedling" for new paths

    - For MERGE: Update existing sections intelligently:
      * Add new items to Ship/Learn sections
      * Update "Last Updated" date
      * Preserve existing progress tracking

11. **Save extracted content**
    - For each source, create markdown file in `sources/`:
      ```markdown
      ---
      source: [original URL]
      type: [youtube/article/pdf]
      title: [extracted title]
      extracted: [date]
      ---

      # [Title]

      [Extracted content]
      ```

    - For user notes, create file in `notes/`:
      ```markdown
      ---
      from: [original inbox file]
      extracted: [date]
      ---

      [User's note content]
      ```

12. **Handle multi-topic sources**
    - If a source belongs to multiple clusters:
      * Save full content in PRIMARY cluster (user specified during approval)
      * Add reference link in SECONDARY clusters:
        ```markdown
        ## Related Resources
        See also: [[../[primary-topic]/sources/[file]|[Title]]]
        ```

### Phase 5: Cleanup & Tracking

13. **Update inbox file**
    - Move processed items to "## Processed (DATE)" section
    - Mark with `[x]` checkboxes
    - Add path reference: `→ [topic-name]`
    - Example:
      ```markdown
      ## Processed (2025-11-22)
      - [x] https://youtube.com/watch?v=abc → kubernetes-networking
      - [x] My notes about service mesh → kubernetes-networking
      ```
    - Preserve unprocessed items in original location

14. **Update resources index**
    - Add new learning paths to `3_Resources/index.md`
    - Format:
      ```markdown
      - [[kubernetes-networking/README|Kubernetes Networking]] 🌱 seedling
      ```
    - For merged paths: Update "Last Updated" timestamp

15. **Generate summary report**
    ```
    ✅ Processing Complete!

    Created 2 new learning paths:
    - 3_Resources/kubernetes-networking/ (3 sources, 1 note)
    - 3_Resources/rust-async/ (2 sources, 2 notes)

    Merged into 1 existing path:
    - 3_Resources/llm-agents/ (+2 sources)

    Processed: 7/8 sources
    Failed: 1 (paywalled article - saved URL for manual review)

    Next steps:
    - Review learning plans in 3_Resources/
    - Start with "Ship" sections for hands-on learning
    - Update progress as you learn
    ```

## Error Handling

### Extraction Failures
- If YouTube transcript unavailable:
  * Report in summary
  * Save URL in learning path with note: "⚠️ Transcript unavailable - watch manually"
  * Continue processing

- If article blocked/paywalled:
  * Report in summary
  * Save URL with note: "⚠️ Manual extraction needed"
  * Continue processing

- If PDF unreadable:
  * Report in summary
  * Save file path with note: "⚠️ Text extraction failed"
  * Continue processing

### Clustering Issues
- If sources too diverse (no clear clusters):
  * Report: "Sources are too diverse for automatic clustering"
  * Offer: "Create individual learning paths for each source?" or "Group all into 'Mixed Topics' for manual organization?"
  * Let user decide

- If only 1-2 sources:
  * Still create learning path but note it's minimal
  * Suggest: "This is a small learning path - consider collecting more resources before studying"

### Ambiguous Classifications
- If source could fit multiple topics equally:
  * Present during approval: "This resource covers both X and Y equally - which should be primary?"
  * Wait for user decision
  * Apply primary/secondary reference strategy

### Existing Path Collisions
- ALWAYS merge into existing paths
- Report: "Merged X new sources into existing [topic-name]/"
- Show what was added in summary

## Best Practices

1. **Process regularly**: Run weekly or when you have 5+ resources collected
2. **Add context**: Include your thoughts in the inbox - helps clustering
3. **Review plans**: The generated Ship-Learn-Next plans are starting points - refine them
4. **Update progress**: Check off items as you learn, update completion %
5. **Merge related paths**: If you later realize two paths should be one, manually merge folders
6. **Archive completed**: Move finished learning paths to `4_Archives/resources/`

## Technical Notes

- Depends on: `youtube-transcript` and `article-extractor` skills
- Creates folders with kebab-case naming (e.g., `kubernetes-networking`)
- Uses Obsidian wikilinks for cross-references
- Compatible with Dataview queries for tracking
- Preserves frontmatter for metadata management
- Status progression: seedling 🌱 → sapling 🌿 → evergreen 🌳 (update manually as path matures)

## Example Session

```
User: process learning from AI/Inbox.md