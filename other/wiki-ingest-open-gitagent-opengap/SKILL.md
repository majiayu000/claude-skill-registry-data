---
name: wiki-ingest
description: "Ingest a raw source document into the wiki. Reads the source, extracts key information, creates or updates wiki pages, maintains cross-references, and logs the operation. Use when the user adds a new source or says 'ingest this'."
allowed-tools: Read Write Edit Glob Grep
---

# Wiki Ingest

Process a new source document and integrate its knowledge into the wiki.

## Workflow

### Step 1: Read the source
Read the full source document from `knowledge/`. Identify:
- Key entities (people, organizations, concepts, technologies)
- Main claims and findings
- Relationships between entities
- Data points and statistics
- Contradictions with or confirmations of existing knowledge

### Step 2: Discuss with the user
Before writing, share a brief summary of key takeaways. Ask:
- What aspects to emphasize?
- Any entities or concepts to prioritize?
- Should this update existing pages or create new ones?

### Step 3: Update the wiki
For each significant entity or concept found in the source:

1. **Check if a wiki page exists** — read `memory/wiki/index.md`
2. **If page exists** — read it, integrate new information, update the "Sources" section, update frontmatter `updated` date and `source_count`
3. **If page doesn't exist** — create a new page in `memory/wiki/` with proper frontmatter, content, and source citations
4. **Update cross-references** — add `[[wikilinks]]` in both directions between related pages

### Step 4: Write a source summary page
Create `memory/wiki/sources/<source-name>.md` with:
- One-paragraph summary
- Key claims extracted
- Entities mentioned (with wikilinks to their pages)
- Date ingested

### Step 5: Update index and log
1. Update `memory/wiki/index.md` — add/update entries for all pages touched
2. Update `knowledge/index.yaml` — ensure the source is cataloged with tags and priority
3. Append to `memory/log.md`:
   ```
   ## [YYYY-MM-DD] ingest | Source Title
   - Pages created: [list]
   - Pages updated: [list]
   - Key findings: [1-2 sentences]
   ```

## Example

User drops `knowledge/quantum-computing-review-2026.pdf` and says "ingest this".

1. Read the paper, identify entities: quantum computing, error correction, IBM, Google, topological qubits
2. Discuss key findings with user
3. Create/update: `quantum-computing.md`, `error-correction.md`, `ibm.md`, `google.md`
4. Create: `sources/quantum-computing-review-2026.md`
5. Update `index.md` with all new/updated pages
6. Append ingest entry to `log.md`

A single source might touch 5-15 wiki pages. This is normal and expected.
