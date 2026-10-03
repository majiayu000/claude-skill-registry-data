---
name: web-dev
description: "Expert web development skill with 25+ years of combined knowledge. Covers full-stack development: React, Next.js, TypeScript, Tailwind CSS, Node.js, databases, security, performance, accessibility, testing, and deployment. Use when building, debugging, or reviewing web applications. Trigger on: 'web development', 'frontend', 'backend', 'full stack', 'React', 'Next.js', 'TypeScript', 'CSS', 'HTML', 'JavaScript', 'Node.js', 'API', 'database', 'deployment', 'web app', 'website', 'web design', 'responsive design', 'accessibility', 'performance optimization', 'security', 'testing', 'CI/CD', 'Docker', 'Kubernetes', 'AWS', 'Vercel', 'Netlify'."
---

# Web Development Expert

## Core Knowledge Base

### 1. Frontend Fundamentals

#### HTML5 (Semantic & Accessible)
- Semantic elements: `<header>`, `<nav>`, `<main>`, `<article>`, `<section>`, `<aside>`, `<footer>`
- ARIA roles, labels, and live regions for screen readers
- Responsive images: `srcset`, `sizes`, `<picture>`, lazy loading
- Forms: validation, `<dialog>`, custom elements
- Web Components: Shadow DOM, Custom Elements, HTML Templates
- Meta tags: Open Graph, Twitter Cards, structured data (JSON-LD)

#### CSS3 (Modern Layout & Animation)
- **Layout**: Flexbox, CSS Grid, Container Queries, Subgrid
- **Responsive Design**: Mobile-first, fluid typography (`clamp()`), viewport units
- **Custom Properties**: CSS variables for theming
- **Animations**: `@keyframes`, `transition`, `animation`, View Transitions API
- **Container Queries**: `@container` for component-level responsive design
- **Cascade Layers**: `@layer` for managing specificity
- **Color Spaces**: `oklch()`, `oklab()`, `color-mix()`
- **Anchor Positioning**: CSS anchor API for popover positioning

#### JavaScript (ES2024+)
- **Modules**: ESM, dynamic imports, import maps
- **Async**: async/await, Promise.allSettled, AbortController
- **Iterators**: Generators, `for await...of`, Iterator helpers
- **Pattern Matching**: Stage 4 proposal
- **Temporal API**: Date/time handling (Stage 3)
- **Web APIs**: Fetch, Web Workers, Service Workers, Web Streams, Web Crypto
- **Proxy & Reflect**: Metaprogramming
- **WeakRef & FinalizationRegistry**: Memory management

### 2. TypeScript (v6.0)

#### Type System
- **Utility Types**: `Partial`, `Required`, `Pick`, `Omit`, `Record`, `Readonly`
- **Generic Constraints**: `extends`, conditional types, mapped types
- **Template Literal Types**: String manipulation at type level
- **Discriminated Unions**: Tagged unions for type narrowing
- **Branded Types**: Nominal typing for domain modeling
- **Type Inference**: `infer`, `ReturnType`, `Parameters`
- **Const Assertions**: `as const` for literal types
- **Decorators**: Stage 3 decorators (v5.0+)

#### Configuration
```json
{
  "compilerOptions": {
    "strict": true,
    "target": "ESNext",
    "module": "ESNext",
    "moduleResolution": "bundler",
    "jsx": "react-jsx",
    "paths": { "@/*": ["./src/*"] },
    "noUncheckedIndexedAccess": true,
    "exactOptionalPropertyTypes": true
  }
}
```

### 3. React (v19+)

#### Core Patterns
- **Server Components**: Default server, `'use client'` directive
- **Server Actions**: `'use server'`, form actions, progressive enhancement
- **Suspense**: Streaming SSR, loading states, `use()` hook
- **useOptimistic**: Optimistic UI updates
- **useActionState**: Form action state management
- **useFormStatus**: Pending state in forms
- **React Compiler**: Automatic memoization (v19+)

#### State Management
- **Local State**: `useState`, `useReducer`, `useRef`
- **Derived State**: `useMemo`, `useCallback` (sparingly)
- **Global State**: Zustand, Jotai, Recoil
- **Server State**: React Query/TanStack Query, SWR
- **URL State**: `useSearchParams`, `useParams`

