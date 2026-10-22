---
name: repo-asset-stocktake
description: "Audit a repo's non-code assets (tool configs, CI workflows, runbooks, docs) for ones whose consumer is gone. Use when configs, workflows or runbooks may be dead."
compatibility: Developed and tested on Claude Code; portable to other Agent Skills-compatible agents.
license: MIT
metadata:
  author: shimo4228
  version: "1.0"
user-invocable: true
origin: shimo4228
---

# repo-asset-stocktake — Non-Code Asset Value Stocktake

Audit a project repository's **non-code assets** — configs, CI workflows, runbooks, and other files that tooling or humans consume — and assign each a holistic **Keep / Update / Retire / Merge** verdict. Evaluation is single-context and holistic; there is no runtime script and no numeric score.

> **Design note 1 — every asset has a consumer.** A non-code asset is not alive because it exists; it is alive because something *consumes* it — a tool invoked from a build script, a CI runner fired by an event, a human who reaches it through a link. When the consumer vanishes, or the asset stops serving the consumer it was written for, the asset becomes a review candidate. The config / workflow / runbook classes below are three **seed** consumer-classes, not the closed set — add a row whenever you meet a new consumer.

> **Design note 2 — two tiers, code then judgment.** Reachability is *structural* (decidable by grep/find) so tier-1 enumerates it as code. Value is *semantic* ("does this still mean anything?") so tier-2 leaves it to holistic LLM judgment. The deterministic scan narrows the gray zone, and the LLM judges only what survives. An asset can be perfectly reachable and still be dead (a workflow that fires but runs a no-op, a runbook that is linked but describes a retired process); tier-1 cannot see that, which is exactly why tier-2 exists.

## Modes (`$ARGUMENTS`)

`$ARGUMENTS` is `[full|changed] [REPO_DIR]` — mode first (default `full`), optional repo path (default the current working directory).

| Mode | When | Scope |
|---|---|---|
| `full` (default) | First audit, or a periodic sweep | Every non-code asset in REPO_DIR |
| `changed` | Re-audit after edits | Tier-1 over every asset; tier-2 over the changed set below |

**`changed` mode scoping.** Tier-1 reachability always runs over the full asset set — a reference edge breaks when a *referenced* target is deleted elsewhere, and the referencing asset's own mtime never changes, so an mtime filter would miss it. Tier-2 re-judges assets modified since the last `evaluated_at` **plus any asset whose reachability changed vs the prior ledger**. Carry a prior verdict forward **only** when its asset is both unmodified **and** reachability-unchanged — an asset whose reachability dropped to zero while its own file was untouched must be re-judged, never left a silent stale `Keep`. Find the modified set as described under the ledger section.

## Phase 1 — Inventory + tier-1 reachability

Enumerate assets, then measure each consumer's reachability with inline grep/find. **Detection is structural → code.** Use throwaway shell; do not bundle a script until the same scan demonstrably repeats across runs.

Exclude VCS, dependency, build, and cache trees from both enumeration and grep — `.git/`, `node_modules/`, `.pytest_cache/`, `vendor/`, `dist/`, `build/`, report/cache dirs. Assets there are vendored or generated, not authored, and pollute the inventory with false candidates.

Seed consumer-classes (extend as needed):

