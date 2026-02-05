---
name: koan-vector-migration
description: Vector export/import, embedding caching, provider migration
---

# Koan Vector Migration

## Core Principle

**Export vectors without regenerating via AI.** Cache embeddings to enable zero-cost vector database migration.

## Vector Export (DATA-0078)

### Export Vectors

```csharp
var vectorRepo = serviceProvider.GetRequiredService<IVectorSearchRepository<Media, string>>();

await foreach (var batch in vectorRepo.ExportAllAsync(batchSize: 100, ct))
{
    // batch.Id: Entity identifier
    // batch.Embedding: float[] vector
    // batch.Metadata: Optional metadata

    // Cache the embedding
    var contentHash = EmbeddingCache.ComputeContentHash(embeddingText);
    await cache.SetAsync(contentHash, modelId, batch.Embedding, ct);
}
```

### Provider Support

- ✅ **ElasticSearch**: Scroll API (default batch: 1000)
- ✅ **Weaviate**: GraphQL pagination (default batch: 100)
- ⏳ **Qdrant**: Planned
- ⏳ **Milvus**: Planned
- ❌ **Pinecone**: Not supported (throws NotSupportedException)

### Migration Pattern

```
1. Export vectors from Provider A → Cache
2. Switch configuration to Provider B
3. Import vectors from Cache → Provider B

Result: Zero AI API calls for migration
```

## Example: Weaviate → ElasticSearch

```csharp
// Step 1: Export from Weaviate
using (EntityContext.Adapter("weaviate"))
{
    var vectorRepo = sp.GetRequiredService<IVectorSearchRepository<Media, string>>();

    await foreach (var batch in vectorRepo.ExportAllAsync(batchSize: 100, ct))
    {
        await cache.SetAsync(batch.Id, "ada-002", batch.Embedding, ct);
    }
}

// Step 2: Switch to ElasticSearch in appsettings.json
{
  "Koan": {
    "Data": {
      "Sources": {
        "Vectors": {
          "Adapter": "elasticsearch",
          "ConnectionString": "http://localhost:9200"
        }
      }
    }
  }
}

// Step 3: Import to ElasticSearch
foreach (var mediaId in allMediaIds)
{
    var embedding = await cache.GetAsync(mediaId, "ada-002", ct);
    if (embedding != null)
    {
        var media = new Media { Id = mediaId, Embedding = embedding };
        await media.Save();
    }
}
```

## When This Skill Applies

- ✅ Migrating vector databases
- ✅ Caching embeddings
- ✅ AI provider switches
- ✅ Cost optimization
- ✅ Vector backup/restore

## Reference Documentation

- **CLAUDE.md:** Lines 96-123 (Vector Export for Migration)
- **ADR:** DATA-0078 (Vector export specification)
- **Guide:** `docs/guides/ai-vector-howto.md`
