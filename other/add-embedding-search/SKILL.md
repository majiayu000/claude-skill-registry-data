---
name: add-embedding-search
description: Add vector similarity search using embeddings for smart matching (property matching, lead-to-listing, similar items). Use when building AI-powered search and recommendations.
---

# add-embedding-search

Creates a vector embedding pipeline: text → embedding → storage → cosine similarity search. Used for smart property matching, "similar listings", and buyer requirement matching.

## Inputs to gather

- **Entity to embed** — e.g., properties, leads (buyer requirements), listings
- **Text fields to embed** — which fields concatenate into the embedding input (title + description + features)
- **Search input** — what the user provides to find matches (free text, or structured requirements)
- **Top-K** — how many results to return (default 10)

## Steps

1. **Choose embedding provider:**
   - **Claude (Voyage):** `voyage-3` via Anthropic — best Arabic support
   - **OpenAI:** `text-embedding-3-small` — cheaper, good enough
   - **Local:** Ollama with `nomic-embed-text` — free, runs on Mac

2. **Create embeddings table:**
   ```prisma
   model embeddings {
     id         String   @id @default(uuid())
     entityType String   // "property", "lead_requirement"
     entityId   String   @unique
     vector     Float[]  // embedding vector
     textHash   String   // hash of input text (skip re-embedding if unchanged)
     createdAt  DateTime @default(now())
     updatedAt  DateTime @updatedAt
   }
   ```

3. **Create embedding service** at `apps/api/libs/embedding-service.ts`:
   ```typescript
   export async function embedText(text: string): Promise<number[]> { ... }
   export async function findSimilar(vector: number[], entityType: string, topK: number) {
     // Cosine similarity using pgvector or manual calculation
   }
   ```

4. **Create the batch embed cron** using `/add-cron-job`:
   - Query entities without embeddings or with stale textHash
   - Generate embeddings in batches of 100
   - Store in embeddings table

5. **Create search API:**
   ```typescript
   router.post("/ai/match", authenticateToken, async (req, res) => {
     const { query, entityType, topK } = req.body;
     const queryVector = await embedText(query);
     const matches = await findSimilar(queryVector, entityType, topK);
     res.json(matches);
   });
   ```

6. **Frontend: "عقارات مقترحة" component** — displays matched properties as cards.

## Verification checklist

- [ ] Embeddings generated for all target entities
- [ ] Search returns relevant results (manual quality check)
- [ ] Stale embeddings auto-refresh when entity text changes
- [ ] Cron batch processing doesn't timeout
- [ ] API response time < 500ms for search queries
- [ ] `/typecheck` passes

## Anti-patterns

- Don't embed on every API request — batch via cron, search against stored vectors
- Don't store embeddings in the main entity table — use a separate table
- Don't re-embed unchanged text — use textHash to skip
- Don't return raw similarity scores to users — return ranked results with entity details
