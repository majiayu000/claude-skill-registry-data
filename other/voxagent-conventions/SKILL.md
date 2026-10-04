---
name: voxagent-conventions
description: Project conventions, architecture rules, and coding standards for VoxAgent. Always follow these rules when writing code in this project.
---

# VoxAgent — AI Coding Guidelines

## Project Overview
VoxAgent is a voice-controlled desktop AI agent. It listens for "Hey Vox", transcribes speech, routes intents through a tiered model system, executes actions, and responds via TTS.

## Architecture Rules

### Module Boundaries (Python Agent)
### Module Boundaries (Python Agent)
- `core/` — Pipeline modules (ears, brain, hands, eyes, mouth, autopilot, memory). These MUST remain provider-agnostic.
- `providers/` — All model/API integrations. Every provider implements abstract interfaces from `providers/base.py`.
- `system/` — OS-specific code ONLY. All system integration code must implement `SystemAutomation` from `system/base.py`.
- `skills/` — Task implementations. Each skill must extend `BaseSkill` and declare `execution_tiers` + `permissions`.

### Critical Design Principles

1. **Provider-agnostic**: Core modules NEVER import specific providers directly. Always go through `providers/registry.py`.
2. **Execution Priority (Tier A→D)**: When implementing skills, always prefer Shell/API over UI automation. UI/mouse is LAST RESORT.
   - Tier A: Native API / Shell (subprocess, os, ctypes)
   - Tier B: App / Service API (Playwright CDP, REST APIs)
   - Tier C: UI Automation (pywinauto, pyobjc, AT-SPI)
   - Tier D: Mouse / Keyboard (PyAutoGUI) — only when no other option
3. **Cross-platform**: Use `system/base.py` interface. Never use win32-specific code outside `system/windows.py`.
4. **Security**: API keys go in OS keyring via `keyring` library, NEVER in config files. Skills must declare permissions.

---

## Dashboard Architecture Rules (React/TypeScript)

### Separation of Concerns — NO MIX CONCERNS

Every feature module MUST follow this folder structure:

```
features/{feature}/
├── components/            # UI only — no business logic
│   └── organisms/
│       └── {Component}/
│           └── {Component}.tsx
├── containers/            # Page-level composition + orchestration
│   └── {Feature}View.tsx
├── hooks/                 # Custom React hooks — API + state logic
│   └── use{Feature}.ts
├── types/                 # ALL type definitions for this feature
│   ├── index.ts           # Barrel re-export ONLY (no definitions)
│   ├── {feature}.types.ts # Domain/data types
│   └── components.types.ts# Component prop types
├── constants/             # Static data, mock data, enums, mappings
│   ├── index.ts           # Barrel re-export ONLY (no definitions)
│   ├── mocks.ts           # Mock/fallback data
│   └── ui.ts              # UI-related constants (styles, categories)
└── utils/                 # Pure utility functions
    ├── index.ts           # Barrel re-export ONLY (no definitions)
    └── {name}.ts          # Individual util modules
```

### Rules:

1. **Types go in `types/`** — NEVER define interfaces/types inline in component or hook files. Always import from `@features/{feature}/types` or `@shared/types`.
2. **Constants go in `constants/`** — NEVER define static arrays, maps, mock data, or configuration objects inline in components or hooks. Always import from `@features/{feature}/constants` or `@shared/constants`.
3. **Utils go in `utils/`** — Pure functions (formatters, filters, validators) MUST be in utils. Components and hooks should only contain React-specific logic.
4. **Components are pure UI** — Organisms receive data via props. No API calls, no direct state management beyond local UI state (open/close, hover, etc.).
5. **Hooks own the data** — All API fetching, state management, and side effects belong in hooks.
6. **Containers orchestrate** — Containers wire hooks to components. They should be thin — mostly just importing + composing.
7. **`index.ts` is barrel-only** — NEVER put definitions directly in `index.ts`. It should only re-export from sibling files. Split into multiple focused files by concern.

### Import Rules (enforced by ESLint):

- **BANNED**: Relative parent imports (`../`) — use `@shared/*` or `@features/*` path aliases.
- **Cross-feature imports**: Features MUST NOT import from other features directly. Share through `@shared/`.
- **Barrel exports**: Each folder (`types/`, `constants/`, `utils/`, `components/organisms/`) MUST have an `index.ts` barrel re-export.

### Shared Module (`shared/`)

```
shared/
├── api/           # API client, interceptors
├── components/    # Reusable atoms, molecules, organisms, templates
├── types/         # Shared TypeScript interfaces
├── constants/     # App-wide constants (routes, config)
└── utils/         # App-wide utilities
```

---

## Code Style

### Python
- Python 3.12+
- Type hints on all public methods
- async/await for all I/O operations
- Use `ruff` for formatting and linting
- Use `mypy` for type checking
- Docstrings in Vietnamese or English (both OK)

### TypeScript/React
- React 19+ with functional components only
- Strict TypeScript (`exactOptionalPropertyTypes: true`)
- Use `eslint` for linting
- Named exports only (no default exports)
- File naming: PascalCase for components, camelCase for hooks/utils

### Testing
- Every new skill needs tests in `tests/test_skills.py`
- Every new provider needs tests in `tests/test_providers.py`
- Mock external APIs, never make real API calls in tests
- Target: >80% coverage on core/ and skills/

### File Naming
- Python modules: `snake_case.py`
- Skills: `skills/{skill_name}.py` matching the `name` field in the class
- Providers: `providers/{type}/{provider_name}.py`
- Tests: `tests/test_{module}.py`
- React components: `PascalCase.tsx`
- React hooks: `use{Name}.ts`
- Types/Constants/Utils: `index.ts` (barrel) or `{name}.ts`

### Commit Convention
- `feat:` new feature
- `fix:` bug fix
- `refactor:` code restructuring
- `docs:` documentation only
- `test:` test changes
- `chore:` build/config changes
