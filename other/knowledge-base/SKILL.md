---
name: knowledge-base
description: Personal knowledge base manager. Processes inbox files (PDF, MD, DOCX, RTF, TXT, HTML, PNG, URL), extracts metadata, renames with citation conventions, generates summaries, maintains a generated searchable index, answers questions grounded in indexed sources, performs full-text keyword search, reports corpus health, moves pipeline output into topic folders, and builds slide decks from indexed or external content through the slides-content and beamer skills. Triggers on "kb", "knowledge base", "process inbox", "kb ask", "kb move", "kb search", "kb find", "kb status", "kb health", "kb slides", "slides from kb", and "build slides from".
when_to_use: Use when the user invokes one of the kb commands or otherwise wants to work the knowledge base, whether that is processing the inbox, asking a question answered from indexed sources, running a keyword search over the corpus, moving pipeline output into a topic folder, checking corpus health, or building slides from indexed or external content. Use knowledge-base-update instead for "kb update" and "kb sync", which resync the generated index and report health rather than adding new material.
allowed-tools: Bash(python*), Bash(pip*), Bash(ls*), Bash(mv*), Bash(cp*), Bash(mkdir*), Bash(find*), Bash(wc*), Bash(file*), Bash(export*), Bash(grep*), Bash(rm -rf *_build/split_*), Bash(kb-index*), Bash(kb-search*), Bash(kb-dup-check*), Bash(kb-status*), Bash(kb-recents*), Bash(kb-fetch-url*), Read, Write, Edit, Glob, Grep, WebFetch, WebSearch, Agent, Skill
model: opus
effort: high
---

# Knowledge Base Manager

## Knowledge Base Location

**Edit the path on the line below to match where your knowledge base lives.** That line is the single place the root is configured; this skill reads no environment variable for it, and there is nothing else to set.

```
~/knowledge-base/
```

Written as `<knowledge-base-root>` where a placeholder reads more clearly. All paths in this skill are relative to this root unless otherwise specified.

**The only deletion this skill performs is the split folder that Mode 1 Step 4a removes.** The `rm` entry in `allowed-tools` is scoped to exactly that path shape (`*_build/split_*`) and grants nothing broader; every other cleanup is a `mv`.

## Directory Structure

The knowledge base supports two document storage patterns:

### Pattern A: Per-document subfolder (default for all filing)

Every filed document gets its own subfolder containing the source, text extraction, summary, and any slides or build artifacts. This is the default for inbox processing (Mode 1), `kb move` (Mode 3), and the content-skill pipelines that write into the knowledge base.

```
knowledge-base/
├── AI-articles/
│   ├── 2026-01-28 Payrolls to Prompts.../     <- per-document subfolder
│   │   ├── Payrolls to Prompts...2026-01-28.pdf
│   │   ├── Payrolls to Prompts...2026-01-28_text.md
│   │   ├── Payrolls to Prompts...2026-01-28_summary.md
│   │   ├── Payrolls to Prompts...2026-01-28_slides.pdf
│   │   └── Payrolls to Prompts...2026-01-28_build/
│   └── 2026-02 Chaining Tasks.../
```

### Pattern B: Flat files (legacy, still readable)

Older items have the source, text, and summary sitting side by side in the topic folder. **Pattern B is no longer produced by new filing, but every reader (the search index, `aa-recents/`, and Q&A) still handles it,** so legacy flat items stay fully functional. When a slides skill generates slides for a flat item, that skill promotes it to Pattern A by creating a per-document subfolder and moving the existing files into it.

```
knowledge-base/
├── AI-teaching/
│   ├── 2026-03-18 Ipeirotis. Scalable Oral Assessments.pdf
│   ├── 2026-03-18 Ipeirotis. Scalable Oral Assessments_text.md
│   ├── 2026-03-18 Ipeirotis. Scalable Oral Assessments_summary.md
│   └── AI-teaching_build/
│       └── split_2026-03-18 Ipeirotis/
```

### Full structure