| Consumer class | Assets (glob) | Reachability check (inline) |
|---|---|---|
| **tool-invocation** | dotfile/tool configs — `.textlintrc*`, `.eslintrc*`, `.prettierrc*`, `.stylelintrc*`, `commitlint.config.*`, `.markdownlint*`, … | grep the tool's name across every invocation site — the `scripts` object of `package.json` (a name under `dependencies`/`devDependencies` proves the tool is *installed*, not *invoked* — do not count it), `.pre-commit-config.yaml`, `Makefile`/`justfile`, `.github/workflows/`, git hooks, **and wrapper / hook-manager configs that invoke other tools** (`lint-staged`, `husky` / `.husky/`, `lefthook`). A tool reached only through a wrapper (lint-staged → prettier) has no *direct* site, so treat **zero direct invocation sites as investigate, not orphan**, until the wrapper chains are ruled out. |
| **CI-trigger** | `.github/workflows/*.yml`, other CI configs | Per workflow — (a) do its **local** references still exist — `run:` script paths and `uses: ./…` local actions / local reusable workflows? (remote `uses: owner/repo@ref` actions are *external consumers*, not dead refs — do not exist-check them). (b) is any `on:` trigger reachable, or is it `if: false` / commented-out / permanently guarded? **All local refs dead or trigger unreachable → dead.** (Superseded-duplicate detection needs content/intent comparison — that is a semantic Merge judgment, handled in Phase 2 Stage 2, not here.) |
| **human-navigation** | `docs/**`, `*.md` runbooks, `RUNBOOK*`, `*/runbooks/*` | Build the inbound-link set. Markdown links are written relative to the *linking* file (`../runbooks/deploy.md`, `./deploy.md`), so a repo-root path grep misses most of them — match by **basename** (`grep -rn 'deploy\.md'`) and disambiguate only when two docs share a basename. Before orphaning, also check **non-Markdown navigation** (`mkdocs.yml`, Docusaurus/site sidebars, generated nav) and **exempt forge-surfaced entrypoints** (`README`, `CONTRIBUTING`, `SECURITY`, `CODE_OF_CONDUCT`, `LICENSE`, which GitHub shows directly). **Zero inbound links → orphaned only after** those consumers are ruled out. |
| _(extend)_ | issue/PR templates, `dependabot.yml` / `renovate.json`, `.editorconfig`, governance files, seed/fixture data consumed by non-code tooling | Define the consumer, then grep for its consumption edge. **Code-loaded data files are out of scope — that edge belongs to `refactor-clean`.** |

Count only *real* consumption edges — a mention in a comment, a changelog, or an old ADR does **not** keep an asset alive (it fools a naive "the name appears somewhere" grep into a false-alive verdict). References cross language boundaries (config→CI shell, doc→doc), so scope the grep to the whole repo, not one language's source tree.

Record per asset — its consumer class and a one-line reachability fact (e.g. "0 invocation sites", "referenced script `ci/build.sh` deleted", "3 inbound links").

## Phase 2 — Evaluation (fully inline, holistic)

Judge each asset in one context. No numeric score, no rubric, no aggregation into a grade.

### Stage 1 — binary screen (surface only the No answers)

For each asset ask, Yes/No:

- Is its consumer still present? (tool invoked / trigger reachable / at least one inbound link)
- Does its content still describe something that currently exists? (the process it documents / the check it configures / the job it runs is still real)
- Is it distinct from every other asset? (not a superseded duplicate)
- Would a reader who opened it today act on it correctly? (not misleading-because-stale)

An asset that answers Yes to all is a **Keep** — do not belabor it. Surface only the assets with a No.

### Stage 2 — verdict pressure-test (non-Keep only)

For each surfaced asset, ask 1–3 refutation questions before committing a verdict:

- *Retire candidate* — "Is there a consumer I failed to grep (a dynamic invocation, an external wiki link, a scheduled trigger)? If I delete this, what breaks?"
- *Update candidate* — "Is the asset itself wrong, or is only my reachability grep incomplete? Is the fix mechanical (repair the trigger, fix the ref) or a content rewrite?"
- *Merge candidate* — "Which surviving asset absorbs this one, and does the merge lose anything?" This is also where **superseded-duplicate workflows** are judged (two workflows whose steps/intent overlap) — it needs content comparison, so it belongs here, not in the tier-1 scan.

### Verdict meaning

| Verdict | Meaning | Action |
|---|---|---|
| **Keep** | Consumer live and content meaningful | none |
| **Update** | Consumer live but content stale or partly broken — refresh it, repair the trigger, fix the dead ref | mechanical fix inline (Phase 4); prose-heavy rewrites → hand to the user / a writing skill |
| **Retire** | Consumer gone or content vestigial — the asset no longer earns its place | soft-delete (Phase 4) |
| **Merge into [X]** | Superseded by / duplicate of another asset | consolidate into X, then retire this |

**Mandatory-surface rule.** Any asset whose tier-1 reachability is **zero** (0 invocation sites / all references dead / 0 inbound links) MUST be surfaced as at least a Retire candidate — reachability zero is never silently a Keep. **This is the opposite of `skill-stocktake`'s stance, deliberately:** there, zero *usage* never creates a candidate, because a skill can be valid and simply unfired. Here the measure is *reachability* — no invocation site, every reference dead — which is a structural fact about the repo, not a behavioural one about the model, so it does create a candidate.

Evaluate **origin-blind** — who wrote the asset, or how long it took, does not bear on whether it still earns its place.

## Phase 3 — Summary

One table, most-actionable first:

