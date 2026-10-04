---
name: revise-best-practice-skill
description: Use when an existing SKILL.md has review-best-practice-skill findings to address, a citation has become inaccurate, steps reference an outdated tool, or scope needs adjusting — splitting a skill that covers two concepts, or expanding one that is too shallow.
source: IETF RFC errata process (BCP 9), MDN Web Docs contribution guidelines, Wikipedia article improvement process
tags: [skill-revision, quality-debt, targeted-fix, contributor, maintainer, review-pass]
---

# Revise Best Practice Skill

Update an existing grimoire SKILL.md to resolve specific findings without touching validated content.

## Why This Is Best Practice

**Adopted by:** Targeted revision of specific findings is the standard maintenance model across all long-lived technical documentation systems — IETF errata correct specific claims in RFCs without replacing the full document, MDN Web Docs uses targeted pull requests per section rather than full-article rewrites, and Wikipedia's peer review process improves articles through iterative section-level fixes rather than wholesale replacement.
**Impact:** Targeted revision preserves validated content while addressing gaps — wholesale rewrite discards working sections and resets review history unnecessarily. Aghajani et al. (2019, MSR) found that the vast majority of documentation fixes in OSS projects are targeted single-section changes; wholesale rewrites are rare and reserved for fundamental practice changes. The IETF errata model demonstrates that long-lived technical documents can remain accurate for decades through targeted correction while full replacements introduce regression risk across all sections.
**Why best:** Fixing only flagged findings — vs. refactoring the whole file "while you're there" — prevents introducing new issues in sections that were already PASS. A full rewrite is the alternative; it costs more, discards verified content, and risks new failures in sections that passed.

Sources: IETF RFC errata process (BCP 9), MDN Web Docs contribution guidelines, Wikipedia article improvement process, Aghajani et al. 2019 (MSR documentation debt)

## Steps

### 1. Load findings

Get the finding set:
- review-best-practice-skill already run → use its structured output directly
- No findings yet → run `review-best-practice-skill` on the file first; use its output
- Findings from user report (not review-best-practice-skill format) → map each to a review-best-practice-skill criterion name before proceeding

### 2. Classify each finding by type

| Finding type | Scope of fix |
|---|---|
| Frontmatter field (name, description, source, tags) | Frontmatter only — don't touch body |
| "Adopted by" inaccurate or vague | `## Why This Is Best Practice` only |
| "Impact" citation weak or fabricated | `## Why This Is Best Practice` only |
| Steps reference outdated tool or API | Affected step(s) only |
| Steps not actionable or too abstract | Affected step(s) only |
| Scope too broad (two separable concepts) | Split — see step 4 |
| Scope too shallow (<50 lines) | Expand Steps with concrete examples |
| Domain safety footer missing | Add footer only |

### 3. Order revisions: structural before content

**Structural before content:** Always apply structural revisions before content revisions.
1. First: fix step ordering, add/remove steps, fix routing logic, add missing required fields
2. Then: improve wording, strengthen examples, tighten descriptions

Structural changes invalidate content — if you improve wording in a step that will be removed, the content work is wasted. Structure is the skeleton; content is the flesh.

### 4. Fix each finding in isolation

Fix the flagged item. Don't touch adjacent text that wasn't flagged.

If the finding involves a citation, adoption claim, or a tool/API's current status, search the internet to confirm the corrected information is accurate before writing it in — don't replace one unverified claim with another. If no internet-access tool is available in this environment, say so explicitly and proceed on best available knowledge — flag the fix as unverified rather than silently skipping the check or asserting it was confirmed. After searching, state what was found (or that nothing conclusive turned up) before proceeding — don't just announce the check and discard the result.

```
❌ Citation wrong → rewrite entire Why section
✅ Citation wrong → replace the one sentence containing the citation
```

```
❌ One step vague → rewrite all steps for consistency
✅ One step vague → rewrite that step only
```

If fixing a citation requires changing the surrounding sentence for grammatical coherence, that is acceptable. Touching unrelated paragraphs is not.

### 5. Scope fix: splitting

If the finding is "skill covers two separable concepts":

1. Identify concept A (primary — stays in this file) and concept B (extract)
2. Remove concept B content from the current skill
3. Create a new directory for concept B's skill
4. Run `write-best-practice-skill` to author the extracted skill from scratch — do not copy the removed content verbatim; the extracted skill needs its own Why section, sources, and steps
5. Run `review-best-practice-skill` on both resulting skills

This is a scope reduction, not a deprecation. Do not add a deprecation notice to the concept A skill.

### 6. Verify: re-run review-best-practice-skill

After all fixes are applied, run `review-best-practice-skill` on the updated file:

- All previously flagged criteria now ✅ → proceed to PR
- New ❌ introduced by the fix → resolve before opening PR
- Previously PASS criteria now ❌ → the fix caused a regression; revert that change

### 7. Open a PR

PR title: `fix(<domain>/<skill-name>): <one-line description of what changed>`

PR description: one line per finding, stating what it was and how it was resolved.

**PR template:** When submitting a skill revision as a PR, title format: `fix(skills): [what was fixed] in [skill-name]`. Body must include:
- What finding triggered this revision (quote the NEEDS-REVISION finding)
- What was changed (structural or content)
- Any STANDARD.md criteria newly passing after the revision

## Rules

- Never fix what wasn't flagged — scope creep in revision introduces regressions
- One PR per skill — if multiple skills need revision, open separate PRs
- Always re-run `review-best-practice-skill` after revision — don't assume the fix resolved the finding
- Splitting is a revision, not a deprecation — do not mark the original skill as deprecated
- If a finding cannot be resolved without invalidating the skill's core claim, use `deprecate-best-practice-skill` instead

## Common Mistakes

**Rewriting the whole skill for one citation**: fix the citation sentence; leave everything else.

**"Improving" unflagged sections**: if review-best-practice-skill didn't flag it, don't touch it — even if you'd write it differently.

**Skipping re-verification**: a fix can introduce a new failure. Always re-run review-best-practice-skill after editing.

**Treating scope reduction as deprecation**: splitting a skill that was too broad is a fix. Both resulting skills live on — neither is retired.