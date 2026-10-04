---
name: documentation-sync
description: Keep project documentation in sync with code changes. Use when implementing React components, modifying hooks or GraphQL operations, changing module architecture, adding configuration, updating auth flows, or making any change that affects user-facing or developer-facing documentation. Not for building an initial documentation suite from scratch (that is the documentation-creation skill).
---

# Documentation Synchronization Skill

## Profile keys consumed

- `framework.ui`
- `framework.state`
- `framework.di`
- `framework.graphql_mock`
- `architecture.source_root`
- `architecture.modules`
- `architecture.component_prefix`
- `make.ci`
- `make.start`
- `make.lint_md`
- `make.storybook_build`
- `quality.metrics_enforced`
- `quality.mutation_msi`
- `quality.lighthouse_desktop`
- `quality.lighthouse_mobile`
- `capabilities.storybook`
- `capabilities.figma`
- `capabilities.accessibility_audit`

## Overview

This skill keeps the repository's documentation surface synchronized with
codebase changes, maintaining accuracy and completeness for both users and
developers. It treats every agent-facing guide, contributor doc, module
README, and project `SKILL.md` as part of the same change set as the code.

## Core Principle

**Documentation is part of the definition of done.** No code change is
complete until the relevant documentation is updated — in the same branch
and PR as the code.

## When to Use This Skill

- **Component / hook changes**: adding or modifying a public `framework.ui`
  component (the `architecture.component_prefix` family) or a reusable hook
- **GraphQL / mock changes**: queries, mutations, or `framework.graphql_mock`
  fixtures and the Mockoon-mocked API surface used by E2E
- **State changes**: adding or reshaping `framework.state` stores and their
  `framework.di` registrations
- **Architecture changes**: module layout, design patterns, path aliases
- **Configuration changes**: environment variables, build or i18n options
- **Security changes**: authentication and authorization flows
- **Testing changes**: new test strategies, suites, or mock infrastructure
- **Performance / accessibility changes**: optimizations, Lighthouse budgets,
  web-vitals, a11y fixes
- **Feature implementation**: new user-facing flows, routes, or copy

## Documentation Map

The table below is the conventional documentation layout for a frontend
template repository. Map each row to the target repository's actual tree;
when a file is absent, put the content in the nearest equivalent — never
create a parallel file when an existing one covers the topic.

| File | Purpose | Update when |
| --- | --- | --- |
| `CLAUDE.md` | Agent-facing project guide: stack, commands, conventions | Tooling, command, or convention changes |
| `agents.md` | Agent workflow guidance + skill catalog and triggers | Agent or skill-layout changes |
| `CONTRIBUTING.md` | Contributor workflow, CI flow, required checks | Workflow or CI changes |
| `README.md` | Project overview, setup, top-level features | Setup or high-level feature changes |
| `.claude/skills/<name>/SKILL.md` | Project skill guidance + support files | Skill behavior or layout changes |
| module `README` under `architecture.source_root` | Per-module / per-feature behavior | Feature or module changes |
| `docs/*` (when present) | Long-form developer / user docs | Topic-specific changes |
| test & workflow docs under the test root | Test strategy, mock behavior, snapshot rules | Test or mock changes |
| Storybook stories (`*.stories.*`) | Component usage and variations | Component API changes |

## Documentation Update Workflow

For each code change:

1. **Identify impact**: which docs need updates (use the map above)? Search
   for existing mentions first so you update the closest owning doc.
2. **Update content**: follow the scenario patterns below.
3. **Cross-reference**: ensure internal links remain valid; use relative
   links for files inside the repository.
4. **Validate examples**: run every command and code sample before committing.
5. **Review checklist**: complete the pre-commit checklist below.

## Update Scenarios

### Components and hooks

Applies to any reusable `framework.ui` component (the
`architecture.component_prefix` family) or shared hook whose public surface
changes. Document the component or hook name, its props or arguments (name,
type, default, required-or-not), the variants it supports, and a minimal
usage example. Update the closest owning module README under
`architecture.source_root` and add usage notes to the user-facing guide.

Component examples ship as Storybook stories: when story coverage changes,
rebuild Storybook via the target mapped by `make.storybook_build` to confirm
the stories compile. This is gated by `capabilities.storybook` — when the
capability is false or the target maps to `null`, **SKIPPED:** note that
Storybook is absent and document the example inline instead.

### GraphQL operations

Applies when `framework.graphql_mock` is set (the Apollo Server local mock
and the Mockoon-mocked API used by E2E); otherwise skip with a note. Document
each operation with a fenced `graphql` block for the query or mutation plus a
`json` block for its input variables, record any change to the mock fixtures
and the schema version they pin, and add client integration examples to the
user-facing guide. Note that E2E runs against the mock, not a live backend.

### State and stores

Update the architecture docs when adding or reshaping a `framework.state`
store: list each slice with its type and purpose, describe the actions and
selectors, and record how the store is wired into `framework.di` (the token,
the registration in the DI config, and the composition root). Render-path
state primitives that must stay container-free keep that constraint
documented. Update the developer guide with the store-and-selector usage
pattern callers should follow.

### Module and feature structure

Update the design-and-architecture section when introducing or moving a
feature module, changing the boundaries between the modules declared in
`architecture.modules`, or adding a path alias: list the new module, its
feature folders, the public surface it exports, and how it depends on the
modules around it. Always add new domain terms to the glossary — define a
term before using it anywhere else. Reference
[architecture](../architecture/SKILL.md) and
[code-organization](../code-organization/SKILL.md) for the placement rules
these docs must stay consistent with.

