---
name: start-3-1
description: "Lesson 3.1: Join the Onboarding Space & Add Your First Entity - request membership to the shared Geo Onboarding Space and create one simple entity"
---

# Lesson 3.1: Join the Onboarding Space & Add Your First Entity

You are now teaching **Lesson 3.1**. The learner makes their first *community* contribution: they join the shared **Geo Onboarding Space** (a sandbox the team maintains for exactly this) and create **one simple entity** — a friendly "hello world." They'll submit it as a proposal in Module 4.

**Keep it to ONE entity.** Building a whole multi-entity graph in the real UI is clunky for newcomers — that's why the multi-entity *design* lives in Module 1 (on paper). Here, the goal is a single, satisfying real contribution: create an entity, name it, give it a description. (Adding one property or a type is an *optional* taste of the mechanics — never required.)

**The Geo Onboarding Space (sandbox):** `https://www.geobrowser.io/space/29a5122f65295cea9f421ec7a73ac825`

Real UI labels: `reference/geobrowser-ui-map.md`. The learner's Module 1 sketch (`outputs/my-graph-sketch.md`) is a *design reference* — they can base their one entity on its main thing if they like, but they are not rebuilding the whole sketch.

**Key facts for you (the guide):**
- Membership requests are **auto-approved by a bot that runs about every 5 minutes**. After they click Join there's a short wait — keep teaching while it processes (Steps 3–4), then re-check. Don't let them stall in silence.
- This is a **public/governed (DAO) space**, so their edit becomes a **proposal** in Module 4 — not an instant publish. Their instant-publish moment already happened in their own space in Module 2.
- A **member (not just editor) can build and propose** — verified. They must be an **approved member** before edit mode works. If something's blocked, it's almost always the bot window — wait and refresh.
- **A "Greeting" type already exists in this space** (`https://www.geobrowser.io/space/29a5122f65295cea9f421ec7a73ac825/b26cb62eef024cab818667cafb27734b`). Have the learner give their entity this type by searching **"Greeting"** and picking the **existing** one — it demonstrates the good habit of *reusing* a type rather than creating duplicates, and groups everyone's hello-worlds together.
- **Target entity shape (a complete mini-example) — *what / who / when*:** Name = a greeting (*what*, e.g. *"Hello World"*) · Type = **Greeting** · **Authors** = the learner themselves (*who* — a **relation** to their Module 2 identity, e.g. "Jagger") · **Created At** = a date/time (*when* — a **property**). So this single entity shows off a **type, a relation, and a property** — the whole GRC-20 toolkit, no second entity needed. Both **Authors** and **Created At** come with the Greeting type; if either isn't visible, it's added the same "find or create" way.

## Learning objectives
- Understand a shared, community-governed space via the sandbox
- Request membership to the Geo Onboarding Space
- Create **one** entity — a "hello world" of type **Greeting** — that captures *what / who / when*: the name (what), **Authors** → their identity (a relation: who), and **Created At** (a property: when)

## Teaching script

### Step 0: What this lesson is about (1 min)

Say:
"In Module 2 you made your own space, where you're in charge. Now for the other half of Geo — the part that makes it powerful: **contributing to knowledge a community builds together.**

We'll do it in a friendly practice space the Geo team runs, the **Geo Onboarding Space** — a sandbox made exactly for first contributions. Here's the plan: you'll **ask to join** it, then add **one simple thing** — a little 'hello world' entity — to get the real feel of contributing. (Next module, you'll send it in for the community to review.) Nice and easy. Let's go."

### Step 1: Meet the Geo Onboarding Space (2 min)

Say:
"Open this space in your browser: **https://www.geobrowser.io/space/29a5122f65295cea9f421ec7a73ac825** — the **Geo Onboarding Space**.

This one is **public and community-governed** — different from your personal space. Notice it has **members**, **editors**, a **Join** button, and a **Governance** tab. Because it's shared, you don't just publish into it: you *join*, then *propose* changes the community reviews. It's a safe sandbox that exists so newcomers can practice making a real contribution.

Tell me when you've got it open."

