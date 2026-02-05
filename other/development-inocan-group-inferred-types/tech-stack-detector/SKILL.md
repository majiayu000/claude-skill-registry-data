---
name: Tech Stack Detector
description: This skill should be used when the user asks about "detecting tech stack", "identifying technologies", "project dependencies", "framework detection", "build tool discovery", or needs to automatically identify and document the technologies used in a project.
version: 1.0.0
---

# Tech Stack Detector Skill

This skill provides intelligent detection of technologies, frameworks, and tools used in a project.

## Detection Matrix

### Languages

| Language | Detection Files | Indicators |
|----------|----------------|------------|
| TypeScript | tsconfig.json, *.ts, *.tsx | `"typescript"` in deps |
| JavaScript | *.js, *.jsx, jsconfig.json | No tsconfig |
| Python | pyproject.toml, setup.py, *.py | `python`, `pip`, `poetry` |
| Go | go.mod, go.sum, *.go | `module` declaration |
| Rust | Cargo.toml, *.rs | `[package]` section |
| Java | pom.xml, build.gradle, *.java | Maven/Gradle markers |
| C# | *.csproj, *.sln | MSBuild configs |
| Ruby | Gemfile, *.rb | `gem` declarations |
| PHP | composer.json, *.php | `"require"` section |

### Frontend Frameworks

| Framework | Detection | Key Indicators |
|-----------|-----------|----------------|
| React | `react` in deps | JSX files, hooks patterns |
| Vue | `vue` in deps | `.vue` files, Options/Composition API |
| Angular | `@angular/core` | `*.component.ts`, decorators |
| Svelte | `svelte` in deps | `.svelte` files |
| Next.js | `next` in deps | `pages/` or `app/` directory |
| Nuxt | `nuxt` in deps | `nuxt.config.*` |
| Remix | `@remix-run/*` | `app/routes/` structure |
| Astro | `astro` in deps | `.astro` files |

### Backend Frameworks

| Framework | Detection | Key Indicators |
|-----------|-----------|----------------|
| Express | `express` in deps | `app.use()`, route handlers |
| Fastify | `fastify` in deps | Plugin architecture |
| NestJS | `@nestjs/core` | Decorators, modules |
| Django | `django` in requirements | `settings.py`, `urls.py` |
| FastAPI | `fastapi` in requirements | `@app.get()` decorators |
| Flask | `flask` in requirements | `@app.route()` |
| Spring | `spring-boot` in pom | `@RestController` |
| Rails | `rails` in Gemfile | MVC structure |
| Laravel | `laravel/framework` | `artisan`, `routes/web.php` |

### Desktop Frameworks

| Framework | Detection | Key Indicators |
|-----------|-----------|----------------|
| Electron | `electron` in deps | `main.js`, `preload.js` |
| Tauri | `@tauri-apps/*` | `tauri.conf.json` |
| Qt | CMakeLists.txt + Qt | `#include <Qt*>` |

### Build Tools

| Tool | Detection File | Config Pattern |
|------|----------------|----------------|
| Vite | vite.config.* | `defineConfig()` |
| Webpack | webpack.config.* | `module.exports = {}` |
| Rollup | rollup.config.* | `export default {}` |
| esbuild | esbuild.config.* | `build()` calls |
| Turbo | turbo.json | `pipeline` config |
| Nx | nx.json | `projects`, `generators` |
| Parcel | package.json "source" | No config file needed |
| SWC | .swcrc | `jsc` config |

### Package Managers

| Manager | Detection File | Lock File |
|---------|----------------|-----------|
| npm | package.json | package-lock.json |
| yarn | package.json | yarn.lock |
| pnpm | package.json | pnpm-lock.yaml |
| bun | package.json | bun.lockb |
| pip | requirements.txt | - |
| poetry | pyproject.toml | poetry.lock |
| cargo | Cargo.toml | Cargo.lock |
| maven | pom.xml | - |
| gradle | build.gradle | gradle.lockfile |

### Testing Frameworks

