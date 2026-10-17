---
name: icp-research
description: Build or refine the Ideal Customer Profile (ICP) and personas using the Jobs-to-be-Done framework (Clayton Christensen / Bob Moesta). Use when the user asks for ICP research, persona development, "who are our customers", buyer personas, audience research, "build our ICP", target customer definition, or wants to update persona docs. JTBD interview questions, three job dimensions (functional/emotional/social), and the Four Forces of Progress are wired into every persona. Writes to knowledge/icp/personas.md so all other skills get smarter. For the individual buyer persona rather than the segment, see customer-persona. For sourcing real customer language, see customer-research.
metadata:
  grounded_in:
    - "Jobs-to-be-Done - Christensen & Moesta"
  reads:
    - knowledge/icp/personas.md
    - knowledge/services/
    - knowledge/markets/positioning.md
    - knowledge/content-library/case-studies/
    - knowledge/learnings.md
  writes:
    - knowledge/icp/personas.md
    - output/icp-research/
---

# icp-research

Builds rigorous, evidence-based personas using Jobs-to-be-Done. Writes to `knowledge/icp/personas.md` directly so the rest of the OS uses the updated context.

## Where this method comes from

The struggling moment, the hiring and firing triggers, and the Four Forces are **Clayton
Christensen and Bob Moesta's Jobs to be Done**, developed in *Competing Against Luck* (2016) and
Moesta's switch-interview work. The unit of analysis is the moment of change, not the demographic:
people do not buy because of who they are, they buy because something happened.

The Four Forces are push of the situation, pull of the new solution, anxiety about the new, and
habit of the present. A segment where push and pull are strong but anxiety and habit are stronger
is a segment that will not switch, however well it matches on firmographics.

Demographics and firmographics are context. The job the customer is hiring you for is the insight.

Christensen's milkshake study is the shape of the whole method: the buyers had nothing in common
demographically, and everything in common situationally. That is why this skill treats a segment
that shares firmographics but not a struggling moment as a failed segment, and says so.

## Before you build: is the evidence strong enough?

Persona work lands in a file six other skills read as truth, so the first decision is whether to
build at all.

| Evidence available | Confidence | What to do |
|---|---|---|
| 10 or more distinct sources: interviews, win/loss records, sales calls | high | Build. Offer the write to `knowledge/icp/personas.md` behind the diff gate |
| 5 to 9 distinct sources | medium | Build, label `confidence: medium`, offer the write behind the diff gate, and list which sections are thin |
| Fewer than 5 distinct sources | low | Build to `output/` only. Do not offer the shared-file write. Say plainly that this is a hypothesis to test, not canon |
| No customer contact at all, only internal opinion | none | Do not build a persona. Run the JTBD interview questions below with the user, or route to `/customer-research`. A persona invented from internal opinion is worse than no persona, because it cannot be argued with |

How many personas to build, in priority order: 1 primary always, then a secondary only if its
struggling moment is genuinely different from the primary's. Two personas with the same struggling
moment and different job titles are one persona. Maximum 4 in total, because past that no downstream
skill can hold them in context.

Hard rules on the numbers, so the judgement is not re-litigated every session:

| Item | Minimum | Maximum |
|---|---|---|
| JTBD statements per persona | 1 | 3 |
| Specific pains per persona | 3 | 6 |
| Four Forces cells filled | 4 of 4, or `[NEEDS INPUT]` | |
| Personas in the file | 1 | 4 |
| Distinct sources for `confidence: high` | 10 | |

**Stop conditions.** Do not proceed to writing personas at all if there has been no customer contact
and no win/loss data. If the struggling moment for the primary persona cannot be written as a scene,
stop and say so: that single gap invalidates every section below it.

Warning signs, in priority order:

1. Two personas share a struggling moment. Merge them, and say why.
2. The anxiety and habit forces are blank while push and pull are full. That means only won deals were studied. Lost deals and no-decision deals are where anxiety and habit live, and they are what explains the losses.
3. The "words they use" section reads like marketing copy. Real customer vocabulary is blunter and more specific than any brand's own language.
4. Firmographics are tight and the struggling moment is vague. That is an account list, not an ICP, and targeting on it will produce well-qualified prospects who do not move.

## When to use

- "Build our ICP from scratch"
- "Refine our buyer personas"
- "Who are we actually selling to?"
- "Update the persona doc based on these customer interviews"
- "I uploaded customer research, build personas from it"

## Inputs needed

- **Source material** (any combination):
  - Existing customer list (CSV in `uploads/`)
  - Customer interview notes
  - Win/loss data
  - Sales team input (paste in chat)
  - Existing case studies in `knowledge/content-library/case-studies/`
  - Pasted survey results
