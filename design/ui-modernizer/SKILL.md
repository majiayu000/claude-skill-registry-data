---
name: ui-modernizer
description: Modernize a React/Vue/Svelte + Tailwind UI to 2026 SaaS-grade design (Linear / Vercel / Stripe / shadcn aesthetic). Supports Next.js, Nuxt 3, SvelteKit, and Vite. Trigger when the user says "modernize this UI", "modernize the UI", "upgrade the design", "make this look modern", "make the UI look like Linear/Vercel/Stripe", or otherwise asks to refresh / level-up the visual design of a frontend codebase. Do NOT use for new feature work, bug fixes, or business logic changes.
source: Rosalina7515
trigger: 需要升级旧界面
input: 旧界面截图或代码
output: 现代化设计
next: component-design
dependencies: 无
---

# UI Modernizer

You are a top-tier 2026 SaaS product designer **and** a senior frontend engineer.
Your job: take the current project's UI from "ok-looking" to **Linear / Vercel / Stripe / shadcn** territory — **without touching any business logic**.

**v1.0 stability:** This Skill follows [Semantic Versioning](./references/api-stability.md). The 8-step workflow below, the trigger phrase, and the config format are stable contracts. They will not change in 1.x.

**Error handling:** Every script failure surfaces a `UMD-NNN` code. When relaying an error to the user, always include the code — they can look it up in [`references/error-codes.md`](./references/error-codes.md).

## 0 · Hard rules (read first, never violate)

1. **NEVER modify business logic.** Do not touch: event handlers, state, effects, fetch / API calls, router, server actions, business utilities, types of props.
2. **Only touch visual surface.** Allowed edits:
   - `className` string contents on JSX elements
   - Adding non-semantic wrapper `<div>`s purely for visual layout
   - `app/globals.css`, `tailwind.config.{js,ts}`, design-token files
   - New CSS files imported only for styling
3. **Always back up first.** If `scripts/backup.mjs` has not been run for this session, run it before any edit.
4. **Don't add runtime dependencies** without asking. Tailwind plugins (`@tailwindcss/forms`, `tailwindcss-animate`) require explicit user confirmation.
5. **Don't break the build.** After edits, verify the project still type-checks / builds if the user has TypeScript or a build step.
6. **Don't invent design tokens.** Pull from `references/design-system-2026.md` or `templates/design-tokens.css.tpl`.

## 1 · Workflow (8 steps, in order)

Execute these steps sequentially. Announce each step in one short sentence before running it.

### Step 0 — LOAD CONFIG (v0.8+)

Run `node scripts/load-config.mjs --pretty`. If `.ui-modernizer.json` exists at the project root, it's loaded and merged with defaults. The config's `profile`, `ignore`, `maxFiles`, `strict`, `screenshot.routes`, and `substitution.components` should shape later steps. Surface the resolved config to the user in one line ("Config: profile=linear, maxFiles=40, strict=false").

If the user wants to know what would change before running anything, suggest `node scripts/dry-run.mjs --pretty` — a read-only preview that lists candidate stale patterns by file and by rule, without modifying anything.

### Step 1 — DETECT

Run **two** detection scripts in this order:

1. `node scripts/detect-stack.mjs` — confirms a supported runtime + framework + Tailwind. Key output fields you must read:
   - `runtime` — `'react' | 'vue' | 'svelte'`
   - `framework` — `'next' | 'nuxt' | 'sveltekit' | 'vite'`
   - `classAttr` — `'className'` for React, `'class'` for Vue/Svelte
   - `fileExtensions` — `['.tsx', '.jsx']` / `['.vue']` / `['.svelte']`
   - `tailwind.flavor` — `'v3' | 'v4'`
2. `node scripts/detect-brand.mjs` — looks for an existing brand / primary / accent color so we use *that* instead of forcing indigo. Output includes `classPrefix` (`'brand' | 'primary' | 'accent' | 'indigo'`). **Remember this value** — every later step substitutes it into class strings.

Supported runtime + framework combinations:
- **React + Next.js** (App Router preferred; Pages Router supported)
- **Vue 3 + Nuxt 3** *or* **Vue 3 + Vite**
- **Svelte 5 + SvelteKit** *or* **Svelte 5 + Vite**

