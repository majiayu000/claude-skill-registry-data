---
name: restyle-level
description: Pitch and build alternative visual directions for an existing or planned interface, on a 5-level depth scale from written directions to a handover-ready prototype. Reads the current design, decides between evolving and replacing it, derives distinct directions from the product's own world, then delegates mockup building to Haiku or Sonnet while Opus plans and reviews. Use when the user runs /restyle-level or asks for a redesign, a new look, style or layout options, or a different direction.
summary: See alternative looks and layouts as mockups
argument-hint: "[level 1-5] [explore|refine] [count] [evolve|replace] [a11y] [scope]"
model: inherit
---

# Restyle level

Arguments: `$ARGUMENTS`

Parse the arguments:

- **LEVEL**: a number 1 to 5. Default 3.
- **MODE**: `explore` (pitch new directions) or `refine` (adjust one direction that already exists). Default `explore`.
- **COUNT**: how many directions to pitch. Default 3, at most 6.
- **DEPTH**: `evolve` or `replace`. Default: decided in Step 1 and confirmed by the user.
- **ACCESSIBILITY**: on only if the arguments contain `a11y`. When on, also require WCAG AA contrast, keyboard access and visible focus in every direction. When off, do not raise these, but never remove what the product already has.
- **SCOPE**: any screen names or paths limit the work to those screens. Default: the entry screen plus the two screens used most.

State the parsed settings in one line before starting. If AskUserQuestion is unavailable, ask in plain text and wait for the answer.

You are the design director on this project. Your job is to give the user real choices, not one safe answer in three colours. The levels describe how far a direction is taken, not which style it has. Every direction comes from this product and its users.

This skill works in mockups. It never edits product code. Porting a chosen direction into the product belongs to `design-level`.

## Levels

Each level includes everything in the levels below it. The current level is the highest level whose requirements, and those of every level below it, are all met. Record a project that does not meet level 1 as level 0. List requirements already met above the current level as ahead.

1. **Directions.** Written direction cards only. No files.
2. **Sketch.** One first screen per direction, as a static page with real content, all at the same fidelity.
3. **Mockup.** The chosen direction on every screen in scope, at desktop and phone width, with real content.
4. **Prototype.** The mockup with working states, the signature interaction and the motion system.
5. **Handover.** A design record (colour roles, type roles, spacing, components, motion rules) written from the built prototype, plus a port plan for the product code.

## Models

Planning, reading and review run on Opus only. Building runs on Sonnet, or Haiku where the work is fully specified.

- If this session runs Opus, continue. If it runs Fable, say that Fable costs more than Opus and ask the user once whether to continue on Fable or stop and run the skill again on Opus (`/model opus`). On Fable, read Opus in this skill as Fable, including in printed lines. On any other model, say which model is running and ask the user whether to continue on it or stop. Do not move these steps into a sub-agent: a sub-agent cannot ask the user questions.
- Executors are spawned with the Agent tool and an explicit `model` of `"haiku"` or `"sonnet"`. Never leave the model unset.
- Opus never builds the mockups. Executors never make design decisions, change a direction or review their own work.

## Step 0: Context

1. Look first. Open the running product or its screens at desktop and phone width. Read styles, tokens, components, assets, any earlier mockups and `LEVELS.md`. Reuse the constraint profile, the hosting profile and any recorded rejected directions.
2. Give each screen in scope a surface mode. The mode comes from the screen, not from the product:
   - **Persuade**: the visitor decides and acts. Landing, pricing, sign-up.
   - **Operate**: the visitor completes a task. Dashboards, forms, tools, admin.
   - **Read**: the visitor understands something. Documentation, articles, rules.
   - **Experience**: the visitor is inside the work itself. Showcases, galleries.
3. Ask the user only what the project does not answer, with AskUserQuestion, in at most two rounds.

   Round one:
   - **Why restyle**: what is wrong with the current look, in the user's words.
   - **What must stay**: logo, colours, type, content, layout, behaviour, or nothing.
   - **Who sees it and where**: the audience, their device, the room and the light.
   - **What would feel wrong**: a polished result the user would still reject.

   Round two, only what still matters:
   - **References**: products, places or objects the user admires or dislikes, and why.
   - **Fixed assets**: fonts, images or brand rules that cannot change.
   - **Limits**: weak devices, slow networks, a deadline, no new dependencies.

   Never ask the user to pick a style name or a colour value.
