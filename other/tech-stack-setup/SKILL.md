---
model: opus
effort: medium
description: Guide a user to a coherent technology stack — language, frameworks, database, host, and providers that work well together — then generate a repository conforming to STACKSPEC, the organization's technology-neutral invariants specification. Also audits an existing repo against those invariants and reports drift by section. Use when the user wants to start a new product, asks "help me pick a stack", "scaffold a conforming repo", "bootstrap a new product", "set up the tech stack", "does this repo conform", "check conformance", or invokes /luismc-project-setup:tech-stack-setup. This skill does NOT build authentication — that is the auth-setup skill, and it only runs if the user asks for it at the end.
---

# Tech stack setup — a guided wizard, then a generator

This skill does two things:

1. **Guides the user to a coherent stack.** It is a filtered interview, not a
   menu. Every option offered is compatible with everything already chosen, and
   every consequence is stated at the moment of the choice.
2. **Generates a repository** conforming to **`STACKSPEC` 8.1.0**, the binding
   invariants specification at `references/invariants.md`.

## The two halves, and why they are separate

`STACKSPEC` 8.1.0 contains **no technology names**. It specifies properties:
contract-first APIs, atomic enqueue, adapter boundaries, retention and erasure,
consent-gated analytics, three-tier promotion. These hold whether the product is
TypeScript on Vercel or Rust in a container.

The technology knowledge lives in `assets/catalog/`, which is data, not
requirements. Nothing in the catalog is graded. `STACKSPEC §0.2` defines a
fourth requirement level, **`CHOICE`**, for this purpose. A `CHOICE` is reported
as *recorded* or *unrecorded*, never as conforming or violating.

**Read the spec before acting on it.** It has about 1,050 lines. Read the
sections a step needs. Do not work from this file's summary, and do not generate
against a clause you have not read.

## Scope — what this skill does not do

**It does not build authentication.** `AUTHSPEC` is a separate binding spec owned
by the sibling `auth-setup` skill. This split exists to stop running both in one
pass. A user who asked to "set up the stack" got a full auth stack that they had
not asked for and could not review in one sitting.

`AUTHSPEC §2.1` resolves the stack by finding a declared stack document in the
project, and the Stack Profile this skill writes *is* that document. So the
order is not a preference: auth-setup has nothing to resolve against until this
skill has finished.

**Phase 9 asks whether to run it. Never start it automatically**, not even if the
user said "set up the whole thing" at the beginning.

## The distribution rule — do not violate it

A product **MUST NOT** contain a copy of the spec (`§2.1`, `§16`). The spec lives
here, versioned with this plugin. A product carries a **Stack Profile** instead:
`assets/stack-profile.md`, deployed to `docs/architecture/stack-profile.md` (STACKSPEC `§18`; a repo that still has it at `docs/specs/stack-profile.md` is read there until it moves), naming the
spec version it conforms to plus its selections, capability gaps and deviations.

A vendored copy becomes a second, competing authority. No CI check can compare
it against the original. The profile's version reference is the only thing that
can go stale in a way that can be detected.

---

# Mode 1 — The wizard

`STACKSPEC` is prescriptive enough to generate from directly. There is no
template repository.

## Phase 0 — Establish the target, then announce the foundation

Confirm the working directory, that it is a git repo (`git rev-parse
--show-toplevel`; offer `git init` if not), and that it is empty or nearly so.
If it already holds a product, switch to Mode 2. Do not generate over existing
code.

Then **show the fixed foundation and ask nothing about it.** From
`assets/catalog/roles.yaml`, the `fixed:` block:

| Layer | Fixed |
|---|---|
| Repo | Git, monorepo `apps/` + `packages/`, `docs/specs` + `docs/notes` |
| CI | GitHub Actions, path-filtered, twelve required gates (`§13.1`), gated E2E (`§11.2`), a default-branch run that skips a tree already tested |
| Delivery | a branch gate with a verifiable result, a pre-push guard hook, a merge script and a CI watcher (`§13.5`, `§13.6`) |
| Promotion | preview per PR, staging on merge, production on release (`§13.2`) |
| Security | gitleaks pre-commit + CI over full history, dependency scanning |
| Contract | One machine-readable contract, authored first, all clients generated from it (`§4.1`) — the *format* is chosen in Phase 3 |
| Secrets | three tiers, one validated config schema, value-free example env |

Everything else is chosen. Say that explicitly. It sets the expectation for the
next eight phases.

## Phase 1 — Profile the product

Six questions, none about technology, from `roles.yaml`'s `profile:` block:
team expertise · cost posture · ops appetite · compliance and residency ·
lock-in tolerance · **does mobile ship**.

