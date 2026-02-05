---
name: opal-frontend-repo-guidelines
description: Repository structure, build/test commands, coding style, and contribution rules for opal-frontend. Use when navigating the repo, running or debugging builds/lint/tests, following style conventions, or setting up local tooling.
---

# Opal Frontend Repo Guidelines

## Overview
Use these rules to keep work aligned with opal-frontend structure, tooling, and contribution expectations.

## ExecPlans
- When asked to create or update an ExecPlan, read `references/plans.md` in this skill and follow it exactly.

## Project Structure
- Keep Angular feature modules, shared services, and unit specs in `src/app`; colocate UI state with feature directories.
- Use `src/assets` and `src/styles.scss` for static assets and global styling; add new bundled assets to `angular.json`.
- Keep deployment and infra logic under `infrastructure/` and `charts/`; keep SSR helpers in `server.ts` and `server-setup.ts`.

## Build, Test, and Development Commands
- Run `yarn start` for `ng serve` at `http://localhost:4200/` with live reload.
- Run `yarn ng lint` for Angular ESLint across `src/**/*.ts` and `src/**/*.html`.
- Run `yarn build` for a production bundle in `dist/`.
- Run `yarn test` for Karma/Jasmine once; use `yarn test:coverage` for lcov in `coverage/`.
- Run `yarn test:a11y` for accessibility checks.

## Coding Style and Naming
- Follow `.editorconfig`: UTF-8, spaces, 2-space indent, trimmed trailing whitespace, single quotes in `.ts`.
- Follow `.prettierrc`: 120 character width, single quotes, and semicolons; run `npx prettier --write` on touched files if formatting drifts.
- Use Angular selectors with the `app` prefix (`app-example`) and order TypeScript members by visibility; keep directive selectors camelCase.

## Testing Basics
- Name Jasmine specs as `*.spec.ts` alongside sources.
- Prefer shallow `TestBed` setups and mock HTTP/Store dependencies.
- Keep major features above 80% branch coverage before merging.

## Commit and Pull Request Guidelines
- Follow Conventional Commits, optionally prefixed with Jira keys (e.g., `PO-716`); keep subjects at or below 72 characters.
- Reference the Jira ticket and linked PR (e.g., `(#1828)`) in subject or body.
- Include a concise summary, testing evidence, and updated checklists in PRs; attach Cypress artifacts when debugging flakes.

## Local Environment and Tooling
- Use Node `22.20.0` from `.nvmrc` and Yarn `4.10.3`; run `corepack enable` before `yarn install`.
- Copy baseline env configs from `config/`; prefer `.env.local` and avoid committing secrets.
- Review `sonar-project.properties` before pipeline builds.
