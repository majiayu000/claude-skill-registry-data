---
name: story-led-website-concept
description: Generates distinct story-led website concepts from a defined business problem, audience transformation, brand material, content evidence, and optional graphic-universe research. Use when a website or landing page needs a central creative idea, narrative structure, message progression, tone, and design implications before visual direction, wireframing, copywriting, or implementation begins.
license: MIT
compatibility: Portable Agent Skill. Can be copied into an Agent Skills-compatible environment with repository file access unless stated otherwise.
metadata:
  category: ui-ux-polish
  task_type: generator
  audience: web-designers-and-creative-directors
  tags:
    - creative-direction
    - website-concept
    - storytelling
    - narrative-design
    - art-direction
    - brand-story
    - concept-development
  status: draft
  side_effects: none
---

# Story-Led Website Concept

## Purpose

Turn a sufficiently understood business problem into distinct website concepts built around meaning, transformation, narrative, and evidence rather than a sequence of generic features and interface sections.

This skill works primarily with words before visuals.

It determines:

* what the website should fundamentally communicate
* which story or narrative lens can communicate it
* how the visitor's understanding should progress
* what evidence supports that progression
* how the concept should influence content, voice, imagery, layout, motion, and interaction at a directional level
* how the narrative supports the user's next action

The result is a set of concept directions ready for evaluation and later visual-system development.

This skill does not produce final copy, final layouts, detailed wireframes, a design system, or implementation code.

---

# Core principle

A strong website concept connects:

```txt
business problem
→ audience need
→ meaningful transformation
→ central idea
→ narrative progression
→ supporting evidence
→ user action
```

Visual decisions should later reinforce this chain.

Avoid:

```txt
interesting aesthetic
→ clever headline
→ arbitrary sections
→ decorative interactions
```

The concept should explain why the experience exists before explaining what it looks like.

---

# Story is not decoration

"Story-led" does not mean every website needs:

* a dramatic protagonist
* a cinematic scroll sequence
* a founder biography
* an emotional testimonial
* a beginning-middle-end screenplay
* a fictional narrative

Story can simply mean that information is deliberately structured so the visitor moves from one meaningful state of understanding to another.

Examples of valid narrative structures include:

```txt
problem
→ consequence
→ solution
→ proof
→ action
```

```txt
raw material
→ process
→ finished result
→ capability
```

```txt
old way
→ tension
→ new way
→ evidence
```

```txt
customer situation
→ challenge
→ experience
→ outcome
```

```txt
mission
→ obstacle
→ method
→ impact
```

```txt
question
→ investigation
→ revelation
→ implication
```

The appropriate narrative intensity depends on the project.

---

# When to use this skill

Use this skill when:

* A website brief has already been sufficiently understood.
* The user asks for a website concept, creative direction concept, central idea, narrative direction, storytelling structure, or story-led landing page.
* A page currently feels like a digital brochure or a sequence of disconnected feature sections.
* A homepage has information but lacks a clear progression or point of view.
* Several messages compete for priority and need to be organized around one central meaning.
* A brand has strong founder, customer, process, product, mission, or transformation material that could structure the experience.
* Graphic-universe research exists and needs to be connected to an actual website idea.
* The user wants several genuinely different creative concepts before choosing a visual direction.
* A product needs to demonstrate value through use, transformation, or evidence rather than simply listing capabilities.
* The design team keeps reaching visual execution before agreeing what the website is actually trying to say.
* A concept must connect headlines, imagery, content structure, calls to action, and eventual interaction into one coherent direction.

Do not use this skill when:

* The business problem or audience is still unclear.
* The user only needs visual inspiration or graphic research.
* The user has mature concepts and only needs to choose between them.
* The task is final copywriting.
* The task is detailed information architecture for a complex application.
* The task is UI component design.
* The task is final layout composition.
* The task is a design-system specification.
* The task is implementation or code.
* The interface is primarily a utility or operational tool where narrative framing would add unnecessary friction.

If the project is not sufficiently understood, run a problem-framing workflow first.

---

# Inputs to inspect

Inspect as many of the following as are available.

## Strategic material

