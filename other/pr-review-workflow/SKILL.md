---
name: pr-review-workflow
description: Step-by-step procedure for reviewing PRs created by the Copilot coding agent, including CI wait, code review checklist, and merge/revision workflow.
disable-model-invocation: true
---

# PR Review Workflow

Step-by-step procedure for reviewing PRs created by the Copilot coding agent.

## Overview

CI workflows (tests, linting) only run on PRs that are **ready for review** — not on draft PRs. The Copilot agent creates PRs in draft state. The orchestrator must follow this sequence:

1. Wait for the agent to finish work
2. Mark the PR as ready for review (triggers CI)
3. Wait for CI workflows to complete
4. Review the code and CI results
5. Merge or request revisions

## Step 1: Wait for agent to finish

Check for `copilot_work_finished` in the PR timeline:

```bash
gh api repos/EvaLok/schema-org-json-ld/issues/{PR}/timeline --paginate \
  --jq '.[] | select(.event) | select(.event | test("copilot")) | {event, created_at}'
```

**Note**: Avoid `!= null` in jq expressions passed via `--jq` — the `!` gets shell-escaped by the permission system. Use chained `select()` instead. Also avoid `tail` (not in allowed commands) — the jq expression already filters to relevant events.

**Do not proceed until `copilot_work_finished` appears.** The agent pushes multiple commits during a session — reviewing mid-session wastes effort.

## Step 2: Mark PR as ready for review

Once the agent finishes, remove the draft status:

```bash
gh pr ready <PR_NUMBER> --repo EvaLok/schema-org-json-ld
```

This triggers CI workflows (test-unit, cs-check, etc.) on the PR branch.

## Step 3: Wait for CI workflows

Check CI status:

```bash
gh pr checks <PR_NUMBER> --repo EvaLok/schema-org-json-ld
```

Wait for all checks to complete. Expected checks:
- **Test and Build** — runs `composer run test-unit`
- **Lint** — runs `composer run cs-check`

If checks fail, review the failure before proceeding. Common failures:
- Test failures → the agent's code has bugs
- CS-check failures → the agent didn't run `composer run cs-fix`

## Step 4: Review the code

Fetch the PR diff:

```bash
gh pr diff <PR_NUMBER> --repo EvaLok/schema-org-json-ld
```

### PHP review checklist:
- [ ] Correct `@type` value in `A_SCHEMA_TYPE`
- [ ] Required properties match Google Rich Results docs
- [ ] Constructor uses promotion for all properties
- [ ] `null|Type` syntax (not `?Type`)
- [ ] Required params first, optional params (with `= null`) last
- [ ] Array properties have `/** @var Type[] */` doc comments
- [ ] No `toArray()` or other serialization methods
- [ ] Tests cover: minimal output, null omission, full output, nested schemas
- [ ] Enums use backed string values with schema.org URLs
- [ ] No modifications to `JsonLdGenerator.php` or `TypedSchema.php`

### TypeScript review checklist:
- [ ] `static readonly schemaType` matches the schema.org type name
- [ ] Required properties match Google Rich Results docs (same as PHP)
- [ ] Options-object constructor pattern used (no positional constructors)
- [ ] `{TypeName}Options` interface exported alongside class
- [ ] `public readonly` on all class properties
- [ ] `Type | null` for optional properties (not `?:` on the class — `?:` is only for options interface)
- [ ] Optional fields use `?? null` in constructor body
- [ ] Import paths include `.js` extension
- [ ] Barrel export added in `ts/src/index.ts`
- [ ] Tests cover: minimal output, null omission, full output, nested schemas, PHP parity
- [ ] Enums use string values with full `https://schema.org/` URLs
- [ ] No modifications to `JsonLdGenerator.ts` or `TypedSchema.ts`
- [ ] Biome formatting passes (`npx biome check`)

## Step 5: Merge or request revisions

**Only merge when the PR is genuinely clean.** Do not merge with known issues, even minor ones.

**If everything passes:**

```bash
gh pr merge <PR_NUMBER> --repo EvaLok/schema-org-json-ld --squash --delete-branch
```

**If revisions are needed:**

Batch feedback into a clear `@copilot` comment:

```bash
gh pr comment <PR_NUMBER> --repo EvaLok/schema-org-json-ld \
  --body "@copilot Please fix the following:
1. ...
2. ...
3. ..."
```

Then go back to Step 1 — wait for the agent to finish the revision before re-reviewing.

**Iterate as many times as necessary.** Copilot requests are effectively unlimited — there is no cost pressure to merge early or limit revision rounds. If the first `@copilot` revision doesn't fully resolve all issues, comment again with further instructions. A PR that takes three rounds to get right is a success. A PR merged with known defects is a process failure.

## Using the review-pr tool

The `tools/review-pr` script automates Steps 1-3:

```bash
tools/review-pr <PR_NUMBER>           # Check status, mark ready if agent finished
tools/review-pr <PR_NUMBER> --merge   # Also merge if CI passes
tools/review-pr --help
```
