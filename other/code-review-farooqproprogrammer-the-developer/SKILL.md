---
name: code-review
description: >
  Review code with ESLint, React Doctor, TypeScript, Prettier, npm audit, and
  CodeRabbit CLI, plus a manual correctness/security pass. Use when reviewing
  PRs, diffs, local changes, or when the user asks for a code review or to
  install CodeRabbit / React Doctor.
---

# Code review

Run **CLI scanners first**, then a short manual pass. Report findings; do not rewrite code unless the user asks. Prefer `/ponytail-review` when the ask is only over-engineering.

## Scope

1. Resolve scope: uncommitted diff, branch vs base, named files, or PR (`gh`).
2. Detect stack from the repo (`package.json`, eslint config, `tsconfig`, React deps). Skip tools that do not apply.
3. Run applicable CLIs below (agent-friendly flags). Then manual checklist.
4. Deduplicate findings across tools; rank by severity.

## CLI pipeline

Copy and track:

```
Review Progress:
- [ ] 1. Scope + stack detected
- [ ] 2. ESLint (if configured)
- [ ] 3. TypeScript check (if tsconfig)
- [ ] 4. Prettier check (if configured)
- [ ] 5. React Doctor (if React/Next)
- [ ] 6. CodeRabbit review --agent (if installed + authed)
- [ ] 7. Dependency audit (optional, when security-relevant)
- [ ] 8. Manual checklist
- [ ] 9. Report merged findings
```

Prefer project scripts when they exist (`npm run lint`, `pnpm lint`, etc.). Otherwise use the defaults below. Run from the package / workspace root that owns the change.

### 1. ESLint

```bash
npx eslint . --max-warnings 0
# narrower:
npx eslint --no-error-on-unmatched-pattern <paths...>
```

If only a script exists: `npm run lint` / `pnpm lint` / `yarn lint`. Summarize rule id, file:line, and message. Do not invent an ESLint config.

### 2. TypeScript (when `tsconfig` present)

```bash
npx tsc --noEmit -p .
```

Monorepo: use the package `tsconfig` that owns the diff.

### 3. Prettier (when config present)

```bash
npx prettier --check .
# or changed files only:
npx prettier --check <paths...>
```

### 4. React Doctor (React / Next / React Native)

Local scan (non-interactive):

```bash
npx react-doctor@latest . -y --verbose --json
```

Diff-only vs base (preferred for PR / branch review):

```bash
npx react-doctor@latest . -y --verbose --json --scope changed --base main
```

Use the repo’s real base (`main` / `master` / …). `--blocking none` when you only want a report. Categories: correctness, performance, security, accessibility, architecture, maintainability.

**Install for agents / CI** (ask first; see [INSTALL.md](INSTALL.md)):

```bash
npx react-doctor@latest install
npx react-doctor@latest ci install -y
```

Docs: https://www.react.doctor/

### 5. CodeRabbit CLI

Prefer structured agent output:

```bash
coderabbit auth status
coderabbit review --agent
# options:
coderabbit review --agent --base main
coderabbit review --agent --uncommitted
coderabbit review --agent --include-untracked
```

`cr` is an alias for `coderabbit`. If the binary is missing, follow [INSTALL.md](INSTALL.md) (Windows: `irm https://cli.coderabbit.ai/install.ps1 | iex`). Auth: `coderabbit auth login` (EU: `--region eu`). Do not paste API keys into chat or commits.

After fixes: `coderabbit review findings` / `coderabbit review findings --clear` when clearing stored findings.

Docs: https://docs.coderabbit.ai/cli

### 6. Other useful CLIs (when relevant)

| Need | Command |
| ---- | ------- |
| Dependency vulns | `npm audit --omit=dev` (or `pnpm audit` / `yarn npm audit`) |
| Next.js hints | `npx next lint` when Next is the app and no shared ESLint script |
| Secrets smell | do not run unknown secret scanners; flag obvious secrets in the diff manually |
| GitHub PR context | `gh pr view` / `gh pr diff` when reviewing a PR |

Skip tools that are not installed and would require a new dependency — except `npx react-doctor@latest` and documenting CodeRabbit install when the user asked for review tooling.

## Manual checklist

- [ ] Logic correct; edge cases and error paths handled
- [ ] No security issues (injection, authz gaps, secret leakage)
- [ ] Matches existing style and architecture
- [ ] Changes scoped; no unrelated churn
- [ ] Tests cover behavior changes (or gap called out)
- [ ] Spec Kit tasks/spec still accurate if this is feature work
- [ ] Public pages: title, description, canonical if UI routes changed

## Feedback format

Merge CLI + manual into one list:

- **Critical** — must fix before merge (incl. ESLint/tsc errors, React Doctor errors when gating, high CodeRabbit severity)
- **Suggestion** — should improve
- **Nice to have** — optional

For each finding: tool (or Manual), location, why it matters, concrete fix direction. If nothing material: say so briefly.

## Rules

- Ask before installing CodeRabbit, React Doctor agent hooks, or CI workflows.
- Never commit secrets, auth tokens, or `.env` values.
- Obey `git-branch-safety` — do not push review fixups to production branches.
- Do not fail the review solely on Prettier noise if the project does not enforce it in CI.
- Over-engineering delete-lists → `/ponytail-review` or `/ponytail-audit`.

## Additional resources

- [INSTALL.md](INSTALL.md) — CodeRabbit + React Doctor install
