---
name: vite-deployment
description: Vite SPA deployment to various platforms. Use when deploying React SPAs.
---

# Vite Deployment Skill

This skill covers deploying Vite-built React SPAs to various hosting platforms.

## When to Use

Use this skill when:
- Deploying React SPAs built with Vite
- Setting up CI/CD pipelines
- Configuring preview deployments
- Optimizing for production hosting

## Core Principle

**BUILD ONCE, DEPLOY ANYWHERE** - Vite produces static assets that can be deployed to any static hosting provider.

## Build Configuration

### Production Build

```typescript
// vite.config.ts
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  build: {
    outDir: 'dist',
    sourcemap: true,
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['react', 'react-dom'],
          router: ['react-router-dom'],
        },
      },
    },
  },
  // Base path for deployment (adjust if not at root)
  base: '/',
});
```

### SPA Router Configuration

```typescript
// For client-side routing, configure redirects for all hosting platforms

// vite.config.ts - Preview server fallback
export default defineConfig({
  preview: {
    port: 4173,
  },
  // This handles local preview, but each platform needs its own config
});
```

## Vercel Deployment

### Configuration

```json
// vercel.json
{
  "buildCommand": "npm run build",
  "outputDirectory": "dist",
  "framework": "vite",
  "rewrites": [
    { "source": "/(.*)", "destination": "/index.html" }
  ],
  "headers": [
    {
      "source": "/assets/(.*)",
      "headers": [
        { "key": "Cache-Control", "value": "public, max-age=31536000, immutable" }
      ]
    }
  ]
}
```

### Deploy Script

```bash
# Install Vercel CLI
npm install -g vercel

# Deploy to preview
vercel

# Deploy to production
vercel --prod
```

### GitHub Actions

```yaml
# .github/workflows/deploy-vercel.yml
name: Deploy to Vercel

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-node@v4
        with:
          node-version: '22'

      - name: Install dependencies
        run: npm ci

      - name: Build
        run: npm run build

      - name: Deploy to Vercel
        uses: amondnet/vercel-action@v25
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.VERCEL_ORG_ID }}
          vercel-project-id: ${{ secrets.VERCEL_PROJECT_ID }}
          vercel-args: ${{ github.ref == 'refs/heads/main' && '--prod' || '' }}
```

## Netlify Deployment

### Configuration

```toml
# netlify.toml
[build]
  command = "npm run build"
  publish = "dist"

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200

[[headers]]
  for = "/assets/*"
  [headers.values]
    Cache-Control = "public, max-age=31536000, immutable"

[[headers]]
  for = "/*"
  [headers.values]
    X-Frame-Options = "DENY"
    X-XSS-Protection = "1; mode=block"
    X-Content-Type-Options = "nosniff"
    Referrer-Policy = "strict-origin-when-cross-origin"
```

### Deploy Script

```bash
# Install Netlify CLI
npm install -g netlify-cli

# Login
netlify login

# Deploy preview
netlify deploy

# Deploy production
netlify deploy --prod
```

### GitHub Actions

```yaml
# .github/workflows/deploy-netlify.yml
name: Deploy to Netlify

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-node@v4
        with:
          node-version: '22'

      - name: Install dependencies
        run: npm ci

      - name: Build
        run: npm run build

      - name: Deploy to Netlify
        uses: nwtgck/actions-netlify@v3
        with:
          publish-dir: './dist'
          production-branch: main
          github-token: ${{ secrets.GITHUB_TOKEN }}
          deploy-message: "Deploy from GitHub Actions"
        env:
          NETLIFY_AUTH_TOKEN: ${{ secrets.NETLIFY_AUTH_TOKEN }}
          NETLIFY_SITE_ID: ${{ secrets.NETLIFY_SITE_ID }}
```

## Cloudflare Pages Deployment

### Configuration

```json
// wrangler.toml (optional)
name = "my-react-app"
compatibility_date = "2024-01-01"
pages_build_output_dir = "dist"

[site]
bucket = "dist"
```

### Redirect Rules

```plain
# public/_redirects
/*    /index.html   200
```

### GitHub Actions

```yaml
# .github/workflows/deploy-cloudflare.yml
name: Deploy to Cloudflare Pages

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      deployments: write
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-node@v4
        with:
          node-version: '22'

      - name: Install dependencies
        run: npm ci

      - name: Build
        run: npm run build

      - name: Deploy to Cloudflare Pages
        uses: cloudflare/pages-action@v1
        with:
          apiToken: ${{ secrets.CLOUDFLARE_API_TOKEN }}
          accountId: ${{ secrets.CLOUDFLARE_ACCOUNT_ID }}
          projectName: my-react-app
          directory: dist
          gitHubToken: ${{ secrets.GITHUB_TOKEN }}
```

