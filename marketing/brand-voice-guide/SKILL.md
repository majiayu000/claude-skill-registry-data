---
name: brand-voice-guide
description: "Define brand voice standards — tone, vocabulary, style rules for aligning content teams."
version: 0.1.0
---


## JTBD (Jobs To Be Done)

### Primary Job
When multiple people or assets need to sound like the same brand,
I want a clear brand voice standard,
so I can create and review content without re-arguing tone every time.

### Secondary Jobs
- When content feels inconsistent across channels, I want shared tone boundaries, so I can make decisions faster.
- When briefing writers or reviewers, I want explicit vocabulary and audience guidance, so the work stays aligned as it scales.

### Job Layers
- Functional: Define reusable voice, tone, audience, and vocabulary rules that other content work can follow.
- Emotional: Reduce the frustration of subjective brand debates and last-minute rewrites.
- Social: Helps writers, reviewers, and stakeholders operate from the same standard instead of personal taste.

### This Skill Is For
- A user standardizing the voice for a content program or set of brand-facing assets.
- A user preparing inputs that other planning and review skills should follow.
- A team that needs one shared reference instead of repeated tone debates.

### This Skill Is NOT For
- A user who needs a concrete content plan for a specific asset; use `copy-planner` instead.
- A user who already has drafted content and mainly needs critique; use `copy-critic` instead.

### Paired With
- `copy-planner`: Use this after the voice standard is clear to turn it into a concrete brief or asset plan.
- `copy-critic`: Use this after content is drafted to audit whether it stays inside the agreed voice rules.

### Resolution Paths
| User's Situation | What Happens | What They Leave With |
|-----------------|-------------|----------------------|
| Has no shared tone standard | The skill defines voice boundaries and examples | A reusable brand voice reference |
| Has multiple writers or channels | The skill aligns vocabulary and audience expectations | A common standard for future work |
| Has recurring feedback about inconsistency | The skill makes subjective brand expectations explicit | Fewer avoidable rewrites |

### When to Escalate
- If the next job is building a specific asset plan, escalate to `copy-planner`.
- If the next job is judging drafted content against the standard, escalate to `copy-critic`.

<Purpose>
Brand Voice Guide is a reference template — not a reviewer, not a planner. It codifies a client's brand voice guidelines in structured form so that copy-critic and copy-planner can enforce consistency across copy.

Other skills invoke this to answer: "Is this copy on-brand?" or "Does this match our voice?"

