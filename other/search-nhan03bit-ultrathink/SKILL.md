---
name: search
description: Full-text search implementation with Algolia, MeiliSearch, PostgreSQL pg_trgm, search UX patterns, autocomplete, and relevance tuning
layer: domain
category: backend
triggers:
  - "full-text search"
  - "search implementation"
  - "algolia"
  - "meilisearch"
  - "pg_trgm"
  - "search autocomplete"
  - "fuzzy search"
  - "search relevance"
  - "typeahead"
  - "search index"
inputs:
  - Data corpus size and type
  - Search requirements (fuzzy, faceted, geo, typo-tolerant)
  - Latency budget
  - Infrastructure constraints
  - UX requirements (autocomplete, filters, highlighting)
outputs:
  - Search architecture recommendation
  - Index configuration and schema
  - Query implementation with ranking
  - Autocomplete/typeahead component
  - Sync strategy between DB and search index
linksTo:
  - postgresql
  - api-designer
  - react
  - performance-profiler
  - caching
linkedFrom:
  - ecommerce
  - ui-ux-pro
preferredNextSkills:
  - caching
  - api-designer
fallbackSkills:
  - postgresql
  - redis
riskLevel: low
memoryReadPolicy: selective
memoryWritePolicy: selective
sideEffects:
  - May add search service dependencies (algoliasearch, meilisearch)
  - May require background sync jobs
  - May add PostgreSQL extensions (pg_trgm, unaccent)
---

# Search Domain Skill

## Purpose

Search is a core UX feature that users judge harshly -- slow or irrelevant results destroy trust. This skill covers choosing the right search backend, building indexes, tuning relevance, and delivering the fast autocomplete-driven UX that users expect.

## When to Use What

| Solution | Best For | Latency | Setup | Cost |
|----------|----------|---------|-------|------|
| **PostgreSQL pg_trgm** | < 1M rows, simple fuzzy search | 10-100ms | None (extension) | Free |
| **PostgreSQL FTS** | < 5M rows, structured search | 5-50ms | Extension + config | Free |
| **MeiliSearch** | < 10M docs, self-hosted, great defaults | 1-20ms | Docker container | Free (self-hosted) |
| **Algolia** | Any scale, zero-ops, instant UX | 1-10ms | SaaS | $$$ (per search) |
| **Typesense** | Self-hosted alternative to Algolia | 1-15ms | Docker container | Free (self-hosted) |
| **Elasticsearch** | > 100M docs, complex aggregations, logs | 5-50ms | Cluster management | $$$ (infra) |

**Default recommendation**: PostgreSQL pg_trgm for MVPs. MeiliSearch for growing apps. Algolia for search-critical products with budget.

## Key Concepts

### Search Relevance Fundamentals

```
TF-IDF (Term Frequency - Inverse Document Frequency):
  - Words that appear often in a document but rarely across all documents score higher
  - "the" appears everywhere -> low signal. "kubernetes" appears rarely -> high signal.

BM25 (Best Match 25):
  - Improved TF-IDF used by PostgreSQL FTS, MeiliSearch, Elasticsearch
  - Accounts for document length normalization
  - Tunable parameters: k1 (term frequency saturation), b (length normalization)

Ranking factors to combine:
  1. Text relevance (BM25/TF-IDF)
  2. Recency (newer content ranked higher)
  3. Popularity (views, sales, ratings)
  4. Exact match boost (title match > body match)
  5. Personalization (user history, preferences)
```

## Patterns

### 1. PostgreSQL pg_trgm (Zero Infrastructure)

```sql
-- Enable extensions
CREATE EXTENSION IF NOT EXISTS pg_trgm;
CREATE EXTENSION IF NOT EXISTS unaccent;

-- Create indexes for fuzzy search
CREATE INDEX idx_products_name_trgm ON products
  USING gin (name gin_trgm_ops);

CREATE INDEX idx_products_description_trgm ON products
  USING gin (description gin_trgm_ops);

-- Combined search with similarity scoring
SELECT
  id,
  name,
  description,
  similarity(name, 'wireles mouse') AS name_score,
  similarity(description, 'wireles mouse') AS desc_score,
  -- Weighted combined score
  (similarity(name, 'wireles mouse') * 2 + similarity(description, 'wireles mouse')) AS combined_score
FROM products
WHERE
  name % 'wireles mouse'  -- % operator uses similarity threshold (default 0.3)
  OR description % 'wireles mouse'
ORDER BY combined_score DESC
LIMIT 20;

-- Adjust similarity threshold (default 0.3)
SET pg_trgm.similarity_threshold = 0.2; -- More permissive for typo tolerance

-- Autocomplete with prefix matching (faster)
SELECT id, name
FROM products
WHERE name ILIKE 'wire%'  -- Uses index if B-tree index exists on name
ORDER BY name
LIMIT 10;
```

