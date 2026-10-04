---
name: finalize-and-ship
description: "End-of-task routine: health checks, fixes, then commit and push. Use when finishing a unit of work, or when the user says 'commit and push', 'ship it', 'get it ready', 'wrap up', or just 'do this' with no push instruction."
---

# finalize-and-ship

Complete the owned feature with its required local proof, then commit and push. A pushed feature
is complete; deployment, production/live-site verification, full release work, and waiting for
other agents belong to release owners. Scheduled release owners follow their ship-first policy
below; they do not run the feature-author checklist as an unconditional release prerequisite.

## Before anything else: is the outcome there, from the user's seat?

Finishing means the user can do what he asked, the way he meets the product — not that the
checks are green. For changed UI, drive the changed code in an actual localhost browser and
confirm what he will see. For non-UI work, exercise the closest real local behavior boundary.
If you cannot, the task is not at its end, and green checks will only make the gap harder to
notice ([reality is the referee](../../../../common-docs/policies/reality-is-the-referee.md)).

## The commit/push contract (read first)

The user task and repository instructions determine commit authorization; invoking a skill grants no additional authority. Two independent decisions — **scope** (what to stage) and **delivery** (commit vs push vs hold). Read both from the user's words.

**Scope — what to stage:**

| User said | Stage |
|---|---|
| "commit **your** work" / "commit what **you** did" / "your changes" | **Only the files you created or modified this session.** Leave everything else in the working tree untouched. |
| "commit **everything**" / "commit **all**" | The explicitly authorized batch, after checking concurrent ownership. |
| A general "commit & push" / **nothing specific** | Only this task's files; shared-checkout work from other agents stays theirs. |

When scope = your-own and the tree also holds files you didn't touch, never sweep them in — stage your paths explicitly (never blind `git add -A`).

**Delivery — what to do with it:**

| User said | Do |
|---|---|
| "commit & push" / "ship it" / "push to main" / **nothing about pushing** / just "do this" | Relevant checks → fix owned behavior → **commit → push to `main`** |
| "get it ready, but don't push" / "don't push" | Relevant checks → fix owned behavior → **commit → STOP** (no push) |
| "don't commit" / "just stage" / "leave it for review" | Relevant checks → fix owned behavior → **stop before committing** |

Defaults: scope = **this task's files**, delivery = **commit and push**. Follow explicit holds. Concurrent edits are normal: stage scoped paths and coordinate overlapping files; do not turn unrelated dirty files into an approval request.

## Feature-author checks

Run checks relevant to changed behavior. Check every touched type boundary and prove the change
introduced no type errors; use the canonical generator for changed contracts and never suppress
errors or hand-edit generated files. Run meaningful tests that reach the changed behavior,
exercise changed UI in an actual localhost browser, and repair every regression your change
introduced before committing. Obtain independent review when the change's risk or scope requires
it. Record unrelated ordinary findings for bounded repair; do not repeat a full `pnpm sync-types`
until green merely to dispatch a release. Migrations belong to their own implementation: never
apply an unrelated pending backlog as release preparation.

## Scheduled release owners

The September 12 pre-production [release policy](../../../../common-docs/policies/reality-is-the-referee.md)
is authoritative. Integrate once, perform prescribed preparation once, dispatch and
return. No unconditional type-generation/type-check or local build gate. Preserve real
organization authorization and hosted build/startup acceptance. A previous failed build
requires a targeted repair and relevant passing check before retry; never blindly
re-dispatch the same failed source. Read bounded script logs after dispatch, batch real
warnings/errors, and fix the actual failure at the next run's start. Normal version
advance is information, not a warning or a reason for a repair loop.

### 3. Touch-based checks — only the rows your change hit

| If your change touched… | Do this before committing |
|---|---|
| A **Tier 1/2 feature** (logic, flows, entry points, invariants) | Update its `FEATURE.md` + add a dated Change Log line |
| A **route / window panel / overlay / official component** | Add it to that feature's `/[feature]/admin` map config |
| A **new type / component / hook / slice** | Confirm no existing primitive could extend instead (PRINCIPLES.md); `pnpm check:doctrine` flags new ones |
| **Scope/context** code | Respect the global-vs-local invariant (CLAUDE.md → Scopes) |
| Any **user-facing surface** | No `window.confirm/alert/prompt`; no new barrel `index.ts`; Lucide icons only, no emojis |
| A **completed plan / handoff / campaign** | Invoke `handoffs` for handoffs: completed handoffs are deleted, not archived. Archive completed plans/history under their owning documentation policy and repair inbound pointers. |

Do not broaden scheduled release preparation into a full validation sweep.

### 4. Open findings in the files you touched — part of done

Run the findings tool on the files in your diff (feature authors; release owners skip it):

