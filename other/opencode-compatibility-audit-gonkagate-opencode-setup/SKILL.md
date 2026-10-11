---
name: opencode-compatibility-audit
description: "Read-only compatibility audit between `opencode-setup` and the latest stable `opencode-ai` release plus official OpenCode docs. Use whenever the task is to decide whether this repository still matches current OpenCode config, custom-provider, auth, model, or CLI contracts, or whether upstream OpenCode changed in a way that breaks our setup plan, even if the user only asks 'is this still compatible?' or 'did OpenCode upstream change?'."
---

# OpenCode Compatibility Audit

## Purpose

Use this skill to answer one practical question:
is `opencode-setup` still compatible with the current stable upstream OpenCode
contract or not?

This is a read-only compatibility gate. The job is to compare official
upstream OpenCode behavior against the assumptions encoded in this repository
and return a clear verdict, not to design or apply a migration.

## Scope

Cover the repository's current and planned OpenCode-facing contract,
especially:

- config location, merge order, and precedence assumptions for
  `~/.config/opencode/opencode.json`, `OPENCODE_CONFIG`, and project
  `opencode.json`
- project activation assumptions where user-level config owns
  `provider.gonkagate` and project scope writes only activation settings
- custom-provider wiring through `provider.<id>`, including custom provider
  `npm`, `name`, `options.baseURL`, `models`, `options.apiKey`, and
  `options.headers`
- model selection assumptions around `model`, `small_model`, `opencode models`,
  and `provider/model` identifiers
- auth strategy assumptions around `/connect`, `opencode providers login`,
  `~/.local/share/opencode/auth.json`, and the repository's decision not to use
  `auth.json` as its integration contract
- variable-substitution assumptions such as `{env:...}` and `{file:...}` for
  secret handling
- transport expectations such as `@ai-sdk/openai-compatible` for current
  `/v1/chat/completions` and `@ai-sdk/openai` for future `/v1/responses`
- workflow and CLI assumptions documented by this repository, such as
  `opencode`, `opencode run`, `opencode models`, and
  `opencode providers login`
- newly required settings, renamed fields, removed commands, or release-level
  behavior changes that would make the documented GonkaGate OpenCode plan stale
  or unsafe

Default compatibility target:

- latest stable `opencode-ai` release from the npm `latest` dist-tag

Secondary watch target:

- newer prerelease channels such as `next`, `alpha`, or `beta`, but only as an
  early-warning watchlist unless the user explicitly asks for prerelease
  compatibility

## Boundaries

Do not:

- modify repository code or docs
- broaden product scope beyond the current GonkaGate OpenCode contract
- propose `.env` writing, shell profile mutation, direct `auth.json` mutation,
  or runtime `/v1/models` discovery as the default integration path unless the
  user explicitly asks for a product change
- use secondary summaries when primary sources are available
- treat prerelease drift as a stable compatibility failure unless the user
  explicitly asked to audit prereleases
- turn the audit into an auto-remediation or full migration plan

## Primary-Source Discipline

Use primary sources only:

- npm registry metadata for `opencode-ai`
- official OpenCode docs, especially:
  - `https://opencode.ai/docs/config/`
  - `https://opencode.ai/docs/providers/`
  - `https://opencode.ai/docs/models/`
  - `https://opencode.ai/docs/cli/`
  - `https://opencode.ai/config.json`
- official repository URL, homepage, releases, and tagged source discovered
  from npm metadata for the matching stable version
- shipped package behavior or CLI help for the same stable version

Prefer this discovery order:

1. `npm view opencode-ai version dist-tags repository.url homepage --json`
2. official docs and config schema
3. official release notes or tagged source for the exact stable version
4. tagged upstream source or tests when docs are incomplete
5. isolated CLI help or read-only inspection when source and docs are still
   insufficient

Useful starting points:

- `npm view opencode-ai version dist-tags repository.url homepage --json`
- `curl -fsSL https://opencode.ai/config.json`
- `curl -fsSL https://opencode.ai/docs/config/`
- `curl -fsSL https://opencode.ai/docs/providers/`
- `npx -y opencode-ai@<version> --help`
- `npx -y opencode-ai@<version> models --help`
- `npx -y opencode-ai@<version> providers login --help`

If official docs and the shipped stable artifact disagree, trust the shipped
stable artifact, schema, or tagged source and call out documentation drift
explicitly.

## Safe Read-Only Execution

Keep the audit read-only.

- Prefer docs, schema, release notes, CLI help, source, and tests over running
  stateful commands.
- Never run upstream OpenCode commands against the user's real
  `~/.config/opencode`, `~/.local/share/opencode`, or project config.
- If you need CLI help or read-only behavior inspection, isolate it in a
  disposable temp directory and point `HOME`, `XDG_CONFIG_HOME`,
  `XDG_DATA_HOME`, `OPENCODE_CONFIG`, and any other relevant config roots at
  temp paths.
- Do not run login flows or commands that mutate real state.
- Treat isolated local execution as a last resort after docs, schema, release
  notes, and tagged source.

## Repository Surfaces To Compare

Start from the current repository contract surfaces:

- `README.md`
- `AGENTS.md`
- `docs/how-it-works.md`
- `docs/security.md`
- `docs/troubleshooting.md`
- `docs/specs/opencode-setup-prd/spec.md`
- `src/cli.ts`
- `package.json`
- `test/package-contract.test.ts`
- `test/docs-contract.test.ts`
- `test/skills-contract.test.ts`

Inspect local skills when they encode product assumptions that affect the
audit, especially:

- `.claude/skills/coding-prompt-normalizer/`
- `.agents/skills/coding-prompt-normalizer/`
- this compatibility-audit skill itself, if its assumptions look stale