* Business problem
* Project brief
* Business goals
* Audience
* Jobs to be done
* User needs
* Desired actions
* Positioning
* Value proposition
* Differentiators
* Competitive context
* Constraints

## Transformation evidence

* Customer outcomes
* Before-and-after states
* Problems solved
* Time saved
* Risk reduced
* Skills gained
* Experience improved
* Emotional outcomes
* Operational improvements
* Social or cultural impact

## Story material

* Founder story
* Company origin
* Customer stories
* Testimonials
* Case studies
* Product-in-use examples
* Behind-the-scenes material
* Manufacturing or service process
* Historical milestones
* Mission
* Research
* Data
* Results
* Product creation

## Brand material

* Brand strategy
* Tone of voice
* Existing messaging
* Campaign language
* Naming
* Terminology
* Existing visual identity
* Photography
* Archive material

## Content material

* Existing page copy
* Sitemap
* Section inventory
* Product descriptions
* Services
* FAQs
* Reviews
* Statistics
* Calls to action

## Upstream design research

When available, inspect output from:

* `design-problem-framer`
* `graphic-universe-builder`

Useful graphic-universe inputs include:

* project vocabulary
* research clusters
* project-owned opportunities
* visual atoms
* metaphor candidates
* candidate graphic universes
* category clichés

Do not require graphic-universe research if the project already contains strong conceptual material.

---

# Preconditions

Before concept generation, determine whether these questions can be answered:

```txt
What does the organization offer?

Who is the primary audience?

What does that audience need, want, fear, or struggle with?

What meaningful change does the offer create?

Why should this organization be believed?

What should the visitor understand?

What should the visitor feel, if emotion is relevant?

What should the visitor do?

What makes this project different from obvious alternatives?
```

If several answers are unknown, mark them as open questions.

Do not invent strategic facts to make a concept feel complete.

---

# Workflow

## 1. Restate the design problem

Condense the brief into a concept-ready statement.

Use:

```txt
The website needs to help <audience>
understand/believe/experience <meaning>
so they can <desired action or outcome>,
while overcoming <key barrier>.
```

Example structure:

```txt
The website needs to help technical buyers understand that the company
does more than manufacture components: it controls the complete process
from raw material to finished precision part, so buyers trust it with
high-risk production work.
```

Do not begin concepting until the problem can be expressed clearly.

---

## 2. Define the essential meaning

Ask:

> If the visitor remembers only one idea from this experience, what should it be?

Write one sentence.

This is not:

* a slogan
* a headline
* a list of features
* a visual style

It is the meaning the concept must communicate.

Example:

```txt
This company turns an unpredictable industrial process into something
precise, visible, and dependable.
```

Test the statement:

* Is it meaningful to the audience?
* Is it relevant to the business?
* Is it more specific than "we are innovative"?
* Can available evidence support it?
* Could it guide content decisions?

---

## 3. Define the audience transformation

Describe the desired shift.

Use:

```txt
Before:
The visitor thinks/feels/believes...

After:
The visitor thinks/feels/believes...

Action:
The visitor is now prepared to...
```

Possible transformations include:

```txt
uncertain → confident
unaware → informed
skeptical → convinced
overwhelmed → clear
curious → invested
detached → emotionally connected
problem-aware → solution-aware
feature-focused → outcome-focused
generic perception → distinctive perception
```

Do not manufacture emotional transformation where a practical change in understanding is sufficient.

---

## 4. Build the evidence inventory

Separate available story material from assumptions.

Use:

| Evidence | Type                                                    | What it proves | Strength             |
| -------- | ------------------------------------------------------- | -------------- | -------------------- |
| ...      | customer / founder / process / data / product / history | ...            | high / medium / weak |

Classify material as:

### Verified

Directly supported by provided material.

### Inferred

A plausible interpretation that still needs validation.

### Missing

Useful evidence that does not currently exist.

A concept should not depend on invented testimonials, fabricated history, hypothetical customer outcomes presented as fact, or nonexistent production material.

---

## 5. Identify possible narrative lenses

Evaluate which lens naturally exposes the project's meaning.

Possible lenses include:

### Transformation

Show the meaningful change created for the customer.

```txt
before
→ intervention
→ after
```

Best when outcome is the strongest differentiator.