- **Number of personas** to build (default: 1 primary, 1-2 secondary; max 4)
- **Use case**: positioning, ABM targeting, content strategy, paid ads, sales enablement

## Framework: Jobs-to-be-Done (JTBD)

People don't buy products. They hire them to do a job in their life. The job - not the demographic - is what drives the purchase.

### Three job dimensions (all three required in every persona)

| Dimension | What it is | Example |
|---|---|---|
| **Functional job** | The practical task they need done | "Get pipeline without relying on the founder for every deal" |
| **Emotional job** | How they want to feel when it's done | "Feel confident when the CEO asks about marketing ROI" |
| **Social job** | How they want to be perceived | "Be seen as the person who finally fixed marketing" |

### The struggling moment

The moment when the customer's current solution broke and they started looking. More predictive of buying behavior than any demographic. Every persona must have one.

Format: "What was happening in their life/job when they started looking? What was the specific situation?"

### Hiring and firing triggers

- **Hiring trigger**: what made them actively seek a solution? (the push)
- **Firing trigger**: what were they using before, and why did it stop being enough? (the pull away)

### Four Forces of Progress

| Force | Direction | Question |
|---|---|---|
| **Push of the situation** | Moves them away from status quo | What's so broken they can't stay put? |
| **Pull of the new solution** | Attracts them to the new option | What's the specific promise that drew them? |
| **Anxiety of the new** | Holds them back | What are they afraid might go wrong? |
| **Habit of the present** | Inertia | What makes it easier to do nothing? |

Understanding all four forces explains why good products still lose deals - anxiety and habit beat push and pull.

### JTBD statement format

"When [struggling situation], I want to [motivation], so I can [expected outcome]."

Example: "When the board asks for pipeline attribution and I can't answer, I want a marketing analytics tool I can trust, so I can show that marketing is driving revenue and keep my budget."

## Process

1. **Load existing knowledge.** Read `knowledge/icp/personas.md` (if any), `knowledge/markets/positioning.md`, and case studies. If personas already exist, ask: "Replace or refine?"

2. **Gather evidence.** If `uploads/` has customer data, run analysis:
   - Common industries
   - Common company sizes (employees, revenue)
   - Common roles (the buyer, the user, the influencer)
   - Common geographies
   - Common acquisition channels
   - Win-rate by segment if available

   If no data, interview the user with these questions (not generic persona questions - JTBD-specific):

   **JTBD Interview Questions**

   *The struggling moment:*
   - "Walk me through the specific day or week when you decided to start looking for a solution."
   - "What was happening that made the status quo no longer acceptable?"
   - "How long had that situation been going on before you started looking?"

   *The firing trigger:*
   - "What were you doing before? A spreadsheet, a different tool, a consultant, nothing?"
   - "What happened that made that stop being enough?"

   *The hiring trigger:*
   - "What made you choose this solution over doing nothing, or staying with the old approach?"
   - "What was the specific promise that made you move?"

   *The four forces:*
   - "What were you most anxious about when you decided to switch?" (anxiety)
   - "What almost made you not do it?" (habit + anxiety)
   - "Who else had to sign off? What were their concerns?" (committee anxiety)

   *The three job dimensions:*
   - "When you imagined this working perfectly, what did that feel like?" (emotional job)
   - "How did you explain this decision to your CEO or team?" (social job)
   - "What specific outcome were you hired to produce?" (functional job)

   Standard questions for firmographic baseline:
   - "Who are your top 5 customers by revenue or fit?"
   - "What pattern do you see across them?"
   - "Who do you NOT want as a customer?"
   - "Which deals close fastest?"

