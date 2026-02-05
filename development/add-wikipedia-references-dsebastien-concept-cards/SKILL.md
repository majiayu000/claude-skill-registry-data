---
name: add-wikipedia-references
description: Add Wikipedia reference links to concepts that don't have one. Searches for relevant Wikipedia articles and adds them to the references array.
allowed-tools: Bash, Read, Edit, Grep, Glob, WebSearch, WebFetch, mcp__playwright__browser_navigate, mcp__playwright__browser_snapshot, mcp__playwright__browser_close
---

# Add Wikipedia References to Concepts

This skill adds Wikipedia reference links to concept cards that are missing them. It searches for relevant Wikipedia articles and adds them to the concept's `references` array.

## When to Use

- When you want to enrich concepts with authoritative Wikipedia references
- After bulk-importing concepts that lack references
- To improve the quality and credibility of concept cards

## Prerequisites

- Concepts are stored in `/home/dsebastien/wks/concept-cards/src/data/concepts/`
- Each concept is a JSON file with a `references` array

## Step-by-Step Process

### Step 1: Find Concepts Without Wikipedia References

Run these commands to find concepts that don't have a Wikipedia reference:

```bash
# List concepts without Wikipedia references (using grep -L for "files without match")
grep -L '"url": "https://en.wikipedia.org' /home/dsebastien/wks/concept-cards/src/data/concepts/*.json | xargs -n1 basename | sed 's/.json$//'

# Count concepts without Wikipedia references
grep -L '"url": "https://en.wikipedia.org' /home/dsebastien/wks/concept-cards/src/data/concepts/*.json | wc -l

# Get first 20 concepts without Wikipedia (for batch processing)
grep -L '"url": "https://en.wikipedia.org' /home/dsebastien/wks/concept-cards/src/data/concepts/*.json | head -20 | xargs -n1 basename | sed 's/.json$//'
```

### Step 2: For Each Concept, Search Wikipedia

For each concept without a Wikipedia reference:

1. **Read the concept file** to get the name and aliases
2. **Search Wikipedia** using the concept name (and aliases if needed)
3. **Verify the article is relevant** - the Wikipedia article should match the concept's meaning

#### Search Strategy

1. **Primary search**: Use the exact concept name
   - Example: Concept "Atomic Notes" → Search "Atomic Notes wikipedia"

2. **Fallback searches** (if primary fails):
   - Try aliases: "Evergreen Notes wikipedia"
   - Try broader terms: "Note-taking method wikipedia"
   - Try the concept with context: "Atomic Notes Zettelkasten wikipedia"

3. **Wikipedia URL patterns**:
   - Standard: `https://en.wikipedia.org/wiki/Article_Name`
   - With underscores: `https://en.wikipedia.org/wiki/Article_Name_Here`

### Step 3: Verify the Wikipedia Article

Before adding a reference, verify:

1. **The article exists** - Navigate to the URL or fetch it
2. **The article is relevant** - It should describe the same concept
3. **The article is specific enough** - Prefer specific articles over general ones

#### Common Pitfalls

- **Disambiguation pages**: If you land on a disambiguation page, choose the most relevant article
- **Redirects**: Wikipedia may redirect to a differently-named article - use the final URL
- **Different meanings**: Some terms have multiple meanings - ensure the article matches your concept's domain (e.g., "Flow" in psychology vs. physics)

### Step 4: Add the Reference

Edit the concept JSON file to add the Wikipedia reference to the `references` array:

```json
{
  "references": [
    {
      "title": "Article Name - Wikipedia",
      "url": "https://en.wikipedia.org/wiki/Article_Name",
      "type": "website"
    }
  ]
}
```

#### Reference Format Rules

- **title**: Use format `"Article Name - Wikipedia"`
- **url**: Use the canonical Wikipedia URL (with underscores, not encoded)
- **type**: Always `"website"`

### Step 5: Handle Edge Cases

#### No Wikipedia Article Exists

If no relevant Wikipedia article exists for a concept:
- Skip the concept
- Log it for reference
- Consider searching for related concepts that might have articles

#### Multiple Relevant Articles

If multiple Wikipedia articles are relevant:
- Add the most specific/relevant one
- Optionally add others as additional references

#### Concept is Too Niche

Some concepts may be too specific for Wikipedia:
- Personal productivity methods (e.g., specific journaling techniques)
- Proprietary frameworks
- Very recent concepts

In these cases, skip the concept.

## Batch Processing

For processing multiple concepts efficiently:

### Option A: Process in Batches

```bash
# Get first 20 concepts without Wikipedia references
grep -L '"url": "https://en.wikipedia.org' /home/dsebastien/wks/concept-cards/src/data/concepts/*.json | head -20 | xargs -n1 basename | sed 's/.json$//'

# Get concepts 21-40 (skip first 20)
grep -L '"url": "https://en.wikipedia.org' /home/dsebastien/wks/concept-cards/src/data/concepts/*.json | tail -n +21 | head -20 | xargs -n1 basename | sed 's/.json$//'
```

Then process each concept using the steps above.

### Option B: Use Sub-Agents

For large batches, spawn sub-agents to process concepts in parallel:
- Each sub-agent handles 5-10 concepts
- Sub-agents search Wikipedia and update files
- Main agent coordinates and verifies

## Example Workflow

### Example 1: Adding Wikipedia to "pomodoro-technique"

1. **Read concept**:
   ```bash
   cat /home/dsebastien/wks/concept-cards/src/data/concepts/pomodoro-technique.json
   ```

2. **Search Wikipedia**:
   - Search: "Pomodoro Technique wikipedia"
   - Found: `https://en.wikipedia.org/wiki/Pomodoro_Technique`

3. **Verify**: The article describes the same time management technique

4. **Edit the file**:
   ```json
   "references": [
     {
       "title": "Pomodoro Technique - Wikipedia",
       "url": "https://en.wikipedia.org/wiki/Pomodoro_Technique",
       "type": "website"
     }
   ]
   ```

### Example 2: Concept with No Wikipedia Article

1. **Concept**: "progressive-summarization"
2. **Search**: "Progressive Summarization wikipedia" → No results
3. **Fallback**: "Tiago Forte Progressive Summarization" → No Wikipedia article
4. **Decision**: Skip - this is a proprietary method without a Wikipedia entry

## Verification

After adding references, verify the build succeeds:

```bash
npm run build 2>&1 | tail -10
```

## Tips for Efficiency

1. **Process alphabetically** to track progress easily
2. **Use WebSearch** to find Wikipedia URLs quickly
3. **Batch similar concepts** (e.g., all psychology concepts together)
4. **Skip obvious misses** - proprietary methods, very recent concepts
5. **Use Playwright** for disambiguation pages or to verify article content

## Reference Quality Guidelines

- **Prefer English Wikipedia** (`en.wikipedia.org`)
- **Use canonical URLs** (not mobile, not shortened)
- **Verify article stability** - well-established articles are better than stubs
- **Match the concept's domain** - "Flow" should link to Flow (psychology), not Flow (physics)
