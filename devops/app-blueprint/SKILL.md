---
name: app-blueprint
description: Analyze a codebase and produce a plain-language Application Blueprint in English and French (Dossier applicatif). Use to document, explain or reverse-engineer an app, or for "cahier des charges", "app blueprint", "application overview".
---

# Application Blueprint Skill

## Purpose

This skill reverse-engineers a codebase to produce a single, comprehensive Markdown document called an **Application Blueprint** (FR: **Dossier applicatif**). The document explains an application from end to end in plain, professional language accessible to non-technical readers, while remaining precise enough to be useful to developers and stakeholders.

The output is **always produced in two files**: one in English, one in French (Canadian conventions).

## When to Use

- User asks to "document this app", "explain how this works", "reverse-engineer this project"
- User mentions "cahier des charges", "blueprint", "application overview", "functional spec from code"
- User provides a codebase and wants a comprehensive understanding document
- User wants onboarding documentation for a new team member

## Workflow

### Phase 1 — Codebase Discovery

Before writing anything, Claude must understand the entire codebase. Execute these steps in order:

1. **List the project structure** — Run `find` or `view` on the root directory to get the full file tree (2-3 levels deep initially, then deeper as needed).

2. **Identify the tech stack** — Look at package files (`package.json`, `requirements.txt`, `*.csproj`, `pom.xml`, `Cargo.toml`, `composer.json`, etc.), configuration files, and framework markers.

3. **Read entry points** — Identify and read the main entry files (e.g., `main.ts`, `app.py`, `Program.cs`, `index.js`, `App.jsx`, `Startup.cs`).

4. **Map the architecture** — Identify patterns: MVC, microservices, serverless, monolith, event-driven, etc. Read routing files, middleware, and configuration.

5. **Catalog all features** — Trace routes/endpoints/pages/screens. Read controllers, services, components, and views. Identify every user-facing feature.

6. **Understand data models** — Read database schemas, migrations, entity definitions, ORMs, or data transfer objects.

7. **Trace integrations** — Identify external APIs, third-party services, authentication providers, payment systems, messaging queues, etc.

8. **Read business logic** — Understand core business rules, validation, calculations, and workflows in service/domain layers.

9. **Identify security model** — Authentication method, authorization/roles, data protection patterns.

10. **Check deployment** — Read Dockerfiles, CI/CD configs, environment files, infrastructure-as-code.

**Critical**: Do NOT skip files or make assumptions. Read every significant file. For large codebases, prioritize breadth first (understand the full structure), then depth (read each module). The goal is 100% coverage of the application's capabilities.

### Phase 2 — Document Writing

After completing Phase 1, write both documents following the canonical structure in `references/document-structure.md`.

**Writing process:**
1. Read `references/writing-guide-en.md` before writing the English version.
2. Read `references/writing-guide-fr.md` before writing the French version.
3. Follow the structure from `references/document-structure.md` exactly.
4. Use `references/style-checklist.md` as a final quality check.

**File naming convention:**
- English: `{app-name}-blueprint-en.md`
- French: `{app-name}-blueprint-fr.md`

Where `{app-name}` is derived from the project name (e.g., `invoice-tracker-blueprint-en.md`).

### Phase 3 — Quality Check

Before delivering, verify against the style checklist:
- Every section from the canonical structure is present (or explicitly marked N/A with rationale)
- Language is plain and accessible to non-developers
- No orphaned technical jargon without explanation
- French version follows Quebec/Canadian typography conventions
- Both versions are natural, professional, and human-sounding
- No AI-sounding filler phrases

## Output

Both files are saved to `/docs/` and presented to the user.

## Important Notes

- **Never fabricate features.** Only document what exists in the code.
- **Never skip modules.** If the codebase is large, process it systematically. Every route, component, service, and model must be accounted for.
- **Plain language first.** Technical terms are allowed but must always be accompanied by a brief explanation on first use.
- **The French version is NOT a translation.** It is a natively written document following French (Canadian) conventions, with the same content but natural phrasing in French. Do not translate the English version — write it fresh.
- **Adapt the structure.** The canonical structure covers most cases, but some sections may not apply (e.g., a CLI tool has no UI). Mark inapplicable sections as "N/A — [reason]" or omit them if they add no value. Conversely, add sections if the application warrants it (e.g., a "Plugin System" section for extensible apps).
