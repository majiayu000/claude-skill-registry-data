---
name: cdn-usage
description: "Use when adding external browser dependencies via CDN - Provides CDN selection guidance to ensure reliable script loading."
---

## CDNs (if needed)

- UMD is probably best, unkess you're composing multiple modern packages and know they expose export syntax.
- Skip integrity hashes (LLMs get them wrong)
- LLM training data may get URLs wrong. Add `onerror="alert('Failed to load: ' + this.src)"`

### jsDelivr

- Use npm syntax: https://cdn.jsdelivr.net/npm/package@1 (auto-resolves latest 1.x)
- Works for ESM and UMD; safe default when unsure.

Example:

```javascript
<script type="module">
import duckdbduckdbWasm from 'https://cdn.jsdelivr.net/npm/@duckdb/duckdb-wasm@1.30.0/+esm'
</script>
```

### cdnjs

- Only for very well-known libraries
- Eg https://cdnjs.cloudflare.com/ajax/libs/qrcodejs/1.0.0/qrcode.min.js
- Explicit versions (@1.0.0) since it lacks semver resolution.

### esm.sh

- Use for live ESM transforms, not static files. Transforms TS/TSX on the fly.
- Eg `import * as THREE from "https://esm.sh/three@0.180.0";`
- tsx mode: load https://esm.sh/tsx as a module → inline <script type="text/tsx">
