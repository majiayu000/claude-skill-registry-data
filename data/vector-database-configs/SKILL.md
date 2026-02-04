---
name: vector-database-configs
description: Vector database configuration and setup for pgvector, Chroma, Pinecone, Weaviate, Qdrant, and FAISS with comparison guide and migration helpers
allowed-tools: Bash, Read, Write, Edit, Grep, Glob
---

# Vector Database Configurations

Provides comprehensive configuration, setup scripts, and templates for six popular vector databases used in RAG pipelines. Includes database selection guide, functional setup scripts, configuration templates, and migration examples.

## Use When

- Setting up vector storage for RAG pipeline
- Comparing vector database options for a project
- Migrating between vector databases
- Configuring vector indexes and schema
- Optimizing vector search performance
- Setting up development or production vector databases
- Generating database-specific configuration files

## Vector Database Comparison

### Quick Selection Guide

**pgvector (PostgreSQL extension)**
- Best for: Existing PostgreSQL users, transactional consistency, complex filtering
- Hosting: Self-hosted, managed Postgres (Supabase, RDS, etc.)
- Scale: Up to millions of vectors with proper indexing
- Cost: Free (open source), hosting costs only
- When to use: You already use PostgreSQL, need ACID guarantees, complex metadata queries

**Chroma**
- Best for: Development, prototyping, local-first applications
- Hosting: In-process, client-server, or cloud
- Scale: Thousands to millions of vectors
- Cost: Free (open source), cloud pricing for hosted
- When to use: Fast prototyping, embedded applications, simple deployments

**Pinecone**
- Best for: Production deployments, managed service, high performance
- Hosting: Fully managed cloud only
- Scale: Billions of vectors
- Cost: Paid service with free tier
- When to use: Production systems, need managed infrastructure, high scale

**Weaviate**
- Best for: GraphQL APIs, semantic search, hybrid search
- Hosting: Self-hosted or cloud
- Scale: Billions of vectors
- Cost: Free (open source), cloud pricing for managed
- When to use: Need GraphQL interface, hybrid keyword+vector search, modules ecosystem

**Qdrant**
- Best for: High performance, filtering, payload indexing
- Hosting: Self-hosted, Docker, or cloud
- Scale: Billions of vectors
- Cost: Free (open source), cloud pricing for managed
- When to use: Need advanced filtering, high-performance search, Rust performance

**FAISS**
- Best for: Research, maximum performance, custom algorithms
- Hosting: Self-managed in application
- Scale: Billions of vectors (with proper hardware)
- Cost: Free (open source)
- When to use: Maximum performance, custom algorithms, research projects, batch processing

### Feature Comparison

| Feature | pgvector | Chroma | Pinecone | Weaviate | Qdrant | FAISS |
|---------|----------|--------|----------|----------|--------|-------|
| Setup Complexity | Medium | Low | Low | Medium | Medium | High |
| Distance Metrics | L2, Cosine, Inner Product | L2, Cosine, IP | Cosine, Euclidean, Dot | Multiple | Multiple | Multiple |
| Metadata Filtering | Excellent (SQL) | Good | Good | Excellent (GraphQL) | Excellent | Manual |
| ACID Transactions | Yes | No | No | No | No | No |
| Horizontal Scaling | Limited | Yes | Yes | Yes | Yes | Manual |
| Cloud Managed | Via providers | Yes | Yes (only) | Yes | Yes | No |
| Open Source | Yes | Yes | No | Yes | Yes | Yes |

## Available Scripts

All scripts are located in `scripts/` directory and are fully functional:

**setup-pgvector.sh**
- Installs pgvector extension
- Creates database and enables extension
- Sets up vector schema with indexes
- Configures optimal settings

**setup-chroma.sh**
- Installs Chroma via pip
- Initializes persistent client
- Creates collections
- Configures embedding functions

**setup-pinecone.sh**
- Validates API key
- Creates indexes with specified dimensions
- Configures metadata indexes
- Sets up serverless or pod-based deployment

**setup-weaviate.sh**
- Starts Weaviate with Docker
- Creates schema classes
- Configures vectorizer modules
- Sets up GraphQL endpoint

**setup-qdrant.sh**
- Starts Qdrant with Docker or installs client
- Creates collections
- Configures vector and payload indexes
- Sets up API endpoints

**setup-faiss.sh**
- Installs FAISS via conda or pip
- Creates index with specified algorithm
- Configures search parameters
- Sets up serialization

## Available Templates

All templates are located in `templates/` directory:

**pgvector-schema.sql**
- Vector column definitions
- Index creation (IVFFlat, HNSW)
- Distance function examples
- Optimized search queries

**chroma-config.py**
- Client initialization
- Collection setup
- Embedding configuration
- Query patterns

