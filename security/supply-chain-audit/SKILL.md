---
name: supply-chain-audit
description: >
  Discover supply-chain manifests, run structured supply-chain audits,
  and export SBOMs through a dedicated MCP surface.
metadata:
  processkit:
    apiVersion: processkit.projectious.work/v2
    id: SKILL-supply-chain-audit
    version: "1.0.0"
    created: 2026-05-18T00:00:00Z
    category: processkit
    layer: 4
    uses:
      - skill: index-management
        purpose: Resolve repository files and paths quickly.
      - skill: release-audit
        purpose: Reuse disciplined audit reporting expectations.
    commands:
      - name: pk-supply-chain
        args: >
          [--root=<path>] [--manifest <path>...]
          [--discover-only] [--run-security]
          [--run-quality] [--export-sbom <path>]
        description: >
          Audit manifests and optionally export SBOM output.
    provides:
      mcp_tools:
        - discover_manifests
        - run_supply_chain_audit
        - export_supply_chain_sbom
---

# Supply-Chain Audit

## Intro

Use `/pk-supply-chain` when you need a release-facing supply-chain view.
The MCP server exposes three tools:

- `discover_manifests`
- `run_supply_chain_audit`
- `export_supply_chain_sbom`

Network-dependent security and quality probes are intentionally off by
default. Enable them only when explicitly requested.

## Overview

1. Discover dependency manifests and supported lockfiles.
2. Run `run_supply_chain_audit` with explicit `run_security_checks` /
   `run_quality_checks` when required.
3. Export SBOM when release evidence is needed.

## Gotchas

- **Offline default.** Missing network adapters must be explicit, not implicit.
- **Discover-only checks are not guarantees.** Discovery does not confirm
  policy.
- **Export output.** Persist SBOM/report output only when `write_output=True`.

## Full reference

### `discover_manifests`

- `project_root: str | None = None`
- `manifest_globs: list[str] | None = None`
- `include_vendor_dir: bool = True`
- `include_ci_manifests: bool = False`

### `run_supply_chain_audit`

- `project_root: str | None = None`
- `manifest_paths: list[str] | None = None`
- `run_security_checks: bool = False`
- `run_quality_checks: bool = False`
- `network_enabled: bool = False`
- `write_output: bool = False`
- `output_path: str | None = None`

### `export_supply_chain_sbom`

- `project_root: str | None = None`
- `manifest_paths: list[str] | None = None`
- `format: str = "json"`
- `write_output: bool = False`
- `output_path: str | None = None`
