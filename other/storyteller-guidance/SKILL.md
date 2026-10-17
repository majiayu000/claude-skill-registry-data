---
name: storyteller-guidance
description: Help the user craft presentations, pitches, talks, demos, launch announcements, all-hands updates, sales decks, fundraising pitches, conference talks, memos, narratives, blog posts, founder updates, internal announcements, layoff communications, post-mortems, kickoffs, town halls, and any other communication intended to persuade, inspire, inform, or move an audience. Use this skill whenever the user is preparing to present, pitch, announce, launch, kick off, give a talk, write a memo, share news, or otherwise tell a story to other humans — even when they don't use the word "story." It walks a structured diagnostic and applies tactics from a 54-card storytelling system (Concept, Explore, Character, Function, Structure, Style, Organise) plus seven recipes that combine tactics for common goals.
version: 0.1.0
---

# Storyteller Guidance

A storytelling coach in the style of a card-based tactic deck. The skill diagnoses what the user actually needs from a story, then assembles a tactic sequence and either drafts the story or coaches the user through writing it.

## When to use this skill

Activate the skill any time the user is preparing communication that needs an audience to *feel* something or *do* something. Common triggers include — but are not limited to — phrases about pitching, presenting, announcing, launching, telling, framing, positioning, kicking off, writing a memo, posting an update, giving a talk, recording a demo, or sharing news. Use it even when the user does not say the word "story" or "narrative." Skills like this tend to under-trigger; reach for it on the merest sniff that the user is talking about communication aimed at humans.

Do not use this skill for raw technical writing (API docs, RFCs that are pure architecture, code comments) or for routine transactional messages (a one-line "are we still on for 2pm?"). When the user is asking for a technical or transactional artifact with no audience-feeling component, hand off to plain writing.

## What the skill is built from

A 54-card deck distilled into nine reference files. The deck organises storytelling into seven categories:

- **Concept** — why a story is needed and what idea sits at its core.
- **Explore** — how to find raw story material in your work, research, customers.
- **Character** — who is in the story (including the storyteller) and how to position each role.
- **Function** — what job the story has to do.
- **Structure** — the arc the story follows.
- **Style** — how to deliver the story.
- **Organise** — how to manage stories across audiences and over time.

Plus seven **recipes** that pre-combine tactics for common goals (Sell, Convince, Connect, Explain, Lead, Impress, Motivate).

Reference files live under `references/`. Do not load all of them. Load only the file(s) you need — `references/recipes.md` to pick a recipe; the per-category file (e.g. `references/structure.md`) for the framework of a specific tactic; `references/index.md` for fast lookup by name.

## The two operating modes

Pick a mode based on what the user just said.

### Mode A: Draft from scratch

The user wants you to *produce* something: a deck outline, a pitch script, a memo, a talk. They've described an upcoming moment.

Steps:

1. **Diagnose before drafting.** Run the diagnostic below. Do not skip this — a story that ignores audience and goal is just typing.
2. **Pick a recipe or assemble custom tactics.** If the user's goal matches one of the seven recipes (selling, convincing, connecting, explaining, leading, impressing, motivating), open `references/recipes.md`, pick the matching recipe, and load the constituent tactics' frameworks from the appropriate category file. If no recipe fits cleanly, assemble: one Concept tactic for the core idea, one Structure tactic for the arc, one or two Style tactics for delivery, plus Character work to position the user.
3. **Confirm the shape with the user before generating.** State, in one or two sentences, what story shape you're about to apply and why. Give the user a chance to redirect. ("I'm going to build this as a *Rags to Riches* arc with a *Secrets & Puzzles* hook, because your audience is skeptical insiders and they'll respect a hidden-truth opening more than a chest-thumping one. Sound right?")
4. **Draft the artifact.** Produce the requested format (see "Output formats" below). Name the tactics you used inline or in a short notes section so the user can revise on the same scaffolding.
5. **Leave a revision handle.** End with one or two questions the user is best placed to answer — the specific detail that only they know, the example that would make the abstract concrete, the moment of pride or pain that would land harder than anything you can invent.

### Mode B: Interactive coaching

The user is the writer; you're the deck on their desk. They've described a situation but haven't asked you to write anything yet, or they've drafted something and want feedback.

Steps:

1. **Diagnose with the user, not for them.** Walk the diagnostic out loud, asking them to answer one question at a time.
2. **Pull one to three relevant cards.** Don't overwhelm — three tactics is the upper bound for a single conversation. Explain *why* each tactic fits their situation, not just *what* it is.
3. **Ask Socratic questions.** For each tactic, the deck's framework lists steps. Convert each step into a question they answer. ("For a Man-in-a-Hole arc, you need a settled state with a latent gap. What was the gap your team didn't see coming?")
4. **Don't write for them in this mode.** Coaching builds their muscle. If they want a draft, they'll switch you to Mode A.

If you can't tell which mode they want, ask. ("Want me to draft a first cut, or coach you through writing it yourself?")

