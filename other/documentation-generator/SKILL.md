---
name: documentation-generator
version: "2.0"
trigger: documentation, README, API docs, auto-document, JSDoc
description: Automated documentation generation, API documentation, code comments, README templates, and knowledge base maintenance. Use when creating documentation, updating READMEs, generating API docs, or maintaining project documentation.
---

# Documentation Generator

## README Templates

### Project README
```markdown
# Project Name

[![CI](https://github.com/org/repo/actions/workflows/ci.yml/badge.svg)](https://github.com/org/repo/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/org/repo/branch/main/graph/badge.svg)](https://codecov.io/gh/org/repo)

> Brief project description

## Features

- Feature 1
- Feature 2
- Feature 3

## Tech Stack

- Next.js 16
- TypeScript 5
- PostgreSQL
- Drizzle ORM

## Quick Start

\`\`\`bash
# Clone
git clone https://github.com/org/repo.git
cd repo

# Install
pnpm install

# Environment
cp .env.example .env.local

# Database
pnpm db:migrate
pnpm db:seed

# Development
pnpm dev
\`\`\`

## Documentation

- [API Documentation](./docs/API.md)
- [Architecture](./docs/ARCHITECTURE.md)
- [Contributing](./CONTRIBUTING.md)

## License

MIT
```

## API Documentation Generation

### OpenAPI/Swagger
```typescript
// Generate OpenAPI spec from routes
import { OpenAPIRegistry } from '@asteasolutions/zod-to-openapi';

const registry = new OpenAPIRegistry();

registry.registerPath({
  method: 'get',
  path: '/api/users',
  description: 'List all users',
  request: {
    query: listUsersQuerySchema
  },
  responses: {
    200: {
      description: 'List of users',
      content: {
        'application/json': {
          schema: z.array(userSchema)
        }
      }
    }
  }
});

// Generate spec
export const openApiSpec = new OpenApiGeneratorV3(registry.definitions).generateDocument({
  openapi: '3.0.0',
  info: {
    title: 'Trinity API',
    version: '1.0.0'
  }
});
```

### TypeDoc Configuration
```json
{
  "entryPoints": ["src/index.ts"],
  "out": "docs/api",
  "theme": "default",
  "exclude": ["**/*.test.ts", "**/node_modules/**"],
  "excludePrivate": true,
  "excludeProtected": true,
  "excludeExternals": true,
  "readme": "README.md",
  "name": "Trinity API",
  "includeVersion": true
}
```

## Code Comment Standards

### JSDoc Comments
```typescript
/**
 * Calculates the trust score for a user based on their interactions.
 * 
 * @param userId - The unique identifier of the user
 * @param interactions - Array of user interactions to analyze
 * @param options - Configuration options for the calculation
 * @returns Promise resolving to the calculated trust score [0, 1]
 * @throws {NotFoundError} If user is not found
 * @throws {ValidationError} If interactions array is empty
 * 
 * @example
 * ```typescript
 * const score = await calculateTrustScore('user-123', interactions, {
 *   timeWindow: '30d',
 *   weightRecent: true
 * });
 * ```
 */
export async function calculateTrustScore(
  userId: string,
  interactions: Interaction[],
  options: TrustScoreOptions = {}
): Promise<number> {
  // Implementation
}
```

### Architecture Decision Records (ADRs)
```markdown
# ADR-001: Use Drizzle ORM

## Status
Accepted

## Context
We needed to choose an ORM for our PostgreSQL database.

## Decision
We will use Drizzle ORM because:
- Type-safe SQL-like syntax
- Better performance than Prisma
- Smaller bundle size
- Native migration support

## Consequences
- Team needs to learn Drizzle syntax
- Less community support than Prisma
```

## Automated Documentation

### Change Log Generation
```typescript
// scripts/generate-changelog.ts
import { generateChangelog } from 'conventional-changelog';

async function updateChangelog() {
  const changelog = await generateChangelog({
    preset: 'angular'
  });
  
  await fs.writeFile('CHANGELOG.md', changelog);
}
```

### API Endpoint Documentation
```typescript
// scripts/generate-api-docs.ts
import { parseSourceFile } from 'ts-morph';

function generateEndpointDocs() {
  const project = new Project();
  const routeFiles = project.getSourceFiles('**/routes.ts');
  
  const endpoints = routeFiles.flatMap(file => 
    extractEndpoints(file)
  );
  
  const markdown = generateMarkdown(endpoints);
  fs.writeFileSync('docs/API_ENDPOINTS.md', markdown);
}
```

## Knowledge Base Maintenance

### Confluence Integration
```typescript
export class ConfluencePublisher {
  async publishPage(title: string, content: string) {
    await this.client.post('/rest/api/content', {
      type: 'page',
      title,
      body: {
        storage: {
          value: content,
          representation: 'storage'
        }
      }
    });
  }
}
```

### Notion Documentation
```typescript
export class NotionDocSync {
  async syncApiDocs(endpoints: Endpoint[]) {
    for (const endpoint of endpoints) {
      await this.notion.pages.create({
        parent: { database_id: this.docsDbId },
        properties: {
          Name: { title: [{ text: { content: endpoint.name } }] },
          Method: { select: { name: endpoint.method } },
          Path: { rich_text: [{ text: { content: endpoint.path } }] },
          Status: { select: { name: 'Documented' } }
        }
      });
    }
  }
}
```
