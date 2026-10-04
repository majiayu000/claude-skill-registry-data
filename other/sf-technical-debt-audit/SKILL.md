---
name: sf-technical-debt-audit
description: Standing technical-debt audit of a Salesforce project and org - inventory the metadata surface, measure API version drift, test and coverage debt, trigger and automation sprawl, retired Workflow Rules and Process Builder still running, hardcoded ids and endpoints, profile-based permissions, dead fields and classes, Apex volume against the 6 MB org limit, and package and dependency debt; then rank findings by impact and effort into a debt register with an owner and a remediation skill per item. Use when taking over an unfamiliar org, planning a refactor or a release-hardening sprint, answering "why is every change here slow", or producing a debt report for an architecture review. Not for reviewing a diff - that is skill sf-code-analyzer-quality and the sf-quality-gate agent.
---

# Salesforce Technical Debt Audit

## When to use

| Situation | Use this skill |
| --- | --- |
| Taking over an org or codebase you did not build | Yes |
| Planning a hardening sprint and needing a ranked debt register | Yes |
| Explaining why small changes take days in this org | Yes |
| Reviewing the diff of the change you just made | Skill `sf-code-analyzer-quality`, agent `sf-quality-gate` |
| Security posture of the org | Skill `sf-org-security-audit` |
| Deciding how small a specific change should be | Skill `sf-minimal-change` |
| A specific governor limit being hit at runtime | Skill `sf-governor-limits` |
| Deployment failures and release mechanics | Skill `sf-deployment-strategies` |

An audit is read-only. It runs against source plus a connected org, never writes, and is safe to
point at production - see Verification for the production posture.

## What counts as debt here

Debt is anything that makes the next change more expensive than it should be. Six categories, each
with a measurable signal:

| Category | Signal you can measure | Why it costs | Remediation skill |
| --- | --- | --- | --- |
| Version drift | `<apiVersion>` spread across metadata; `sourceApiVersion` in `sfdx-project.json` | Behaviour differs per class; upgrades become archaeology | `sf-project-structure` |
| Test debt | Classes without a test, coverage below the gate, `SeeAllData=true`, assertion-free tests | No safety net, so every change is manual QA | `sf-apex-testing`, `sf-lwc-jest-testing` |
| Automation sprawl | Triggers per object, Workflow Rules and Process Builder still active beside Flows | Order of execution becomes unknowable | `sf-flow-automation`, `sf-process-builder-migration`, `sf-apex-development` |
| Structural debt | Hardcoded ids and URLs, profiles instead of permission sets, no layering, duplicated selectors | Every environment needs manual fixes | `sf-minimal-change`, `sf-fflib-foundations` |
| Dead weight | Fields, objects, classes and permission sets nothing references; Apex volume against the org limit | Search noise, deploy time, limit headroom | `sf-minimal-change` |
| Delivery debt | Untracked manual org changes, no package boundaries, no CI gate | Releases are irreproducible | `sf-deployment-strategies`, `sf-packaging-release` |

## Core patterns

### 1. Fix the scope before measuring anything

```bash
sf org display --target-org vf-int
sf org list limits --target-org vf-int
sf org list metadata-types --target-org vf-int --output-file .vibeforce/reports/metadata-types.json
```

Record: org alias and type, API version, the package directories from `sfdx-project.json`, and
whether the source you hold is the whole org or one package. An audit of a partial source tree that
claims org-wide coverage is worse than no audit.

### 2. API version drift, measured from source

```bash
# every declared apiVersion, most common first
grep -rho "<apiVersion>[0-9.]*</apiVersion>" force-app | sort | uniq -c | sort -rn

# the files furthest behind the project baseline
grep -rl "<apiVersion>4[0-9]\." force-app --include="*-meta.xml" | head -50
```

The baseline is `sourceApiVersion` in `sfdx-project.json` and `apiVersion` in
`config/vibe-force.defaults.json` (67.0). The post-edit hook already flags a mismatch on files you
touch (`scripts/lib/xml-lint.js`); the audit is the org-wide version of the same question.

Org-side equivalent, when the source is not the whole truth:

```bash
sf data query --use-tooling-api --target-org vf-int \
  --query "SELECT Name, ApiVersion FROM ApexClass WHERE NamespacePrefix = null ORDER BY ApiVersion"
```

`[unverified: the ApexClass.ApiVersion field name was not confirmed against the Tooling API
reference in this session - run sf sobject describe --sobject ApexClass --use-tooling-api first]`

### 3. Test debt, in the two places it hides