### Product in use

Show the offer through real situations rather than isolated features.

```txt
context
→ use
→ result
```

Best when seeing the product perform creates trust.

### Process

Expose how something is created, delivered, transformed, or solved.

```txt
input
→ stages
→ output
```

Best when process, craft, transparency, or expertise differentiates the organization.

### Founder or origin

Use why the organization exists as the organizing narrative.

```txt
frustration
→ decision
→ new approach
→ current mission
```

Best when the origin meaningfully explains the product or brand.

Do not use founder narrative simply because founder material exists.

### Customer story

Let a real customer's situation demonstrate relevance.

```txt
situation
→ problem
→ experience
→ outcome
```

Best when social proof and lived experience are stronger than product claims.

### Mission and impact

Structure the experience around the change the organization wants to produce.

```txt
current condition
→ challenge
→ intervention
→ evidence of impact
```

Useful for charities, cultural institutions, mission-driven organizations, and public-interest work.

### Contrast

Define the offer by exposing the weakness of the conventional alternative.

```txt
old assumption
→ contradiction
→ better model
```

Useful when the category has an entrenched default.

### Journey

Take the visitor through a meaningful sequence.

```txt
stage 1
→ stage 2
→ stage 3
→ destination
```

Useful when progression itself matters.

### System

Reveal how apparently separate pieces work together.

```txt
parts
→ relationships
→ system
→ outcome
```

Useful for platforms, infrastructure, complex services, and ecosystems.

### Investigation

Begin with a question and reveal the answer gradually.

```txt
question
→ evidence
→ discovery
→ conclusion
```

Useful for editorial, research, cultural, or explanatory experiences.

### Demonstration

Structure the website around proving a claim.

```txt
claim
→ demonstration
→ evidence
→ invitation
```

Useful when trust must be earned quickly.

Multiple lenses may coexist, but each concept should have one dominant narrative mechanism.

---

## 6. Choose the appropriate story intensity

Not every project should become an immersive narrative experience.

Classify candidate concepts as:

### Light narrative

Narrative primarily affects:

* message order
* section progression
* headings
* proof placement

The interface remains conventional and efficient.

Good for:

* SaaS
* professional services
* B2B
* product pages
* conversion-focused sites

### Integrated narrative

Narrative influences:

* page progression
* content rhythm
* imagery
* repeated language
* selected interactions
* section transitions

Good for:

* brand sites
* portfolios
* launches
* differentiated service companies
* editorial commerce

### Immersive narrative

The experience itself behaves like a story.

Narrative may influence:

* scroll progression
* media sequencing
* scene changes
* interaction
* chapter structure
* rich motion

Good for:

* campaigns
* cultural experiences
* product launches
* storytelling projects
* experiential brand sites

Immersion should only be proposed when:

* the content supports it
* the value justifies it
* the production budget can plausibly support it
* the narrative remains understandable without requiring fragile interaction

---

## 7. Generate verbal territories before visual territories

Start concept exploration with language.

Generate words and phrases connected to:

* transformation
* customer language
* project vocabulary
* process
* objects
* domain terminology
* contrasts
* outcomes
* cultural associations
* graphic-universe findings

Possible ideation methods include:

### Phrase combinations

Combine project language in unexpected but defensible ways.

### Idioms

Explore relevant idioms as sparks.

Do not force idioms into final concepts.

Reject those that are:

* clichéd
* confusing
* culturally inappropriate
* too clever
* unrelated to the actual business

### Domain language

Reinterpret terminology already used by the audience.

### Double meanings

Explore words with both functional and emotional meanings.

### Contrast statements

Examples:

```txt
Not X. Y.
From X to Y.
Beyond X.
What if X were Y?
```

### Transformation language

Use verbs describing movement or change.

### Questions

Use a meaningful unresolved question to create tension.

### Project-owned phrases

Prefer terminology or language competitors cannot easily claim.

Do not write final website copy in this stage.

The purpose is concept generation.

---

## 8. Diverge before converging

Generate several rough concepts before refining any single one.

Aim for approximately:

```txt
4–7 rough ideas
```

when the brief is broad enough.

The exact number is not important.

The purpose is to avoid overcommitting to the first plausible idea.

