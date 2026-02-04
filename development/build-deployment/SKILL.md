---
name: Build & Deployment
description: Verify production builds pass all quality checks, analyze bundle impact, and ensure readiness for Vercel deployment with zero errors
---

# Build & Deployment Skill

This skill ensures your Next.js application builds successfully with zero errors and is ready for production deployment to Vercel. It validates TypeScript, runs linters, executes tests, analyzes bundle size, and provides pre-deployment verification.

## When to Use This Skill

Claude will automatically invoke this skill when:
- You ask to "verify build"
- You request "check if ready to deploy"
- You say "prepare for production"
- You want to "check for build errors"
- You mention "pre-deployment checks"

## Build Quality Checklist

Before deployment, this skill verifies:

```
✅ Pre-Deployment Verification
├── TypeScript Type Safety
│   ├── No TypeScript compilation errors
│   ├── Strict mode enabled
│   └── Full type coverage
├── Code Quality
│   ├── ESLint passes with zero errors
│   ├── No warnings in strict mode
│   └── Code style consistent
├── Test Suite
│   ├── All tests passing
│   ├── No test failures
│   └── Coverage maintained
├── Build Process
│   ├── Production build succeeds
│   ├── No build warnings
│   ├── All assets optimized
│   └── Output size acceptable
├── Bundle Analysis
│   ├── Bundle size tracked
│   ├── No bloated dependencies
│   ├── Code splitting effective
│   └── Performance metrics
└── Production Readiness
    ├── Environment variables configured
    ├── API endpoints correct
    ├── Analytics integrated
    └── Error tracking ready
```

## Build Verification Workflow

### Step 1: Check TypeScript (Type Safety)

```bash
# Check for TypeScript errors
npx tsc --noEmit
```

**What it checks:**
- ✅ All files compile without errors
- ✅ Strict mode enabled (`strict: true`)
- ✅ No `any` types (unless explicitly allowed)
- ✅ All imports resolve correctly
- ✅ Type definitions complete

**Common TypeScript Errors:**
```
error TS2304: Cannot find name 'X'
error TS2339: Property 'X' does not exist on type 'Y'
error TS2345: Argument of type 'X' is not assignable to parameter of type 'Y'
```

**Fix Command:**
```bash
npm run ts-fix  # Automatically fix fixable TS errors
```

### Step 2: Check Code Style (ESLint)

```bash
# Run ESLint
npm run lint
```

**What it checks:**
- ✅ No unused imports or variables
- ✅ No console.log left in production code
- ✅ No debugger statements
- ✅ Imports are sorted alphabetically
- ✅ Code follows Next.js best practices

**Common ESLint Issues:**
```
warning  'variable' is assigned a value but never used  no-unused-vars
warning  Unexpected console statement  no-console
error    'image' is missing the required 'alt' prop  jsx-a11y/alt-text
```

**Fix Command:**
```bash
npm run lint -- --fix  # Auto-fix linting issues
```

### Step 3: Run Test Suite

```bash
# Run all tests in CI mode (no watch)
npm run test:ci
```

**What it checks:**
- ✅ All 481+ tests pass
- ✅ No failing test suites
- ✅ Coverage thresholds met (48% baseline, 70% target)
- ✅ No snapshot diffs (unexpected UI changes)

**Expected Output:**
```
PASS  src/components/ui/__tests__/Button.test.tsx
PASS  src/components/examples/__tests__/AdaptiveInterfacesExample.test.tsx
...
Test Suites: 24 passed, 24 total
Tests:       481 passed, 481 total
Coverage:    48.28% statements, 36.19% branches
```

**If Tests Fail:**
```bash
npm run test:watch  # Debug in watch mode
npm test -- --no-coverage  # Faster feedback
```

### Step 4: Build for Production

```bash
# Create optimized production build
npm run build:production
```