```
knowledge-base/
├── aa-inbox/                     <- Drop files here for processing (required)
├── aa-recents/                   <- Generated symlink view of the newest items (required)
├── other-articles/               <- Overflow folder: anything with no clear topic fit (required)
├── AI-articles/                  <- Topic folders (create as needed; at least one)
├── AI-teaching/                  <-   names are examples, not a fixed list
├── aa-blog/                      <- Optional: drop your own blog posts here for processing
├── aa-slides-inbox/              <- Optional: drop folder for unattended slide builds
├── index.md                      <- Generated document index, never hand-edited (required)
└── topics.md                     <- Topic descriptions, one section per folder (required)
```

**The five required entries are created at installation** (README, Installation). A run with no topic folder and no overflow folder has nowhere legal to file anything, because Mode 1 Step 5 never auto-creates a folder; and a missing `index.md` makes every membership `grep` error instead of returning nothing.

**`aa-recents/` holds symlinks, not documents.** Mode 1 Step 5 rebuilds it after each filing run: the most recently processed items, ranked by the `ingested:` date in each `_summary.md`, named `NN - folder - basename.md`. It is a browse convenience. Nothing else reads it, so a knowledge base whose recents folder is stale or empty is still fully correct.

**`aa-blog/` is optional** and exists only if you file your own writing; Blog Post Processing in `references/inbox.md` covers it. **`aa-slides-inbox/` is optional too, and this skill never writes to it.** It is the conventional drop folder for an unattended slide queue you supply (`references/slides-headless.md`), watched by that queue rather than by anything here. Create it only if you build one; `kb status` counts its backlog when it exists and passes over it silently when it does not.

**Topic folders are dynamic.** The skill does not maintain a hardcoded list. Any immediate subdirectory of `knowledge-base/` (other than `aa-inbox/`, `aa-blog/`, `aa-recents/`, `aa-slides-inbox/`, an optional full-text search folder such as `aa-search/`, an optional documentation folder that describes the system itself, and `*_build/`) is treated as a topic folder. Adding a new folder requires no skill or config changes; running the [knowledge-base-update](../knowledge-base-update/) skill will discover it automatically.

**Reference material (`materials/` subfolders):** Any subfolder named `materials/` at any depth inside the knowledge base holds reference items that are not indexable content (third-party documentation, working notes, external project artifacts). Mode-specific behavior:
- **Inbox processing (Mode 1) and Move Project (Mode 3):** never file items into `materials/`. Treat it as not a valid destination. Items that belong there are placed by hand, not by the pipeline.
- **Q&A (Mode 2):** include `.md` files from `materials/` when scanning for relevant sources. Do not read binary files from `materials/` (PDF, images, Office documents). When citing a materials source, note it as reference material rather than an indexed entry.
- **Index generation and the full-text reindex:** skip `materials/` entirely (no index rows, no health warnings).

**Conventions:**
- Both patterns are valid; the index treats them identically.
- When scanning for documents, search both `<topic-folder>/*_summary.md` (flat) and `<topic-folder>/*/*_summary.md` (subfolder). Also check for `_text.md` files as the engagement artifact.
- The `aa-inbox/` folder is the ingestion point for new unprocessed content.
- Summary or slides skills can run directly in topic folders; they do not need to go through inbox.
- Topic folders are created by the user; the skill suggests but does not create them without approval.

## Helper commands

This skill delegates its mechanical work to small scripts you supply, so that no step depends on a model remembering to do bookkeeping. Wire each one behind the name used throughout this skill; any implementation meeting the contract works. Each is deterministic and costs no model time.

