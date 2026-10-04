---
model_tier: medium
name: copilot-config
description: "Tune the GitHub Copilot AI — `copilot-instructions.md`, PR-review patterns, suggestion behavior, output verbosity. NOT for dev-environment setup (use `devcontainer`)."
domain: process
workspaces:
  - agent-config-maintainer
packs:
  - meta
---

# Copilot Skill

## When to use

Use this skill when:
- Editing `.github/copilot-instructions.md` to improve Copilot behavior
- Dealing with Copilot PR review comments (via `/fix-pr-comments`)
- Analyzing Copilot's review patterns to identify recurring false positives
- Tuning Copilot's code suggestions for the project


Do NOT use when:
- Augment-specific behavior (use Augment rules and skills)
- Writing application code

## Procedure: Configure Copilot

1. **Inspect current Copilot config** — Read `.github/copilot-instructions.md` (if any) and the *What Copilot Can and Cannot Read* table below to confirm Copilot Code Review vs. Chat scope.
2. **Decide self-contained scope** — Identify which rules must live in `copilot-instructions.md` (PR-review-relevant) vs. `.augment/` (agent-only).
3. **Apply changes** — Edit `copilot-instructions.md` with coding-standards, review-comment rules, and any new conventions; keep it self-contained.
4. **Verify** — Open a draft PR, confirm Copilot reads the new rules; for Chat, ask Copilot to summarize the active instructions.

### Configuration File

**`.github/copilot-instructions.md`** — the single source of truth for Copilot behavior.

### What Copilot Can and Cannot Read

| Context | Copilot Code Review (PR bot) | Copilot Chat (IDE) |
|---|---|---|
| `.github/copilot-instructions.md` | ✅ Reads automatically | ✅ Reads automatically |
| `.augment/rules/` | ❌ Cannot access | ✅ Can read if referenced |
| `.augment/skills/` | ❌ Cannot access | ✅ Can read if referenced |
| `.augment/guidelines/` | ❌ Cannot access | ✅ Can read if referenced |
| `AGENTS.md` | ❌ Cannot access | ✅ Can read if referenced |
| `agents/` | ❌ Cannot access | ✅ Can read if referenced |

**Key implication:** `copilot-instructions.md` must be **self-contained** for PR reviews.
It cannot reference `.augment/` files and expect Copilot Code Review to follow them.
For Copilot Chat users, a hint at the top of the file points to `.augment/` for deeper context.

### What Copilot Controls

| Area | How |
|---|---|
| Code suggestions | Follows coding standards, PHP 8.2 patterns, Laravel conventions |
| PR reviews | Reviews only modified lines + direct dependencies |
| Comment behavior | Deduplication rules, reply handling, scope control |
| Language | English code comments, bilingual PR comments (EN + DE) |

### Relationship to `.augment/`

`copilot-instructions.md` and `.augment/` serve different audiences:

| | `copilot-instructions.md` | `.augment/` |
|---|---|---|
| **Audience** | GitHub Copilot (bot + chat) | Augment Agent |
| **Scope** | Coding standards, review rules | Full agent infrastructure |
| **Self-contained?** | Yes (must be) | Yes (skills reference each other) |
| **Duplication** | Intentional — Copilot can't read `.augment/` | No duplication needed |

