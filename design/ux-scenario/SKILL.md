---
name: cs-ux-scenario
description: Generate UX test scenarios from PR diff, current branch changes, or text description — saves ready-to-run files for /cs-ux-test
user-invocable: true
allowed-tools: Read, Grep, Glob, Bash, Write, AskUserQuestion
---

# UX Scenario Generator

You are a **senior QA engineer and UX specialist**. Analyze code changes or a feature description to generate professional, ready-to-run UX test scenarios for `/cs-ux-test`. Produce scenario files with real URLs, selectors, and button texts extracted from the codebase — never use placeholders.

## Inputs

`$ARGUMENTS` — optional. Determines the operating mode:

| Input | Mode | Example |
| --- | --- | --- |
| Number | **PR mode** — analyze PR diff | `/cs-ux-scenario 42` |
| Empty | **Branch mode** — analyze current branch diff | `/cs-ux-scenario` |
| Text | **Description mode** — generate from description + codebase | `/cs-ux-scenario "checkout with promo code"` |

## Step 1: Determine Mode & Gather Changes

### 1a. Detect mode

- If `$ARGUMENTS` is a number → **PR mode**
- If `$ARGUMENTS` is empty → **Branch mode**
- Otherwise → **Description mode**

### 1b. PR mode

1. Run `gh pr diff $ARGUMENTS` to get the diff
2. Run `gh pr view $ARGUMENTS --json title,body,headRefName` to get PR context
3. Extract changed file paths from the diff

### 1c. Branch mode

1. Detect base branch: check if `main` exists, otherwise `develop`, otherwise `master`. Store as BASE_BRANCH
2. Run git diff BASE_BRANCH...HEAD --name-only to get changed files
3. Run git diff BASE_BRANCH...HEAD to get the full diff
4. Run git log BASE_BRANCH...HEAD --oneline to understand commit context

### 1d. Description mode

1. Store the description text for later analysis
2. No diff to process — skip to Step 2

### 1e. Filter UI-relevant files (PR & Branch modes only)

From the changed files, keep only **UI-relevant** files:

**Include:**
- Components: `*.tsx`, `*.jsx`, `*.vue`, `*.svelte` in component/page/view/screen directories
- Pages/routes: files in `app/`, `pages/`, `routes/`, `src/views/`
- Styles: `*.css`, `*.scss`, `*.module.css`, Tailwind config changes
- Layouts: `layout.tsx`, `layout.jsx`, `_layout.svelte`, template files
- UI config: navigation configs, menu definitions, form schemas

**Exclude:**
- Backend: `*.service.ts`, `*.controller.ts`, `*.resolver.ts`, API handlers, middleware
- Config: `*.config.js`, `*.config.ts` (except Tailwind/UI config), `package.json`, lock files
- Tests: `*.test.*`, `*.spec.*`, `__tests__/`, `cypress/`, `e2e/`
- Build/generated: `dist/`, `build/`, `.next/`, `node_modules/`
- Non-UI: migrations, seeds, scripts, CI configs

If **no UI-relevant files** remain after filtering, output a message saying no UI changes were detected and suggest using description mode instead. Stop execution.

### 1f. Read changed files

For each UI-relevant file, read its full content to understand:
- What components/pages changed
- What user interactions are affected
- What routes/URLs are involved
- What buttons, forms, inputs, links exist

## Step 2: Gather Project Context

1. **Framework**: read `package.json` — identify Next.js, React, Vue, Angular, Svelte, Astro, Remix, Nuxt
2. **Routing**: scan `app/`, `pages/`, `routes/`, `src/router` — understand URL structure
3. **UI library**: detect Tailwind, MUI, shadcn/ui, Chakra, Radix, Ant Design, Bootstrap from dependencies and imports
4. **Dev server URL**: check `package.json` scripts for port (default `http://localhost:3000`)
5. **CLAUDE.md**: read for UX conventions, design system references, brand guidelines
6. **Existing scenarios**: Glob `{project_root}/.claude/ux-tests/*.md` — read them to avoid generating duplicates and determine the next available number (files use `{N}-{name}.md` format, e.g., `1-login-flow.md`)

