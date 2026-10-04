---
name: sync-inspiration
description: "Pull quick-capture notes from all files in inspiration-inbox/ into the shared raw-ideas/ library. Fetches any URLs found, researches the content, and writes a synthesized idea file with a proper title and context. Use when the user says /sync-inspiration, 'sync my notes', 'sync the inbox', or 'pull inbox into raw ideas'."
trigger: /sync-inspiration
---

# /sync-inspiration

Promotes rough notes from every file in `inspiration-inbox/` into the shared, immutable `raw-ideas/` library, one file per idea. When a chunk contains URLs, it fetches and researches each link, synthesizes the key insights, and writes a rich idea file — not just a dump of the raw text.

It also promotes notes Altaf has already flagged in his personal knowledge vault (see "Vault source
path" below) straight into `raw-ideas/`, with no re-fetch, since the vault already did the fetch and
the synthesis.

## Config

- `VAULT_ROOT`: `/Users/altaf.shaikh/Code-Space/AI/knowledge-vault`. This is the only place this path
  is written; every step below refers to it as `VAULT_ROOT`.

## Steps

1. List all files in `inspiration-inbox/`. Process every file found — not just `inbox.md`. If the folder is empty or every file has no real content, report "inbox is empty" and stop.
2. For each file:
   - If it is `inbox.md`: ignore the leading HTML comment header. Treat the rest as content.
   - For all other files: read the full content as-is.
   - Skip files that are blank or whitespace-only after stripping any header comment.
3. Within each file, split content into idea chunks on lines containing only `---`. A file with no `---` is a single idea. Discard chunks that are blank/whitespace-only.
4. Find the next available numeric prefix: list `raw-ideas/*.md` filenames matching `NNN-*.md`, take the highest `NNN`, add 1 (zero-padded to 3 digits). Start at `001` if none exist.
5. For each idea chunk across all files, in order:
   a. **Detect URLs.** Scan the chunk for any `http://` or `https://` links.
   b. **If the source is a folder** (contains images/screenshots alongside a links.txt or similar): read all image files using the Read tool to extract visual content, read any text files for links or notes, then synthesize everything together.
   c. **If URLs are present:**
      - Fetch each URL using WebFetch. Read the page content thoroughly.
      - If a URL is a social media post (X/Twitter, Instagram, LinkedIn), extract: the post text, any key claim or hook, what makes it interesting or shareable.
      - Synthesize the fetched content into a coherent idea: what is being shown, what is the insight, why would an audience care.
      - Generate a descriptive title and a short kebab-case slug from the synthesized idea (not from the raw URL).
      - Write the idea file with:
        - A `# Title` heading (human-readable, descriptive)
        - A `## Context` section with the synthesized insight in plain prose — what you found, what it demonstrates, what the angle is
        - A `## Source` section listing the original URLs verbatim
        - A `## Inspiration` section with the relative path to the source folder (e.g. `../inspiration-inbox/inspiration 1/`) so channel agents can read the original screenshots and materials directly
   d. **If no URLs are present:**
      - Write the chunk's text **verbatim** — do not rewrite, expand, or clean up the wording.
      - Generate a short kebab-case slug from the chunk's content (gist of the first line or two).
   e. Write to `raw-ideas/NNN-slug.md` using the next available prefix, then increment for the next chunk.
6. Once all chunks from a file are written:
   - If it is `inbox.md`: reset it back to just the header comment (empty otherwise).
   - For all other files (including folders): **do NOT delete them.** They are kept as supporting material. Channel agents can read the original screenshots and files when generating posts.
7. Report which new `raw-ideas/` files were created and a one-line summary of each.

## Vault source path

A third source, alongside `inspiration-inbox/`. Runs every time `/sync-inspiration` runs.

1. Search `VAULT_ROOT/notes/sources/`, `VAULT_ROOT/notes/concepts/`, and `VAULT_ROOT/notes/entities/`
   for pages whose frontmatter has `promote: yes`. This flag is Altaf's alone, set in Obsidian —
   never set or clear it yourself except in step 4 below.
2. If none are flagged, skip this source entirely (no report line needed for an empty vault pass).
3. For each flagged note, take the no-fetch path — the note has already been fetched and
   synthesized by the vault's own ingest workflow, so **never WebFetch its `raw_source` or any URL
   in it**:
   - Read the note's frontmatter for `title`, `topic`, and `raw_source` (or a URL if the note
     carries one directly).
   - Generate a kebab-case slug from the title (not from the raw filename).
   - Write `raw-ideas/NNN-slug.md` using the same next-available-prefix rule as the inbox path
     (one shared counter across both sources) with:
     - A `# Title` heading from the note's `title`.
     - A `## Context` section carrying the note's own body forward verbatim in substance — its
       existing synthesis, not a re-synthesis. Keep its `[[wiki-link]]` cross-links inline so a
       channel agent can trace them back into the vault, and note its `topic:` at the top of the
       section (e.g. `topic: ai-engineering`).
     - A `## Source` section with the note's `raw_source` (or URL, if present).
   - Apply the strip rule (below) to the written file before it is saved.
4. After a successful write, edit the vault note's frontmatter in place: replace `promote: yes`
   with `promoted: <ISO date>`. This is a write into `VAULT_ROOT/notes/`, which is mutable content
   under the vault's own schema; never touch `VAULT_ROOT/raw/`. This is what stops the same note
   from promoting twice.
5. Report each vault-sourced `raw-ideas/` file created, same one-line-per-idea format as the inbox
   path, tagged `(from vault)`.

`inspiration-inbox/` keeps working exactly as it does today — this is an additional source, not a
replacement.

## Rules

- Never edit or remove existing files in `raw-ideas/` — it's append-only.
- For URL-based ideas: the synthesized context is your judgment call — write it as insight, not a summary of the webpage.
- For plain-text ideas: verbatim only; slug generation is the only judgment call.
- For vault-sourced ideas: never re-fetch or re-synthesize — the vault note's own content is the
  source of truth; only the strip rule may change its wording.
- No em dashes in any written content. Use plain punctuation or rewrite as two sentences.
- Strip rule: no company names and no internal tool names in anything written to `raw-ideas/`
  (applies to all three sources, not just the vault path).