## AWS S3 + CloudFront

### S3 Bucket Policy

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "PublicReadGetObject",
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::your-bucket-name/*"
    }
  ]
}
```

### GitHub Actions

```yaml
# .github/workflows/deploy-aws.yml
name: Deploy to AWS

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-node@v4
        with:
          node-version: '22'

      - name: Install dependencies
        run: npm ci

      - name: Build
        run: npm run build

      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: us-east-1

      - name: Deploy to S3
        run: |
          aws s3 sync dist/ s3://${{ secrets.S3_BUCKET }} --delete

      - name: Invalidate CloudFront
        run: |
          aws cloudfront create-invalidation \
            --distribution-id ${{ secrets.CLOUDFRONT_DISTRIBUTION_ID }} \
            --paths "/*"
```

## GitHub Pages

### Configuration

```typescript
// vite.config.ts
export default defineConfig({
  base: '/repository-name/', // Set to your repo name
  plugins: [react()],
});
```

### GitHub Actions

```yaml
# .github/workflows/deploy-ghpages.yml
name: Deploy to GitHub Pages

on:
  push:
    branches: [main]

permissions:
  contents: read
  pages: write
  id-token: write

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-node@v4
        with:
          node-version: '22'

      - name: Install dependencies
        run: npm ci

      - name: Build
        run: npm run build

      - name: Setup Pages
        uses: actions/configure-pages@v4

      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: './dist'

  deploy:
    needs: build
    runs-on: ubuntu-latest
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    steps:
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
```

### 404 Handling for SPA

```bash
# Create 404.html that redirects to index.html
cp dist/index.html dist/404.html
```

## Firebase Hosting

### Configuration

```json
// firebase.json
{
  "hosting": {
    "public": "dist",
    "ignore": ["firebase.json", "**/.*", "**/node_modules/**"],
    "rewrites": [
      {
        "source": "**",
        "destination": "/index.html"
      }
    ],
    "headers": [
      {
        "source": "/assets/**",
        "headers": [
          {
            "key": "Cache-Control",
            "value": "public, max-age=31536000, immutable"
          }
        ]
      }
    ]
  }
}
```

### Deploy Script

```bash
# Install Firebase CLI
npm install -g firebase-tools

# Login
firebase login

# Initialize (select Hosting)
firebase init

# Deploy
firebase deploy --only hosting
```

## Environment Variables

### Build-Time Variables

```typescript
// vite.config.ts
export default defineConfig({
  define: {
    __APP_VERSION__: JSON.stringify(process.env.npm_package_version),
  },
});
```

```env
# .env.production
VITE_API_URL=https://api.production.com
VITE_ANALYTICS_ID=UA-XXXXX
```

### Platform-Specific Variables

```yaml
# GitHub Actions
env:
  VITE_API_URL: ${{ vars.API_URL }}
  VITE_ANALYTICS_ID: ${{ secrets.ANALYTICS_ID }}
```

## Caching Strategy

### Asset Caching

```typescript
// vite.config.ts
export default defineConfig({
  build: {
    rollupOptions: {
      output: {
        // Add hash to filenames for cache busting
        entryFileNames: 'assets/[name]-[hash].js',
        chunkFileNames: 'assets/[name]-[hash].js',
        assetFileNames: 'assets/[name]-[hash].[ext]',
      },
    },
  },
});
```

### Headers Configuration

```plain
# Hashed assets - cache forever
/assets/*
  Cache-Control: public, max-age=31536000, immutable

# HTML - always revalidate
/index.html
  Cache-Control: no-cache, no-store, must-revalidate

# Service worker - no cache
/sw.js
  Cache-Control: no-cache, no-store, must-revalidate
```

## Preview Deployments

### Vercel

```yaml
# Automatic preview deployments on PRs
# No additional config needed with Vercel
```

### Netlify

```toml
# netlify.toml
[context.deploy-preview]
  command = "npm run build"

[context.branch-deploy]
  command = "npm run build"
```

## Commands

```bash
# Build for production
npm run build

# Preview production build locally
npm run preview

# Deploy to Vercel
vercel --prod

# Deploy to Netlify
netlify deploy --prod

# Deploy to Firebase
firebase deploy --only hosting
```

## Best Practices

1. **Enable source maps** - Helps debug production issues
2. **Use content hashing** - Enables aggressive caching
3. **Set security headers** - X-Frame-Options, CSP, etc.
4. **Configure SPA routing** - Redirect all paths to index.html
5. **Environment separation** - Different configs for staging/production
6. **Preview deployments** - Test changes before production

## Notes

- Vite outputs static files to `dist/` by default
- All platforms need SPA routing configured
- Use environment variables for API URLs
- Monitor bundle size with `vite-bundle-visualizer`
