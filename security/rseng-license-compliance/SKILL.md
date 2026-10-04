---
name: rseng-license-compliance
description: >-
  Covers license compliance engineering: auditing the full dependency tree's
  licenses, compatibility analysis (permissive vs weak vs strong copyleft, GPL
  interactions, combining and linking), dual and multi-licensing, SPDX
  expressions and REUSE-compliant repositories, attribution and NOTICE
  obligations, and license policy in CI. Use when the user asks whether
  dependencies' licenses are compatible, wants a license audit, considers dual
  licensing or relicensing, must satisfy GPL/LGPL obligations, mentions SPDX,
  REUSE, NOTICE files or license scanners, or needs a license recommendation
  under real constraints. (License basics and first-time license choice:
  rseng-licensing.)
license: CC-BY-4.0
metadata:
  version: 0.1.0
---

# License compliance for research software

Choosing a license is a decision; staying compliant is engineering.
Every dependency in the tree grants rights under conditions, and a
project distributing software must satisfy all of them at once -
which is checkable, automatable and routinely neglected in research
code. This skill covers the audit-and-verify side of licensing;
license basics (what MIT/GPL/Apache mean, adding a LICENSE file,
licensing docs and data) live in rseng-licensing. One boundary stated
up front: an agent can analyze, flag and prepare, but consequential
calls - relicensing, dual-licensing contracts, anything with
commercial stakes - belong with the institution's legal or tech
transfer office. Say so when the stakes warrant it.

## Auditing the dependency tree

Inventory before judgment:

- Enumerate licenses of ALL transitive dependencies with a tool, not
  by hand: pip-licenses (Python), the equivalent per ecosystem
  (license-checker for npm, cargo-license), or ScanCode Toolkit for
  a thorough multi-language scan that reads actual file texts rather
  than trusting declared metadata.
- Treat "declared vs actual" skeptically: packages misdeclare;
  vendored files and copied snippets carry their own licenses; data
  and models bundled in the repo have licenses too
  (rseng-data-management).
- Flag the findings in three buckets: fine (compatible), obligations
  (compatible but with duties - attribution, notices, source offers),
  and conflicts (incompatible or unknown/unlicensed). "No license
  found" means all rights reserved and is a conflict, not a shrug.
- Record the audit result (a license inventory file or SBOM with
  license fields - rseng-security's SBOM practice carries license data
  naturally) so the next audit is a diff, not a redo.

## Compatibility analysis

The mental model that resolves most questions:

- Direction matters: compatibility means "may I combine this
  dependency into a work distributed under MY license". Permissive
  code (MIT/BSD/Apache) flows into almost anything; copyleft code
  pulls the combined work toward its own terms.
- Strong copyleft (GPL family): distributing a work that links or
  combines GPL code requires the whole to be GPL-compatible; GPLv2-
  only vs GPLv3 is a real incompatibility to check, and Apache-2.0
  is compatible with GPLv3 but not GPLv2.
- Weak copyleft (LGPL, MPL, EPL): obligations attach to the covered
  files/library, not the whole work - dynamic linking against LGPL
  is generally fine for any project; modifying the LGPL library
  itself is not.
- Network use: AGPL triggers source obligations on network service
  use - relevant the moment research software becomes a hosted
  service.
- Non-commercial and academic-only licenses (CC-NC variants,
  homegrown academic licenses) are incompatible with OSI open source
  and block downstream reuse; flag them loudly in dependencies and
  discourage them for new projects (rseng-licensing explains why).
- When a genuine conflict exists, the options in order: replace the
  dependency (rseng-software-reuse to find alternatives), isolate it
  behind a process/service boundary, seek an exception from its
  author, or change the project's own license. Present options with
  trade-offs; do not silently pick.

Authoritative references for specific pairs: the FSF license list
and the EU Joinup Licensing Assistant's compatibility checker beat
folklore; cite them when a pairing is contested.

## Suggesting a license (constraint-driven)

Recommend from constraints, not fashion. Ask or infer: what do the
dependencies already require (a GPL dependency decides the question
for distributed works)? Does the institution or funder have a
policy? Is commercial adoption desired (permissive lowers friction)
or is reciprocity the goal (copyleft)? Is the artifact a library
(LGPL/MPL/permissive keep adopters) or an application? Then suggest
one license with a one-paragraph rationale and the runners-up -
choosealicense.com framing works well for users; rseng-licensing
covers the fuller decision guidance. Never leave a repository
unlicensed while the decision pends; that blocks everyone.

## Dual and multi-licensing

- Dual licensing offers the same code under two licenses: commonly
  copyleft-or-commercial (revenue model requiring copyright
  concentration - every contributor must agree via CLA or
  assignment, which changes community dynamics -
  rseng-community-governance), or license-choice offers like "MIT OR
  Apache-2.0" (adopter-friendly, common in some ecosystems).
- Express it precisely with SPDX expressions: `MIT OR Apache-2.0`
  (recipient chooses), `MIT AND CC-BY-4.0` (different artifacts
  under different terms - code vs docs/data is the research-typical
  case). Put the expression in package metadata and per-file tags.
- Relicensing an existing project requires consent of all copyright
  holders; enumerate contributors (git history) and treat it as a
  months-long consent project, not an edit. This is a
  route-to-legal-office decision.

## Verifiable compliance: SPDX, REUSE and CI

Make license state machine-checkable:

<!-- REUSE-IgnoreStart -->
- Per-file SPDX tags (`SPDX-License-Identifier: Apache-2.0`) plus
  LICENSES/ directory per the REUSE specification; `reuse lint`
  then verifies the whole repository mechanically - the license
  analogue of a test suite.
<!-- REUSE-IgnoreEnd -->
- Enforce policy in CI (rseng-ci-cd): a license-audit step that fails
  on new dependencies outside the allowlist, and reuse lint where
  adopted. Policy-as-code prevents the quiet arrival of an
  incompatible dependency two years before anyone notices.
- Fulfill obligations at release time (rseng-publishing-releasing):
  ship required notices (Apache NOTICE files aggregated, copyright
  lines preserved), include dependency license texts where
  distribution requires them, and keep binary/container
  distributions in mind - an image distributes everything inside it.
- Record AI-assisted audits and license changes in aidecl.yaml
  (rseng-ai-declaration); license history is provenance.

## Working with this skill

This skill is source-independent: its authority is the SPDX and
REUSE specifications, the FSF and OSI license references and the
tool documentation linked below. It complements rseng-licensing
(fundamentals and first license choice).

Learn more (verified):
  - https://spdx.org/licenses/ - SPDX license list and identifiers
  - https://reuse.software - REUSE specification and tooling
  - https://www.gnu.org/licenses/license-list.html - FSF license
    list and GPL-compatibility notes
  - https://opensource.org/licenses - OSI-approved licenses
  - https://choosealicense.com - license chooser
  - https://interoperable-europe.ec.europa.eu/collection/eupl/solution/licensing-assistant/find-and-compare-software-licenses -
    EU Joinup Licensing Assistant compatibility checker
  - https://github.com/aboutcode-org/scancode-toolkit - ScanCode
    Toolkit license scanner
  - https://github.com/raimon49/pip-licenses - pip-licenses
    dependency license reporting

<!-- related-skills:begin -->

## Related skills

Check whether any of these applies before moving on:

- rseng-ci-cd - policy-as-code license gates
- rseng-community-governance - CLA implications of dual licensing
- rseng-dependency-management - license axis of intake vetting
- rseng-licensing - first license choice basics
- rseng-publishing-releasing - notice obligations at release
- rseng-security - SBOM carries license data

<!-- related-skills:end -->