### Configuration

Update the advanced-configuration doc for every new environment variable:
name, type, default, required-or-not, a one-line description, a usage
example, and validation rules. Update the getting-started doc when the
variable is required for basic setup. When an i18n key or generated locale
file changes, document the regeneration step rather than hand-editing
generated output.

### Security

Update the security doc (auth flows, permission changes, security
considerations) and the per-operation auth requirements wherever the API
surface is documented. Add client auth examples to the user-facing guide.
Phrase the flow from the module the story names — never hardcode a concrete
feature path; resolve it from `architecture.source_root`.

### Testing

Update the testing doc when adding test types: command, directory, and
purpose. Cover the Jest client (jsdom) and server (node) environments,
Playwright E2E and visual suites, the Mockoon mock, and the Stryker mutation
run. Documented thresholds must come from the profile `quality.*` keys —
canonical defaults are 100% coverage across statements, branches, functions,
and lines; the mutation MSI floor read from `stryker.config.mjs` `break`
(`quality.mutation_msi`); the rust-code-analysis hard-fail policy
(`quality.metrics_enforced`, authoritative source `config/metrics-policy.json`);
and the Lighthouse performance floors (`quality.lighthouse_mobile` and
`quality.lighthouse_desktop`). Thresholds are raise-only: never document a
lowered bar. See [testing-workflow](../testing-workflow/SKILL.md) and
[frontend-testing-workflow](../frontend-testing-workflow/SKILL.md) for how
the suites run, and the `qa-visual-tester` agent for the visual + E2E gate.

### Performance and accessibility

Update the performance doc with the optimization name, measured impact
(metric: before → after), and any required configuration change. Record the
Lighthouse budget the change defends — the CI score is the one that counts,
floored by `quality.lighthouse_mobile` for mobile and
`quality.lighthouse_desktop` for desktop. Accessibility is non-negotiable:
document a11y-affecting changes (focus order, ARIA, contrast, keyboard
paths) and, when
`capabilities.accessibility_audit` is set, note the audit that signed them
off. Pair this with
[frontend-performance-accessibility](../frontend-performance-accessibility/SKILL.md)
and the `accessibility-auditor` agent; when the capability is false,
**SKIPPED:** record that no automated audit ran and flag the manual review.

### Architecture patterns

Update the patterns section when adopting or deprecating a pattern: pattern
description, implementation example, benefits and trade-offs, and a migration
path from the old pattern. Update diagrams for structural changes. When
`capabilities.figma` is set, keep the design source and any exported screens
synced in the same change (see the
[figma-design-check](../figma-design-check/SKILL.md) skill); when it is
false, **SKIPPED:** note that no design source is wired and document the
visual intent in prose.

## Documentation Quality Standards

### Consistency

- Follow the existing doc structure, heading levels, and formatting
- Use terminology from the glossary; define new terms first
- Fenced code blocks carry a language hint and blank lines around them
- Keep commands copy-pasteable and aligned with actual repository paths
- Respect the 100-character soft line limit; before presenting changes,
  disclose any changed doc line over 100 chars as `path:line` with its
  measured length (disclosure, not failure, unless `make.lint_md` fails)
- Cross-reference related sections with relative links

### Completeness

- Document all public surfaces: component and hook props, GraphQL
  operations, store actions and selectors, every error path, and a runnable
  example
- Cover error handling and edge cases, not just the happy path
- Provide both basic and advanced examples with realistic data and expected
  output

### Maintenance

- Remove outdated information; never leave stale content beside new
- Mark deprecations clearly with a migration path and removal timeline
- Update the release notes for significant changes and the versioning doc
  for version bumps and breaking changes
- Validate all internal and external links; remove dead ones
- Keep architecture, sequence, and module diagrams in sync
- Keep BMAD planning skills and frontend project skills in their separate
  directories; a skill-layout change is documented in `agents.md` and the
  affected `SKILL.md`, never mirrored across both locations
- When the formatting target's behavior changes, document that it runs both
  Prettier and `qlty fmt`
- Document only the frontend surface — never copy upstream backend-service
  instructions into the frontend docs

## Pre-Commit Checklist

- [ ] **Identify impact**: all affected docs listed
- [ ] **Update content**: scenario patterns applied
- [ ] **Cross-reference**: links verified
- [ ] **Test examples**: every sample executed (boot the dev server via the
      target mapped by `make.start` to verify component, route, and GraphQL
      examples; a `null` target means note the capability as absent)
- [ ] **Check consistency**: terminology matches the glossary
- [ ] **Rebuild stories**: when component docs changed and
      `capabilities.storybook` is set, run the target mapped by
      `make.storybook_build`
- [ ] **Lint docs**: run the target mapped by `make.lint_md`
- [ ] **Review changes**: complete, accurate, nothing stale

## Integration with Development

- **During development**: documentation is code — update docs in the same
  PR, test examples, validate links.
- **During code review**: reviewers check accuracy, example completeness,
  terminology consistency, and link validity. See
  [code-review](../code-review/SKILL.md).
- **During CI**: the target mapped by `make.ci` runs the automated doc checks
  (Markdown lint, link validation, example syntax). Fix the docs when a check
  fails — never disable the check. See
  [ci-workflow](../ci-workflow/SKILL.md).

## Success Criteria

- All affected docs updated in the same PR as the code
- Code and command examples tested and working
- Links and references valid
- Terminology consistent with the glossary
- Release notes updated for significant changes
- Docs reflect actual code behavior
</content>

</invoke>
