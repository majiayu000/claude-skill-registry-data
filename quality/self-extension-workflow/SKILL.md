---
name: self-extension-workflow
description: Apply when executing the self-extension workflow. Six steps from a mistake to a merged rule, with CI gates and CODEOWNERS approval.
license: MIT
version: 1.0.0
tokens_target: 2000
triggers:
  - executing self-extension
loads_after: [error-log]
supersedes: []
---

# Self-extension workflow
*Exact prompt and procedure the agent executes after every mistake. The agent never pushes to `main` directly. Every self-extension is a PR.*

> *Five agent steps plus a search-prerequisite, from mistake to merged rule. The agent never pushes to main. Every rule that lands is CODEOWNERS-approved. This page is the contract.*

<!-- target: ~1100 tokens -->

---

## TRIGGER CONDITIONS
*Five conditions. Any one of them starts the workflow.*

The agent starts this workflow when **any** of these is met:

- A test fails and the agent wrote the faulty code.
- A code review comment corrects the agent.
- The agent realises during implementation that its first approach was wrong.
- A deployment problem occurs that the agent caused.
- The user explicitly says: "That was wrong" / "Remember this".

---

## STEP-BY-STEP PROCEDURE
*Five steps after the search-prerequisite. Every step is mandatory before the next one.*

### Step 0 — Search before write
*Mandatory. Duplicates in the error log destroy the signal.*

Before creating a new error entry, search the existing error log:

```text
1. Read skills/error-log/SKILL.md.
2. Search for similar errors (same category + similar context).
3. If a similar entry exists:
   - Increment its `count` field by 1.
   - Update `last_seen` to today.
   - Supplement the context if needed.
   - Do NOT create a new entry.
4. Only if no similar entry exists, continue with Step 1.
```

### Step 1 — Analyse the error
*The agent answers six questions before writing anything.*

```text
1. What exactly did I do? (concrete code/action)
2. What should I have done instead?
3. Why did I do it wrong? (false assumption, missing knowledge, carelessness)
4. Which category applies?
   - development: code error, wrong implementation
   - git: commit/branch mistake
   - deployment: deployment order, configuration
   - security: security vulnerability
   - performance: N+1, missing indexes, oversized datasets
   - domain: wrong understanding of business rules
5. How severe was the error? (critical/high/medium/low)
6. Which target file does the rule belong in?
```

### Step 2 — Determine new error ID
*Take the next number after the latest entry.*

```bash
# Find last entry in error-log.md
grep "id: ERR-" skills/error-log/SKILL.md | tail -1
# Take next number: ERR-2026-004 -> ERR-2026-005
```

### Step 3 — Formulate the entry
*Action directive only. The CI verb allow-list rejects anything else.*

Use the template at `skills/error-log/_entry-template.md`. The schema at [`schemas/error-entry.json`](../../schemas/error-entry.json) is enforced by CI.

> [!WARNING]
> **CI GATE · verb allow-list** — `new_rule` must start with one of `Always`, `Never`, `Before`, `After`, `Prefer`, `Avoid`, `Use`, `Do`, `Ensure`. Anything else is rejected.

Bad: `"SQL injection is dangerous"`
Good: `"Never concatenate user input directly into SQL queries. Always use prepared statements."`

### Step 4 — Determine target file
*One file per category. Domain rules go to a project file, not a global one.*

| Error category | Target file |
|---|---|
| `development` | `skills/code-quality/SKILL.md` |
| `git` | `skills/git-conventions/SKILL.md` |
| `deployment` | `skills/review-deployment/SKILL.md` |
| `security` | `skills/code-quality/SKILL.md` (Security section) |
| `performance` | `skills/code-quality/SKILL.md` (Performance section) |
| `domain` | `skills/<project>/SKILL.md` |

### Step 5 — Insert the rule
*At the end of the matching section. Reference the ERR-ID.*