```bash
# structural: which classes and bundles have no test at all
node "${CLAUDE_PLUGIN_ROOT}/scripts/checks/vf-check.mjs" pairing --json

# behavioural: coverage per class, from a real run
node "${CLAUDE_PLUGIN_ROOT}/scripts/checks/vf-check.mjs" apex --target-org vf-int --json

# tests that read org data instead of creating it
grep -rn "SeeAllData\s*=\s*true" force-app --include="*.cls"

# tests with no assertion at all - one file per iteration, so an empty list is simply an empty loop
grep -rli "@isTest" force-app --include="*.cls" | while read -r f; do
  grep -q "Assert\.\|System.assert" "$f" || echo "no assertion: $f"
done
```

Coverage above the gate with assertion-free tests is not coverage; report both numbers.

### 4. Automation sprawl per object

```bash
# triggers per object, from source
grep -rho "trigger [A-Za-z0-9_]* on [A-Za-z0-9_]*" force-app --include="*.trigger" \
  | awk '{print $4}' | sort | uniq -c | sort -rn

# what still runs beside your Flows
sf data query --use-tooling-api --target-org vf-int \
  --query "SELECT MasterLabel, ProcessType, TriggerType, Status FROM FlowDefinitionView WHERE Status = 'Active'"
```

Two triggers on one object is a finding on its own: the platform does not define their order.
Workflow Rules and Process Builder lost support on 31 December 2025 - an active one beside a
record-triggered Flow on the same object is the single most common source of "it depends" bugs
(skills `sf-flow-automation` for workflow rules, `sf-process-builder-migration` for processes).

### 5. Hardcoded ids, endpoints and environment assumptions

```bash
# 15 and 18 character ids in code
grep -rnE "'[a-zA-Z0-9]{15}'|'[a-zA-Z0-9]{18}'" force-app --include="*.cls" --include="*.js"

# endpoints that should be Named Credentials
grep -rnE "https?://" force-app --include="*.cls" | grep -v "schema.org\|w3.org"
```

Every hit is an environment coupling: it works in the org it was written in and breaks everywhere
else. Fixes are Custom Metadata, Custom Settings, `Schema.SObjectType` describes, and Named
Credentials (skill `sf-integration-patterns`). Turn the recurring ones into a Code Analyzer regex
rule so the audit does not have to find them twice (skill `sf-code-analyzer-quality`, pattern 5).

### 6. Permission debt

```bash
ls force-app/main/default/profiles/ 2>/dev/null | wc -l
ls force-app/main/default/permissionsets/ 2>/dev/null | wc -l

sf data query --target-org vf-int \
  --query "SELECT Assignee.Username FROM PermissionSetAssignment WHERE PermissionSet.PermissionsModifyAllData = true"
```

Profiles carrying feature access instead of permission sets is debt: profiles cannot be composed,
and a profile diff is unreviewable. The deep version of this audit - object matrices, dangerous
permissions, guest access - is skill `sf-org-security-audit`.

### 7. Dead weight and limit headroom

```bash
# Apex volume against the org limit
find force-app -name "*.cls" -not -name "*Test.cls" -exec cat {} + | wc -c

# classes nothing references - skip tests and every entry point the platform calls for you
for f in force-app/main/default/classes/*.cls; do
  n=$(basename "$f" .cls)
  grep -qiE "@isTest|@AuraEnabled|@RestResource|@InvocableMethod|webService|implements +(Schedulable|Batchable|Queueable|Database\.)" "$f" && continue
  refs=$(grep -rl "\b$n\b" force-app --include="*.cls" --include="*.js" --include="*.xml" | grep -cv "/$n\.")
  [ "$refs" -eq 0 ] && echo "unreferenced: $n"
done

# custom fields on an object, to compare against what the UI and code actually use
sf data query --use-tooling-api --target-org vf-int \
  --query "SELECT QualifiedApiName, DataType FROM FieldDefinition WHERE EntityDefinition.QualifiedApiName = 'Account'"
```

Limits that matter for this category: 1 million characters per class or trigger, 6 MB of Apex per
org (10 MB in scratch orgs, raisable by support case), 7,500 code units per deployment - all from
skill `sf-governor-limits`. Report headroom as a percentage, not a byte count.

### 8. Delivery debt

```bash
sf project deploy preview --target-org vf-int          # what differs between source and org
sf project retrieve preview --target-org vf-int        # what was changed in the org by hand
```

Anything that shows up only in `retrieve preview` was changed in Setup and exists in no branch.
Count those components: they are the debt that makes every deployment a negotiation.

### 9. Rank, do not list

