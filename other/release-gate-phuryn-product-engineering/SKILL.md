---
name: release-gate
description: "Before 'push it', 'ship it', a deploy, release or go-live, or calling a stage done: the gate, the owner's preview, go/no-go, promote, prove it serves, roll back."
---

# Release gate — how a change ships

A release is a decision: **the owner says go; the agent supplies the evidence.** This skill defines the evidence needed at each shipping step, the promotion procedure and how to prove the reviewed build serves.

**The product's own instructions come first.** Use its named branches, gate, backlog and record files, taking these rules as defaults where its instructions or release doc say nothing.

**On another stack, keep the principle and swap the mechanism.** Each rule states its principle first and the stack's mechanism second. The web-app rules were learned on Next.js (App Router), Supabase, Clerk and Netlify, with Vitest and Playwright. The client-and-backend rules were learned on a relay service with a web client and an editor extension with desktop installers (`references/runbook.md`).

## Two branches, named once

**Name the product and production branches in the release doc.** Write their real names there at the first push, and nowhere else.

- **Land stage work on the product branch.** Its default name is `<product>`.
- **Move the production branch only by fast-forward after release approval.** The host deploys this branch to production, with `<product>-prod` as its default name. Require the local gate, independent review and owner's go first.

**Treat product-branch pushes as deploys until the production branch exists.** Before then, the host deploys the product branch itself; apply the `environments` skill for branch-to-environment mapping.

When uploading a working tree with a host CLI or releasing code used by a local scheduled job, open `references/deployments.md`.

## The product's records

**Keep the release's evidence in the product's existing records.**

When setting up the release records or matching their names and scripts to your product, open `references/records-and-audits.md`.

## Stage and phase close

**Phase ends and deploying pushes require the full applicable gate.** Apply `test-harness` to compare the script with its suite contract. The owner decides any narrower set; record the choice in the plan with its reason and revisit trigger.

**Close stages with coordinator checks, reserving the full process for phases.** The coordinator runs touched and new tests and confirms changed journeys' end-to-end specs. Tests and corrected docs land with the change. Read the diff and run the router rows it matches (apply `agent-instructions` for those checks). An edited test, gate script or instruction file needs its reason, so a change cannot loosen the check that judges it. For screens, the coordinator takes a quick look at the running result, at phone and desktop widths and both themes when two exist. The builder never substitutes for that look. A stage owes no mandatory full gate, fresh review or `document-app` check. Mark its plan line done when its done-when holds from the coordinator's evidence, or write what keeps it open.

**Finish phase checks in order before its closing push and preview.**

