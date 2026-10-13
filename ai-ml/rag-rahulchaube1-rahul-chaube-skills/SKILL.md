---
name: rag
description: Retrieval-Augmented Generation, chunking, metadata tags, and retrieval flows.
---

# Rag

Retrieval-Augmented Generation, chunking, metadata tags, and retrieval flows.

## Core Guidelines

- **Chunking Strategy**: Size chunks based on document structure (e.g., paragraph or section level).
- **Overlap**: Include context overlaps to maintain semantic continuity between chunks.
- **Re-ranking**: Apply re-ranking models on retrieved logs to prioritize top-quality matches.
