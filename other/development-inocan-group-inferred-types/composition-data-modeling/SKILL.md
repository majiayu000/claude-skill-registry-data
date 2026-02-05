---
name: Composition Data Modeling
description: Design and work with composition data structures. Use when defining schemas, creating database models, building API responses, or transforming composition data between formats.
---

# Composition Data Modeling Skill

## Purpose

This skill provides patterns for modeling composition data - the hierarchical structure that represents what things are made of, from product down to elements.

## Core Data Model

### TypeScript Types

```typescript
// types/composition.ts

export type ConfidenceLevel = 'verified' | 'estimated' | 'speculative'
export type CompositionType = 'product' | 'component' | 'material' | 'chemical' | 'element'

export interface CompositionNode {
  id: string
  name: string
  description?: string
  type: CompositionType

  // Quantity
  percentage: number
  percentageRange?: [number, number]  // For uncertain values
  unit?: string                        // 'weight' | 'volume' | 'count'

  // Confidence & Source
  confidence: ConfidenceLevel
  source?: string
  sourceUrl?: string

  // Hierarchy
  children?: CompositionNode[]

  // Element-specific (when type === 'element')
  symbol?: string           // Periodic table symbol
  atomicNumber?: number

  // Visual config
  visualConfig?: {
    color?: string
    material?: 'metal' | 'glass' | 'organic' | 'standard'
    modelUrl?: string
  }

  // Metadata
  metadata?: Record<string, unknown>
}

export interface Composition {
  id: string
  query: string              // Original search query
  name: string               // Identified product name
  category: string           // Product category
  description?: string

  root: CompositionNode      // Top-level composition tree

  sources: Source[]
  confidence: ConfidenceLevel  // Overall confidence

  // Timestamps
  createdAt: Date
  updatedAt: Date
  researchedAt: Date         // When AI research was performed
}

export interface Source {
  id: string
  url: string
  title: string
  type: 'official' | 'scientific' | 'analysis' | 'industry' | 'secondary'
  accessedAt: Date
  reliability: number        // 0-1 score
}
```

### Prisma Schema

```prisma
// prisma/schema.prisma

model Composition {
  id            String   @id @default(cuid())
  query         String   @db.Text
  queryNorm     String   // Normalized for search
  name          String
  category      String
  description   String?  @db.Text

  // Store full tree as JSON
  rootData      Json     @map("root_data")
  sourcesData   Json     @map("sources_data")

  confidence    String   // 'verified' | 'estimated' | 'speculative'

  // Stats
  viewCount     Int      @default(0)
  shareCount    Int      @default(0)

  // Timestamps
  createdAt     DateTime @default(now()) @map("created_at")
  updatedAt     DateTime @updatedAt @map("updated_at")
  researchedAt  DateTime @map("researched_at")

  // Relations
  shares        Share[]

  @@index([queryNorm])
  @@index([category])
  @@index([viewCount(sort: Desc)])
  @@map("compositions")
}

model Share {
  id            String      @id @default(cuid())
  shortCode     String      @unique
  compositionId String      @map("composition_id")
  composition   Composition @relation(fields: [compositionId], references: [id])

  // Share config
  depthLevel    Int         @default(4) @map("depth_level")
  viewMode      String      @default("exploded") @map("view_mode")

  // Stats
  viewCount     Int         @default(0) @map("view_count")

  createdAt     DateTime    @default(now()) @map("created_at")

  @@index([shortCode])
  @@map("shares")
}
```

## API Response Formats

### Search Response
```typescript
interface SearchResponse {
  success: true
  data: {
    composition: Composition
    cached: boolean
    researchTime?: number  // ms, if freshly researched
  }
}

interface SearchErrorResponse {
  success: false
  error: {
    code: 'INVALID_QUERY' | 'RESEARCH_FAILED' | 'RATE_LIMITED'
    message: string
  }
}

// For long-running research
interface SearchPendingResponse {
  success: true
  status: 'researching'
  jobId: string
  estimatedTime: number  // seconds
  progress?: {
    stage: 'identifying' | 'researching' | 'synthesizing'
    percentage: number
  }
}
```

### Composition Response
```typescript
interface CompositionResponse {
  success: true
  data: {
    composition: Composition
    // Flattened for easier rendering
    nodes: CompositionNode[]
    maxDepth: number
    totalElements: number
  }
}
```

## Data Transformations