A rough concept needs only:

```txt
Working title:
Essential idea:
Narrative lens:
Audience transformation:
Why it might work:
```

Do not polish typography, layouts, or headlines while divergence is still needed.

---

## 9. Reject weak concept types

Reject concepts that are merely visual styles.

These are not sufficient concepts:

```txt
Brutalist
Swiss
Minimal
Luxury
Editorial
Dark mode
Y2K
Retro-futurist
Neo-brutalism
Bento
Cinematic
```

They may later become visual characteristics.

A concept needs meaning and narrative logic.

Also reject concepts that amount to:

```txt
Use lots of animation.
Make it immersive.
Use large typography.
Make it look premium.
Use unexpected layouts.
Make it emotional.
```

Those are execution directions, not central ideas.

---

## 10. Filter to the strongest 2–3 concepts

Evaluate the rough concepts against:

| Criterion                | Question                                                          |
| ------------------------ | ----------------------------------------------------------------- |
| Business relevance       | Does it solve the actual communication problem?                   |
| Audience relevance       | Does it matter to the intended visitor?                           |
| Evidence                 | Can real content support it?                                      |
| Specificity              | Does it belong to this project?                                   |
| Narrative strength       | Does it create a meaningful progression?                          |
| Distinctiveness          | Is it more than a category default?                               |
| Extensibility            | Can it survive beyond the hero?                                   |
| Clarity                  | Can the idea be explained simply?                                 |
| Conversion support       | Does it lead naturally toward action?                             |
| Production realism       | Can the organization plausibly make it?                           |
| Accessibility resilience | Can the concept survive without inaccessible presentation tricks? |

Keep only directions with meaningful differences.

Two strong concepts are better than three where the third is filler.

---

# Build each concept

## 11. Create a concept title

Give each concept a short working title.

Usually aim for:

```txt
3–6 words
```

when possible.

The title should capture the conceptual premise.

It does not have to become the final hero headline.

Avoid:

```txt
Concept 1
Modern Future
Bold Direction
Premium Experience
```

Prefer titles that reveal an idea.

---

## 12. Write the concept thesis

Explain the concept in one short paragraph.

Use:

```txt
This concept presents <brand/product> as <central meaning>
by taking the visitor through <narrative mechanism>.
Rather than focusing primarily on <category default>,
the experience emphasizes <distinctive evidence or transformation>.
```

A stakeholder should understand the concept without seeing a mockup.

---

## 13. Define the central tension

Strong narratives usually contain some form of tension.

This does not need to be dramatic.

Possible tensions include:

```txt
complexity vs clarity
raw vs refined
uncertainty vs control
speed vs care
old model vs new model
distance vs connection
individual parts vs unified system
risk vs confidence
hidden process vs transparency
generic category vs specific human experience
```

Write:

```txt
The concept is driven by the tension between <A> and <B>.
```

Then explain why that tension matters to the audience.

Do not invent conflict purely for drama.

---

## 14. Define the story spine

Describe how understanding develops.

Use approximately 4–6 beats.

Example:

```txt
1. Opening — establish the central promise or tension.
2. Context — show why the problem matters.
3. Transformation — reveal the new possibility.
4. Evidence — prove the promise using real material.
5. Resolution — make the resulting value clear.
6. Action — provide the appropriate next step.
```

Adapt the structure to the concept.

Alternative:

```txt
1. Raw material
2. Transformation process
3. Precision result
4. Real application
5. Trust evidence
6. Start a project
```

Do not force every concept into the same narrative template.

---

## 15. Map the concept through the page

For each major section describe:

| Section | Narrative role | Visitor question | Content/evidence | Concept behavior |
| ------- | -------------- | ---------------- | ---------------- | ---------------- |

Example questions:

```txt
Why should I care?
What is different here?
How does this work?
Can I trust this?
Is this for me?
What should I do next?
```

Sections should exist because the narrative or user decision requires them.

Avoid defaulting automatically to:

```txt
Hero
Features
About
Testimonials
FAQ
CTA
```

Those modules may still be correct, but their role should be explained.

---

## 16. Connect features to meaning

Features remain important.

Do not remove useful product information in the name of storytelling.