| Command | Contract | If you have not built it |
|---|---|---|
| `kb-index` | Walk the knowledge base and regenerate `index.md` from every `_summary.md`'s frontmatter. Atomic write, guarded by a count floor so a partial walk cannot truncate the index. Prints warnings (missing frontmatter, topic drift, invalid date, duplicate rows). | Claude regenerates the WHOLE table from frontmatter (see below). |
| `kb-search search <query>` | Ranked full-text hits over `_summary.md` and `_text.md` bodies. See Mode 4. | `grep -ril` over the same files. Cannot rank and cannot filter; say so. |
| `kb-search reindex [--incremental]` | Rebuild the full-text index from current content. | Nothing to rebuild: with no index, `kb search` is the `grep` fallback every time. Skip the step silently. |
| `kb-dup-check "<stem>" [--url <url>]` | Duplicate check on a prospective filename stem. Prints and exits `OK` (0), `DUP` (1), `NEAR` (2), or `ERROR` (3). | Targeted `grep index.md` on the stem, and on the URL when known (see below). No fuzzy `NEAR`. |
| `kb-status` | One-screen corpus health readout. See Mode 6. | Partial: the counts below run, drift and full-text freshness do not. See Mode 6. |
| `kb-recents` | Rebuild the `aa-recents/` symlink folder. See Mode 1 Step 5. | Skip the rebuild and say so once per run. `aa-recents/` is a browse view; nothing reads it. |
| `kb-fetch-url <url> --out <path>` | Mechanically capture a web page to a file and print its metadata. Exit codes are contract; see Mode 1 Step 1. | Fetch with the built-in web fetch tool and save the returned text VERBATIM (see below). |

**These fallbacks are real and named at each call site, with two exceptions stated plainly here rather than left to be discovered.** They are slower and less exact than the scripts, and each carries a caveat worth reading before you rely on it.

- **`kb-index`: regenerate, never hand-edit.** The fallback is Claude walking every `_summary.md` and rendering the entire table from their frontmatter, exactly as the script would, then writing `index.md` in one pass. **That is generation, and it is the correct fallback.** What "generated and never hand-edited" forbids is different: opening `index.md` and changing, adding, or deleting an individual row, which makes that row disagree with the summary nothing knows was edited. The test is whether the whole file was rebuilt from the summaries (allowed) or one row was touched in place (never). To change a row either way, edit the item's frontmatter and regenerate.
- **`kb-dup-check`: a targeted `grep`, which is not the read the prohibition forbids.** Run `grep -i -F "<stem>" index.md`, and `grep -i -F "<url>" index.md` as well when the item's URL is known. A hit is a `DUP` (show the matched row), no hit is an `OK`, and a grep that cannot run, because `index.md` is missing or unreadable, is an `ERROR`. There is no fallback for `NEAR`: fuzzy matching needs the script, so a knowledge base without it detects exact duplicates and not near ones, which is worth saying once in the run report. **The rule "never eyeball-compare against a whole-file `index.md` read" bans reading the index into context and judging by eye; a `grep` for one stem reads one line back and is the sanctioned substitute.**
- **`kb-fetch-url`: fetch mechanically, and never write the body yourself.** With no script, fetch the page with the built-in web fetch tool and save what it returns to the output path verbatim, then add the `extract_note:` disclosure Mode 1 Step 1 requires for any non-script capture. **Saving retrieved text verbatim is legal. Composing the source's body is not, and no absence of a script authorizes it:** writing prose assembled from search results into the source file is the one thing `references/inbox.md` prohibits outright, because downstream skills read that file as the publication. Without the script you also lose the exit code that sets `source_basis` mechanically, so set it by the rules in Mode 1 Step 1 instead: `partial` when what came back is visibly a fragment, `excerpts` only on a reconstruction after nothing could be captured, and absent otherwise.
- **`kb-status`: partial, and Mode 6 says which half is missing.** Inbox backlog counts and an index row count run without it; index-versus-full-text drift and full-text freshness do not, because both compare against a database the script owns.
- **`kb-recents`: no fallback, and no consequence.** Building the symlink set by hand is not worth the steps. Skip the rebuild, note it once in the run report, and leave `aa-recents/` as it is. Every other reader (the index, search, and Q&A) walks topic folders directly.

## Modes

**Index-first gate (lookups and membership questions).** Any request to find, locate, recall, or check whether something is in the knowledge base (whether phrased as `kb ask`, `kb search`, "is X in my kb?", "what do I have on X?", or an informal question) MUST begin by consulting the index before reading or scanning topic folders directly. Run `kb search <terms>`, and `grep index.md`. Direct folder browsing is a fallback only, used after the index returns nothing relevant. Never answer a lookup from a folder scan you ran before checking the index.

**Read exactly one mode file.** The modes are mutually exclusive on any one run. Read this file plus the row that matches the invocation, and **do not read the other mode files**; they describe work this run is not doing.