```typescript
// Drizzle ORM with pg_trgm
import { sql, desc } from 'drizzle-orm';
import { products } from './schema';

async function searchProducts(query: string, limit = 20) {
  const results = await db
    .select({
      id: products.id,
      name: products.name,
      price: products.price,
      score: sql<number>`
        similarity(${products.name}, ${query}) * 2 +
        similarity(${products.description}, ${query})
      `.as('score'),
    })
    .from(products)
    .where(sql`
      ${products.name} % ${query}
      OR ${products.description} % ${query}
    `)
    .orderBy(desc(sql`score`))
    .limit(limit);

  return results;
}
```

### 2. PostgreSQL Full-Text Search (Built-in FTS)

```sql
-- Add tsvector column with auto-update
ALTER TABLE articles ADD COLUMN search_vector tsvector
  GENERATED ALWAYS AS (
    setweight(to_tsvector('english', coalesce(title, '')), 'A') ||
    setweight(to_tsvector('english', coalesce(subtitle, '')), 'B') ||
    setweight(to_tsvector('english', coalesce(body, '')), 'C') ||
    setweight(to_tsvector('english', coalesce(tags_text, '')), 'B')
  ) STORED;

-- GIN index for fast search
CREATE INDEX idx_articles_search ON articles USING gin(search_vector);

-- Search with ranking and highlighting
SELECT
  id,
  title,
  ts_rank_cd(search_vector, query) AS rank,
  ts_headline('english', body, query,
    'StartSel=<mark>, StopSel=</mark>, MaxFragments=2, MaxWords=30'
  ) AS snippet
FROM articles,
  websearch_to_tsquery('english', 'typescript database migration') AS query
WHERE search_vector @@ query
ORDER BY rank DESC
LIMIT 20;

-- Phrase search
SELECT * FROM articles
WHERE search_vector @@ phraseto_tsquery('english', 'react server components');

-- Prefix search (for autocomplete)
SELECT * FROM articles
WHERE search_vector @@ to_tsquery('english', 'react:* & server:*');
```

```typescript
// TypeScript wrapper for PostgreSQL FTS
async function fullTextSearch(query: string, options: {
  limit?: number;
  offset?: number;
  category?: string;
} = {}) {
  const { limit = 20, offset = 0, category } = options;

  const results = await db.execute(sql`
    SELECT
      a.id,
      a.title,
      a.slug,
      a.published_at,
      ts_rank_cd(a.search_vector, query) AS rank,
      ts_headline('english', a.body, query,
        'StartSel=<mark>, StopSel=</mark>, MaxFragments=2, MaxWords=30'
      ) AS snippet
    FROM articles a,
      websearch_to_tsquery('english', ${query}) AS query
    WHERE a.search_vector @@ query
      ${category ? sql`AND a.category = ${category}` : sql``}
      AND a.published_at IS NOT NULL
    ORDER BY rank DESC
    LIMIT ${limit}
    OFFSET ${offset}
  `);

  return results.rows;
}
```

### 3. MeiliSearch (Self-Hosted, Instant Search)

```bash
# Docker setup
docker run -d --name meilisearch \
  -p 7700:7700 \
  -e MEILI_MASTER_KEY='your-master-key' \
  -v meili_data:/meili_data \
  getmeili/meilisearch:latest
```