**What happens:**
- ✅ Next.js compiles all pages and components
- ✅ Optimizes and bundles JavaScript
- ✅ Generates static assets
- ✅ Applies tree-shaking (removes dead code)
- ✅ Creates source maps for error tracking
- ✅ Optimizes images (WebP, AVIF conversion)

**Expected Output:**
```
  ▲ Next.js 15.4.6

  ○ Checking validity of types
  ✓ Types checked
  ✓ Compiled client and server successfully
  ✓ Exported 24 pages
  ✓ Generated robots.txt
  ...

Route (pages)                              Size    Files
┌ ○ /                                      XX KB   XX KB
├ ○ /patterns                              XX KB   XX KB
├ ○ /patterns/[slug]                       XX KB   XX KB
...
○ (Static)  prerendered as static HTML + JSON
```

**If Build Fails:**
```bash
npm run build:local  # Analyze build issues locally
npm run build:analyze  # Detailed analysis
```

### Step 5: Analyze Bundle Impact

```bash
# Analyze bundle with detailed report
npm run build:analyze
```

**Output includes:**
- 📊 Total bundle size
- 📊 Bundle breakdown by page
- 📊 JavaScript bundle composition
- 📊 Unused code opportunities
- 📊 Large dependencies
- 📊 Performance metrics

**Expected Bundle Sizes:**
```
Total JavaScript: ~150-200 KB (gzipped)
Main bundle: ~60-80 KB
Patterns page: ~40-60 KB
Individual pattern: ~30-40 KB
```

**If Bundle Too Large:**
```bash
# Identify large dependencies
npm ls --depth=0

# Check package sizes
npx webpack-bundle-analyzer

# Implement code splitting
# See Build Optimization section below
```

### Step 6: Verify Environment Configuration

Check that production environment is configured:

```bash
# Verify .env variables exist
cat .env.example  # See what's required

# Check for required vars in .env
NEXT_PUBLIC_API_URL=https://api.example.com
NEXT_PUBLIC_ANALYTICS_ID=...
DATABASE_URL=...
```

**Required Variables:**
- ✅ `NEXT_PUBLIC_API_URL` - API endpoint
- ✅ `NEXT_PUBLIC_ANALYTICS_ID` - Vercel Analytics
- ✅ `DATABASE_URL` - Prisma database
- ✅ `RESEND_API_KEY` - Newsletter service
- ✅ `NODE_ENV=production` - Production mode

### Step 7: Pre-Deployment Checklist

✅ **TypeScript**: Zero errors (`npx tsc --noEmit`)
✅ **ESLint**: Zero errors (`npm run lint`)
✅ **Tests**: All passing (`npm run test:ci`)
✅ **Build**: Successful (`npm run build:production`)
✅ **Bundle**: Acceptable size (~150-200 KB gzipped)
✅ **Environment**: All variables configured
✅ **Git**: No uncommitted changes (`git status`)
✅ **Branch**: On `main` branch
✅ **Remote**: Pushed to GitHub (`git push`)

## Automated Build Script

Run all checks at once:

```bash
npm run fix-all
```

This automatically:
1. Runs TypeScript type checking
2. Fixes linting issues with `--fix`
3. Runs tests
4. Reports results

**Output:**
```
=== TypeScript Errors ===
0 errors found ✅

=== ESLint Errors ===
Fixed 2 warnings

=== Test Status ===
All 481 tests passing ✅

=== Build Ready ===
✅ Ready for deployment!
```

## Build Optimization Strategies

### 1. Code Splitting

For large pages, implement route-based code splitting:

```typescript
// components/examples/HeavyComponent.tsx - lazy load
import dynamic from 'next/dynamic'

const HeavyDemoComponent = dynamic(
  () => import('@/components/examples/HeavyExample'),
  { loading: () => <Skeleton /> }
)
```

### 2. Image Optimization

Images are automatically optimized:

```bash
# Optimize all images before commit
npm run optimize-images

# Convert GIFs to WebM/MP4
npm run convert-gifs
```