| Invocation | Mode | Read |
|---|---|---|
| `kb`, `process inbox` | 1. Process Inbox | `references/inbox.md` |
| `kb ask <question>` | 2. Q&A | `references/qa.md` |
| `kb move <dir> <topic>`, "file this in `<topic>`" | 3. Move Project | `references/move.md` |
| `kb search <query>`, `kb find <query>` | 4. Search | inline below |
| `kb slides <target>`, `slides from kb`, `build slides from` | 5. Slides | `references/slides.md` |
| `kb slides <path> headless`, `mode=headless` | 5. Slides, headless | `references/slides.md`, then `references/slides-headless.md` |
| `kb status`, `kb health` | 6. Status | inline below |

**Mode 5 is the one mode that may need a second mode file.** Its Step 2 file-first cases invoke Mode 1, and its file-after step invokes Mode 3; `references/slides.md` states at each point whether to open `references/inbox.md` or `references/move.md`, and when not to. No other mode opens a second file.

### 1. Process Inbox (`/kb` or "process inbox"): read `references/inbox.md`

Mode 1 lives in **`references/inbox.md`**: the processing levels and the companion-`.txt` convention, the agent-per-item architecture and its Flow, the subagent model and effort table, Step 1 (file-type routing, the visual-content check, the source-fetch failure rule), Step 4 (`_text.md` and the summary), Step 5 (filing, the index, `aa-recents/`, the search refresh, the report and rate-usage formats), Correcting a filing, and Blog Post Processing.

On any inbox invocation, **read `references/inbox.md` now and follow it in full.** Every reference elsewhere in this skill to a Mode 1 step, to the Flow, to Correcting a filing, or to Blog Post Processing resolves into that file, except three blocks held here because more than one mode needs them: Citation metadata and naming (below), The frontmatter block (below), and Index Format. **In Mode 5, read it only where `references/slides.md` Step 2 says to. Skip it entirely in Modes 2, 3, 4, and 6.**

### 2. Q&A (`/kb ask [question]` or "kb ask"): read `references/qa.md`

Mode 2 lives in **`references/qa.md`**: the mandatory index-first consult, source selection including the `materials/` markdown rule, answer synthesis and its citation and provenance requirements, and the optional save-the-answer step. On a `kb ask` invocation, **read `references/qa.md` now and follow it in full.** It writes the frontmatter block held in this file, not a copy of its own. **Skip it in every other mode.**

### 3. Move Project (`kb move <source_dir> <topic>`): read `references/move.md`

Mode 3 lives in **`references/move.md`**: the `materials/` refusal, Step 1 (inventory and the artifact pattern table), Step 2 (always Pattern A), Step 3 (renaming and the pre-move duplicate check), Step 4 (the move and its verification), and Step 5 (index, recents, and search refresh). On a `kb move` invocation, **read `references/move.md` now and follow it in full.** Mode 5's file-after step invokes its Steps 3 to 5 and says so at that point. **Skip it in Modes 1, 2, 4, and 6.**

### 4. Search (`kb search <query>`)

Keyword search over the full body of every indexed `_summary.md` and `_text.md`. Use this when the question is "find me everything that touches X" rather than "answer this question." Q&A synthesis is not invoked.

**Triggers:** `kb search <query>`, `kb find <query>`, `search kb for <query>`.

Run:

```bash
kb-search search <query>
```

Optional filters: `--since YYYY[-MM[-DD]]` (items dated on or after; a partial stored date matches as its earliest day, undated items drop out), `--type <t>`, `--source <topic>` (topic folder name). **`--type` takes the values of the `type:` frontmatter field and no others: `paper`, `article`, `web`, `doc`, `blog`, `podcast`, `video`, `report`** (the enum is defined once, under The frontmatter block). `qa-answer` is deliberately not a filter value: those artifacts are `_notes.md` files, never walked by the index generator or the reindexer, so no stored row carries that type. A `grep` fallback cannot filter; with filters active, say so rather than returning unfiltered rows as though they were filtered.

