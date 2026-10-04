---
name: story-mapping-and-workshops
kind: skill
status: ready
provenance:
  principles:
  - P011
  - P028
  - P034
  - P050
  - P070
  - P071
  - P101
  - P023
  claims:
  - C00610
  - C00611
  - C00612
  - C00613
  - C01083
  - C01084
  - C01075
  - C01076
  - C01080
  - C01085
  - C01089
  - C01094
  - C01095
  - C01096
  - C01097
  - C01098
  evidence:
  - E00217
  - E00218
  - E00219
  - E00220
  - E00359
  - E00360
  - E00355
  - E00356
  - E00357
  - E00361
  - E00362
  - E00363
  - E00364
  - E00365
  - E00366
  - E00367
  source_anchors:
  - 95f398b45f1f-c0007
  - eaae3b395dea-c0000
  - eaae3b395dea-c0001
  authored_from_digest: 47fceccc4cc992c28700401772c9953a558b4959518bf19e35a47fd88d519209
---

# Map and slice user stories through collaborative workshops

## Purpose

Guide teams to build genuine shared understanding of what to build by mapping and slicing user
stories *together*, rather than by perfecting written specifications. This skill maps what
end-users do to get value along a left-to-right narrative backbone, uses the story template and
small opt-in workshops to start real conversations, and sizes each story to the conversation at
hand. It advises on, reviews, and compares story-mapping and workshop approaches; it does not own
the map, write the team's backlog, or make the scope decision.

## When to use

- The caller is planning a release or backlog and wants it structured as a story map organized
  around what users *do* to get value, not around implementation tasks.
- A story map, backlog, or set of user stories needs reviewing for implementation-first framing, a
  missing narrative backbone, or oversized / template-driven stories.
- The caller is preparing a story-writing or mapping workshop and wants help on who to invite, how
  many, and how to run it so real conversations happen.
- The caller is weighing how to size or slice stories for an upcoming conversation (users vs.
  developers vs. business), or wants to shift a team off big written specs toward collaborative
  storytelling.
- Do not invoke when the caller wants the backlog written for them, a single story exhaustively
  specified as a contract, or a tracking tool / vendor configured — hand those to the owning
  product team, which owns the map and the scope decision.

## Procedure

These steps roughly sequence a mapping workshop, but story mapping is iterative — revisit the map,
the sizing, and the stories as conversations reveal more. Each step names the principle(s) it rests
on and states the trade-off it carries, because every practice here buys one thing at the cost of
another.

1. **Reframe from perfecting documents to telling stories (P028).** Set the goal of the work as
   building shared understanding — understanding the problem and finding the best solution
   together — not writing and reading requirements "correctly." Stop polishing documents and get
   the group together to tell the story of the product. You are telling a story well when it
   generates energy, interest, and vision in the listeners; if the room is not having rich
   discussions, it is not really using stories. **Trade-off:** you trade the apparent completeness
   and sign-off comfort of a polished document for genuine shared understanding — a good trade, but
   only if the discussion is actually rich; a flat room that merely reviews a document gets neither
   (P028).

2. **Convene a small, opt-in workshop group (P101, P071).** Announce the stories ahead of time and
   let people opt in rather than conscripting a crowd — crowds do not collaborate, and the
   conversation gets harder with more people, especially uninterested ones. Keep the group to
   roughly three to five, including a user or UI person, one or two developers who know the
   codebase, and a tester. If everyone wants in, use a fishbowl: three to five at the board, the
   rest observing, an outsider stepping in only as an insider steps out. Invite the complainers to
   the *next* session rather than the current one. **Trade-off:** a small, opt-in group makes the
   conversation possible but risks leaving people out — mitigate with the fishbowl when demand is
   high and by rotating who is invited; and note that a regular planning meeting can host this only
   if the team already collaborates well (P071, P101).

3. **Make the work visible on a big, shared wall (P023).** Put the work on a big, transparent wall
   of sticky notes so everyone can see it and participate — for example, arranged left-to-right by
   time, top-to-bottom by priority, and color-coded by activity. A visible wall bridges developers
   and the stakeholders who will never open the tracking tool. **Trade-off:** a visible wall invites
   everyone in, but expect stakeholders to distrust incremental delivery until they watch the
   product improve week over week — so plan to show that steady progress (P023).