For each important feature, ask:

```txt
What does this enable?

Why does that matter?

What evidence demonstrates the claim?

Where does it belong in the narrative?
```

Use:

```txt
feature
→ capability
→ user consequence
→ evidence
```

Example:

```txt
Real-time synchronization
→ everyone sees current information
→ fewer handoff mistakes
→ operational metrics or workflow demonstration
```

This keeps the concept commercially useful rather than merely expressive.

---

## 17. Define the evidence plan

For each narrative claim, identify what should prove it.

Possible evidence:

* Customer quote
* Case study
* Statistic
* Product demonstration
* Process photography
* Founder material
* Technical specification
* Before-and-after comparison
* Timeline
* Certification
* Result
* Real interface
* Documentary media
* Product-in-context imagery

Use:

| Claim | Evidence needed | Available? | Dependency |
| ----- | --------------- | ---------: | ---------- |

Flag concepts that depend heavily on content the organization does not have.

---

## 18. Define voice behavior

Describe the verbal character of the concept without writing the final copy.

Cover:

```txt
Voice:
Sentence behavior:
Headline behavior:
Terminology:
CTA behavior:
Microcopy behavior:
Humor:
Emotional intensity:
```

Examples:

```txt
precise and restrained
direct and conversational
curious and investigative
warm without sentimentality
confident without hype
technical but legible
playful without becoming flippant
```

Also specify what the voice should avoid.

Example:

```txt
Avoid startup superlatives, fake urgency, and vague transformation claims.
```

---

## 19. Connect the graphic universe

If `graphic-universe-builder` output exists, map relevant findings into the concept.

Use:

| Graphic-universe signal | Narrative relevance | Possible conceptual use |
| ----------------------- | ------------------- | ----------------------- |

Select only signals that strengthen the concept.

Do not force every visual atom into the website.

A visual metaphor should reinforce an existing narrative idea, not create one retroactively.

---

## 20. Describe visual implications

Describe what the concept implies for later design work.

Cover:

### Imagery

What kind of imagery would best tell this story?

Examples:

* process documentation
* product in use
* archival material
* portraits
* extreme detail
* environmental photography
* diagrams
* illustration

### Typography

What should typography express?

Examples:

```txt
authority
urgency
intimacy
precision
editorial depth
playfulness
technical character
```

Do not prescribe exact fonts unless explicitly requested.

### Composition

What kinds of relationships should layout emphasize?

Examples:

```txt
contrast
sequence
scale
before/after
parallel perspectives
progression
density changes
reveals
```

Do not create the grid yet.

### Motion

What conceptual role could motion serve?

Examples:

```txt
transformation
assembly
progression
focus
connection
cause-and-effect
```

Do not specify detailed timelines or animation code.

### Interaction

Where could interaction reveal meaning or evidence?

Examples:

```txt
compare states
explore stages
inspect details
navigate chapters
reveal proof
```

Interaction must remain optional unless it is genuinely required for the task.

---

## 21. Define the conversion path

Storytelling must not obscure the reason the website exists.

For each concept identify:

```txt
Primary user action:
Secondary action:
When the first meaningful CTA appears:
What the visitor should understand before it:
What evidence should precede higher-commitment actions:
```

The narrative should reduce uncertainty before asking for commitment.

Do not postpone the primary action merely to preserve a theatrical story sequence.

Users who already understand the offer should be able to act without consuming the entire narrative.

---

## 22. Test navigation independence

The concept must survive non-linear browsing.

Ask:

* Does the homepage still make sense if the visitor enters halfway down?
* Can users navigate directly to product, pricing, services, or contact pages?
* Does the concept require everyone to consume content in one exact order?
* Can important information be accessed directly?
* Does skipping an interaction destroy comprehension?

A narrative website is still a website.

Do not convert basic navigation into a puzzle.

---

## 23. Define responsive conceptual behavior

Do not design breakpoints.

Instead ask what must remain true across screen sizes.

For example:

```txt
The process sequence must remain understandable.
The contrast between old and new must remain explicit.
The two perspectives must remain distinguishable.
The visual metaphor must not be required to understand the copy.
The CTA must remain available without completing the full story.
```

The concept should adapt, not collapse, on smaller screens.

