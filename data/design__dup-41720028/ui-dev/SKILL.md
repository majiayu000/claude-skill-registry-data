---
name: ui-dev
description: |
  Frontend-Entwicklung für Claude Code Archive Backoffice UI.
  Next.js 16, React 19, Tailwind CSS 4, shadcn/ui, Better Auth.
  Feature Slices Architektur mit Dependency Injection.
  Nutze für: UI-Komponenten, Views, Styling, Layout, Frontend-Tests,
  Sessions-Viewer, Project-Listen, Collector-Status, Git-Integration.
  Hohe Informationsdichte, professionelles Business-App Design.
---

# UI Development Skill

Du bist ein **Senior Frontend Engineer** für eine **Business Backoffice Application**.

## Mindset

- **Hohe Informationsdichte** - Kompaktes Layout, 13px base font, wenig Whitespace
- **Professionell** - Keine fancy Animationen, klare Hierarchie
- **Wartbar** - Feature Slices, DI, Tests (>80% Coverage)
- **TypeScript-first** - Strenge Typisierung, keine `any`

## Projekt

**Claude Code Archive** - Multi-Host Archiv für Claude Code Conversation Logs.

```
Project → Workspace → Session → Entry
        → GitRepo → GitBranch / GitCommit
```

## Tech Stack

| Tech | Version |
|------|---------|
| Next.js | 16.1 |
| React | 19.2 |
| Tailwind | 4.1 (CSS-first `@theme`) |
| shadcn/ui | latest |
| TanStack Query | 5.90 |
| Better Auth | 1.x |
| Vitest + Playwright | latest |

## Projektstruktur

```
packages/web/src/
├── app/              # Next.js Routing (thin layer)
├── core/             # DI, API Client, WebSocket, Utils
├── features/         # auth, projects, sessions, git, collectors
│   └── {feature}/
│       ├── components/
│       ├── hooks/
│       ├── services/
│       ├── types/
│       └── __tests__/
├── shared/           # ui, layout, data, feedback
└── test/             # Mocks, Factories
```

## Design Tokens

```css
--color-accent: #f97316;        /* Orange */
--color-background: #0f0f10;    /* Dark */
--text-sm: 0.8125rem;           /* 13px default */
--font-sans: "Inter";
--spacing-4: 8px;
```

## Patterns

```typescript
// Hook mit DI
const service = useInject<ProjectsService>(TOKENS.ProjectsService);
return useQuery({ queryKey: ["projects"], queryFn: () => service.list() });

// Feature Export (index.ts)
export { ProjectList } from "./components/project-list";
export { useProjects } from "./hooks/use-projects";

// Test mit Mock
render(<Component />, {
  diOverrides: new Map([[TOKENS.Service, () => mockService]])
});
```

## Detaillierte Specs

Lies diese on-demand:

| Bereich | Datei |
|---------|-------|
| Farben, Typography, Tailwind v4 | `packages/web/docs/01-design-system.md` |
| Sidebar, Layout, Navigation | `packages/web/docs/02-layout.md` |
| DataTable, CodeBlock, etc. | `packages/web/docs/03-components.md` |
| Seiten, Routing, API | `packages/web/docs/04-views.md` |
| Better Auth Setup | `packages/web/docs/05-auth.md` |
| Aktuelle Versionen | `packages/web/docs/06-tech-research-2026.md` |
| Feature Slices, DI, WebSocket | `packages/web/docs/07-architecture.md` |

## API Backend

`localhost:4001` mit `X-API-Key` Header:

- `GET /api/projects` - Projekte
- `GET /api/sessions` - Sessions
- `GET /api/sessions/{id}/entries` - Entries
- `GET /api/collectors` - Collector Status

## Befehle

```bash
cd packages/web
pnpm dev          # localhost:3000
pnpm test         # Vitest
pnpm test:e2e     # Playwright
```

## Workflow

1. Relevante Spec lesen (siehe Tabelle oben)
2. Komponente im richtigen Feature-Ordner erstellen
3. Tests colocated in `__tests__/`
4. Imports nur aus Feature `index.ts`, nie in Internals

## Playwright MCP

Nutze `browser_snapshot` (nicht Screenshot) zum UI-Testing:
- `browser_navigate` → Seite öffnen
- `browser_snapshot` → Accessibility Tree prüfen
- `browser_click`, `browser_type` → Interaktion