```typescript
// src/lib/search.ts
import { MeiliSearch } from 'meilisearch';

const client = new MeiliSearch({
  host: process.env.MEILISEARCH_URL ?? 'http://localhost:7700',
  apiKey: process.env.MEILISEARCH_MASTER_KEY,
});

// Configure index
async function setupSearchIndex() {
  const index = client.index('products');

  await index.updateSettings({
    // Fields to search (ordered by priority)
    searchableAttributes: ['name', 'description', 'brand', 'tags'],
    // Fields returned in results
    displayedAttributes: ['id', 'name', 'description', 'price', 'image_url', 'brand'],
    // Filterable fields (for faceted search)
    filterableAttributes: ['category', 'brand', 'price', 'in_stock', 'rating'],
    // Sortable fields
    sortableAttributes: ['price', 'rating', 'created_at'],
    // Typo tolerance
    typoTolerance: {
      enabled: true,
      minWordSizeForTypos: { oneTypo: 4, twoTypos: 8 },
    },
    // Ranking rules (order matters)
    rankingRules: [
      'words',        // Number of matched words
      'typo',         // Fewer typos ranked higher
      'proximity',    // Matched words closer together ranked higher
      'attribute',    // Match in name > match in description
      'sort',         // User-requested sort
      'exactness',    // Exact match > prefix match
      'rating:desc',  // Custom: higher rated first
    ],
    // Synonyms
    synonyms: {
      phone: ['smartphone', 'mobile', 'cell phone'],
      laptop: ['notebook', 'computer'],
      tv: ['television', 'monitor', 'screen'],
    },
  });
}

// Index documents
async function indexProducts(products: Product[]) {
  const index = client.index('products');
  // MeiliSearch handles batching internally
  const task = await index.addDocuments(products, { primaryKey: 'id' });
  // Optionally wait for indexing to complete
  await client.waitForTask(task.taskUid);
}

// Search
async function searchProducts(query: string, options: {
  category?: string;
  minPrice?: number;
  maxPrice?: number;
  sort?: 'price:asc' | 'price:desc' | 'rating:desc';
  page?: number;
  hitsPerPage?: number;
} = {}) {
  const index = client.index('products');

  const filters: string[] = [];
  if (options.category) filters.push(`category = "${options.category}"`);
  if (options.minPrice) filters.push(`price >= ${options.minPrice}`);
  if (options.maxPrice) filters.push(`price <= ${options.maxPrice}`);
  filters.push('in_stock = true');

  const results = await index.search(query, {
    filter: filters.join(' AND '),
    sort: options.sort ? [options.sort] : undefined,
    page: options.page ?? 1,
    hitsPerPage: options.hitsPerPage ?? 20,
    attributesToHighlight: ['name', 'description'],
    highlightPreTag: '<mark>',
    highlightPostTag: '</mark>',
    attributesToCrop: ['description'],
    cropLength: 30,
    showMatchesPosition: true,
  });

  return {
    hits: results.hits,
    totalHits: results.totalHits,
    page: results.page,
    totalPages: results.totalPages,
    processingTimeMs: results.processingTimeMs,
    facets: results.facetDistribution,
  };
}
```

### 4. Algolia (Managed, Highest Quality)

```typescript
// src/lib/algolia.ts
import algoliasearch from 'algoliasearch';

const client = algoliasearch(
  process.env.ALGOLIA_APP_ID!,
  process.env.ALGOLIA_ADMIN_KEY!
);

const index = client.initIndex('products');

// Configure index settings (run once)
async function configureIndex() {
  await index.setSettings({
    searchableAttributes: [
      'name',           // Most important
      'brand',
      'description',
      'tags',           // Least important
    ],
    attributesForFaceting: [
      'searchable(brand)',
      'filterOnly(in_stock)',
      'category',
      'price_range',
    ],
    customRanking: ['desc(rating)', 'desc(sales_count)'],
    distinct: 1,
    attributeForDistinct: 'product_group_id',
    typoTolerance: true,
    queryLanguages: ['en'],
    removeStopWords: true,
    ignorePlurals: true,
    hitsPerPage: 20,
  });
}

// Sync data (use webhooks or cron for production)
async function syncProducts(products: Product[]) {
  const objects = products.map((p) => ({
    objectID: p.id,
    name: p.name,
    description: p.description,
    brand: p.brand,
    category: p.category,
    price: p.price,
    price_range: getPriceRange(p.price),
    rating: p.rating,
    sales_count: p.salesCount,
    in_stock: p.stock > 0,
    image_url: p.imageUrl,
    tags: p.tags,
  }));

  // Partial updates (only changed fields)
  await index.partialUpdateObjects(objects, { createIfNotExists: true });
}

// Search (client-side key -- safe to expose)
const searchClient = algoliasearch(
  process.env.NEXT_PUBLIC_ALGOLIA_APP_ID!,
  process.env.NEXT_PUBLIC_ALGOLIA_SEARCH_KEY! // Read-only key
);
```

