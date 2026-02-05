---
name: documentation-generation
description: "Automated documentation generation patterns. Covers TSDoc, JSDoc, OpenAPI, README templates, and documentation-as-code workflows."
version: 1.0.0
triggers:
  - documentation
  - tsdoc
  - jsdoc
  - openapi
  - readme
  - docs generation
---

# Documentation Generation Skill

Create and maintain high-quality documentation with automated generation tools.

## TSDoc / JSDoc Standards

### Function Documentation

```typescript
/**
 * Calculates the total price including tax and discounts.
 *
 * @param items - Array of cart items to calculate
 * @param taxRate - Tax rate as decimal (e.g., 0.08 for 8%)
 * @param discountCode - Optional discount code to apply
 * @returns The calculated total with tax and discounts applied
 *
 * @example
 * ```ts
 * const total = calculateTotal(
 *   [{ price: 100, quantity: 2 }],
 *   0.08,
 *   'SAVE10'
 * );
 * // Returns: 194.40
 * ```
 *
 * @throws {InvalidDiscountError} If discount code is invalid
 * @see {@link applyDiscount} for discount logic
 */
export function calculateTotal(
  items: CartItem[],
  taxRate: number,
  discountCode?: string
): number {
  // Implementation
}
```

### Interface Documentation

```typescript
/**
 * Represents a user in the system.
 *
 * @remarks
 * Users are created during registration and can have
 * multiple roles assigned for authorization.
 */
export interface User {
  /** Unique identifier (UUID v4) */
  id: string;

  /** Email address (must be unique) */
  email: string;

  /** Display name shown in UI */
  name: string;

  /**
   * User roles for authorization.
   * @defaultValue `['user']`
   */
  roles: Role[];

  /** ISO 8601 timestamp of account creation */
  createdAt: string;
}
```

### Component Documentation

```tsx
/**
 * A reusable button component with multiple variants.
 *
 * @example
 * ```tsx
 * <Button variant="primary" onClick={handleSubmit}>
 *   Submit Form
 * </Button>
 * ```
 *
 * @example
 * ```tsx
 * <Button variant="outline" size="sm" disabled>
 *   Loading...
 * </Button>
 * ```
 */
export function Button({
  variant = 'primary',
  size = 'md',
  children,
  ...props
}: ButtonProps) {
  // Implementation
}
```

## API Documentation with OpenAPI

### Generate from Types

```typescript
// lib/openapi.ts
import { generateOpenApi } from '@ts-rest/open-api';
import { contract } from './contract';

export const openApiDocument = generateOpenApi(contract, {
  info: {
    title: 'FrankX API',
    version: '1.0.0',
    description: 'API for the FrankX creator platform',
  },
  servers: [
    { url: 'https://api.frankx.ai', description: 'Production' },
    { url: 'http://localhost:3000', description: 'Development' },
  ],
});

// Serve at /api/docs
export async function GET() {
  return Response.json(openApiDocument);
}
```

### Swagger UI Integration

```tsx
// app/api/docs/page.tsx
'use client';

import SwaggerUI from 'swagger-ui-react';
import 'swagger-ui-react/swagger-ui.css';

export default function ApiDocs() {
  return <SwaggerUI url="/api/openapi.json" />;
}
```

## README Template

```markdown
# Project Name

Brief description of what this project does.

## Features

- Feature 1: Description
- Feature 2: Description

## Quick Start

\`\`\`bash
# Install dependencies
npm install

# Start development server
npm run dev
\`\`\`

## Installation

\`\`\`bash
npm install package-name
\`\`\`

## Usage

\`\`\`typescript
import { Component } from 'package-name';

// Basic usage
const result = Component.doSomething();
\`\`\`

## API Reference

### `functionName(param1, param2)`

Description of what this function does.

**Parameters:**
- `param1` (string): Description
- `param2` (number, optional): Description

**Returns:** `ReturnType` - Description

**Example:**
\`\`\`typescript
const result = functionName('value', 42);
\`\`\`

## Configuration

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `option1` | `string` | `'default'` | Description |
| `option2` | `boolean` | `false` | Description |

## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md) for guidelines.

## License

MIT - see [LICENSE](./LICENSE) for details.
```

## TypeDoc Setup

### Configuration

```json
// typedoc.json
{
  "entryPoints": ["src/index.ts"],
  "out": "docs",
  "plugin": ["typedoc-plugin-markdown"],
  "readme": "README.md",
  "excludePrivate": true,
  "excludeProtected": true,
  "githubPages": true
}
```

### Generate Docs

```bash
# Add to package.json scripts
"scripts": {
  "docs": "typedoc",
  "docs:watch": "typedoc --watch"
}

# Generate
npm run docs
```

## Docusaurus for Documentation Sites

### Project Structure

```
docs/
├── docs/
│   ├── intro.md
│   ├── getting-started/
│   │   ├── installation.md
│   │   └── configuration.md
│   └── api/
│       └── reference.md
├── blog/
├── src/
├── docusaurus.config.js
└── sidebars.js
```

### Configuration

```javascript
// docusaurus.config.js
module.exports = {
  title: 'FrankX Docs',
  tagline: 'Documentation for the FrankX platform',
  url: 'https://docs.frankx.ai',
  baseUrl: '/',

  presets: [
    [
      '@docusaurus/preset-classic',
      {
        docs: {
          sidebarPath: require.resolve('./sidebars.js'),
          editUrl: 'https://github.com/frankxai/docs/edit/main/',
        },
        blog: {
          showReadingTime: true,
        },
        theme: {
          customCss: require.resolve('./src/css/custom.css'),
        },
      },
    ],
  ],
};
```

## Documentation Best Practices

### What to Document

| Document | When |
|----------|------|
| **Public APIs** | Always - every exported function/type |
| **Complex logic** | When not self-evident |
| **Configuration** | All options with defaults |
| **Examples** | For every public API |
| **Breaking changes** | In CHANGELOG |

### Documentation Checklist

- [ ] All public APIs have TSDoc/JSDoc
- [ ] README has quick start guide
- [ ] API reference is generated
- [ ] Examples are tested and working
- [ ] CHANGELOG is updated
- [ ] Migration guides for breaking changes

## Automation

### Pre-commit Hook

```bash
# .husky/pre-commit
npx typedoc --emit none  # Validate docs compile
```

### CI Documentation Build

```yaml
# .github/workflows/docs.yml
name: Documentation

on:
  push:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
      - run: npm ci
      - run: npm run docs

      - name: Deploy to GitHub Pages
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./docs
```

## Anti-Patterns

❌ Documenting obvious code (`// increment i`)
❌ Outdated documentation
❌ No examples
❌ Missing parameter descriptions
❌ Documentation separate from code

✅ Document "why" not "what"
✅ Keep docs near code
✅ Include runnable examples
✅ Automate doc generation
✅ Review docs in PRs