The reference implementation is a local SQLite FTS5 index built from every `_summary.md` and `_text.md` and queried with BM25 ranking; any equivalent full-text indexer works. **Without one, the fallback is `grep -ril "<query>" <knowledge-base-root>/*/*_summary.md <knowledge-base-root>/*/*/*_summary.md`** (add the matching `_text.md` globs to search extractions too). It returns unranked, unfiltered, exact-substring matches, so report it as what it is rather than presenting its output as ranked hits. Each hit from a real index prints date, topic, author, title, type, score, summary and body snippets with the matched terms in `[brackets]`, and the absolute path to the source file.

Relay the ranked output to the user verbatim, plus a one-line interpretation if the top hit is unobvious. Do not synthesize an answer from the snippets; that is `kb ask`'s job.

**When the index is empty or stale:** if the search reports no results and the query terms are common, suggest a full `kb-search reindex` to rebuild from current source content. The rebuild completes in well under a minute at a few hundred documents and costs no model time.

**The index is authoritative; the full-text database is not.** `index.md` is the complete, generated inventory of every document. The full-text database is a derived accelerator that covers only a subset of the corpus: it skips `$`-, `_`-, and `.`-prefixed folders, `*_build`, and `materials/`. A document can be fully catalogued in `index.md` yet absent from the full-text index. Treat a `kb search` miss as "not in the full-text index," never as "not in the knowledge base."

**Membership questions ("is X in the kb?") must consult `index.md` directly.** Before concluding any document is absent, `grep index.md` for the title, author surname, or concept terms. A reindex should also ingest `index.md` itself as a backstop row, so a catalogued term normally surfaces there even when no per-document hit exists; the authoritative check, though, is the `index.md` grep, not the full-text result.

### 5. Slides (`kb slides <target> [beamer] [deck] [lite] [structure=...] [register=...] [plan=...]`): read `references/slides.md`

**The default builds a compiled Beamer PDF through [slides-content](../slides-content/), which runs [beamer](../beamer/).** Both ship alongside this skill, so `kb slides <target>` works on a fresh install with nothing wired and no tokens typed. `beamer` names that same route explicitly.

**`deck` and `lite` are an optional upgrade and need a native PowerPoint generator you supply; none ships here.** Until you replace the `<your deck generator>` placeholder in `references/slides.md` Step 4 with your own generator's skill name, both tokens are refused with a message naming the two ways out, rather than failing partway through a build. The same holds for `headless`, which needs an unattended entry point you supply (`references/slides-headless.md`).

Mode 5 lives in **`references/slides.md`**: generator and tier selection, the optional deck generator and its gate, the outside-source move confirmation, the slide-path model pin, Step 1 (resolve the target), Step 2 (the lite gate and the Case A, B, and C file-first logic with the reuse bar and the grandfather sentinel), Step 3 (existing-slides check), Step 4 (generator handoff and the provenance gate), and Step 5 (post-build sync, the file-after step, and the post-build assertion).

On any slides invocation, **read `references/slides.md` now and follow it in full.** Every reference elsewhere in this skill to Mode 5, to the reuse bar, or to the slide-path model pin resolves into that file. **Skip it in Modes 1, 2, 3, 4, and 6.**

**Headless** (`kb slides <path> headless`, `mode=headless`, or any unattended caller) applies seven overrides to those same Steps 1 to 5; they live in **`references/slides-headless.md`**. Read it after `references/slides.md` when, and only when, the `headless` token is present. **Skip it on every interactive run.**

### 6. Status (`kb status`)

One-screen health readout: index-versus-full-text row drift, full-text freshness and integrity and whether the last build was full or incremental, and inbox backlog counts (`aa-inbox/`, `aa-blog/`, `aa-slides-inbox/`). Read-only; no content reads, no disk walk.

**Triggers:** `kb status`, `kb health`.

Run:

```bash
kb-status
```

**Without the `kb-status` script, Mode 6 runs at half strength and says so.** Two of its four readouts are plain counts and still run: the inbox backlogs (`ls aa-inbox/ | wc -l`, and the same for `aa-blog/` and `aa-slides-inbox/` where they exist) and the index row count (`grep -c '^| ' index.md`, minus the header rows). The other two, index-versus-full-text drift and full-text freshness and integrity, compare against a database the script owns and **cannot be produced by hand: report them as unavailable rather than estimating them.** Say which half ran.