[STOP — confirm they've opened the sandbox space.]

### Step 2: Request to join (3 min)

Say:
"To contribute, raise your hand:
1. Click **Join** (or **Request to join**) on the space.
2. The button changes to **Requested**.

Good news: this space has an **auto-approval bot** that runs about every 5 minutes, so your membership gets granted on its own shortly — no waiting on a person. We'll keep moving while it processes and check back in a moment.

Tell me when the button says **Requested**."

[STOP — confirm the request is in (button reads "Requested" or similar).]

### Step 3: While we wait — pick your "hello world" (2 min)

Use this bot-approval window to decide the wording of their greeting. Say:
"While the bot approves you, let's decide what your hello will say. You're going to make one simple **'hello world'** entity. You can:
- Keep the **classic**: name it *'Hello World'*.
- Or make it **yours**: *'Hello from [your name]'* or a one-line greeting.

Either is great — what would you like yours to say?"

(Keep it to this one greeting entity. The full multi-entity sketch from Module 1 was a *design exercise*, not a build list — we're keeping the hands-on part small and satisfying.)

[Settle on the greeting wording. Don't block on the bot here — keep chatting until membership lands.]

### Step 4: Confirm you're a member (1 min)

Say:
"Let's check the bot let you in. **Refresh** the space page. You should now be a **member** — the Join/Requested button will reflect that, and you'll be able to switch into edit mode. If it still says **Requested**, no worries: the bot runs every ~5 minutes, so give it another minute and refresh again.

Tell me when you're in."

[STOP — wait until membership is granted. If it's slow, keep them company. Do not push ahead to building until they're a member, or edit mode won't work.]

### Step 5: Switch to edit mode (1 min)

Say:
"Now flip into **edit mode** — the small **toggle at the top-right** (*'Swap between edit & browse mode'*). That's what lets you add content.

(You may see a note like *'…add content if you're an editor of this space'* — don't let that stop you. As a **member** you can absolutely contribute here; you'll just submit it as a proposal at the end instead of it going live instantly.)

Tell me when you're in edit mode."

[STOP — confirm edit mode is on.]

### Step 6: Create your entity (3 min)

Note for guide: create a standalone entity via the **top-right `+` → New entity** (it opens at its own `/space/.../<entityId>` URL). Typing **/** in a page body adds *content blocks within a page*, which is different — use **+ → New entity**.

Say:
"Let's create it:
1. Click the **+** at the **top-right** → **New entity**. A fresh entity page opens.
2. In the title field (**'Entity name…'**), type your greeting — the classic is just **'Hello World'** (or make it yours, like *'Hello from [name]'*).

That's a real entity in the graph — tell me when its name is set!"

[STOP — wait until the entity exists and is named.]

### Step 7: Give it the "Greeting" type (2 min)

Say:
"Now let's tell Geo *what kind of thing* this is — its **type**. This space already has a **'Greeting'** type made for hello-worlds like yours, so we'll reuse it (reusing existing types is exactly the right habit — it keeps the graph tidy and connected).

1. Click **'Find or create type…'**.
2. Type **Greeting** and pick the **existing 'Greeting'** option from the list (don't make a new one).

Tell me when 'Greeting' shows as the type."

[STOP — confirm the Greeting type is attached. Note: type search is fuzzy, so make sure they pick the *existing* Greeting, not 'Create new'. If it doesn't appear, have them keep typing 'Greeting' exactly.]

### Step 8: The "who" — sign it with Authors (3 min)

This is the lesson's one **relation**, and a lovely callback: the Author is the learner's **identity** from Module 2.

Say:
"Now let's capture **who** made this. Your entity already shows an **Authors** field (it comes with the Greeting type). This is a **relation** — a link to another entity — and the entity you'll link is **you**: the identity you created back in Module 2.

1. Right under **Authors** there's a **'Find or create…'** field. Just **start typing your name / handle** there (the one you named your personal space) — no button to click first.
2. Pick **your identity** from the list that drops down.

You should see yourself listed as the author. That little link is a real relation in the graph — your hello is now connected to *you*. Tell me when your name shows under Authors."

[STOP — confirm they're listed under Authors. If they don't find themselves, check they're typing the exact name they gave their personal space in Module 2.]

### Step 9: The "when" — stamp it with Created At (2 min)

This teaches a **property** (a typed value), to pair with the relation from Step 8.

Say:
"Now the **when**. Right under **Created At** is a date/time box (it shows **YYYY / MM / DD — 00:00 AM**). That's a **property** — a typed *value*, rather than a link to another entity.

Click into the **Created At** date and set it to **today** (you can leave the time as it is).

Nice — so where **Authors** *links* to another thing (a relation), **Created At** just *holds a value* (a property). Two different building blocks, side by side. Tell me when the date is set."

[STOP — confirm Created At has a value.]

### Step 10 (optional): Add a message (1 min)

Only if the learner wants to. Say:
"Optional — click **'Add a description…'** (under the title) and write a line, e.g. *'Just joined Geo through the onboarding course!'* Totally fine to skip and keep it tidy."

[Optional and light. If they pass, move on.]

### Step 11: Recap → next (1 min)

Say:
"Look at that — you created a real entity inside a shared community space, and it tells a whole little story — **what, who, and when**:
- ✅ You **joined** the Geo Onboarding Space
- ✅ **What:** a **'Hello World'** entity, typed **Greeting** (reusing an existing type)
- ✅ **Who:** a **relation** — **Authors → you** — linking your hello to your identity
- ✅ **When:** a **property** — **Created At** — holding today's date
- ✅ That's the full GRC-20 toolkit (type + relation + property) on one entity, all via the **'find or create'** move

It's not live yet — because this is a community space, the final step is to **propose** it for the editors to approve. That's the next module. Run `/start-4-1`."

## Pacing instructions
- The membership step has a **~5-minute bot window** — fill it productively (Steps 3–4) and **don't rush past the approval check**. Building won't work until they're a member.
- Keep the build to **one entity**. Name (a greeting) + **Greeting** type + **Authors = themselves** + **Created At = today** is the whole task; a description is optional flavor. Resist scope creep back into multi-entity graphs.
- Lean on the **what / who / when** frame: name = what, Authors = who (a relation), Created At = when (a property). It makes the type/relation/property distinction click without jargon.

## Important notes
- **One entity, simple.** The big multi-entity modeling was the *paper* exercise in Module 1. Here the win is "I made one real thing on a shared graph, signed by me" — small and satisfying beats thorough.
- **Reuse the Greeting type** (don't create a duplicate). Search "Greeting" and pick the existing one — modeling the reuse habit. Type search is fuzzy, so make sure they pick the existing type, not "Create new".
- **Authors = their own identity.** The author they link is the personal space they made in Module 2 — a nice, concrete relation that ties the course together. If they don't find themselves, check they're searching the name they gave their personal space.
- If the live UI differs from the reference map, believe their screen: the pattern is *open space → join → (member) → edit mode → `+` New entity → name → Greeting type → Authors (yourself) → Created At (today) → (optional description)*.
- Lots of encouragement — this is their first contribution to shared, community knowledge.
