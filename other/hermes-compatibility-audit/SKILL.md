---
name: hermes-compatibility-audit
description: "Read-only compatibility audit between `hermes-agent-setup` and the latest stable upstream `hermes-agent` release plus official Hermes docs. Use whenever the task is to decide whether this repository still matches current Hermes config, profile, custom-provider, auth, model, or CLI contracts, or whether upstream Hermes changed in a way that makes the current GonkaGate setup plan stale, unsafe, or overclaimed."
---

# Hermes Compatibility Audit

## Purpose

Use this skill to answer one practical question:
is `hermes-agent-setup` still compatible with the current stable upstream
`hermes-agent` contract or not?

This is a read-only compatibility gate. The job is to compare official
upstream Hermes behavior against the assumptions encoded in this repository and
return a clear verdict, not to design or apply a migration.

Treat the repository's current runtime baseline as a repository fact, not as
current upstream truth. Today the shipped helper targets latest-only
`hermes-agent` `v2026.5.16` / `v0.14.0` or newer; the historical PRD baseline
was `v2026.4.13` / `v0.9.0`, but that legacy baseline is no longer the
supported public runtime contract.

## Scope

Cover the repository's current and planned Hermes-facing contract, especially:

- config location, resolution, and precedence assumptions for
  `~/.hermes/config.yaml`, `~/.hermes/.env`, `HERMES_HOME`, profiles, and any
  official config-path or env-path surfaces
- custom-endpoint wiring through `providers.gonkagate`,
  `model.provider = gonkagate`, `model.default`, `key_env`,
  `transport`, `discover_models`, and old direct custom `model.*` cleanup
- model and provider selection assumptions around `hermes model`,
  `provider:model` syntax, curated model choice, and custom provider behavior
- auth and secret-handling assumptions around `OPENAI_API_KEY`, unsupported
  legacy endpoint env such as `OPENAI_BASE_URL`, `auth.json`, credential
  pools, and the repository's decision to keep secrets in `~/.hermes/.env`
  rather than `config.yaml`
- workflow and CLI assumptions documented by this repository, such as
  `hermes model`, `hermes config set`, `hermes config path`,
  `hermes config env-path`, `hermes setup`, `hermes doctor`, and profile
  selection behavior
- read-side conflict surfaces described by the PRD, including matching custom
  credential pools, `cron/jobs.json`, inherited process env, and managed-install
  or blocked-write behavior
- newly required settings, renamed fields, removed commands, or release-level
  behavior changes that would make the documented GonkaGate Hermes plan stale
  or unsafe

Default compatibility target:

- latest stable upstream `hermes-agent` release tag

Secondary watch target:

- newer prerelease or unreleased main-branch signals, but only as an
  early-warning watchlist unless the user explicitly asks for prerelease
  compatibility

## Boundaries

Do not:

- modify repository code or docs
- broaden product scope beyond the current GonkaGate Hermes contract
- treat the PRD's current release baseline as proof that latest upstream still
  matches it
- propose shell profile mutation, arbitrary custom base URLs, secret storage in
  `config.yaml`, or direct mutation of `auth.json` as the default integration
  path unless the user explicitly asks for a product change
- use secondary summaries when primary sources are available
- treat prerelease drift as a stable compatibility failure unless the user
  explicitly asked to audit prereleases
- turn the audit into an auto-remediation or full migration plan

## Primary-Source Discipline

Use primary sources only:

- official Hermes docs, especially:
  - `https://hermes-agent.nousresearch.com/docs/getting-started/installation/`
  - `https://hermes-agent.nousresearch.com/docs/user-guide/configuration/`
  - `https://hermes-agent.nousresearch.com/docs/integrations/providers/`
  - `https://hermes-agent.nousresearch.com/docs/reference/cli-commands/`
  - `https://hermes-agent.nousresearch.com/docs/reference/profile-commands/`
  - `https://hermes-agent.nousresearch.com/docs/user-guide/features/credential-pools/`
- official upstream release source for the exact stable tag, such as:
  - `https://github.com/NousResearch/hermes-agent/releases`
  - the matching tagged source under `https://github.com/NousResearch/hermes-agent`