Relay the output verbatim. If it reports drift, suggest `kb-index` followed by `kb-search reindex --incremental`. The deeper judgment-carrying maintenance pass (health check, topics, warnings triage) stays in the [knowledge-base-update](../knowledge-base-update/) skill. The output should include a "largest topics (indexed)" line and warn when any topic reaches a size threshold you set (300 indexed items is a workable default); a warning means it is time to split the topic, by meaning where a real distinction exists and by year otherwise.

## Citation metadata and naming

#### Step 2: Extract citation metadata

For each file, attempt to identify:
- **Date** (publication date, not file date)
- **Author(s)** (last name of first author for filename; full citation for extract)
- **Title**

Search order:
1. Explicit citation block in the document (bibliography entry, header metadata, DOI)
2. Document headers, title page, or first paragraph
3. Filename (if already in `YYYY-MM-DD Author. Title` format, preserve it)
4. Web search using title and author keywords to find the canonical citation
5. If still ambiguous, ask the user

#### Step 3: Rename

Rename to: `YYYY-MM-DD Last. Title.ext`

- Date: publication year and month if available; year only if month unknown (use `YYYY-01-01`)
- Author: first author's last name only
- Title: shortened to approximately 60 characters if needed; no special characters except hyphens
- Preserve the original extension

If the file is already correctly named, skip renaming.

## The frontmatter block

**Begin every `_summary.md` with the frontmatter block below** (inlined into the agent prompt by the parent), then the summary content per the format template.

**Which fields you fill, stated once so "fill every field" and "omit the line if unknown" do not read as a contradiction.** Nine fields are always written: `kb`, `title`, `authors`, `date`, `type`, `topic`, `tags`, `index_line`, `ingested`, and `level`, plus `model` which the parent pre-fills. Of those, `topic:` and `tags:` are written blank and stay blank for the parent to set together at filing (`tags:` defaults to a single-element list matching `topic:`; you can add more by hand afterward). **Four fields are conditional, and the condition is the comment beside each: `venue`, `url`, `source_basis`, and `capture_caveat`. When the condition holds, delete the whole line rather than writing an empty value**, because a present-but-empty `source_basis:` reads as a degraded provenance to a downstream gate and a present-but-empty `url:` costs the duplicate check its highest-precision layer. Every free-text value (`title`, `authors`, `venue`, `url`, `index_line`) is double-quoted with `\"` and `\\` escaping; the closed-format fields (`kb`, `date`, `type`, `topic`, `ingested`, `level`, `model`, `source_basis`) stay unquoted. `index_line` is one sentence that locates and disambiguates the document, never summarizes it (target 30 words or fewer, per the Summary cell rule in Index Format).

```yaml
---
kb: v1
title: "<full title>"
authors: "<citation-form author list>"
date: <YYYY-MM-DD publication date, matching the filename prefix>
venue: "<publication, platform, or show>"   # omit the line if unknown
url: "<primary URL or DOI>"                 # omit the line if unknown
type: <paper|article|web|doc|blog|podcast|video|report|qa-answer>
topic:
tags:
index_line: "<one locate-and-disambiguate sentence>"
ingested: <today>
level: <full|triage|lite|fast-extract>
model: <the reading model's bare alias>     # pre-filled by the parent at agent launch
source_basis: <partial|excerpts>            # omit the line when the source is the complete published text
capture_caveat: "<one sentence>"            # omit unless the capture carries recorded doubt

---
```

**The `type:` enum above is the whole set, and it is defined here and nowhere else.** Mode 4's `--type` filter takes these values, minus `qa-answer`. `qa-answer` is written only by Mode 2's optional save step onto a `_notes.md` artifact, which the index generator and the reindexer both skip, so it never becomes a stored row or a filter value. There is no `post` type; a blog post is `type: blog`, and the index generator renders its `[blog]` marker from that field.

**Keep the blank line before the closing `---`.** It is part of the block, not stray whitespace. Without it, any Markdown renderer that does not strip front matter reads the last field line plus the `---` beneath it as a Setext heading and displays that field as an H2 (whichever field happens to land last is the one promoted). The blank line makes the closing delimiter a thematic break instead. Make your frontmatter reader skip blank lines inside the block, and field values, the generated index row, and the full-text database are all unaffected.

