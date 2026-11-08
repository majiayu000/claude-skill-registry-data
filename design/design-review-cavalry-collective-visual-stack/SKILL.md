---
name: design-review
description: Audit the UI and UX of what we are working on at a chosen level of polish, open the proposed changes in vstack:review for comments, then build what the owner approves. Product code stays untouched until approval. New UI copy goes to ChatGPT through vstack:proofread where the host supports it. Use when the user invokes /vstack:design-review or $vstack:design-review, asks for a design review, design audit, UI or UX review, or another review round, or wants a screen or app to look more polished, premium or consistent, even if they do not say "review". To comment on a wireframe, page or running app with no audit, use vstack:review.
---

# Design Review

Audit first, propose second, build after the owner approves. The owner comments on the proposal in vstack:review before any product code changes.

Read `lenses.md` before Step 3 and `report.md` before Step 4. Both sit beside this file.

## Host

Follow §0 of `../review/SKILL.md` to load the adapter for your host. This skill uses the Host ops `run`, `edit` and `browser_capture`, defined in `contracts/host.md`.

## Step 1: Set the scope and the polish level

The skill runs inside a conversation, so take the target and any focus areas from the current work. Ask only if the conversation leaves the target unclear.

Ask which level of polish this review should aim for, unless the owner has already said:

| Level | Aim |
|---|---|
| **Clean** | Consistent and easy to use. Clear hierarchy, spacing and type, every state handled, and the design system followed. No new effects. |
| **Refined** | Clean, plus a premium feel. Considered depth, small interactions, and a transition on every state change. |
| **Showcase** | Refined, plus thoughtful animation, special effects and moments of delight. |

The level decides which lenses apply and how far each proposal goes. Do not propose effects above the chosen level.

If `.vstack/local/design-review/` holds an earlier round for this target, also follow **Later rounds** below.

## Step 2: Read the current instructions

Read the project instructions and anything design-related: the design guide, frontend contract, token file and stylesheets. Then read the code for the screens in scope. The review must fit the rules the project already has.

## Step 3: Look at the work

Open whatever we are working on, whether that is a dev server, a preview or a live site, with `browser_capture`. Choose the screen sizes, themes and states from the requirements.

If the adapter says `browser_capture` is not available, ask the owner for screenshots of each screen and take sizes from the stylesheets. Say in the page footer what you could not measure.

Collect evidence:

- Screenshot each screen, and save the images a finding will need.
- Measure with JavaScript in the page: `scrollWidth` against `clientWidth`, heights, counts, font sizes, contrast. Use numbers in findings, because "33 cards, 4,312px" can be acted on and "feels heavy" cannot.
- Stress the layout with the longest title, the largest list and an empty list. Check for sideways overflow.
- Read the console for errors, where the host's browser tools can reach it.

## Step 4: Write the review and open it for comments

1. Write the findings with the lenses for the chosen level:
   - Name the weakness, with its evidence and its location in the code.
   - Propose a concrete change with values, such as "13.5px, weight 600, two-line clamp".
   - Show the finding visually: a before and after comparison, or a screenshot with a red box around the area. See `report.md`.
   - Report one finding per kind of defect.
   - Mark **Owner's call** on any change to something the owner clearly chose. Offer a way to keep the idea.
   - Say what already works, so the owner knows what to protect.
2. Build the review as one self-contained HTML page, in the format in `report.md`. Save it as `.vstack/local/design-review/<target>-round-<n>.html`, from the project root.
3. Read `../review/SKILL.md` and start at §3, with the review page as `$FILE`. Follow its comment loop. Use the page form of the review, because each comment changes the review page. Do not use §7, which changes source.
4. Reply in chat with the verdict and the top changes.

Product code stays unchanged until the owner chooses **Approve & finish** or says to build.

## Step 5: Build

Build what the owner approved, one slice at a time.

- Follow the target repo's own workflow for specs, branches, tests and release.
- After the tests pass, look at the slice in a browser with long content and real-sized data.
- Run `vstack:proofread` on any new UI copy, by reading `../proofread/SKILL.md` and following it. Running design-review counts as the request that skill requires, for UI copy only. Do not run it on the review page.
- If proofread stops, do not send the copy. It stops on secrets, credentials or personal data, on a host without `user_browser`, and on a browser that is not connected or not signed in. Tell the owner why it stopped and continue the build.
- Report after each slice: what changed, how you verified it, and what you left out.
- Ask first if a change alters what a screen is for. Moving a type of item off the main board is one example.

## Later rounds

A later round reviews the result of the last plan. Earlier fixes can create new problems or move an old one elsewhere. Read the last round's page, and save this round under the next number.

- Mark each earlier area **Landed**, **Landed, broken** or **Moved**.
- List bugs the slices introduced first. Fix a bug that blocks use in its own small change.
- Look for what the fixes made louder.
- Carry forward items left out of the last plan.
- End with one plan, and say where you would stop polishing.

## Notes

- **Browser pass.** Tests miss layout faults. In the first run, visual passes caught overflowing tabs and hidden filter chips. A long title that made the panel scroll sideways shipped because no test used one.
- **Louder after a fix.** In the first run, removing the empty grey cells left one 4,312px column as the heaviest thing on the board.