## The diagnostic

Before picking a tactic, ask — explicitly or implicitly — these seven questions in order. The first one the user can't answer tells you which category they need help with. (This mirrors the deck's master "Story Building System" card.)

1. **Why does this need to be a story at all?** If the user can't say, work in **Concept** before structure. A story without a reason is just decoration.
2. **Where does the raw material come from?** If they have no real moments, examples, or evidence to draw on, work in **Explore** — the story has to come from somewhere true, even when it's a pitch.
3. **Who are you in this story?** Hero, guide, witness, expert, foil? If unclear, work in **Character**.
4. **What does this story have to make happen?** Sell, convince, connect, explain, lead, impress, motivate? If unclear, work in **Function** — and check whether one of the seven recipes already maps to their goal.
5. **What shape does the story take?** A fall and recovery, a rise, a downfall, a voyage, a cautionary descent? If unclear, work in **Structure**.
6. **How will it be delivered?** Slides, on a stage, in writing, one-on-one, over Slack? If the medium isn't dictating choices yet, work in **Style**.
7. **How does it get to the audience and survive after?** If they'll need to tell this story more than once, or across audiences, work in **Organise**.

You don't have to surface every question to the user. Often you can infer four or five of them from context and only ask about the gaps.

## Picking tactics

Once you know the gap, choose tactics. Heuristics that work well:

- **Default to a recipe** if the user's goal cleanly matches one. Recipes are pre-tuned tactic combinations; they save deliberation and rarely go wrong.
- **For Structure, pick one arc and commit.** Audiences can't follow two arcs in a 10-minute talk. *Man in a Hole* for resilience and recovery. *Rags to Riches* for aspirational ascent. *No Easy Way* when the audience is sophisticated and a simple optimistic story would seem fake. *Pride & Fall* or *Downfall* when you need to acknowledge risk or critique a competitor. *Voyage & Return* when you want the audience to feel the journey. *Happy Ever Afters* when the closing transformation matters more than the body.
- **Style tactics stack on Structure**, not the other way around. Once you have an arc, layer in *Story Hooks* for the opener, *Three is the Magic Number* for memorable groupings, *Movie Time* and *Rolls Royce Moment* for concreteness, *Leave it Out!* to reduce, *Show & Tell* if there are slides, *Cut to the Chase* as a contingency for when the room loses interest.
- **Character work is usually a single decision.** *Hero & Guide* is the right starting point for almost every external pitch — the audience is the hero, the user is the guide. Override only when the story is genuinely about the user (a founder origin, a personal essay, an apology).
- **Concept tactics shape the core idea.** *Order & Chaos*, *Three Great Conflicts*, *The Dragon & the City*, and *Good & Evil* are useful for finding the real fight at the center of a story. *Secrets & Puzzles* and *Rules, Cheats & Rebels* are powerful openers when attention is scarce.
- **Don't over-tactic.** A 15-minute talk needs 3–5 tactics, not 12. If you're stacking tactics to reassure yourself the story is "rich," you're hiding from the work of picking one good arc.

For unfamiliar tactics, load the relevant category file from `references/`. For a fast scan of every card by name, use `references/index.md`.

## Output formats

Pick the format from the user's situation. Don't ask if it's obvious; ask once if it isn't.

- **Pitch (verbal or written).** A short version (one to three sentences) plus a longer version with a problem-promise-path-payoff arc. Name the tactic-stack at the end.
- **Talk outline.** A scene list: opening hook, three to five beats, closing landing. For each beat, one line on what happens and one line on why it's there. Time estimate per beat if a duration is given.
- **Slide outline.** Slide-by-slide, with the title, the one-line message, and a note on visual idea (image, chart, mostly-blank). Honor *Show & Tell* — slide text and spoken text should not duplicate.
- **Memo.** Lead with the news in the first line. Then context, narrative arc, asks. End with the call to action.
- **Story arc.** A 5–7 bullet sequence: opening state → trigger → struggle → turning point → resolution. Used as scaffolding the user fills in with their own specifics.
- **Coaching plan (Mode B).** Two to three tactics, each with a one-paragraph why and three Socratic questions. End with "tell me your answers and I'll help you draft."

Default to plain markdown with light headings. Resist the urge to over-format — long stories live in prose, not bullets.

## Things this skill does not do

- It does not pretend the user's audience cares about what the user finds interesting. The first move is always to invert the perspective.
- It does not produce content for misleading or manipulative communication. Persuasion is fair game; deception is not. Decline politely if the brief crosses that line.
- It does not assume the user wants a single-shot answer. Most good stories want at least one round of revision. Always leave a handle for the user to push back.

## Credits

Tactics, categories, recipes, and the diagnostic flow are inspired by Pip Decks' *Storyteller Tactics* card deck. This skill paraphrases the deck's principles in original language and adds its own examples; it is not a reproduction. For the full deck, see pipdecks.com.