---

## 24. Evaluate production dependencies

For every concept, identify dependencies such as:

* Custom photography
* Documentary video
* Customer participation
* Archive access
* Illustration
* 3D
* Motion design
* Development complexity
* Data
* Copywriting
* Translation
* Product integration

Classify:

```txt
essential
helpful
optional
```

If an expensive asset is essential, state it.

Do not disguise production requirements as design details.

---

## 25. Run the "beyond the hero" test

Ask:

> If the hero treatment disappeared, would the concept still exist?

A strong concept should influence several of:

* message hierarchy
* section progression
* evidence
* imagery
* voice
* CTA language
* interaction
* page relationships
* motion principles

Reject concepts that are really only hero ideas.

---

## 26. Run the substitution test

Ask:

> Could the company name be replaced with a competitor and the concept still work unchanged?

If yes, increase project specificity.

Return to:

* customer transformation
* process
* history
* project language
* evidence
* graphic-universe findings
* distinctive business model
* product behavior

---

## 27. Run the evidence test

Ask:

```txt
Which claims are facts?
Which claims are interpretations?
Which claims are aspirations?
Which claims still need evidence?
```

Never turn marketing ambition into fabricated proof.

---

## 28. Run the clarity test

A concept fails when explaining it requires several paragraphs of abstract language.

The central idea should be explainable approximately as:

```txt
The website tells <this story>
because the audience needs to understand <this meaning>.
```

Complex execution may follow a simple concept.

Prefer conceptual clarity over cleverness.

---

## 29. Run the restraint test

Do not make every element participate aggressively in the concept.

Separate:

### Core narrative devices

Essential to understanding the concept.

### Supporting devices

Strengthen it when appropriate.

### Optional expressive devices

Can increase personality without carrying critical meaning.

This prevents the website from becoming a theme park built around one metaphor.

---

# Concept differentiation

When presenting multiple concepts, explicitly compare them.

Use:

| Dimension                   | Concept A | Concept B | Concept C |
| --------------------------- | --------- | --------- | --------- |
| Essential meaning           |           |           |           |
| Narrative lens              |           |           |           |
| Story intensity             |           |           |           |
| Emotional character         |           |           |           |
| Main evidence               |           |           |           |
| Graphic-universe connection |           |           |           |
| Interaction role            |           |           |           |
| Conversion strategy         |           |           |           |
| Production complexity       |           |           |           |
| Main risk                   |           |           |           |

If the concepts differ only in typography, color, or mood, they are not separate concepts.

---

# Output format

Return:

## Concept Brief

```md
Project:
Primary audience:
Business objective:
User action:
Core barrier:
Essential meaning:
Audience transformation:
Available evidence:
Important constraints:
```

## Narrative Opportunities

| Lens | Why it fits | Evidence available | Potential |
| ---- | ----------- | ------------------ | --------- |

## Rejected or Weak Territories

List obvious, generic, unsupported, or misleading ideas that should not proceed.

---

## Concept A — `<working title>`

```md
### Concept thesis

...

### Essential meaning

...

### Audience transformation

Before:
After:
Action:

### Narrative lens

...

### Central tension

...

### Story intensity

Light / Integrated / Immersive

### Story spine

1. ...
2. ...
3. ...
4. ...
5. ...

### Section narrative

| Section | Narrative role | Visitor question | Evidence/content | Concept behavior |
|---|---|---|---|---|

### Feature-to-meaning mapping

| Feature or capability | User consequence | Evidence | Narrative role |
|---|---|---|---|

### Evidence plan

| Claim | Evidence | Available? | Dependency |
|---|---|---:|---|

### Voice direction

Voice:
Headline behavior:
CTA behavior:
Microcopy behavior:
Avoid:

### Graphic-universe connection

...

### Visual implications

Imagery:
Typography:
Composition:
Motion:
Interaction:

### Conversion path

...

### Production dependencies

Essential:
Helpful:
Optional:

### Why this belongs to the project

...

### Risks

...
```

---

## Concept B — `<working title>`

Use the same structure.

---

## Concept C — `<working title>`

Use the same structure only when a third strong concept exists.

Do not manufacture a third concept for symmetry.