- shipped stable source, tests, or CLI help for the same stable tag when docs
  are incomplete or ambiguous

Prefer this discovery order:

1. official latest stable release tag from GitHub releases
2. official Hermes docs for configuration, providers, CLI, profiles, and
   credential handling
3. tagged upstream source for the exact stable version
4. tagged source tests or code paths when docs are incomplete
5. isolated CLI help or read-only inspection when docs and source are still
   insufficient

Useful starting points:

- `https://github.com/NousResearch/hermes-agent/releases`
- `https://hermes-agent.nousresearch.com/docs/user-guide/configuration/`
- `https://hermes-agent.nousresearch.com/docs/integrations/providers/`
- `https://hermes-agent.nousresearch.com/docs/reference/cli-commands/`
- `https://hermes-agent.nousresearch.com/docs/reference/profile-commands/`

If official docs and the tagged stable source disagree, trust the tagged stable
source or shipped stable behavior and call out documentation drift explicitly.

## Safe Read-Only Execution

Keep the audit read-only.

- Prefer docs, release notes, tagged source, source tests, and CLI help over
  running stateful commands.
- Never run upstream Hermes commands against the user's real `~/.hermes`.
- If you need CLI help or read-only behavior inspection, isolate it in a
  disposable temp directory and point `HOME`, `HERMES_HOME`,
  `XDG_CONFIG_HOME`, `XDG_DATA_HOME`, and any other relevant config roots at
  temp paths.
- Do not run setup flows, login-like flows, or anything that mutates real
  state.
- Treat isolated local execution as a last resort after docs, release source,
  and tagged code inspection.

## Repository Surfaces To Compare

Start from the current repository contract surfaces:

- `README.md`
- `AGENTS.md`
- `docs/how-it-works.md`
- `docs/security.md`
- `docs/specs/hermes-agent-setup-prd/spec.md`
- `src/cli.ts`
- `src/constants/contract.ts`
- `package.json`
- `release-please-config.json`
- `test/cli.test.ts`
- `test/package-contract.test.ts`
- `test/docs-contract.test.ts`
- `test/skills-contract.test.ts`

Inspect local skills when they encode product assumptions that affect the
audit, especially:

- `.agents/skills/coding-prompt-normalizer/`
- this compatibility-audit skill itself, if its assumptions look stale

If the repository later adds implementation modules, inspect those too instead
of stopping at docs. In particular, compare any future surfaces under:

- `src/install/`
- `src/constants/`
- config-reading or config-writing modules
- secret-handling helpers
- model qualification artifacts
- runtime verification flows

## Upstream Evidence To Gather

For the target stable release, gather evidence for:

- the exact stable tag or version, matching release source, and publish date
- whether official docs and the stable release tag agree on configuration,
  profiles, provider wiring, and command surfaces
- where Hermes loads global config from and how `HERMES_HOME`, profiles, and
  any official config-path commands affect target resolution
- the official contract for named custom providers, `gonkagate`,
  `model.default`, `key_env`, `transport`, `discover_models`, and direct custom cleanup fields
- whether current Hermes guidance still routes secrets to `.env` and non-secret
  config to `config.yaml`
- whether unsupported legacy endpoint env such as `OPENAI_BASE_URL`,
  `OPENAI_API_KEY`, `auth.json`, credential pools, or `cron/jobs.json` remain
  active upstream surfaces that could affect the latest-only helper contract
- whether managed installs or blocked-write modes remain relevant to a local
  mutation helper
- whether Hermes added or removed CLI surfaces relevant to this repository's
  documented flow
- whether release notes or stable source mention changes to config precedence,
  provider wiring, profile semantics, auth handling, or command surfaces
- any newly required settings, schema migrations, or structural requirements
  that this repository does not currently satisfy

When searching source or docs, start with these literals:

- `~/.hermes/config.yaml`
- `~/.hermes/.env`
- `HERMES_HOME`
- `provider: custom`
- `gonkagate`
- `custom_providers`
- `OPENAI_API_KEY`
- `OPENAI_BASE_URL`
- `auth.json`
- `cron/jobs.json`
- `credential_pool`
- `hermes model`
- `hermes config set`
- `hermes config path`
- `hermes config env-path`
- `hermes setup`
- `hermes doctor`
- `profile`
- `base_url`
- `transport`
- `discover_models`