3. **Write the persona doc.** Use this structure (one block per persona):

   ```
   # ICP and Personas (DD-MM-YYYY)

   ## Primary persona: <Name + role>
   Example: "Maya, Head of Demand Gen at Series B SaaS"

   ### Demographics
   - Role: <title>
   - Seniority: <IC | Manager | Director | VP | C-level>
   - Team size: <range>
   - Reports to: <role>

   ### Firmographics
   - Company stage: <seed | A | B | C | growth | enterprise>
   - Employees: <range>
   - Revenue: <range>
   - Industries: <list>
   - Geographies: <list>

   ### The struggling moment
   <Specific narrative of the situation that triggered them to look for a solution.
   Must be a concrete scenario, not a general pain point.>
   Example: "It's the Thursday before the board meeting. Pipeline is flat.
   The CEO just asked 'what is marketing doing?' and Maya doesn't have an answer
   that will hold up to scrutiny."

   ### Jobs-to-be-Done

   **Functional job** (the practical task):
   <What they need done, specifically.>

   **Emotional job** (how they want to feel):
   <How they want to feel when the job is done.>

   **Social job** (how they want to be perceived):
   <How they want others to see them as a result.>

   **JTBD statement**:
   "When [struggling situation], I want to [motivation], so I can [expected outcome]."

   List 2-3 JTBD statements if the persona has multiple jobs.

   ### Four Forces of Progress

   | Force | What it is for this persona |
   |---|---|
   | Push (away from status quo) | <specific situation that's making them move> |
   | Pull (toward new solution) | <specific promise that attracted them> |
   | Anxiety (about the new) | <what they're afraid might go wrong> |
   | Habit (inertia) | <what makes doing nothing easier> |

   ### Goals (what they're measured on)
   1. ...
   2. ...
   3. ...

   ### Pains (what's broken today)
   1. ... (specific, not generic)
   2. ...
   3. ...

   ### Hiring / Firing triggers
   - **Hiring trigger**: <what caused them to actively seek a solution>
   - **Firing trigger**: <what they were using before and why it stopped working>

   ### How they buy
   - Discovery channels: <where they find tools>
   - Influencers: <who they trust>
   - Decision criteria: <ranked: outcomes, price, fit, brand, integrations>
   - Buying committee: <other roles involved>
   - Typical sales cycle: <weeks/months>
   - Common objections: <list - mapped to the four forces where possible>

   ### Where they hang out
   - Communities (Slack, Discord, Reddit subs)
   - Newsletters and podcasts
   - Conferences
   - LinkedIn groups, hashtags

   ### Voice (how to write to them)
   - Words they use: ...
   - Words they avoid: ...
   - Tone: <formal | conversational | technical>
   - Length tolerance: <skim | medium | deep dives>

   ### Anti-persona (NOT this person)
   Who looks similar but isn't a fit. Example: "Solopreneurs and pre-seed founders.
   They don't have budget or scale."

   ### Evidence
   - Source 1: <interview, survey, win-rate analysis>
   - Source 2: ...
   - Confidence level: high / medium / low (based on N data points)

   ---

   ## Secondary persona: <Name + role>
   Same structure, shorter
   ```

4. **Cross-check against case studies.** Open `knowledge/content-library/case-studies/`. Do the existing customers fit the personas? Specifically: do their struggling moments match? If not, flag the mismatch. Demographic fit without JTBD fit is a weak persona.

5. **Check against `knowledge/learnings.md`**. Past campaigns may have revealed which struggling moment converts fastest. Update the four forces accordingly.

6. **Self-check.** Each item is checkable by reading the persona document. Where an item says count,
   count it in the artifact rather than asserting the item passed.

   - [ ] Every persona's struggling moment describes a scene with a time, a person and an event in it. If it can be read as a job description, it fails
   - [ ] Every persona has all three job dimensions filled, and the emotional and social entries use different words from the functional one rather than restating it
   - [ ] Every JTBD statement matches the template exactly: "When ..., I want ..., so I can ...". Count the statements per persona and confirm 1 to 3
   - [ ] All four force cells are filled for every persona. A blank anxiety or habit cell is a research gap, so mark it `[NEEDS INPUT]` rather than leaving it empty
   - [ ] Hiring and firing triggers are both named, and the firing trigger names an actual prior solution
   - [ ] At least 3 pains, each containing a number, a frequency, or a named artifact. "Wants to grow" fails, "spends 30% of the week pulling reports" passes
   - [ ] Anti-persona names a specific group that looks like a fit and is not, with the reason
   - [ ] The evidence section lists the sources by name and the `Confidence level` matches the count of them against the table above. Compare the two, do not assert
   - [ ] Every "words they use" entry is traceable to a named source, or is written `[NEEDS INPUT: real customer language]`. Count the sourced entries
   - [ ] Each persona block has exactly one struggling moment, and no two blocks share it

7. **Write to `knowledge/icp/personas.md`**, only through the ownership rules below.

8. **Save a version snapshot** to `output/icp-research/<DD-MM-YYYY>-personas.md` so prior versions are preserved.

9. **Offer follow-ups**:
   - Update positioning to match (`/brand-context` or manual edit)
   - Build content briefs targeted at the struggling moment (not generic persona)
   - Run `/competitor-analyst` to map competitors against the same JTBD

## Rules

