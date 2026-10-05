---
name: ai-text-to-image-app
description: Template for creating text-to-image applications. ONLY trigger when user explicitly requests to CREATE/BUILD a text-to-image app (e.g., "创建文生图应用", "做一个AI生图应用", "build a text-to-image app", "create an image generation application").
_meta_type: template
_meta_template_name: web
---

## Prerequisites

1. Initialize Project (if needed):
```bash
REPO_ROOT/.genie/scripts/bash/setup-project.sh web ai-text-to-image
```

2. **Generate `docs/product/features.md` before writing any code** — product overview, core features, user stories, page structure, data models, API endpoints.

**Validation**: If `docs/product/features.md` does not exist, STOP and create it first.

3. Make a best design by SKILL: `ui-ux-pro-max` for first time
4. Use SKILL `text-to-image` for generating images, icons, or illustrations when needed.
5. Use the SKILL `*-integrator` to fully realize the user's needs.
6. **CRITICAL: Set up database tables using TCB**
```
bash /workspace/.codebuddy/skills/genie-tcb-db-integrator/scripts/tcb-pg-migrate.sh --project-dir /workspace --sql "CREATE TABLE ..."
```

**CRITICAL**: On the first conversation, after initializing the project (REPO_ROOT/.genie/scripts/bash/setup-project.sh web ai-text-to-image), end the current conversation turn immediately and inform the user that the project has been generated.

## Best Practices

### General Principles

- **Perfect Architecture**: Refactor when needed, eliminate duplication, maintain clean separation
- **Parallel Tool Calls**: Execute independent operations simultaneously
- **Less is More**: Quality over quantity unless enterprise landing page requested
- **Leverage Existing Dependencies**: Prefer existing libraries over new ones
- **Animations**: Use the **ui-animation** skill for all animation needs (MotionPrimitives for page transitions, ReactBits for creative effects)

### SEO (Automatic for All Pages)

- Title tags under 60 chars with keyword
- Meta description max 160 chars
- Single H1 matching page intent
- Semantic HTML (`<header>`, `<nav>`, `<main>`, `<footer>`, `<article>`, `<section>`)
- Image alt attributes with keywords
- JSON-LD for products/articles/FAQs
- Lazy loading for images
- Canonical tags

## Web Template Architecture

```
/
├── backend/                           # Express.js + TypeScript
│   ├── package.json
│   ├── tsconfig.json
│   ├── jest.config.mjs
│   ├── eslint.config.js
│   ├── .env / .env.example
│   └── src/
│       ├── index.ts                   # Server entry point
│       ├── app.ts                     # Express configuration
│       ├── config/
│       │   ├── env.ts                 # Environment validation (Zod)
│       │   └── logger.ts              # Pino logger factory
│       ├── modules/
│       │   ├── generate.ts            # Image generation API
│       │   ├── image.ts               # Image CRUD operations
│       │   └── system.ts              # Health check endpoints
│       ├── types/
│       │   ├── generate.types.ts
│       │   └── image.types.ts
│       ├── middleware/
│       │   ├── auth.middleware.ts
│       │   ├── errorHandler.ts
│       │   ├── logger.ts
│       │   └── validation.ts
│       └── __tests__/
│           ├── setup.ts
│           └── system.test.ts
│
├── frontend/                          # React 19 + Vite
│   ├── package.json
│   ├── vite.config.ts
│   ├── tailwind.config.ts
│   ├── components.json                # shadcn/ui config
│   ├── index.html
│   └── src/
│       ├── main.tsx                   # Entry point
│       ├── App.tsx                    # Root component with providers
│       ├── index.css                  # Global styles + Tailwind theme
│       ├── components/
│       │   ├── generator/             # Image generation components
│       │   │   ├── AdvancedSettings.tsx
│       │   │   ├── ImageResult.tsx
│       │   │   └── PromptInput.tsx
│       │   ├── layout/                # Layout components
│       │   │   ├── Header.tsx
│       │   │   ├── Footer.tsx
│       │   │   └── Layout.tsx
│       │   └── ui/                    # shadcn/ui components
│       ├── contexts/
│       │   └── AuthContext.tsx
│       ├── hooks/
│       │   ├── use-auth.ts
│       │   ├── use-images.ts
│       │   └── use-mobile.ts
│       ├── lib/
│       │   ├── api-client.ts          # Axios with interceptors
│       │   └── utils.ts               # cn utility
│       ├── pages/
│       │   ├── Index.tsx
│       │   ├── Gallery.tsx
│       │   ├── Login.tsx
│       │   ├── Register.tsx
│       │   ├── Help.tsx
│       │   ├── Privacy.tsx
│       │   ├── Terms.tsx
│       │   └── NotFound.tsx
│       └── types/
│
└── docs/
    ├── project.json
    ├── pages.json
    ├── design/
    │   └── default.style-guide.html
    ├── posters/
    │   └── app/
    │       └── app-poster.png
    └── product/
        └── features.md
```


## Technical References

Detailed implementation patterns in `references/`:

- **[api-protocol.md](references/api-protocol.md)**: JSON-based API standard (CRITICAL - no URL parameters for data operations)
- **[frontend-patterns.md](references/frontend-patterns.md)**: Import management, React Router compatibility, WebSocket
- **[architecture.md](references/architecture.md)**: Complete monorepo structure, key files, commands

## Quick Reference

### Adding New Resources

**Frontend:**
1. Define types in `src/types/[resource].ts`
2. Create hooks in `src/hooks/use-[resources].ts`
3. Build components using JSON-based API calls

**Backend:**
1. Create types in `src/types/[resource].types.ts`
2. Create module in `src/modules/[resource].ts`
3. Register router in `src/app.ts`

### Key Commands

```bash
# Debugging
python3 "$PROJECT_ROOT/.genie/scripts/python/fetch_monitor_errors.py"
```

### Critical Rules

1. **JSON Protocol**: All data operations use POST with JSON body, not URL parameters
2. **BrowserRouter Only**: No Data Router features (ScrollRestoration, useMatches, etc.)
3. **Import Everything**: Every component/function used must be imported
4. **53 shadcn/ui Components**: Use existing, DO NOT create custom versions
5. **WebSocket**: Must use `/api` prefix and dynamic protocol/host
6. **oklch Color Format**: ALL color CSS variables in `index.css` MUST use `oklch()` format. NEVER use bare HSL (`220 14% 96%`), hex, hsl(), or rgb().

### Launch Configuration

`.cloudstudio` file defines startup - DO NOT modify. Always use unified process script.