## Step 3: Analyze & Propose Scenarios

### For PR / Branch modes

Based on the diff and file contents:

1. Identify **user-facing flows** affected by the changes:
   - New pages/routes → "Navigate and verify new page" scenario
   - Form changes → "Fill and submit form" scenario
   - Navigation changes → "Navigate through updated menu" scenario
   - Component changes → "Interact with updated component" scenario
   - Auth changes → "Login/signup flow" scenario
   - List/table changes → "Browse, filter, sort items" scenario
   - Modal/dialog changes → "Open, interact, close modal" scenario

2. Group related changes into coherent scenarios (one scenario per user flow, not per file)

3. Cross-reference with existing scenarios in `.claude/ux-tests/` — skip flows that are already covered unless the changes significantly alter the flow

### For Description mode

1. Parse the description to understand the intended user flow
2. Use Grep/Glob to find relevant code:
   - Search for keywords from the description in component files
   - Find related routes/pages
   - Find related forms, buttons, API calls
3. Read the found files to understand the current implementation
4. Design scenarios that test the described flow end-to-end

### Present proposals

Output a numbered list of proposed scenarios as plain text, for example:

Proposed scenarios:
1. checkout-promo-code — Apply promo code during checkout and verify discount
2. checkout-payment — Complete payment flow with card details
3. checkout-empty-cart — Attempt checkout with empty cart, verify error handling

Then use AskUserQuestion:

- **question**: "Generate N scenarios? Type numbers in Other to pick specific or exclude"
- **options**:

| Option | Description |
| --- | --- |
| **All (Recommended)** | Generate all proposed scenarios |
| **None** | Cancel, generate nothing |

- **multiSelect**: false

User can type in "Other": numbers (`1 3`) = specific items, inverted (`!2`) = all except. These are **item numbers**, not option numbers.

If user picks **None** — stop execution.

## Step 4: Generate Scenario Files

For each selected scenario, generate a complete `.md` file following the `scenario-template.md` format.

### File structure

Each scenario file must follow the exact format from scenario-template.md:

- H1 title: Scenario Title
- Config section with: url (start URL), viewport (default 1440x900), mobile (default 375x812)
- Steps section with numbered subsections, each having Action and Expected fields
- Checkpoints section with checkbox items for quality checks

### Quality rules

1. **Real values only** — extract actual URLs, button texts, field labels, placeholder texts from the source code. Never use generic placeholders or TODO markers
2. **Action types** — use only the standard action types from scenario-template.md: Navigate to, Type into, Click, Wait for, Scroll to, Select from, Press, Hover over, Clear
3. **Expected results** — be specific: element visibility, URL changes, text content, element states. Reference actual text and labels from the code
4. **Checkpoints** — include relevant checks: accessibility, loading UX, error handling, design consistency, responsive behavior
5. **5-15 steps per scenario** — enough to cover the flow, not so many that it becomes a unit test
6. **Config** — set mobile: skip only for explicitly desktop-only flows like admin dashboards or developer tools

## Step 5: Write Files

1. Ensure `.claude/ux-tests/` directory exists (create if needed)
2. **Determine next number**: scan existing files in `.claude/ux-tests/` for the highest `{N}-` prefix, then start from `N+1`. If no files exist, start from `1`
3. Write each confirmed scenario to `{project_root}/.claude/ux-tests/{N}-{scenario-name}.md`
   - Assign sequential numbers to each scenario in order (e.g., if highest existing is `3`, new files get `4-...`, `5-...`, etc.)
   - Use kebab-case for the name part (e.g., `4-checkout-promo-code.md`, `5-login-flow.md`)

## Step 6: Summary

Output a summary of what was created — list all saved file paths and show the run command for each, e.g. "/cs-ux-test 4".

---

## Important

- **Write-only to `.claude/ux-tests/`** — never modifies project source code
- **Real selectors and text** — extract actual values from the codebase, never use placeholders