### 5. Search UX: Autocomplete Component

```tsx
// src/components/search-bar.tsx
'use client';

import { useState, useRef, useEffect, useCallback } from 'react';

interface SearchResult {
  id: string;
  title: string;
  subtitle?: string;
  url: string;
  highlight?: string;
}

interface SearchBarProps {
  onSearch: (query: string) => Promise<SearchResult[]>;
  placeholder?: string;
  debounceMs?: number;
}

export function SearchBar({
  onSearch,
  placeholder = 'Search...',
  debounceMs = 200,
}: SearchBarProps) {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState<SearchResult[]>([]);
  const [isOpen, setIsOpen] = useState(false);
  const [activeIndex, setActiveIndex] = useState(-1);
  const [isLoading, setIsLoading] = useState(false);
  const inputRef = useRef<HTMLInputElement>(null);
  const listRef = useRef<HTMLUListElement>(null);
  const abortRef = useRef<AbortController | null>(null);

  // Debounced search
  useEffect(() => {
    if (query.length < 2) {
      setResults([]);
      setIsOpen(false);
      return;
    }

    const timer = setTimeout(async () => {
      abortRef.current?.abort();
      abortRef.current = new AbortController();

      setIsLoading(true);
      try {
        const hits = await onSearch(query);
        setResults(hits);
        setIsOpen(hits.length > 0);
        setActiveIndex(-1);
      } catch {
        // Ignore abort errors
      } finally {
        setIsLoading(false);
      }
    }, debounceMs);

    return () => clearTimeout(timer);
  }, [query, onSearch, debounceMs]);

  const handleKeyDown = useCallback(
    (e: React.KeyboardEvent) => {
      switch (e.key) {
        case 'ArrowDown':
          e.preventDefault();
          setActiveIndex((i) => Math.min(i + 1, results.length - 1));
          break;
        case 'ArrowUp':
          e.preventDefault();
          setActiveIndex((i) => Math.max(i - 1, -1));
          break;
        case 'Enter':
          e.preventDefault();
          if (activeIndex >= 0 && results[activeIndex]) {
            window.location.href = results[activeIndex].url;
          }
          break;
        case 'Escape':
          setIsOpen(false);
          inputRef.current?.blur();
          break;
      }
    },
    [results, activeIndex]
  );

  // Close on outside click
  useEffect(() => {
    const handler = (e: MouseEvent) => {
      if (!listRef.current?.contains(e.target as Node) &&
          !inputRef.current?.contains(e.target as Node)) {
        setIsOpen(false);
      }
    };
    document.addEventListener('mousedown', handler);
    return () => document.removeEventListener('mousedown', handler);
  }, []);

  return (
    <div className="relative w-full max-w-xl" role="combobox" aria-expanded={isOpen}>
      <div className="relative">
        <svg
          className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400"
          fill="none" viewBox="0 0 24 24" stroke="currentColor"
        >
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
            d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
        </svg>
        <input
          ref={inputRef}
          type="search"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onFocus={() => results.length > 0 && setIsOpen(true)}
          onKeyDown={handleKeyDown}
          placeholder={placeholder}
          className="w-full px-4 py-3 pl-12 rounded-lg border border-gray-200
                     text-base bg-white shadow-sm
                     transition-all duration-200
                     focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2
                     focus-visible:outline-none
                     motion-reduce:transition-none"
          role="searchbox"
          aria-autocomplete="list"
          aria-controls="search-results"
          aria-activedescendant={activeIndex >= 0 ? `result-${activeIndex}` : undefined}
        />
        {isLoading && (
          <div className="absolute right-4 top-1/2 -translate-y-1/2">
            <div className="w-4 h-4 border-2 border-gray-300 border-t-blue-500 rounded-full animate-spin" />
          </div>
        )}
      </div>

      {isOpen && (
        <ul
          ref={listRef}
          id="search-results"
          role="listbox"
          className="absolute z-50 w-full mt-2 bg-white rounded-xl border border-gray-200
                     shadow-lg overflow-hidden max-h-96 overflow-y-auto"
        >
          {results.map((result, i) => (
            <li
              key={result.id}
              id={`result-${i}`}
              role="option"
              aria-selected={i === activeIndex}
              className={`px-4 py-3 cursor-pointer transition-colors duration-150
                ${i === activeIndex ? 'bg-blue-50' : 'hover:bg-gray-50'}
                ${i > 0 ? 'border-t border-gray-100' : ''}`}
              onMouseEnter={() => setActiveIndex(i)}
              onClick={() => { window.location.href = result.url; }}
            >
              <div className="text-base font-medium text-gray-900"
                dangerouslySetInnerHTML={{ __html: result.highlight ?? result.title }}
              />
              {result.subtitle && (
                <div className="text-sm text-gray-500 mt-0.5">{result.subtitle}</div>
              )}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
```

