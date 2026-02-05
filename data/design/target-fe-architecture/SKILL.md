---
name: target-fe-architecture
description: Target frontend architecture for Lingx. Progressive FSD Hybrid combining Next.js App Router with Feature-Sliced Design layers. Use when implementing frontend features, reviewing code, or making architectural decisions.
---

# Lingx Frontend Architecture

Progressive FSD Hybrid: Next.js App Router + FSD layers when complexity grows.

## Why Progressive FSD?

| Challenge                   | Solution                                                      |
| --------------------------- | ------------------------------------------------------------- |
| Simple pages become complex | Migrate to widgets/features when needed                       |
| Shared components scattered | Organize by business domain (entities)                        |
| Feature coupling            | Strict layer imports (shared → entities → features → widgets) |
| App Router integration      | Keep pages thin, compose FSD components                       |

## Directory Structure

```
apps/web/src/
├── app/                        # Next.js App Router (thin pages)
│   ├── (auth)/                 # Auth route group
│   ├── (dashboard)/            # Dashboard route group
│   ├── (project)/              # Project route group
│   └── workbench/              # Translation editor
├── widgets/                    # Complex UI blocks (when needed)
│   └── translation-editor/     # Real-time collaborative editor
├── features/                   # User actions (when needed)
│   └── ai-translate/           # AI translation feature
├── entities/                   # Business entities (when needed)
│   └── project/                # Project card, list item
├── shared/                     # Always use
│   ├── ui/                     # shadcn/ui components
│   ├── api/                    # API client, React Query hooks
│   ├── lib/                    # Utilities (cn, formatters)
│   └── hooks/                  # Shared hooks
└── components/                 # Legacy (migrate over time)
```

## Layer Hierarchy

```
┌─────────────────────────────────────────────────────────────┐
│  app/                                                        │
│  Pages compose widgets and features, fetch data on server    │
└─────────────────────┬───────────────────────────────────────┘
                      │ imports
┌─────────────────────▼───────────────────────────────────────┐
│  widgets/                                                    │
│  Complex UI blocks with internal state and multiple features │
└─────────────────────┬───────────────────────────────────────┘
                      │ imports
┌─────────────────────▼───────────────────────────────────────┐
│  features/                                                   │
│  User actions: forms, modals, buttons with side effects      │
└─────────────────────┬───────────────────────────────────────┘
                      │ imports
┌─────────────────────▼───────────────────────────────────────┐
│  entities/                                                   │
│  Business objects: cards, list items, viewers                │
└─────────────────────┬───────────────────────────────────────┘
                      │ imports
┌─────────────────────▼───────────────────────────────────────┐
│  shared/                                                     │
│  UI primitives, utilities, API client - no business logic    │
└─────────────────────────────────────────────────────────────┘
```

**Import Rule**: Lower layers cannot import from higher layers.

## When to Use Each Layer

| Complexity              | Location                   | Example               |
| ----------------------- | -------------------------- | --------------------- |
| Simple page-specific    | `app/[route]/_components/` | Dashboard stats card  |
| Shared UI primitive     | `shared/ui/`               | Button, Input, Card   |
| Business entity display | `entities/`                | ProjectCard, KeyRow   |
| User action             | `features/`                | AITranslate, BulkEdit |
| Complex widget          | `widgets/`                 | TranslationEditor     |

## Documentation

| Document                                     | Purpose                   |
| -------------------------------------------- | ------------------------- |
| [fsd-overview.md](fsd-overview.md)           | FSD layers explained      |
| [migration-rules.md](migration-rules.md)     | When to adopt FSD layers  |
| [widgets.md](widgets.md)                     | Widget patterns           |
| [features.md](features.md)                   | Feature patterns          |
| [entities.md](entities.md)                   | Entity patterns           |
| [server-components.md](server-components.md) | RSC patterns              |
| [hooks.md](hooks.md)                         | Custom hooks              |
| [data-fetching.md](data-fetching.md)         | Server vs client fetching |

## Quick Reference

### App Router Page (Thin)

```tsx
// app/(project)/projects/[id]/page.tsx
import { getProject } from '@/shared/api/projects';
import { ProjectHeader } from '@/entities/project';
import { TranslationEditor } from '@/widgets/translation-editor';

export default async function ProjectPage({ params }: Props) {
  const project = await getProject(params.id);

  return (
    <div className="space-y-6">
      <ProjectHeader project={project} />
      <TranslationEditor projectId={project.id} />
    </div>
  );
}
```

### Widget (Complex UI Block)

