---
name: refinement-pass
description: Decide whether a design needs a redesign or a refinement, and when it's a refinement, keep the structure and fix only the few things that are actually wrong. Diagnose, rank, fix the top three, check by screenshot, stop. Use when a page is close but not right, when feedback says "something feels off", or when a project keeps getting redesigned without getting better.
---

# /refinement-pass

The most common way an agent ruins a good design is by answering criticism with a new design. Someone says "it feels generic", and the reply is a new art direction, a new section grammar and a new layout. Each round is different. None is better. The parts that worked are lost along with the parts that didn't.

This skill is the opposite habit: find out what is actually wrong, fix that, and leave the rest alone.

## Purpose

Turn vague dissatisfaction into a ranked list of specific problems, decide whether each one is structural or local, and fix the smallest set of things that makes the page right, without discarding what already works.

## Use when

- A page is close: the direction is right, but something is off.
- Feedback is a feeling ("it looks basic", "it's too much", "it doesn't feel like us") rather than a list.
- The same page has already been redesigned two or more times.
- You're tempted to start over.

## Don't use when

- There is no design yet. Use `/art-director` or `/landing-page-art-director`.
- The structure itself is wrong and the diagnosis says so. Then a redesign is the right call. Do it once, deliberately.
- The task is a bug, a defect or an accessibility failure. Fix it directly, or use `/responsive-audit` or `/accessibility-pass`.

## Inputs

Before changing anything, collect:

1. **Screenshots of the current page** at 390, 768, 1280 and 1920 wide, full page and first screen. Judge what's rendered, not the code or the plan.
2. **Every piece of feedback, word for word.** Note which parts are observations ("the cards are all the same size") and which are feelings ("it's boring").
3. **What has already been tried,** if the page has a history. A change that was made and reverted is information.
4. **What works.** Ask, or decide: which sections, components and choices must survive?

## Process

### 1. Name what works, first

Write down the three to five things that must not change. A good headline, a strong image, a clear navigation, a component that's the star. This list protects them from the fixes that follow.

### 2. Diagnose

For each piece of feedback, find the concrete cause on the screenshots. "It looks basic" might be:

- every section uses the same heading, grid and card;
- nothing is larger than anything else, so there is no hierarchy;
- the one distinctive element is too small to notice;
- the spacing is even everywhere, so there's no rhythm.

A diagnosis points at something you could circle on a screenshot. "It needs more personality" is not a diagnosis.

If you can't find a cause for a feeling, say so. **Discomfort without a diagnosis means you don't change anything yet.** Ask, look again, or compare against a reference first.

### 3. Classify each problem

| Kind | What it looks like | What to do |
|---|---|---|
| **Structural** | The page answers the wrong question, sections are in the wrong order, the main thing isn't the main thing. | A redesign of that part may be justified. Say so explicitly and keep it to that part. |
| **Local** | One section is weak, two elements compete, a size or a gap is off, one treatment is generic. | Keep the structure. Fix the element. |
| **Undiagnosed** | A feeling with no visible cause. | Don't change it. Investigate. |

Most problems are local. If everything looks structural, check that you aren't reacting to taste.

### 4. Rank and pick three

Order the problems by how much fixing each one improves the page. Fix the top three. Write the rest down and leave them.

Three is a rule, not a guideline. More changes at once make it impossible to tell which one helped, and they're how a refinement quietly turns into a redesign.

### 5. Fix with existing material

Fix each problem with what the project already has: its components, type scale, colours, spacing, buttons. Reach for something new only when nothing existing can do it, and check with `/design-system-consistency` first.

### 6. Check by screenshot, then stop

Capture the same four widths again and compare them with the originals (`/screenshot-iteration`). For each fix: did it solve the diagnosed problem, and did it break anything on the "what works" list?

Then stop. If problems remain, that's the next pass, with its own diagnosis.

## Acceptance criteria

- Every change traces to a written diagnosis that points at something visible.
- Nothing on the "what works" list changed.
- No more than three problems were fixed in this pass.
- Before and after screenshots exist at the same widths.
- The page's structure is unchanged, unless a structural problem was diagnosed and named.

## Common failure modes

- **Redesigning in response to taste.** "It feels generic" answered with a new art direction, when the cause was one oversized gap and a repeated card.
- **Over-correcting.** Removing a generic pattern by making every section a "moment": giant type, unusual grids, sticky layouts, extra whitespace. The page stops being generic and becomes noisy. (`/template-tells` covers this.)
- **Fixing everything at once.** Twelve changes, three regressions, no idea which change did what.
- **Losing the good parts.** A strong element disappears because it was inside a section being rebuilt.
- **Trusting the plan over the render.** A spacing value from a written plan is kept although the screenshot shows it's wrong.
- **Adding decoration to fix hierarchy.** A glow, badge or icon added to make one item "stand out", when the fix was size, position or space.

## Final self-review

- I can point at each problem I fixed on a screenshot.
- I fixed at most three things.
- Everything on the "what works" list is still there and unchanged.
- I used existing components and tokens.
- Before and after screenshots are at the same four widths.
- I wrote down what I didn't fix, for next time.

## Copyable instruction

```text
Do a refinement pass on this page, not a redesign.
1. Screenshot it at 390, 768, 1280 and 1920 wide.
2. List what already works; those things must not change.
3. Turn each piece of feedback into a concrete cause you can point at on a screenshot.
   If a complaint has no visible cause, don't change anything for it; say so.
4. Mark each problem structural (wrong order, wrong main thing) or local (one element, size, gap, treatment).
   Only a structural problem justifies redesigning that part.
5. Rank the problems by impact and fix only the top three, using the project's existing components and tokens.
6. Screenshot the same widths again and compare. Confirm each fix worked and nothing on the "works" list changed.
Do not introduce a new art direction, layout system or section style. List the remaining problems instead of fixing them.
```