| Asset | Consumer | Reachability | Verdict | Reason |
|---|---|---|---|---|
| `.textlintrc` | tool-invocation | 0 invocation sites | Retire | textlint dropped from CI and package.json; config now inert |

Close with a one-line count — total assets, and how many Keep / Update / Retire / Merge — plus the delta since the previous audit if the ledger exists.

## Phase 4 — Consolidation

**Confirm one by one**. Walk the non-Keep candidates sequentially; show the evidence first, then ask `[y/n/skip]`. **Never batch the approval** — "Retire all 6? [y/n]" defeats the design. `skip` records the verdict without acting.

- **Retire** — soft-delete first, never an autonomous hard-delete. Rename to `<file>.disabled` or move to a repo-local trash; real deletion is a later, separate human step. Offer `adr-writer` when the retirement encodes a decision worth recording.
- **Update** — apply mechanical fixes inline after confirm (repair a broken `on:` trigger, fix a dead `uses:` / `run:` ref, delete a stale config key). Flag prose-heavy content rewrites (a runbook describing a changed process) for the user or a writing skill rather than guessing the new content.
- **Merge** — consolidate into the surviving asset, then soft-delete the absorbed one.

## Reason quality (required)

Every reason must stand alone — a reader who did not run the scan should understand *why* from the row. Cite the concrete reachability fact.

- ❌ Bad — "Retire — unused." / "Update — stale." (states the verdict, not the evidence)
- ✅ Good — "Retire — `.stylelintrc` names a tool absent from package.json, CI, and pre-commit since the CSS pipeline was removed; nothing invokes it."
- ✅ Good — "Update — `deploy.yml` still fires on push but its `run: ./scripts/release.sh` target was deleted; repair or point it at the new path."
- ✅ Good — "Merge — `ci-lint.yml` and `lint.yml` both run the same ruff/black steps on push; fold `ci-lint.yml` into `lint.yml` and retire it."
- ✅ Good — "Keep — `RUNBOOK.md` is linked from README and its rollback steps still match the current deploy job."

## Ledger — `.repo-asset-stocktake.json`

Persist verdicts so `changed` mode can carry them forward. Written inline via Read/Write — never a script. The ledger lives **inside the audited repo** at `REPO_DIR/.repo-asset-stocktake.json` (not under the skill folder) — one ledger per repo, so auditing multiple repos never clobbers a shared file and `changed` mode's `evaluated_at` is scoped to the repo it belongs to. Suggest adding it to the repo's ignore file if it should not be committed.

```json
{
  "evaluated_at": "2026-07-05T12:00:00Z",
  "repo": "<REPO_DIR>",
  "assets": [
    {
      "path": ".textlintrc",
      "consumer": "tool-invocation",
      "reachability": "0 invocation sites",
      "verdict": "Retire",
      "reason": "textlint absent from package.json/CI/pre-commit; config inert",
      "action": "pending | soft-deleted | skipped"
    }
  ]
}
```

`evaluated_at` is an ISO-8601 UTC stamp (`date -u +%Y-%m-%dT%H:%M:%SZ`). To find the modified set in `changed` mode, prefer git (`git diff --name-only` / `git log --since`) when the repo is version-controlled — clone/checkout reset mtimes, so `find -newermt` comparisons mislead in git-managed trees even though the flag itself works on BSD/macOS find — or parse `evaluated_at` and compare each asset's mtime in the agent's own logic.

## Related

- **`refactor-clean`** — its Non-Code Assets sweep covers **code-consumed** data (files a program loads by glob/registry); its test is *structural* — whether any consumption edge exists at all. This skill covers **non-code-consumed** assets (tool / CI / human consumers) and judges *semantic value* — an asset can have a live edge and still be dead (a workflow that fires but no-ops). Structural deadness → refactor-clean; diminished value → here.
- **`context-sync`** — audits the four documentation *roles* (CLAUDE.md / graph.jsonld / ADR / README) for placement overlap and freshness against code. Runbooks are the overlap zone — context-sync asks "is this doc in the right role and consistent with the code," this skill asks "does this doc still describe something that exists / earn its place at all."
- **`skill-stocktake` / `rules-stocktake`** — the same stocktake pattern over a different asset class (installed skills / always-loaded rules). This skill is their sibling for a project repo's non-code assets.
- **Your publish step** (the author's harness uses `harness-sync`) — syncs this `origin: shimo4228` skill to its public repo after edits.