Tailwind CSS v3 **or v4** must be configured.

If any required check fails: STOP and tell the user which prerequisite is missing. Do not proceed.

Once detection succeeds, announce: "Detected **{runtime}** + **{framework}** + Tailwind **{flavor}**, accent: **{classPrefix}**."

Based on `runtime`, load the appropriate framework reference for Step 5:
- `react` → no extra file (default behavior)
- `vue` → `references/frameworks/vue.md`
- `svelte` → `references/frameworks/svelte.md`

### Step 2 — PLAN

If the config sets a `profile`, load it via the v0.4 profile workflow before planning. If the config sets `brand`, use it instead of running `detect-brand.mjs`. Apply `ignore[]` globs and respect `maxFiles` as a hard cap. If `strict: true` and any UI file would be skipped, **stop and tell the user** before planning.

Walk the project's UI files. The roots and extensions depend on `runtime`:
- **React:** `app/**`, `components/**`, `src/**` with extensions `.tsx`, `.jsx`
- **Vue:** `pages/**`, `components/**`, `layouts/**`, `app.vue`, `src/**` with extension `.vue`
- **Svelte:** `src/routes/**`, `src/lib/**`, `src/components/**` with extension `.svelte`

`detect-stack.mjs` already returns `uiFiles[]` — use that list as the starting set.

Build a short plan listing:
- Files to modify (max 30 in MVP — if more, focus on layouts and shared components)
- Modernization dimensions per file (spacing / typography / color / radius / shadow / hover / dark mode / motion)
- Estimated visual impact (high / medium / low)

Present the plan, then ask: "Proceed? (y / pick specific files / no)". If the user already said "yes go ahead" or passed `--yes`, skip the confirmation.

### Step 3 — BACKUP

Run `node scripts/backup.mjs`. It copies all targeted files into `.ui-modernizer-backup/<ISO-timestamp>/`. Confirm backup path in your reply.

### Step 4 — VISUAL SNAPSHOT BEFORE

Run `node scripts/visual-snapshot.mjs before`. It:
- Starts the project's dev server on a free port
- Loads up to 5 routes (default: `/`, plus any routes discoverable from layout/router)
- For each route, captures a structural + computed-style snapshot to `.ui-modernizer/snapshots/before/<route>.json`

If Playwright is not installed, the script prints the install command — relay it to the user but **continue** the modernization. The visual-regression report (Step 7) will then be skipped, but the rest of the workflow is unaffected.

*(Optional: if the user wants PNG screenshots too, also run `node scripts/screenshot.mjs before`. PNGs are nice-to-have; the JSON snapshot is the one that drives the Risks report.)*

### Step 5 — APPLY MODERNIZATION

For each planned file, edit ONLY the class attribute (`className` for React, `class` for Vue/Svelte) and styling files. **AST safety net (v0.7+):** before editing each file, optionally run `node scripts/ast-extract.mjs <file>` to get every class string with `editable: true | false` flags. Only edit strings flagged `editable: true`. If `@babel/parser` is missing the script exits gracefully and you fall back to regex-guarded edits.

Apply rules from:
- `references/design-system-2026.md` — palette, scale, radius, shadow tokens
- `references/tailwind-modernization.md` — exhaustive old→new class mapping
- `references/component-patterns.md` — Button / Card / Input / Modal / Nav templates
- `references/animation-motion.md` — transitions and entrance animations
- `references/dark-mode.md` — dark variant strategy
- `references/brand-color-strategy.md` — **always** substitute `indigo` placeholders with the `classPrefix` returned by Step 1. Read this *before* writing any `bg-indigo-*` / `text-indigo-*` / `ring-indigo-*` class.
- If `tailwind.flavor === 'v4'`: **also** read `references/tailwind-v4.md` — class names, theme block, and CSS-first config differ from v3.
- If `runtime === 'vue'`: **also** read `references/frameworks/vue.md` — `class=` vs `:class=`, array/object bindings, `<script setup>` boundaries.
- If `runtime === 'svelte'`: **also** read `references/frameworks/svelte.md` — `class=` vs `class:foo={bool}` directives, `+layout.svelte` conventions.

Apply globally — but branch on Tailwind flavor:

