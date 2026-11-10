---
name: x-myth-check
description: Use when a user asks whether a claim, viral tip, ranking formula or X/Twitter algorithm guide is accurate, supported by code, outdated or misleading.
---

# Check X claims

For a new natural-language request, use `x-assistant` first when installed. If this workflow was explicitly selected, delegated with `routed_by: x-assistant`, or installed alone, execute directly; do not route back.

Use [the evidence guide](references/knowledge-guide.md). Answer in the user's language. Work from the exact supplied claims; quotation is not agreement.

1. Split the material into independently testable propositions, including numbers, implied universality and practical promises. Retain enough original wording to identify each claim.
2. Retrieve relevant full entries and Q items. Inspect the source's function, caller, audience, code revision and units when they determine the verdict. A source repeating a claim is not evidence for it.
3. Classify each proposition: **supported**, **supported under stated conditions**, **misread/contradicted**, **not established**, or **outdated**. “Not established” does not mean disproven. Reserve “outdated” for evidence of a later change.
4. For each give the verdict, precise correction, original evidence, practical consequence and remaining uncertainty. If a long guide contains several independent claims, cover all of them; group duplicates explicitly.
5. If requested, return a corrected passage preserving the author's meaning and voice. Separate corrected copy from your explanation. Current or uncovered claims require fresh primary-source research, clearly labeled.

Use a compact table when comparing multiple claims. For a single claim use a direct paragraph. Never turn predicted-action weights into fixed payouts per observed action, a candidate count into a daily quota, or a mechanism's existence into a measured reach increase. For “the second daily post loses 40%”, check exactly what the count and multiplier apply to before giving publishing advice.

For claims about the present algorithm, first read the dated-update procedure in [the knowledge guide](references/knowledge-guide.md). Apply relevant current updates alongside historical claims, and state the reviewed revision when it matters.
