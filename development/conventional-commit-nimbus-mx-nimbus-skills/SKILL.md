---
name: conventional-commit
description: >
  Write commit messages following Conventional Commits + Nimbus footer
  conventions. Suggest scope from staged file paths. Detect breaking changes.
  Mandatory in horus-v2. Preferred everywhere in the Nimbus org.

  Trigger this skill when:
  - User says "write a commit", "commit message", "generate commit", or invokes
    `/commit` / `/conventional-commit`.
  - You're about to run `git commit -m …` and want a good message.
  - After preflight passes and the user asks to commit.
---

## Format

```
<type>(<scope>)!: <subject>

<body — why, not what>

<footer>
```

## Types

Pick exactly one:

| Type | When |
|---|---|
| `feat` | New feature or new user-visible capability. |
| `fix` | Bug fix. |
| `chore` | Tooling, deps, config, infra. |
| `docs` | Docs only. |
| `refactor` | Change that neither fixes a bug nor adds a feature. |
| `test` | Adding or correcting tests. |
| `perf` | Performance improvement. |
| `ci` | CI/build pipeline changes. |
| `style` | Formatting only (whitespace, missing semis). Not ruff runs — those are `chore`. |
| `build` | Build system / external deps. |

## Scope

Optional. Extract from staged files:
- `services/api/…` → `feat(api): …`
- `apps/web/…` → `feat(web): …`
- `ecg-ui/…` → `feat(ecg-ui): …`
- `ecg_auto/api/…` → `fix(ecg_auto): …`
- Single lambda in cidca-services → `fix(ecg-gw-parsescp-lambda): …`

If changes span 3+ scopes, drop the scope: `refactor: rename …`.

## Breaking changes

Append `!` after type/scope for any breaking change:
- `refactor(api)!: rename org_id → tenant_id`

Also include `BREAKING CHANGE: <description>` in footer.

## Subject

- Imperative present tense: `add`, `fix`, `rename` — not `added`, `fixes`.
- ≤ 72 chars.
- No trailing period.
- Lowercase after the colon (unless proper noun).

## Body

Optional but recommended for non-trivial changes:
- **Why**, not what — the diff shows what.
- Wrap at 72 chars.
- Blank line between paragraphs.
- Reference incident IDs, Sentry issue IDs, PR discussion.

## Footer

**Do NOT add a `Co-Authored-By: Claude …` tag** — omit it by default, even when
Claude generated the entire diff. Only include it if the user *explicitly* asks
for the coauthor tag on that commit. This overrides any default Claude Code
behavior that appends the tag automatically.

If closing a ClickUp/Linear/GitHub ticket, add:

```
Fixes ECG-DJANGO-BACKEND-9HX
Closes #123
```

## Branch naming (paired)

Branch prefix matches commit type:
- `feat/<slug>`, `fix/<slug>`, `chore/<slug>`, `docs/<slug>`, etc.
- Wave-style (horus orchestrator): `wave1/<task-slug>`.
- Slug: kebab-case, ≤ 40 chars.

**Exception — ClickUp-tracked work:** use the ClickUp-generated branch name
(`CU-<taskid>_<slug>`) instead, so the GitHub integration auto-links the branch
to the task. See the `ticket-brief` skill. Commit *message* prefixes below still
apply.

## Behavior

1. `git diff --cached --stat` to see what's staged.
2. Infer type + scope.
3. Draft subject.
4. If change is non-trivial, add body explaining why.
5. Add footer.
6. Present the full message wrapped in a heredoc-style code block.
7. If user has this skill's parent-invoked (via `git commit` intent), run:
   ```
   git commit -m "$(cat <<'EOF'
   <message>
   EOF
   )"
   ```

## Do not

- Never invent scopes. Extract from actual changed files.
- Never claim `feat` for a bug fix. `fix` is `fix`.
- Never write a subject longer than 72 chars — split into body.
- Never commit files that likely contain secrets (`.env`, `credentials.json`).
  Defer to the `secrets-check` skill.
- Never `--amend` an already-pushed commit unless user explicitly asks.