Mobile has the largest cascade of the six. It forces generated Swift and Kotlin
clients, push credentials and store declarations, and it makes hypermedia web
approaches cost double. Ask it even when the answer seems obvious.

Two answers are worth reacting to immediately:

- **Compliance is anything but `none`** → the free bundle is eliminated outright.
  Free tiers rarely offer a DPA and often pin no region. Say so now, not later.
- **Lock-in tolerance is "want a clean exit"** → single-vendor bundles are the
  highest-lock-in options in the catalog. Surface the contradiction. Do not let
  both answers stand.

## Phase 2 — Entry fork

Three ways in, not two:

| Path | What it does |
|---|---|
| **Recommend me a stack** | Derive 2–3 complete candidates from Phase 1 and present them side by side. Most users should take this. |
| **Infrastructure first** | Host constrains language. |
| **Language first** | Language constrains host. |

The two ordered paths are the same solver with a different binding order —
`roles.yaml`'s `entry_paths:` holds both orders.

## Phase 3 — Bind the roles, filtering after every answer

Work the chosen order. For each role:

1. **Filter** candidates against everything already chosen, using the
   `conflicts`, `requires` and `hosting` scores in the catalog files.
2. **Compare** the survivors on the axes that decide it: cost band, ops burden,
   lock-in, and fit with what is already chosen. Use a table, not prose.
3. **Recommend** one, with a reason referencing the Phase 1 profile.
4. **Say why anything was eliminated.** "ElastiCache is VPC-only and you said no
   VPC" is the guidance. Silently omitting it is not.

### The cross-constraint that matters most

Server language largely determines which hosting is viable. From
`tech/hosting.yaml`:

- Picking **Vercel or Cloudflare first eliminates Go, Rust and .NET** for the API.
- Picking **Go, Rust or .NET first eliminates them as API hosts**, but **not**
  as web hosts. Offer split hosting (web on an edge platform, API in
  containers). Do not treat "not all one vendor" as a failure. `§4.1`'s generated
  client is the seam, and it already has to exist.

### Vendor roles are open, and that is the point

Every provider (database engine and host, cache, storage, mail, error tracking)
is a `CHOICE`. None produces a deviation. Say out loud why this is safe:
**`§3.3` confines each vendor SDK to exactly one adapter module**. That turns
"we picked the wrong provider" into a change to one file. That rule is what
allows the freedom. Mention it when the user hesitates over a vendor.

**No role is closed, but four carry a property the candidate must satisfy.** The
spec names no technology anywhere (`§20` makes doing so a defect). Present these
as a bar to clear, not a list to pick from:

| Role | The property (`§`) | What falls out, and why |
|---|---|---|
| Contract format | Maintained generators for every client language (`§4.1`) | Anything without a Swift or Kotlin generator, when mobile ships |
| Mail | Authenticated bounce/complaint feedback into a suppression list (`§8.1`) | Bare SMTP with no event channel — SMTP *plus* a feedback source conforms |
| Push | Device tokens never disclosed outside the `§10.4` register (`§8.3`) | Nothing. A push vendor is priced, not banned — it adds a register entry |
| Analytics | Non-essential events gated on server-side consent at an ingestion point you control (`§10.3`) | Any SDK reporting to a backend you don't control |

Users argue with the analytics property. It excludes Vercel Web Analytics,
Cloudflare Web Analytics, CloudWatch RUM, Pinpoint and GA, but on
**architecture, not brand**. An SDK that reports to a vendor backend cannot be
gated on consent state that the backend never sees. A vendor that offers
consent-gated ingestion under your control passes the clause. Say it that way:
"not allowed" invites a fight, and "here is the bar" does not.

State the consequence too. With first-party collection, `§14`'s field-vitals
budgets need `web-vitals` reporting to your own endpoint, which is real work.

## Phase 4 — Announce the derived decisions

Do not ask these. Compute and state them:

| Derived | From | Source |
|---|---|---|
| Queue substrate | `db_engine` | `tech/data.yaml` → `queue_derivation` |
| Data access + migrations | `language` + `db_engine` | `tech/data.yaml` → engine `data_access` |
| Package manager, task runner, lint, test, boundary check | `language` | `tech/languages.yaml` → `derives` |

**Explain the queue derivation, do not just state it.** If the engine supports
transactional enqueue, the queue is a table in the product's own datastore and
enqueue happens inside the business transaction. If it does not, an outbox with a
relay is mandatory, and that is a `§18` item 14 capability gap.

Say what is counter-intuitive: **an external queue is not an upgrade.** Where the
engine supports transactional enqueue, moving the queue out *adds* a
sub-processor and brings back the dual-write problem that the outbox then has to
solve.