#### Performance
- **Code Splitting**: `React.lazy`, dynamic imports
- **Virtualization**: `react-window`, `react-virtual`
- **Concurrent Features**: `startTransition`, `useDeferredValue`
- **Bundle Analysis**: `next/bundle-analyzer`, webpack-bundle-analyzer

### 4. Next.js (v16+)

#### App Router
```
app/
├── layout.tsx          # Root layout (required)
├── page.tsx            # Home page
├── loading.tsx         # Loading UI (Suspense)
├── error.tsx           # Error boundary
├── not-found.tsx       # 404 page
├── template.tsx        # Re-renders on navigation
├── route.ts            # API routes (Route Handlers)
├── middleware.ts       # Request middleware
├── [slug]/page.tsx    # Dynamic routes
├── [...slug]/page.tsx # Catch-all routes
└── (group)/layout.tsx # Route groups
```

#### Key Features
- **Streaming**: Progressive rendering with Suspense boundaries
- **Parallel Routes**: `@slot` for simultaneous route rendering
- **Intercepting Routes**: `(.)`, `(..)`, `(...)` for modals
- **Partial Prerendering (PPR)**: Static shell + dynamic holes
- **Server Actions**: Direct database mutations from components
- **Image Optimization**: `next/image` with AVIF/WebP, lazy loading
- **Font Optimization**: `next/font` for zero layout shift
- **Metadata API**: `generateMetadata`, `generateStaticParams`
- **Incremental Static Regeneration (ISR)**: `revalidatePath`, `revalidateTag`

#### Configuration
```js
// next.config.ts
const nextConfig = {
  images: {
    formats: ['image/avif', 'image/webp'],
    remotePatterns: [{ protocol: 'https', hostname: '**.example.com' }],
  },
  experimental: {
    ppr: true,
    reactCompiler: true,
    viewTransition: true,
  },
};
```

### 5. Tailwind CSS (v4.3)

#### Core Concepts
- **Utility-First**: Compose styles via class names
- **Responsive**: `sm:`, `md:`, `lg:`, `xl:`, `2xl:` prefixes
- **Dark Mode**: `dark:` variant (class or media query)
- **State Variants**: `hover:`, `focus:`, `active:`, `group-hover:`
- **Container Queries**: `@sm:`, `@md:` for component-level responsive
- **Theme Variables**: CSS custom properties via `@theme`

#### Installation (Vite)
```bash
npm install tailwindcss @tailwindcss/vite
```
```ts
// vite.config.ts
import tailwindcss from '@tailwindcss/vite'
export default defineConfig({ plugins: [tailwindcss()] })
```
```css
@import "tailwindcss";
```

#### Best Practices
- Use `@apply` sparingly — prefer utility composition
- Extract components, not utility classes
- Use `clsx` or `cn()` for conditional classes
- Leverage `@layer` for custom utilities

### 6. Node.js & Backend

#### Express/Fastify/Hono
- **Middleware**: Authentication, CORS, rate limiting, compression
- **Routing**: RESTful design, parameter validation (Zod)
- **Error Handling**: Centralized error middleware
- **Logging**: Pino, Winston, structured logging
- **Security**: Helmet, express-rate-limit, CSRF protection

#### API Design
- **REST**: Resource naming, HTTP methods, status codes, HATEOAS
- **GraphQL**: Schema design, resolvers, DataLoader, subscriptions
- **tRPC**: End-to-end type safety
- **OpenAPI/Swagger**: API documentation

#### Authentication & Authorization
- **JWT**: Access tokens, refresh tokens, rotation
- **OAuth 2.0**: Authorization code flow, PKCE
- **Session-based**: Cookie sessions, secure attributes
- **Passport.js**: Strategy pattern for auth providers
- **Lucia Auth**: Modern, framework-agnostic auth

### 7. Databases

#### PostgreSQL
- **Schema Design**: Normalization, indexing, partitions
- **ORMs**: Prisma, Drizzle, TypeORM, Kysely
- **Migrations**: Version-controlled schema changes
- **Full-Text Search**: `tsvector`, `pg_trgm`
- **Extensions**: PostGIS, pg_cron, pgvector

