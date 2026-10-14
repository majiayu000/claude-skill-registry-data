---
name: linting-workflow-skill
description: "Lint execution workflow — detect configs, run linters, auto-fix, resolve errors across languages. Triggers: lint, auto-fix lint. Per-language rules and configs: language-linting-skill; executor agent: linting-subagent. Gate sequence and pass semantics: verification-loop-skill."
license: Apache-2.0
compatibility: opencode
metadata:
  protocol: autoresearch-opt-in
category: Framework
---

## What I do

I provide a generic linting workflow for multiple languages:
- Detect project language and linter configuration
- Run linting and apply auto-fix when available
- Guide resolution of linting errors
- Verify fixes and commit changes

## When to use me

Use when:
- Linting code before committing or PRs
- Building workflow skills with code quality checks
- Need consistent linting across multiple languages

This is a **framework skill** - provides linting logic that other skills extend.

## Steps

### Step 1: Detect Language and Linter

**Detection**:
- `package.json` + `tsconfig.json` → TypeScript (ESLint)
- `package.json` → JavaScript (ESLint)
- `pyproject.toml` / `requirements.txt` → Python (Ruff)
- `go.mod` → Go (golint/golangci-lint)
- `Gemfile` → Ruby (RuboCop)

**Configuration files**:
- ESLint: `eslint.config.ts/js/mjs`, `.eslintrc.json/js/yaml`
- Ruff: `pyproject.toml`, `.ruff.toml`, `ruff.toml`

### Step 2: Detect Package Manager

| Language | Manager | Lock File | Command |
|----------|---------|-----------|---------|
| JS/TS | npm | `package-lock.json` | `npm run <script>` |
| JS/TS | yarn | `yarn.lock` | `yarn <script>` |
| JS/TS | pnpm | `pnpm-lock.yaml` | `pnpm run <script>` |
| Python | Poetry | `pyproject.toml` | `poetry run <script>` |
| Python | pip | `requirements.txt` | Direct command |

### Step 3: Run Linting

**Commands**:
```bash
# JavaScript/TypeScript (ESLint)
npm run lint              # npm
yarn lint                 # yarn
pnpm run lint            # pnpm
npx eslint .             # direct

# Python (Ruff)
ruff check .             # direct
poetry run ruff check .  # poetry
```

### Step 4: Apply Auto-Fix

**Auto-fix commands**:
- ESLint: `npm run lint -- --fix`
- Prettier: `npx prettier --write .`
- Ruff: `ruff check . --fix`
- Black: `black .`

**Auto-fix capabilities**:
- Style violations, unused variables, simple syntax issues
- Formatting, indentation, quotes
- Unused imports, simple refactorings

### Step 5: Fix Remaining Errors

**Error categories**:
- Syntax errors (prevents code from running)
- Style violations (code style guidelines)
- Potential bugs (risky code patterns)
- Deprecation warnings (deprecated features)
- Type errors (TypeScript type mismatches)
- Missing docstrings (public functions/classes)

**Resolution workflow**:
1. Run auto-fix first
2. Fix remaining errors incrementally
3. Re-run linting after each batch
4. Use error messages for guidance

### Step 6: Verify and Commit

**Re-run linting**:
```bash
# Re-check after manual fixes
npm run lint      # or
ruff check .
```

**Commit fixes**:
```bash
git add .
git commit -m "fix(lint): resolve linting errors"
```

## Best Practices

- Run linting before committing
- Apply auto-fix before manual fixes
- Fix errors incrementally, re-run between batches
- Don't disable rules as workaround
- Configure editor to lint on save
- Integrate into CI/CD pipelines
- Use pre-commit hooks (Husky, pre-commit)

## Common Issues

### Linter Not Found
**Install linter**:
```bash
npm install --save-dev eslint  # ESLint
pip install ruff                # Ruff
```

### Config File Missing
**Create default config**:
- ESLint: `.eslintrc.json` with `{"extends": "eslint:recommended"}`
- Ruff: `pyproject.toml` with `[tool.ruff] line-length = 88`

### Too Many Errors
- Focus on one category at a time
- Fix incrementally
- Re-run after each batch

### Auto-Fix Doesn't Work
- Some errors require manual intervention
- Review error messages
- Check if rule supports auto-fix

## Iteration Protocol (opt-in)

**DO NOT execute any of the following unless `AUTORESEARCH_PROTOCOL=1` is set in your environment.** When unset, this skill behaves exactly as documented in all sections above; the Iteration Protocol block is descriptive only.

When `AUTORESEARCH_PROTOCOL=1`:

1. **Gate check**: confirm env var is set; if unset, follow default behavior above.
2. **Auto-detection**: if this skill is invoked on a task that looks iterative (multiple cycles expected), prompt ONCE per session: "This looks iterative. Enable autoresearch protocol? (y/n)". On "y", continue; on "n", default behavior. Cache the answer for the session.
3. **5-stage loop**: cycle Understand → Hypothesize → Experiment → Evaluate → Log & Iterate. See `autoresearch-core-skill/SKILL.md`.
4. **Evaluator contract**: emit `{"pass":bool,"score":N}` JSON from a mechanical evaluator. Pass determines keep/revert; score logged to `linting-results.tsv`. See `autoresearch-core-skill/references/evaluator-contract.md`.
5. **Stuck detection**: 3 consecutive non-improving iterations → strategy pivot; 5 consecutive → paradigm shift. See `autoresearch-core-skill/references/stuck-detection.md`.
6. **Audit trail**: append every iteration to `linting-results.tsv` (8-column: iteration, commit, metric, delta, status, description, timestamp, evaluator_output). See `autoresearch-core-skill/references/audit-trail.md`.
7. **Crash recovery**: syntax errors → fix immediately (don't count); runtime → max 3 fix attempts then skip; timeout → revert + log; OOM → smaller variant. See `autoresearch-core-skill/references/crash-recovery.md`.
8. **Git-as-memory**: commit before each verify; auto-revert (`git reset --hard HEAD~1`) on `pass:false`.
9. **Iteration safety**: bounded-by-default (`Iterations: 25`); safety blocks `.env`, `node_modules/`, `rm -rf`, `git push --force`. See `autoresearch-core-skill/references/iteration-safety.md`.

### Skill-specific override

**Stuck detection + crash recovery.** 3 consecutive iterations without reducing lint-error-count → pivot to a different rule category (e.g., from `E` to `W`, or from style to type). Crash recovery: syntax errors introduced by auto-fix → revert immediately (don't count as iteration); rule conflicts → skip rule, log to `linting-results.tsv`.

### Max iterations
- Default: 25 iterations
- Hard cap: 100 (explicit `Iterations: unlimited` overrides)