```bash
# the task's files: uncommitted + committed-but-unpushed (add any you already pushed this task)
files=$(git diff --name-only HEAD; git diff --name-only origin/main...HEAD)
[ -n "$files" ] && pnpm findings $files                      # matrx-frontend
[ -n "$files" ] && uv run python scripts/findings.py $files  # aidream
```

Never run it with no paths as a done-check: no paths means every converted check's whole backlog.

Exit 1 means a converted check names a NEW item in a file you touched. **An open finding in files
you touched is part of done: fix it, or accept it with a reason.** Each item prints its fix hint
and the exact accept command (`pnpm findings accept <check> '<key>' --reason "<why>"`), which
writes the key into that check's own allowlist with your reason, proves the item is now known,
and commits only that allowlist. Accept only what is genuinely fine and say why; never accept to
get green. Known debt is not printed and is not yours unless you touched it.

### 5. Commit & push

Plain git, per the global commit rules: review `git status` + `git diff` first, stage the **specific** files (never blind `git add -A`), write a conventional commit (`feat(...)`/`fix(...)`) via a HEREDOC, then `git push origin main`. Quality gates (`check:doctrine`, UI primitives, migrations, dead-relations) run at **release time** via `./scripts/release.sh` / `pnpm check:release-gates` — not on every commit. The one narrow runtime admission is different: `release.sh` read-only checks the committed candidate's required surface registrations before tag/push. It neither syncs nor repairs manifests, and it does not make advisory registry drift a release gate.

> `pnpm ship "msg"` is the **versioned-release** path. Only the existing release owner uses the
> release-freshness rule below; feature authors stop after local proof, commit, and push.

### 6. Release-owner only — deployment is downstream of feature completion

Feature authors stop after their required local proof, commit, and push. They do not run,
wait for, or report deployment. The following release procedure applies only to the designated
release owner or an assignment that explicitly includes immediate release work.

**Vercel skips every commit whose first line is not release-prefixed** (`vercel.json` → `scripts/vercel-ignore-build.sh`). A plain `git push origin main` reaches GitHub and **no user, ever**: no build starts, the deployment reads `CANCELED`, and production stays on the last release.

The release owner dispatches; the central build monitor observes completion on its configured
schedule:

| Situation | Do |
|---|---|
| Latest applicable `origin/main` code is already contained in every affected target's latest `Ready` deployment | No release; record the verified target SHAs. |
| Any affected target is missing applicable `origin/main` code | The pushed `origin/main` commit is the durable handoff; the frontend owner picks it up on its normal pass and cadence. Do not send or request an expedited-release message. Run `./scripts/release.sh` yourself only when the user requested an immediate release, per `CLAUDE.md`. Shared runtime changes affect all three targets. |
| A release for the exact applicable SHA is already queued or building | Do not duplicate or wait through it. The central build monitor records a new failure in durable lane state; the owner reads unresolved state on its normal pass. |

Verify a release actually landed: a `READY` production deployment whose commit is yours or a descendant (Vercel MCP `list_deployments`), then assert on a string that exists **only** in the new build — a marker the old build also contained reports a false success.

Release-script changes require task authorization and must preserve real authorization,
source-integrity and hosted build/boot boundaries. Arman's September 12 release review
explicitly authorizes removing redundant quality prerequisites; a stale sentence in this
skill cannot reintroduce them.

## Recover before escalating

Read `protected-resources` before changing admins, RLS, or SECURITY DEFINER code; a skill name
alone does not require approval. Fix non-idempotent migrations, type-contract mismatches, and
failed checks at their source. Never use forbidden casts/suppressions to force a pass.
Escalate only when safe discovery and repair are exhausted and a missing credential,
human-only authentication gate, destructive action outside authorization, or consequential
unresolved product decision actually requires the user. Record exact unfinished evidence;
a status report does not replace an available repair.

Verified 2026-09-09 during Agent Review First Pass: reconciled shared-checkout scope, database capability recovery, release ownership, and handoff cleanup with repository instructions.

## Reference

| Thing | Where |
|---|---|
| All-checks runner | `pnpm validate` (`scripts/validate.mjs`) |
| Type sync | `pnpm sync-types` (`scripts/sync-types.mjs`) |
| Migration verify + apply/record | `pnpm check:migrations`; CLAUDE.md → "Database migrations" |
| Type-fix rules | `type-safety` skill (`.claude/skills/type-safety/`) |
| Doctrine (new primitives) | `pnpm check:doctrine`; `PRINCIPLES.md` |
| Pre-release gates | `pnpm check:release-gates` or `./scripts/release.sh` (each gate announces itself; advisory by default) |
| Versioned release | `pnpm ship "msg"` |
