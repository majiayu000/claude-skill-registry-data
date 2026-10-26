---
name: setup-project
description: Initialize a fresh clone of the Expo skeleton into a real project — interviews for product identity, then renames the app (app.config.ts + package.json), fills docs/product/vision.md, sets CODEOWNERS, stubs the data-layer ADR and env vars, optionally removes the demo feature, and verifies everything is still green. Run ONCE, immediately after creating a repo from the template.
argument-hint: [project-name-kebab-case]
disable-model-invocation: true
allowed-tools: Read Write Edit Glob Grep AskUserQuestion Bash(npm install*) Bash(npm run verify*) Bash(npm run lint*) Bash(npm test*) Bash(npx expo *) Bash(git status*) Bash(git add *) Bash(git commit *)
---

## Context

- Current package name: !`node -p "require('./package.json').name"`
- Git status: !`git status --short | head -5 || echo "no git repo"`

## Task

Turn this skeleton clone into project **$ARGUMENTS**. If the package name above is not `expo-skeleton`, this repo was already initialized — stop and confirm with the user before re-running anything.

### 1 · Interview (AskUserQuestion — don't guess any of these)

Collect in at most two rounds:

- **Identity:** project name (default `$ARGUMENTS`), one-sentence pitch, one-paragraph product description, primary user + what success looks like for them, 2–3 explicit anti-goals.
- **App identity:** display name, slug, URL scheme, iOS/Android bundle identifier base (e.g. `com.acme.app`).
- **Data layer:** none yet (keep painted-door stubs) / REST API / Supabase / Firebase / other. Plus auth: none yet / provider (note platform mandates like Sign in with Apple).
- **Demo feature:** keep `tasks` as the canonical pattern (recommended until the first real feature ships) or delete it now.
- **GitHub:** org/team handles for CODEOWNERS (replace every `@yourorg/*` placeholder).

### 2 · Apply (small, reviewable edits — preserve all formatting conventions)

1. **Rename app identity:** `app.config.ts` (`name`, `slug`, `scheme`, `ios.bundleIdentifier` / `android.package` bases — clear the `TODO(company)` markers) · `package.json` `name` · README `# title` + first paragraph (keep the rest — it documents the workflow, which doesn't change).
2. **Product memory:** rewrite `docs/product/vision.md` from the interview — remove any placeholder banner; keep the section structure. This is the file every agent grounds on; make it specific.
3. **CODEOWNERS:** replace every `@yourorg/*` placeholder in `.github/CODEOWNERS` with the real handles.
4. **Data layer & auth:** if chosen, create `docs/architecture/decisions/0007-data-layer.md` from `_template.md` (status: proposed — a human accepts it) and add the corresponding `EXPO_PUBLIC_*` variables to BOTH `.env.example` and the Zod schema in `src/shared/lib/env.ts`. Do not install or wire the dependency here — that's the first spec's job, with the ADR as its anchor.
5. **Skeleton-only files:** delete `HANDBOOK.pdf` (it documents the skeleton itself, not this project).
6. **Demo feature, if deletion was chosen:** remove `src/features/tasks/`, its route in `src/app/`, `.maestro/flows/tasks-cuj.yaml`, and any home-screen entry pointing to it; mark PRD-0001 (`docs/product/prds/0001-task-capture.md`) as removed-at-init; update the CUJ table in `docs/quality/critical-user-journeys.md` and `.maestro/flows/smoke.yaml` if it referenced tasks. ESLint `boundaries/*` guarantees nothing else imports the slice — verify with Grep anyway. Run `npm run docs:lint` after.

### 3 · Verify and hand off

- Run `npm install`, then `npm run verify`. Everything must be green — a red gate here means step 2 broke something; fix before proceeding.
- Commit as `chore: initialize project from skeleton` (one commit — reviewable as a unit).
- Report what was set, then list the steps only a human can do, with exact locations:
  1. `eas init` + set `extra.eas.projectId` and the `updates.url` in `app.config.ts`.
  2. Push and protect `main` (require the CI + E2E checks) — GitHub → Settings → Branches.
  3. Add the `CLAUDE_CODE_OAUTH_TOKEN` secret for persona reviews / agentic QA — Settings → Secrets.
  4. Invite the CODEOWNERS teams.
- Close with: the project is ready for its first feature — run `/create-spec <idea>`.