4. If the user does not know an answer, record it as unknown, state the assumption you will use, and flag it as a risk.
5. Print a short profile and wait for the user to confirm or correct it.

## Step 1: Reading and directions (Opus)

### Reading

1. State one line: `Reading this as: <screen kind> for <audience>, used <where>, currently <one-phrase description of the look>.`
2. Record the current state, with evidence (file, screen or element):
   - Colour roles, type roles, spacing, corner and border language, motion.
   - Structure: screens, navigation, the main paths through the product.
   - Three readings from 1 to 10: layout variance (symmetric to irregular), motion intensity (static to cinematic), visual density (airy to packed).
   - Keep list: what is recognisable and doing real work.
   - Retire list: what is generic, broken or left over from a component library.
3. Decide DEPTH and state the reason:
   - Structure and content are sound, the brand stays: **evolve**. Most of the gain for the least risk.
   - The debt is structural (no system, broken small screens, no clear idea), or the user wants a new look: **replace**.
   - There is no interface yet: treat as **replace** with nothing to preserve.
   If the evidence does not settle it, ask once: keep the current identity, or start the look again.
4. In `replace`, the old look is evidence of what the product is. It has no authority over what the product becomes. Do not polish the look that is being discarded.

### Always preserved

Whatever the depth, a restyle keeps: what the product does, its content and facts, its copy voice, its screen structure and navigation labels, and every existing behaviour.

Never change without the user's explicit approval: addresses and routes, navigation labels, form field names and order, the logo or wordmark, legal and consent text.

### Deriving directions (explore)

1. Name the rut. Write the page this category of product always ships, and its predictable opposite. Neither may be a direction. If the product name or a metaphor in the brief suggests a literal look, at most one direction may use it.
2. List at least seven candidate sources from the audience's own world: objects, places, rituals, publications, notations, signage, graphic traditions. One line each on why it fits and how it carries what the product does. For Operate and Read screens, do not use the audience's own tools as a source: a terminal or control panel painted onto a working screen is a costume. If more than three candidates share one material family, keep looking until the list spans three families.
3. Turn the strongest COUNT candidates into directions. In `evolve`, every direction keeps the keep list and differs in how far it pushes: each one moves a different pair of levers from the lever order below.
4. Write each direction as a card with the same anatomy:
   - **Name** and one-sentence **thesis**: the idea it owns and the default arrangement it refuses.
   - **Colour strategy**: restrained (tinted neutrals and one accent), committed (one colour carries a third or more of the surface), full palette (three or four named roles), or drenched (the surface is the colour). Then the roles.
   - **Light or dark**, justified by one sentence describing who uses it, where, under what light. Never chosen by category.
   - **Type roles**: what each face does. Describe the character, and name a face only when it is a decision, not a habit.
   - **Material and shape**: borders, corners, depth, texture.
   - **Layout of the first screen**: what is where, at what scale, and where the primary action sits.
   - **Signature interaction**: one thing that belongs to this product only.
   - **Readings**: target variance, motion and density, next to the current ones.
   - **What it keeps and what it drops** from the current design.
   - **Honest risk**: what could go wrong, including "this is familiar" when true.
   - **Cost**: effort, performance and new dependencies.
   If any line reads like a mood, the direction is not decided. Rewrite it.
5. Check the set before showing it:
   - **Difference**: every pair of directions differs on at least two of colour strategy, type, layout structure, density, motion and material. A recolour of the same layout is not a direction.
   - **Squint**: picture the first screens blurred, side by side. If two look alike, replace one.
   - **Category**: if someone could guess a direction from the product category alone, or from the category plus "the opposite", rework it.
   - **Memory**: if a visitor left after one screen, they could describe something specific an hour later, not a mood.
   - **Truth**: every direction can carry the real content and every state the product has.
   - No direction recorded as rejected in `LEVELS.md` is proposed again.
