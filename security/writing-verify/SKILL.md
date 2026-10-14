---
name: writing-verify
description: "Fact-check audit: extract every claim of fact from a draft and report which are sourced, unsourced, or unverifiable, ranked by publication risk. Use before anything goes out with numbers, names, dates, quotes, superlatives, or causal claims; when the user asks to fact-check, verify claims, or check sources. Flags only — never deletes or rewords claims silently. For fiction canon consistency, use writing-bible instead."
---

# Verify

Report what the piece claims and whether the text supports it. This skill
**flags**; it never deletes or weakens a claim silently — an unsourced true
statement is not a false one, and deletion is the user's call, not the skill's.

1. **Extract every claim of fact**: numbers, names, dates, quotes, superlatives
   (_best_, _first_, _#1_), and causal assertions (_causes, drives, leads to_).
   Skip opinion and clearly signposted judgment — a labeled opinion is not a
   claim to source.
2. **Classify each**: **sourced** (the text carries the source — quote it
   verbatim), **unsourced** (checkable, no source in the text), or
   **unverifiable from text** (a judgment dressed as fact, or checkable only
   externally). No external search unless the user authorized it; until then,
   "unverified" is the finding — never assume true, never assume false.
3. **Rate by stakes, not difficulty**: `blocking` (a named person or company, a
   public number, a superlative — publication risk), `should-source` (a claim
   that would embarrass if challenged), `fine`. Stakes govern severity, not how
   hard the claim is to check.
4. **Report a table** — claim · classification · source-or-none · severity —
   then the blocking set alone. For each unsourced claim, propose a source to
   find or a safe rewording; never a deletion the user didn't ask for.
5. **Offer the external check** of the unsourced set as a next step, naming what
   kind of source would settle each claim. Until the user opts in, the finding
   stands as unverified, and the draft should not go out carrying it as fact.