If the repository later adds implementation modules, inspect those too instead
of stopping at docs. In particular, compare any future surfaces under:

- `src/install/`
- `src/constants/`
- config-writing modules
- provider or secret helpers
- model-registry generation
- runtime verification flows

## Upstream Evidence To Gather

For the target stable release, gather evidence for:

- the exact stable version, release tag if available, and publish date
- whether npm `latest` and the official homepage or repository links agree
- whether newer prerelease channels exist and whether they signal upcoming
  contract drift
- where OpenCode loads global config from and how project `opencode.json`
  overrides are discovered and merged
- the official shape of `provider.<id>`, custom provider `npm`, `name`,
  `options.baseURL`, `models`, `model`, and `small_model`
- whether custom-provider auth still relies on `/connect` or
  `opencode providers login` storage plus config, and whether `auth.json`
  remains an internal credential store detail rather than a stable integration
  contract
- whether current custom-provider guidance still recommends
  `@ai-sdk/openai-compatible` for `/v1/chat/completions` and `@ai-sdk/openai`
  for `/v1/responses`
- whether OpenCode added or removed CLI surfaces relevant to this repository's
  documented flow
- whether release notes mention changes to config precedence, custom providers,
  provider auth, project config loading, model loading, or command surfaces
- any newly required settings, schema migrations, or structural requirements
  that this repository does not currently satisfy

When searching source or docs, start with these literals:

- `~/.config/opencode/opencode.json`
- `opencode.json`
- `OPENCODE_CONFIG`
- `provider`
- `provider.gonkagate`
- `small_model`
- `@ai-sdk/openai-compatible`
- `@ai-sdk/openai`
- `chat_completions`
- `responses`
- `auth.json`
- `/connect`
- `opencode providers login`
- `opencode models`
- `opencode run`
- `{file:`
- `custom provider`

## Workflow

1. Identify the audit target.
   - Determine the latest stable `opencode-ai` release from npm metadata.
   - Confirm the matching repository URL and any stable release notes.
   - Note any newer prerelease channels from dist-tags, but keep them separate
     from the stable compatibility verdict unless the user asked for them.
2. Capture the upstream contract before judging compatibility.
   - Read official config, providers, models, and CLI docs.
   - Read the official config schema.
   - Read tagged source or tests when docs are vague, incomplete, or missing
     exact field or behavior details.
   - Use isolated CLI help only when docs and source still leave an important
     ambiguity.
3. Map the repository's assumptions.
   - Read `README.md`, `AGENTS.md`, and `docs/` first.
   - Then inspect `src/cli.ts`, `package.json`, tests, and any implementation
     surfaces that exist.
   - Keep current scaffold truthfulness separate from the planned future
     product contract.
4. Compare the critical seams one by one.
   - `Config locations and precedence`
     Compare upstream global and project config behavior against the repo's
     `~/.config/opencode/opencode.json`, `OPENCODE_CONFIG`, and
     `opencode.json` assumptions.
   - `Provider wiring`
     Compare upstream custom-provider expectations against the repo's planned
     `provider.gonkagate`, `baseURL`, `npm`, `models`, `model`, and
     `small_model` usage.
   - `Auth and secret handling`
     Compare upstream auth surfaces against the repo's planned use of
     user-managed secret files, `{file:...}` substitution, and refusal to use
     `auth.json` as a write target.
   - `Model and transport contract`
     Compare upstream model-loading and custom-provider transport guidance
     against the repo's curated-model and `chat_completions` today /
     `responses` later plan.
   - `Workflow and command surfaces`
     Compare upstream CLI surfaces and documented workflows against what this
     repo promises users today.
   - `Recent release drift`
     Compare the latest stable release notes, and optionally newer prerelease
     signals, against the repo's setup plan.
5. Classify the evidence.
   - Label each material point as:
     `confirmed upstream change`, `confirmed still compatible`,
     `confirmed repo-overstatement`, or `inferred risk`.
   - Keep observed upstream facts separate from your interpretation of impact.
6. Decide the verdict.
   - `compatible`
     No confirmed upstream stable change breaks the repository's current or
     planned OpenCode contract.
   - `compatible with caveats`
     No confirmed stable break yet, but there is meaningful ambiguity,
     documentation drift, prerelease warning, or repository overstatement that
     weakens confidence.
   - `incompatible`
     A confirmed upstream stable change conflicts with a required repository
     assumption or makes the documented GonkaGate OpenCode plan stale or
     unsafe.
7. Name the minimum follow-up.
   - Point to the exact repo surfaces that would need attention.
   - Keep this as `recommended fix areas`, not a redesign.

## Reasoning Discipline

- Separate confirmed upstream changes from inferred risk.
- Base the main verdict on the latest stable release, not on prereleases.
- Use prerelease channels only as an explicit watchlist unless the user asked
  for prerelease compatibility.
- If the repo docs are still compatible with upstream but the placeholder
  implementation is misleading, call that a repository truthfulness issue, not
  an upstream break.
- If the upstream docs are vague but the schema, release tag, or shipped stable
  behavior is clear, cite the shipped behavior and call out doc drift.
- Treat config precedence, custom providers, secret handling, and
  `small_model` behavior as high-sensitivity by default.
- Do not infer support for out-of-scope product changes that this repository
  explicitly rejects.

## Output

Load `references/report-template.md` before writing the final answer.

The report should:

- cite the exact stable version audited and its publish date
- link the primary sources used
- separate confirmed upstream changes from inferred risk
- separate stable-verdict impact from prerelease watchlist signals
- point to the exact repository surfaces that would break or need clarification
- include a short `recommended fix areas` section only when the verdict is
  `compatible with caveats` or `incompatible`

Keep the output short, decisive, and evidence-backed.