- Never invent firmographics. If you have 3 customers, say "based on 3 interviews, low confidence" rather than overstating.
- The struggling moment is mandatory. A persona without one is just a demographic profile.
- The anti-persona is mandatory. If you don't know who is NOT your customer, you don't know who is.
- Pains must be specific. "Wants to grow revenue" is not a pain. "Spending 30% of week manually pulling reports that still don't answer the CEO's questions" is.
- All three job dimensions (functional, emotional, social) are required. Most personas have functional jobs only. Emotional and social jobs are where messaging differentiation lives.
- Voice notes must be concrete enough to use. "Professional" is useless. "Uses 'GTM' not 'go-to-market', avoids exclamation points, prefers numbered lists" is useful.
- **Never invent the "words they use" vocabulary.** Invented customer language is the worst thing
  this skill can emit, because `/content-writer` and `/copy-review` then treat it as observed speech
  and put it into public copy. Unsourced vocabulary is `[NEEDS INPUT: real customer language]`.

## Shared file ownership: knowledge/icp/personas.md

**This skill owns `knowledge/icp/personas.md`.** It owns the file's structure, the section order,
the primary and secondary persona slots, the ICP firmographic summary, and the anti-persona.
`/customer-persona` also writes to this file, as a contributor of single persona blocks into the
structure this skill defines.

| Part of the file | This skill may | `/customer-persona` may |
|---|---|---|
| File structure, headings, section order, persona slot ordering | Create and replace | Read only |
| ICP firmographic summary and anti-persona | Create and replace | Read only |
| An individual persona block | Create, replace, or merge | Add one block, or replace that one block in full |

When a persona block already exists and carries a `confidence` value higher than the one you are
about to write, do not silently replace it. Show both, name the difference in evidence, and let the
user choose.

The write gate, which is not optional and is identical in both skills. Neither may relax it:

1. Write to this file **only after showing the user the diff and getting an explicit yes.** Six other skills read it as truth, so an ungated write turns one thin session into permanent canon nobody can trace back.
2. If confidence is low, meaning fewer than 5 distinct data points, write to `output/` only and say plainly that the persona is not yet canon. Do not offer the shared-file write at all.
3. Carry the `confidence: high | medium | low` field into every block written, so a reader can tell canon from draft without opening the sources.
4. Never invent a firmographic, a struggling moment, a quote, an objection, or a piece of customer vocabulary to complete a block. `[NEEDS INPUT: <what would fill it>]` is the correct output.

## What this skill cannot know

These are the limitations that bite in practice. Where one applies to the artifact, write it into the document as an open question rather than leaving the reader to assume it was verified.

1. **Whether the struggling moment generalises.** Interviews capture the people who bought and agreed to talk. The buyers who never reached you, and the ones who churned quietly, have struggling moments this method never sees.
2. **Whether the segment is commercially worth serving.** Nothing here sizes the segment, prices it, or estimates acquisition cost. A perfectly evidenced persona can still describe a segment too small or too cheap to build a business on.
3. **What people will actually do, as opposed to what they said.** Switch interviews are reconstructions, and reconstructions rationalise. Anxiety in particular is under-reported, because nobody enjoys describing what scared them.
4. **Whether the four forces have shifted since the interviews.** A competitor's launch, a price change, or a regulation can flip habit and anxiety within a quarter. Every persona block should carry the date its evidence was gathered so a reader can judge staleness.

## Related skills

- `/customer-research` for running the interviews and surfacing the verbatim language, and it must run first when there are fewer than 5 distinct data points
- `/customer-persona` for a single deep buyer profile inside a segment this skill has already defined, and it contributes blocks into the file this skill owns
- `/positioning-doc` for turning the struggling moment and the pull force into a positioning statement
- `/competitor-analyst` for mapping who else is being hired for the same job, which is where the anxiety and habit forces usually come from
- `/brand-context` for creating the knowledge base when `knowledge/icp/personas.md` does not exist yet
- `/content-writer` for consuming the voice notes, which is why unsourced vocabulary is forbidden above
- `/campaign-brief` for targeting a campaign at the struggling moment rather than at the job title

## Quick Reference: JTBD Framework

| Concept | What to capture | Why it matters |
|---|---|---|
| Struggling moment | The specific situation that triggered the search | More predictive than demographics |
| Functional job | The practical task needing done | The baseline - everyone captures this |
| Emotional job | How they want to feel | Where messaging resonates |
| Social job | How they want to be perceived | Where brand and positioning live |
| Push force | What's making them leave status quo | Drives urgency |
| Pull force | What attracted them to the new option | Drives conversion |
| Anxiety force | What might make them not switch | Drives objections |
| Habit force | Inertia keeping them in status quo | Drives loss to "do nothing" |
| Hiring trigger | What started active search | Defines the entry point |
| Firing trigger | What they used before and why it failed | Defines the competitive switch |
