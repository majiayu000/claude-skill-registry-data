---
name: troubleshooting-bundler-compatibility
description: Diagnose and fix third-party library loading failures in Vite, Webpack, or other bundlers. Use when encountering "Failed to fetch dynamically imported module", worker loading failures, CDN 404 errors, "Invalid type" errors when importing library assets, or assets loading in wrong format. Covers version mismatches, worker loading patterns, and bundler-specific solutions.
---

# Troubleshooting Bundler Compatibility Issues

Systematic approach for diagnosing library compatibility issues with modern bundlers.

## Diagnostic Checklist

### 1. Version Verification
- Check installed npm version vs CDN availability (CDNs often lag behind npm)
- Use Context7 to get latest library documentation
- Check library changelog for breaking changes in asset loading

### 2. Identify Asset Type
- What does the library need: worker, wasm, static asset, CSS?
- Expected format: URL string, blob, or module import?
- ES module vs CommonJS vs raw text?

### 3. Bundler Investigation

**Vite:**
- `?url` suffix returns URL reference, not content
- `?raw` suffix imports as text string
- Check `publicDir` in vite.config.js
- Verify asset not treated as ES module incorrectly

**Webpack:**
- Check loader configuration for asset type
- Verify `asset/resource` vs `asset/source` handling

## Solution Patterns

**Pattern A: Blob URL (Most Reliable for Workers)**
```javascript
const workerCode = await import("library/worker.js?raw");
const blob = new Blob([workerCode.default], { type: "application/javascript" });
const workerUrl = URL.createObjectURL(blob);
library.workerSrc = workerUrl;
```

**Pattern B: Public Directory**
```javascript
// Copy asset to public/ folder, reference with absolute path
library.assetSrc = "/asset-file.js";
```

**Pattern C: CDN with Verified Version**
```javascript
// MUST verify version exists on CDN first
const cdnUrl = `https://cdn.example.com/library/${VERIFIED_VERSION}/asset.js`;
```

## Common Pitfalls

1. **npm version != CDN version** - npm releases faster than CDN updates
2. **Protocol-relative URLs** - `//cdn.example.com` can resolve to `http:`
3. **?url misconception** - Returns URL to bundled asset, not the content itself
4. **ES module workers** - Some workers must load as classic scripts
5. **MIME type issues** - Blob URLs need correct MIME type

## Validation

After applying fix:
- Test in dev mode (`npm run dev`)
- Test in production build (`npm run build && npm run preview`)
- Verify no console errors
- Test actual functionality
- Check network tab for failed requests

## Documentation

After resolving, log in ConPort:
- Root cause (e.g., "npm version not on CDN")
- Solution applied (e.g., "blob URL pattern")
- Why other approaches failed
- Create system pattern if reusable