| Framework | Detection | Config File |
|-----------|-----------|-------------|
| Jest | `jest` in deps | jest.config.* |
| Vitest | `vitest` in deps | vitest.config.* |
| Mocha | `mocha` in deps | .mocharc.* |
| Cypress | `cypress` in deps | cypress.config.* |
| Playwright | `@playwright/test` | playwright.config.* |
| Pytest | `pytest` in requirements | pytest.ini, pyproject.toml |
| JUnit | pom.xml + junit | - |
| RSpec | `rspec` in Gemfile | .rspec |

### Databases

| Database | Detection | Connection Patterns |
|----------|-----------|---------------------|
| PostgreSQL | `pg`, `psycopg2` | `postgres://`, `postgresql://` |
| MySQL | `mysql2`, `mysqlclient` | `mysql://` |
| MongoDB | `mongodb`, `mongoose` | `mongodb://` |
| Redis | `redis`, `ioredis` | `redis://` |
| SQLite | `sqlite3`, `better-sqlite3` | `.db`, `.sqlite` files |
| Prisma | `@prisma/client` | `schema.prisma` |
| Drizzle | `drizzle-orm` | `drizzle.config.ts` |

### Cloud & Infrastructure

| Service | Detection | Config |
|---------|-----------|--------|
| AWS | `@aws-sdk/*` | `.aws/`, `serverless.yml` |
| GCP | `@google-cloud/*` | `gcloud` references |
| Azure | `@azure/*` | `azure-pipelines.yml` |
| Vercel | `vercel` in deps | `vercel.json` |
| Docker | Dockerfile | `docker-compose.yml` |
| Kubernetes | k8s manifests | `*.yaml` with `apiVersion` |
| Terraform | `*.tf` files | `main.tf`, `variables.tf` |

## Detection Algorithm

```typescript
async function detectTechStack(projectRoot: string): Promise<TechStack> {
  const detections: Detection[] = [];

  // Phase 1: File-based detection (fast)
  const files = await glob(['package.json', 'tsconfig.json', '*.config.*', ...]);
  for (const file of files) {
    detections.push(...detectFromFile(file));
  }

  // Phase 2: Content-based detection (selective)
  const sampleFiles = selectRepresentativeFiles(projectRoot);
  for (const file of sampleFiles) {
    detections.push(...detectFromContent(file));
  }

  // Phase 3: Confidence scoring
  const stack = aggregateDetections(detections);
  return rankByConfidence(stack);
}
```

## Output Format

```markdown
## Tech Stack Analysis

### Primary Technologies
| Technology | Version | Confidence | Evidence |
|------------|---------|------------|----------|
| TypeScript | 5.3.x | HIGH | tsconfig.json, *.ts files |
| React | 18.x | HIGH | package.json, JSX patterns |
| Next.js | 14.x | HIGH | next.config.js, app/ directory |

### Build & Development
| Tool | Version | Purpose |
|------|---------|---------|
| pnpm | 8.x | Package manager |
| Turbo | 1.x | Monorepo build |
| Vite | 5.x | Dev server, bundling |

### Testing
| Framework | Coverage | Purpose |
|-----------|----------|---------|
| Jest | HIGH | Unit tests |
| Playwright | MEDIUM | E2E tests |

### Infrastructure
| Service | Purpose |
|---------|---------|
| Docker | Containerization |
| Vercel | Deployment |

### Uncertain Detections
⚠️ Redis: Found redis dependency but no connection config
⚠️ GraphQL: Found @apollo/client but no schema files
```

## Integration with Steering

When invoked during `/steering`:

1. **Phase 2 (Tech Discovery)** automatically uses this skill
2. Populates `tech.md` with detected stack
3. Generates accurate build commands
4. Identifies environment variable requirements
5. Detects testing framework for test commands

## Confidence Levels

```
HIGH:   Config file + code evidence + dependencies
MEDIUM: Config file + dependencies (no code evidence)
LOW:    Dependencies only (may be unused)
```
