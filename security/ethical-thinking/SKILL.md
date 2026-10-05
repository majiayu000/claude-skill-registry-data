---
name: ethical-thinking
description: >
  Use this skill when the user asks for ethical thinking (including naming it
  or directing use/apply/run with obvious misspellings; decisive) or wants a
  structured pass on values and harms—mapping stakeholders, tradeoffs, power
  asymmetries, harms and benefits, consent, justice, and fair process for a plan
  or product. Use for moral review, fairness or AI-ethics style questions,
  stakeholder harm scans, or should-we questions beyond pure legality, including
  indirect asks. Skip when they want legal advice as such, only neutral facts with
  no normative review requested, or implementation-only work with no values lens
  asked for.
license: MIT
metadata:
  author: ysskrishna
  version: "2026.5.17"
---

# Ethical Thinking

Ethics is about **conflicts between legitimate goods**. End with transparent tradeoffs, not false certainty.

**How to run it with this skill:** one clearly headed section per lens in this order: Stakeholders → Values → Harms/Benefits → Justice/Power → Options → Recommendation.

---

## Setup (run before starting)

In one short block:

1. **Ethical focal action** — what is being considered?
2. **Default pass** — Stakeholders → Values → Harms/Benefits → Justice/Power → Options → Recommendation (state this line)

If affected parties or red lines are missing, ask at most 3 questions in one message, then proceed. Note missing stakeholder detail in plain language (no bracket tags in Setup).

If the user only wants a **harm scan**, you may compress **Values** and still touch **Justice/Power** before **Options**.

---

## The Lenses

### Stakeholders

Who is **affected** (direct / indirect / future / non-human if ecologically relevant)? **Vulnerability** — describe dependence, cognitive load, or marginalization in plain language and one sentence on why that raises duty-of-care or caution (justify from context; do not stereotype).

### Values

Which **values** are in play (autonomy, beneficence, non-maleficence, justice, dignity, solidarity, etc.)? Map **value tension** pairs: **A vs B** — why both matter here.

### Harms / Benefits

Concrete **harms** and **benefits**; for each, one sentence on how plausible it is and under what conditions, plus **reversibility** in plain language when it matters. Distinguish **predicted** vs **observed** (if user gave history).

### Justice / Power

Distribution of **burdens and boons**. **Power asymmetry** — who can say no, who bears error cost? Note **procedural** fairness (voice, consent, appeal).

### Options

2+ ethically distinct paths (including **do not proceed** if plausible). For each:

> **Option:** … — **Value fit:** … — **Residual harm:** … — **Safeguards:** …

### Recommendation

State a **preferred** option if the analysis supports one, or **conditional** guidance. Include **dissenting consideration** — strongest reason against your recommendation. Add **monitoring** — what to watch if you proceed.

---

## Execution Rules

1. Do not **demonize** actors; focus on structures, incentives, and foreseeable effects.
2. If values irreconcilably clash, say so — recommend **process** (deliberation, oversight) not fake unanimity.
3. Never invent sensitive personal attributes about real people; stick to user-supplied facts.
4. This skill is **not legal advice**; when law may bind, flag **legal review needed** and keep analysis non-authoritative on legal outcomes.

---

## Checklist (verify before responding)

- [ ] Setup: focal action + default pass (note if harm-scan style compression)
- [ ] Stakeholders include indirect/future if relevant
- [ ] At least one explicit **value tension** pair
- [ ] Harms/benefits state plausibility in plain language (no Low/Med/High scale); options have safeguards
- [ ] Justice/power addresses distribution and voice/consent
- [ ] Recommendation names residual harm and dissenting consideration
