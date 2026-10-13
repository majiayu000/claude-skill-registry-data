---
name: ui-brief
description: Turn a vague UI idea into a structured product and design brief before any layout, component, or code work begins. Use this skill whenever a user describes a feature, screen, or product idea in loose terms ("I want to build a dashboard for...", "we need a login flow", "make a settings page") and wants to start designing or building. Always use it as the first step of any new UI work — even if the user seems eager to skip ahead to wireframes or code, because skipping the brief is the single most common cause of mismatched expectations between user and model.
---
# UI Brief

A skill for converting vague feature ideas into a precise, testable brief that downstream UI work can be traced back to. This is the foundation of the UI Specification Kit. Everything else — blueprints, components, code — should reference a brief produced by this skill.

## When to use this skill

Use this skill when:
- The user describes a feature in loose terms and wants to start building.
- The user says things like "I want a screen that...", "we need a flow for...", "build me a UI for...".
- Earlier conversation has produced design or code without a brief and the result missed the user's intent — a brief should be reconstructed before continuing.
- **Spec Recovery:** A UI implementation already exists but no specification was created. In this case, use the brief to recover the missing product and design intent.

Do **not** use this skill when:
- A brief already exists and is current. Read it instead.
- The user is asking a narrow technical question that doesn't require a product framing (e.g. "what's the WCAG contrast minimum?").

## Core principle

**A brief is not a wishlist. It is a constraint document.** Its job is to make decisions explicit so that downstream work (layout, components, code) cannot drift. If the brief does not constrain a choice, expect the model to invent one — so either constrain it or mark it as an open question.

## Anti-vague vocabulary

These words are banned from briefs unless translated into concrete choices:

| Banned word | Ask instead |
|---|---|
| modern | What concrete properties? Sans-serif type? Generous whitespace? Flat surface style? Name 1–2 reference products. |
| clean | Same as above. "Clean" usually means low information density and minimal chrome — say so. |
| intuitive | Intuitive for whom? Someone who has used what other tool before? |
| user-friendly | Friendly for which user? In what context? On what device? |
| sleek / beautiful / elegant | Drop the adjective and describe a concrete visual property. |
| simple | Simple compared to what? Fewer fields? Fewer steps? Less density? |
| professional | What signals professionalism in this context? Muted palette? Serif type? Dense data tables? |

When the user uses one of these words, ask them to translate it before proceeding. If they can't, mark it as an assumption (see Assumptions protocol below).

## Observed vs. Target (Spec Recovery protocol)

When using this skill to recover a brief from an existing UI (Retrospective Specification), every section must distinguish between what is **Observed** (the current code/UI) and what is the **Target** (the recovered intent).

- **Observed:** What the current implementation actually does.
- **Target:** What the user intended or what the spec says it *should* do.
- **Issue/Gap:** Any mismatch between Observed and Target.

Use this pattern in your reasoning and, where appropriate, in the brief's sections to prevent accidental implementation choices from being silently promoted to "official" design decisions.

## Workflow

### Step 1 — Pre-flight check

Before drafting, confirm you have answers to these. If any are missing, ask the user. Do not invent defaults silently.

1. **Who is the primary user?** Role, context, technical literacy, device. (Not "everyone".)
2. **What is the single most important action they take on this UI?** (One verb. If the user names three, push back and rank.)
3. **What problem does completing that action solve for them?**
4. **What is the success criterion?** Measurable if possible. ("User completes signup in under 60 seconds" not "signup feels easy".)
5. **What constraints exist?** (Brand, platform, regulatory, technical, time.)
6. **What is explicitly out of scope?** (At least one non-goal.)

If the user says "I don't know" to a question, that is a valid answer — record it as an open question. Do not fabricate one.

### Step 2 — Draft the brief

Use the template in the next section. Do not deviate from the structure — downstream skills depend on it.

### Step 3 — Validate against the acceptance criteria

Before delivering the brief, check it against the "Acceptance criteria for this skill's output" section at the bottom of this file. If any criterion fails, revise.

### Step 4 — Confirm with the user

End with a numbered list of every assumption made and every open question. Ask the user to confirm or correct each one. Do not move on to `ui-blueprint` or any other skill until the user has signed off.

## Output template

Always produce output in this exact structure. Save it as `brief.md` inside a `<feature-name>/` spec package folder. The folder name carries the feature slug — the file name is always `brief.md`. Do not rename it to `brief-<slug>.md`; downstream skills look for the canonical name.

