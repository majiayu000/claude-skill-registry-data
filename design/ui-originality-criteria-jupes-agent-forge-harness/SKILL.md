---
name: ui-originality-criteria
description: Grade and steer UI work using Anthropic-style design dimensions—coherence, originality, craft, and usability—for generators and evaluators.
---

# ui-originality-criteria

Use when **building or reviewing** user-visible UI (marketing pages, dashboards, app shells, flows). Encodes the four grading dimensions from [Anthropic — Harness design for long-running application development](https://www.anthropic.com/engineering/harness-design-long-running-apps) so subjective quality stays **gradable** and **anti-“AI slop”**.

Pair with `.claude/protocols/evaluation-rubric.md` for harness-wide severity (BLOCKER / HIGH / …); this skill is the **product-design lens**.

---

## The four dimensions

### 1. Design quality (coherent whole)

**Question:** Does the layout feel like one intentional system—not a pile of unrelated components?

**Strong:** Color, type, spacing, imagery, and motion share a clear mood; hierarchy tells a single story.

**FAIL signals:** Mismatched radii/shadows; competing focal points; “default component” look with no unifying thread.

---

### 2. Originality (deliberate choices)

**Question:** Would a human designer see **custom decisions**, or stock templates / library defaults / clichéd AI patterns?

**Strong:** Distinct typography pairing, palette, or layout rhythm tied to the product’s domain.

**FAIL signals:** Unmodified stock cards; purple-on-white hero gradients “because SaaS”; generic three-column icon grids with lorem tone; interchangeable with ten other AI landing pages.

---

### 3. Craft (technical execution)

**Question:** Are fundamentals solid—type scale, spacing rhythm, contrast, alignment?

**This is competence, not creativity.** Most honest implementations pass unless something is broken.

**FAIL signals:** Illegible contrast; broken hierarchy; ragged grids; tap targets too small; obvious misalignment.

---

### 4. Functionality (usability without relying on beauty)

**Question:** Can a user understand what the UI does, find primary actions, and complete tasks without guessing?

**FAIL signals:** Hidden primary actions; misleading labels; dead ends; keyboard traps; unclear empty/error states.

---

## Weighting (from the article)

When **both** generator and evaluator see these criteria, bias feedback toward **design quality** and **originality** first—Claude often scores **craft** and **functionality** well by default. Use **craft** and **functionality** as hygiene gates, not as excuses to ship bland work.

---

## Generator rules

1. Pick **one** clear visual metaphor (e.g. “mission control”, “workshop”, “terminal calm”) and thread it through nav, surfaces, and accents.
2. **Avoid** the banned patterns in Originality unless the spec explicitly demands them.
3. After a first pass, self-check against all four bullets in writing before requesting evaluator review.

---

## Evaluator rules

1. **Assume** generic patterns until disproven—require evidence (screenshots, DOM notes, contrast checks).
2. Cite **which dimension** each finding belongs to.
3. If UI-heavy AC exists, treat **Originality** + **Design quality** gaps as at least **HIGH** when the spec asked for a distinctive or branded experience.

---

## References

- Anthropic article (full context): https://www.anthropic.com/engineering/harness-design-long-running-apps  
- Harness evaluator rubric: `.claude/protocols/evaluation-rubric.md`  
- Example dashboard applying this lens: `docs/index.html` (Agent Forge static dashboard — NASA retro / space-console theme)
