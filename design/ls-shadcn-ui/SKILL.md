---
name: ls-shadcn-ui
description: "Project-aware shadcn/ui guide. Use for shadcn setup, components, CLI/MCP, registry, theming, forms, Radix/Base UI, aliases, updates, and troubleshooting in React UI projects."
metadata:
  version: "1.0"
compatibility:
  notes:
    - "Includes a read-only verifier for source reachability and skill structure."
---

# shadcn/ui

Use this skill when working with shadcn/ui in React projects: setup, adding
components, choosing components, theming, forms, registry items, MCP, monorepos,
package imports, Radix vs Base UI, or updating customized local components.

## First Inspect The Project

Before recommending commands or editing UI code:

- Find the project root: `package.json`, lockfile, app framework, and nearest
  `components.json`.
- Choose the runner from `packageManager` first, then lockfiles: `pnpm dlx`,
  `npx`, `yarn dlx`, or `bunx`.
- Run the current project probe from the relevant root:

```bash
<runner> shadcn@latest info
```

Interpret the project, config, preset, components, and links from the output. If
current `shadcn info --help` confirms `--json`, you may rerun with `--json` for
structured parsing. If `config` is absent or reported as `null`, treat the repo
as not initialized and inspect framework setup before running `init`.

Use `config.aliases`, `components`, `resolvedPaths`, `project.rsc`,
`project.typescript`, `project.tailwindVersion`, `config.iconLibrary`,
`config.rtl`, `config.registries`, and the derived base (`base`, `radix`, or `aria`)
when planning code changes. Never assume `@/components/ui`.

## Decision Flow

- **New setup:** read [framework setup](./references/frameworks.md), then choose
  the exact template or manual flow.
- **Add a component:** inspect [component index](./components/index.md), run
  `docs`/`view` first for unfamiliar items, then `add`.
- **Forms:** use [form rules](./rules/forms.md) and [forms reference](./references/forms.md).
- **Theming:** use semantic tokens and [theming reference](./references/theming.md).
- **Registry or blocks:** preview with `view`, `add --view`, or `add --dry-run`;
  see [registry reference](./references/registry.md).
- **Monorepo:** map each `components.json` to its package root and pass `--cwd`.
- **Update:** use `add --dry-run`, targeted `--diff`, and manual merge; see
  [safe update procedure](./references/update-procedure.md).

## Core Guardrails

- Do not fetch raw GitHub component source manually. Prefer `shadcn docs`,
  `shadcn view`, registry JSON, or the installed project files.
- Do not overwrite customized local components without previewing the diff.
- Do not invent CLI flags. Prefer live `shadcn@latest --help` and official docs.
- Use semantic theme tokens over raw colors and variants over custom one-off
  class strings.
- Use the configured icon library; do not assume `lucide-react`.
- Respect RSC/client boundaries. Interactive components usually need a client
  boundary in Next.js App Router projects.
- Radix composition uses `asChild`; Base UI composition uses `render`. Use
  `nativeButton={false}` only when a Base UI part that defaults to native button
  behavior is rendered as a non-button element; parts with inverse/default-false
  behavior may need `nativeButton={true}` when rendered as a native button.

## Reference Map

- [Source ledger](./references/source-ledger.md)
- [CLI](./references/cli.md)
- [Project context](./references/project-context.md)
- [components.json](./references/components-json.md)
- [Frameworks](./references/frameworks.md)
- [Theming](./references/theming.md)
- [Forms](./references/forms.md)
- [Accessibility](./references/accessibility.md)
- [Registry](./references/registry.md)
- [MCP](./references/mcp.md)
- [Troubleshooting](./references/troubleshooting.md)
- [Update procedure](./references/update-procedure.md)

## Component Guides

- [Component index](./components/index.md)
- [Forms and inputs](./components/forms-inputs.md)
- [Buttons and actions](./components/buttons-actions.md)
- [Layout and navigation](./components/layout-navigation.md)
- [Overlays and menus](./components/overlays-menus.md)
- [Feedback, status, and loading](./components/feedback-status-loading.md)
- [Data display and dashboards](./components/data-display-dashboards.md)
- [Media, typography, and utilities](./components/media-typography-utilities.md)
- [Registry patterns](./components/registry-patterns.md)

## Scenario Examples

Use examples as starting checklists, not as copy-paste source:

- [Login form](./examples/login-form.md)
- [Settings page](./examples/settings-page.md)
- [Dashboard](./examples/dashboard.md)
- [Command dialog](./examples/command-dialog.md)
- [Destructive alert dialog](./examples/destructive-alert-dialog.md)
- [Responsive navigation](./examples/responsive-navigation.md)
- [Data table](./examples/data-table.md)
- [Date picker and calendar](./examples/date-picker-calendar.md)
- [Theme customization](./examples/theme-customization.md)
- [Monorepo imports](./examples/monorepo-imports.md)
- [Custom registry](./examples/custom-registry.md)
- [Safe component update](./examples/safe-component-update.md)

## Verifier

```bash
python3 ls/skills/ls-shadcn-ui/scripts/verify_shadcn_sources.py --help
python3 ls/skills/ls-shadcn-ui/scripts/verify_shadcn_sources.py
python3 ls/skills/ls-shadcn-ui/scripts/verify_shadcn_sources.py --json
python3 ls/skills/ls-shadcn-ui/scripts/verify_shadcn_sources.py --refresh --json
```

Run these repository validation commands from the LocalSetup repository root.
For an installed copy of the skill, run the equivalent `scripts/...` path from
the `ls-shadcn-ui` skill directory. The default verifier path is offline and
uses only the Python standard library to check skill structure. `--refresh`
checks official source reachability and npm latest metadata; it does not replace
manual review of syntax-sensitive current docs.
