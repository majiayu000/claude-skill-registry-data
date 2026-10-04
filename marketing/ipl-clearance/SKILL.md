---
name: ipl-clearance
version: 1.0.0
description: Run a trademark clearance search before adopting a new brand name, mark, or logo and risk-rate it clear, caution, or high-risk with a proceed/modify/abandon recommendation.
author: matrixx0070
tags: [trademark, clearance, brand, likelihood-of-confusion, search, risk, ip]
capabilities: []
---

## When to use

Use this before a client commits to a new brand name, product name, mark, or logo — while changing course is still cheap. It applies a consistent knockout-then-full search so obvious conflicts surface early and a real risk read backs the naming decision.

**Not for:** deciding whether a product design or feature is patent-clear (see ipl-fto-triage), reacting to an alleged conflict already raised against you (see ipl-infringement-triage), or interviewing an inventor about what they built (see ipl-cold-start-interview). This clears marks, not inventions or freedom-to-operate.

## Method

1. **Define the mark and scope.** Capture the exact mark, any logo/stylization, and the goods/services with their Nice classification classes. Clearance is per-class — a mark clear in one class can be blocked in another.
2. **Knockout search.** Look for identical and near-identical marks in USPTO TESS, common-law and state registrations, and domain/social handles. **Decision point:** an identical live mark on related goods usually ends it here — recommend a new candidate rather than paying for a full search.
3. **Full search if knockout clears.** Broaden to phonetic equivalents, translations, and design/coexisting marks across the relevant classes and channels.
4. **Analyze under likelihood-of-confusion** using the factors in Reference. Weigh mark similarity and relatedness of goods most heavily.
5. **Risk-rate:** clear / caution / high-risk. Map to a recommendation: proceed, modify (alter the mark, narrow the goods, or disclaim), or abandon.
6. **ATTORNEY-ESCALATION GATE.** You assist; you do not render legal opinions and this is not legal advice. Route any caution/high-risk result, any registrability opinion, and any filing decision to a licensed trademark attorney before the client relies on it or files.

## Example

Client wants "LUMENADE" for canned beverages (Class 32). Knockout finds "LUMINADE" live for fruit drinks, same class. Marks are near-identical in sound and meaning; goods are directly related; senior mark is suggestive (moderately strong). Rating: high-risk. Recommendation: modify or abandon; route to attorney before any filing.

## Pitfalls

- **Searching only for exact spellings.** Confusion turns on sound and meaning — phonetic and foreign-equivalent hits matter more than identical text.
- **Ignoring common-law use.** Unregistered senior users hold rights TESS never shows; a clean register is not a clean field.
- **Clearing across the wrong classes.** Rate risk against the actual goods/channels, not the whole register.
- **Treating a rating as a legal opinion.** A "clear" read is triage; registrability and enforcement calls belong to counsel.

## Output format

```
Mark / logo / stylization:
Goods-services & Nice class(es):
Knockout results: <identical | near-identical hits + class/status>
Full search results (if run):
Likelihood-of-confusion analysis (by factor):
Risk rating: CLEAR | CAUTION | HIGH-RISK
Recommendation: proceed | modify (<how>) | abandon
Attorney escalation: <yes/no + why>
```

## Reference

Likelihood-of-confusion factors: similarity of the marks (sight, sound, meaning/commercial impression); relatedness of the goods/services; strength/distinctiveness of the senior mark on the fanciful > arbitrary > suggestive > descriptive > generic spectrum; channels of trade and marketing; purchaser sophistication; evidence of actual confusion; intent of the junior user; and likelihood of expansion ("bridging the gap"). US frameworks applying these: DuPont (TTAB), Sleekcraft (9th Cir.), and Polaroid (2nd Cir.).
