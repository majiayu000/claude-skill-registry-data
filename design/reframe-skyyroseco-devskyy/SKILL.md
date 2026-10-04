---
name: reframe
description: >
  Choose or migrate the UI component framework of a project (shadcn/ui, Aceternity, Magic UI, DaisyUI, HeroUI, Chakra, Flowbite, Preline, Park, Origin, Headless UI, Cult UI) using the OpenWolf knowledge base at `.wolf/reframe-frameworks.md`. Use when the user asks to change, pick, migrate, or "reframe" their project's UI framework, or asks "which component library should we use". Do NOT use for restyling inside a framework the project already uses (that is `frontend-design` / `ui-ux-pro-max`), and do NOT use for the WordPress theme at `wordpress-theme/skyyrose-flagship/` — that surface is classic PHP + self-hosted vanilla JS and has no component framework to swap.
---

# Reframe — pick or migrate a UI framework

The knowledge base is `.wolf/reframe-frameworks.md` (25.9 KB): decision questions, a quick
selection guide, a 12-row comparison matrix, and one ready-to-adapt migration prompt per
framework under `## Framework Prompts`.

## When to use

Use when an observable one of these happens:

- The user says "reframe", "switch to shadcn", "migrate to Chakra", "which UI library",
  "pick a component library", or "redo the dashboard with <framework>".
- A new surface is being started in `frontend/` (Next.js 16 + React 19) and no component
  framework has been chosen yet.
- An existing framework is being replaced wholesale — not tweaked.

**Do NOT use when:**

- The project already uses a framework and the request is a visual change (spacing, palette,
  motion) — that is a design task, not a reframe.
- The target is `wordpress-theme/skyyrose-flagship/`. That theme is classic PHP with
  self-hosted vanilla libs in `assets/js/lib/` (`gsap.min.js`, `ScrollTrigger.min.js`,
  `lenis.min.js`, `motion.min.js`) and a zero-CDN policy. There is nothing to reframe.
- The user wants one component built. Installing a whole framework to place one button is a
  net loss; say so and build the component.

## Inputs

| Required before starting | How to confirm | If absent |
|---|---|---|
| `.wolf/reframe-frameworks.md` | `ls -la .wolf/reframe-frameworks.md` | **STOP.** Do not recommend a framework from memory — the matrix (cost, styling engine, animation weight, setup difficulty) is the whole value of this skill. Say the knowledge base is missing and stop. |
| `.wolf/anatomy.md` | `ls -la .wolf/anatomy.md` | **STOP** before writing the migration prompt. A prompt written against invented routes/components produces invented edits. |
| The user's answers to the 5 decision questions | Ask them | **STOP.** Never pick for the user on priority, Tailwind usage, theme, or app type. |
| A clean working tree in the target workspace | `git status --porcelain frontend/` | **STOP.** A framework migration touches many files; mixing it with uncommitted work makes attribution impossible. |

## Procedure

1. `ls -la .wolf/reframe-frameworks.md .wolf/anatomy.md` — both must exist.
2. Read ONLY the first ~50 lines of the knowledge base: `## Decision Questions`,
   `## Quick Selection Guide`, `## Comparison Matrix`. **Do not read the whole file** — the
   12 framework prompt sections are ~500 lines and only one of them will be used.
3. Ask the 5 decision questions in order (current stack · priority · Tailwind already? ·
   light/dark · landing vs dashboard). Stop early once the field narrows to 1–2.
4. Present one recommendation with the matrix row as the reasoning — styling engine, animation
   weight, setup difficulty, cost. Name the runner-up and why it lost.
5. Wait for the user to confirm. This is a multi-file rewrite; do not start on a guess.
6. Read only the chosen framework's `### <Name>` section, then adapt its prompt to the real
   project using `.wolf/anatomy.md` file paths, routes, and component names.
7. Execute: install deps (**npm, never pnpm** — `ERR_INVALID_THIS` on Node 22+ with Vercel),
   update config, refactor components leaf-first.
8. Run the Verification checks below before reporting anything.
9. Capture screenshots with `npx openwolf designqc` and read them — the framework swap is a
   visual change, and a type-check cannot see a broken layout.

## Verification

Run all three. The first two are the gates; the third is eyes-on and cannot be skipped silently.

1. Types still resolve after the swap:

```bash
cd /Users/theceo/DevSkyy/frontend && npm run type-check
```

**PASS:** `tsc --noEmit` exits 0 with no diagnostics. Observed on this tree 2026-07-28: exit 0.
`[repro]`

2. Lint has no NEW violations. This repo's lint is green-with-warnings, so "exits 0" alone is
   too weak a condition:

```bash
cd /Users/theceo/DevSkyy/frontend && npm run lint
```

**PASS:** `0 errors`, and the warning count does not exceed the pre-change baseline. Observed
baseline 2026-07-28: `ESLint: 0 errors, 235 warnings in 51 files`. To attribute a new warning to
your change rather than inheriting it, run the same command against a pristine tree —
`git archive HEAD frontend | tar -x -C <scratch>` then symlink `node_modules` — and diff the
*contents*, not just the error/warning counts. **Never `git stash`**: the stash stack is shared
across worktrees and you can pop another session's work. `[test]`

3. Eyes-on capture, because a framework swap breaks layout without breaking types:

```bash
npx openwolf designqc
```

**PASS:** screenshots land in `.wolf/designqc-captures/` and you have READ them. Observed:
`npx openwolf --version` resolves 2.0.1 — there is **no global `openwolf` binary** on this
machine (`command -v openwolf` → not found), so always invoke via `npx`. `[repro]`

**A gate that dies is not a gate that passed.** If `designqc` errors, the dev server is not up,
or a capture is blank, that is an artifact, not a pass — re-run by hand (bug-230).
**A SKIP is not a PASS:** if you cannot capture screenshots in this environment, say so
explicitly and name the founder as the person who closes the visual check. Silence reads as
success.

## Worked example

Verified on this tree 2026-07-28:

```bash
$ ls -la .wolf/reframe-frameworks.md
.wolf/reframe-frameworks.md  25.9K

$ grep -c '^### ' .wolf/reframe-frameworks.md
12

$ grep -n '^## ' .wolf/reframe-frameworks.md | head -5
5:## Decision Questions
15:## Quick Selection Guide
28:## Comparison Matrix
47:## Framework Prompts
```

Twelve framework prompt sections exist — shadcn/ui, Aceternity UI, Magic UI, DaisyUI, HeroUI,
Chakra UI, Flowbite, Preline UI, Park UI, Origin UI, Headless UI, Cult UI. Reading lines 1–50
gives the full decision apparatus at ~1 KB; reading the whole file costs ~25 KB of context to
use one of twelve sections. `[repo]`

For the DevSkyy dashboard specifically, the decision inputs are already known and constrain the
answer: `frontend/` runs Next.js **16.2.9** with React 19 and `cacheComponents: true`
(`frontend/next.config.ts:32`). Any framework whose components read request-time values must
sit inside a `<Suspense>` boundary or the build fails — that rules against drop-in kits that
hide `useSearchParams()` inside unwrapped internals, and favours the copy-in-source families
(shadcn/ui, Origin UI, Cult UI) where the boundary is yours to place. `[repo]`

## Failure modes

| Symptom | Root cause | Do this |
|---|---|---|
| Whole 25.9 KB knowledge base pulled into context to answer one question | Reading the file top-to-bottom instead of the first 50 lines | Read decision questions + matrix only; read the `### <Name>` section after the user chooses |
| `openwolf: command not found` | No global install on this machine (verified 2026-07-28) | `npx openwolf designqc` — never the bare binary |
| Migration edits reference routes/components that do not exist | The framework's stock prompt was pasted unadapted | Adapt against `.wolf/anatomy.md` real paths before executing; a prompt is not a plan |
| Build fails with `Uncached data was accessed outside of <Suspense>` | `cacheComponents: true` and a new component reads `useSearchParams()` / `usePathname()` / `cookies()` unwrapped | Wrap at the mount point or split shell/content — see `interactive-web-development` for both patterns |
| `ERR_INVALID_THIS` during install or Vercel deploy | pnpm on Node 22+ | Use npm. Repo rule, not a preference |
| Recommendation given before the user answered the decision questions | Skipping step 3 because the framework "seems obvious" | A reframe is a multi-file rewrite; an unconfirmed choice is unbounded rework |
| Framework swapped, types green, page visually broken | Type-check cannot see layout | Step 9 is not optional. Screenshots read, not just captured |