```tsx
// widgets/translation-editor/ui/translation-editor.tsx
'use client';

import { KeyList } from './key-list';
import { PresenceBar } from './presence-bar';
import { useRealtimeSync } from '../model/use-realtime-sync';
import { usePresence } from '../model/use-presence';

export function TranslationEditor({ projectId }: Props) {
  const { keys, updateKey } = useRealtimeSync(projectId);
  const { users, focusKey } = usePresence(projectId);

  return (
    <div className="island">
      <PresenceBar users={users} />
      <KeyList keys={keys} onUpdate={updateKey} onFocus={focusKey} />
    </div>
  );
}
```

### Feature (User Action)

```tsx
// features/ai-translate/ui/ai-translate-button.tsx
'use client';

import { Button } from '@/shared/ui/button';
import { useAITranslate } from '../model/use-ai-translate';

export function AITranslateButton({ keyId, targetLanguages }: Props) {
  const { translate, isPending } = useAITranslate();

  return (
    <Button onClick={() => translate({ keyId, targetLanguages })} disabled={isPending}>
      {isPending ? 'Translating...' : 'AI Translate'}
    </Button>
  );
}
```

### Entity (Business Object)

```tsx
// entities/project/ui/project-card.tsx
import Link from 'next/link';
import type { Project } from '@lingx/shared';

interface ProjectCardProps {
  project: Project;
}

export function ProjectCard({ project }: ProjectCardProps) {
  return (
    <Link href={`/projects/${project.id}`} className="island p-4">
      <h3 className="font-medium">{project.name}</h3>
      <p className="text-muted-foreground text-sm">{project.slug}</p>
    </Link>
  );
}
```

## Decision Tree

```
Should I use FSD layer?

Is it a simple page-specific component?
  └─ YES → Keep in app/[route]/_components/

Is it used across 3+ pages?
  └─ YES → Consider entities/ or features/

Does it have complex internal state?
  └─ YES → Consider widgets/

Is it a reusable UI primitive?
  └─ YES → Put in shared/ui/

Is it a user action with side effects?
  └─ YES → Put in features/

Otherwise → Start in _components/, migrate later
```

## Real-time Collaboration Widget

```
widgets/translation-editor/
├── index.ts                    # Public API
├── ui/
│   ├── translation-editor.tsx  # Main widget
│   ├── presence-bar.tsx        # Who's online
│   ├── key-list.tsx            # Keys with translations
│   ├── key-row.tsx             # Single key
│   └── conflict-dialog.tsx     # Conflict resolution
├── model/
│   ├── use-realtime-sync.ts    # WebSocket sync
│   ├── use-presence.ts         # Presence state
│   ├── use-optimistic-update.ts
│   └── types.ts
└── lib/
    └── conflict-resolver.ts    # OT/CRDT logic
```

## Anti-Patterns

### ❌ Feature importing widget

```tsx
// BAD - features cannot import widgets
import { TranslationEditor } from '@/widgets/translation-editor';

export function AITranslateFeature() {
  return <TranslationEditor />; // ❌
}
```

### ✅ Widget using feature

```tsx
// GOOD - widgets compose features
import { AITranslateButton } from '@/features/ai-translate';

export function TranslationEditor() {
  return (
    <div>
      <AITranslateButton keyId={keyId} /> {/* ✅ */}
    </div>
  );
}
```

### ❌ Entity with side effects

```tsx
// BAD - entities shouldn't have mutations
export function ProjectCard({ project }) {
  const { mutate } = useDeleteProject(); // ❌

  return (
    <Card>
      <button onClick={() => mutate(project.id)}>Delete</button>
    </Card>
  );
}
```

### ✅ Feature handles action

```tsx
// GOOD - features handle mutations
// features/delete-project/ui/delete-button.tsx
export function DeleteProjectButton({ projectId }) {
  const { mutate, isPending } = useDeleteProject();
  return <Button onClick={() => mutate(projectId)}>Delete</Button>;
}

// entities/project/ui/project-card.tsx
// Pass render prop or slot for actions
export function ProjectCard({ project, actions }) {
  return (
    <Card>
      <h3>{project.name}</h3>
      {actions}
    </Card>
  );
}
```

## Progressive Adoption

1. **Start simple**: New pages use `_components/`
2. **Extract when reused**: Move to entities when used 3+ places
3. **Extract on complexity**: Move to features when adding mutations
4. **Promote to widget**: When combining multiple features with state
5. **Keep shared lean**: Only true primitives (Button, Input, Card)

## Benefits

1. **Clear boundaries** - Each layer has one responsibility
2. **Predictable imports** - Always know where to look
3. **Isolated changes** - Modify one layer without affecting others
4. **Team scalability** - Different teams own different layers
5. **Progressive complexity** - Start simple, scale when needed

Sources:

- [Feature-Sliced Design](https://feature-sliced.design/)
- [Next.js App Router](https://nextjs.org/docs/app)
- [React Server Components](https://www.joshwcomeau.com/react/server-components/)
