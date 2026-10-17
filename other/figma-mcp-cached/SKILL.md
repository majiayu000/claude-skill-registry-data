---
name: figma-mcp-cached
description: Cache-enabled Figma Context MCP server with persistent disk caching to reduce API rate limits and improve performance for AI-powered design workflows
triggers:
  - "access Figma designs through MCP"
  - "set up Figma caching for faster API responses"
  - "configure Figma MCP server with disk cache"
  - "reduce Figma API rate limit hits"
  - "prepare and cache Figma files locally"
  - "download images from Figma designs"
  - "get Figma design data with caching"
  - "encrypt Figma cache for security"
---

# Figma MCP Cached

> Skill by [ara.so](https://ara.so) — Design Skills collection.

A cache-enabled Figma Context MCP (Model Context Protocol) server that uses persistent disk caching to dramatically reduce Figma API requests, mitigate rate limiting issues, and improve response times. Built on TypeScript, this MCP server is optimized for AI coding agents in Cursor, Claude Desktop, and other MCP-compatible clients.

## What It Does

- **Persistent Disk Caching**: Stores Figma API responses locally with configurable TTL (time-to-live)
- **Rate Limit Mitigation**: Reduces API calls by 10x+ after initial cache, perfect for free Figma accounts
- **Smart File Preparation**: `figma_prepare_file` tool validates cache, checks nodeIds, and auto-refreshes when needed
- **Force Refresh**: Override cache to fetch latest design updates on demand
- **LRU Memory Cache**: In-memory caching layer to avoid repeated disk I/O
- **Optional Encryption**: AES-256-CBC encryption for sensitive design data
- **Auto Cleanup**: Scheduled cleanup of expired cache files
- **System Integration**: Saves downloaded images to OS-specific Downloads folder by default

## Installation

### For MCP Clients (Cursor, Claude Desktop, etc.)

Add to your MCP configuration file (e.g., `~/.cursor/mcp.json` or `~/Library/Application Support/Claude/claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "figma-mcp-cached": {
      "command": "npx",
      "args": [
        "-y",
        "@pactortester/figma-mcp-cached",
        "--stdio",
        "--figma-api-key=${FIGMA_API_KEY}",
        "--figma-caching={\"ttl\":{\"value\":7,\"unit\":\"d\"}}"
      ]
    }
  }
}
```

### Get Figma API Key

1. Visit [Figma Developer Settings](https://www.figma.com/developers/api#access-tokens)
2. Create a Personal Access Token
3. Set environment variable: `export FIGMA_API_KEY=your_token_here`

### Verify Installation

Restart your MCP client and check that the `figma-mcp-cached` server appears in the tools list with three tools:
- `figma_prepare_file`
- `get_figma_data`
- `download_figma_images`

## Configuration Options

### Basic Configuration

```json
{
  "mcpServers": {
    "figma-mcp-cached": {
      "command": "npx",
      "args": [
        "-y",
        "@pactortester/figma-mcp-cached",
        "--stdio",
        "--figma-api-key=${FIGMA_API_KEY}",
        "--figma-caching={\"ttl\":{\"value\":30,\"unit\":\"d\"}}"
      ]
    }
  }
}
```

### Full Configuration with All Options

```json
{
  "mcpServers": {
    "figma-mcp-cached": {
      "command": "npx",
      "args": [
        "-y",
        "@pactortester/figma-mcp-cached",
        "--stdio",
        "--figma-api-key=${FIGMA_API_KEY}",
        "--figma-caching={\"ttl\":{\"value\":30,\"unit\":\"d\"},\"cacheDir\":\"~/figma-cache\",\"autoCleanup\":true,\"cleanupInterval\":{\"value\":1,\"unit\":\"h\"},\"maxMemoryCacheSize\":200,\"encryptionKey\":\"${FIGMA_CACHE_ENCRYPTION_KEY}\"}"
      ]
    }
  }
}
```

### Configuration Parameters

#### `ttl` (Required)
Cache time-to-live. Units: `ms`, `s`, `m`, `h`, `d`

```json
{"ttl": {"value": 7, "unit": "d"}}  // 7 days
{"ttl": {"value": 2, "unit": "h"}}  // 2 hours
```

#### `cacheDir` (Optional)
Custom cache directory. Defaults:
- **Linux**: `~/.cache/figma-mcp`
- **macOS**: `~/Library/Caches/FigmaMcp`
- **Windows**: `%LOCALAPPDATA%/FigmaMcpCache`

```json
{"cacheDir": "~/my-figma-cache"}
```

#### `autoCleanup` (Optional)
Enable automatic cleanup of expired cache. Default: `true`

```json
{"autoCleanup": true}
```

#### `cleanupInterval` (Optional)
Auto-cleanup frequency. Default: 1 hour

```json
{"cleanupInterval": {"value": 1, "unit": "h"}}
```

#### `maxMemoryCacheSize` (Optional)
Max LRU memory cache entries. Default: `100`

```json
{"maxMemoryCacheSize": 200}
```

#### `encryptionKey` (Optional)
AES-256-CBC encryption key for cache files. Use for sensitive designs.

```json
{"encryptionKey": "${FIGMA_CACHE_ENCRYPTION_KEY}"}
```

## MCP Tools Reference

### 1. figma_prepare_file

**Purpose**: Prepare and validate Figma file cache before fetching data. This tool should ALWAYS be called before `get_figma_data`.

**Parameters**:
```typescript
{
  figmaUrl: string;      // Full Figma URL
  forceRefresh?: boolean; // Force fresh API fetch, bypass cache
}
```

**Usage Pattern**:
```typescript
// Step 1: Prepare file (LLM does this automatically)
await figma_prepare_file({
  figmaUrl: "https://www.figma.com/design/QlQwKAl9abcdhvlfvpM5K/Design?node-id=2777-9428"
});

// Step 2: Get data (LLM does this next)
await get_figma_data({
  fileKey: "QlQwKAl9abcdhvlfvpM5K",
  nodeId: "2777-9428"
});
```

**Force Refresh Example**:
```typescript
// User says: "Get me the latest design updates"
await figma_prepare_file({
  figmaUrl: "https://www.figma.com/design/QlQwKAl9abcdhvlfvpM5K/Design",
  forceRefresh: true  // Bypass cache, fetch from API
});
```

**Return Values**:
- Cache exists & valid → "File is ready, cache is fresh"
- Cache expired or missing → Fetches from API, caches, returns "File prepared and cached"
- Force refresh → Always fetches from API, updates cache
- NodeId not found → Re-fetches and validates

### 2. get_figma_data

**Purpose**: Retrieve Figma design data with layout, styles, components, and content.

**Parameters**:
```typescript
{
  fileKey: string;   // Figma file key from URL
  nodeId?: string;   // Optional node ID (format: "1234:5678" or "1234-5678")
  depth?: number;    // Optional traversal depth (omit unless user specifies)
}
```

**Usage Examples**:

```typescript
// Get entire file
const result = await get_figma_data({
  fileKey: "QlQwKAl9abcdhvlfvpM5K"
});

// Get specific node
const result = await get_figma_data({
  fileKey: "QlQwKAl9abcdhvlfvpM5K",
  nodeId: "2777-9428"
});

// Limit traversal depth (rare, only if user asks)
const result = await get_figma_data({
  fileKey: "QlQwKAl9abcdhvlfvpM5K",
  nodeId: "2777-9428",
  depth: 3
});
```

**Return Structure**:
```typescript
{
  metadata: {
    name: string;
    lastModified: string;
    version: string;
  };
  nodes: {
    // Node tree with layout, styles, text, etc.
  };
  globalVars: {
    // Reusable styles extracted as variables
  };
  components: {
    // Component definitions
  };
  componentSets: {
    // Component set definitions
  };
}
```

### 3. download_figma_images

**Purpose**: Download SVG and PNG images from Figma nodes.

**Parameters**:
```typescript
{
  fileKey: string;     // Figma file key
  nodes: Array<{
    nodeId: string;           // Node ID
    fileName: string;         // Output filename (.png or .svg)
    imageRef?: string;        // Image fill reference ID (required for image fills)
    needsCropping?: boolean;  // Apply crop transform
    cropTransform?: number[]; // Figma transform matrix
    requiresImageDimensions?: boolean; // Return dimensions for CSS
  }>;
  localPath?: string;  // Save directory (default: OS Downloads folder)
  pngScale?: number;   // PNG export scale (default: 2)
}
```

**Usage Examples**:

```typescript
// Download to default Downloads folder
const result = await download_figma_images({
  fileKey: "QlQwKAl9abcdhvlfvpM5K",
  nodes: [
    {
      nodeId: "2777-9428",
      fileName: "hero-image.png"
    },
    {
      nodeId: "2777-9430",
      fileName: "icon-star.svg"
    }
  ],
  pngScale: 2  // 2x resolution
});

// Download to custom path
const result = await download_figma_images({
  fileKey: "QlQwKAl9abcdhvlfvpM5K",
  nodes: [
    {
      nodeId: "2777-9428",
      fileName: "hero.png",
      requiresImageDimensions: true  // Get width/height for CSS
    }
  ],
  localPath: "/Users/dev/project/assets",
  pngScale: 3
});

// Download image with cropping
const result = await download_figma_images({
  fileKey: "QlQwKAl9abcdhvlfvpM5K",
  nodes: [
    {
      nodeId: "2777-9428",
      fileName: "cropped-image.png",
      imageRef: "abc123ref",
      needsCropping: true,
      cropTransform: [1, 0, 0, 1, 0, 0]
    }
  ]
});
```

**Return Structure**:
```typescript
{
  downloadedCount: number;
  savedTo: string;
  images: Array<{
    fileName: string;
    width?: number;
    height?: number;
    cropped?: boolean;
  }>;
}
```

### 4. list_cache (Bonus Tool)

View current cache status and statistics.

```typescript
await list_cache();
// Returns: { enabled, cacheDir, ttl, files, totalSize }
```

### 5. cleanup_cache (Bonus Tool)

Manually clean up expired and corrupted cache files.

```typescript
await cleanup_cache();
// Returns: { removed, freedSpace }
```

## Common Workflows

### Workflow 1: First-Time Design Fetch
```typescript
// User provides Figma URL
const url = "https://www.figma.com/design/QlQwKAl9abcdhvlfvpM5K/MyDesign?node-id=2777-9428";

// Step 1: AI calls figma_prepare_file
await figma_prepare_file({ figmaUrl: url });
// → Fetches from API, caches locally

// Step 2: AI calls get_figma_data
const data = await get_figma_data({
  fileKey: "QlQwKAl9abcdhvlfvpM5K",
  nodeId: "2777-9428"
});
// → Returns cached data
```

### Workflow 2: Cached Design Fetch (10x+ faster)
```typescript
// Same URL, within cache TTL
const url = "https://www.figma.com/design/QlQwKAl9abcdhvlfvpM5K/MyDesign?node-id=2777-9428";

// Step 1: AI calls figma_prepare_file
await figma_prepare_file({ figmaUrl: url });
// → Cache valid, skips API call

// Step 2: AI calls get_figma_data
const data = await get_figma_data({
  fileKey: "QlQwKAl9abcdhvlfvpM5K",
  nodeId: "2777-9428"
});
// → Returns from cache (disk or memory), no API call
```

### Workflow 3: Force Refresh After Design Update
```typescript
// User says: "The design was just updated, get the latest"
const url = "https://www.figma.com/design/QlQwKAl9abcdhvlfvpM5K/MyDesign";

// AI calls with forceRefresh
await figma_prepare_file({
  figmaUrl: url,
  forceRefresh: true  // Bypass cache
});

const data = await get_figma_data({
  fileKey: "QlQwKAl9abcdhvlfvpM5K"
});
// → Fresh data from API, cache updated
```

### Workflow 4: Download Design Assets
```typescript
// User: "Download the hero image and all icons"
const fileKey = "QlQwKAl9abcdhvlfvpM5K";

// First, get design data to find image nodes
const data = await get_figma_data({ fileKey });

// Extract node IDs for images
const nodes = [
  { nodeId: "2777-9428", fileName: "hero.png" },
  { nodeId: "2777-9430", fileName: "icon-home.svg" },
  { nodeId: "2777-9431", fileName: "icon-settings.svg" }
];

// Download to Downloads folder
const result = await download_figma_images({
  fileKey,
  nodes,
  pngScale: 2
});
// → Images saved to ~/Downloads (or OS equivalent)
```

## Cache Behavior Deep Dive

### How Caching Works

1. **First Request**: API fetch → Cache write → Return data
2. **Subsequent Requests (within TTL)**: Cache read → Return data (no API call)
3. **After TTL Expires**: API fetch → Cache update → Return data

### Cache Invalidation Strategies

```typescript
// Strategy 1: Wait for TTL expiration (automatic)
// Cache expires after configured TTL, next request fetches fresh

// Strategy 2: Force refresh via tool parameter
await figma_prepare_file({
  figmaUrl: url,
  forceRefresh: true
});

// Strategy 3: Manual cache cleanup (via bonus tools)
await cleanup_cache();

// Strategy 4: Delete cache directory (nuclear option)
// Linux/macOS: rm -rf ~/.cache/figma-mcp
// Windows: rmdir /s %LOCALAPPDATA%\FigmaMcpCache
```

### Multi-Layer Caching

```
Request Flow:
1. Check LRU memory cache (maxMemoryCacheSize entries)
   ↓ miss
2. Check disk cache (encrypted if encryptionKey set)
   ↓ miss
3. Fetch from Figma API
   ↓
4. Write to disk cache
   ↓
5. Add to memory cache
   ↓
6. Return data
```

## Troubleshooting

### Issue: Cache not reducing API calls

**Check**:
```typescript
// 1. Verify caching is enabled in config
"--figma-caching={\"ttl\":{\"value\":7,\"unit\":\"d\"}}"

// 2. Check cache directory exists and is writable
// macOS: ls -la ~/Library/Caches/FigmaMcp
// Linux: ls -la ~/.cache/figma-mcp

// 3. Verify TTL hasn't expired
await list_cache();  // Check file ages
```

### Issue: "File not prepared" error

**Solution**: Always call `figma_prepare_file` before `get_figma_data`:
```typescript
// ✅ Correct order
await figma_prepare_file({ figmaUrl });
await get_figma_data({ fileKey, nodeId });

// ❌ Wrong - missing prepare step
await get_figma_data({ fileKey, nodeId });  // Error!
```

### Issue: Getting stale design data

**Solution**: Use force refresh when design updates frequently:
```typescript
// During active design phase
await figma_prepare_file({
  figmaUrl,
  forceRefresh: true  // Always get latest
});

// Or reduce TTL for shorter cache
"--figma-caching={\"ttl\":{\"value\":1,\"unit\":\"h\"}}"
```

### Issue: Encrypted cache can't be read

**Check**:
```typescript
// 1. Ensure FIGMA_CACHE_ENCRYPTION_KEY is set consistently
echo $FIGMA_CACHE_ENCRYPTION_KEY

// 2. If key changed, clear old cache
await cleanup_cache();

// 3. Restart MCP server to pick up new env vars
```

### Issue: Rate limit still hit

**Possible causes**:
- Cache TTL too short for request frequency
- Using `forceRefresh: true` too often
- Multiple MCP clients/servers with separate caches

**Solution**:
```typescript
// Increase TTL for stable designs
"--figma-caching={\"ttl\":{\"value\":30,\"unit\":\"d\"}}"

// Share cache directory across clients
"--figma-caching={\"cacheDir\":\"/shared/figma-cache\"}"
```

### Issue: Large cache consuming disk space

**Monitor**:
```typescript
await list_cache();
// Returns totalSize in bytes

// Enable auto cleanup
"--figma-caching={\"autoCleanup\":true,\"cleanupInterval\":{\"value\":6,\"unit\":\"h\"}}"

// Or manual cleanup
await cleanup_cache();
```

## Environment Variables

```bash
# Required
export FIGMA_API_KEY=figd_xxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# Optional - for cache encryption
export FIGMA_CACHE_ENCRYPTION_KEY=your-secret-key-min-16-chars

# Optional - alternative to command-line args
export FIGMA_CACHE_TTL_VALUE=7
export FIGMA_CACHE_TTL_UNIT=d
export FIGMA_CACHE_DIR=~/my-figma-cache
```

## Best Practices

1. **Use high TTL for finalized designs** (30 days)
2. **Use low TTL for active development** (1-2 hours)
3. **Enable encryption** for sensitive/proprietary designs
4. **Always call figma_prepare_file first** - let the LLM handle this automatically
5. **Use forceRefresh** when user says "latest", "updated", "refresh"
6. **Monitor cache size** with `list_cache` tool
7. **Set reasonable maxMemoryCacheSize** based on available RAM (100-200 entries typical)
8. **Use auto cleanup** to prevent cache bloat

## When to Use This vs. Standard Figma MCP

**Use figma-mcp-cached when**:
- Free Figma account (rate limits)
- High-frequency context requests
- Stable/finalized designs
- Need faster response times
- Working with large design files

**Use standard Figma MCP when**:
- Designs change constantly (hourly)
- Real-time design collaboration
- No rate limit concerns (Pro account + low usage)
