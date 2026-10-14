---
name: documentation-search
description: "Runtime doc-research behavior: detect technology and installed version, consult official docs for that version when uncertain, implement, verify against docs. Use for any version-sensitive API, framework, config, CLI, or integration work."
---

# documentation-search

Behavior, not links: detect what the project uses, research the official source for that version when uncertain, verify the result against it.

## Runtime pipeline

```
understand task -> inspect repository -> identify technology -> identify installed version
  -> decide: confident from repo evidence? implement : research official docs first
  -> retrieve docs + official examples -> implement -> verify against docs -> test -> review diff
```

## Mandatory research rule

If the implementation depends on an API, framework behavior, library behavior, configuration option, CLI command, or version-sensitive behavior you are not highly confident about, research the official documentation BEFORE implementing. Model memory is never authoritative when it conflicts with current docs — docs win.

## Version detection (mandatory before framework research)

`installed version != latest version`. Never use latest docs for a pinned older version. Detect first with `scripts/detect-versions.sh <repo-root>` (resolves `references/framework-registry.yaml`), or manually:

- Python: pyproject.toml, uv.lock, requirements.txt, poetry.lock, Pipfile.lock
- JS/TS: package.json, package-lock.json, pnpm-lock.yaml, yarn.lock, bun.lock/bun.lockb
- Rust: Cargo.toml, Cargo.lock, rust-toolchain.toml
- Go: go.mod, go.sum
- Java: pom.xml, build.gradle, build.gradle.kts, gradle.lockfile
- Mobile: package.json, app.json, app.config.*, Expo SDK version
- Infra: Dockerfile, compose.yaml/yml, Terraform files, Helm charts, K8s manifests
- Cloud: provider config, SDK/CLI version, IaC provider version

## Source hierarchy

L1 official documentation · L2 official API/reference · L3 official GitHub repo · L4 migration/upgrade guide · L5 changelog/release notes · L6 official examples · L7 maintainer-authored material · L8 high-quality community. Search engines, SO, Reddit, blogs, YouTube, X may surface problems and experience but must NOT override L1–L7 without strong evidence. Never treat a search snippet as documentation.

## SEARCH official docs when

API unfamiliar · framework behavior uncertain · dependency version matters · docs may have changed · framework rapidly evolving · feature experimental · API deprecated · migration involved · config security-sensitive · deployment behavior matters · external service integration · error suggests changed behavior · types disagree with memory · generated code depends on an external SDK.

## Do NOT search when

Ordinary language syntax · trivial refactoring · renames · formatting · changes fully covered by existing local tests and known project conventions. Use judgment: research depth scales with uncertainty × blast radius.

## Search strategy

Prefer `site:` queries against the registry entry, e.g. `site:fastapi.tiangolo.com OAuth2 JWT`, `site:nextjs.org/docs server actions`, `site:react.dev useEffect`, `site:docs.spring.io/spring-boot configuration`, `site:docs.expo.dev router authentication`, `site:docs.rs/axum middleware`, `site:docs.aws.amazon.com EC2 autoscaling`.

Tool gates: IF a documentation/browser/search tool exists, use it. IF an MCP doc/search tool exists, prefer the authoritative source through it. IF the project vendors local docs/API references, inspect those too. ELSE fall back to repository/source inspection below. Never assume a search engine is available.

## Result handling

Extract: relevant API, supported behavior, version, required configuration, constraints, caveats, security considerations, migration/deprecation warnings. Implement only what is supported. For complex decisions record internally:

```
FACT: Official documentation says X.
PROJECT: This project uses version Y.
DECISION: Therefore implement Z.
```

## Confidence and scope

Rate every researched claim HIGH (official docs for the installed version + runtime proof), MEDIUM (official docs, version close but unproven here), or LOW (community/ambiguous). LOW confidence triggers more inspection, never silent version selection. Cover the full scope: monorepo workspace packages (detect per-package manifests, not just root), transitive dependencies when the behavior flows through them, generated code (read the generator + schema, not just output), and project-local wrappers/abstractions (which override library defaults — map them first).

## Docs-vs-observed reconciliation

When official docs conflict with actual repo behavior, reconcile explicitly: official documentation + installed version + observed behavior + tests/runtime evidence. Possible outcomes: repo pins an older behavior (follow repo, note upgrade path), repo works around a docs gap (verify workaround still holds on this version), or repo is wrong (fix with evidence). Never silently let community content override L1–L7.

## Evidence record

For important decisions record: installed version, documentation consulted + why it applies, decision, verification. Classify each line FACT / PROJECT FACT / DECISION / ASSUMPTION / UNKNOWN. Never promote ASSUMPTION or UNKNOWN to FACT. Proportionality: full records for version/security/architectural calls, one line otherwise.

## Source fallback (docs ambiguous)

1. Official GitHub repository source code. 2. Official tests (most valuable for actual supported behavior). 3. Release notes. 4. Migration guides. 5. Official issues if necessary. Do NOT jump to random community posts.

## Citation / traceability

For version-sensitive, security-sensitive, architectural, migration-related, external-API, or likely-questioned decisions, record: source URL, version, and why this API. No citations on trivial lines.

## References
- `references/framework-registry.yaml` — central machine-readable registry (official sources + version files).
- `scripts/detect-versions.sh` — repo technology/version detector; `scripts/run-doc-behavior-tests.sh` + `tests/fixtures/` — behavior scenarios.
- Deltas: `../technology-evaluation/`; compat: `../dependency-evaluation/`.
