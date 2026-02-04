---
name: rag-architecture
description: Design retrieval-augmented generation pipelines including chunking, embedding, retrieval, and context assembly strategies.
allowed-tools: Read, Write, Glob, Grep, Task
---

# RAG Architecture Design

## When to Use This Skill

Use this skill when:

- **Rag Architecture tasks** - Working on design retrieval-augmented generation pipelines including chunking, embedding, retrieval, and context assembly strategies
- **Planning or design** - Need guidance on Rag Architecture approaches
- **Best practices** - Want to follow established patterns and standards

## Overview

Retrieval-Augmented Generation (RAG) combines retrieval from a knowledge base with LLM generation to provide accurate, grounded responses. Proper architecture is critical for performance and quality.

## RAG Pipeline Architecture

```text
┌─────────────────────────────────────────────────────────────────┐
│                      RAG Pipeline                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                  INDEXING PIPELINE                        │   │
│  │                                                           │   │
│  │  Documents → Chunking → Embedding → Vector Store          │   │
│  │                                                           │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                  QUERY PIPELINE                           │   │
│  │                                                           │   │
│  │  Query → Embedding → Retrieval → Reranking → Context →   │   │
│  │         LLM Generation → Response                         │   │
│  │                                                           │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Document Chunking

### Chunking Strategies

| Strategy | Description | Best For |
|----------|-------------|----------|
| Fixed Size | Split by character/token count | Simple, general |
| Sentence | Split at sentence boundaries | Prose, articles |
| Paragraph | Split at paragraph boundaries | Structured docs |
| Semantic | Split by topic/meaning | Technical docs |
| Recursive | Hierarchical splitting | Mixed content |
| Document Structure | Use headers, sections | Manuals, specs |

### Chunk Size Guidelines

| Document Type | Chunk Size | Overlap |
|---------------|------------|---------|
| FAQ | 100-300 tokens | 10-20% |
| Articles | 300-500 tokens | 15-25% |
| Technical Docs | 500-1000 tokens | 20-30% |
| Legal/Contracts | 200-400 tokens | 25-35% |
| Code | 50-150 lines | By function |

### Chunking Implementation

```csharp
public class DocumentChunker
{
    public IEnumerable<Chunk> ChunkDocument(
        Document document,
        ChunkingOptions options)
    {
        return options.Strategy switch
        {
            ChunkingStrategy.FixedSize =>
                FixedSizeChunk(document.Content, options.ChunkSize, options.Overlap),

            ChunkingStrategy.Sentence =>
                SentenceChunk(document.Content, options.MaxSentences),

            ChunkingStrategy.Semantic =>
                SemanticChunk(document.Content, options.SemanticThreshold),

            ChunkingStrategy.Recursive =>
                RecursiveChunk(document.Content, options),

            _ => throw new NotSupportedException()
        };
    }

    private IEnumerable<Chunk> RecursiveChunk(
        string content,
        ChunkingOptions options)
    {
        var separators = new[] { "\n\n", "\n", ". ", " " };

        foreach (var separator in separators)
        {
            var splits = content.Split(separator);

            if (splits.All(s => CountTokens(s) <= options.ChunkSize))
            {
                return MergeSmallChunks(splits, options.ChunkSize, options.Overlap)
                    .Select((text, i) => new Chunk
                    {
                        Id = Guid.NewGuid(),
                        Content = text,
                        Index = i,
                        Metadata = new ChunkMetadata
                        {
                            TokenCount = CountTokens(text),
                            Separator = separator
                        }
                    });
            }
        }

        return FixedSizeChunk(content, options.ChunkSize, options.Overlap);
    }
}
```

## Embedding Strategies

### Embedding Model Selection

| Model | Dimensions | Speed | Quality | Cost |
|-------|------------|-------|---------|------|
| text-embedding-3-small | 1536 | Fast | Good | Low |
| text-embedding-3-large | 3072 | Medium | Excellent | Medium |
| text-embedding-ada-002 | 1536 | Fast | Good | Low |
| Cohere embed-v3 | 1024 | Fast | Excellent | Medium |
| BGE-large | 1024 | Medium | Excellent | Free (local) |

### Embedding Best Practices

```csharp
public class EmbeddingService
{
    private readonly IEmbeddingClient _client;
    private readonly SemaphoreSlim _rateLimiter;