4. **Build the map by assuming the solution already exists (P011).** Map the idea as though the
   solution is already built, and describe what end-users *do* to get value — not what it takes to
   implement. Identify every actor who must interact with it (including the software or interface
   itself as an actor), and lay out their steps in sequence along the successful path. Map the best
   solution you can from what you know today, and refine it as you test. **Trade-off:** describing
   what users do rather than what to build keeps the map on value, but the map is only the best
   solution you can draw from today's knowledge — treat it as a hypothesis to refine as you test,
   not a finished plan (P011).

5. **Organize the map along a narrative backbone (P050).** Give the map a backbone: the row of big
   steps across the top, read left-to-right as the narrative flow of the user's journey. When the
   backbone gets long, summarize it at a second level so the story still reads as a flow. Place
   persona thumbnails above the backbone to track who you are discussing (a backend service can be a
   persona too). Keep the size vocabulary loose — talk in "big things and little things" rather than
   precise units. **Trade-off:** a loose, narrative backbone keeps the whole story graspable at a
   glance but deliberately avoids precise sizing, so use it to build shared understanding, not to
   produce an estimate (P050).

6. **Frame stories to start conversations, not to specify them (P070).** Write stories with the
   template "As a [type of user], I want to [do something], so that I can [get some benefit]"
   because it forces who / what / why into the open, and a feature name alone will not help you find
   the right people to talk to. But treat the template as a conversation starter and a learning-stage
   device only — never as a specification or contract. Beware "template zombies" who let the template
   drive the work or insist nothing counts as a story unless it is templated; the value is in telling
   the story, not in the written form. **Trade-off:** the template reliably surfaces who/what/why,
   but if you let the written card stand in for the conversation you recreate the very
   specification-worship you were trying to escape (P070).

7. **Size each story to the current conversation (P034).** There is no single right story size — the
   right size is the one that fits the conversation you are having now: need-sized for users, small
   enough to build-and-test in a few days for developers, and a business-outcome bundle for the
   business (which should aim to release smaller and more frequently). Big stories contain smaller
   ones, and conversation is the best tool for breaking them down, so keep the size language
   deliberately imprecise. **Trade-off:** sizing to the conversation keeps a story useful to whoever
   is discussing it, but it resists a single fixed estimate on purpose — accept that "what size is
   this story?" has no one right answer and keep the size words loose (P034).

## Inputs

- The artifact or situation under review: an existing story map, backlog, set of user stories, or a
  plan for a story-writing / mapping workshop.
- The outcome or release the mapping should serve, and who the end-users (personas) are.
- Constraints: who is available to participate, the appetite or timeline, whether the team already
  collaborates well, and what is known versus still assumed.

## Output

A story-mapping / workshop recommendation or critique that:

- names the outcome the map serves and centers the map on what users do to get value, not on
  implementation;
- structures or checks the narrative backbone, persona coverage, and second-level summary;
- checks that stories start conversations rather than acting as contracts, and are sized to the
  conversation at hand;
- recommends who should be in the workshop and how to run it so real discussion happens;
- makes each recommendation's trade-off explicit — what is gained and what is sacrificed; and
- ends with a concrete next step tied to the caller's outcome and appetite.

In **review** mode this is a findings list with remediations; in **compare** mode it is a
side-by-side of the options (for example, story slices or workshop formats) ending in an
outcome-weighted pick. The map, the backlog, and the scope decision stay with the owning product
team.

## References

- `references/product-principles-index.md` — index of the product-design principles cited here
  (P011, P023, P028, P034, P050, P070, P071, P101) and the sources they trace to.

## Provenance

Distilled and paraphrased from the product-design principles cited in the frontmatter (P011, P023,
P028, P034, P050, P070, P071, P101), which draw chiefly on Jeff Patton, *User Story Mapping* (2014),
and Teresa Torres, *Continuous Discovery Habits* (2021). Both are distillation-only sources:
paraphrased here with no verbatim text.