```markdown
---
spec_type: brief
spec_id: <short-slug, e.g. "billing-overview">
created: <YYYY-MM-DD>
status: draft
---

# Brief: <descriptive title>

## 1. Goal
<One sentence. What does this UI exist to do? Not "help users with X" — say what changes in the world after a user completes the primary action.>

## 2. Primary user
- **Role / context:** <who they are and what they're doing when they hit this UI>
- **Technical literacy:** <novice | intermediate | expert; with one sentence of justification>
- **Primary device:** <mobile | desktop | tablet | mixed; with reason>
- **Accessibility considerations:** <any known constraints — low vision, keyboard-only, screen reader, motor, cognitive>

## 3. Primary action
<One verb. The single most important thing the user does here. If you have to write "and", you have two actions — pick the more important one and demote the other.>

## 4. Secondary actions
<Bulleted list, ranked. Anything beyond ~5 means the screen is doing too much.>

## 5. Why it matters
<What problem this solves for the user. One short paragraph.>

## 6. Success criteria
- <Measurable, testable. e.g. "80% of users who land on this screen complete the primary action without leaving.">
- <At least one quantitative if possible.>
- <At least one qualitative if quantitative is impossible.>

## 7. Constraints
- **Brand:** <existing identity, palette, type system to honor — or "none, greenfield">
- **Platform:** <web, iOS, Android, cross-platform; framework if known>
- **Regulatory / compliance:** <GDPR, HIPAA, accessibility legal requirements, etc., or "none known">
- **Technical:** <integrations, data sources, performance budgets>
- **Time / scope:** <deadline or scope constraints>

## 8. Non-goals (what this is NOT)
- <Bulleted list. At least one item.>
- <Things you might be tempted to add but explicitly will not.>

## 9. Open questions
- <Numbered list of decisions the user has not made yet.>
- <Each question must be specific and answerable.>

## 10. Assumptions made in this brief
- <If the user couldn't answer something and the brief proceeded anyway, list each assumption here with a ⚠️ marker.>
- <e.g. ⚠️ ASSUMED: Primary device is desktop because user mentioned "team uses this at work">
```

## Examples

### Example 1 — vague input, well-handled

**User says:** "I want to build a clean modern dashboard for my SaaS."

**Bad model behavior:** Starts drafting a brief based on assumed goals.

**Correct skill behavior:** Stop and ask:
1. What does your SaaS do, and who uses the dashboard?
2. What is the single most important thing a user does on this dashboard? (View metrics? Take an action? Configure something?)
3. "Clean modern" — name one product whose UI you'd point to as a reference.
4. What does success look like — what should the user feel or do after using it?
5. Mobile or desktop primary?

Only after answers proceed to draft.

### Example 2 — input rich enough to draft

**User says:** "Build a brief for a settings page in our team chat app where admins manage members. They need to invite, remove, change roles. We're a B2B SaaS, web only, our users are IT admins at mid-sized companies."

**Correct output:** Draft the brief. Likely open questions to surface:
- Bulk operations or per-row only?
- What's the team size range? (Affects whether pagination/search is required.)
- SSO — does role assignment integrate with an external identity provider?

These go in the **Open questions** section, not silently assumed.

## Rules that prevent hallucinated decisions

1. **Never name a reference product the user did not name.** If the user says "make it look modern", do not write "Stripe-style." Ask which product they want it to resemble.
2. **Never write a number unless the user provided it or it is a documented standard.** No invented user counts, no invented timelines, no invented performance budgets.
3. **Never resolve a contradiction silently.** If the user says "casual users" and "power-user features" in the same sentence, surface the contradiction in Open Questions.
4. **One primary action only.** A brief with two co-equal primary actions is a brief for two screens. Push back.

## Acceptance criteria for this skill's output

A brief produced by this skill is acceptable only if every one of these is true:

- [ ] All ten template sections are present (none deleted, none renamed).
- [ ] Goal is one sentence and describes a change in the world, not a feature description.
- [ ] Primary action is one verb.
- [ ] At least one success criterion is measurable.
- [ ] At least one non-goal is listed.
- [ ] No banned vague words (modern, clean, intuitive, user-friendly, sleek, simple, professional, beautiful, elegant) appear in the body unless followed by a concrete translation in the same sentence.
- [ ] Every assumption is flagged with ⚠️.
- [ ] Open questions are specific enough that a yes/no or single-word answer would resolve them.

If any check fails, revise before delivering.