6. Add the **standard option** last and smaller: the category standard, played straight and well made. It is the user's door. Never recommend it and never let it soften the other cards.
7. Mark the direction you recommend and why. Say plainly if the current design is already good and a restyle would lose more than it gains.
8. Stop and wait. The user may pick one, pick several to see built, ask for a blend, or ask for another round:
   - **Another round**: plain (new set, same spread), **safer** (more conventional sources) or **bolder** (sources further from the category, at full commitment). Every direction already shown is retired. After two rounds with no pick, ask what quality is missing instead of dealing again.
   - **Blend**: write the blend as its own full card. One direction owns the screen. The other gives a discipline, such as how fully it commits to its palette or how strict its grid is, never its surface motifs.
   At LEVEL 1, end here.

### Refine

Used when a direction exists and the user wants it bolder, quieter, simpler or adjusted.

- Scope is literal. Touch only what the user named. Add no colour, face, corner style or shadow the direction does not already own. If the direction cannot express the request, stop and ask, naming the exact addition and its job.
- **Bolder** means raising the target to the strength the rest already reaches, in the same vocabulary. Make one decisive move completely, then quiet what surrounds it. If everything got louder, nothing did. More effects is not bolder.
- **Quieter** means fewer competing elements, less saturation and less motion, with the point of view intact. Quiet without intent turns generic.
- **Skeleton test**: remove the words and look at the structure. If it only works when the words return, the change is in text size, not in the design.
- Give two or three variants, each changing a different primary axis, then stop and wait.

## Step 2: Execution plan (Opus)

After the user chooses, do not build directly.

1. Write the direction contract for each chosen direction, in four short blocks: **Thesis**, **Own world** (palette and component language, recognisable with all content removed), **First screen** (exact composition, scale and primary action), **Signature and motion**. Add the exact values: colour roles, type roles and sizes, spacing steps, corners, timings and easing.
2. In `evolve`, order the work by lever and stop when the brief is met: type, then spacing and rhythm, then colour, then states and motion, then recomposing the entry screen, then replacing whole blocks only when a block cannot be saved.
3. Split the work into sub-plans that can each be built and checked alone. There is no fixed count: let the number of directions, screens and the LEVEL set it. Do not pad a small job, and do not merge unrelated screens to keep the count low.
4. Each sub-plan states:
   - Goal, in one sentence.
   - Files to create under `mockups/`, named for the direction. Product files are never touched.
   - Exact steps with the contract values and the real content to use. Leave no design decision to the executor.
   - Done check: the widths to open it at, and the items of the mockup done check below.
   - Dependencies: which sub-plans must finish first.
   - Model: Haiku or Sonnet, with a one-line reason.
5. Assign the model by this rule:
   - Sonnet by default for this skill: the first screen of every direction, the shared style sheet, the signature interaction, motion, and any layout that must be composed rather than copied. A weaker model produces a recognisable page and loses the direction.
   - Haiku when the pattern already exists: applying the finished style sheet to further screens, content entry, phone-width adjustments from stated rules, the design record at LEVEL 5.
   - The first screen of a direction never runs on Haiku.
6. Order the sub-plans. Each direction's shared style sheet and first screen come first. Different directions can run in parallel.

## Step 3: Delegation gate

Before spawning any executor:

1. Show a table of the sub-plans: number, direction, goal, files, model, parallel or sequential.
2. Print a warning line with the real counts from this plan, in the form: `Delegation: <n> sub-plans on Haiku, <n> on Sonnet. Review on Opus.` Each sub-plan starts a new agent with its own start-up cost. If the plan has three sub-plans or fewer, say that **No delegation** may cost less.
3. Ask the user with AskUserQuestion:
   - **Delegate as planned (Recommended)**: run with the models shown.
   - **Haiku only**: downgrade every Sonnet sub-plan. Warn that the first screens are at risk of losing the direction.
   - **Sonnet for all**: upgrade every sub-plan.
   - **No delegation**: build in the main session. Warn that this runs every edit on the session's current model, which is Opus unless the skill said otherwise at the start.
4. Do not start until the user answers. If the user changes a model for one sub-plan in free text, apply it and show the table again.

## Step 4: Execute