### 6. Database-to-Search Sync

```typescript
// src/jobs/search-sync.ts
// Keep search index in sync with database changes

import { db } from '@/db';
import { products } from '@/db/schema';
import { gt, sql } from 'drizzle-orm';

const BATCH_SIZE = 500;

// Incremental sync using updated_at timestamp
async function incrementalSync(searchIndex: SearchIndex, since: Date) {
  let offset = 0;
  let synced = 0;

  while (true) {
    const batch = await db
      .select()
      .from(products)
      .where(gt(products.updatedAt, since))
      .orderBy(products.updatedAt)
      .limit(BATCH_SIZE)
      .offset(offset);

    if (batch.length === 0) break;

    await searchIndex.addDocuments(
      batch.map(transformForSearch),
      { primaryKey: 'id' }
    );

    synced += batch.length;
    offset += BATCH_SIZE;

    // Avoid hammering the DB
    if (batch.length === BATCH_SIZE) {
      await new Promise((r) => setTimeout(r, 100));
    }
  }

  return synced;
}

// Full reindex (for schema changes or corruption)
async function fullReindex(searchIndex: SearchIndex) {
  // Create a new index, swap when done (zero-downtime)
  const tempIndex = client.index('products_temp');

  await tempIndex.updateSettings({ /* same settings */ });

  let offset = 0;
  while (true) {
    const batch = await db
      .select()
      .from(products)
      .limit(BATCH_SIZE)
      .offset(offset);

    if (batch.length === 0) break;

    await tempIndex.addDocuments(batch.map(transformForSearch));
    offset += BATCH_SIZE;
  }

  // Atomic swap
  await client.swapIndexes([{ indexes: ['products', 'products_temp'] }]);
  await client.index('products_temp').delete();
}

function transformForSearch(product: typeof products.$inferSelect) {
  return {
    id: product.id,
    name: product.name,
    description: product.description?.slice(0, 500), // Limit field size
    brand: product.brand,
    category: product.category,
    price: product.price,
    rating: product.rating,
    in_stock: product.stock > 0,
    tags: product.tags,
  };
}
```

## Best Practices

1. **Start with PostgreSQL** -- pg_trgm and FTS handle most use cases under 1M rows with zero extra infra
2. **Debounce autocomplete** -- 150-250ms delay prevents hammering your search backend
3. **Return results in < 100ms** -- users perceive > 200ms as slow for search
4. **Show results as-you-type** -- do not require pressing Enter; update on every keystroke (debounced)
5. **Highlight matched terms** -- users need to see why a result matched
6. **Include faceted filtering** -- category, price range, brand filters alongside search
7. **Handle zero results gracefully** -- suggest corrections, related terms, or popular items
8. **Log search queries** -- the single most valuable analytics for product improvement
9. **Use synonyms and stop words** -- "tv" should match "television"; "the" should be ignored
10. **Separate search API key from admin key** -- Algolia/MeiliSearch search keys are safe for client-side

## Common Pitfalls

| Pitfall | Impact | Fix |
|---------|--------|-----|
| No debounce on keystroke search | API hammered, rate limits hit | Debounce 150-250ms, abort previous requests |
| Syncing search index synchronously | Slow writes, failed search updates block UX | Use background jobs, event-driven sync |
| Not tokenizing properly | "don't" fails to match "dont" | Configure tokenizer, use unaccent extension |
| Returning entire documents | Slow network, wasted bandwidth | Return only needed fields (id, title, snippet) |
| Case-sensitive search | "React" does not match "react" | Normalize to lowercase in index and query |
| No relevance tuning | Title matches ranked same as body matches | Weight searchable attributes (title > body) |
| Single search field for everything | Users cannot filter results | Add faceted filters (category, date, type) |
| Stale search index | Search returns deleted/outdated content | Webhook-based sync or frequent incremental sync |