The guide contains:
- Brand personality (adjectives + definitions specific to the client)
- Tone spectrum (formal ↔ casual, technical ↔ accessible)
- Vocabulary (preferred terms, banned terms, jargon policy)
- Voice examples (good vs bad for web copy, email, social, technical docs)
- Audience definitions (who we're talking to, in priority order)
- Message hierarchy (what matters most, what's secondary)
- Reading level target (Flesch-Kincaid grade level or equivalent)

Users customize this template per-client and save it to their project. Copy-critic and copy-planner reference it automatically.
</Purpose>

<Use_When>
- You are starting a new client engagement and need to document their brand voice
- You are creating a style guide for a team or organization
- You need a shared reference for copy review (pass to copy-critic)
- You need a shared reference for copy planning (pass to copy-planner)
- Copy-critic or copy-planner ask you to provide a brand voice guide
- You want to enforce consistency across marketing, product, and technical documentation
</Use_When>

<Do_Not_Use_When>
- You want to review existing copy against a brand voice — use copy-critic instead
- You want to plan new copy following a brand voice — use copy-planner instead
- You just want general writing advice without client-specific guidelines
- You don't yet have enough context about the client's voice to define it
</Do_Not_Use_When>

<Template>

# Brand Voice Guide: [CLIENT NAME]

**Created:** [DATE]
**Owner:** [YOUR NAME]
**Last Updated:** [DATE]

---

## Brand Personality

3-5 core traits defining how your brand communicates.

| Trait | Definition | Example |
|-------|-----------|---------|
| [e.g., "Trustworthy"] | [How it shows in copy] | [Concrete example] |
| | | |

---

## Tone Spectrum

Where your brand sits on key dimensions (guides context-specific choices).

- **Formal ↔ Casual:** (e.g., "Casual for social, formal for legal docs")
- **Technical ↔ Accessible:** (e.g., "Explain jargon to SMB, assume expertise for engineers")
- **Authoritative ↔ Conversational:** (e.g., "Authoritative on features, conversational on culture")
- **Optimistic ↔ Pragmatic:** (e.g., "Pragmatic challenges, optimistic solutions")

---

## Vocabulary

### Preferred Terms
Terms that signal our voice. Use these consistently.

| Term | Context | Why This | Don't Use |
|------|---------|---------|----------|
| [e.g., "help you build"] | Product benefits | Shows agency and partnership | "enable your ability to" |
| | | | |

### Banned Terms
Words/phrases that contradict our voice. Never use.

- [e.g., "enterprise-grade" — too corporate]
- [e.g., "synergy" — jargon-y and vague]
- [e.g., "click here" — generic, accessibility problem]

### Jargon Policy
- **Define on first use:** [Yes / No / Context-dependent]
- **Format:** [Parenthetical / Glossary link / Explainer section]
- **Acronyms:** [Spell out first mention, then acronym]

---

## Voice Examples

Show GOOD + BAD for each context. Copy-critic uses these as standards.

### Web Copy
**GOOD:** [On-brand example] **Why:** [Voice choices]
**BAD:** [Off-brand example] **Why:** [Violations]

### Email
**GOOD:** [On-brand example] **Why:** [Voice choices]
**BAD:** [Off-brand example] **Why:** [Violations]

### Social Media
**GOOD:** [On-brand example] **Why:** [Voice choices]
**BAD:** [Off-brand example] **Why:** [Violations]

### Technical Docs
**GOOD:** [On-brand example] **Why:** [Voice choices]
**BAD:** [Off-brand example] **Why:** [Violations]

---

## Audience Definitions

### Primary
- **Who:** [e.g., "Mid-market product managers, 3-10 years experience"]
- **Care about:** [e.g., "Speed to value, team adoption"]
- **How we talk to them:** [e.g., "Practical, outcome-focused, no hype"]

### Secondary (optional)
- **Who:** [e.g., "Engineering leads"]
- **Care about:** [e.g., "Technical soundness, scalability"]
- **How we talk to them:** [e.g., "Technical depth, implementation details"]

### Tertiary (if applicable)
- **Who:** [e.g., "Executives"]
- **Care about:** [e.g., "ROI, risk mitigation"]
- **How we talk to them:** [e.g., "Business impact, minimal jargon"]

---

## Message Hierarchy

Rank by importance (shapes emphasis and word choice).

1. **[Top message]** — [Why it comes first]
2. **[Secondary]** — [Why it matters]
3. **[Tertiary]** — [Supporting point]
4. **[Nice-to-have]** — [Context-dependent]

---

## Reading Level Target

- **Target:** [e.g., "8th grade for web, college-level for technical docs"]
- **Why:** [e.g., "Wide accessibility, professional tone"]
- **How:** [e.g., "15-20 word sentences, 90% common words, short paragraphs, active voice"]

---

## How to Use This Guide

### For Copy-Critic
When asked to review copy:
1. Check copy against the Brand Personality traits
2. Verify it matches the Tone Spectrum for its context
3. Confirm Vocabulary is followed (preferred terms used, banned terms absent)
4. Compare against Voice Examples (GOOD vs BAD)
5. Confirm it addresses the relevant Audience
6. Validate Reading Level

### For Copy-Planner
When asked to plan copy:
1. Start with the relevant Audience definition
2. Shape outline around Message Hierarchy
3. Draft in Tone Spectrum that matches context
4. Use Preferred Terms consistently
5. Write at target Reading Level
6. Reference Voice Examples as style inspiration

### For Writers
When creating copy:
1. Review the Brand Personality traits before starting
2. Check which Audience you're writing for
3. Find the Voice Example for your context
4. Write, then verify against the Tone Spectrum
5. Search for Banned Terms and replace
6. Verify Reading Level (use online tool: Flesch-Kincaid calculator)

---

</Template>

<Example>

# Brand Voice Guide: HealthFirst Coalition

**Created:** 2025-09-15
**Owner:** Sarah Chen
**Last Updated:** 2025-09-15

---

## Brand Personality

| Trait | Definition | Example |
|-------|-----------|---------|
| Empathetic | Acknowledge real struggles, never shame. | "Hard AND doable" not "Just try harder" |
| Clear-headed | Evidence-based, no fearmongering, no false hope. | "73% of participants" not "cure" |
| Practical | Actionable today, not distant ideals. | "This week" not "Perfect health in 30 days" |
| Collaborative | Partner with reader, not lecture from above. | "Let's explore" not "You must" |

---

## Tone Spectrum

- **Formal ↔ Casual:** Conversational on web/social, professional on clinical resources. Never cold or distant.
- **Technical ↔ Accessible:** Always explain medical terms on first mention. Assume no background unless healthcare provider.
- **Authoritative ↔ Conversational:** Authoritative on facts (cite sources), conversational otherwise.
- **Optimistic ↔ Pragmatic:** Pragmatic about challenges, optimistic about wins. "Hard AND worth it."

---

## Vocabulary

### Preferred Terms
| Term | Context | Why This | Don't Use |
|------|---------|---------|----------|
| "manage" or "live well with" | Chronic conditions | Empowering, realistic | "suffer from," "victim of" |
| "support" | Relationships and resources | Collaborative language | "allow," "permit" |
| "evidence shows" | Clinical claims | Grounds us in research | "doctors say," "studies prove" |
| "your provider" | Healthcare professionals | Respectful, inclusive | "your doctor" (not all patients have one) |

### Banned Terms
- "cure" (unless literally a cure exists with 100% evidence)
- "everyone should" (too prescriptive, ignores individual variation)
- "just" (dismissive: "just exercise more")
- "naturally" or "organic" (vague, often implies unregulated products)
- "breakthrough" (hype, breaks trust)

### Jargon Policy
- **Define on first use:** Yes, in parenthetical format
- **Example:** "Hypertension (high blood pressure) affects one in three adults"
- **No separate glossary:** Keep definitions inline so readers understand without switching tabs

---

## Voice Examples

### Context: Web Copy (Homepage, Landing Pages)

**GOOD**
> Diabetes changes how you eat, exercise, and sleep. We help you manage it without letting it manage you. Our community of 50,000+ members shares what actually works — not perfect-world advice, but real strategies for real life.

Why this works: Empathetic (acknowledges real impact), practical (mention community and strategies), collaborative (we help YOU), clear-headed (realistic tone), avoids shame.

**BAD**
> Don't let diabetes control your life! Our proven system will help you achieve perfect blood sugar in just 6 weeks. Join thousands of people who have already been cured.

Why this fails: Uses "cured" (false claim), "just" (dismissive), "perfect" (unrealistic), "proven system" (hype), ignores individual variation, shame-adjacent.

### Context: Email (Newsletter, Transactional, Nurture)

**GOOD**
> Hi Sarah — Three things that helped this week:
> 1. Sarah's tip: pre-dose your snacks so you're not eyeballing portions at 3pm
> 2. New: Interactive meal planner (works with what you actually eat)
> 3. Community: 47 members shared what helped them this week [See the thread]
>
> —HealthFirst

Why this works: Specific (Sarah's tip shows personalization), practical (actionable), collaborative (community voices), short paragraphs, clear action.

**BAD**
> Achieve optimal wellness through comprehensive lifestyle transformation. Our scientifically-designed program synergizes nutrition, movement, and mindfulness to maximize your health outcomes. Learn how thousands have already achieved transformational results.

Why this fails: Jargon-heavy ("synergizes," "optimal wellness"), overpromising ("transformational results"), no specific action, cold tone, hype language.

### Context: Social Media

**GOOD**
> What helped YOU this week?
>
> One member shared: "I stopped forcing myself to meal-prep like Instagram food bloggers. Now I do 20 min of prep on Sunday and grab pre-portioned stuff all week. WAY less stress."
>
> Drop your strategy below. ↓

Why this works: Invites participation, shows real example, normalizes non-perfect approaches, conversational, clear ask.

**BAD**
> Transform your life in 30 days with our proprietary wellness framework! 💪 Don't settle for mediocrity. Join the revolution. Link in bio.

Why this fails: Hype, unrealistic timeline, shame-based ("don't settle"), vague ("proprietary framework"), generic.

### Context: Technical Documentation

**GOOD**
> ### How to log your blood sugar readings
>
> The app syncs your readings from compatible devices (Dexcom, FreeStyle Libre) automatically every 5 minutes, or you can enter them manually.
>
> **To add a manual entry:**
> 1. Tap the glucose icon on your home screen
> 2. Enter your reading and the time you measured it
> 3. Optional: add notes (e.g., "before breakfast")
>
> Your readings are encrypted and stored securely. [Privacy policy]

Why this works: Clear steps, technical detail without jargon, acknowledges both automatic and manual, explains benefits (encrypted), accessible language.

**BAD**
> The glucometric input interface leverages bidirectional sync protocols compatible with class II medical devices. Configure your CGM endpoint via the settings manifest. Payload schema utilizes ISO 8601 timestamps.

Why this fails: Over-technical, assumes expertise, no user context, no step-by-step guidance, excludes non-technical users.

---

## Audience Definitions

### Primary
- **Who:** Adults (25-65) newly diagnosed or managing chronic conditions. Digital-native, seeking community.
- **Care about:** Live life without health consuming it. Real strategies, not shame.
- **How we talk to them:** "What worked for others AND how to know if it works for you."

### Secondary
- **Who:** Caregivers and family members.
- **Care about:** How to help without overstepping, normalize rather than isolate.
- **How we talk to them:** Collaborative, actionable, their role is hard too.

### Tertiary
- **Who:** Healthcare providers wanting to share resources.
- **Care about:** Evidence-based, patient-accessible, saves time explaining.
- **How we talk to them:** Professional, cite sources, complementary to clinical care.

---

## Message Hierarchy

1. **You're not alone AND it's possible** — Our core message.
2. **Real strategies from real people** — What differentiates us.
3. **Evidence matters, not hype** — Builds trust.
4. **We're here when you need us** — Community (CTAs and sign-offs).

---

## Reading Level Target

- **Target:** 8th-9th grade for web/email, 10th-11th grade for clinical resources
- **Why:** Wide accessibility + credibility.
- **How:** 15-18 word sentences, 2-4 sentence paragraphs, 90% common words, active voice ("You can" not "It is possible to"), bullet points for steps.

---

</Example>

<Steps>

1. **Gather:** Review website, marketing, past copy. Identify patterns.
2. **Interview:** "How describe your personality?" "What tone feels wrong?" "Who are you NOT?"
3. **Fill template:** Start Personality + Audience, they inform everything else.
4. **Collect examples:** 2-3 GOOD examples from existing copy, 2-3 BAD examples to avoid.
5. **Calibrate spectrum:** Place on formal-casual, technical-accessible, authoritative-conversational, optimistic-pragmatic.
6. **Define vocabulary:** Extract preferred terms, define banned terms.
7. **Save to project:** Store at `/docs/brand-voice-guide.md`, commit, reference in copy-critic/copy-planner.

</Steps>

<Integration>

### Copy-Critic Integration
```
copy-critic: "Can you provide your brand voice guide?"
You: "Path: /docs/brand-voice-guide.md"
copy-critic: "Checking against [Brand] personality: [Trait], [Trait], [Trait]..."
```

### Copy-Planner Integration
```
copy-planner: "What brand voice?"
You: "/docs/brand-voice-guide.md, primary audience: [audience name]"
copy-planner: "Using [Brand] personality + tone spectrum + hierarchy..."
```

### Maintenance
- Review quarterly (brand evolves)
- Update Vocabulary (new terms, banned phrases)
- Refresh Examples annually
- Add Audiences if expanding market

</Integration>

<Final_Checklist>
- [ ] Brand Personality defined with 3-5 traits + specific examples
- [ ] Tone Spectrum placed on all key dimensions (formal-casual, technical-accessible, etc.)
- [ ] Preferred Terms table has at least 5 entries
- [ ] Banned Terms list has at least 5 entries
- [ ] Jargon Policy clearly states yes/no/context-dependent
- [ ] Voice Examples include GOOD + BAD for all 4 contexts (web, email, social, technical docs)
- [ ] Each example explains WHY it works or fails
- [ ] Audience Definitions include primary, secondary, tertiary (if applicable)
- [ ] Each audience section includes: Who, What they care about, Pain points, How we talk to them
- [ ] Message Hierarchy ranked 1-4 (or more) with rationale
- [ ] Reading Level target specified with HOW you achieve it
- [ ] Template saved to project repo and linked in README or docs
</Final_Checklist>
