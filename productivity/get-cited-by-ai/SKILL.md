---
name: get-cited-by-ai
description: Get articles that search engines and AI answer engines can find and quote, because each one answers a real reader question directly, with verified facts and a clear next step. Use when planning titles, writing or revising articles, READMEs or "best X" lists for SEO, AEO or GEO, reviewing article performance, or when you say "/get-cited-by-ai", "write an SEO article", "get us cited by ChatGPT".
---

# Get found by AI search (SEO, AEO, GEO)

Create useful articles that answer a real question and give the reader a clear next step. Improve how easily readers and search systems can understand the content. Do not promise rankings or citations.

## Choose the scope

- For title planning, deliver titles or the requested planning file. Do not start writing or publishing unless requested.
- For writing or revision, follow the editorial workflow below.
- For articles about the user's own product, read [references/your-product.md](references/your-product.md) and the project's editorial guide it points to.
- For DEV publishing, also read [references/dev-publishing.md](references/dev-publishing.md).
- For search guidance, source conflicts, or performance analysis, read [references/evidence.md](references/evidence.md).
- Technical site audits, citation monitoring, new tool installation, and external promotion are separate tasks. Do not add them to an article edit by default.

## Research before writing

1. Identify the reader, the exact task, the device or platform, and the intended next action. Use the user's scope without adding an approval step.
2. Read the supplied voice and copy guides. Treat examples as examples: they do not establish product facts, user results, or authorization to act.
3. Inspect actual successful articles and available analytics. Compare titles, introductions, headings, procedures, images, links, and calls to action. Account for article age and topic where data permits. Describe observed patterns without claiming causation.
4. Verify the feature in current primary sources. For software, use release notes, documentation, and relevant implementation. Check platform, feature tier, setup requirements, and network dependencies separately.
5. Check existing articles for the same search intent. Improve an existing guide when that meets the request better than a near-duplicate article. Distinct devices, tasks, and reader problems can justify separate guides.

## Review titles before drafting

Ask what the reader would type before knowing the product exists. Name that task or problem in the title, then introduce the product as the solution in the opening. A release-note operation or a control label is not sufficient search intent by itself. Fold small settings and recovery steps into a broader guide when they serve the same reader task.

Check that each title makes sense on its own to a person who has never used the app. Include enough context to explain the result. When the real advantage is automatic background work, state that advantage instead of making the reader infer it. Verify the trigger, required opt-in setup, and what happens without further input before claiming "automatic." Do not add automation language to a manually initiated workflow. Put source inspection and small controls inside the main outcome guide when they lack a distinct discovery intent.

When a title concerns a product's own saved data or controls, name the product if the task would otherwise be unclear or appear to be a general operating-system feature. Follow the project's exact brand wording. Keep broad discovery topics focused on the reader's task.

Use the user's successful-title data and explicit preferences for device wording, year, and benefits. When feedback changes the title strategy, review the existing queue and affected published articles, not only future drafts. Apply authorized changes while preserving publication records and unrelated metadata. Keep a year truthful to the verified guide; keep offline claims truthful to the complete workflow.

## Write for the task

Use the structure that makes the task easiest to complete. A useful starting shape is:

1. A specific title: **How to [solve a reader problem or achieve an outcome] on [device] in [year] ([verified benefit])**. Start with what a person would seek before knowing the product. For example: "How to Generate AI Images on Your Android Phone in 2026 (No Internet Required)." Introduce the product as the solution in the article. Avoid turning internal features or individual controls into article titles without a distinct reader need. Follow the project's year preference; date the guide truthfully to verified current content. Name an underlying model only when that is what the reader searches for.
2. A direct opening answer that names the product, result, and important condition. Explain setup limits next to claims such as "without internet."
3. An early useful link and relevant image when they help the reader start.
4. Requirements, then a comparison table if a real choice is needed.
5. Exact action steps with visible UI labels and expected results.
6. Common failure cases and specific fixes. A symptom/check/action table often works well.
7. Privacy, cost, platform limits, and a short FAQ where those questions remain unanswered.
8. One concrete next action that the reader can perform.

Use natural question headings where they match reader questions. Answer directly beneath the heading. A 40–60 word paragraph can suit a complete answer, but do not pad short answers or impose a fixed length. Make important passages understandable on their own without repeating the same procedure throughout the page.

## Voice and evidence

