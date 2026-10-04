---
name: sflow-workflows
description: List, preview, transfer, duplicate governed workflows, or explicitly share inert Git-backed workflow drafts.
disable-model-invocation: true
argument-hint: "[list|author list|author where-used SKILL-ID|author preview WFD-ID|author submit WFD-ID --revision N|skills-recipe ID ...|simulate ID|export ...|import FILE|copy SOURCE TARGET ...]"

---
# Workflows and shared drafts

<!-- sflow-output-contract: deterministic-mutation -->
**Output contract:** Let the CLI validate and mutate state; preserve its exact result, warnings, publication status, artifacts, and next actions.
<!-- sflow-execution-boundary -->
**Boundary:** no Story required; cwd=opened Git root or verified `repositoryPath` from `singularity-flow workspace current --json`; refuse if neither resolves; never search `$HOME`/parents.

Run `singularity-flow workflow $ARGUMENTS`; default `list`.

Run `author` from opened root; only explicit `--repository-story-refs` may read other local roots.
`list|read|history|show|preview|catalog|where-used|op-status` is read-only; relay coverage/gaps.
`author where-used <SKILL-ID> --json` reads approved configuration; `--story <ID>` selects
one accepted local Story. Preserve exact ref/commit/revision selectors; never fetch or infer.
`--story-refs` selects local first-parent windows; `--repository-story-refs` selects up to
four explicit local roots. No provider scan, invented selectors, or repairs. Later pages need
the returned `--expected-source`; unavailable history never means empty usage.
Create/Save: user direction, operation ID, observed head, matching `--expected-authority`.
`--input @approved-starter/<ID>` reads the verified authority, not the app checkout.
Inert JSON only; no rebase, replay or deleted-draft recreation. Lost acknowledgement:
`author op-status <ID> --json`.
Headless `author submit <WFD-ID> --revision N` or `author delete` only hands off:
never supply receipts, answers or tokens. Direct terminal captures the human action.
Submit creates only an exact review proposal; no approval, activation or execution.

Install: preview first; no unconfirmed `--replace` or auto-commit.

BYO: `singularity-flow workflow skills-recipe <NEW-ID> --label <TEXT>
--phases <APPROVED-PHASE-IDS> --json`; requires `--planned-claims required
--clause-phases <CRITERIA> --claim-owners <CODE=PLAN>`. Never invent omissions or execution.
Proposals need separate authorization.

`singularity-flow workflow export --workflow <ID> [--workflow <ID>...] --out <FILE> --json`.
Relay complete dependency closure/locks; Policy/World Model prerequisites remain. Never edit bundles.

Import preview: `singularity-flow workflow import <FILE> --dry-run --propose --json`.
After digest/path/collision review and explicit acceptance run
`singularity-flow workflow import <FILE> --confirm <PLAN-SHA256> --propose --json` once.
Skill invocation is not confirmation. Never substitute digests, overwrite or retry stale destination plans.

`duplicate` aliases `copy`. Require a distinct lower-kebab target and label. Preview:
`singularity-flow workflow copy <[story|initiative:]SOURCE> <TARGET> --label <TEXT> --dry-run --propose --json`.
Qualify ambiguous IDs. Linked dependencies stay shared; later edits affect both. Review and wait:
`singularity-flow workflow copy <[story|initiative:]SOURCE> <TARGET> --label <TEXT> --confirm <PLAN-SHA256> --propose --json`.
Run once; never overwrite, bypass review, commit, activate, merge or refresh automatically.

On refusal, relay routes.
