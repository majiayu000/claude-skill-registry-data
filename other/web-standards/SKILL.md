---
name: web-standards
description: "Index of official React, Next.js, TypeScript, Testing Library, Playwright and MDN docs, and web house patterns."
---

Read the project AGENTS.md and applicable global guidance first. Fall back to CLAUDE.md if AGENTS.md is absent. Follow the global rules for optional tools, specialist agents and Git actions.

# Web standards reference

Use this to pick the authoritative source for a question. For a standard, quote its anchor in
`references/source-anchors.md` instead of fetching the page. Look up framework versions, deprecations and changed
defaults when you use them (`npm view <package> version`, release notes, web fetch), because they change between anchor
checks. Do not answer those from memory.

| Question | Read |
|---|---|
| Component purity, hooks, Effects, list keys | `references/official-docs.md` §React |
| Server and Client Components, route files, environment variables | `references/official-docs.md` §Next.js |
| Strictness, narrowing, `unknown` | `references/official-docs.md` §TypeScript |
| Unit, component and end-to-end tests, screenshots | `references/official-docs.md` §Testing |
| Semantics and ARIA | `references/official-docs.md` §Accessibility, then `$design-standards` |
| A skill a playbook names is missing, or how to install it | `references/companions.md` |
| Starting a per-repo `AGENTS.md` | `references/project-agents-md-template.md` |

Guardrails when applying any reference to this repo:
- Target repos vary: App Router, Pages Router, a Vite single-page app, a monorepo. Follow the repo's choice. Do not
  propose migrating the router, the data library or the state library unless the ticket is a migration.
- React and Next.js change defaults between majors, such as caching, rendering and data fetching. State the version the
  source targets and the repo's version from `package.json`.