---

## Concept Comparison

| Criterion                | Concept A | Concept B | Concept C |
| ------------------------ | --------: | --------: | --------: |
| Business alignment       |           |           |           |
| Audience relevance       |           |           |           |
| Evidence strength        |           |           |           |
| Distinctiveness          |           |           |           |
| Narrative strength       |           |           |           |
| Extensibility            |           |           |           |
| Conversion support       |           |           |           |
| Production feasibility   |           |           |           |
| Accessibility resilience |           |           |           |

Use qualitative assessments such as:

```txt
strong
medium
weak
```

unless the user explicitly requests numerical scoring.

---

## Handoff

Finish with:

```md
Concepts ready for design-direction evaluation:
Most important evidence gaps:
Content that needs commissioning:
Graphic-universe signals worth carrying forward:
Concept assumptions requiring validation:
Recommended next skill:
```

Do not automatically choose the winner unless the user explicitly asks this skill to recommend one.

When multiple concepts are mature, prefer handing them to `design-direction-decision`.

---

# Evidence discipline

Clearly distinguish:

### Known

Supported directly by supplied project material.

### Inferred

A reasonable interpretation.

### Proposed

A creative idea generated by this workflow.

### Needed

Information or content required before the concept can be executed confidently.

Example:

```txt
Known:
Customers currently submit reports manually.

Inferred:
The manual process creates uncertainty and delay.

Proposed:
Frame the experience around moving from fragmented reporting to one
continuous operational record.

Needed:
Validated customer evidence describing the actual reporting pain.
```

Do not blur these categories.

---

# Writing guardrail

This is a concept-development skill, not the final copywriting stage.

It may create:

* working concept titles
* sample phrases
* message territories
* headline behavior
* CTA behavior
* illustrative microcopy fragments

It should not produce a complete polished page unless the user explicitly requests a separate copywriting task.

Do not spend concept-development time polishing sentences that may disappear after concept selection.

---

# Art-direction guardrail

The skill may describe conceptual implications for:

* imagery
* typography
* composition
* motion
* interaction

It must not define:

* exact font families
* exact font scales
* final color values
* detailed grids
* exact component layouts
* animation timelines
* responsive breakpoints
* design tokens
* CSS
* JavaScript

Those belong downstream.

---

# Storytelling guardrails

Do not:

* invent customer stories
* fabricate founder motivations
* exaggerate outcomes
* create false urgency
* manufacture emotional trauma
* hide basic information for dramatic effect
* force visitors through mandatory narrative sequences
* turn every product into a hero's journey
* confuse sentimentality with emotional relevance
* use storytelling to avoid explaining the actual offer
* assume emotion always matters more than clarity
* replace proof with atmosphere
* propose immersive execution without acknowledging its production cost

The story must serve understanding.

---

# Accessibility and usability guardrail

Creative direction must remain compatible with:

* understandable reading order
* keyboard access
* reduced-motion alternatives
* legible typography
* sufficient contrast
* clear navigation
* direct access to important actions
* comprehension without animation
* meaningful alternative text and media equivalents
* responsive layouts

A narrative device should not require:

```txt
hover-only discovery
scroll-jacking
precision pointer movement
audio
motion
visual effects
```

for the user to understand essential information.

Flag concepts where accessibility constraints materially affect execution.

Do not reject expressive concepts automatically when an accessible implementation is plausible.

---

# Quality bar

The task is complete only when:

* The concept begins from an understood business and audience problem.
* One essential meaning has been identified.
* The intended audience transformation is explicit.
* Real evidence has been separated from assumptions.
* Several narrative lenses were considered before choosing directions.
* Divergent ideas were explored before convergence.
* Final candidate concepts differ in meaning or narrative mechanism, not merely aesthetics.
* Each concept has a clear thesis.
* Each concept has a coherent story spine.
* Each concept maps meaning through multiple sections rather than only the hero.
* Important features are connected to user consequences rather than discarded.
* Claims identify appropriate supporting evidence.
* Voice direction supports the concept without becoming final copywriting.
* Graphic-universe findings are used selectively and meaningfully when available.
* Visual implications remain directional rather than becoming detailed design specifications.
* The primary user action remains accessible.
* The narrative does not depend on consuming the entire website linearly.
* Mobile and reduced-motion conditions do not destroy comprehension.
* Production dependencies are explicit.
* Unsupported stories or claims are not invented.
* Generic visual-style labels are not presented as concepts.
* The concepts survive the beyond-the-hero test.
* The concepts survive the substitution test.
* The output is ready for a design-direction decision workflow.