## Workflow

1. Identify the audit target.
   - Determine the latest stable upstream `hermes-agent` release tag from the
     official releases page.
   - Confirm the matching repository source for that stable tag.
   - Note any prerelease or main-branch signals separately, but keep them out
     of the stable verdict unless the user asked for them.
2. Capture the upstream contract before judging compatibility.
   - Read official configuration, providers, CLI, profile, and credential docs.
   - Read tagged source when docs are vague, incomplete, or omit exact field or
     command behavior.
   - Use isolated CLI help only when docs and source still leave an important
     ambiguity.
3. Map the repository's assumptions.
   - Read `README.md`, `AGENTS.md`, and `docs/` first.
   - Then inspect `src/cli.ts`, `src/constants/contract.ts`, release config,
     tests, and any implementation surfaces that exist.
   - Keep current shipped-runtime truthfulness separate from broader future
     product changes.
4. Compare the critical seams one by one.
   - `Config locations and precedence`
     Compare upstream config and env behavior against the repo's
     `~/.hermes/config.yaml`, `~/.hermes/.env`, and secret-boundary
     assumptions.
   - `Profile and home resolution`
     Compare upstream `HERMES_HOME`, profile, and path-resolution behavior
     against the repo's target-home assumptions.
   - `Provider wiring`
     Compare upstream custom-provider expectations against the repo's planned
     `gonkagate`, canonical base URL, and named-provider usage.
   - `Auth and conflict surfaces`
     Compare upstream auth and env behavior against the repo's planned use of
     `.env`, `OPENAI_API_KEY`, `OPENAI_BASE_URL`, `auth.json`, credential
     pools, and `cron/jobs.json` detection.
   - `Workflow and command surfaces`
     Compare upstream CLI surfaces and workflows against what this repo
     promises users today.
   - `Managed installs and write-path safety`
     Compare upstream blocked-write or managed-mode behavior against the repo's
     planned fail-fast assumptions.
   - `Recent release drift`
     Compare the latest stable release notes and stable source against the
     repo's setup plan.
5. Classify the evidence.
   - Label each material point as:
     `confirmed upstream change`, `confirmed still compatible`,
     `confirmed repo-overstatement`, or `inferred risk`.
   - Keep observed upstream facts separate from your interpretation of impact.
6. Decide the verdict.
   - `compatible`
     No confirmed upstream stable change breaks the repository's current or
     planned Hermes contract.
   - `compatible with caveats`
     No confirmed stable break yet, but there is meaningful ambiguity,
     documentation drift, or repository overstatement that weakens confidence.
   - `incompatible`
     A confirmed upstream stable change conflicts with a required repository
     assumption or makes the documented GonkaGate Hermes plan stale or unsafe.
7. Name the minimum follow-up.
   - Point to the exact repo surfaces that would need attention.
   - Keep this as `recommended fix areas`, not a redesign.

## Reasoning Discipline

- Separate confirmed upstream changes from inferred risk.
- Base the main verdict on the latest stable release, not on prerelease or
  main-branch signals.
- If the repo docs are still compatible with upstream but the repository
  overstates shipped behavior or qualification scope, call that a repository
  truthfulness issue, not an upstream break.
- If the upstream docs are vague but the tagged stable source or shipped stable
  behavior is clear, cite the stable source and call out doc drift.
- Treat config precedence, profile resolution, `OPENAI_BASE_URL`,
  shared `OPENAI_API_KEY`, `auth.json`, credential pools, `cron/jobs.json`, and
  managed-install behavior as high-sensitivity by default.
- Do not infer support for out-of-scope product changes that this repository
  explicitly rejects.

## Output

Load `references/report-template.md` before writing the final answer.

The report should:

- cite the exact stable Hermes release audited and its publish date
- link the primary sources used
- separate confirmed upstream changes from inferred risk
- separate stable-verdict impact from prerelease or main-branch watchlist
  signals
- point to the exact repository surfaces that would break or need clarification
- include a short `recommended fix areas` section only when the verdict is
  `compatible with caveats` or `incompatible`

Keep the output short, decisive, and evidence-backed.