    public async Task<float[][]> EmbedBatch(
        IEnumerable<string> texts,
        CancellationToken ct)
    {
        var textList = texts.ToList();
        var embeddings = new List<float[]>();

        // Process in batches to avoid rate limits
        foreach (var batch in textList.Chunk(100))
        {
            await _rateLimiter.WaitAsync(ct);

            try
            {
                var batchEmbeddings = await _client.EmbedAsync(
                    batch.ToArray(),
                    ct);

                embeddings.AddRange(batchEmbeddings);
            }
            finally
            {
                _rateLimiter.Release();
            }
        }

        return embeddings.ToArray();
    }

    public async Task<float[]> EmbedQuery(string query, CancellationToken ct)
    {
        // Some models need different prompts for queries vs documents
        var formattedQuery = $"query: {query}";
        return await _client.EmbedAsync(formattedQuery, ct);
    }
}
```

## Vector Store Design

### Store Selection

| Store | Type | Scalability | Features |
|-------|------|-------------|----------|
| Azure AI Search | Managed | High | Hybrid search, filters |
| Pinecone | Managed | High | Simple API |
| Qdrant | Self-hosted/Managed | High | Payload filters |
| Weaviate | Self-hosted/Managed | High | GraphQL, modules |
| Chroma | Self-hosted | Medium | Simple, local dev |
| pgvector | PostgreSQL extension | Medium | SQL integration |

### Index Design

```csharp
public class VectorIndexSchema
{
    public string IndexName { get; set; } = "documents";

    public List<VectorField> VectorFields { get; set; } =
    [
        new VectorField
        {
            Name = "content_vector",
            Dimensions = 1536,
            Similarity = SimilarityMetric.Cosine,
            IndexType = IndexType.HNSW,
            HnswConfig = new HnswConfig
            {
                M = 16,
                EfConstruction = 100,
                EfSearch = 40
            }
        }
    ];

    public List<MetadataField> MetadataFields { get; set; } =
    [
        new MetadataField("document_id", FieldType.String, Filterable: true),
        new MetadataField("source", FieldType.String, Filterable: true),
        new MetadataField("created_at", FieldType.DateTime, Filterable: true),
        new MetadataField("category", FieldType.StringArray, Filterable: true),
        new MetadataField("content", FieldType.Text, Searchable: true)
    ];
}
```

## Retrieval Strategies

### Retrieval Methods

| Method | Description | Pros | Cons |
|--------|-------------|------|------|
| Vector Search | Semantic similarity | Handles synonyms | May miss exact |
| Keyword Search | BM25/TF-IDF | Exact matches | Misses synonyms |
| Hybrid | Vector + Keyword | Best of both | More complex |
| Multi-Query | Generate variations | Better recall | Higher cost |
| HyDE | Hypothetical answer | Better precision | Latency |

### Hybrid Search Implementation

```csharp
public class HybridRetriever
{
    private readonly IVectorStore _vectorStore;
    private readonly ISearchClient _keywordSearch;

    public async Task<List<SearchResult>> Retrieve(
        string query,
        RetrievalOptions options,
        CancellationToken ct)
    {
        // Run vector and keyword search in parallel
        var vectorTask = _vectorStore.SearchAsync(
            query,
            options.TopK * 2,  // Retrieve more for fusion
            ct);

        var keywordTask = _keywordSearch.SearchAsync(
            query,
            options.TopK * 2,
            ct);

        await Task.WhenAll(vectorTask, keywordTask);

        var vectorResults = await vectorTask;
        var keywordResults = await keywordTask;

        // Reciprocal Rank Fusion
        var fused = ReciprocalRankFusion(
            vectorResults,
            keywordResults,
            options.VectorWeight,
            options.KeywordWeight);

        return fused.Take(options.TopK).ToList();
    }

    private List<SearchResult> ReciprocalRankFusion(
        List<SearchResult> vectorResults,
        List<SearchResult> keywordResults,
        float vectorWeight,
        float keywordWeight,
        int k = 60)
    {
        var scores = new Dictionary<string, float>();

        for (int i = 0; i < vectorResults.Count; i++)
        {
            var id = vectorResults[i].Id;
            scores.TryAdd(id, 0);
            scores[id] += vectorWeight / (k + i + 1);
        }

        for (int i = 0; i < keywordResults.Count; i++)
        {
            var id = keywordResults[i].Id;
            scores.TryAdd(id, 0);
            scores[id] += keywordWeight / (k + i + 1);
        }

        return scores
            .OrderByDescending(kv => kv.Value)
            .Select(kv => new SearchResult
            {
                Id = kv.Key,
                Score = kv.Value
            })
            .ToList();
    }
}
```

## Context Assembly

### Context Window Management

```csharp
public class ContextAssembler
{
    private readonly int _maxTokens;

