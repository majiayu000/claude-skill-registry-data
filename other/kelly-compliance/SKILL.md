---
name: kelly-compliance
license: MIT; includes Apache-2.0 method adaptations (see LICENSES/Apache-2.0.txt)
description: Prepare outbound SaaS cloud security baselines and SOC 2 readiness with accountable controls, normalized/Prowler/Security Hub reports, scoped read-only AWS metadata collection, period-aware evidence review, gaps, exceptions, and a Busabase visual workbench. Use for 云服务器合规、SOC 2 就绪、审计准备、证据期间、控制矩阵、合规缺口. Produces preparation materials, never certification or an audit opinion.
metadata:
  category: platform
  tags:
    - risk:gated-write
    - surface:busabase
  busabase:
    template: true
    folderSlug: kelly-compliance
    resources:
      - programs
      - resources
      - controls
      - assessments
      - evidence
      - evidence-links
      - issues
      - exceptions
    risk: gated-write
---

# Kelly Compliance

Help the service owner answer **which cloud checks failed, which control evidence is missing, and who owns the next step**. The local Agent owns AWS CLI execution; the AirApp manages scope, imports, reviews and accountable follow-up. No credential belongs in the browser or a Base.

## Start with a service and period

Use existing conversation authorization. Establish service description, owner, exact accounts and regions, authorization reference, scope version, framework `kelly-soc2-readiness@1`, assessment type, explicit ISO timestamps with timezone, and period. A saved account row does not authorize cloud access. A point assessment cannot claim period operation. First use works without cloud credentials through supplied reports or private evidence indexes.

The original readiness templates are illustrative mappings to public SOC 2 Trust Services Criteria categories. They do not reproduce AICPA criteria or CIS benchmark text. SOC 2 readiness is not certification. The independent auditor decides adequacy, selection and opinion.

## Install and open

Use the selected Busabase connection and current Space. Run `npx busabase-cli@0.99.1 install <this-directory>` or `BUSABASE_BASE_URL=... node scripts/setup.mjs --apply` from this directory. The complete template includes eight typed Bases, native table Views, the manual, guide, private Drive and canonical Hono/vanilla AirApp. Re-run setup to verify owned resources and scenario prompts; it preserves user additions and rejects ownership/schema conflicts. `--publish` deploys reviewed canonical source updates. Runtime binding uses SDK app/resource ownership, never deployment IDs or similarly named foreign Bases.

Open the installed 云安全与合规准备台. Create a scoped project; initialize original control templates. Templates declare independent evidence dimensions, owner and frequency. An example project never authorizes real AWS. ChangeRequest writes may queue for review; stop dependent execution until saved, then refetch. See [resource map](references/resource-map.md).

## Import or collect within the authorized scope

Read [input contracts](references/imports.md). `node scripts/import.mjs --program ID --file report.json --format normalized` validates and previews; `--apply` persists sanitized results through SDK ChangeRequests. Supported formats: normalized v1, Prowler CheckID JSON, Security Hub ASFF 2018-10-08 and GitHub change-evidence v1. Retain raw sensitive artifacts privately; only index/source locator, SHA-256, bounded redacted excerpt and timestamps are stored. Imported findings outside the project's account/region or mapping versions are rejected. Unknown check IDs stay unmapped.

For currently authorized AWS reads use `node scripts/aws.mjs --program ID --profile PROFILE --allow-account ACCOUNT --allow-region REGION --scope REFERENCE --scope-version 1 --apply`. Profile is a local AWS configuration name, not a secret. Exact scope and explicit account/region allowlists are independently checked, then `sts get-caller-identity` binds the selected profile. Only the finite catalog in `lib/aws.mjs` runs: EC2 describe-security-groups, CloudTrail describe-trails, Security Hub get-findings, RDS describe-db-instances. No shell interpolation, arbitrary command flags, auto-pagination, assume-role, remediation, log enabling, scan enabling or paid service configuration. Missing permissions, missing configuration and budget truncation are coverage gaps, never passes. See [AWS reads](references/aws.md). Live cloud results are environment-gated; do not claim real AWS verified from synthetic CLI tests.

## Review evidence without inventing history

Keep observed-at, collected-at and actual coverage-start/end distinct. Require consistent chronology, exact scope/reference/version, account/region/resource, requirement key and private source/hash. A current configuration snapshot does not prove past operation. Late collection of authentic historical records may support the real past interval after an explicit reviewer explains applicability. Do not fabricate backdated execution, reviews, logs or history.

Every evidence→control mapping has its own reviewer, reason and verdict. Acceptance for one control does not accept another. Each declared dimension must be supported independently; identity snapshots do not cover offboarding/access review, and backup success does not cover restore tests. A single passing source does not make a broad control green. Organizational controls require actual execution evidence and interpretation. Technical failures remain visible. Only later reviewed passing snapshot evidence for the exact resource/check/scope can supersede a prior snapshot failure; period failures retain the historical operating gap.

## Close gaps with verification

Assign gap owner and due date; track open → in-progress → needs-verification → closed/reopened. Closing requires a reason and new, accepted supporting evidence matching the gap's resource/check/account/region and observed later than the failure. Risk acceptance requires reason, compensating controls, accepting owner and future expiry. It expires visibly and never changes the underlying technical result. Stop on conflicts and refetch; never overwrite another reviewer silently.

`node scripts/report.mjs --program ID --output preparation.md --max-rows 500` performs an explicit bounded export, including scope, periods, dimensions, review decisions, source/hash indexes, gaps, owners, exceptions and limitations. No fabricated readiness percentage or audit opinion. Use the private Drive for intentionally shared preparation outputs; do not expose raw customer data.

Research provenance and licenses: [sources](references/sources.md). For suspected host intrusion use kelly-security; for application authorization/API business logic use kelly-appsec.