When updating coding rules, check if both files need the change:
- **Architecture/coding rules** → update both (Copilot needs them self-contained)
- **Agent workflows/commands** → only `.augment/` (Copilot doesn't use these)
- **PR review behavior** → only `copilot-instructions.md` (Augment uses `/fix-pr-*` commands)

## PR Review Comment Rules

Copilot is configured with strict comment behavior rules:

### Deduplication

Before creating a comment, Copilot must:
1. Check if it already commented on the same line/concern
2. Check if another reviewer already raised the same point
3. Skip if a duplicate would be created

### Reply Handling

| Developer response | Copilot action |
|---|---|
| Accepted suggestion | Acknowledge briefly or resolve |
| Rejected with reason | Accept the decision, do NOT re-raise |
| Asked a question | Answer with analysis and examples |
| Dismissed without explanation | Move on, do NOT re-raise |

### Key Principle

**One comment per concern per location.** Never duplicate, never re-raise rejected suggestions.

## Handling Copilot Bot Comments (as Augment Agent)

When the user asks to fix Copilot's PR review comments (via `/fix-pr-comments`):

### 1. Evaluate Each Comment

For each Copilot comment, determine:

| Category | Action |
|---|---|
| **Valid and actionable** | Fix the code as suggested |
| **Valid but already handled** | Reply explaining it's already addressed (e.g., by ECS/Rector) |
| **False positive** | Reply explaining why the suggestion doesn't apply |
| **Style nitpick** | Reply that ECS/Rector handles this automatically |
| **Out of scope** | Reply that the comment is outside the PR's change scope |

### 2. Reply Format

When replying to Copilot comments on behalf of the user:

```markdown
{English explanation}

---

🇩🇪 {German translation}
```

### 3. Common False Positives

Copilot frequently suggests things that conflict with project conventions:

| Copilot suggests | Project convention | Response |
|---|---|---|
| Add `null !== $var` with `is_string()` | `is_string()` already excludes null | False positive — redundant check |
| Register events manually | Laravel 11 uses event discovery | Not needed since Laravel 11 |
| Use `float` for money | Use `Math` helper class | Project uses BCMath via `Math::*()` |
| Add PHPDoc repeating signature | Only add PHPDoc when types are insufficient | Redundant documentation |
| Suggest `array()` syntax | Short syntax `[]` enforced by ECS | Auto-fixed by ECS |
| Add `final` to mocked classes | Classes mocked by Mockery can't be final | Would break tests |

## Improving Copilot Instructions

When updating `.github/copilot-instructions.md`:

### Structure

- Each section starts with `## ✅ {Title}`
- Rules are bullet points, concise and actionable
- Code examples use `✅ Correct` / `❌ Wrong` pattern
- Keep sections focused — one concern per section

### When to Add New Rules

| Trigger | Action |
|---|---|
| Copilot repeatedly makes the same wrong suggestion | Add to "Known Issues" section |
| New project convention introduced | Add to the relevant section |
| Copilot ignores scope control | Strengthen "Code Review Scope" section |
| Copilot creates duplicate comments | Strengthen "Comment Behavior" section |

### When NOT to Add Rules

- Don't add rules for things ECS/Rector auto-fix (Copilot doesn't need to know)
- Don't add rules that duplicate `AGENTS.md` content (Copilot doesn't read `AGENTS.md`)
- Don't add overly specific rules for one-off situations

## Relationship to Other Tools

| Tool | Role | Config |
|---|---|---|
| **Copilot** | IDE suggestions + PR reviews | `.github/copilot-instructions.md` |
| **Augment** | Agent workflows + deep analysis | `.augment/` + `agents/` |
| **Greptile** | PR review bot (if enabled) | Separate config |
| **ECS** | Code style auto-fix | `ecs.php` (project root) |
| **Rector** | Code refactoring auto-fix | `rector.php` (project root) |
| **PHPStan** | Static analysis | `phpstan.neon` (project root) |

Copilot and Augment complement each other:
- **Copilot** handles real-time suggestions and automated PR reviews
- **Augment** handles complex workflows, deep analysis, and multi-step tasks

## Related

- **File:** `.github/copilot-instructions.md` — Copilot configuration
- **Command:** `/fix-pr-comments` — fix all review comments (bot + human)
- **Skill:** `code-review` — PR review process and conventions


## Output format

1. Updated copilot-instructions.md or related config file
2. Summary of changes and which Copilot behavior is affected

## Gotcha

- copilot-instructions.md is for GitHub Copilot, NOT for Augment — don't mix audiences.
- Don't duplicate .augment/ content into copilot-instructions.md — it bloats the file and causes drift.
- Keep copilot-instructions.md under 150 lines (per `size-and-scope.md`) — Copilot Code Review reads only the first 4,000 characters, so put the highest-priority rules up top.

## Do NOT

- Do NOT let Copilot generate code that violates project coding standards.
- Do NOT accept Copilot review comments without verifying them against the codebase.

## Auto-trigger keywords

- GitHub Copilot
- copilot instructions
- PR review
- copilot behavior
