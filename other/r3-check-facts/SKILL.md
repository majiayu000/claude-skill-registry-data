---
name: r3-check-facts
description: Fact-check R3 Data Recovery content against the repo's FACTS.md. Use when writing or reviewing R3 website copy, case studies, or marketing text, or when the user says "check facts", "fact-check this", or asks whether a claim about R3 is accurate.
---

# Check Facts

Verify every factual claim in R3 content against `FACTS.md` — the single source of truth in the repo you're working in. This skill reads and reports; edits happen only after the verdict.

## 1. Load the source of truth

Read the repo's `FACTS.md` in full. If the repo has none, stop and say so — don't fact-check from memory. Known copies live in `r3comv2`, `r3comv2-business`, and `r3-wiki`; these have drifted. The repo-local copy is authoritative for that repo's content, but flag any claim where the copies disagree so the drift gets fixed at the source.

## 2. Extract the claims

Walk the content under review and list every **checkable claim**: numbers, dates, names, certifications, capabilities, coverage, guarantees, superlatives ("largest", "first", "only", "more than any other"). Marketing tone isn't a claim; "50,000+ recoveries" is.

## 3. Verdict per claim

Grade each claim against FACTS.md:

- **Verified** — matches FACTS.md.
- **Overclaim** — stronger than the recorded fact. Watch the recorded terminology guidance: e.g. FACTS.md distinguishes "ISO 27001 aligned" from "certified", and approximate figures carry a "+". Use the exact preferred wording.
- **Contradicted** — conflicts with FACTS.md. Quote both sides.
- **Unrecorded** — plausible but absent from FACTS.md. Ask the user whether it's true; if confirmed, propose the row to add to FACTS.md rather than letting the claim ride unrecorded.

**Done when** every extracted claim carries one of these four verdicts — no claim left ungraded.

## Output

A table: claim → verdict → FACTS.md line (or "not recorded") → suggested rewording where needed. Then, separately, any rows to add to FACTS.md and any cross-repo drift found.

Wait for the user before editing content or FACTS.md.