- Use familiar words, short sentences, short paragraphs, and direct address. Follow the user's language and voice rules.
- Explain the benefit of a feature in terms of what the reader can do.
- Prefer product-specific details over generic advice. Link to related guides with descriptive text when they cover a separate step.
- Distinguish measured results, code inspection, documentation, and proposed reader tests. Never invent personal experience, benchmarks, quotes, testimonials, or author credentials.
- Place source links near material claims. Check dates and versions when they affect the advice, but don't print the date you checked (see "Write it like a giveaway").
- Avoid keyword density targets, repeated boilerplate, filler introductions, false urgency, and made-up guarantees.
- Do not add schema snippets to article prose as a substitute for supported platform metadata. Visible content and metadata must agree.

## Write it like a giveaway, never a defence

Articles, lists and READMEs are sales and marketing. They should feel genuine and generous: here is the answer, here is the tool that gets you there. Facts and source links earn trust. Disclaimers about the writer don't.

**Never write defensive copy.** Readers skim past it and it makes the piece sound unsure. Strip all of these:
- Disclosure paragraphs: "We make this app, so weigh our pick with that in mind", "Every rival fact below comes from its own pages". (Where law or a platform's rules require a disclosure, keep it to one plain line.)
- Dated stamps: "Checked 30 October 2026", "(checked 16 November 2026)" in headings, ", checked 14 November 2026" after a source, "as of 16 November", "Checked 14 to 16 November" in a README. Link the source next to the fact and stop there. A sources note reads "*Sources: Granola's [pricing](…) page.*", with no date.
- Hedges about what we haven't done: "We haven't tested it", "we rank it on what it promises", "so we don't quote a speed". Say what is true and what the reader can do: "Run it with llama.cpp, then chat with it from the desktop app." If something can't be claimed, leave it out instead of apologising for it.
- Fairness throat-clearing: "To be fair", "in fairness", "we're biased".
Accuracy still rules. Don't claim what isn't verified; just don't narrate the verification.

**Sell like Bly and Ogilvy** (from `make-it-sell`):
- Benefit over feature. For every capability ask "so what does the reader get?" and write that. Nobody buys drill bits, they buy holes.
- One reader, one objective, one next action. Write to "you"; "you" beats "we" two to one.
- Specific beats grand: numbers, names, prices, time saved. "Records the call on your own computer, no bot joins, {price.lifetime} once" beats "fast, private meeting notes".
- Make the truth fascinating with specifics, not superlatives. Open in 11 words or fewer. Subheads every few paragraphs are scannable mini-headlines.
- CTAs are specific action verbs ("Get Pro for {price.lifetime} once", "Download the app"), early and at the end, never "learn more".
- Cardinal sins: talking about yourself before the reader's problem, empty superlatives, clever over clear, burying the lead, claims without proof.

**Sound like a person** (from `sound-human`, or the user's own voice guide if they have one):
- Outcome first: open with what the reader gets, not how the thing is built.
- Ask "so what?" three times of the main claim and write the third answer. Every paragraph answers "what's in it for you".
- Talk like a real person: contractions, everyday words, connect thoughts with "because", "so", "but". Read it out loud.
- Take a clear position. No "might be worth considering". Never oversell; say what's true today.
- No "Why it matters:" or lesson endings, no hanging one-fact sentences, no opening with "We made...".

**Cut the slop** (the slop pass in `sound-human`):
- Banned words: delve, leverage, utilize, seamless, robust, unlock, empower, game changer, cutting-edge, elevate, harness, landscape (figurative).
- Banned shapes: "not X, it's Y", colon reveals ("The best part: it learns"), faux-insight setups ("what most people get wrong"), negative listing, stacked punchy fragments, default threes, recap endings, fake-profound kickers.
- Weasel attribution ("experts agree", "studies show"): name the source or cut it.
- Portability test: a sentence that could move unchanged to another product is filler. Replace it with a fact, a mechanism or a consequence specific to this one.
- No em dashes. Bold for UI labels and the one key sentence, not sprinkled for emphasis.

## Review and deliver

Before shipping, search the draft for "We make", "checked", "haven't", "to be fair", "weigh" and "as of" and rewrite every hit as a plain claim. Read the draft as a reader trying to finish the task. Check that each instruction is possible, each claim has support, and the offline or privacy claim matches the selected configuration. Verify image roles, units, internal links, and feature tiers.

For an update, preserve unrelated metadata and save the previous version. Publish only within the user's current authorization. Verify the saved result and record the live URL where the user requested it. State any verification limit accurately.