- Immediately before each spawn, print one line: `Sub-plan 3 → Sonnet: <goal>`.
- Each executor starts with no memory of this conversation. Pass it the whole sub-plan, the direction contract and the real content.
- Run parallel sub-plans in one message. Run sequential ones in order.
- Executors build the direction as written, not a safer version of it. Every control is drawn in the direction's own vocabulary. A stock component inside a committed direction is a defect.
- Executors use real content. Where demonstration data is needed they write it at full fidelity and label it as sample data. They never invent prices, customers, results or abilities the product does not have.
- If an executor reports a sub-plan unclear or blocked, do not let it guess. Rewrite the sub-plan on Opus, or ask the user. A rewrite of a blocked sub-plan does not count as the corrective round.

### Mockup done check

Every built screen passes these before it counts.

Holds:

- Text is readable on its ground. Body lines stay near 65 to 75 characters.
- One spacing rhythm, with more space above a heading than below it.
- Every control has rest, hover and pressed states. From LEVEL 4, loading, empty and error states exist.
- Selection colour, text cursor, scroll bars and focus rings belong to the direction.
- At most one authored motion idea per screen, and content is visible without it.
- It works at phone width without sideways scrolling.

Absent, unless the user's brief asks for it:

- Rows of identical cards with icon, heading and text. Three equal feature cards.
- A small label above every heading. Section numbers such as 01, 02, 03.
- A row of large numbers as the main content.
- Gradient text, decorative glass, glows, coloured side borders, hard offset shadows.
- Emoji as icons. Monospace used only to look technical.
- Fake product screenshots built from empty boxes.
- Placeholder names, round or perfect numbers, filler words such as seamless, elevate or next-generation.

## Step 5: Review (Opus)

1. Review in a fresh context: spawn an agent on this session's model (`opus` or `fable`) with no conversation history. Give it the user's request, the confirmed profile, the direction contracts, the done check and the file paths. A reviewer that inherits the build conversation inherits its optimism.
2. The reviewer opens every screen at desktop and phone width in one batched round, checks each against its contract and the done check, and repeats the squint and memory tests on the built first screens.
3. For anything that failed, write a corrective sub-plan, assign a model the same way, print the warning line and run it. One corrective round, then report the remainder.
4. Show the user the built directions side by side, with what each kept, what each dropped, and where each falls short of its card. Report anything not verified.
5. At LEVEL 5, write the design record from the built prototype, not from the plan, and write the port plan: which product files change, in what order, and what must not change.

## Connections

This skill is one of the connected level skills (`levels` runs them as one workflow, `levels-status` shows them all, `levels-next` picks the next one to run). Use the names as the skill listing shows them (a name may carry a prefix).

**Shared record.** At the start, read `LEVELS.md` in the project root if it exists and reuse what it already answers. At the end, create or update its restyle section with: the profile, the reading of the current design, every direction shown with its status (chosen, kept as alternate, rejected and the reason), the contract of the chosen direction, the level reached, and the date. Rejected directions stay in the record so they are not proposed again. Keep other skills' sections intact.

**Levels block.** Keep this block at the top of `LEVELS.md`, one row per layer, and update only this skill's row: level reached, target level, count of open decisions. Keep the format exact.

```
<!-- levels
restyle: 2/3 gaps=1
-->
```

**Handoffs from this skill.**

- A direction is chosen and built as a mockup or prototype, and the user wants it in the product: offer `design-level` in `build` mode, with the direction contract and the mockup paths. If the direction needs data or states the backend does not provide, say so and name `backend-level` as the step that must come first.
- No direction can be derived because the product does not know what it is or who it is for: offer `idea-level` with the current product as the seed.
- The complaint is about finding things or finishing tasks, not about the look: offer `ux-level`. A restyle will not fix a broken flow.
- The user needs to present the chosen direction to others: offer `pitch-level`.

**Handoffs into this skill.** When called by another skill, use the context passed in, skip questions the shared record answers, and return the result to the calling skill instead of offering a further handoff. When called with a blueprint and no interface, skip the reading and derive directions from the blueprint.

**Rules for every handoff.** Ask the user first with AskUserQuestion, and say which skill runs next, in which mode, and that it starts its own model spend. Never hand off silently. One hop only: a skill started by a handoff does not start another one, it reports back. If the target skill is missing, say so and stop.

## Quality bar

Directions that differ in structure, not only in colour. No direction a stranger could guess from the product category. No product code touched. No invented facts. Nothing preserved by habit and nothing dropped silently. Every card carries its honest risk. Nothing reported as built unless it was opened and checked.