    public string AssembleContext(
        List<SearchResult> results,
        string query,
        int reservedTokens = 500)
    {
        var availableTokens = _maxTokens - reservedTokens;
        var context = new StringBuilder();
        var usedTokens = 0;

        // Sort by relevance (already sorted from retrieval)
        foreach (var result in results)
        {
            var chunkTokens = CountTokens(result.Content);

            if (usedTokens + chunkTokens > availableTokens)
                break;

            context.AppendLine($"[Source: {result.Source}]");
            context.AppendLine(result.Content);
            context.AppendLine();

            usedTokens += chunkTokens;
        }

        return context.ToString();
    }
}
```

## RAG Evaluation

### Evaluation Metrics

| Metric | Description | Target |
|--------|-------------|--------|
| Retrieval Precision | Relevant docs / Retrieved docs | > 80% |
| Retrieval Recall | Retrieved relevant / All relevant | > 70% |
| Answer Accuracy | Correct answers | > 90% |
| Faithfulness | Answer supported by context | > 95% |
| Answer Relevancy | Answer matches query | > 85% |

### Evaluation Framework

```csharp
public class RagEvaluator
{
    public async Task<EvaluationReport> Evaluate(
        List<TestCase> testCases,
        IRagPipeline pipeline,
        CancellationToken ct)
    {
        var results = new List<TestResult>();

        foreach (var testCase in testCases)
        {
            var response = await pipeline.Query(testCase.Query, ct);

            results.Add(new TestResult
            {
                Query = testCase.Query,
                ExpectedAnswer = testCase.ExpectedAnswer,
                ActualAnswer = response.Answer,
                RetrievedDocs = response.Sources,
                RelevantDocs = testCase.RelevantDocs,
                Metrics = new TestMetrics
                {
                    RetrievalPrecision = CalculatePrecision(
                        response.Sources, testCase.RelevantDocs),
                    RetrievalRecall = CalculateRecall(
                        response.Sources, testCase.RelevantDocs),
                    AnswerCorrect = await EvaluateAnswer(
                        response.Answer, testCase.ExpectedAnswer),
                    Faithful = await CheckFaithfulness(
                        response.Answer, response.Context)
                }
            });
        }

        return new EvaluationReport(results);
    }
}
```

## Architecture Template

```markdown
# RAG Architecture: [System Name]

## Overview
[Brief description of the RAG system purpose]

## Components

### Document Processing
- **Source**: [Document sources]
- **Chunking**: [Strategy and parameters]
- **Embedding**: [Model and dimensions]

### Vector Store
- **Provider**: [Azure AI Search / Pinecone / etc.]
- **Index**: [Index configuration]
- **Metadata**: [Stored fields]

### Retrieval
- **Method**: [Vector / Hybrid / Multi-query]
- **Top-K**: [Number of results]
- **Filters**: [Applied filters]

### Generation
- **Model**: [LLM model]
- **Context Window**: [Token allocation]
- **Prompt**: [Template reference]

## Data Flow
[Mermaid diagram of the pipeline]

## Performance Targets
| Metric | Target |
|--------|--------|
| Retrieval Latency | < 200ms |
| E2E Latency | < 3s |
| Answer Accuracy | > 90% |
```

## Validation Checklist

- [ ] Document sources identified
- [ ] Chunking strategy selected and tested
- [ ] Embedding model chosen
- [ ] Vector store provisioned
- [ ] Retrieval method determined
- [ ] Context assembly strategy defined
- [ ] Evaluation metrics established
- [ ] Performance targets set
- [ ] Monitoring planned

## Integration Points

**Inputs from**:

- Data sources → Documents to index
- `model-selection` skill → Embedding/LLM choice

**Outputs to**:

- `prompt-engineering` skill → Context integration
- `token-budgeting` skill → Cost estimation
- Application code → RAG implementation
