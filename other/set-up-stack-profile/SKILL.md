---
name: set-up-stack-profile
description: Use when starting in a repo with no .claude/stack-profile.md, when the stack changed, or when the user asks which plugins and skills to use. Detects the stack, asks only the gaps, writes the profile, and lists plugins and skill order.
---

# Set Up Stack Profile

Writes `.claude/stack-profile.md`, the file every other skill reads first. Schema and precedence: [stack-profile.md](../_shared/stack-profile.md). Question wording and plugin map: [wizard-reference.md](wizard-reference.md).

## 1. Audit (change nothing)

```bash
cat .claude/stack-profile.md 2>/dev/null; cat ~/.claude/stack-profile.md 2>/dev/null
ls -a | head -50
ls pnpm-lock.yaml package-lock.json bun.lock bun.lockb yarn.lock uv.lock go.mod Cargo.toml pyproject.toml mise.toml .tool-versions .nvmrc justfile Makefile vercel.json supabase/config.toml drizzle.config.* sqlc.yaml biome.json* .golangci.y*ml 2>/dev/null
ls .github/workflows .gitlab-ci.yml 2>/dev/null; ls *.tf infra 2>/dev/null | head
grep -hE '"(react|vue|nuxt|next|hono|drizzle-orm|zod|@opentelemetry/[a-z-]+|@sentry/[a-z]+|@anthropic-ai/sdk|openai)"' package.json 2>/dev/null
```

Apply the detection table in [stack-profile.md](../_shared/stack-profile.md) to the results. Result: a draft profile with each key marked **detected** (with the file as evidence), **inherited** (from `~/.claude`) or **gap**.

## 2. Decide

| State | Action |
|---|---|
| No project profile | Full run: steps 3–7. |
| Profile exists, nothing changed | Print "already in place" with the profile and stop. |
| Profile exists, detection differs or keys are missing | **Delta run**: show the diff (key: old → detected), ask only about changed and unknown keys. |
| `profile_version` older than the schema | Migrate, show the diff, confirm. |

Never ask what the repo already answers. A detected value is shown for confirmation in the final summary, not asked as a question.

## 3. Ask only the gaps

Use `AskUserQuestion`, at most **4 questions per round**, the recommended option first and labelled `(Recommended)`. Round order: (1) language and framework gaps, (2) backend, database, hosting, (3) tooling (package manager, lint/format, task runner, tests, CI), (4) observability, AI. Skip a round when it has no gaps. Skip questions the answer of an earlier round made moot (no `backend` question for `frontend`-only static sites unless the user said otherwise).

Recommended options come from the Adopt rows in [tech-radar.md](../_shared/tech-radar.md). Before recommending a version-sensitive tool, check the live version per [version-protocol.md](../_shared/version-protocol.md). A deviation the user picks goes into the profile's notes with the reason.

Stop at three rounds if the user answers "defaults": fill the rest from the radar and say so.

## 4. Write the profile

- Write `.claude/stack-profile.md` (create `.claude/`). Frontmatter exactly per the schema; notes below list deviations and why.
- Keys the user marked `none` are written as `none`; undecided keys are omitted.
- Show the final file and the diff against the old one.
- **Offer** (do not do unasked) a user-wide default: `~/.claude/stack-profile.md` holding only taste keys (`package_manager`, `runtime_manager`, `lint_format`, `tests`, `task_runner`, `ci`, `observability`). Never copy project-specific keys (`frontend`, `database`, `hosting`) into it.
- Suggest adding `.claude/stack-profile.md` to version control: it is team knowledge, not a secret.

## 5. Output: plugins to enable

Marketplace name is `ai-development-skills`; install id is `<plugin>@ai-development-skills`. Map profile → plugins with the table in [wizard-reference.md](wizard-reference.md). Always `devcore`. Print the exact commands:

```
/plugin marketplace add VelimirMueller/ai-development-skills
/plugin install devcore@ai-development-skills
/plugin install <other>@ai-development-skills
```

Plugins already enabled (`/plugin` lists them) are not repeated. Each plugin depends on `devcore`, so installing any of them installs it too.

## 6. Output: ordered skills to run

Print a numbered list, only skills that apply and whose result is not already in place. Order template and rules: [wizard-reference.md](wizard-reference.md). Typical start: `validate-env` → lint/format → TypeScript → tests → CI → security headers → logging/observability → feature skills.

## 7. Output: gaps no skill covers

For each profile choice with no matching skill in an installed or listed plugin (an unusual framework, a hosting provider not in the schema, `other:<x>` values), list it and offer `extend-skillset`. Do not run it unasked.

## 8. Verify

```bash
head -30 .claude/stack-profile.md
```

Expected: starts with `---`, has `profile_version: 1`, parses as YAML, every value is in the schema's allowed list (or `other:<name>`). A second run of this skill prints "already in place".

## Edge cases

- Monorepo: ask once whether to write one root profile or one per package; nearest profile wins.
- Conflicting evidence (two lockfiles): treat as a gap; ask which is canonical and suggest deleting the other.
- No `.git`: still write the profile; mention that it is untracked.
