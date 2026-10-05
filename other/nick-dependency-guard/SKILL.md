---
name: nick-dependency-guard
description: Dependency auditing for Nick's projects with focus on Node and Python. Use before deploys, during maintenance, or when checking packages for vulnerabilities, outdated versions, license issues, and upgrade risk. Flags critical CVEs as deploy blockers and produces a prioritized upgrade plan.
---

# Nick Dependency Guard

Use this as the default dependency auditing skill.

## Purpose
Scan projects for:
- vulnerable dependencies
- outdated packages
- risky major upgrades
- license issues
- deploy blockers

## Hard rules
- Critical CVEs are deploy blockers
- Do not recommend shipping with known critical vulnerabilities
- Separate patch/minor/major upgrade risk clearly
- Call out license issues explicitly
- Prefer actionable upgrade guidance over noisy output

## Default workflow
1. Detect package ecosystem
2. Audit installed/declared dependencies
3. Identify vulnerabilities and blockers
4. Identify outdated packages
5. Flag license risks
6. Produce prioritized upgrade plan

## Default output
- Critical vulnerabilities / blockers
- Other vulnerabilities
- Outdated packages
- License issues
- Prioritized upgrade plan
- Breaking change warnings

## Focus ecosystems
- Node / npm
- Python / pip

## References
- Read `references/node-audit.md` for Node guidance
- Read `references/python-audit.md` for Python guidance
- Read `references/license-guidance.md` for license risk rules
- Read `references/upgrade-priorities.md` for prioritization logic

## Bundled scripts
- `scripts/scan_node_dependencies.sh` — audit npm dependencies
- `scripts/scan_python_dependencies.sh` — audit Python dependencies
- `scripts/generate_upgrade_plan.sh` — create an upgrade planning stub
