---
name: source-map-setup
description: Configure source maps for readable stack traces. Use when setting up error tracking, debugging production issues, or configuring build tools.
triggers:
  - "source maps"
  - "readable stack traces"
  - "minified errors"
  - "debug production"
  - "symbolication"
  - "upload source maps"
priority: 1
---

# Source Map Setup

Make production stack traces readable by uploading source maps to your error tracking service.

## Why Source Maps?

**Without source maps:**
```
TypeError: Cannot read property 'x' of undefined
    at e.render (main.a1b2c3.js:1:45678)
    at t.update (main.a1b2c3.js:1:12345)
```

**With source maps:**
```
TypeError: Cannot read property 'x' of undefined
    at ProductCard.render (src/components/ProductCard.tsx:45:12)
    at CartList.update (src/features/cart/CartList.tsx:78:8)
```

## Build Tool Configuration

### Vite

```typescript
// vite.config.ts
import { sentryVitePlugin } from '@sentry/vite-plugin';

export default defineConfig({
  build: {
    sourcemap: true, // Generate source maps
  },
  plugins: [
    sentryVitePlugin({
      org: 'your-org',
      project: 'your-project',
      authToken: process.env.SENTRY_AUTH_TOKEN,
      sourcemaps: {
        filesToDeleteAfterUpload: ['**/*.map'], // Don't deploy maps
      },
    }),
  ],
});
```

### Webpack (Next.js, CRA)

```javascript
// next.config.js
const { withSentryConfig } = require('@sentry/nextjs');

module.exports = withSentryConfig(
  {
    // Your Next.js config
  },
  {
    org: 'your-org',
    project: 'your-project',
    silent: true,
    widenClientFileUpload: true,
    hideSourceMaps: true, // Don't expose in production
  }
);
```

### esbuild

```typescript
// esbuild.config.ts
import * as Sentry from '@sentry/esbuild-plugin';

await esbuild.build({
  entryPoints: ['src/index.ts'],
  bundle: true,
  sourcemap: true,
  plugins: [
    Sentry.sentryEsbuildPlugin({
      org: 'your-org',
      project: 'your-project',
      authToken: process.env.SENTRY_AUTH_TOKEN,
    }),
  ],
});
```

### Rollup (SvelteKit)

```javascript
// vite.config.ts (SvelteKit uses Vite)
import { sentrySvelteKit } from '@sentry/sveltekit';

export default defineConfig({
  plugins: [
    sentrySvelteKit({
      sourceMapsUploadOptions: {
        org: 'your-org',
        project: 'your-project',
        authToken: process.env.SENTRY_AUTH_TOKEN,
      },
    }),
    sveltekit(),
  ],
});
```

## Vendor-Specific Setup

### Sentry

```bash
# Install CLI
npm install @sentry/cli --save-dev

# Upload manually (CI/CD)
sentry-cli sourcemaps upload \
  --org your-org \
  --project your-project \
  --release "1.0.0" \
  ./dist
```

### Datadog

```typescript
// datadog-ci upload
// In CI/CD:
// npx @datadog/datadog-ci sourcemaps upload ./dist \
//   --service your-service \
//   --release-version 1.0.0 \
//   --minified-path-prefix /static/js
```

### New Relic

```javascript
// newrelic.js
exports.config = {
  app_name: ['Your App'],
  browser_monitoring: {
    enable: true,
    debug: false,
  },
  // Source maps uploaded via CLI or agent
};
```

## CI/CD Integration

### GitHub Actions

```yaml
# .github/workflows/deploy.yml
- name: Upload Source Maps
  env:
    SENTRY_AUTH_TOKEN: ${{ secrets.SENTRY_AUTH_TOKEN }}
  run: |
    npx sentry-cli releases new ${{ github.sha }}
    npx sentry-cli sourcemaps upload \
      --release ${{ github.sha }} \
      --url-prefix '~/' \
      ./dist
    npx sentry-cli releases finalize ${{ github.sha }}
```

### Vercel

```javascript
// next.config.js - automatic with @sentry/nextjs
module.exports = withSentryConfig(nextConfig, {
  // Vercel automatically sets VERCEL_GIT_COMMIT_SHA
  release: process.env.VERCEL_GIT_COMMIT_SHA,
});
```

## Security Considerations

| Approach | Pros | Cons |
|----------|------|------|
| **Upload & delete** | Secure, no exposure | Requires CI/CD setup |
| **Hidden source maps** | Simple | Still on server |
| **Private source maps** | Full control | Complex setup |

**Best practice:** Upload to error tracking service, then delete from build output.

```typescript
// Vite config
sentryVitePlugin({
  sourcemaps: {
    filesToDeleteAfterUpload: ['**/*.map'],
  },
});
```

## Verification

```bash
# Verify upload worked
sentry-cli releases files YOUR_RELEASE list

# Test with a real error
throw new Error('Test source maps');
```

Check in Sentry/Datadog that:
1. Stack trace shows original file names
2. Line numbers match source code
3. Context code is visible

## Common Issues

| Issue | Cause | Fix |
|-------|-------|-----|
| Still minified | Maps not uploaded | Check CI/CD logs |
| Wrong lines | Version mismatch | Ensure release matches |
| Missing files | Incorrect path prefix | Set `--url-prefix` correctly |
| Partial mapping | Tree shaking | Upload all chunks |

## Related Skills

- See `skills/error-tracking` for error capture
- See `skills/bundle-performance` for build optimization

## References

- `references/frameworks/*.md` - Framework-specific setup
- `references/platforms/*.md` - Vendor-specific guides
