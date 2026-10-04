---
name: exit-eval
description: Structured stress-test evaluation of any exit scenario from the 95-scenario list. Interactive dialogue with the developer (who provides chef operational expertise) combined with rubric analysis. Picks or accepts a scenario number, presents it for developer stress-testing, synthesizes insights through the 7-question rubric, reclassifies it, and outputs a spec-ready evaluation. Use when evaluating exit points, planning round-trip UX, or batch-processing the exit scenario list.
user-invocable: true
---

# EXIT SCENARIO EVALUATION (Round-Trip Intelligence Engine)

Structured stress-test of ChefFlow exit scenarios. Every exit is a round-trip that must succeed 100%. The chef leaving is not the failure. The failure is friction, context loss, or data loss on the way out or back.

---

## INVOCATION

```
/exit-eval          -> pick random scenario from list
/exit-eval 58       -> evaluate scenario #58
/exit-eval batch    -> evaluate next 5 unprocessed scenarios
/exit-eval status   -> show progress (evaluated vs remaining)
```

---

## SOURCE FILE

The master scenario list lives at: `docs/research/chef-exit-points-analysis.md` (95 scenarios, 17 categories)
Reclassification results go to: `docs/specs/exit-scenario-reclassification-sprint.md`
Individual specs go to: `docs/specs/` (named by feature, not by number)

---

## INTERACTIVE MODE (Default)

This skill produces its BEST output through dialogue, not solo analysis. The developer is a 10+ year private chef. Their operational expertise reveals angles Claude cannot infer from data alone.

**The flow:**

1. **Claude presents** the scenario: number, title, category, what the master list says.
2. **Claude asks** one open question: "How do you handle this today? What would make it frictionless?"
3. **Developer reacts** with real chef operational knowledge (physical workflow, what they actually do, what annoys them, what the client experiences).
4. **Claude synthesizes** the developer's input + rubric analysis into the output format.
5. **If a spec is warranted**, Claude writes it incorporating the developer's exact language and design instincts.

**Why interactive:** The weather spec came from the developer saying "weather.com should just become a source." The venue spec came from "Street View is perfect." The mid-cook spec came from "you should just print it out." These product decisions require chef expertise Claude doesn't have.

**Solo mode (batch):** When running batch without developer input, Claude applies the rubric but marks output as `NEEDS-DEVELOPER-REVIEW` and flags scenarios where chef operational knowledge would change the classification.

---

## THE RUBRIC (7 Questions, Applied to Every Scenario)

For each scenario, answer these IN ORDER:

### 1. WHY DOES THE CHEF LEAVE?

Not the surface reason. The OPERATIONAL reason. What decision are they trying to make? What information gap are they filling? What action requires the external tool?

**Go deeper than the obvious.** "Check weather" is surface. "Decide whether to move cocktail hour indoors and adjust setup timeline" is operational.

### 2. WHAT CONTEXT DOES CHEFFLOW ALREADY HAVE?

List every piece of data ChefFlow possesses that's relevant:

- Event date, time, location
- Client name, preferences, allergies
- Menu items, recipes, ingredients
- Past events at same venue/client
- Chef's region, home address
- Financial data (quotes, payments)

If ChefFlow has 80%+ of the context needed, this is likely reducible.

### 3. IS THE EXTERNAL TOOL JUST A DATA SOURCE?

**Yes (source it):** Weather APIs, nutrition databases, food safety tables, unit conversion math, seasonal data, mileage calculators, timezone lookups.

**No (bridge it):** Social media posting, phone calls, physical vendor interactions, government portals, creative inspiration browsing.

If yes -> ChefFlow should DRINK from that source. The chef never visits it.

### 4. WHAT'S THE CLIENT-COLLABORATIVE ANGLE?

Ask: "Does the CLIENT know something here that the chef would otherwise have to hunt for?"

Examples that worked:

- Venue access: Client knows their own building (codes, parking, entrance)
- Dietary needs: Client knows their allergies better than anyone
- Guest count changes: Client knows before chef does
- Event timing: Client knows their schedule constraints

If the Dinner Circle can collect this info during setup, the chef's exit DISAPPEARS before it happens. The question is answered before it's asked.

### 5. WHAT'S THE PHYSICAL/ANALOG REALITY?

Chefs work with their hands. Not everything is a screen problem.

Ask:

- Would a printed PDF solve this better than any screen?
- Is voice (Remy reads aloud) the natural interface here?
- Is this a "messy hands" moment where the phone shouldn't be touched?
- Does the chef's muscle memory already have a physical workflow?

**Rules from stress-test #94:**

- Print is primary for mid-cook reference. Digital is backup.
- Voice (Remy) is the hands-free bridge.
- Large text + minimal UI for glance moments.
- Never fight the physical reality of kitchen work.

### 6. DOES IT COMPOUND OVER TIME?

**High compounding:** Venue profiles (visit once, know forever), client preferences (learn once, serve forever), seasonal patterns (build library over years).

**No compounding:** One-off calculations, weather checks, route planning.

High-compounding scenarios deserve richer data capture because the investment pays dividends across hundreds of future events.

### 7. WHAT'S THE RECLASSIFICATION?

Based on answers above, assign one:

| Classification                       | Meaning                                              | ChefFlow's job                                             |
| ------------------------------------ | ---------------------------------------------------- | ---------------------------------------------------------- |
| **Reducible**                        | ChefFlow can eliminate this exit entirely            | Build the feature. Chef never leaves.                      |
| **Reducible + Client-Collaborative** | Circle collects the info                             | Client provides. Chef never asks.                          |
| **Partially Reducible**              | ChefFlow handles 80%, one slice stays external       | Build what we can. Smooth the remaining exit.              |
| **Bridgeable**                       | Chef will always leave, but we smooth the round-trip | Pre-load context out, capture intel back.                  |
| **Permanent**                        | External tool IS the destination                     | Clean door out. Optional: store what they learn on return. |

