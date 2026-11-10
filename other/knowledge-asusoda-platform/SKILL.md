---
name: knowledge
description: The org's searchable knowledge, live queries of shared content such as ASU, and web search.
---

# Knowledge

Use it to find facts: the org's own documents and crawled pages, live answers from shared content (submodules such as ASU classes, clubs and events), and the web.

## Flow

1. `search` (in the tool list) is the one entry point for most questions. It tries stored passages, then live sources, then the web.
2. `knowledge.search` searches only stored passages. `knowledge.read_source` reads a whole source a page at a time.
3. `knowledge.query` asks one live source by name, such as `asu/courses` or `asu/clubs`. Its description lists the sources and their arguments.
4. `knowledge.web_search` searches the web when nothing stored fits.
5. To add knowledge: `knowledge.add_document` for text, `knowledge.set_crawl` for a web page the crawl job fetches, `knowledge.sync_submodule` for shared content.

## Watch out

- Cite the URL a result gives.
- Some live sources need the org's saved sign-in. A 409 means an officer has to sign in again on Explore, Shared.
- `knowledge.reindex` and `knowledge.reembed` redo every source and can take a while.