#### MongoDB
- **Schema Design**: Embedding vs referencing
- **Indexes**: Compound, text, geospatial
- **Aggregation Pipeline**: Complex queries
- **Change Streams**: Real-time updates

#### Redis
- **Use Cases**: Caching, sessions, pub/sub, queues
- **Data Structures**: Strings, hashes, lists, sets, sorted sets
- **Pattern**: Rate limiting, leaderboard, real-time analytics

#### SQLite (Turso/LibSQL)
- **Edge Databases**: Distributed SQLite for edge computing
- **Drizzle ORM**: Type-safe SQLite queries

### 8. Security (OWASP Top 10 - 2025)

#### Critical Vulnerabilities
1. **Broken Access Control**: RBAC, principle of least privilege
2. **Cryptographic Failures**: TLS 1.3, bcrypt/argon2, key rotation
3. **Injection**: Parameterized queries, input validation
4. **Insecure Design**: Threat modeling, secure architecture
5. **Security Misconfiguration**: Hardening, env variables
6. **Vulnerable Components**: Dependency scanning (Snyk, npm audit)
7. **Auth Failures**: MFA, rate limiting, account lockout
8. **Data Integrity Failures**: CI/CD security, signed commits
9. **Logging Failures**: Audit trails, SIEM integration
10. **SSRF**: Allowlisting, network segmentation

#### Security Headers
```
Content-Security-Policy: default-src 'self'; script-src 'self'
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
Strict-Transport-Security: max-age=63072000; includeSubDomains
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: camera=(), microphone=()
```

### 9. Performance Optimization

#### Core Web Vitals
- **LCP** (Largest Contentful Paint): < 2.5s
- **INP** (Interaction to Next Paint): < 200ms
- **CLS** (Cumulative Layout Shift): < 0.1

#### Strategies
- **Code Splitting**: Route-based, component-based lazy loading
- **Tree Shaking**: Eliminate unused code
- **Image Optimization**: WebP/AVIF, responsive images, lazy loading
- **Font Optimization**: `font-display: swap`, subsetting, preloading
- **Caching**: Service workers, HTTP cache headers, CDN
- **Compression**: Brotli, gzip
- **Preloading**: `<link rel="preload">`, DNS prefetch, preconnect
- **Bundle Analysis**: Identify and eliminate large dependencies

### 10. Testing

#### Unit Testing
- **Vitest**: Fast, ESM-native, Vite-compatible
- **Jest**: Widely adopted, extensive ecosystem
- **Testing Library**: Component testing (React, Vue, etc.)

#### Integration & E2E
- **Playwright**: Cross-browser testing, auto-wait, network interception
- **Cypress**: Developer-friendly E2E testing
- **Storybook**: Component development and visual testing

#### Best Practices
- Test behavior, not implementation
- Use MSW for API mocking
- Snapshot testing for UI regression
- Coverage thresholds for critical paths

### 11. DevOps & Deployment

#### Containerization
```dockerfile
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM node:20-alpine AS runner
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
CMD ["node", "dist/index.js"]
```

#### CI/CD
- **GitHub Actions**: Lint, test, build, deploy
- **GitLab CI/CD**: Pipeline configuration
- **Vercel/Netlify**: Zero-config deployments

#### Platforms
- **Vercel**: Next.js optimized, edge functions, ISR
- **Cloudflare Workers**: Edge computing, KV storage
- **AWS**: Lambda, ECS, RDS, S3
- **Railway/Fly.io**: PaaS for full-stack apps

### 12. Monitoring & Observability

- **Error Tracking**: Sentry, LogRocket, Bugsnag
- **APM**: Datadog, New Relic, OpenTelemetry
- **Analytics**: Plausible, PostHog, Mixpanel
- **Uptime**: BetterStack, UptimeRobot

## Tool Integration

### Context7 MCP (Documentation Access)
For up-to-date library documentation, use Context7 MCP:
```json
{
  "mcpServers": {
    "context7": {
      "url": "https://mcp.context7.com/mcp"
    }
  }
}
```
Tools: `resolve-library-id`, `get-library-docs`