1. Open the target file.
2. Find the matching category section.
3. Add the new rule at the end of the section.
4. Add reference: `Reference: ERR-YYYY-NNN`.

### Step 6 — Open a PR
*Never push to `main` directly. The label triggers the lint-rules workflow.*

```bash
git checkout -b learn/ERR-YYYY-NNN
git add skills/
git diff --cached            # MANDATORY human review step
git commit -m "learn(errors): ERR-YYYY-NNN — <short description>

Co-Authored-By: <your real name> <your-email@example.com>"
git push -u origin learn/ERR-YYYY-NNN
gh pr create --label needs-rule-review \
             --title "learn(errors): ERR-YYYY-NNN" \
             --body "Auto-generated rule. Reviewer: confirm rule wording and target file. CI \`lint-rules\` must pass."
```

![PR flow — branch, commit, push, PR; lint-rules and auto-approve-rule-pr CI gates run in parallel; CODEOWNERS human gate; squash-merge into main behind branch protection](../../docs/pr-flow.svg)

*Branch through CI gates and CODEOWNERS into a squash-merge on `main`.*

**Why a PR (not a direct commit).** *Four layers of gating.*

| Layer | What it gates | Where |
|---|---|---|
| `lint-rules` | Schema + verb allow-list + forbidden patterns | [`schemas/error-entry.json`](../../schemas/error-entry.json) |
| `auto-approve-rule-pr` | Diff scope (`skills/**` — error-log entry plus the target sub-skill) and `Co-Authored-By:` trailer | `.github/workflows/auto-approve-rule-pr.yml` |
| Branch protection | CODEOWNERS approval for `skills/error-log/` | `.github/CODEOWNERS` |
| Human review | Final read of rule wording and target file | maintainer |

> [!NOTE]
> **CI GATE · four-layer gating** — Every rule that goes live has been seen by a human. The validator is best-effort, not airtight — see [SECURITY.md](../../SECURITY.md) Limitations section.

The commit type `learn` makes self-extension visible in `git log --grep="learn("`.

---

## FALSE POSITIVES IN THE VALIDATOR
*When a legitimate rule must mention a forbidden pattern (e.g. preventing `subprocess` misuse).*

1. Add the new error ID to `skills/error-log/exceptions.yml`:
   ```yaml
   allow_forbidden_pattern_for:
     - ERR-YYYY-NNN  # rationale: rule must mention `subprocess` to be specific
   ```
2. Open the PR. CODEOWNERS approval is required for `exceptions.yml` changes — the bypass is auditable in git history.
3. The verb allow-list still applies even with a bypass entry.

---

## CONSOLIDATION LOOP
*When the error log exceeds 50 entries. Manual diff review until eval framework lands.*

```text
1. Read all entries in skills/error-log/SKILL.md.
2. Group by root_cause similarity.
3. For groups with the same root cause:
   - Keep the most detailed entry.
   - Sum up all `count` values.
   - Set `last_seen` to the most recent date.
   - Delete the duplicates.
4. For entries older than 6 months with severity: low:
   - Archive (move to a comment block or separate archive file).
   - The rules derived from them remain in the sub-skills.
5. Open a PR: "chore(errors): consolidate error log (N entries merged)".
```

LLM-driven consolidation is non-deterministic. Until the eval framework (Phase 2 roadmap) reports a stable baseline, do consolidation **manually** with diff review. The threshold of 50 entries is a soft signal, not a forced rebuild.

---

## WHY THIS SUB-SKILL MATTERS
*Self-extension as a normal version-control discipline.*

The agent doesn't just fix errors — it learns from them, and **every lesson is a Git commit you can review, revert, or share.** The PR-flow brings the standard engineering toolkit to rule learning: deterministic validation, branch protection, CODEOWNERS approval, and a public audit trail.

> ***Your agent's mistakes — versioned. Self-learning skills, every commit. One source, four agent runtimes.*** *That's the loop.*
