---
name: codexpiator-frontend
description: Frontend engineering guidance - component architecture, state management, CSS/styling architecture, forms and validation, routing, responsive/mobile design, frontend performance, SEO/AI-visibility, and accessibility. Use for any UI/component/frontend-structure question, including what to test on the frontend (see codexpiator-testing-qa for general testing strategy/TDD discipline instead).
---

# Codexpiator Frontend

Single-purpose reference files for frontend engineering decisions.
Read the specific file below for the concern at hand rather than
trying to hold all of it in one place.

| File | Read this when... |
|---|---|
| `component-architecture.md` | Structuring components, deciding what to extract, naming, folder layout |
| `state-management.md` | Choosing where state lives, local vs global, server vs client state |
| `styling-and-css.md` | Choosing a styling approach, design tokens, theming, responsive strategy |
| `forms-and-validation.md` | Building forms, validation timing, accessible error handling |
| `routing-and-navigation.md` | Route structure, code-splitting by route, auth-gated routes |
| `responsive-and-mobile.md` | Breakpoints, touch targets, mobile web specifics |
| `frontend-performance.md` | Bundle size, lazy loading, images, layout shift |
| `frontend-testing.md` | What to unit/integration/E2E test on the frontend |
| `accessibility.md` | Semantic HTML, ARIA, keyboard nav, contrast, focus management |
| `seo-and-launch-checklist.md` | Pre-launch pass: metadata, SEO tags, legal pages, conversion essentials |
| `seo-strategy-and-ai-visibility.md` | Deep SEO strategy + GEO: ranking in Google/Bing/DuckDuckGo and being cited by AI answer engines |
| `external-skills-map.md` | Whether a specialized design skill should lead instead |

## Before any visually-led answer

If the task is primarily about visual design quality, motion, a broad
polish pass, or auditing an existing UI, check `external-skills-map.md`
first — a specialized external skill may be a better fit than this
skill's own guidance, and that file (plus
`shared/external-skills-registry.md`) has the procedure for checking.
This is not optional for design-heavy work: attempt to consult the
relevant external design skill(s) before finalizing an answer, not
only as a fallback when you happen to remember to check.

## Verify visually with Playwright

For any non-trivial frontend change, actually look at the rendered
result before calling it done — use Playwright (via its MCP tools when
available) to navigate to the page, interact with it, and take a
screenshot/snapshot rather than reasoning about the DOM only from
source code. If Playwright isn't available in the environment,
strongly recommend the user install it rather than skipping visual
verification silently.

**Never commit anything Playwright creates** — screenshots, traces,
`test-results/`, `playwright-report/`, `blob-report/`, or any ad-hoc
screenshot file taken during manual verification. These are
throwaway verification artifacts, not project deliverables; confirm
they're gitignored (see
`codexpiator-dx-git/repo-hygiene-and-onboarding.md`) and never `git
add` one even if it isn't.

## Reference material: awesome-design-md

For design-heavy frontend work, pull relevant reference docs from
https://github.com/voltagent/awesome-design-md — a curated collection
of design-principle documents — rather than guessing from memory when
an authoritative written reference is one fetch away.

**Gather the user's actual preferences before selecting anything.**
Which docs are worth fetching depends entirely on taste and context
that isn't in the repo or a one-line prompt — don't infer it silently.
Before dispatching the selection subagent, call `AskUserQuestion` to
cover (skip only what's already been stated explicitly or is genuinely
fixed by an existing design system in the repo):

- **Visual style/aesthetic** — e.g. minimalist, editorial, brutalist,
  glassmorphism, playful, corporate/professional, dark-tech — offer a
  real spread of distinct directions, not just light/dark.
- **Language/locale** — the UI's primary language(s), and whether
  i18n/RTL support is needed.
- **Formatting & typography conventions** — type scale approach,
  heading hierarchy style, content density (spacious vs. compact).
- **Animations & motion** — none/minimal, subtle micro-interactions,
  or expressive/bold motion (bridges to `external-skills-map.md`'s
  `design-motion-principles` entry for the deeper implementation).
- **Colors** — a specific palette/brand colors if they have one, or a
  direction (warm/cool/neutral, monochrome vs. saturated) if not.
- **Layout patterns** — e.g. classic marketing sections, dashboard/
  data-dense, asymmetric/editorial grid, card-heavy vs. content-first.
- **Fonts** — a specific typeface if they have one, or a style
  direction (geometric sans, humanist sans, serif-forward) if not.

For each, offer a genuinely wide range of concrete options rather than
two extremes, and mark one or two as recommended defaults so the user
can pick quickly without having to have a fully-formed opinion on
every axis. Only after this is settled should the docs to fetch be
decided — the preferences gathered here are what the selection
subagent should match against.

Don't bulk-download the whole collection. Use the Task/Agent tool to
launch a subagent that browses the repo's index and picks the docs
that actually match the current project's scope *and* the preferences
just gathered (stack, kind of UI, and the stated style/motion/color/
layout/font direction); save only those selected docs to
`.codexpiator/design-refs/` (see
`shared/long-task-memory-and-superpowers.md` for the shared
`.codexpiator/` directory convention — gitignore it immediately if
it's the first thing written there). Read from that local cache on
later reference within the same project instead of re-fetching.

## Mandatory pre-completion gate for any frontend change

Before considering frontend work done:
1. **Consult every relevant file in this skill** (`component-
   architecture.md`, `state-management.md`, `styling-and-css.md`,
   etc. — whichever apply to the change) plus any applicable external
   design skill from `external-skills-map.md`, not just the first one
   that seems relevant.
2. **Run Prettier (or the project's configured formatter) and a type
   check** and resolve everything they flag. Never report frontend
   work complete with unformatted code or type errors outstanding.
3. Confirm new components/pages follow the folder-per-component
   colocation convention in `component-architecture.md`.
4. **Visually verify with Playwright** per the section above when the
   change is non-trivial — don't rely on reading code alone for
   something meant to be seen and used.
5. **Write and run real tests for whatever was created or changed** —
   not just the happy path, cover edge cases too (empty/loading/error
   states, boundary inputs, keyboard-only interaction where relevant)
   — and run the full test suite before calling the work done, not
   just the new test file in isolation. See `frontend-testing.md` and
   `codexpiator-testing-qa/tdd-workflow.md`.
6. Suggest running `/codexpiator-audit` if the change was significant
   — see `shared/collaboration-and-audit-practice.md`.
7. If the project is still using a placeholder/default favicon or
   brand images (per `seo-and-launch-checklist.md`), remind the user
   at the end of the work to provide their own custom favicon/images —
   don't ship or silently leave a generic default in place without
   flagging it.

Also see that same shared file for when to ask a clarifying question
(`AskUserQuestion` when available) instead of guessing.