### 3. Remove Unused Dependencies

```bash
# Check for unused packages
npm prune

# Check for vulnerabilities
npm audit

# Fix security issues
npm audit fix
```

### 4. Monitor Bundle Growth

Track bundle size over time:

```bash
# Generate build metrics
npm run build:analyze

# Track in build-metrics.json
cat build-metrics.json
```

## Deployment Process

### Deploy to Vercel

```bash
# Vercel auto-deploys on push to main
git push origin main

# Monitor deployment
# https://vercel.com/dashboard
```

**Vercel Configuration:**
- ✅ Connected to GitHub repository
- ✅ Auto-deploy on main branch push
- ✅ Preview deployments for PRs
- ✅ Environment variables configured
- ✅ Build command: `npm run build`
- ✅ Start command: `npm start`

### Deployment Checklist

Before pushing to main:

- [ ] All TypeScript errors fixed
- [ ] All ESLint issues resolved
- [ ] All tests passing
- [ ] Production build succeeds
- [ ] Bundle size acceptable
- [ ] No console errors in build
- [ ] Environment variables set in Vercel
- [ ] Git history clean
- [ ] Commit message descriptive

### Post-Deployment Verification

After deployment:

```bash
# Check live site health
curl https://aiuxdesign.guide/api/health

# Monitor analytics
# https://vercel.com/analytics

# Check error tracking
# https://sentry.io (if configured)

# Monitor performance
# https://vercel.com/speed-insights
```

## Error Handling & Recovery

### Build Fails - TypeScript Errors

```bash
npm run ts-fix  # Auto-fix
# or manually review and fix
npx tsc --noEmit
```

### Build Fails - ESLint Errors

```bash
npm run lint -- --fix  # Auto-fix most issues
# Review remaining manual fixes
```

### Build Fails - Test Failures

```bash
npm run test:watch  # Debug in watch mode
# Fix failing tests
# Verify snapshots are intentional
npm test -- -u  # Update snapshots if needed
```

### Build Fails - Bundle Issues

```bash
npm run build:analyze  # Identify large files
# Remove unused dependencies
# Implement code splitting
# Optimize imports
```

## Commands Reference

```bash
# Type checking
npx tsc --noEmit           # Check types
npm run ts-fix             # Fix types

# Linting
npm run lint               # Check lint
npm run lint -- --fix      # Fix lint

# Testing
npm test                   # Run tests
npm run test:ci            # CI mode
npm run test:coverage      # With coverage

# Building
npm run build              # Dev build analysis
npm run build:production   # Prod build
npm run build:analyze      # Bundle analysis
npm run build:local        # Local optimization

# Image optimization
npm run optimize-images    # Optimize all
npm run convert-gifs       # Convert GIFs

# All-in-one
npm run fix-all            # TypeScript + ESLint + Tests
```

## Performance Monitoring

After deployment, monitor:

**Core Web Vitals:**
- ✅ Largest Contentful Paint (LCP) < 2.5s
- ✅ First Input Delay (FID) < 100ms
- ✅ Cumulative Layout Shift (CLS) < 0.1

**Vercel Speed Insights:**
- Check at https://vercel.com/analytics
- Monitor page load times
- Track performance trends

**Build Metrics:**
```bash
# View historical build metrics
cat build-metrics.json
```

## Success Criteria

Deployment is successful when:

✅ **Build Status**: Green (all checks pass)
✅ **Test Coverage**: Maintained at 48%+ (targeting 70%)
✅ **Bundle Size**: ~150-200 KB gzipped
✅ **Performance**: LCP < 2.5s, FID < 100ms, CLS < 0.1
✅ **Errors**: Zero TypeScript, ESLint, and test failures
✅ **Analytics**: Tracking page views and web vitals
✅ **Uptime**: 99.9% availability

---

**Goal**: Maintain high code quality standards with automated pre-deployment verification, ensuring every production release is stable, performant, and error-free.
