---
name: start-1-1
description: "Lesson 1.1: Entities, Properties & Relations - the mental model behind Geo's knowledge graph"
---

# Lesson 1.1: Entities, Properties & Relations

You are now teaching **Lesson 1.1** — the heart of the conceptual part. By the end, the learner should *get* how knowledge is built up as a graph.

Background for you: `reference/grc20-cheatsheet.md`. Teach the intuition, not the spec. The learner never needs the term "GRC-20."

## Learning objectives
- Understand the three building blocks: **entities**, **properties**, **relations**
- See how they combine into a connected graph
- Build the instinct for "is this a thing, or a fact about a thing?"

## Teaching script

### Step 0: What this lesson is about (1 min)

Say:
"Before you can build anything in Geo, it helps to know how knowledge is actually *shaped* here. So this lesson is the mental model — the small set of building blocks that everything in Geo is made of.

We'll keep it concrete: I'll walk you through the pieces using a running example, and by the end you'll be able to look at almost anything and see how it would fit into the graph. Quick and no app yet — just the idea. Let's go."

### Step 1: The whole model in one breath (2 min)

Say:
"Everything in Geo is built from just **three** ideas. That's it. Once you have these, you understand the whole model:

1. **Entities** — the *things*
2. **Properties** — the *facts about a thing*
3. **Relations** — the *connections between things*

Let's take them one at a time, with a running example. Pick something you'd enjoy: a band, a football club, a city, a favorite book. I'll use a band — **Radiohead** — but tell me yours and I'll switch to it."

[Soft prompt — if they offer a topic, use it throughout. If not, use Radiohead.]

### Step 2: Entities — the things (2 min)

Say:
"An **entity** is anything you can name: a person, a place, an idea, a project, a song. Each one is a single 'thing' in the graph with its own identity.

In our example, **Radiohead** is an entity. So is the band member **Thom Yorke**. So is the album **OK Computer**. Three separate things.

Picture three dots on a page. Each dot is an entity. We haven't said anything *about* them yet — that's next."

### Step 3: Properties — facts about a thing (3 min)

Say:
"A **property** is a fact attached to an entity — a value that belongs to it.

Radiohead the entity might have:
- **Name** = 'Radiohead'
- **Formed** = 1985
- **Description** = 'English rock band from Abingdon'

Notice the facts have different *kinds*: 'Radiohead' is **text**, 1985 is a **number** (a year). Geo keeps track of what kind each value is — text, number, date, yes/no, a link, an image — so it can be smart about them. When you add a property in the app, you just pick the kind from a menu.

So now our dots have details written next to them. Still just three separate dots, though. The magic is the next part."

Pause here:
"Make sense so far? Entities are the things, properties are the facts on them. Type `ok` or `.` and we'll connect them up."

[STOP — wait for the learner]

### Step 4: Relations — the connections (3 min)

Say:
"A **relation** is a link from one entity to another — and it has a direction, so it reads like a little sentence:

- **Thom Yorke → member of → Radiohead**
- **OK Computer → by artist → Radiohead**

Now draw lines between your dots. *That's the graph.* Three things, wired together by relations. From Radiohead you can hop to its members, and to its albums. From an album you can hop back to the band, then out to another member. Knowledge becomes a web you can travel.

This is the whole point of Geo: not isolated facts, but **connected** ones. A relation always points to *another real entity* — which means everything links into one big shared graph."

### Step 5: The instinct — thing vs. fact (3 min)

Say:
"Here's the one judgment call you'll make over and over: **is this a *thing*, or a *fact about a thing*?**

- If it has its own details and connects to other stuff → it's an **entity**, and you link to it with a **relation**.
- If it's just a simple value → it's a **property**.

Example: a band's *genre*. 'Rock' could be a text property... but 'Rock' is really its own thing — other bands are rock too, and you might want to describe the genre itself. So 'Rock' is better as an **entity**, with a relation **genre → Rock**. Now every rock band links to the same Rock entity, and you can ask 'show me all rock bands.'

Rule of thumb: **if it's another nameable thing, prefer a relation to it over burying it in text.** That keeps the graph connected instead of full of dead-end words."

### Step 6: The delightful twist (2 min)

Say:
"One mind-bender to leave you with — and it's optional, so don't worry if it's slippery:

In Geo, **the categories themselves are also entities.** The *type* 'Band' is an entity. The *property* 'Formed' is an entity. Even the *relation* 'member of' is an entity.

Why that's cool: the structure of the knowledge lives *inside* the graph, right alongside the knowledge. There's no separate hidden rulebook — it's all part of the same web. It means Geo can describe literally anything, including how it describes things.

You don't need to do anything with that today. Just know: when something feels like 'everything is an entity here' — yep, that's by design."

### Step 7: Recap (1 min)

Say:
"You've got the whole model now:
- ✅ **Entities** — the things
- ✅ **Properties** — typed facts on them
- ✅ **Relations** — directed links that connect them into a graph
- ✅ The instinct: another nameable thing → relation; a simple value → property

Next, the fun part: you'll sketch a tiny graph for a topic *you* care about — a design exercise to make this click. Later it'll be the inspiration for your first real contribution to a shared space.

When you're ready, run `/start-1-2`."

## Pacing instructions

Deliver Steps 1–3, then [STOP] (built into Step 3).
After the learner responds, deliver Steps 4–5, then pause:
"Still with me? Want the fun mind-bender before we wrap? Type `ok` or `.`"
[STOP — wait before Steps 6–7]

## Important notes
- Anchor every example in the learner's chosen topic if they give one.
- Use the dots-and-lines mental image consistently — it's the most effective frame.
- Don't introduce data-type names exhaustively; "text, number, date, yes/no, link, image" is plenty.
- The "everything is an entity" twist is a bonus, not a requirement. If they look lost, skip it.
