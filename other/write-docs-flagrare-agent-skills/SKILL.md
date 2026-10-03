---
name: write-docs
description: Write documentation that reads like a person wrote it for another person. The skill teaches the craft layer first, how to set context, how to calibrate tone, how to escape the curse of knowledge, when prose beats a bullet list, and only then the structural conventions (Diátaxis modes, README landing-page arc). Use whenever you're writing or restructuring a README, a docs tree, a CONTRIBUTING file, a guide, an architecture document, or any other documentation surface.
---

# Write docs

Most bad documentation is not unclear, ungrammatical, or factually wrong. It is technically correct prose that nobody wants to read, written by someone who already knows the answer for an imagined reader who knows almost as much. The fix is not another style rule. The fix is to write the way a person teaches another person, assuming nothing, leading with the situation the reader is actually in, providing context where it lands rather than where it's tidiest, and resisting the urge to convert every paragraph into a bulleted enumeration.

This skill teaches the craft first and the conventions second. The craft is what makes a docs page feel earned. The conventions just keep you out of the most expensive failure modes.

Four sources do the heavy lifting:

- **[Steven Pinker, *The Sense of Style*](https://www.psychologicalscience.org/observer/the-curse-of-knowledge-pinker-describes-a-key-cause-of-bad-writing)** for *the curse of knowledge* and *classic style*.
- **[Chip & Dan Heath, *Made to Stick*](https://heathbrothers.com/made-to-stick-introduction/)** for *tappers and listeners* (Newton 1990) and concrete-over-abstract diction.
- **[Mailchimp Content Style Guide](https://styleguide.mailchimp.com/voice-and-tone/)** for *voice is consistent, tone shifts*.
- **[Diátaxis](https://diataxis.fr/)** + the celebrated landing pages (React, Stripe, Anthropic, SpacetimeDB, Tokio) for *structural shape*.

## When to invoke

Whenever you're writing or restructuring documentation, a README, a docs tree, a CONTRIBUTING file, a guide, an API reference, an architecture document, an FAQ, or release notes (though release notes have their own skill at `/flagrare:release-check`). Invoke proactively after implementing a feature whose docs need to land alongside the code, or when a staleness audit surfaces documentation drift as the blocker.

This skill does **not** handle changelogs or release notes themselves, `/flagrare:release-check` owns those with its own voice (Valve Dota patch notes).

## The procedure

### 1. Start with the reader's situation, not the page's topic

The single most useful question to ask before writing the first sentence is: *what just happened to the reader, that they ended up on this page?* They Googled an error message. They followed a link from a tutorial. They're three months into using your library and just hit an edge case. They're a new team member reading the docs because their manager said to.

The reader's situation is the context you have to honor. Pinker calls the failure to do this **the curse of knowledge**: "a difficulty in imagining what it is like for someone else not to know something that you know." The Heath brothers ground this in Elizabeth Newton's 1990 Stanford experiment, the *tappers and listeners* study: tappers were asked to tap the rhythm of a well-known song on a table while listeners tried to identify it. Tappers predicted listeners would get it 50% of the time. The actual rate was 2.5%. The tapper hears the melody in their head. The listener hears Morse code.

Every paragraph of mediocre documentation is a tapper writing for someone who can only hear taps. The antidote is structural: do not open with what the page is about. Open with what the reader is trying to do.

Look at how React's "Thinking in React" begins, *"React can change how you think about the designs you look at and the apps you build."* The opening sentence names a shift in the reader, not a feature of the library. Or Anthropic's prompt-engineering page, which leads with a preconditions block: *"This guide assumes that you have a clear definition of the success criteria…"*, the reader's state is acknowledged before the page proceeds.

Compare those with the failure mode you've seen a thousand times: *"This document describes the configuration options for the X system."* That sentence has done zero work. It's metadata.

So: before you write anything, name in one sentence what the reader was doing two minutes ago. Then write a first sentence that meets them there.

### 2. Identify which kind of doc you're writing

There are four. They are not interchangeable, and most documentation problems are mode-confusion problems, a tutorial that's really a feature tour, a reference page that lectures, a how-to guide that opens with a paragraph of theory. The four-mode framework comes from [Diátaxis](https://diataxis.fr/) and has been adopted by Python, Ubuntu, Canonical, and Cloudflare.

| Mode | Question it answers | Reader's state | Form |
|---|---|---|---|
| **Tutorial** | "How do I learn this?" | Novice; seeking confidence | Narrative, imperative, step-by-step. Ends with the reader having built something real. |
| **How-to guide** | "How do I do X?" | Competent; pursuing a specific goal | Directive, conditional, assumption-laden. Skips theory; links to it instead. |
| **Reference** | "What is/are…?" | Practitioner; seeking facts | Declarative, atomic, scannable. Each entry stands alone. |
| **Explanation** | "Why? What does this mean?" | Reader; seeking understanding | Discursive. Explores trade-offs. Does not prescribe action. |

When the call is close, ask the decisive question. *Tutorial or how-to?* Is the reader learning the domain, or already trying to do something specific. *How-to or reference?* Does the reader know why they're here. *Reference or explanation?* Is this what it is, or why it matters. *Explanation or tutorial?* Is this building understanding, or capability.

If you can't pick one mode for the page, the page is trying to do two jobs. Split it.

### 3. Write to be seen through, not at

Pinker's *classic style* is the second-most-important idea in this skill. The metaphor is *seeing*: the writer has been somewhere, has noticed something, and is now orienting the reader's gaze so that the reader sees it too. The writer is a guide, not a performer. The reader is a collaborator, not an audience.

Classic style is the opposite of two failure modes you'll recognise.

The first is **performed expertise**: prose that's secretly about the writer's competence rather than the reader's understanding. Long sentences with multiple subordinate clauses. Latinate vocabulary where Anglo-Saxon would land. Hedging and qualifying where direct would land. *"It is generally considered that…"*, by whom, and why are they hedging?

The second is **mechanical recipe-card mode**, where every paragraph collapses into the same texture: a heading, a list of three bullets, a code block, repeat. This is the failure mode the user critiqued in the earlier draft of this skill. A docs page made entirely of enumerations has nowhere for *causality* to live. *X happens because Y* and *do X before Y or you'll hit Z* and *X is fast when Y is small* all become *X. Y. Z.* The reader has to reassemble the relationships you flattened.

The remedy is small and concrete. Prefer verbs over nominalized verbs, *"the request is cancelled"* beats *"cancellation of the request occurs"* (Pinker calls these zombie nouns). Prefer concrete nouns over abstract ones, *"the colleague who joined yesterday"* lands harder than *"a less-experienced reader."* Trust the reader to follow a sentence with a comma in it; not every clause needs to be its own bullet. And every so often, ask whether the next thing you're about to write needs to be a list, or whether it's three steps that depend on each other and would be clearer as a paragraph.

The Stripe docs do this routinely. They could have written:

> A `PaymentIntent`:
> - Tracks the customer payment lifecycle
> - Records failed attempts
> - Guarantees the charge runs once
> - Provides a client secret for the frontend

They wrote:

> A `PaymentIntent` tracks the customer payment lifecycle, recording all failed attempts and ensuring the charge runs only once. Return the `client_secret` of the `PaymentIntent` in the response to complete the payment on the client.

The prose carries the causality the bullets erased. "Recording… and ensuring…" tells you these are *consequences* of tracking the lifecycle, not co-equal features. "Return the client secret in the response *to complete* the payment" tells you what depends on what.

Use lists for things that are genuinely parallel and order-independent, a roster of supported languages, an error-code table, the cells in the Diátaxis matrix above. Use prose when one thing causes, requires, or depends on another. Most of technical writing is the second.

### 4. Provide context where it lands, not in a glossary

Reader context is the second-most-common reason a docs page fails (after mode confusion). The writer either gives the reader too much context up front, a five-paragraph background section the reader will skip, or too little, and the reader doesn't know what a `client_secret` is by paragraph three.

The good docs put context at the point of need, not in a glossary that ships separately. Stripe again: when the reader hits the term `client_secret` for the first time, they get the definition inline, in a parenthetical, in the same sentence: *"Return the client secret (a unique key returned from Stripe as part of a `PaymentIntent`…) of the PaymentIntent in the response."* The reader who already knows skips the parenthetical. The reader who doesn't gets the definition where they need it. Nobody is sent to a glossary tab.

A few moves to reach for, all attributable:

- **Name what you're assuming**, up front (Anthropic's preconditions block). *"This guide assumes you have a Stripe account and have installed the Node SDK."* The reader who lacks one of those self-selects out before they get lost.
- **Name what the project *is* before naming how to install it**, especially on multi-component projects. If the codebase is a Rust engine exposed to Python via PyO3, or a JVM library with a native core, or a C library with multi-language wrappers, name that fact in two sentences before the install commands appear. The reader landing in your Quick Start may not yet know whether they're installing a library, a service, or a CLI tool; whether they need a compiler; whether the language on the badges is the language they'll actually call. Forcing them to reverse-engineer the architecture from `pip install` output is unkind. *"TardigradeDB is a Rust engine with a Python API; the install command is `pip install tardigrade-db` regardless of what language you write your consumer in"* costs almost nothing and answers the question every reader was already asking.
- **Pre-announce the error the reader will hit** (React's pattern). *"You'll see a console warning here, that's expected, and we'll fix it in the next section."* Surfacing the failure mode before the reader encounters it converts a frustrating moment into a validating one.
- **Name the gap you don't fill.** When a feature path is unsupported, say, *"there is no third-party Rust API today; the workspace crates are unpublished and not designed as a public surface"*, say so in the same paragraph where the option would have appeared, not three pages later when the reader has already started trying it. Honest gap-naming pairs with the preconditions block: it lets the reader who can't use a path self-select out, and lets the reader who *can* work around the gap (fork and path-depend, embed Python, wait for the roadmap item) make that decision deliberately. The honest move is also the kind one.
- **Drop the definition inline, not in a sidebar.** A parenthetical, a footnote, or a single sentence at the moment of first use. Reserve glossaries for the cases where the term appears many times across many pages.
- **Lead with the conclusion, then back up the claim** (the inverted pyramid; GOV.UK's house style). The opening sentence states what's true; the rest of the paragraph supports it. Don't make the reader wait for the verdict.
- **Treat the reader as a collaborator, not a recipient.** Ask them direct questions when you want them to think: *"Which of these are state? Identify the ones that are not."* React uses this constantly. The reader who answers in their head is now learning rather than scanning.

What these moves share is that they put the context in the reader's path *exactly when the reader needs it*, not earlier, where it bores them, and not later, where it's too late.

### 5. Calibrate tone to the reader's state, keep your voice constant

Mailchimp draws a useful distinction: **voice is consistent, tone shifts.** Your project's voice, the underlying personality the docs sound like, stays the same across every page. The tone, how warm, how careful, how decisive, calibrates to the reader's situation on each specific page.

A reader following a Sunday-afternoon tutorial wants warmth and patience. A reader debugging a production outage wants decisiveness and brevity. A reader on a reference page wants you out of their way. The voice can be the same person speaking; the tone is which mood that person is in.

Concretely:

- React's docs sound friendly without sounding like a tweet. The warmth comes from second-person address and direct questions, *"Notice that editing this works,"* *"Start by drawing boxes around every component and subcomponent in the mockup"*, inside sentences that are otherwise syntactically careful. Contractions yes, *"Awesome!"* no.
- Stripe sounds decisive without sounding bossy. *"Stripe recommends using the Checkout Sessions API… Don't use Payment Intents directly unless…"*, directive but not lecturing.
- Anthropic's prompt-engineering docs sound technical without sounding cold. The preconditions block reads like a colleague's email, not a man page.

What unites them: contractions are fine inside structurally careful sentences. Imperatives address the reader directly without exclamation marks. Humor, if it appears at all, is dry and never explained. If a joke needs a footnote, cut the joke.

Avoid two specific failure modes. **Performed casualness**: *"So, basically, you'll just want to grab the SDK and, like, get cooking!"*, is condescending and reads as a brand voice rather than a person's voice. **Performed formality**: *"It is hereby recommended that the practitioner first establish their development environment…"*, is the same problem in the opposite direction. Both are the writer thinking about themselves rather than the reader.

### 6. The README is a special form

A README is not a docs page. It is the project's storefront, the only thing many readers will ever see. It compresses all four Diátaxis modes into one page, plus does brand work the rest of the docs don't have to. It has a different shape than anything else you'll write, and the shape is non-negotiable because every celebrated example converges on roughly the same one.

The shape that wins (verified across SpacetimeDB, Tokio, RocksDB, Qdrant, Stripe's homepage, dvc, choo, gofiber):

```
1. Title + ≤6 badges (one row, no vanity badges)              ~5 lines
2. Status line + 2-3 sentence pitch                           ~10 lines
3. Hero example, runnable, real, copy-pasteable              ~20 lines
4. Why / decision criterion ("use this when / reach for X     ~15 lines
   else when")
5. Features table (Capability → Status → Where to learn more) ~20 lines
6. Performance snapshot (3-5 honest numbers, link to bench)   ~20 lines
7. Architecture diagram + one paragraph                       ~25 lines
8. Quick start (one path per audience, audience-tagged)       ~30 lines
9. Project status (current version, what's stable, what's     ~15 lines
   experimental, one-sentence audit link if relevant)
10. Documentation map (Architecture, Guides, Community,       ~15 lines
    Roadmap)
11. FAQ (name origin, recurring questions, design principles, ~30 lines
    terse comparison), short, scannable
12. Acknowledgments + License + Citation                      ~10 lines

Target total: 200-300 lines.
```

The first 80 lines are the only part that matters to most readers. They must answer *what is this, why should I care, how do I try it.* No retraction walls. No research diary entries. No 30-item milestone checklists. If your project has a benchmark methodology that's currently under audit, that lives in the Project Status section near the bottom, behind a one-sentence link, not at the top of the page.

The hero example is the single most load-bearing section. If you cannot write a 10-to-20-line snippet that does something *real* on a fresh install, `pip install <name> && python -`, your project's onboarding is broken before the docs are. Fix the onboarding before you ship the README.

Several things stay out, no matter how tempted you are. Long narrative introductions. Generic motivational language, *"revolutionise"*, *"game-changer"*, *"next-generation"*. A Table of Contents in a ≤500-line doc (it just clutters the top). The full changelog (link to `CHANGELOG.md`). The full roadmap (link to `docs/roadmap.md`). Detailed installation steps (link to the contributor or user guide). Multiple "Getting Started" sections aimed at different audiences without explicit audience tagging.

Several things are mandatory and easy to forget. A link to `LICENSE`, `CHANGELOG.md`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SECURITY.md`, and `CITATION.cff` if the project is research-adjacent. A truthful status line, pick one of *Research-grade preview*, *Beta*, *Stable*, *Archived*, and own it. And the hero example, again, because it's that important.

#### Label Quick-Start paths by intent, not by audience

The most common Quick-Start failure on multi-language projects is heading the subsections with audience labels, *"Python users"*, *"Rust contributors"*, *"Java developers"*. Audience labels route by identity. The Rust developer who lands on the page wanting to *use* the library now reads "Python users" and assumes that section doesn't apply to them, even though it does, because the project's only third-party API happens to ship as a Python wheel. The reverse misroute happens too: the Python developer who wants to contribute reads "Rust contributors" and assumes they need to switch languages, when the contributor workflow is actually identical regardless of what language they call the library from.

Use intent labels instead. *"Using TardigradeDB from Python"* and *"Building TardigradeDB from source"* route by what the reader is trying to do, which is the only routing that's stable across the reader's actual mental state. *"Using"* means *the reader is calling the library*; *"Building"* means *the reader is modifying the library*. Whether they happen to write Rust or Python or Go elsewhere doesn't enter the routing decision. The label switch costs nothing and prevents an entire class of routing failure. (TardigradeDB hit this on 2026-05-21, the rewrite is `dac44c3e` in that repo.)

### 7. Self-check by reading it aloud

The cheapest, most reliable craft check is to read the page out loud. Sentences that work on the screen but choke on the tongue are usually sentences that nominalize a verb, bury the subject, or rely on visual structure (a bullet list) to carry a relationship the prose should have carried. If a paragraph makes you take a breath in the middle of a clause, the clause is too long.

Pinker's second remedy is to show the draft to a representative reader, someone who genuinely doesn't already know the answer. This is harder to arrange but more valuable. The version-of-you that already knows the answer is the worst reader you can imagine; the colleague who started yesterday is the best.

Before you ship a doc, run two passes. First: for every page, name in one sentence which Diátaxis mode it occupies and what the reader was doing two minutes before they arrived. If you can't, the page isn't ready. Second: for every section of the page, check that the opening sentence does some work, names the reader's situation, states a conclusion, asks a question, rather than describing what the section is about.

If the page is a README, run the additional check that the first 80 lines tell a stranger what the project is, who it's for, and how to try it. If they don't, restructure.

## Anti-patterns

**No em-dashes. Ever.** This is a hard rule, not a craft nuance: documentation this project produces must never contain an em-dash (the long dash), nor an en-dash used as one. They are a conspicuous AI tell and the reader finds them grating. Use a comma, a colon, parentheses, or two sentences, whichever the sentence actually wants. Numeric ranges take a plain hyphen (`3-5`, not a dash). This applies to every surface: READMEs, PR descriptions, TDDs, tickets, changelogs, standups, review comments. A repo hook flags any em-dash that slips into a generated `.md`, so treat it as enforced, not advisory.

Three failure modes show up in every documentation review. They are all forms of the same underlying problem, the writer is writing for themselves, not for the reader, but they look different on the page.

**Tutorial-as-tour.** The page says it's teaching the reader how to use the library, but there's no project the reader actually finishes. The page walks through features in the order the writer thought of them, with no destination. A tutorial without a finished artifact is a brochure. The fix is to commit to building one specific thing end-to-end, even something small, and to make every step land the reader closer to it.

**Reference-that-lectures.** An API reference entry that spends two paragraphs explaining the design philosophy of the endpoint before listing its parameters. Reference catalogs; explanation contextualises. Move the philosophy to an explanation page and link to it. The reference entry should be scannable: signature, one-paragraph description, parameters, returns, exceptions, example. Done.

**The endless useless enumeration.** A page that converts every paragraph into a five-bullet list. The reader gets through the page faster but learns less, because all the causality has been flattened. Use lists for things that are genuinely parallel; use prose for things that depend on each other. If you find yourself writing a list where each bullet starts with a verb and the next one assumes the previous one happened, that's a procedure, not a list, it can be prose.

A handful of smaller anti-patterns are worth naming, but they're checkable rather than craft-deep. Title-case headings (use sentence case; *"Create An Instance"* is dead, *"Create an instance"* is what every modern style guide uses). `-ing` heading openings (use the bare infinitive; *"Transferring data"* becomes *"Transfer data"*). Code font on product names (`Google Docs` reads as a class name; Google Docs reads as a product). README narrative intros ("Once upon a time, our team was frustrated with…", gone). And the granddaddy of them all: shipping the auto-generated CHANGELOG entry verbatim. Tooling output is a starting point, not a final product. See `/flagrare:release-check` for the rewrite discipline.

## Cross-references

- `/flagrare:editorial-pass` is the read-and-repair counterpart: this skill writes, that one reviews a finished draft whole-document (throughline, pacing, agent-noise deletion) and applies fixes on approval.
- `/flagrare:atdd-plan` for the doc structure that ships *alongside* a feature.
- `/flagrare:staleness-audit` runs before commit and surfaces doc drift (broken cross-links, stale version claims, references to removed symbols).
- `/flagrare:release-check` handles changelog and release-note writing, which has its own voice (Valve Dota patch notes). Do not duplicate that work here.
- `/flagrare:research-catalog` cross-links research artifacts back to the consuming docs.

## Why this exists

There is no shortage of advice on writing documentation. There is a shortage of advice that is *short, opinionated, citeable, and operationalises the craft layer*, the layer most style guides skip because it's hard to reduce to a checklist. Diátaxis tells you which kind of doc you're writing. Google and Microsoft tell you to use the active voice. The Heath brothers tell you why your reader can't hear what you're tapping. The trick is putting those three things into a single short document that a writer can reach for at the moment they're stuck on a paragraph.

The most expensive documentation failure is not a single bad page, it's a project whose docs grow without a shape, where every page has its own register, where the README absorbs every new feature's narrative until it's 756 lines long and nobody reads past the first screenful. Those failures are recoverable but expensive. The project at `/home/flagrare/Dev/ares-project/tardigrade-db` cut its README from 756 lines to 229 in May 2026, after about four hours of restructure work, because it had drifted exactly that way. Catching the failure at write time, by asking *what was the reader doing two minutes ago, and does this page meet them there?*, costs nothing.
