---
name: supply-chain-lord
description: Lord skill for software supply-chain security in AI-generated code — dependency guarding, SBOM, Cosign signing, and lockfile integrity.
triggers:
  - supply chain lord
  - supply chain
  - sbom
  - cosign
  - dependency guard
  - lockfile
  - سلسلة التوريد
  - تبعيات
personas:
  - SEC
  - DEVOPS
  - SRE
  - ARCH
tech_stack: []
lord: true

---

# Supply Chain Lord

[OBJ] Supply-chain security for AI-generated code. AI agents add imports faster than humans can review them.

## Problem

AI agents commonly add imports of external packages not declared in the project manifest. This is a supply-chain attack vector: a hallucinated package name may match a malicious typosquatted package. SAST/DAST catch this downstream — by then the code is committed.

## Rules

1. [REQ] **Dependency guard at diff time.** Every diff with new imports MUST pass through `runtime/supply_chain_guard.py`. Undeclared import = WARN (strict mode = BLOCK).
2. [REQ] **Lockfile as source of truth.** Declared dependencies come from `pyproject.toml`/`requirements.txt` (Python), `package.json`/`package-lock.json` (Node), `composer.json`/`composer.lock` (PHP), `go.mod` (Go). Never trust `import` statements as the dependency list.
3. [REQ] **Typosquat detection.** New import names within edit distance ≤ 2 of a declared dependency = WARN (e.g., `reqeusts` vs `requests`). Use Levenshtein distance.
4. [REQ] **Pin SHAs.** Container images and GitHub Actions pinned by SHA, not tag. Tags are mutable; SHAs are immutable. `uses: actions/checkout@v4` = reject; `uses: actions/checkout@<sha>` = accept.
5. [REQ] **SBOM generation.** Every release artifact ships with an SBOM (CycloneDX or SPDX). `aizee sbom generate` before release. No SBOM = no release.
6. [REQ] **Cosign signing.** Container images signed with Cosign (keyless OIDC). Unsigned image = BLOCK deploy. Verify signature on pull.
7. [REQ] **Minimum release age.** New dependency versions must be published ≥ 7 days before adoption. Brand-new releases have not been vetted; a non-trivial fraction of supply-chain attacks are caught and yanked within the first few days.
8. [REQ] **No floating ranges.** Prohibit `latest`, `*`, unbounded `>=` in manifests. These auto-resolve to brand-new releases. Pin to exact versions or bounded ranges.
9. [REQ] **Audit dependencies.** `pip-audit` / `npm audit` / `composer audit` before every release. Critical CVE = BLOCK.
10. [REQ] **No downgrade for type errors.** Never downgrade a dependency to fix a type error. Fix the code or upgrade. Downgrading = security regression.
11. [REQ] **Provenance verification.** Verify dependency provenance (e.g., `pip --require-hashes`, `npm ci` with lockfile, `composer install` with lock). No `pip install` without hash checking in CI.
12. [REQ] **MCP server provenance.** MCP servers registered as securables (`runtime/mcp_securable.py`) with verified endpoints. No ungoverned MCP server in the supply chain.
13. [REQ] **Diff scope.** A diff that adds a new dependency MUST also update the lockfile in the same diff. Dependency without lockfile update = BLOCK.
14. [REQ] **License compliance.** Every declared dependency has a license in the allowlist (MIT, Apache-2.0, BSD, ISC). GPL/AGPL in a commercial project = BLOCK (require LEGAL persona review).
15. [PROHIBIT] `git add .` / `git add -A` — stage only files you modified.
16. [PROHIBIT] Installing a dependency published < 7 days ago.
17. [PROHIBIT] Floating version ranges (`latest`, `*`, unbounded `>=`).
18. [PROHIBIT] Unsigned container images in production.
19. [PROHIBIT] A new import without a corresponding lockfile/manifest update in the same diff.
20. [REQ] **MCP tool poisoning defense.** Hash-pin or sign allowed MCP tool definitions. Re-validate on every list refresh. CVE-2025-54136 (CVSS 8.8) showed tool definitions can change server-side after initial review.
21. [REQ] **Model weight provenance.** Verify model weights have provenance metadata. Unsafe serialization (pickle) must be rejected. Use safe formats (safetensors, GGUF). AI/ML SBOMs required for all model deployments.
22. [REQ] **MCP CVE tracking.** Monitor and patch: CVE-2026-52869 (Python SDK session-ID injection), CVE-2026-52870 (cross-client task access), CVE-2026-59950 (WebSocket origin bypass), CVE-2026-25536 (TypeScript SDK data leak), CVE-2026-27896 (Go SDK key parsing). Pin SDK versions above fix releases.
23. [REQ] **Deadbugz campaign awareness.** Malicious MCP servers may activate payloads after a call-count threshold, evading initial review. Monitor for behavioral changes in MCP servers over time.
24. [REQ] **Confused-deputy prevention.** MCP proxies with static client_id and DCR can let malicious clients hijack consent cookies. Use CIMD (Client ID Metadata Documents) instead of DCR. Validate issuer per RFC 9207.
25. [REQ] **AI/ML SBOM.** Every AI/ML release artifact ships with an AI-specific SBOM (model weights, training data provenance, serialization format, dependencies). CycloneDX AI extension or SPDX 3.0 AI profile.
26. [PROHIBIT] Using MCP servers without hash-pinned tool definitions and CVE compliance verification.

## Enforcement Stack

```
Agent diff → SupplyChainGuard.check_diff (undeclared imports)
           → Typosquat check (edit distance ≤ 2)
           → Lockfile sync check (import + manifest in same diff)
           → pip-audit / npm audit / composer audit (CVEs)
           → SBOM generation (CycloneDX)
           → Cosign signing (container images)
           → Release gate (all green = release)
```

## References

- repo-contract: dependency guard warns when diff adds undeclared imports.
- SLSA framework: provenance, build integrity.
- Cosign: keyless container signing via OIDC.
- aiZee `runtime/supply_chain_guard.py`: implementation.