## Phase 5 — Consequence review

Show the complete stack on one screen. Then run the validator:

```
python3 assets/check_stack.py --selection <selections.yaml>
```

It reports **errors** (combinations that cannot be built) and **warnings**
(capability gaps that `STACKSPEC` requires to be recorded). Do not skip it
because the reasoning "already checked". A wizard that reasons its way to "Go on
Vercel" in a long session is the failure the script exists to make
impossible.

For each warning, capture a one-line reason and the compensating control. These
become `§18` item 14. Pushback rules, from `roles.yaml`:

| Situation | Action |
|---|---|
| Hard conflict | Block. Offer the nearest working alternative. |
| Weakens an invariant | Explain, capture a reason, record it |
| Ordinary tradeoff | State it once, proceed. No ceremony. |

## Phase 6 — Provisioning ledger

For every external service in the stack, ask three things: *do you have an
account?* → *do you have the dev credential?* → *should I provision it now?*

Three outcomes per row: **have it**, **provision now**, **defer with a
placeholder and a TODO**.

**Dev is automatic, production is manual.** This split is deliberate:

- **Dev / preview** — provision freely where a CLI exists (`neonctl projects
  create`, `wrangler r2 bucket create`, `supabase projects create`, `fly secrets
  set`, …). Write values to a git-ignored `.env.local`.
- **Production** — generate the exact commands and have the **user** run them via
  the `!` prefix, so production secrets never enter the transcript. If a value is
  read into a tool call it lands in conversation history and possibly in logs.

Four rules for this phase:

1. **Never write a production secret to the repo, and never echo one into the
   transcript.** `.env.example` gets key names and descriptions only (`§15`).
2. **Verify, don't assume.** After each credential, smoke-test it: a trivial
   query, a cache ping, an upload-then-delete, a send to a sink. A wrong-but-
   present credential fails at 2am instead of now.
3. **Three tiers, so it is a matrix** (`§15`). Dev, staging, production, with
   separate credentials. A single list invites sharing one.
4. **Resumable.** Write the ledger to the Stack Profile (`docs/architecture/stack-profile.md`, else the old `docs/specs/stack-profile.md`) item 6 with
   statuses only, never values, so a later run picks up the deferred rows.

