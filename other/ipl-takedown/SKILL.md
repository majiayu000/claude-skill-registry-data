---
name: ipl-takedown
version: 1.0.0
description: Prepare a DMCA 512(c) takedown notice or a 512(g) counter-notice for online copyright infringement with all statutory elements.
author: matrixx0070
tags: [dmca, takedown, copyright, counter-notice, safe-harbor, infringement, notice]
capabilities: []
---

## When to use

Use this when your copyrighted work appears online without authorization and you want it removed, or to contest a takedown of your own content. Reach for it once you can point to a specific work and infringing URL.

**Not for:** trademark, patent, or non-copyright disputes (DMCA is copyright-only); a direct demand to the infringer (`ipl-cease-desist`); or clearing whether your use of someone else's work is permitted (`ipl-clearance`). This prepares DMCA notices only.

## Method

1. **Confirm standing.** You own or represent the copyright.
2. **Identify the work and infringement.** Name the exact copyrighted work and every infringing URL.
3. **Locate the host's DMCA agent** and submission channel.
4. **Consider fair use before sending.** A good-faith belief the use is unauthorized is required; obvious fair use undercuts it and risks §512(f) liability.
5. **Draft the notice** with all six §512(c)(3) statutory elements.
6. **Decision point:** DMCA takedown vs cease-desist (`ipl-cease-desist`) vs a trademark/patent claim. DMCA fits third-party-hosted copyright; a direct dispute or non-copyright claim does not.
7. **File and track** for a counter-notice.
8. **ATTORNEY-ESCALATION GATE:** contested or counter-noticed matters, §512(f) misrepresentation exposure, and non-copyright claims go to a licensed attorney. You assist; you do not advise.

## Example

Your photograph is reposted on a marketplace listing without permission. You confirm ownership, capture the exact listing URL, and find the marketplace's DMCA agent. You check fair use — a commercial resale listing is not fair use — and draft a 512(c) notice with all six elements, including the good-faith and penalty-of-perjury statements. You file and watch for a counter-notice, escalating to counsel if the seller counter-notices.

## Pitfalls

- **Skipping fair use.** A takedown against clear fair use invites §512(f) liability for misrepresentation.
- **Vague identification.** "Somewhere on their site" is not enough — give the exact URL.
- **Omitting the perjury and good-faith statements.** Both are mandatory; a notice missing either is defective.
- **Using DMCA for trademarks or patents.** It is copyright-only; the host will reject the claim.

## Output format

```
DMCA §512(c) TAKEDOWN NOTICE
To: <host DMCA agent>
1. Signature (physical/electronic) of owner or authorized agent:
2. Copyrighted work(s) claimed infringed:
3. Infringing material + URL(s) to locate it:
4. Complaining party contact (name, address, email, phone):
5. Good-faith-belief statement (use not authorized by owner, agent, or law):
6. Accuracy + authority statement, under penalty of perjury:
Date:
```

## Reference

DMCA §512(c)(3) takedown notice elements: (1) physical or electronic signature of the owner or authorized agent; (2) identification of the copyrighted work infringed; (3) identification of the infringing material and information reasonably sufficient to locate it (URL); (4) contact information of the complaining party; (5) a statement of good-faith belief that the use is not authorized by the owner, agent, or law; (6) a statement, under penalty of perjury, that the information is accurate and the complainant is authorized to act.

Also note: the **§512(g) counter-notice** carries its own elements and a **10-14 business-day** restoration window before the host may replace the material. **§512(f)** imposes liability for knowing misrepresentation. The **safe harbor is the host's**, requiring a registered agent and repeat-infringer policy. Assistive analysis, not legal advice.
