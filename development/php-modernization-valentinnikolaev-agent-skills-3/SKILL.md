---
name: php-modernization
description: Modernize PHP runtimes, types, or tooling with scoped previews and compatibility checks; not diff review.
---

<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# PHP Modernization

Modernize a bounded PHP project while preserving its declared behavior and supported consumers. This skill and its compatibility reference adapt and substantially rewrite Netresearch DTT GmbH's `php-modernization-skill` at commit `8df68546e8d9fa00e4530e9c26e73adcc3322834`. They are distributed under CC-BY-SA-4.0; see [LICENSE.netresearch-content](LICENSE.netresearch-content) and [NOTICE.netresearch](NOTICE.netresearch). Upstream scripts and automated fix loops are not bundled.

## Route precisely

- Use for an explicit PHP runtime upgrade, adoption of modern PHP features, or a PHP typing/static-analysis/refactoring-tool migration with a defined target.
- Use `code-review` to inspect an existing diff without edits, `code-simplification` for a local behavior-preserving cleanup, and `vet-dependency` when selecting a replacement package is the primary decision.
- Use `deprecation-and-migration` for live API, schema, or stored-data rollout. When a PHP upgrade touches such a contract, identify those transition gates separately rather than assuming runtime compatibility proves rollout safety.
- A request for assessment or a plan authorizes discovery and planning only. Apply local changes when implementation is requested; do not deploy, publish, commit, or run external mutations merely because a preview is ready.

## Discover before running tools

1. Read repository and path-scoped instructions; record status, requested paths, current behavior, and existing local/parallel changes. Preserve dirty files. Never reset, stash, or overwrite unrelated work to prepare a migration.
2. Establish current and target PHP versions, minimum supported runtime, extensions, application/library role, and deployment or consumer matrix from the request, Composer, and CI. Ask for an unresolved target instead of choosing the newest release.
3. Read Composer constraints, lock policy, platform emulation, autoloading, framework/ORM/test versions, baselines, and tool configuration as data. Do not include PHP config, install dependencies, or run lifecycle scripts merely to discover the project.
4. Inventory available project tools and documented narrow commands. Classify each planned command by what it executes, writes, downloads, or contacts. A command called `check`, `audit`, `summary`, or `dry-run` is not inherently read-only.
5. Read [references/compatibility-and-tools.md](references/compatibility-and-tools.md) for applicable compatibility and execution boundaries. Consult version-matched official migration/tool documentation for selected transformations; do not preload unrelated feature guides.

## Define a bounded transition

1. State the goal, allowed paths, excluded generated/vendor files, intended transformations, compatibility promises, and observable success criteria.
2. Separate runtime/dependency prerequisites from source transformations and tool-policy changes. Do not combine a PHP version upgrade, broad framework upgrade, formatting sweep, and architecture rewrite without task scope for each.
3. Identify public symbols, named arguments, serialization, persisted values, ORM hydration/proxies, mocks, and downstream callers affected by the change. Mark inaccessible consumers unknown.
4. Choose a small first slice and identify tests or before/after observations that would reject an unsafe transformation. Preserve a recoverable record of the specific pre-change state without touching other sessions' work.
5. Record required checks and runtime cells, tools unavailable, and changes that need a live-contract migration. Do not invent fixed durations, a mandatory PHPStan level, coverage percentage, or universal DTO/enum policy.

## Preview, then apply within scope

1. Prefer cheap static inspection and existing evidence before project execution. Use installed project tools and verified version-specific flags; do not install or upgrade tools automatically.
2. Preview automated transformations before applying. Invoke the actual tool rather than assuming a Composer alias forwards safety flags. Explain preview artifacts and cache writes; keep them in an approved or isolated location.
3. Inspect the preview against the intended files and behavior. Reject unrelated churn, generated changes, unsafe inferred types, incompatible syntax, and unrequested policy changes.
4. For an authorized implementation, apply the inspected transformation to the same bounded paths. Recheck current status and any changes since the preview. An apply command may omit the tool's preview flag only in this scoped implementation phase; a preview does not authorize broader edits.
5. Inspect the resulting diff before continuing. If the tool exceeds scope or a check fails, stop that transformation and preserve evidence. Reverse only this task's isolated edits when safe; never restore whole dirty files or clean a shared tree.

## Verify behavior and compatibility

- Run proportionate configured syntax, class-load, type/architecture, and behavioral checks for affected paths. Record the actual commands, tool/runtime versions, selected tests, exit status, and observed outcomes.
- Check supported minimum and target runtime cells when the compatibility promise spans them. A lock resolved on a newer runtime or Composer platform emulation alone does not establish installability and runtime behavior on every supported cell.
- Compare baseline/ignore changes with resolved findings; do not hide new errors or regenerate a baseline merely to get green output. Baseline updates need a stated reason and reviewable delta.
- Treat absent tools, skipped tests, timeouts, stale caches, or missing runtime cells as incomplete evidence. A zero exit status, config-file presence, or package declaration does not prove the intended check executed.
- Broad mutation testing, benchmarks, full security scans, dependency downloads, and deployments require their own task scope. Do not run them as a default completion ritual.

## Report

Return current/target environment, scope and exclusions, compatibility risks and consumers, preview reviewed, changes applied or plan-only status, checks with outcomes, skipped/missing evidence, baseline/dependency deltas, and remaining transition gates. Mark the result `verified` only for criteria supported by observed evidence; otherwise use `partial` or `blocked` and identify the exact missing check or input. Do not claim a deployment, full compatibility matrix, or external consumer migration was verified when it was not.