1. The coordinator runs the full applicable gate on the finished phase.
2. The coordinator explores the phase's added or changed journeys and screens. Apply `ui-design` § Complete phase visual checks before its review series and owner preview. Do a rendered check of affected screens. For a new or materially changed journey, a kit change or an owner request, also do the newcomer walkthrough, screenshot critique and scored audit. Fix visual defects before starting the review series.
3. Apply `document-app` in check mode. It reports disagreements without rewriting docs.
4. Apply `independent-review` to the whole phase and run fresh rounds until the bar holds. List Lows for the owner. If a fix followed the last full gate, rerun the full gate on the cleared state. A resulting fix needs another fresh round. Earlier phase series never replace the first release's whole-product review.
5. Where the branch deploys, push the cleared state to close the series. Before hosting, keep the state local or push a branch that does not deploy. From the first deploying push onward, keep stage commits local or on a branch that does not deploy until the phase's closing push. An advisory stage round can overlap the next build for migration, authorization or money risks and clears nothing.
6. Offer the owner a development preview (§ The owner's preview). Record whether the owner tried each visible phase separately from its completion.

## Deploying pushes and production promotions

| Moment | What it owes |
|---|---|
| A push to a branch that deploys | The full applicable gate and a clean independent review round covering everything the push adds; **the push closes that round**. Before go-live the product branch is that branch: its URL is shared with nobody, so the production preconditions are not yet owed — but the gate and the round are, and pending migrations are applied to development first. **"Just push it" is a go for the push it names**: name back, in one line, any of these still open rather than pushing past it. |
| **A promotion to production** | Every precondition (`references/checklist.md`), then the go/no-go, the promote and the verify. **Going live is the first promotion** (`references/go-live.md`). |

## What counts as evidence

- **Read the exit code from the log, never the notification.** A background wrapper can report exit 0 when its inner command failed, so read that command's code rather than the notification.
- **An inherited report is a claim, not evidence.** Run the gate yourself before repeating a count, and take the release subject from git.
- **The coverage map is written by whoever ran the gate, and by nobody else.** A builder records its actual runs and their limits. Read every line it adds and rewrite completion evidence from your own applicable run, rather than editing its numbers. Apply `test-harness` for the map's format.
- **A delegated diff is unreviewed code.** Read what comes back before believing it; nothing delegated ships or deploys without independent review. Keep product decisions, review-finding acceptance and stage-completion judgement with you. Keep operational changes too: deploys, applied migrations, pushes, workers, provider settings and secrets, including development, plus production credentials. Builders run development suites within their brief's boundary. Apply the `delegation` skill for these boundaries, including its Codex reference when Codex builds.
- **What was left out is stated, not hidden.** Record preconditions the owner waives as waived, never ticked as completed.
- **A caveat is a claim about the world, and gets checked like one.** Before saying something has not happened, was not tested or still needs doing, find where its evidence would live and look. Caveats can sound humble enough to escape verification, yet wrong ones still cost the owner's time.
- **The gate is the exit code, not the printed counts.** Printed passing counts can accompany exit 1 (`test-harness`).

## The independent review — mandatory at every release

**Review before every deploying push and again before production promotion.** Apply this however small the change and however green the gate. Before every round, apply `independent-review` § Reviewer selection and isolation and § Running it for its wrapper, selection, fallbacks and failed-round evidence.

**Use fresh Codex when no reviewer is named.** Prefer a qualifying product-named reviewer or recorded fallback. Otherwise use the wrapper's available reviewer without asking. A fresh session of the builder's family can serve when other families cannot. Record the reviewer, why it ran and anything left enabled.

When reviewer CLIs cannot run, open `references/checklist.md` § Manual review before clearing the release or deploying push.

**Compute review subjects from git and repeat until the bar holds.** Cover the whole unreleased range in round one, then only changes since the last round, with everything else as context. Fix what the bar names, rerun the tests each fix touches yourself, then review again. Apply `independent-review` for full gate timing and recording accepted Lows. Stop only when the round has no INTRODUCED finding above Low after `independent-review` § Triage, and no High or Critical of any age remains open. Put pre-existing findings in the backlog with a reason and revisit trigger. Fix High and Critical now, regardless of age.

## Static audits — proposed, never run unasked

**Propose static audits at each release and wait for the request.** Propose both the security and performance audits in the `static-audit` skill on the release's changes. Propose a whole-repository pass only for the first release, after a large refactor, or when the owner asks. Run these steered passes beside the independent review rather than using them to replace it. Keep reports under gitignored `reports/` so security reports stay out of repository history. Fix findings or backlog them, and record declined passes as declined. Exact ranges are in `references/checklist.md`.

When docs and coverage evidence are maintained with changes, open `references/records-and-audits.md` before running doc checks or acting on audit recommendations.

## Migrations: never rely on a push to apply them, or not to

Before a deploying push or promotion for a product with database migrations, open `references/migrations.md`. Check the integration, the ledger and what must be applied before the push.

## The paid-launch check

**Sell only what runs.** Every selling or promising surface reads the same launch list. Require its separate, non-skippable test to pass on the exact commit before production billing exists and at every promotion. Flip an area's flag and update its claims in the release that makes it live. The list, its consumers and the test are in `references/go-live.md` § The paid-launch check.

## The owner's preview

**Send the owner a preview after phase checks and any closing deploy.** Ready means the phase checks passed and its review series is clean (§ Stage and phase close). Give a link and a short list of what to try, including the look review. Ten minutes using the product finds what reading code does not.

When the owner asks for an early preview, open `references/preview.md` before sharing it.

- **List changed flows as actions with their expected results.** For example: "Upload a 6 MB photo as the logo: the page shows it sharp." Then state missing or unverified work and unbuilt features, naming the stage that brings each. This keeps the owner's review focused on what exists.
- **Every preview and go message names each suite that did not run.** Counts alone can imply the running app and real sign-in were tested. For example: "Unit and integration passed; `e2e:auth` did not run: development test mode is not configured." Name the reason and what brings each run back, even when the coverage map already records the gap.
- **Link deployed development or use a temporary development tunnel.** Prefer the deployed development URL when hosting exists and contains the change. When the change lacks a deployed development URL, open `references/preview.md`.
- **Keep owner feedback in the phase currently in flight.** Add stages for it and review fixes like any other change. A pending owner preview does not block the next phase. Track whether each visible phase was tried. Stage 3's explicit sample-data click-through remains its done-when; one link and list fulfil that request.
- **Offer owner previews after phase checks without blocking the next phase.** Design direction, artboards, options, legal text and release go remain owner decisions. The release go message names every visible phase the owner has not tried.
- **"Ready to test" means installed on every surface the owner holds, with nothing for the owner to do first.** When the change reaches an installed app, an extension or a phone the owner uses, open `references/preview.md` § Promotion and installed surfaces before sending the link.
- **Explore changed screens and affected shared surfaces at promotion.** For a go-live or broad UI change, or a preview on an installed app, extension or phone, open `references/preview.md`.

## Verify — the build serving is the one you reviewed

Commands and the record are in `references/checklist.md § 4`.

- **First prove the new build is the one serving.** A failed build can leave the old deploy serving, letting checks pass against old code. Find something the diff adds and something it removes, then check both in production's response. A cache holding two builds can serve an addition, while a removal rules that out.
  For content probes or a build that changes no served bytes, open `references/deployments.md`.
- When the deploy serves code that reads a database or leaves other runtimes on separate bundles, open `references/deployments.md` for the schema and runtime checks.
- **Deploy only from a clean checkout at the release branch's tip.** Make every deploy and status command refuse any other tree. A promotion does not move an operator's checkout, and "current" compares only with the tree running the check.
- When a CDN sits in front of the origin, or the origin is moving, open `references/deployments.md`.
- **A deploy can change behaviour nothing in your diff touched.** Reverify hardening controls after every deploy. The local gate has no edge. An unpinned host adapter is an untracked release input. When behaviour changes without a diff, check versions before changing code. **A transient control is worse than an absent one.** Its passing run is the one you quote.
- **The smoke runs last.** Edge limits can refuse your own address for a minute.
- For a deploy touching sign-in, sessions, ownership or entitlements, or a release with an installed client, open `references/deployments.md` for the canary and installation checks.
- **Tag after the checks, never before.** Record the results with the release.

## Any release, not only a web deploy

**Run each release as one ordered, logged checklist.** This includes packages, extensions, installers, store listings, and clients with backends. Log each step's command, pass and evidence in the release plan (`references/runbook.md`). Record every skip with its reason; correct a faulty list in the same pass.

- **If a script exists for a step, use the script.**
  When running or writing a release script, open `references/runbook.md` § One list, run with a log.
- For a client with a backend, or a shared contract across repositories, open `references/runbook.md` § C.
- For release artifacts or a store listing, open `references/runbook.md` § D.
- **Nothing unreleased is described in the present tense.** Describe it as future work.
- Before closing an issue whose fix ships through a store, open `references/runbook.md` § E.
- For a public ref, generated listing or contribution going out in the release, open `references/runbook.md`.
- When a plugin or skill marketplace serves a branch, open `references/runbook.md` § The marketplace branch before pushing.

## Never

Force-push the production branch · promote with an unapproved suite omission, a stale doc, or an unrun local gate · run any authenticated smoke with a real user's credentials · test against production data · apply a migration through an MCP server or the dashboard · link the database CLI to any project · deploy a runtime from a checkout that is not the release tip · hand-roll a step a release script encodes · infer a go from an ambiguous reply · announce a store listing as live before it serves the version.

## A promotion, in order

1. **Complete every precondition with evidence.** Use `references/checklist.md § 1`.
2. **Silence is not go.** Post the go/no-go with the checklist, evidence and one paragraph (`§ 2`), and get the owner's answer in chat.
3. **Migrate by production connection string before promoting by fast-forward.** Apply pending migrations through the CLI and reread the ledger (`§ 3`).
4. **Verify the serving build, schema and runtimes before tagging and recording.** Check that every other runtime is current (`§ 4`).

When rolling back code, schema, a runtime, configuration or a key, or when adding guards or hosted CI, open `references/go-live.md`.

Each rule's origin, the case that taught it, is in `receipts.md` beside this file; read it when a rule's edge is unclear.

## How you can tell it worked

The reviewed commit serves on the live site, beyond the deploy log, and the post-promotion checks passed. The owner gave the go after the preview.

## Files

When choosing a reference or related skill for a release task, open `references/records-and-audits.md` § Files.

For a Netlify edge rule, client-IP check, redirect, or deploy whose behaviour changed without a diff, open `references/netlify.md`.