`source_basis` records what the summary was built from, a separate axis from `level:` (which records reading depth of a source that IS on disk). Its values: `full-text` (the filed source is the complete published text; this is the default, and the line is omitted when it holds), `partial` (an incomplete capture of the real source: paywall preview, abstract only, truncated fetch), and `excerpts` (no source was captured; content reconstructed from web-search excerpts and snippets). Absent means `full-text`. The Source-fetch failure rule (Mode 1, Step 1) is what sets this field when a URL will not fetch, and the slide skills read it before authoring and gate on BOTH degraded values. Each gates in the shape its own discipline allows: a **non-interactive deck generator** refuses terminally on either value, escaped by a standalone `useexcerpts` or `usepartial` token; an **interactive generator** confirms once on either; an **unattended batch entry point** refuses on `excerpts` and flags `partial` into the result line its queue reports, because its gate sits after the read is already paid and the queue cannot retry.

`capture_caveat` records doubt that does NOT rise to a gate: a metered publisher that may have served the whole article or a teaser, or a capture obtained by a fallback method. It is free text, one sentence, written by `kb-fetch-url` and copied verbatim into the summary. It is deliberately a separate axis from `source_basis`, whose two values gate the slide skills: a caveat is read by a human and by `kb ask` when citing, and stops nothing. Absent means no recorded doubt.

