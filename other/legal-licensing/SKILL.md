---
name: legal-licensing
description: Get licensing right — license choice, NOTICE/attribution, dependency compatibility, contributor terms.
version: 1
triggers: licensing, license choice, open source license, attribution, notice file, contributor terms
category: Money & markets
blurb: Get licensing right — the right license, attribution, dependency compatibility and contributor terms.
archetype: knowledge
example: Which license fits this project, and what notices do I owe?
---

# Legal & Licensing

Licenses decide who can use your work and how. Choose deliberately, attribute honestly, and keep dependencies compatible — before the lawyers have to.

## When to use
- Starting a repo/product; choosing or changing a license.
- Adding dependencies or vendoring code.
- Preparing releases with attribution requirements (ASF-style NOTICE chains).

## Method
1. **Pick by intent**: permissive default (MIT/Apache-2.0) for tools you want adopted; copyleft (AGPL/GPL) or split licensing (open interface + protected core) only as a conscious product decision — logged like an ADR.
2. **Headers & files**: `LICENSE` at root; source headers per house convention; license texts kept verbatim (never edited); `NOTICE`/attribution included when dependencies require it.
3. **Dependency compatibility**: automated license scan of dependencies (`dependency-governance` runs it — this skill judges fit); incompatible combinations resolved before merge, not after release.
4. **Contributor terms**: pick a policy (DCO sign-off or CLA) and enforce it in the contribution flow; document in CONTRIBUTING.
5. **Trademarks & brand**: name/logo usage rules; no implied endorsement; public claims ("compliant", "certified") only with real attestation behind them.
6. **Contracts awareness**: for client work, know the SOW/MSA constraints on IP and reuse — flag conflicts for review (counsel owns interpretation).
7. **Release hygiene**: bundled third-party licenses shipped with binaries where required; provenance/signing per `secure-build-pattern`.

## Quality gates
- [ ] Root LICENSE + NOTICE present; texts unmodified.
- [ ] Dependency license scan clean or consciously accepted with a record.
- [ ] Contributor policy documented and enforced.
- [ ] Public claims have evidence; attribution shipped where required.

## Red lines
- No license text edits; no incompatible dependency shipped "for now"; not legal advice — counsel decides contested calls.

## Related
`dependency-governance` · `technical-writing` · `release-management`.
