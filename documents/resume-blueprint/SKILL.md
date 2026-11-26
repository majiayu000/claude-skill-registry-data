---
name: resume-blueprint
description: Given a target company (and optionally a role), produce a company-specific resume blueprint covering what that company's screen looks for, the sections and order to use, which of the candidate's projects and experiences to lead with, must-have keywords, bullet templates tuned to the company's values, what to cut, and a fill-in-the-blanks resume skeleton built only from the candidate's real experience. Use when the user asks "what should my resume have for Google/Amazon/Microsoft/…", wants to tailor their resume to a company, or asks for a resume reference or template for a specific company.
---

# Resume blueprint

"What should my resume look like for <Company>?" deserves a better answer than a generic template. This skill combines what the company's screen rewards with the candidate's **real** material, and produces a resume plan they can fill in today.

## 0. Inputs

1. Call the Skill tool with "cracked-profile" (level, roles, resume path).
2. Company: from the request. If none is given, ask for it in one line. This skill only exists for company targeting; for a general review, point them to `/roast-my-resume`.
3. Role: from the request or profile. Default to the profile's first target role.
4. Call the Skill tool with "company-intel" for the company. You need the **Resume screen**, **Values** and **DSA focus** sections.
5. Read their current resume if there is one (same reading rules as `roast-my-resume`). The blueprint is far better with it, but it still works without one.

## 1. What this company's screen rewards

Write 5–8 bullets, each tied to a source in the brief (the company's careers page, published values, or reported experiences), or to its archetype, labelled as such. For example:

- "Impact at scale, quantified: bullets with users, latency or throughput numbers (big-tech archetype; consistent with reported screens)."
- "Ownership and bias for action map to the published Leadership Principles, so frame bullets as *you* deciding and delivering."
- "For new-grad SDE roles, DSA proof is a strong signal, given that their OA is reported as 2 medium–hard problems."

Then list **what it doesn't care about** (cut these): e.g. a long skills dump, an objective statement, non-technical hobbies, certificates without projects.

## 2. The blueprint

1. **Section order** for this company, role and level, with a one-line reason each.
2. **Lead with**: which of their projects and experiences go first, and why, mapped to what the company values. Flag any project that hurts more than it helps here.
3. **Must-have keywords** for this role at this company, drawn from its JD language and stack. Mark each `✅ you have it` / `🟡 true but missing from resume` / `❌ gap`. Only `✅` and `🟡` go on the resume; `❌` goes to the prep list.
4. **Bullet templates in this company's language**: 4–6 templates showing how to frame *their* real experiences, e.g. `Led <project> end-to-end, choosing <tech> over <alt> to <reason>; shipped to [N] users, cutting <metric> by [X]%` (ownership and impact).
5. **Proof to add before applying**: the 1–3 highest-leverage things they could add in under 2 weeks (a contest rating, deploying an existing project, one metric they can actually measure), each tied to a cracked skill (`/make-it-hireable`, `/github-glowup`).

## 3. Resume skeleton

Write `$CRACKED_DIR/resume/<company>-blueprint.md`: a full one-page resume skeleton in Markdown, in the recommended order, **pre-filled only with facts from their resume or profile**, with `[placeholders]` everywhere else, plus a `<!-- why -->` comment on each section explaining the choice. Mention that it converts cleanly to a single-column PDF (e.g. `pandoc`, or paste it into a plain single-column template).

## 4. Close

- 3-line summary: the bar, their biggest gap against it, and the first fix.
- Offer: `/roast-my-resume` (after they fill it in), `/jd-match` (once they have a specific JD), `/oa-sim <company>`.

## Rules

- **Never fabricate.** No invented experience, metrics, or "what <Company> secretly wants". Everything is sourced, archetype-labelled, or comes from the candidate.
- Company facts come only from the `company-intel` brief. If the brief says `unverified`, say the same here.

---

*Skill calls:* if your agent has no Skill tool, open the named skill's `SKILL.md` in the cracked skills folder (`core/`, `interview/`, `profile/`, `strategy/`) and follow it instead.