### Flatten Tree for Rendering
```typescript
function flattenComposition(
  node: CompositionNode,
  depth = 0,
  parentId?: string
): FlatNode[] {
  const flat: FlatNode = {
    ...node,
    depth,
    parentId,
    childIds: node.children?.map(c => c.id) ?? []
  }

  const children = node.children?.flatMap(child =>
    flattenComposition(child, depth + 1, node.id)
  ) ?? []

  return [flat, ...children]
}
```

### Calculate Totals by Depth
```typescript
function calculateDepthTotals(root: CompositionNode): DepthSummary[] {
  const summaries: Map<number, DepthSummary> = new Map()

  function traverse(node: CompositionNode, depth: number) {
    const summary = summaries.get(depth) ?? {
      depth,
      nodeCount: 0,
      types: {}
    }
    summary.nodeCount++
    summary.types[node.type] = (summary.types[node.type] ?? 0) + 1
    summaries.set(depth, summary)

    node.children?.forEach(c => traverse(c, depth + 1))
  }

  traverse(root, 0)
  return Array.from(summaries.values())
}
```

### Filter by Depth Level
```typescript
function filterByDepth(
  node: CompositionNode,
  maxDepth: number,
  currentDepth = 0
): CompositionNode {
  if (currentDepth >= maxDepth) {
    return { ...node, children: undefined }
  }

  return {
    ...node,
    children: node.children?.map(c =>
      filterByDepth(c, maxDepth, currentDepth + 1)
    )
  }
}
```

### Calculate Element Totals
```typescript
function calculateElementTotals(
  node: CompositionNode,
  parentPercentage = 100
): Map<string, number> {
  const totals = new Map<string, number>()
  const effectivePercentage = (node.percentage / 100) * parentPercentage

  if (node.type === 'element' && node.symbol) {
    totals.set(node.symbol, effectivePercentage)
  }

  node.children?.forEach(child => {
    const childTotals = calculateElementTotals(child, effectivePercentage)
    childTotals.forEach((value, key) => {
      totals.set(key, (totals.get(key) ?? 0) + value)
    })
  })

  return totals
}
```

## Caching Strategy

### Redis Cache Keys
```typescript
// Hot cache for popular queries
`composition:query:${normalizeQuery(query)}`  // TTL: 1 hour

// Composition by ID
`composition:id:${id}`  // TTL: 24 hours

// Popular compositions list
`compositions:popular`  // TTL: 15 minutes

// Search suggestions
`search:suggestions:${prefix}`  // TTL: 1 hour
```

### Cache Invalidation
```typescript
async function invalidateCompositionCache(id: string, query: string) {
  await redis.del([
    `composition:id:${id}`,
    `composition:query:${normalizeQuery(query)}`,
    'compositions:popular'
  ])
}
```

## Validation

```typescript
import { z } from 'zod'

const CompositionNodeSchema: z.ZodType<CompositionNode> = z.lazy(() =>
  z.object({
    id: z.string(),
    name: z.string().min(1),
    description: z.string().optional(),
    type: z.enum(['product', 'component', 'material', 'chemical', 'element']),
    percentage: z.number().min(0).max(100),
    percentageRange: z.tuple([z.number(), z.number()]).optional(),
    confidence: z.enum(['verified', 'estimated', 'speculative']),
    source: z.string().optional(),
    sourceUrl: z.string().url().optional(),
    children: z.array(CompositionNodeSchema).optional(),
    symbol: z.string().length(1, 2).optional(),
    atomicNumber: z.number().int().positive().optional(),
    visualConfig: z.object({
      color: z.string().optional(),
      material: z.enum(['metal', 'glass', 'organic', 'standard']).optional(),
      modelUrl: z.string().url().optional()
    }).optional(),
    metadata: z.record(z.unknown()).optional()
  })
)

export const CompositionSchema = z.object({
  id: z.string(),
  query: z.string().min(2),
  name: z.string().min(1),
  category: z.string(),
  description: z.string().optional(),
  root: CompositionNodeSchema,
  sources: z.array(z.object({
    id: z.string(),
    url: z.string().url(),
    title: z.string(),
    type: z.enum(['official', 'scientific', 'analysis', 'industry', 'secondary']),
    accessedAt: z.date(),
    reliability: z.number().min(0).max(1)
  })),
  confidence: z.enum(['verified', 'estimated', 'speculative']),
  createdAt: z.date(),
  updatedAt: z.date(),
  researchedAt: z.date()
})
```