---

# Edge cases

## No customer stories exist

Do not invent them.

Consider:

* process
* product-in-use
* demonstration
* data
* founder origin
* contrast
* system
* transformation based on verified product behavior

Mark customer-story content as a future opportunity only.

---

## No founder story is relevant

Ignore it.

A founder story is useful only when it explains:

* why the organization exists
* why its approach differs
* why the visitor should care

Do not turn ordinary company chronology into forced storytelling.

---

## Technical B2B product

Do not remove technical detail.

Use narrative to create context for the detail.

Possible structure:

```txt
operational problem
→ technical challenge
→ system behavior
→ measurable outcome
→ technical evidence
```

Technical credibility may be the emotional reassurance the audience needs.

---

## SaaS product

Avoid automatically turning the homepage into:

```txt
hero
→ logo cloud
→ feature cards
→ integrations
→ testimonial
→ pricing
```

Ask whether a stronger progression exists.

Possible lenses:

* fragmented workflow → unified workflow
* repeated problem → automated resolution
* invisible complexity → controlled system
* reactive work → proactive insight

Still preserve direct product explanation and early CTAs.

---

## Ecommerce

Do not let narrative interfere with shopping.

Story may support:

* product context
* craftsmanship
* provenance
* performance
* identity
* customer use

Keep:

* product discovery
* pricing
* availability
* purchasing actions

direct and recognizable.

---

## Portfolio

Possible narrative lenses include:

* way of thinking
* recurring creative problem
* transformation across projects
* practice evolution
* selected point of view

Do not make the visitor solve an elaborate interaction before they can see the work.

---

## Cultural or editorial website

Narrative may be more expressive.

Consider:

* chronology
* multiple voices
* investigation
* juxtaposition
* thematic chapters
* contrasting perspectives

Still preserve semantic structure and direct navigation.

---

## Charity or impact project

Avoid emotional manipulation.

Connect:

```txt
human reality
→ systemic issue
→ intervention
→ evidence
→ action
```

Use dignity, specificity, and verified impact.

---

## Very little content exists

Do not design a concept whose success depends on a large documentary content library.

Prefer a lighter narrative based on:

* language
* product behavior
* process
* existing evidence

List content worth commissioning later.

---

## Existing visual direction already exists

Do not replace it automatically.

Ask how the visual direction can reinforce the narrative.

If the existing visual direction conflicts with the strongest concept, flag the contradiction for later `design-direction-decision`.

---

## One concept is clearly stronger

Still avoid pretending weaker alternatives are equally strong.

If the user requested exploration:

* present the strongest concept
* present genuinely plausible alternatives
* explain weaknesses transparently

Do not manufacture false balance.

---

# Related skills

Use before this skill when available:

* `design-problem-framer` — clarifies the business problem, audience, constraints, transformation, and communication goal.
* `graphic-universe-builder` — discovers project-specific visual research territories, patterns, metaphors, and graphic-universe candidates.

Use after this skill when available:

* `design-direction-decision` — compares mature concept directions and recommends which should proceed.
* `brand-derived-visual-system` *(proposed)* — converts the selected concept and project material into a reusable visual grammar.
* `expressive-grid-planner` *(proposed)* — explores content-driven layout structures after the concept is chosen.
* `art-direction-coherence-review` *(proposed)* — checks whether the executed experience communicates the intended meaning consistently.
* `layout-principles-review` — evaluates hierarchy, proportion, rhythm, alignment, balance, and composition.

Do not duplicate those downstream workflows here.

The story-led-website-concept skill should end when the project has a small set of clear, evidence-supported, extensible creative concepts ready to evaluate.

This keeps the skill compatible with the repository convention that each skill has one reusable job, explicit triggers and outputs, and a canonical `skills/<category>/<skill-name>/SKILL.md` source path.

