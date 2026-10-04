---
name: apply-hicks-law
description: Use when simplifying navigation menus, option lists, decision points, or any interface where too many choices slow users down
source: Hick "On the Rate of Gain of Information" Quarterly Journal of Experimental Psychology (1952); Nielsen Norman Group Hick's Law article; Raskin "The Humane Interface" (2000)
tags: [hicks-law, decision-design, ux, navigation, simplicity]
verified: true
---

# Apply Hick's Law

Reduce the number and complexity of choices at each decision point so users can act faster, with less cognitive effort and fewer errors.

## Why This Is Best Practice

**Adopted by:** Apple iOS navigation patterns, Google Material navigation drawer, Amazon checkout funnel reduction, Basecamp progressive disclosure
**Impact:** Hick (1952) showed reaction time increases logarithmically with choices: doubling options adds a fixed decision overhead; Amazon's 1-Click checkout (minimal choice) increased conversion by ~20%
**Why best:** Decision time = a + b × log2(n+1) where n = number of choices. Reducing n directly reduces task time. Progressive disclosure and chunking maintain access to full functionality while reducing per-screen load.

Sources: Hick (1952) Quarterly J. Experimental Psychology; Hyman (1953) confirmation study; Raskin (2000) Ch. 5; Nielsen Norman Group Hick's Law

## Steps

1. **Audit decision points** — map every screen where users choose between options; record the number of choices at each point.
2. **Identify high-stakes decision points** — prioritize menus, CTAs, onboarding flows, and checkout funnels; small reductions here have largest impact.
3. **Remove unnecessary options** — eliminate choices that <5% of users select; relocate them to advanced settings or help docs.
4. **Chunk remaining options** — group 7±2 items into categories of 3–5; the total decision is now "which category" + "which item" rather than all at once.
5. **Apply progressive disclosure** — show only the most critical 3–5 choices initially; reveal advanced or contextual options on demand.
6. **Order options meaningfully** — place most-used options first (frequency), most-important first (priority), or alphabetically for large lists users already know (recall).
7. **Distinguish options clearly** — ensure each option is visually and semantically distinct; ambiguous options multiply effective choice count.
8. **Simplify option labels** — shorter, crisper labels reduce time to read and compare; "Download" beats "Click here to download your file."
9. **Test decision speed** — measure time-on-task for key decisions before and after reduction; target ≥15% improvement.
10. **Monitor abandonment** — track form abandonment and drop-off rates at simplified decision points; if they worsen, options removed may have been needed.

## Rules

- Never reduce options below what users need to complete their goal — simplicity that breaks task completion is anti-simplicity.
- Removing options is not the only lever — improving option clarity and ordering also reduces decision time.
- Chunking must reflect users' mental models, not designers' categories — validate groupings with card sorting.
- Progressive disclosure requires clear affordance to reveal hidden options — "More options" or "Advanced" must be visible.
- Apply Hick's Law per screen, not per product — each screen's decision load is evaluated independently.

## Common Mistakes

- **Hiding necessary options too aggressively** — power users cannot find settings; abandonment increases among expert segment.
- **Chunking by internal org structure** — groups that make sense to the team often make no sense to users.
- **Applying Hick's Law to search results** — search results should be comprehensive; Hick's Law applies to navigation, not retrieval.
- **Removing secondary actions without alternatives** — deleting options without providing another path (e.g., keyboard shortcut, search) breaks workflows.
- **Confusing fewer with simpler** — 3 ambiguous options can be slower to decide than 7 clear ones.

## When NOT to Use

- Expert users with established workflows who need direct access to all options
- Configurator tools (e.g., product builders, IDE settings) where completeness is the core value
- Comparison shopping interfaces where all options must be simultaneously visible