An audit that returns 300 findings changes nothing. Rank each finding on two axes and report the
top of the list:

| Impact | Meaning |
| --- | --- |
| 3 | Blocks or breaks releases, or risks data loss |
| 2 | Slows every change in one area |
| 1 | Local annoyance |

| Effort | Meaning |
| --- | --- |
| 1 | One PR, no behaviour change |
| 2 | One sprint, needs tests first |
| 3 | Needs a migration plan and a rollback path |

Order by impact descending, then effort ascending. The first five items are the report; the rest is
an appendix.

### 10. The debt register

```markdown
## Debt register - <org alias> - <ISO date>

| # | Category | Finding | Evidence | Impact | Effort | Owner | Remediation skill |
| --- | --- | --- | --- | --- | --- | --- | --- |

## Measured baseline
| Metric | Value | Gate or limit |
| --- | --- | --- |
| Apex classes / triggers | | |
| Org Apex volume | | 6 MB |
| Apex coverage (org) | | gates.apexOrgCoverageMin |
| Classes with no test | | 0 |
| LWC bundles with no spec | | 0 |
| Active Workflow Rules / Process Builders | | 0 for new automation |
| Objects with more than one trigger | | 0 |
| Profiles / permission sets in source | | |
| Components changed in the org only | | 0 |

## Not measured
<what the audit could not see, and why>
```

Write it to `.vibeforce/reports/debt-<ISO>.md` so the next audit can diff against it. A debt
register without a baseline cannot show progress, and progress is the only reason to run it twice.

## Anti-patterns

| Anti-pattern | Consequence | Fix |
| --- | --- | --- |
| Auditing source and calling it an org audit | Org-only changes stay invisible | Run `sf project retrieve preview` and say what you could not see |
| Counting findings instead of ranking them | The report is ignored | Impact x effort, top five first |
| "Refactor everything to fflib" as a finding | Rewrite proposal, not a debt item | Name the cost of the current shape in changes per week |
| Treating coverage percentage as test quality | Assertion-free tests pass the gate | Report coverage and assertion density together |
| Deleting a field because nothing in source references it | Reports, list views and Flows reference fields too | Check `FieldDefinition`, reports and Flow metadata before proposing deletion |
| Running the audit against production with a mutating check | Guard trips, or worse, it does not | Only the read-only checks; see Verification |
| Filing debt with no owner | Nothing moves | Every register row names a person and a remediation skill |

## Verification

```bash
# the local gates, on the whole tree rather than the diff
node "${CLAUDE_PLUGIN_ROOT}/scripts/checks/vf-check.mjs" static --json
node "${CLAUDE_PLUGIN_ROOT}/scripts/checks/vf-check.mjs" pairing --json

# org-side, read-only
node "${CLAUDE_PLUGIN_ROOT}/scripts/checks/vf-check.mjs" apex --target-org vf-int --json
sf org list limits --target-org vf-int
sf project deploy preview --target-org vf-int
```

Production posture: the queries and previews in this skill are read-only and legitimate against a
production alias, and `vf-check` prints a production banner rather than refusing for the read-only
family. `vf-check apex` runs tests in the org and is not part of a production audit - take its
numbers from the last release pipeline instead. Never set `VF_ALLOW_PROD=1` to force a mutating
check through as part of an audit.

Exit codes are the runner contract: `0` pass, `1` gate failed, `2` misconfiguration or missing
tool, `3` org or network error.

## References

- [`references/debt-signals.md`](references/debt-signals.md) - the full signal catalogue: detection command, threshold, remediation and owning skill per signal.
- Related skills: `sf-org-security-audit` (security posture), `sf-code-analyzer-quality` (static analysis and custom rules), `sf-minimal-change` (how small a change should be), `sf-governor-limits` (the limit tables cited here), `sf-flow-automation` (automation consolidation), `sf-apex-testing` and `sf-lwc-jest-testing` (test debt), `sf-deployment-strategies` and `sf-packaging-release` (delivery debt), `sf-project-structure` (API version baseline).
- Official: [Salesforce CLI Command Reference](https://developer.salesforce.com/docs/platform/salesforce-cli-reference/guide/cli_reference_unified.html), [org list metadata](https://developer.salesforce.com/docs/platform/salesforce-cli-reference/guide/cli_reference_org_list_metadata.html), [Apex Governor Limits](https://developer.salesforce.com/docs/atlas.en-us.apexcode.meta/apexcode/apex_gov_limits.htm), [Migrate to Flow](https://developer.salesforce.com/docs/platform/flow-builder/guide/flow-migrate-to-flow.html).