---

## OUTPUT FORMAT

For each evaluated scenario, produce:

```markdown
## Scenario #[N]: [Title]

**Original classification:** [from master list]
**Reclassified to:** [new classification]

**Why chef leaves:** [operational reason, not surface reason]
**Context ChefFlow has:** [bullet list]
**Data source?** [yes/no + which API/database]
**Client-collaborative angle:** [what Circle can collect]
**Physical reality:** [print/voice/screen/hands-free needs]
**Compounding:** [high/medium/low + why]

**Solution design:**
[2-5 bullet description of what to build]

**Where it appears:**

- [surface 1]
- [surface 2]
- [Dinner Circle angle]

**What remains as permanent exit:**
[What the chef still leaves for, even after we build this]

**Priority:** [pain frequency] x [effort] = [rank signal]

**Spec needed?** [yes -> write to docs/specs/ | no -> add to reclassification sprint doc]
```

---

## PRINCIPLES (Discovered Through Stress-Testing)

1. **Source it, don't link it.** If the external tool is just a data source with a free API, ChefFlow should drink from it. The chef never visits.

2. **The Circle is an intelligence-collection surface.** Every Dinner Circle quietly gathers what the chef would otherwise hunt for. Weather, access notes, dietary updates, preferences, guest count, timing.

3. **Measure success by what DISAPPEARS.** Not "chef found weather faster." It's "that text message never happened." Quality = things that vanish from chef's inbox.

4. **Knowledge compounds.** Venue profiles, client preferences, seasonal patterns. Capture once, serve forever. The 50th event at a client's house should have zero friction.

5. **Respect the physical world.** Chefs have messy hands, loud kitchens, hot environments. Print > screen for mid-cook. Voice > typing for hands-full. Large text > detailed UI for glance moments.

6. **Progressive disclosure, always.** Tier 1: glance (one line on card). Tier 2: expand (operational details). Tier 3: deep (everything, tucked away). Never bombard. Tuck weird stuff one tap deeper.

7. **The exit isn't the failure.** The failure is: can't find way back, lost context, nowhere to store what they learned, had to manually assemble the exit.

8. **Client knows best about their own space.** Access codes, parking, building rules, kitchen setup, guest allergies. Ask them via Circle. Chef never calls to ask.

---

## BATCH MODE

When running `batch`, process 5 scenarios sequentially:

1. Read the evaluated registry (bottom of sprint doc) to find what's done
2. Pick next 5 unevaluated scenarios from master list
3. Run each through the rubric (solo mode, mark `NEEDS-DEVELOPER-REVIEW`)
4. Update sprint doc with results
5. Write individual specs for any scenario that warrants one (Reducible + complex enough)
6. Report: "Evaluated #X, #Y, #Z, #A, #B. [N] reclassified. [M] specs written. [K] need developer review."

---

## PROGRESS TRACKING

### Evaluated Scenarios Registry

Maintained at the BOTTOM of `exit-scenario-reclassification-sprint.md` under a `## Evaluated Registry` heading.

Format:

```markdown
## Evaluated Registry

| #   | Title                          | Date       | Mode        | Classification                   | Spec                          |
| --- | ------------------------------ | ---------- | ----------- | -------------------------------- | ----------------------------- |
| 58  | Weather for outdoor event      | 2026-05-25 | Interactive | Reducible                        | event-weather-intelligence.md |
| 90  | Parking/loading dock logistics | 2026-05-25 | Interactive | Reducible + Client-Collaborative | venue-access-intelligence.md  |
| 94  | Quick recipe glance mid-cook   | 2026-05-25 | Interactive | Reducible                        | mid-cook-reference-system.md  |
```

**Rules:**

- Add entry immediately after evaluation completes
- `Mode` = Interactive (developer participated) or Solo (batch, needs review)
- `Spec` = filename if written, or "sprint-doc-only" if just added to priority table
- Use this registry to determine "next unevaluated" for batch and random modes
- `/exit-eval status` reads this registry and reports counts

### Summary Stats (update on each run)

```
Total: 95 | Evaluated: [N] | Remaining: [95-N]
Reducible: [n] | Client-Collaborative: [n] | Partially Reducible: [n] | Bridgeable: [n] | Permanent: [n]
Specs written: [n] | Needs developer review: [n]
```

---

## MERGING RESULTS INTO SPRINT DOC

The sprint doc (`exit-scenario-reclassification-sprint.md`) has two sections:

1. **Priority table** (top): ranked by pain-frequency x effort. Add new evaluated scenarios here if they're actionable.
2. **Evaluated registry** (bottom): ALL evaluated scenarios go here regardless of classification.

When adding to the priority table:

- Insert at correct priority position (not just appended)
- Match the existing format: Priority | Scenario | Frequency | Effort | Impact
- Only Reducible and Partially Reducible scenarios get priority entries
- Permanent and Bridgeable exits go to registry only (they don't need builds)

---

## INTEGRATION WITH OTHER SKILLS

- After evaluation, if a spec is written -> add to `docs/UNIFIED-BUILD-QUEUE.md`
- If scenario touches a route -> `/page-xray` on that route
- If scenario touches Dinner Circles -> check `lib/circles/` wiring
- If scenario touches Remy -> check `docs/remy-complete-reference.md`
- Weather/location scenarios -> check event detail page architecture
