---
name: osint-recon-automation
description: OSINT and reconnaissance automation skill for passive collection, pivoting, deduplication, and graph-based analysis using subfinder, amass, dnsx, chaos, crt.sh, github-dorks, waybackurls, gau, gitleaks, trufflehog, theHarvester, h8mail, holehe, sherlock, Shodan, Censys, FOFA, and Hunter. Use for asset discovery, exposure monitoring, and authorized reconnaissance only.
---

# OSINT Recon Automation

## Authorization Boundary

- Restrict to your own assets, bug bounty programs with explicit scope, or assignments with written authorization.
- No social engineering, doxing, harassment, or targeting individuals.
- Respect rate limits and provider terms; never weaponize discovered credentials.

## Recon Workflow

1. Seed: registered domains, ASNs, org names, GitHub orgs, app store handles.
2. Expand passively: cert transparency, passive DNS, reverse WHOIS, ASN ranges, code search, leaked credential repos, archive snapshots.
3. Resolve and validate: `dnsx`, `httpx`, screenshot with `gowitness` or `aquatone`.
4. Pivot: shared favicons (`favfreak`), Google Analytics IDs, S3 bucket naming, JS endpoints, ASN neighbors.
5. Dedupe and graph: build a node-edge model `(asset)-[relation]->(asset)` and store in Neo4j or JSONL.
6. Monitor: diff snapshots; alert on new subdomain, new exposed service, leaked secret, or impersonation domain.

## Exposure Signals

- Exposed admin panels, dev/stage hosts, open S3/Blob/GCS, leaked `.env`, `.git/`, `.DS_Store`, swagger, GraphQL introspection, package registry takeover candidates, dangling DNS.

## Output Contract

- `seeds.yaml`, `assets.jsonl`, `graph.json`, `screenshots/`, `exposures.csv`, `diff/<date>.md`.
- `report.md`: new exposures since last run with severity and owner.
- `takedowns.md`: impersonation domains and reporting paths.
