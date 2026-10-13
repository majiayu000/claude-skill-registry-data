---
name: devops-advisor
description: Audits infrastructure setup — database config, caching, performance, and scaling patterns. Provides concrete detection commands and improvement steps. Use when the user asks about "infrastructure", "database setup", "caching", "scaling", "performance", or "architecture". Don't use for CI/CD setup (use deployment-engineer), monitoring (use monitoring-setup), or security (use security-auditor).
---

# DevOps Advisor

Assesses infrastructure maturity and provides actionable improvement steps with concrete detection commands.

## How It Works

1. Run detection commands to understand current infrastructure
2. Assess each infrastructure dimension
3. Generate prioritized recommendations with effort estimates
4. Provide concrete implementation steps

## Step-by-Step Procedure

### Step 1: Detect Database Setup
```bash
# Check for ORM/database config
grep -rn "prisma\|drizzle\|typeorm\|sequelize\|mongoose\|knex\|sqlalchemy\|diesel" package.json Cargo.toml requirements.txt pyproject.toml 2>/dev/null | head -10

# Check for connection pooling
grep -rn "connectionLimit\|pool\|pgbouncer\|connection_pool\|max_connections\|pool_size" --include="*.ts" --include="*.js" --include="*.py" --include="*.toml" . 2>/dev/null | head -10

# Check for migrations
ls -la prisma/migrations/ migrations/ alembic/ db/migrate/ 2>/dev/null

# Check for database backups config
grep -rn "backup\|pg_dump\|mongodump\|mysqldump" --include="*.yml" --include="*.yaml" --include="*.sh" . 2>/dev/null | head -5
```

### Step 2: Detect Caching Strategy
```bash
# Check for Redis/cache usage
grep -rn "redis\|upstash\|memcached\|cache-control\|stale-while-revalidate\|@cacheable" --include="*.ts" --include="*.js" --include="*.py" . 2>/dev/null | head -10

# Check for CDN configuration
grep -rn "cdn\|cloudfront\|cloudflare\|fastly\|images.*remotePatterns" --include="*.ts" --include="*.js" --include="*.json" . 2>/dev/null | head -5

# Check for ISR/SSG in Next.js
grep -rn "revalidate\|getStaticProps\|getStaticPaths\|generateStaticParams" --include="*.ts" --include="*.tsx" . 2>/dev/null | head -5
```

### Step 3: Detect Performance Setup
```bash
# Check for image optimization
grep -rn "next/image\|sharp\|imagemin\|squoosh" --include="*.ts" --include="*.tsx" --include="*.js" package.json 2>/dev/null | head -5

# Check bundle size tooling
grep -rn "analyze\|webpack-bundle-analyzer\|source-map-explorer\|bundlephobia" package.json 2>/dev/null

# Check for code splitting / lazy loading
grep -rn "dynamic(\|lazy(\|React.lazy\|import(" --include="*.ts" --include="*.tsx" . 2>/dev/null | head -5

# Measure build output size (if Next.js)
ls -lh .next/static/chunks/ 2>/dev/null | tail -5
```

### Step 4: Detect Scaling Readiness
```bash
# Check for queue/background job setup
grep -rn "bullmq\|bull\|celery\|sidekiq\|inngest\|trigger.dev\|temporal" package.json requirements.txt 2>/dev/null

# Check for statelessness indicators
grep -rn "session\|cookie-session\|express-session\|JWT_SECRET\|NEXTAUTH" --include="*.ts" --include="*.js" . 2>/dev/null | head -5

# Check for horizontal scaling config
cat docker-compose.yml 2>/dev/null | grep -A5 "replicas\|scale\|deploy"
```

### Step 5: Check Database Indexing
```bash
# Prisma: check for @@index annotations
grep -rn "@@index\|@@unique" --include="*.prisma" . 2>/dev/null | head -10

# SQL: check for CREATE INDEX
grep -rn "CREATE INDEX\|ADD INDEX" --include="*.sql" . 2>/dev/null | head -10
```

## Output Format

```markdown
## 🏗️ Infrastructure Assessment

### Database
- Connection pooling: {✅/⚠️/❌} {details}
- Migrations: {✅/⚠️/❌} {details}
- Backups: {✅/⚠️/❌} {details}
- Indexing: {✅/⚠️/❌} {details}

### Caching
- Redis/cache layer: {✅/⚠️/❌} {details}
- CDN: {✅/⚠️/❌} {details}
- Static generation: {✅/⚠️/❌} {details}

### Performance
- Image optimization: {✅/⚠️/❌} {details}
- Bundle analysis: {✅/⚠️/❌} {details}
- Code splitting: {✅/⚠️/❌} {details}

### Scaling
- Background jobs: {✅/⚠️/❌} {details}
- Stateless design: {✅/⚠️/❌} {details}
- Horizontal scaling: {✅/⚠️/❌} {details}

### Recommendations (Priority Order)
1. **{Recommendation}** — Impact: {High/Med/Low} — Effort: {Low/Med/High}
   Why: {one sentence explaining business impact}
   How: {one sentence with concrete first step}
```

## Important
- Prioritize by business impact, not technical elegance
- Explain WHY each recommendation matters in plain English
- Always start with what's ALREADY working before listing gaps
- For databases: connection pooling > indexing > backups > read replicas
- For caching: CDN > static generation > application cache > Redis