Generate `.env.example`, the config-validation schema (`§15`'s "one schema,
validated at startup") and the CI secret list **from the ledger**, so the three
cannot drift.

## Phase 7 — Generate

Build in dependency order. Each step is a precondition of the next:

| Step | Owner |
|---|---|
| 1. Repository skeleton, workspace, CI, hooks, secret scanning, branch gate and delivery scripts — copy the hooks, linters and guards from `assets/tooling/shared/` and `assets/tooling/<track>/` (see below); the CI and delivery files come from `luismc-delivery`'s installer (see below) | this skill and `luismc-delivery` |
| 2. `core`, then the data module with initial schema and migration runner | this skill |
| 3. `contract` — the OpenAPI document and generators | this skill |
| 4. *(auth)* | **`auth-setup`** — skip entirely |
| 5. `apps/api` — skeleton, health route, error envelope, route-coverage test **harness**, non-auth routes only | split |
| 6. `jobs` + `apps/worker` with `§7.4`'s required job set | this skill |
| 7. Adapters: `mail`, `storage`, `notify`, `observability` | this skill |
| 8. `tokens` and the UI module | this skill |
| 9. `apps/web`, `apps/admin` | this skill |
| 10. `apps/ios`, `apps/android` — whenever wanted | this skill |
| 11. Stack Profile, runbooks, conformance run | this skill |

### Step 1 in detail — what is copied where

Paths and owners are fixed by `CONTRACT.md` in `luismc-delivery` (`templates/shared/scripts/delivery/CONTRACT.md`).
This skill carries no CI logic. It picks technologies and copies the hooks, linters and guards below. At the end of step 1 it calls the delivery installer, which writes the delivery scripts, the workflow files and the per-track `gate.json` and `smoke.json`:

`python3 <luismc-delivery>/scripts/delivery_ci_install.py install --track <track> --root .`

Do it in the first commit, so the first branch is already gated:

| Into the repository | From `assets/tooling/` | Clause |
|---|---|---|
| `scripts/delivery/*`, `.github/workflows/*`, `scripts/delivery/gate.json`, `smoke.json` | the delivery installer (`luismc-delivery`, `templates/`). Afterwards set `default_branch` in `gate.json` to the repo's own and `ui_paths` to the apps that exist. `CONTRACT.md` is not copied. | `§13.5`, `§13.6`, `§13.1`, `§11.2` |
| `e2e/quarantine.json` (TypeScript track only) | `ts/e2e/quarantine.json` | `§11.2` |
| `.githooks/pre-push` | `shared/.githooks/pre-push`, beside `pre-commit` | `§13.5` |
| `.githooks/commit-msg` | `shared/.githooks/commit-msg`, beside `pre-commit`; does nothing unless `.delivery/config.json` sets `no_attribution: true` (DL-74). `pre-commit` also refuses staged conflict markers (DL-24) | DELIVERYSPEC |
| `.gitattributes` | `shared/.gitattributes` — LF for shell scripts, hooks and the delivery scripts, so a CRLF checkout cannot break them | `§13.5` |
| the guard-test starter, TypeScript | `ts/guards/*.guard.test.ts` and `ts/vitest.config.ts` (its `guard` project) | `§13.5` item 4 |
| the guard-test starter, Go | `go/guards/` (`TestGuard*`) | `§13.5` item 4 |
| the guard-test starter, Rust | `rust/crates/guards/` — a member crate (`guard_*` tests); add `crates/guards` to the workspace `members` in the root `Cargo.toml` | `§13.5` item 4 |
| the guard-test starter, .NET | `dotnet/tests/Guards/` (`Category=Guard`); add `Guards.csproj` to the solution and match its `TargetFramework` to `global.json` | `§13.5` item 4 |
| a `.gitignore` line `.delivery/` | no asset: append it to the generated `.gitignore` | `§13.5` |

Turn on the repository setting that deletes a merged pull request's head
branch, so the platform does its part of the `§13.6` cleanup:
`gh api -X PATCH repos/{owner}/{repo} -F delete_branch_on_merge=true`. It is a
repository setting the user owns: ask before changing it on an existing
repository.

If the product adds a workflow that uploads a build artifact (an installer such
as an MSI, a bundle, a report), give each kind a stable name, with no version,
run number or commit in it. Add the workflow to `artifact-prune.yml`'s
`workflows:` list (`§13.1`).

**CI option, per OS (DL15).** Ask the owner where CI runs, once for each OS the product tests on (linux, windows, macos). There is no default and no assumed answer. The choices are (a) GitHub self-hosted runners, (b) GitHub-hosted runners, (c) Claude cloud sessions. Record each answer with `python3 <luismc-delivery>/scripts/delivery_ci.py set --os <os> --option a|b|c`, then run `delivery_doctor.py` and fix what its `ci` check reports. The owner changes the choice later with the same command. Everything about the options (shard table, runners, cloud sessions, statuses) is in `luismc-delivery`.

**Runners (`§13.1`).** For option (a) or (b): ask whether CI runs on hosted or self-hosted runners.
Every workflow template reads its runner labels from the repository variable
`CI_RUNS_ON` (a JSON string or list; unset means `ubuntu-latest`). For
self-hosted or shared runners, set it and turn on one-at-a-time ready-PR CI
(`§13.6`): `gh variable set CI_RUNS_ON --body '["self-hosted","linux"]'` and
`gh variable set CI_SERIAL --body true`. These are repository settings the user
owns: ask before changing them on an existing repository.

Warn against requiring a label that only one runner carries (`gh api
repos/{owner}/{repo}/actions/runners` lists them when the user has admin rights; else ask):
if that runner is offline, every job waits. Suggest a second runner with the label, or a
fallback job on hosted labels. Warn; never block. `join.py` and `ci_watch.py` warn at
run time when no online runner carries a job's labels (`§13.6`).

**Splitting the dominant CI job (`§13.1`, SHOULD).** The ts template already runs the
browser suite as two Playwright shards behind the unchanged `web E2E (§11.2)` check (one
`shard:` list sets the count). For any track, once CI has run, read the slowest-job summary
that `ci_watch.py` prints. If one job or test step takes most of the run, give it its own job
or shards. Leave small steps together, because every job repeats setup.

**End-to-end selection (`§13.5`).** When the product has more than a handful of
end-to-end specs, add an `e2e_map` to `gate.json` (specs to source paths, plus
`full_on` for shared configuration and the API contract), so a branch gate runs
only the affected specs. Without a map the gate runs them all.

**Change notes (`§13.6`).** Create `docs/specs/changes/` with a short README.
Branches add a note per spec change instead of editing a spec's version line
or change log. `scripts/delivery/change_notes.py fold` applies them on the
release branch. The `change-notes` gate step enforces it. If the product's
specs number their change-log headings, set `changelog_headings` in
`gate.json`.

Install the pre-push hook so a project's existing check survives:

- Find the existing pre-push hook: in `.githooks/`, in the directory `core.hooksPath` points to, or `.git/hooks/pre-push` when `core.hooksPath` is unset.
- If it differs from the template, move it to `pre-push.local` in that hooks directory before copying the template; never overwrite it.
- The template runs `pre-push.local` after its own guards pass, with the same arguments and stdin, and fails the push if it fails.
- If `core.hooksPath` already points at another directory (for example `.husky`), install both hooks into that directory; do not change `core.hooksPath`.
- If `core.hooksPath` is unset, copy into `.githooks/` and set it: `git config core.hooksPath .githooks`; say so in the repo's setup notes.

Mark
`agent_setup.sh` and the hooks (`pre-push`, `commit-msg`) executable (`git update-index --chmod=+x`). Otherwise a
checkout on another machine cannot run them. Copy `.gitattributes` before the
first commit, so those files are never stored with CRLF. If the repo already has
one, append the four lines. Do not replace it.

**`scripts/delivery/agent_setup.sh` is the first step for any cloud agent.** It
installs Python 3.11+ if missing, the scanners pinned in `tools.json` (the version
CI installs, so the gate runs the scanner CI runs) and `gate.json`'s `setup`
commands. It is idempotent. Put one line in the repo's agent instructions:
run it before the first gate.

Do not write the delivery scripts yourself. Do not edit them in the
generated repo to fit a product. They belong to the plugin and are versioned
with `STACKSPEC`. Product differences belong in `gate.json`.

**Hosting.** A change that touches only `docs/` has nothing to deploy, so
configure the host to skip it, using whatever the host offers for deciding
whether to build (an ignored-build-step command, a path filter). For example, a
host that runs a command and skips the build on exit 0 can be given
`git diff --quiet HEAD^ HEAD -- . ':!docs'`. This is a hosting setting, not a
repository file; record it in the Stack Profile's environment inventory.

**Delivery log (`§13.6`).** The deploy job, after its production smoke test,
runs `python3 scripts/delivery/delivery_log.py live --pr <N>` (the merged PR
number) with `contents: write`, so the train's release notes record when each
change went live. A failure there warns and never fails the deploy.

**Packaged programs (`§13.7`, a `MUST`).** A product that ships a packaged
program (single executable, installer, app bundle, container image) declares
its start command and every worker's readiness line in
`scripts/delivery/smoke.json`; the track's `package.yml` builds the packaged
form and runs `scripts/delivery/smoke_packaged.py` on it. An empty `start` means
the product ships no packaged program.

### The seam is at steps 4 and 5 — do not paper over it

- **Step 4 is entirely `auth-setup`'s.** Do not create the auth module, not even
  an empty one with a README. An empty auth package makes `auth-setup`'s
  preflight see a requirement as met when it is not.
- **Step 5 splits.** Create the API app, its bootstrap, its health route, its
  error envelope and the `§11.1` route-coverage test **harness**. Leave the auth
  endpoints out. The coverage test over zero auth routes is correct here. It
  starts to fail, usefully, as soon as `auth-setup` adds routes without
  declarations.
- **Step 7's mail adapter is a dependency of auth**, not of it. Build it here;
  `auth-setup` wires notifications into it.
- **Step 6's job set** is `§7.4`'s. `AUTHSPEC`'s pruners belong to `auth-setup`,
  which adds them to the same jobs module.

**Do not create modules speculatively.** `§2.1`: a shared module MUST NOT exist
before it has a second consumer or a clear adapter role. Generating eleven
packages for a product with one app is a defect.

## Phase 8 — Verify and report

Run Mode 2 against what you generated. A generation that has not been checked is
not finished. Expect and ignore auth-shaped absences. They are the declared gap,
not findings. Also run the branch gate once (`python3 scripts/delivery/branch_gate.py
--no-publish`) so the first result is a real one. Fix `gate.json` if a step
cannot run.

Report: what was generated · what was deferred and why · every profile field the
user still has to fill · every open ledger row · the Mode 2 findings.

## Phase 9 — Ask about authentication

Authentication is absent by design. Say so plainly, then **ask**:

> The stack is set up and authentication is not part of it. `auth-setup` builds
> `packages/auth` against `AUTHSPEC`, a separate binding spec. Want to run it
> now, or later?

**Do not start it without an answer**, and do not treat an earlier "set up the
whole thing" as that answer. Two binding specs in one unreviewable pass is the
failure this split exists to prevent. If the user says later, say what to run and
stop.

---

# Mode 2 — Check conformance

`STACKSPEC §19` is the checklist. Until a script implements it, this mode is that
check, performed by reading.

1. **Find the declared standard.** Read `docs/architecture/stack-profile.md`, or the old `docs/specs/stack-profile.md` when the repo has not moved it (say so in the audit: moving it is a finding). Note the
   `STACKSPEC` version it claims. If it is behind the version in `references/`,
   say so first. Every finding is relative to the version the product claims.
   The difference between versions is itself a finding.

   A profile claiming **5.x** (5.2.0 and earlier) predates `STACKSPEC` 6.0.0's
   four new `MUST`s, listed in the spec's `§0.1` 6.0.0 entry: the `§11.2` E2E
   gate, the `§13.1` default-branch skip, the `§13.5` branch gate and pre-push
   hook, and the `§13.6` integration flow. Report the product as conforming to
   its claimed version and list each of the four as an upgrade item. Upgrading is
   the repair pass in step 7 plus a profile edit: change the claimed version to
   6.0.0 only after the re-check passes, never before.

   A profile claiming **7.x** predates `STACKSPEC` 8.0.0's one new `MUST`,
   `§13.7`: a product that ships a packaged program has CI start the packaged
   form and exercise every worker it starts (`smoke.json` plus a `package.yml`
   job). List it as an upgrade item only for such a product. A product that
   ships none conforms to 8.0.0 as it stands. Offer the 8.0.0 improvements as
   suggestions: `inert_paths` and `lockfile_scope` in `gate.json`, the light join
   check, the train freeze in pre-push, runner-health warnings, path-filtered
   build-artifact workflows and the delivery log in release notes.

   A profile claiming **7.0.x** conforms to 7.1.0 as it stands (7.1.0 adds no
   `MUST`). Offer the 7.1.0 improvements as suggestions, not findings: the
   current delivery scripts (the gate fetches its base, pre-push compares with
   the fork point, pinned scanner checksums, the default-branch skip for
   ignored paths), runner labels as a setting, an `e2e_map`, change notes, and
   one-at-a-time ready-PR CI on shared runners.

   A profile claiming **6.x** predates `STACKSPEC` 7.0.0's new `MUST`s, listed
   in the spec's `§0.1` 7.0.0 entry: `§13.1` keeps only the newest build
   artifact of each name, the `§13.5` gate installs from the lockfile in frozen
   mode first, stops at the first failure and has a time limit, and `§13.6`
   removes a merged train automatically. Report each as an upgrade item, the
   same way; the repair is copying the current delivery scripts, the two new
   workflows and the setting above.

   A profile claiming **4.x or earlier** predates the technology-neutral split.
   Report that its technology clauses no longer exist as requirements, and that
   its recorded vendor deviations are now `CHOICE`s needing recording, not
   approval. That conversion is the main finding for such a product.

   Check the profile's `AUTHSPEC` version too, but do not audit auth here.
   Report only whether the product claims one.

2. **If there is no profile, that is finding number one.** `§16` and `§18` make
   it mandatory. Without it there is no declared engine, no RPO/RTO, no pinning
   decision, no capability-gap record and no deviation record. So most clauses
   cannot be evaluated. Report it and continue with what is checkable.

3. **Work `§19`'s checklist**, section by section: Repository and layering ·
   Contract · Data · Jobs and integrations · Caching · Clients · Observability ·
   Testing and CI · Configuration and compliance. For each item resolve one of:
   **conforms**, **violates**, **absent**, **not applicable** (with the reason).
   Cite file and line for every violation. A finding without a location is not
   actionable.

4. **Check the structural gates specifically.** These fail silently when absent:
   - layer-boundary check (`§3.2`) and the adapter rule (`§3.3`) — every vendor
     SDK confined to one module
   - route-coverage test exists and runs (`§11.1`) — authorization *and*
     rate-limit declarations. Whether the *auth* routes declare authorization is
     `auth-setup`'s finding, not this skill's
   - contract drift: all generated clients regenerated and committed (`§4.1`)
   - a test suite finding zero tests fails rather than passes (`§11.3`)
   - secret scan covers full history (`§12`)
   - CI cost (`SHOULD`, `§13.1`'s CI-cost clause) — drift findings at `SHOULD`
     severity, so each needs a recorded reason or it is a violation (step 5):
     a separate secret-scan job where a step in another job would do; the
     gitleaks step without `pull-requests: read` (it 403s on a PR before
     scanning); `cancel-in-progress: true` that also applies to the default
     branch; no draft-PR skip; no task-runner result cache
   - field classification, retention declaration, export inclusion (`§5.7`)
   - data-collection inventory vs. generated artifacts (`§9.7`)
   - **E2E gate (`§11.2`)** — the web E2E job runs on ready pull requests and is
     not advisory (no `continue-on-error`, and it is a required check); a
     committed quarantine file exists (`e2e/quarantine.json` on the TS track),
     each entry with an owner, a date and a reason; quarantined specs run in a
     separate non-blocking step; nothing retries a spec until green
   - **Default-branch skip (`§13.1`)** — a `decide` job runs first on a push to
     the default branch, every other job needs it and runs unless it says skip,
     `ci_skip_check.py` is present, and a skipped or failed `decide` still runs
     the suite. Default-branch runs are never cancelled
   - **Branch gate (`§13.5`)** — `scripts/delivery/` holds the gate scripts;
     `gate.json` parses and its steps cover typecheck, lint, unit, guards (scope
     `always`), secret scan and E2E (scope `ui-changed`), with `widen_on` naming
     the lockfile, the task-runner config and the CI workflows; a guard-test
     suite exists and is selected by the track's convention; `.githooks/pre-push`
     exists in the hooks directory `core.hooksPath` points at (`.githooks` unless
     the project already used another), and any earlier pre-push hook it
     replaced is kept as `pre-push.local` beside it; `agent_setup.sh` installs
     the scanner at the version in `tools.json`, and CI installs that same
     version; `.delivery/` is git-ignored; `.gitattributes` forces LF on `*.sh`,
     `.githooks/*` and `scripts/delivery/*.py`, so the hooks run on every OS
     (a CRLF shebang line fails on Linux and macOS). The guard starter is
     registered: the Rust `crates/guards` is in the workspace `members`, the
     .NET `tests/Guards` project is in the solution. `gate.json`'s `setup`
     installs in frozen or locked mode, and its `timeout_minutes`, when set, is
     a positive integer. A branch result that is not tied to the current head
     and base is not a result
   - **Build artifacts (`§13.1`)** — `artifact-prune.yml` is present and its
     `workflows:` list names every workflow that uploads an artifact; every
     `upload-artifact` name is stable for its kind (no version, run number or
     commit in it)
   - **Train cleanup (`§13.6`)** — `train-cleanup.yml` and
     `scripts/delivery/cleanup.py` are present; the repository setting
     `delete_branch_on_merge` is on (`gh api repos/{owner}/{repo} --jq
     .delete_branch_on_merge`)
   - **Integration flow (`§13.6`)** — advisory, because it is process: read the
     repo's rules and agent instructions for task-ID branches, draft pull
     requests into an integration branch, the merge script, one ready pull
     request, and CI watched by commit with no auto-merge. Report documented or
     not documented; do not infer a violation from the absence of a file

5. **Classify divergence correctly.** This is where Mode 2 most often produces
   false positives, and 5.x changed the rules:

   | Kind | Test | Verdict |
   |---|---|---|
   | `MUST` violated | No waiver in the profile | **violation** |
   | `MUST` waived | Reason + named approver recorded | conforming |
   | `SHOULD` not followed | Reason + named approver recorded | conforming |
   | `SHOULD` not followed | Not recorded | **violation** |
   | `CHOICE` | Recorded in profile item 2 | **conforming — always** |
   | `CHOICE` | Not recorded | **unrecorded**, not a violation |
   | Capability gap | Compensating control in item 14 | conforming |
   | Capability gap | No control recorded | **violation** |

   **A vendor is never a violation.** Postgres vs. MySQL, Sentry vs. Bugsnag,
   Neon vs. RDS, Drizzle vs. Prisma, Vercel vs. Fly — all `CHOICE`s. The only
   question is whether the profile records them. Do not import 4.x's graded
   `SHOULD`s for Neon, Upstash or Vercel Blob; they no longer exist.

   **The tools are also never a violation.** `§13.1` requires twelve gates to run
   and fail the build. It names no tool. A repo on Biome instead of ESLint, or
   `go test` instead of Vitest, conforms perfectly.

6. **Report severity-ranked findings, grouped by section. Edit nothing while
   surveying.** A check that repairs as it goes cannot show you what the repo
   looked like.

7. **Then offer to fix the mechanical findings — opt-in, never automatic.** Some
   violations are decisions (a missing RPO, a layering breach needing code
   moved). Others are absent files this plugin carries. Offer the second kind,
   listed explicitly, as one confirmation:

   - `.gitleaks.toml`, pre-commit hook missing → `§12` secret scanning
   - CI workflow missing or short of `§13.1`'s twelve gates, or drifting from
     its CI-cost clause (the `SHOULD` findings from step 4)
   - boundary-check config missing → `§3.2` has no enforcement, so the layer
     rules decay by default
   - lint, format, test and task-runner configs missing
   - `scripts/delivery/`, `gate.json`, `tools.json` or `.githooks/pre-push`
     missing → `§13.5`; the `.delivery/` line missing from `.gitignore`;
     `.gitattributes` missing or not forcing LF on the hooks and scripts
   - `ci.yml` without the `decide` job or its job conditions → `§13.1`; E2E
     advisory or `e2e/quarantine.json` missing → `§11.2`
   - `artifact-prune.yml` missing, or an upload with a per-run name → `§13.1`;
     `train-cleanup.yml` or `cleanup.py` missing → `§13.6`

   Copy the hooks and guards from `assets/tooling/`, and the delivery assets with
   `delivery_ci_install.py update` (paths per `CONTRACT.md` in `luismc-delivery`), keep the repo's own
   `default_branch` in `gate.json`, and leave the `§13.6` documentation to the
   user: offer to draft the text for the repo's rules file, as a diff.

   Rules for the repair pass:

   - **Diff before replacing.** If the file exists but differs, show the diff and
     ask. An existing CI workflow may carry project-specific jobs that a blind
     overwrite destroys. Generation and repair MUST NOT touch those jobs, only
     the gates and CI-cost settings the template owns. An existing
     `.gitleaks.toml` may carry allowlist entries added for real false positives.
   - **Never touch a conforming file**, even if it differs from the template. The
     template is one way to satisfy a clause, not the only one.
   - **Re-run the check afterwards.** A repair that was not re-verified is a
     claim, not a fix.
   - If the user declines, leave everything untouched and say which findings
     remain open.

---

# The catalog

`assets/catalog/` is the compatibility model. It is data, not requirements.
Nothing in it is graded.

| File | Holds |
|---|---|
| `roles.yaml` | The slots, which are asked vs. derived vs. fixed, the Phase 1 profile questions, the two entry orders, the pushback rules |
| `tech/languages.yaml` | The four tracks, their per-track derived foundation, hosting scores |
| `tech/frameworks.yaml` | Web and API frameworks by track; the rich vs. server-rendered distinction |
| `tech/hosting.yaml` | Compute platforms, language scores, VPC and cold-start implications, spec exclusions |
| `tech/data.yaml` | Engines, hosts, the capability matrix, and the queue derivation |
| `tech/services.yaml` | Cache, object storage, mail, error tracking, uptime |
| `bundles.yaml` | Pre-pinned coherent stacks, plus the anti-combinations to block or warn on |

Two habits when using it:

- **`say_out_loud` blocks are not optional.** They exist because the consequence
  is invisible at selection time and expensive later. Read them to the user.
- **Run `check_stack.py --catalog` after editing any of it.** It verifies that the
  files agree with each other: framework tracks name real languages, hosts
  name real engines, every engine answers every declared capability, and bundle
  selections reference technologies that exist.

## Keeping the catalog honest

The catalog carries claims about the world: Workers have no raw TCP, D1 lacks
interactive transactions, PlanetScale discouraged foreign keys. These go stale.
When a recommendation depends on a claim and you are not current on it, say so.
Do not assert it. Verify it before blocking a user's choice on it.

## The tooling assets

`assets/tooling/<track>/` holds working implementations of `§13.1`'s twelve
gates, one set per track. Copy in Phase 7 step 1, before any module exists, so
the first commit is already gated. `luismc-delivery`'s `templates/shared/scripts/delivery/`
holds the track-independent delivery scripts (branch gate, verifier, pre-push
guards, merge script, CI watcher, default-branch skip check, agent setup), and
its `CONTRACT.md` is the one place their paths, exit codes and file formats are
defined.

Three properties every track's templates must preserve. They exist so that an
absent check cannot pass for a passing one:

- **A suite that finds no tests fails** (`§11.3`). A mis-globbed suite must not
  report green over zero tests.
- **The codegen drift check regenerates then diffs**, so a stale committed
  artifact cannot satisfy it.
- **The secret scan checks out full history.** At the default clone depth
  gitleaks silently examines one commit and reports clean. It is a step in the
  `verify` job, not a job of its own: a few-second job bills a full minute.

### The tool names are this generator's choice, not the spec's

`STACKSPEC §13.1` requires the twelve gates to run and fail the build. It names
no tool, and it must not start to. `§20` makes a new `MUST` a major version, and
defines naming a vendor anywhere in the spec as a defect.

So record the tools in `docs/architecture/stack-profile.md`, not here. In Mode 2 that
distinction is the difference between a finding and a false positive.

---

# Editing `STACKSPEC` itself

Not part of using this skill. The spec is maintained in the `dev-standards`
repository, which gates every edit with `tools/spec_check.py` and documents the
process in its README. A product never edits its copy, because it never has one.

Two governance rules worth knowing before proposing a change (`§20`):

- **A new `MUST` is a major version.**
- **Promoting a `CHOICE` to a `SHOULD` or `MUST` is a major version, and naming a
  vendor anywhere in the spec is a defect, not an edit.** Technology belongs in
  the catalog.