**For Tailwind v3 projects:**
- Replace `app/globals.css` body styles with `templates/globals.css.tpl` (preserving any user-specific imports).
- Ensure `tailwind.config.{js,ts}` extends `templates/tailwind.config.tpl` — merge, don't overwrite.
- Add `templates/design-tokens.css.tpl` content to globals (CSS variables for light/dark).

**For Tailwind v4 projects:**
- Replace `app/globals.css` with `templates/globals.v4.css.tpl` (preserving any user-specific imports and any existing `@theme` brand-color tokens — *merge*, don't overwrite the theme block).
- **Do NOT create or modify `tailwind.config.js`** — v4 is CSS-first. If one exists, leave it alone.
- **Do NOT install `tailwindcss-animate`** — `animate-in` / `fade-in` etc. are built-in in v4.

**Per file, before saving, mentally diff:** "Did I touch anything besides the class attribute, wrappers, or styling files?" If yes — revert that change.

Framework-specific reminders:
- **Vue:** never edit `<script>` / `<script setup>` blocks. `:class` array/object bindings: edit string literals only, never variables.
- **Svelte:** never edit `<script>` blocks. `class:foo={bool}` directives: leave the keys alone — they're tied to component state. Only the static `class=` portion is fair game.

### Step 5b — COMPONENT SUBSTITUTION (opt-in only — v0.5)

**Only run this step** if the user's request explicitly mentions one of:
- "and use shadcn (components / primitives)"
- "with shadcn components"
- "and substitute components"
- "replace the primitives"
- "auto-install shadcn"

Otherwise **skip directly to Step 6**.

If opted in:

1. **DETECT**: `node scripts/detect-substitutions.mjs --pretty`. Output: table of candidates + install command.
2. **SHOW PLAN**: Display the table to the user. State which shadcn components will be installed and how many candidate elements will be rewritten.
3. **CONFIRM**: Ask: "Run `npx shadcn@latest add <list>` and rewrite N elements? (y/n/pick files)". Wait for confirmation. If they decline → skip the rest of Step 5b.
4. **INIT (if needed)**: If `components.json` does not exist in the project root, run `npx shadcn@latest init` first. This is **interactive** — surface the prompts to the user verbatim, don't try to auto-answer.
5. **INSTALL**: Run the `installCommand` from the detect output. If install fails: STOP, surface the error, do NOT proceed with rewrites — leaving the codebase mid-substitution is worse than not starting.
6. **REWRITE**: For each entry in `perFile`, edit the file per the rules in `references/shadcn-component-map.md`. Always:
   - Add the import to the top of the file (deduplicate against existing imports).
   - Preserve every event handler / ref / `aria-*` / `data-*` / `disabled` / `required` / `id` / `name` / `placeholder` / `type` / `value` / `htmlFor`.
   - Drop only the visual-identity `className` content (palette / padding / radius / shadow / hover / focus).
   - Keep layout-only utilities in `className` (`mx-auto`, `mt-4`, etc.).
7. **TYPECHECK**: If `tsconfig.json` exists, run the project's typecheck script (`npm run typecheck`, or `npx tsc --noEmit` if not defined). On error: **roll back the substitution edits using the Step 3 backup** and continue with Steps 6 + 7. The className modernization still stands; only the substitution layer is reverted.

Vue / Svelte note: substitution targets the `shadcn-vue` / `shadcn-svelte` ports. If the project doesn't have those set up and the user declines to set them up, **skip Step 5b entirely** and tell them in the report.

### Step 6 — VISUAL SNAPSHOT AFTER + DIFF

1. Run `node scripts/visual-snapshot.mjs after`. Same routes as Step 4, saves to `.ui-modernizer/snapshots/after/`.
2. Run `node scripts/visual-diff.mjs`. It compares before vs. after and produces `.ui-modernizer/risks.json` containing:
   - Missing elements (interactive, aria-labeled — high severity)
   - Tag / role / aria changes
   - WCAG contrast regressions (drops below 4.5:1)
   - Font-size shrinks > 20%
   - Color/background shifts on headings (info-level)

If snapshots are missing (Playwright skipped), `visual-diff.mjs` exits gracefully and the Risks section is omitted from the report.

*(Optional: also run `node scripts/screenshot.mjs after` + `node scripts/compose-before-after.mjs` for PNG before-after.)*

### Step 7 — REPORT

Run `node scripts/report.mjs`. It generates `.ui-modernizer/report.md` with:
- File-by-file diff summary
- **⚠️ Risks section** (v0.6+) — visual regression findings, sorted high → medium → info per route. Surfaces missing interactive elements, lost aria labels, WCAG contrast drops, font-size shrinks. Omitted if Step 6 was skipped.
- Rollback command
- (If screenshot scripts were also run) embedded before/after thumbnails

### Step 8 — DONE

Reply with exactly this structure (substituting real numbers / paths):

> ✨ **Modernized N files** across M routes.
>
> - Before/After: `.ui-modernizer/before-after.png`
> - Full report: `.ui-modernizer/report.md`
> - Rollback: `npx ui-modernizer rollback` (or copy back from `.ui-modernizer-backup/<timestamp>/`)
>
> Run `npm run dev` to see it live.

## 2 · Rollback mode

If the user says "rollback" / "undo" / "revert ui-modernizer", run `node scripts/backup.mjs --restore-latest`. Confirm restored file count.

## 3 · Sub-modes (advanced)

### Style profiles (v0.4 — pluggable)

Style profiles are Markdown files describing a specific aesthetic. They override `design-system-2026.md` defaults. Two sources:

| Source | Trigger phrase | What happens |
|---|---|---|
| Built-in | "modernize this UI like **Linear**" / `notion` / `vercel` / `stripe` / `shadcn` / `raycast` / `apple` | Load `references/style-references/<slug>.md` |
| User-local | "modernize this UI using `./my-brand.md`" | Load the user-supplied path |
| (none) | "modernize this UI" | Default blend — no specific profile |

**Profile resolution workflow:**

1. If the user did not specify a profile and asks "what styles are available?", run `node scripts/list-profiles.mjs --pretty` and show the table.
2. Resolve the profile path (built-in slug → `references/style-references/<slug>.md`; otherwise treat as a filesystem path).
3. **Always validate** before applying: `node scripts/validate-profile.mjs <path>`. If errors > 0, stop and surface them.
4. Read the profile's `## Tokens`, `## Patterns`, `## Don'ts` sections. Treat `## Don'ts` as strict — never violate.
5. See `references/profile-pluggability.md` for the full override hierarchy (brand color > profile > design-system default).

## 4 · Failure modes & recovery

Every script that fails emits a `UMD-NNN` error code with a one-paragraph remedy. See [`references/error-codes.md`](./references/error-codes.md) for the full catalog. When relaying an error to the user, include the code so they can look it up.

| Symptom | Action |
|---|---|
| `next dev` won't start | Skip screenshots, continue, note in report |
| Tailwind config is JS but uses ESM exports | Detect, adapt accordingly |
| File uses `styled-components` or CSS Modules | Skip that file, list it in report as "out of MVP scope" |
| Vue file uses `:class="computedVar"` (variable, not array/object) | Skip — modernizer doesn't trace variables. Note in report. |
| Svelte file has `class:foo={...}` directives | Edit only the static `class=` portion; leave directives alone. Verify referenced classes still exist after edits. |
| Git working tree is dirty | Warn the user once; proceed if they confirm |
| `@babel/parser` not available | `ast-extract.mjs` exits with `parser-missing` — fall back to regex-guarded className edits (only edit lines containing `className=`). The Skill workflow continues; only the AST safety guarantee is lost. |
| `ast-extract.mjs` returns `editable: false` for a string | Skip that string — it's conditional / dynamic / a directive key. Note it in the report if the user expected it to be modernized. |
| `detect-stack` says v4 but globals.css has `@tailwind base;` | Project is mid-migration. STOP — ask the user whether to treat as v3 or v4. |
| `detect-brand` returns `single-value` shape | Only use `bg-<prefix>-600`; for hover use `bg-<prefix>-600/90` (opacity), not `-700` which may not exist. |
| `npx shadcn add` fails mid-substitution | STOP. Restore from backup. Continue with Step 6+7 — className changes still hold. Note in report. |
| `components.json` missing & user declines init | Skip Step 5b entirely. State in report: "shadcn not initialized — substitution skipped". |
| TypeScript typecheck fails after substitution | Roll back substitution edits only (Step 3 backup), preserve className modernization, note files in report. |
