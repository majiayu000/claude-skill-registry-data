---
name: wiki
description: Capture sources into this Commonplace wiki, answer questions from its notes, connect knowledge, or maintain its Markdown collection. Use for requests to save a source, ask the wiki, or organize existing notes.
---

# Work with the wiki

Work from the repository root. This skill operates on authored Markdown; the Nuxt app is its reading interface. Read the root [AGENTS.md](../../../AGENTS.md) for project commands and boundaries.

## Route the user's request

| Request | Read |
| --- | --- |
| Save a YouTube video or talk | [YouTube](playbooks/ingest-youtube.md) |
| Save an article, documentation page or PDF | [Article](playbooks/ingest-article.md) |
| Save a podcast episode, including one hosted on YouTube | [Podcast](playbooks/ingest-podcast.md) |
| Save a book or reading notes | [Book](playbooks/ingest-book.md) |
| Save a film or viewing notes | [Film](playbooks/ingest-film.md) |
| Ask what the wiki knows | [Answer](playbooks/answer-question.md) |
| Find connections or audit the collection | [Maintenance](playbooks/maintain-wiki.md) |

A URL in an explicit capture request routes automatically. A URL supplied for discussion or comparison does not authorize saving. For an otherwise unexplained URL, clarify the intended action. Do not create a new playbook for each URL.

## Shared decisions

Before processing a source, read [evidence first](../principle-evidence-first/SKILL.md), [reuse existing knowledge](../principle-reuse-existing-knowledge/SKILL.md), [explain connections](../principle-explain-connections/SKILL.md), and [private by default](../principle-private-by-default/SKILL.md). These are the canonical rules; playbooks specialize the work rather than restating them.

Use [source extraction](../wiki-extract-source/SKILL.md) to inspect input, [connection discovery](../wiki-connect-notes/SKILL.md) to integrate it, and [validation](../wiki-validate/SKILL.md) before reporting saved changes. Read the [note contract](references/note-contract.md) when writing Markdown. Load only the chosen playbook and relevant supporting resources.

An interrupted run begins by inspecting existing files and source identity. Reuse completed work; do not restart with new IDs. Finish with changed note IDs, evidence limitations, validation results and whether anything was committed or published. Saving a note does not authorize either Git operation.