`model:` records which model performed the reading (on a fast-extract record, the summary agent's model), as a bare alias; the parent pre-fills it at agent launch (Flow step 2), so the record itself says what produced it. The slide path (Mode 5) reads `level:` and `model:` together as its reuse bar; a record with no `model:` field counts as below the bar there. One sentinel value, `model: grandfathered`, is set only by a one-time bulk backfill on records filed before the `model:` field existed; it marks a pre-existing record (whose true reading model is unknown) as trusted for slide-path reuse. New filing never writes `grandfathered`.

Save as `<filename>_summary.md` alongside the source file. The summary is the analytical reference artifact; the index row is rendered from this frontmatter by script, so a missing or malformed block means the item gets a degraded, flagged index row rather than a silently wrong one.

## Index Format

**`index.md` is generated and never hand-edited.** Run `kb-index` to regenerate it from every `_summary.md`'s frontmatter (atomic write, count-floor guarded); without the script, Claude rebuilds the whole table from that same frontmatter, which is generation and is the sanctioned fallback (see Helper commands). **What is banned in both cases is editing an individual row in place.** The Summary cell is the `index_line` frontmatter field; to change a row, edit the item's frontmatter and regenerate. It is a markdown table, one row per document:

```markdown
| Date | Author | Title | Topic | Summary |
|------|--------|-------|-------|---------|
| 2026-03-18 | Ipeirotis | Scalable Oral Assessments Using Voice AI | AI-articles | Voice AI oral exams at $0.42/student with multi-model deliberation achieving alpha=0.86 |
| 2026-02-18 | AuthorName (blog) | Did an Autonomous AI Write a Hit Piece | AI-safety | Analysis of an autonomous agent incident and implications for AI governance [blog] |
```

**Summary cell rule (the authoring rule for `index_line`):** one line, one sentence. It locates and disambiguates the document; it does not summarize it (the `_summary.md` holds the detail, and the search database indexes the full summary and text, so keywords crammed into the row add nothing to recall). Target 30 words or fewer; a single dense sentence carrying distinguishing figures may run longer but must stay one sentence. The hard rule is no second sentence and no paragraph. This rule governs the `index_line` frontmatter field at authoring time; the generator renders it into the row unmodified and untruncated.

**Provenance marker.** When a summary's frontmatter carries `source_basis: excerpts` or `source_basis: partial`, the generator appends `[excerpts]` or `[partial]` to that row's Summary cell, parallel to the `[blog]` marker rendered from `type: blog`. This is a browse-path convenience for a human scanning `index.md` or grepping it; the load-bearing provenance check lives in the slide skills, which read the `source_basis` frontmatter field directly, not the index row.

No mode reads this file whole into context; access is by `grep` (membership checks) or by script (`kb-search`, `kb-dup-check`, `kb-index`, `kb-status`). Topic narrowing reads `topics.md`, which stays small by construction. This is what lets the index grow without breaking any mode.

## Topics File

`topics.md` describes each topic folder:

```markdown
# Knowledge Base Topics

## AI-articles
AI's impact on labor markets, productivity, organizational design, and business strategy. Papers and reports analyzing economic and operational effects of AI adoption.

## AI-teaching
AI in education: assessment, tutoring, pedagogy, and curriculum design. How AI changes teaching and learning.

## other-articles
Non-AI articles on diverse topics. Overflow for content that does not fit a specific AI category.
```

Updated by the [knowledge-base-update](../knowledge-base-update/) skill. The user's folder organization choices over time teach the system what belongs where.

## Integration with Other Skills

### Skills that feed into knowledge-base
- **split-pdf**: used by inbox processing for PDF extraction
- A web-to-text conversion skill for URL ingestion (web page to extracted text)

### Skills that consume knowledge-base data
- **Your summary skills (academic and general)**: the user can request a full summary of any indexed document; the extract is not a substitute.
- **Your blog writing skill**: Q&A mode can find relevant sources for post research.
- **[slides-content](../slides-content/) and [beamer](../beamer/)**: the default slide route, and the one that ships. Mode 5 (`kb slides`) is the direct invocation path. It resolves the name fragment, path, or URL, files the source into the knowledge base first on every path, then hands the filed path to `slides-content`, which reuses the filed `_text.md` as its notes and the filed `_summary.md` if present, so an indexed extract feeds slide generation without re-reading the source PDF. The deliverable is a compiled Beamer PDF, with an optional PPTX conversion that `slides-content` offers at its own final step. `beamer` names this route explicitly and selects nothing extra.
- **An optional deck generator you supply**: a native PowerPoint generator, reached by Mode 5's `deck` and `lite` tokens. **None ships in this repository**, and until you replace the placeholder in `references/slides.md` Step 4 with your own generator's skill name, both tokens are refused. Once wired, it adds a second direction for a source new to the knowledge base: nothing is filed first, the generator reads the source once and writes the text, the summary, and the build's source brief in that single pass, and Step 5 files the finished set afterwards. `references/slides.md` owns that route and states its applicability test and its exclusions; do not restate them here.
- **Your analyze-and-reply skill**: Q&A can identify relevant indexed sources to support or challenge forwarded content.
- **Your chart skill**: Q&A answers involving data comparisons can generate charts.
- **Your diagram skill**: system architecture and topic maps can be generated as standalone diagrams.

### Index-update hook for content skills

When any content skill (slides, summary, and so on) completes work inside the `knowledge-base/` directory tree:

1. If the document's `_summary.md` lacks the frontmatter block (see The frontmatter block above), add it first, with `topic:` set to the containing folder and `tags:` defaulted to `[<topic>]`.
2. Run `kb-index`. Relay any warnings it prints.

This replaces a read-index, grep, and append hook: the generator walks the disk and renders every row from frontmatter, so a document appears in `index.md` as soon as its summary carries the block. It does not require invoking the knowledge-base-update skill. Content skills should perform this as a final step after writing their deliverables.

**Where to run content skills:** run them directly in the topic folder where the document lives. Do not route through inbox for documents that are already organized. The skill creates its subfolder and build artifacts in place. The index-update hook ensures the index stays current regardless of where processing happens.

## Constraints

- **Never delete original source files.** The skill renames and moves but never deletes.
- **Never overwrite extracts.** If an extract already exists, skip unless the user explicitly asks to regenerate. One standing authorized regeneration exists: the Mode 5 slide path's below-bar re-read, which replaces `_text.md` and `_summary.md` only after preserving the old artifacts as timestamped copies in the item folder.
- **The index is generated from disk, never edited by hand.** A document appears in `index.md` while its folder exists and disappears when it is removed; to change a row, edit the item's `_summary.md` frontmatter and rerun `kb-index`.
- **Topic folders are user-created.** The skill suggests new folders but waits for approval before creating them.
