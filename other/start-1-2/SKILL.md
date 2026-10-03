---
name: start-1-2
description: "Lesson 1.2: Model Your Own Topic - a design exercise: sketch a tiny knowledge graph to make the model concrete"
---

# Lesson 1.2: Model Your Own Topic

You are now teaching **Lesson 1.2**. This is a **design exercise** — the learner sketches a tiny graph for a topic they care about, to make the GRC-20 model (entities/properties/relations) concrete. You capture it as a sketch in `outputs/`. It is **not a build spec**: in Module 3 the learner publishes just **one simple entity** (optionally the main thing from this sketch), not the whole graph. The sketch is theirs to understand the model now and grow from later.

This is the one place you write a file. Everything later happens in the browser.

## Learning objectives
- Turn a real interest into a small graph (2–4 entities, a few properties, 1–2 relations)
- Practice the "thing vs. fact" instinct from Lesson 1.1
- Produce a design sketch saved to `outputs/` — a reference for how they'd model the topic (not a build list)

## Teaching script

### Step 0: What this lesson is about (1 min)

Say:
"In the last lesson you learned the *pieces* of Geo — entities, properties, and relations. Now let's put them to work: **this lesson is where you learn to *design* knowledge in Geo.**

Here's the plan. We'll take a topic you actually care about and sketch a tiny knowledge graph for it — a couple of things, a few facts, and the connections between them. It stays on paper (well, on screen); no app yet. This is a **design exercise** — the goal is to *get* how knowledge connects. It's not a to-do list: later, in Module 3, you'll publish just one simple entity to get the hands-on feel. Think of this as learning to *see* the graph — and you can always grow your sketch into the real thing on your own afterward.

Ready? Let's pick something to model."

### Step 1: Pick a topic (2 min)

Say:
"Time to make this yours. Pick a topic you know and enjoy — small and concrete is best. Good first topics:
- A band, artist, or album you love
- A book or author
- A favorite place (a city, a café, a park)
- A project, team, or community you're part of
- A hobby (a recipe, a plant, a game)

What would you like to model? Don't overthink it — we only need a handful of facts."

[STOP — wait for the learner to choose a topic. Do not proceed without one.]

### Step 2: Find the entities (3 min)

Once they pick a topic, say:
"Great choice. First, let's find the **things** — the entities. Usually there's one *main* thing and one or two *related* things.

If your topic were the band Radiohead, the entities might be: **Radiohead** (the band), **Thom Yorke** (a member), **OK Computer** (an album). Three things.

For *your* topic — what's the main thing, and what are one or two other things connected to it?"

[Help them land on 2–4 entities. Gently steer: if they list 10, suggest starting with 2–3. If they only have 1, ask "what's one thing connected to it — a person, a place, a part of it?"]

### Step 3: Add a few facts (properties) (3 min)

Say:
"Now let's put a couple of **facts** on each thing. For the main entity especially:
- It should have a **Name** (always).
- Maybe a **Description** (a sentence).
- One or two more: a date, a number, a place — whatever's natural.

What facts do you know about your main thing? I'll help sort which are text, which are numbers or dates."

[For each fact, lightly note the kind: text / number / date / yes-no / link / image. Keep it 2–4 properties per entity max for a first sketch.]

### Step 4: Wire the relations (3 min)

Say:
"Now the best part — **connect** them. Remember relations read like a sentence: *[this] [relation] [that]*.

For Radiohead: 'Thom Yorke → member of → Radiohead' and 'OK Computer → by artist → Radiohead.'

For yours — how do your things connect? Give me one or two links in that sentence form."

[Help phrase 1–2 directed relations. Watch for the "thing vs fact" instinct: if they describe something as a property that's really another entity, point it out gently and offer to make it a relation.]

### Step 5: Write the sketch to outputs/ (2 min)

Say:
"Let me capture your graph so you've got it as a reference — something you can bring to life in the real graph later. I'll save it as a little map."

Then create `outputs/my-graph-sketch.md` using the template below, filled in with *their* topic. Confirm the topic/details with them as you write.

Template to write:
```markdown
# My Geo graph sketch — <TOPIC>

_Created in Lesson 1.2 — a design sketch to understand the model. In Module 3 I'll publish one simple entity (maybe the main thing here) to the Geo Onboarding Space; I can grow the rest later._

## Entities (the things)

### <Main entity name>  — type: <e.g. Band / Person / Place / Project>
- Name: <value>            (text)
- Description: <value>     (text)
- <Other property>: <value> (<kind>)

### <Second entity name> — type: <…>
- Name: <value>
- <property>: <value> (<kind>)

### <Third entity (optional)> — type: <…>
- Name: <value>

## Relations (the connections)
- <Entity A>  → <relation, e.g. "member of">  → <Entity B>
- <Entity C>  → <relation, e.g. "by artist">  → <Entity A>

## Notes
- <anything to remember about this design>
```

After writing it, show them the result and say:
"Here's your graph on paper. Read it back — does it capture what you meant? We can tweak anything now."

[STOP — let them review and adjust. Update the file if they want changes.]

### Step 6: Recap (1 min)

Say:
"Look at that — you just designed a piece of a knowledge graph. ✅
- A few **entities** (your things)
- Some **properties** (facts on them)
- One or two **relations** (the connections)

It's saved in `outputs/my-graph-sketch.md` — a little design you can grow from anytime. Next, in Module 2 you'll set up your identity in Geo; then in Modules 3–4 you'll make your first real contribution to a shared space — starting simple, with a single entity.

Ready to create your space? Run `/start-2-1`."

## Pacing instructions
- This lesson is a back-and-forth, not a monologue. Ask, listen, refine.
- One [STOP] at Step 1 (must have a topic) and one at Step 5 (review the sketch). Don't rush past either.

## Important notes
- Keep the sketch **small** — 2–4 entities. A tiny complete graph beats a sprawling unfinished one, and it keeps the focus on *learning the model* rather than completeness.
- Steer toward reuse-friendly choices (common types like Person, Place, Band) — the app will have existing types/properties for these, which makes Module 3 smoother.
- If they pick something with no obvious second entity, suggest splitting out a part, a person, a place, or a category as the second entity so there's a relation to draw.
- Only write inside `outputs/`.
