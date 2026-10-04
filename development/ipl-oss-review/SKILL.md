---
name: ipl-oss-review
version: 1.0.0
description: Review a codebase or dependency set for open-source license compliance and flag copyleft contamination risk against your distribution model.
author: matrixx0070
tags: [open-source, license, compliance, copyleft, sbom, dependencies, ip]
capabilities: []
---

## When to use

Use this when you ship, sell, or embed software and need to know whether its open-source dependencies fit how you distribute it. Reach for it before a release or acquisition, or any "can we keep this library?" question — especially where a copyleft term could force disclosure of your own code.

**Not for:** OSS reps and warranties inside a contract (`ipl-ip-clause-review`); freedom-to-operate on patents (`ipl-fto-triage`); or clearing one third-party asset for a single use (`ipl-clearance`). This reviews obligations across a dependency tree, not contract text.

## Method

1. **Build the inventory.** Enumerate direct and transitive dependencies (an SBOM).
2. **Identify each license** (SPDX); note dual-licensed and unlicensed ones.
3. **Classify by obligation tier:** permissive, weak/file-level copyleft, strong copyleft, network copyleft.
4. **Check compatibility with your distribution model** — proprietary distribution, SaaS, or internal-only. The same license can be fine internally and fatal when distributed.
5. **Decision point:** for each copyleft dep, keep vs replace. Distributed proprietary code with a strong/network copyleft dep usually means replace or isolate; internal-only may be fine as-is.
6. **List required obligations** (notices, NOTICE reproduction, source disclosure, change statements) and **remediate:** replace, isolate, or comply.
7. **ATTORNEY-ESCALATION GATE:** route strong/network copyleft in distributed proprietary code, license conflicts, and M&A due-diligence findings to a licensed attorney. You assist; you do not advise.

## Example

A proprietary app pulls in an AGPL-3.0 charting library transitively. AGPL's source-disclosure triggers on network interaction and its copyleft reaches the combined work — contamination risk is high. Decision: replace with an MIT library, or isolate the AGPL component as a separate service reviewed by counsel. Escalate before release.

## Pitfalls

- **Skipping transitive dependencies.** The risky license is rarely a direct dep — walk the full tree.
- **Confusing SaaS with "no distribution."** AGPL triggers on network use; SaaS does not exempt you.
- **Treating permissive as obligation-free.** MIT/BSD/Apache still require retained notices; Apache-2.0 also needs the NOTICE file and change statements.
- **Ignoring compatibility.** GPL-2.0-only and Apache-2.0 cannot be combined — two acceptable licenses can still conflict.

## Output format

```
OSS COMPLIANCE REVIEW — <project> | distribution model: <proprietary-dist|SaaS|internal>
Dependency inventory (SBOM): <count direct / transitive>
| Component | License | Tier | Distributed? | Obligation | Action |
Contamination risks:
Required obligations (notices/NOTICE/source disclosure/change statements):
Remediation: <replace|isolate|comply>
Escalated to counsel: <items>
```

## Reference

OSS license obligations by tier:
- **Permissive** (MIT, BSD-2/3-Clause, Apache-2.0): retain copyright notice + license text. Apache-2.0 adds an express patent grant, a NOTICE file, and a duty to state changes.
- **Weak / file-level copyleft** (MPL-2.0 file-level, LGPL): reciprocity limited to the library or modified files; dynamic linking to proprietary code is allowed.
- **Strong copyleft** (GPL-2.0, GPL-3.0): derivative and combined works must ship under the GPL with corresponding source. GPL-3.0 adds patent grant and anti-tivoization terms.
- **Network copyleft** (AGPL-3.0): source-disclosure triggers on network/SaaS use, not only on distribution.

Copyleft triggers on **distribution** (AGPL: also on network interaction); permissive obligations are mainly attribution. Check compatibility — GPL-2.0-only is incompatible with Apache-2.0. Assistive analysis, not legal advice.