### MCP Servers for Web Development
- **@modelcontextprotocol/server-filesystem**: Secure file operations
- **@modelcontextprotocol/server-git**: Git repository operations
- **@modelcontextprotocol/server-fetch**: Web content fetching
- **@upstash/context7-mcp**: Up-to-date library documentation
- **Playwright MCP**: Browser automation and testing
- **Puppeteer MCP**: Browser automation

### Recommended MCP Configuration
```json
{
  "mcpServers": {
    "context7": { "url": "https://mcp.context7.com/mcp" },
    "filesystem": { "command": "npx", "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/project"] },
    "git": { "command": "uvx", "args": ["mcp-server-git", "--repository", "/path/to/repo"] }
  }
}
```

## Workflow

### When Building a Web Application
1. **Architecture**: Choose stack (Next.js + TypeScript + Tailwind + PostgreSQL)
2. **Setup**: Initialize project, configure tooling (ESLint, Prettier, Husky)
3. **Database**: Design schema, run migrations, seed data
4. **API**: Implement routes/endpoints, validate input (Zod)
5. **UI**: Build components, implement responsive layout
6. **Auth**: Set up authentication (NextAuth, Lucia)
7. **Testing**: Write unit, integration, and E2E tests
8. **Performance**: Optimize images, fonts, bundle size
9. **Security**: Implement OWASP best practices
10. **Deploy**: Set up CI/CD, deploy to production

### When Debugging
1. **Reproduce**: Create minimal reproduction case
2. **Check Console**: Browser dev tools, server logs
3. **Network**: Inspect requests/responses
4. **Performance**: Lighthouse, Core Web Vitals
5. **Security**: npm audit, dependency scanning

### When Reviewing Code
1. **Correctness**: Logic errors, edge cases
2. **Security**: Injection, XSS, CSRF, auth bypasses
3. **Performance**: Unnecessary re-renders, N+1 queries
4. **Accessibility**: ARIA, keyboard navigation, screen readers
5. **Maintainability**: Clean code, SOLID principles, DRY

## Reference Documentation

### Primary Sources (Fetched & Embedded)
- **MDN Web Docs**: https://developer.mozilla.org/en-US/docs/Learn
- **Next.js Docs**: https://nextjs.org/docs (v16.2.10)
- **React Docs**: https://react.dev/learn
- **Tailwind CSS**: https://tailwindcss.com/docs (v4.3)
- **TypeScript Handbook**: https://typescriptlang.org/docs/handbook
- **OWASP Top 10**: https://owasp.org/Top10/2025/

### MCP Registry
- **Official MCP Servers**: https://github.com/modelcontextprotocol/servers
- **Awesome MCP Servers**: https://github.com/punkpeye/awesome-mcp-servers (90.8k stars)
- **Glama MCP Registry**: https://glama.ai/mcp/servers (56,310+ servers)
- **Official MCP Registry**: https://registry.modelcontextprotocol.io/

### Key MCP Servers for Web Dev
- **Context7**: `@upstash/context7-mcp` — Up-to-date library documentation
- **Playwright**: Browser automation and E2E testing
- **Puppeteer**: Headless Chrome automation
- **Filesystem**: Secure file operations
- **Git**: Repository operations
- **Fetch**: Web content retrieval

## Environment Setup

### Recommended Toolchain
- **Runtime**: Node.js 20+ LTS
- **Package Manager**: pnpm (preferred), npm, yarn
- **Bundler**: Vite (preferred), Webpack, Turbopack
- **Linter**: ESLint 9+ with flat config
- **Formatter**: Prettier
- **Type Checker**: TypeScript 5.5+
- **CSS**: Tailwind CSS 4+
- **Testing**: Vitest + Playwright
- **Database**: PostgreSQL 16+ with Drizzle ORM

### Quick Start Commands
```bash
# Create Next.js project
npx create-next-app@latest my-app --typescript --tailwind --eslint --app --src-dir

# Install Context7 MCP
claude mcp add --scope user context7 -- npx -y @upstash/context7-mcp

# Start development
npm run dev
```
