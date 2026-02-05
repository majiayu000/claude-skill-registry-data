---
name: context7-usage
description: Tips and best practices for using Context7 MCP server to get library documentation
---

# Context7 Usage Guide

This skill provides guidance for using the Context7 MCP server effectively.

## Overview

Context7 provides documentation lookup for popular libraries and frameworks. It has two main tools:
- `resolveLibraryId` - Find the library ID for a given library name
- `getLibraryDocs` - Get documentation for a specific topic

## Resolving Library IDs

The `resolveLibraryId` tool returns results that are **automatically parsed** into structured objects. The response includes:

```typescript
{
  libraries: Array<{
    id: string;           // Context7-compatible library ID
    name: string;         // Library title
    description: string;  // Short description
    codeSnippets: number; // Number of code examples
    sourceReputation: string; // "High", "Medium", "Low", or "Unknown"
    benchmarkScore?: number;  // Quality score (optional)
  }>;
  raw: string;  // Original text response
}
```

Here's how to pick the right library:

### Library ID Naming Patterns

| Pattern | Description | Example |
|---------|-------------|---------|
| `/websites/<name>` | Official documentation (usually best) | `/websites/laravel` |
| `/websites/<name>-<version>` | Version-specific docs | `/websites/laravel-11.x` |
| `/websites/<name>_<version>` | Version-specific (alt format) | `/websites/laravel_12_x` |
| `/<org>/<repo>` | GitHub repository content | `/laravel/laravel` |

### Recommended Library IDs by Framework

| Framework | Recommended ID | Notes |
|-----------|---------------|-------|
| **Laravel 12** | `/websites/laravel_12_x` | Latest version |
| **Laravel 11** | `/websites/laravel-11.x` | Previous LTS |
| **Laravel (latest)** | `/websites/laravel` | General docs |
| **React** | `/websites/react` | Official React docs |
| **Vue 3** | `/websites/vue` | Vue.js documentation |
| **Next.js** | `/websites/nextjs` | Next.js framework |
| **TypeScript** | `/websites/typescript` | TS documentation |
| **Node.js** | `/websites/nodejs` | Node.js docs |

### Selection Tips

1. **Look for "High" reputation** - Libraries with high reputation have better quality content
2. **Check snippet count** - More snippets = more comprehensive content
3. **Use version-specific IDs** - When you need docs for a specific version
4. **Prefer `/websites/` prefix** - These are usually official documentation

## Using getLibraryDocs

### Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `context7CompatibleLibraryID` | Yes | The library ID from resolveLibraryId |
| `topic` | Yes | What you want to learn about |
| `mode` | No | `"code"` for examples, `"docs"` for explanations |

### Example Usage

```typescript
import { resolveLibraryId, getLibraryDocs } from '../servers/context7/index.js';

// Step 1: Find the library - result is automatically parsed
const result = await resolveLibraryId.call({ libraryName: "Laravel" });

// Step 2: Access the parsed libraries array
console.log(`Found ${result.libraries.length} libraries`);

// Step 3: Find best match programmatically
const best = result.libraries
  .filter(lib => lib.sourceReputation === 'High')
  .sort((a, b) => b.codeSnippets - a.codeSnippets)[0];

// Step 4: Get documentation using the library ID
const docs = await getLibraryDocs.call({
  context7CompatibleLibraryID: best?.id || "/websites/laravel_12_x",
  topic: "middleware",
  mode: "code"  // Get code examples
});
console.log(docs);
```

### Using Known Library IDs (Faster)

Skip the resolve step when you know the library ID:

```typescript
// Direct usage with known IDs
const docs = await getLibraryDocs.call({
  context7CompatibleLibraryID: "/websites/laravel_12_x",
  topic: "middleware"
});
```

### Mode Options

- `"code"` - Returns code examples and snippets (best for implementation)
- `"docs"` - Returns explanatory documentation (best for understanding concepts)

## Common Issues

### Too Many Results from resolveLibraryId

**Problem:** You get 30+ results and don't know which to pick.

**Solution:** Use the parsed `libraries` array to filter programmatically:

```typescript
const result = await resolveLibraryId.call({ libraryName: "React" });

// Filter to high-reputation libraries with many snippets
const best = result.libraries
  .filter(lib => lib.sourceReputation === 'High' && lib.codeSnippets > 100)
  .sort((a, b) => b.codeSnippets - a.codeSnippets);

console.log('Best matches:', best.map(l => `${l.name} (${l.id})`));
```

Or use the recommended IDs table above for common frameworks.

### Library ID Not Found

**Problem:** `getLibraryDocs` fails with "library not found".

**Solution:**
1. Run `resolveLibraryId` first to get valid IDs
2. Copy the exact ID from the results (case-sensitive)
3. Check for typos in the library ID

## Quick Reference

```typescript
// Common library IDs (no need to resolve)
const LIBRARY_IDS = {
  laravel12: "/websites/laravel_12_x",
  laravel11: "/websites/laravel-11.x",
  react: "/websites/react",
  vue: "/websites/vue",
  nextjs: "/websites/nextjs",
  typescript: "/websites/typescript",
  nodejs: "/websites/nodejs",
};