**pinecone-config.py**
- API authentication
- Index creation
- Upsert and query examples
- Metadata filtering

**weaviate-schema.py**
- Schema class definition
- Vector configuration
- Module setup
- GraphQL queries

**qdrant-config.py**
- Collection creation
- Vector and payload config
- Search API examples
- Filter queries

**faiss-config.py**
- Index factory patterns
- Training and adding vectors
- Search configuration
- Serialization helpers

## Available Examples

Located in `examples/` directory:

**migration-guide.md**
- Migration paths between databases
- Data export/import scripts
- Schema mapping examples
- Testing migration accuracy

**performance-tuning.md**
- Index optimization for each database
- Query performance tips
- Batch operation patterns
- Monitoring and metrics

## Usage Examples

### Compare Databases for Project

Read SKILL.md comparison table and selection guide to choose the right database based on:
- Existing infrastructure (PostgreSQL → pgvector)
- Scale requirements (Billions → Pinecone, Qdrant, Weaviate)
- Hosting preference (Managed → Pinecone, Self-hosted → others)
- Budget constraints (Free tier needed → Chroma, pgvector, FAISS)
- Feature requirements (GraphQL → Weaviate, Advanced filtering → Qdrant)

### Setup pgvector on Existing PostgreSQL

```bash
# Run setup script
bash scripts/setup-pgvector.sh --database mydb --user postgres --dimensions 1536

# Apply schema template
psql -U postgres -d mydb -f templates/pgvector-schema.sql
```

### Setup Chroma for Development

```bash
# Install and configure
bash scripts/setup-chroma.sh --persist-dir ./chroma_data --collection documents

# Use Python configuration template
cp templates/chroma-config.py ./config/vector_db.py
```

### Setup Pinecone for Production

```bash
# Configure with API key
export PINECONE_API_KEY="your-key"
bash scripts/setup-pinecone.sh --index production-docs --dimensions 1536 --metric cosine

# Use configuration template
cp templates/pinecone-config.py ./config/vector_db.py
```

### Migrate from Chroma to Qdrant

```bash
# Export from Chroma
python examples/migration-scripts/export-chroma.py --output vectors.json

# Setup Qdrant
bash scripts/setup-qdrant.sh --collection documents --dimensions 1536

# Import to Qdrant
python examples/migration-scripts/import-qdrant.py --input vectors.json
```

## Integration with RAG Pipeline

This skill integrates with other rag-pipeline components:

**document-chunking skill** → Generates chunks to be embedded
**embedding-models skill** → Generates vectors to be stored
**vector-database-configs** → Stores and retrieves vectors
**retrieval-strategies skill** → Queries vector database

## Distance Metrics Guide

**Cosine Similarity**
- Range: -1 to 1 (higher is more similar)
- Best for: Text embeddings (OpenAI, Cohere, etc.)
- Normalized: Yes (magnitude independent)

**Euclidean (L2)**
- Range: 0 to infinity (lower is more similar)
- Best for: Image embeddings, spatial data
- Normalized: No (affected by magnitude)

**Inner Product (Dot Product)**
- Range: -infinity to infinity (higher is more similar)
- Best for: When embeddings are normalized
- Normalized: Depends on vectors

## Performance Optimization Tips

**For All Databases:**
- Use appropriate index type for scale (HNSW for large datasets)
- Batch insert operations
- Monitor query latency and adjust index parameters
- Pre-filter on metadata before vector search when possible

**pgvector Specific:**
- Use `ivfflat` for 100K-1M vectors, `hnsw` for 1M+
- Increase `maintenance_work_mem` for index building
- Use partial indexes for filtered queries
- Consider table partitioning for very large datasets

**FAISS Specific:**
- Choose index based on dataset size (Flat < 10K, IVF < 100M, HNSW for most)
- Use GPU indices for maximum performance
- Pre-train IVF indices with representative data
- Adjust nprobe parameter for accuracy/speed tradeoff

## Error Handling

All scripts include:
- Dependency checking before execution
- Connection validation
- Clear error messages with resolution steps
- Rollback on failure where applicable
- Environment variable validation

## Security Considerations

- Store API keys in environment variables (never hardcode)
- Use connection pooling for database connections
- Enable TLS/SSL for network connections
- Implement authentication for self-hosted deployments
- Use read-only credentials for query-only applications
- Sanitize user inputs before using in filters

## References

- pgvector: https://github.com/pgvector/pgvector
- Supabase pgvector: https://supabase.com/docs/guides/ai/vector-columns
- Chroma: https://docs.trychroma.com/
- Pinecone: https://docs.pinecone.io/
- Weaviate: https://weaviate.io/developers/weaviate
- Qdrant: https://qdrant.tech/documentation/
- FAISS: https://faiss.ai/
