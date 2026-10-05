---
name: app-builder
description: Build, deploy, and iterate on web projects using Nick's full stack and design system. Enforces enterprise-grade quality and Nick's visual standards on every build.
metadata:
  openclaw:
    requires: {}
---

<!-- CHANGELOG
2026-03-19 — Fix 3: Added competitor/aspiration screenshots as mandatory spec inputs. Builds must include visual benchmarks, not just design tokens.
-->

# App Builder

## When to Use
When Nick asks to build an app, website, or web project. Called by `nick-project-orchestrator` after design and schema steps are complete.

## Workflow

### Step 0 — Name the Project
Generate a kebab-case name from the description. All projects go in ~/Projects/. Never ask the user for a folder name.

### Step 1 — Confirm Upstream Work Is Done
Before building, verify these inputs exist (from the orchestrator):
- ✅ Stitch design output (screens generated, Stitch chat ID saved)
- ✅ Stitch full-res screenshots downloaded to /tmp/stitch-<project>-<screen>.png
- ✅ Competitor screenshots (/tmp/competitor-<project>-desktop.png, /tmp/competitor-<project>-mobile.png)
- ✅ Aspiration screenshot (/tmp/aspiration-<project>.png)
- ✅ Project-specific design brief (50-100 words — accent color + reason, 2 reference sites, hero treatment, one thing to nail, one thing to avoid)
- ✅ nick-design-director direction (trust signals, conversion moments, interface decisions)
- ✅ nick-design-system anti-pattern check (loaded for validation, NOT copy-pasted into spec)
- ✅ nick-schema-designer output (tables, RLS policies, TypeScript types)

If any are missing and this isn't a quick build — stop and generate them first.

### Step 2 — Plan
Create a brief project plan:
- App name and description
- Key features
- Tech stack (Next.js App Router + Tailwind CSS + Supabase + Vercel unless told otherwise)
- Chosen brand accent color and why
- Page structure / key sections
- DB schema summary (key tables from schema-designer)
- File structure overview

Share with Nick for approval before building.

### Step 3 — Build
Once approved:
1. `mkdir -p ~/Projects/<name>`
2. Launch Claude Code with the COMPLETE spec:

```bash
cd ~/Projects/<name> && claude --permission-mode bypassPermissions --print -p "FULL SPEC HERE"
```

The spec MUST include:
- Every feature in detail
- Design-director interface direction (trust, conversion, activation)
- **Stitch screenshots passed inline via `--image` flags** (pixel-match target, not just tokens)
- **Competitor + aspiration screenshots passed inline via `--image` flags** with instruction:
  "Match or exceed the competitor's visual density and polish. Take design inspiration from
  the aspirational reference. Do not produce anything that looks like a template."
- **Project-specific design brief** (the 50-100 word brief, NOT the full design-system rulebook)
- Pixel-match instructions: "The attached Stitch screenshots are the exact visual target.
  Do NOT use default shadcn/ui styling. Style from scratch to match the visual."
- Complete DB schema (tables, columns, types, RLS policies from nick-schema-designer)
- Supabase patterns (from nick-supabase-reference — client/server setup, auth flow)
- Fullstack standards (from nick-fullstack — error handling, security, SEO, accessibility)
- Responsive breakpoints and rules
- Anti-patterns list (from nick-design-system — what NOT to do)

The Claude Code invocation should use `--image` for all visual references:
```bash
cd ~/Projects/<name> && claude \
  --permission-mode bypassPermissions \
  --print \
  --image /tmp/stitch-<project>-hero.png \
  --image /tmp/stitch-<project>-dashboard.png \
  --image /tmp/competitor-<project>-desktop.png \
  --image /tmp/aspiration-<project>.png \
  -p "FULL SPEC HERE"
```

Never give Claude Code vague instructions. The spec should be 800+ words minimum.

### Step 4 — Deploy
ALWAYS deploy immediately after building without asking:
```bash
cd ~/Projects/<name> && vercel --yes --prod
```
Share the live URL.

### Step 5 — Post-Deploy QA
Run all 3 QA steps (handled by orchestrator):
1. vercel-qa → codebase-aware functional testing
2. nick-visual-design-review → design + conversion QA
3. nick-deep-uat → click every button, every form, every link

### Step 6 — Iterate
For any changes, re-pass all visual references so design quality holds:
```bash
cd ~/Projects/<name> && claude \
  --permission-mode bypassPermissions \
  --print \
  --image /tmp/stitch-<project>-hero.png \
  --image /tmp/stitch-<project>-dashboard.png \
  --image /tmp/competitor-<project>-desktop.png \
  --image /tmp/aspiration-<project>.png \
  -p "CHANGE REQUEST + design brief + fullstack standards"
```
ALWAYS redeploy after changes. Run all 3 QA steps. Share the updated live URL.

**If Stitch screenshots no longer exist** (old project): re-run the visual review skill to capture current screenshots, then use those as the --image references. Design quality must be maintained across every iteration, not just the first build.

## Rules
- Always auto-generate folder name — never ask
- Always put projects in ~/Projects/
- Always deploy after building — never ask
- Always redeploy after changes
- Always share the live URL
- Claude Code flag: `--permission-mode bypassPermissions --print` — NEVER `--dangerously-skip-permissions`
- Always include: design-director direction + Stitch output + design system + schema + fullstack in every spec
- Spec minimum: 800+ words. Vague specs produce mediocre output.
- Every project must pass all 3 QA steps before reporting to Nick
- Schema is always designed BEFORE code — never let Claude Code invent the DB structure
