---
name: docs-fetcher
description: This skill allows the assistant to fetch documentation for various libraries and packages directly from the web. It supports searching by package name (e.g., npm, pip) or directly by URL. Use it whenever you need to understand how to use a specific programming library, API, or framework.
---

# Docs Fetcher

## Overview

This skill leverages the `docsFetcher` MCP server to retrieve up-to-date documentation for software libraries and packages. It's particularly useful for exploring unfamiliar APIs or getting the latest usage examples without manually searching the web.

## Core Capabilities

### 1. Fetch by URL
Directly retrieve documentation from a specific website URL.
- `fetch-url-docs(url: string)`: Fetch content from the provided URI.

### 2. Fetch by Package Name
Get documentation for a package in a specific programming ecosystem.
- `fetch-package-docs(packageName: string, language?: string)`: Search for a package. `language` can be `javascript`, `python`, `java`, `dotnet`, etc.

### 3. General Library Fetch
A flexible tool that accepts either a package name or a direct URL.
- `fetch-library-docs(library: string, language?: string)`: The `library` parameter can be a name or a URL.

### 4. Multilingual Search
Check for documentation across multiple programming languages for the same package name.
- `fetch-multilingual-docs(packageName: string, languages: string[])`: Takes a list of languages to check.

## Usage

All tools are executed via `mcporter call docsFetcher.<tool_name>`.

**Example: Fetching documentation for a specific URL**
```bash
mcporter call docsFetcher.fetch-url-docs url="https://docs.npmjs.com/cli/v10/commands/npm-install"
```

**Example: Fetching documentation for a Python package**
```bash
mcporter call docsFetcher.fetch-package-docs packageName="pandas" language="python"
```

**Note:** The `docsFetcher` MCP server must be configured via `mcporter` for this skill to work.

## Resources

### scripts/
- `docs-fetcher.ts`: The TypeScript interface for the `docsFetcher` MCP server.
