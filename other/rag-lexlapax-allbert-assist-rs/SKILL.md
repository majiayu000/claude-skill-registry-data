---
name: rag
description: Create, ingest, search, and attach explicit user RAG collections for task-specific corpora.
intents: [task, memory_query, meta]
allowed-tools:
  - list_rag_collections
  - create_rag_collection
  - ingest_rag_collection
  - delete_rag_collection
  - attach_rag_collection
  - detach_rag_collection
  - search_rag
---

# RAG

Use this skill when the operator explicitly asks to create, ingest, search, use, attach, detach, or delete a task-specific RAG collection.

## Collection posture

- User collections are explicit task/corpus context. They are not default memory and are not automatically injected into prompts.
- Create collections only from sources the operator names directly. Do not infer a collection source from incidental URLs or paths in the conversation.
- Local sources must pass kernel trusted-root checks. URL sources must pass kernel URL policy, robots, redirect, content-type, and SSRF checks.
- Search user collections only by naming `collection_type: "user"` and the collection name.
- Attach a collection only when the operator asks to use it for the current task or session. Detach it when the operator asks to stop using it.
- Deleting a collection removes the manifest and derived index rows only. It does not delete local source files or remote content.

## Typical flow

1. Use `list_rag_collections` when checking whether a collection exists.
2. Use `create_rag_collection` for an explicit local path or HTTP(S) URL source.
3. Use `ingest_rag_collection` after creation or when sources changed.
4. Use `search_rag` with `collection_type: "user"` and `collections: ["name"]` for scoped lookup.
5. Use `attach_rag_collection` only after the operator asks to use that collection as task context.
