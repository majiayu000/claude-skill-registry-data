---
name: vibe-brainstorm
description: >
  Comprehensive brainstorming workflow for turning any app idea into a clear,
  validated, buildable brief. Two paths: personal project (8 steps) and
  client/business project (13 steps). Fast path for fully-formed ideas.
  Detects agentic/AI projects and routes to agent: before architect:.
  Pre-write quality check ensures BRIEF.md has specific users, measurable
  success criteria, explicit non-goals, and a clear v1 boundary before writing.
  Complexity sizing (S/M/L/XL) signals build effort to downstream skills.
  BRIEF.md is structurally consistent — architect:, new-app:, change-spec:,
  and review: all read known field names. Does not create code or project
  structure — thinking and brief only.
  Step 0 INGESTS an idea produced elsewhere (pasted text, or a dropped file —
  canonical BRIEF.md, an arbitrary idea doc, or an empty/sparse file) and
  normalizes it to a canonical BRIEF.md so it reaches parity and flows through
  the full downstream pipeline (architect → scaffold → design → build) instead
  of skipping steps.
  Triggers on "brainstorm:" prefix, "I have an idea", "I want to build",
  "help me think through", "I have a client project", "thinking about building",
  "I want to validate this idea", "let's plan a project", "I already have a
  brief", "here's my idea/spec from elsewhere", "I brainstormed this in another
  chat", "ingest this idea", "onboard this brief", "I dropped a file with my idea".
---

# Vibe Brainstorm Skill v2

Turns a fuzzy idea into a clear, validated, buildable brief.
Asks the right questions. Surfaces unknowns. Prevents mid-build surprises.

Personal projects: 15-20 minutes.
Client/business projects: 25-35 minutes.
Every minute here prevents hours of rework later.

**Always run in Plan Mode (Shift+Tab). No code. No project files.**

> **Autonomous / headless mode.** At startup resolve the settings with
> `python3 ~/.claude/skills/vibe-mode/scripts/vibe_state.py mode`. If `vibe_mode` is
> `autonomous`, every "wait", "ask", "confirm" and approval step in this skill follows
> vibe-mode's `references/HEADLESS.md` §2 instead: take the recommended option, accept your
> own draft after one self-check, log each choice to `vibe/DECISIONS.md`, never ask the
> user, and stop — writing `vibe/.run_state.json` — only when a person is genuinely required.

---

## The O'Reilly principle this serves

Spec before code — and brief before spec.
The brief is where the hardest thinking happens:
what is the real problem, who has it, what does v1 genuinely need.
Every question skipped here becomes a scope change mid-build.

---

## What's new in v2

- **BRIEF_MD.md template** — structurally consistent output that all downstream skills parse reliably
- **Pre-write quality check** — catches weak user descriptions, unmeasurable criteria, missing non-goals before writing
- **Non-goals as a first-class step** — not optional, always included
- **Agentic detection** — detects AI/agent projects and routes appropriately
- **Fast path floor** — minimum P0 verification even on fast path
- **Complexity estimate** — S/M/L/XL sizing in every brief

---

## How to run this skill — the AI co-founder, not an interrogator

This is the **single front door** for every project. Whether the user brings a raw
idea, a stack of documents, or both, it always starts here and always flows fully
downstream (architect → scaffold → design → build) — nothing is skipped.

Behave like a sharp co-founder who is skeptical *for the user's benefit* — and who
knows when to stop talking and start building.

**1. Research before you interrogate.** Do real web research on the idea first (see
`## Co-founder research`), so your questions are specific and evidence-based, not
generic. A co-founder who's read the market asks better questions and asks fewer.

**2. Weight the thinking: desirability → viability → feasibility.**
Lead with **user-desirability** (does anyone actually want this — the #1 killer),
then **commercial viability** (does the model work), then **technical feasibility**
last (with AI-assisted coding it's rarely the binding constraint). Adapt per idea: a
deep-tech idea pulls feasibility up; a marketplace pulls viability up.

**3. Bounded questioning — DO NOT PESTER.** This is a hard rule, not a preference.
- Ask only the **few highest-leverage questions** — the ones that would change the
  build if answered. Target **≤ 3 questions per round** and **≤ 2 rounds** before you
  have enough for a solid brief. Batch them; never ask one at a time; never re-ask.
- Stop at **"good enough to build,"** not "perfect." Diminishing-returns questions
  (edge cases, far-future features, nice-to-knows) do NOT get asked — they become
  *assumptions to validate* in the brief instead.
- The moment you have enough to write a solid brief, **stop asking and offer to
  proceed.** Over-questioning is a failure mode here, equal to under-questioning.

**4. The user can start building at any time — and they win.** If the user says
"let's build", "start building", "just proceed", "enough questions", or similar —
**stop immediately.** Do not argue or squeeze in "just one more". Show the
**readiness card** (see `## Readiness gate`), get a single "Yes, continue", write the
brief with the open items recorded as assumptions-to-validate, and hand off
downstream. Their call overrides your desire for a tighter brief. Every time.

**5. When documents are provided, critique — don't just accept.** Read them, find
disparities, gaps, and things that could be stronger, and surface those concisely.
But the same bounded/advisory rules apply: point it out once, don't nag.

The path sections (Fast / Personal / Client) below are the *menu of topics* to cover.
Under co-founder mode they are a checklist to satisfy efficiently — not a script to
march the user through step by step. Cover what research and the docs didn't already
answer, within the question budget above.

---

## Step 0 — Intake: read everything the user already has

Thinking, specs, and even the visual design often happen elsewhere (e.g. the Claude
desktop app) and arrive here as pasted text or **one or more dropped files**. This is
the universal front door — inventory and understand it all first, so nothing the user
already produced is ignored and no downstream step is skipped.

**Inventory the project root and the user's message.** There may be several documents
of different kinds. Read each one fully and classify it to the pipeline artifact it
maps to:

| Provided document | Maps to | Satisfies stage |
|-------------------|---------|-----------------|
| idea / brief / PRD / pitch / notes | `BRIEF.md` | THINK (brief) |
| architecture / tech-stack / system-design notes | `ARCHITECTURE.md` | architect |
| spec / requirements / detailed feature list | `vibe/SPEC.md` (via new-app) | — |
| **design: mockup image (PNG/JPG), prototype HTML, Figma export, or a written "the look I want" description** | `DESIGN.md` (ingest via `design-md:` design-artifact mode) | **DESIGN gate** |
| existing source code | → this is `vibe-init:` territory, not new-app |

**Then, as the co-founder:**
- **Empty / near-empty file** (< ~5 lines of real content): say so briefly and build
  the brief together — don't emit a hollow BRIEF.md.
- **Already a canonical BRIEF.md**: accept it, but still **critique it once** (below)
  before moving on — you're a co-founder, not a printer.
- **Real content in a different shape** (external brainstorm, PRD, loose notes):
  **normalize** it onto the canonical BRIEF.md fields (problem, user, core value,
  features, non-goals, stack, complexity) — never discard the user's work by
  re-running a full interview over it.
- **A provided design artifact**: note it — it will satisfy the design gate via
  `design-md:` design-artifact ingestion (image/HTML/prose → DESIGN.md). Do not make
  the user re-do design they already brought.

**Critique what was provided (once, concisely — then stop).** Cross-check the docs for
disparities and gaps: contradictions between docs (e.g. target user vs pricing),
missing brief essentials (unnamed failure mode, no measurable success, no non-goals),
or a claim the research (next section) contradicts. Surface these as a short list —
"here's what's strong, here's what's soft" — and fold the genuine gaps into the
bounded question round. Do **not** nag; point each thing out once.

Whatever the entry, continue through the *same* pipeline: research → (bounded)
questions → quality check → BRIEF.md → spec-review → downstream handoff (architect →
scaffold → design → build). This is what brings externally-produced work to parity.

---

## Step 1 — Capture the idea, assess richness, determine path

Read the user's message carefully.
Extract: core idea, problem mentioned, references, constraints.

**Assess message richness first:**

If the message contains ALL of these clearly:
- Problem stated specifically (not just a domain)
- Primary user described with specificity (not "people" or "users")
- Core value or outcome stated (a single thing, not a list)
- Feature set indicated
- Platform and tech preferences mentioned
- Timeline or constraints mentioned

→ **Fast path** — go to the **Fast Path** section below.

If any of these is missing or vague → run the full path.

**Determine project type — ask if not clear:**
> "Quick question: are you building this for yourself, or for a client or business?"

- **Personal project** → Personal Path (Steps 2P–9P)
- **Client / business project** → Client Path (Steps 2C–13C)

If extremely vague — ask ONE question first:
> "What problem are you trying to solve, or what made you think of this?"

---

# CO-FOUNDER RESEARCH

Run this **before** the question rounds (and before Fast/Personal/Client topics),
so questions are specific and evidence-based. This is what makes it feel like a
co-founder who did their homework rather than a form.

**If web tools are available** (WebSearch / WebFetch): do focused research —
- **What already exists** — direct competitors and substitutes (what people use
  today, even if it's a spreadsheet). Note how the idea is differentiated, or isn't.
- **How similar ideas fail** — common failure modes / graveyard for this category.
- **Market & timing** — is there a "why now"? demand signals, obvious tailwinds/headwinds.
- **Landmines** — regulatory, privacy, platform-policy, or technical constraints that
  could block v1 (e.g. health data, payments, scraping, app-store rules).
- Keep it tight — a few high-signal searches, not a literature review. Capture 3–6
  findings with source URLs; they feed both the questions and the BRIEF's research/risk
  section.

**If web tools are NOT available:** say so plainly —
> "I can't run live research in this session, so I'll reason from what I know and
>  flag assumptions to validate. (Enable web tools for grounded market research.)"
Then proceed from domain knowledge and mark research-dependent claims as assumptions.

**Turn research into leverage, not lecture.** Use findings to sharpen the ≤3 questions
that matter (e.g. "X already does this well for $9/mo — what's your wedge?") — not to
deliver a report the user didn't ask for. Two or three crisp insights, then the questions.

---

# FAST PATH

For messages with a complete, clear picture.

**Step F1 — Confirm understanding:**
> "You've given me a solid picture. Let me confirm before writing the brief:
>
> Problem: [one sentence]
> User: [specific description]
> Core value: [single outcome]
> v1 features: [list]
> Stack direction: [tech choices mentioned]
>
> Anything to correct?"

Wait for confirmation.

**Step F2 — Run P0 quality checks (internal):**
Read `references/BRIEF_QUALITY_CHECK.md` — Fast path quality floor section.

Run ONLY the P0 checks:
- P0-1: User specific enough?
- P0-2: Core value single outcome?
- P0-3: Success criteria measurable?
- P0-4: Non-goals stated?
- P0-5: Feature boundary clear?

If all pass — proceed immediately to non-goals and agentic check.

If 1-2 fail — ask only about those:
> "Two quick things before I write this:
> [Question for failing P0-1 if relevant]
> [Question for failing P0-3 if relevant]"

Wait for answers. Then proceed.

**Step F3 — Non-goals (always, even on fast path):**
> "One more: what is v1 explicitly NOT? Even the most complete briefs
> benefit from naming what's out of scope — it protects the build.
> Two or three things that someone might expect but v1 won't include."

Wait for answer.

**Step F4 — Agentic detection:**
Read `references/BRIEF_QUALITY_CHECK.md` — Agentic detection section.
Run the signal check. Announce if detected.

→ Skip to **Pre-write quality check** and **Generating BRIEF.md**

---

# PERSONAL PATH

---

## Step 2P — The problem

> **Let's start with the problem:**
>
> 1. What frustrates you (or someone you know) that this would fix?
> 2. How do people solve this today — spreadsheet, another app, manually?
> 3. What's wrong with the current approach?

Wait for answers. If shallow — ask the follow-ups you need (batched, not one at a time).

Synthesise and confirm:
> "So the problem is: [one sentence]. People currently [cope by X]
> but that's frustrating because [why it falls short]. Is that right?"

Wait for confirmation before continuing.

---

## Step 3P — The user

> **Who uses this?**
>
> 1. Who has this problem most acutely — be specific.
>    Not "everyone." Try "freelancers invoicing 5+ clients a month"
>    or "parents tracking teen driving hours."
> 2. How often — daily, weekly, when a specific event happens?
> 3. Building for yourself, for others, or both?

If vague — push:
> "Can you describe a real person who has this problem?
> What do they do, how often does this come up, and in what context?"

Synthesise: "Primary user: [specific]. Uses it [frequency] because [trigger]."

---

## Step 4P — The core value

> **The one thing:**
>
> If this could only do ONE thing perfectly, what would it be?
> Not a feature — the outcome. What changes for the user because this exists?

Push back if multiple things listed:
> "If you had to pick just one — the thing that makes someone say
> 'I can't go back to not having this' — what is it?"

Lock this in. Every feature must serve this one thing.

Then ask:
> "How will you know in 4 weeks whether this is working?
> What would you see that tells you users are getting that value?"

This establishes the success signal. Lock it alongside the core value.

---

## Step 5P — Features, navigation, and non-goals

> **Features — let's be ruthless:**
>
> Based on what you've told me, here's what I think v1 needs:
> [List 4-6 features derived from the conversation — with one sentence
> explaining how each serves the core value]
>
> For each: must have for v1, v2, or cut entirely?

Wait for responses. Ask:
- Anything missing that makes v1 feel incomplete?
- Is anything here actually scope creep?

Finalise v1 feature set.

> **Navigation structure — lock it now:**
>
> Based on the features, the top-level destinations are:
> [Derived navigation — e.g. "Today / Projects / History"]
> Does this feel right?

**Rule:** v1 is the smallest thing that delivers the core value. Not the full vision.

> **Non-goals — what v1 explicitly does NOT include:**
>
> Based on what we've cut and what wasn't mentioned:
> - [Derived non-goal from what was deferred]
> - [Derived non-goal from what's out of scope]
>
> Anything to add? What might someone assume this does that it won't?

At least 2 non-goals required. Push if the user can't name any:
> "Think about features people often ask for in [this type of app] that you
> deliberately don't want to build yet. What's out of scope?"

---

## Step 6P — Competitive check

> **Quick market check:**
>
> 1. Who else has built something like this?
> 2. What do they do well that you want to match or exceed?
> 3. What gap do they leave that yours fills?

If the user says nothing exists — surface similar-adjacent solutions.
If they know competitors well — capture the differentiation in the brief.

---

## Step 7P — UI direction

> **How does it feel to use?**
>
> 1. Mobile, desktop, or both?
> 2. Quick interactions (30 seconds) or deep sessions (20 minutes)?
> 3. Any apps whose UI you love — even if unrelated?
> 4. One word for the feeling: calm, powerful, playful, minimal, premium?

Synthesise: "UI: [platform], [quick/deep], feel: [word]. References: [apps]."

---

## Step 8P — Tech and constraints

> **Practical stuff:**
>
> 1. Stack preference, or happy for a recommendation?
> 2. User accounts / login needed?
> 3. Data stored long-term or synced across devices?
> 4. Any third-party services? (payments, maps, notifications, AI)
> 5. Deploying publicly or personal/internal use?
> 6. How much time do you realistically have for v1?

Recommend a stack with reasoning. Full range of options:

| Scenario | Options |
|----------|---------|
| Static / simple | Plain HTML + CSS + JS, Astro, 11ty |
| Frontend only | React + Vite, SvelteKit, Vue + Vite |
| Full-stack web | Next.js, SvelteKit, Remix, Nuxt |
| Mobile | React Native + Expo, Flutter |
| Backend API | Node + Express/Fastify, Python + FastAPI |
| BaaS | Supabase (auth + DB + storage), Firebase |
| Deployment | Vercel, Netlify, Railway, Fly.io |

Choose the simplest stack that fits the actual requirements.
Never default to a heavy stack when something simpler fits.
Present with reasoning. Ask: "Does this work, or any constraints?"

---

## Step 9P — Risks and complexity

> **Honest risk check:**
>
> Here are the things most likely to cause pain mid-build:

Specific risks to surface:
- "Daily notifications require a backend even though everything else is client-side"
- "Real-time sync is significantly harder than local-only storage"
- "The calendar view will take longer than all other features combined"
- "Sharing data between users makes auth and permissions non-trivial"

For each: flag it, note the implication, suggest the simpler alternative.

**Complexity estimate (internal — for the brief):**
Read `references/BRIEF_MD.md` — Complexity sizing guide.
Assign S / M / L / XL based on feature count, backend, integrations, AI.
State the complexity driver — the one thing that makes this harder than it looks.

→ Run **Agentic Detection** then proceed to **Pre-write quality check**

---

# CLIENT PATH
*All steps mandatory. No exceptions.*
*The questions that feel unnecessary on a small job are the ones that save you.*

---

## Step 2C — Client context

> **Tell me about the client and this project:**
>
> 1. What does the client do? (business type, size, industry)
> 2. New product, or replacing/extending something existing?
> 3. What triggered this project right now? (pain point, deadline, competitor)
> 4. Have they tried to solve this before? What happened?
> 5. How technical is the client?

Synthesise and confirm.

---

## Step 3C — The problem

> **The problem the client is trying to solve:**
>
> 1. What frustrates the client or their users that this would fix?
> 2. How do they solve it today?
> 3. What does the problem cost? (time lost, money lost, errors, customers lost)
>    Push for specifics — "it's frustrating" is not enough. "3 hours per invoice" is.

The cost framing matters — it establishes what the solution is worth and sets delivery stakes.

Synthesise and confirm.

---

## Step 4C — Stakeholders

> **Who are the people involved?**
>
> 1. Who is the decision-maker — approves spec, signs off on delivery?
>    (Often different from your day-to-day contact)
> 2. Who are the actual users day-to-day?
> 3. Other stakeholders with opinions? (IT, legal, finance, other departments)
> 4. Who defines "done" — one person or a committee?
> 5. What does approval look like — one round or multiple?

If stakeholders are vague — push:
> "Who specifically signs off? 'The team' isn't specific enough.
> Unclear sign-off authority is one of the most common causes of project delays."

Synthesise and confirm.

---

## Step 5C — The user

> **Who actually uses this day-to-day?**
>
> 1. Describe specifically — not "staff." Try "warehouse staff logging inventory
>    on tablets while standing at shelves."
> 2. How often and in what context?
> 3. Technical comfort level?
> 4. Any workflow constraint that breaks standard patterns?
>    (always on mobile, spotty internet, gloves, screen reader, accessibility)

Synthesise and confirm.

---

## Step 6C — Success definition

The step most often skipped. Never skip it.

> **What does success look like?**
>
> 1. Primary metric — push for a number.
>    "Reduce invoice processing time" → "by how much? 50%? 80%? From what baseline?"
> 2. What would make the client consider this a failure?
>    (Most important question — surfaces hidden expectations.)
> 3. Hard deadline? What's the consequence of missing it?
> 4. What does successful v1 look like in 3 months? 12 months?

Push back on vague answers:
> "'Users should find it easy' — can we make that measurable?
> 'A new user completes their first invoice in under 5 minutes without help.'"

Synthesise and confirm.

---

## Step 7C — The core value

> **The one thing:**
>
> If this could only do ONE thing perfectly for users, what would it be?

Push back if multiple listed. Lock one answer.

Check alignment with success metric from Step 6C:
> "The core value is [X] but the success metric is [Y].
> These need to point in the same direction — do we need to revisit either?"

---

## Step 8C — Features, navigation, and non-goals

Same structure as Step 5P, with additions:

> **Features — derive from core value and success metric:**
>
> [List features, noting: client-requested vs framework-derived]
> For each: must have for v1, v2, or cut?

> **Navigation structure — lock it now:**
> [Derive and confirm]

> **Non-goals — at least 3 for client projects:**
>
> Based on what we've discussed:
> - [Derived non-goal]
> - [Derived non-goal]
> - [Derived non-goal]
>
> What else might the client assume v1 includes that it won't?

If client-requested features don't serve the core value:
> "[Feature] doesn't directly serve [core value]. Recommend v2 — would the client accept that?"

---

## Step 9C — Competitive check

> **Who else has built something like this for this market?**
>
> 1. Competitors or adjacent tools the client knows?
> 2. What do they do well — what should yours match?
> 3. What gap does this fill that existing solutions miss?
> 4. Has the client looked at off-the-shelf solutions? Why build vs buy?

Capture build vs buy decision in the brief.

---

## Step 10C — Constraints

> **Constraints — things we don't control:**
>
> 1. **Timeline:** v1 delivery date? Hard or preference?
> 2. **Budget:** Monthly infrastructure cap?
> 3. **Tech:** Mandatory stack, platforms to avoid, existing systems to integrate?
>    (CRM, ERP, existing DB, auth provider)
> 4. **Compliance:** GDPR, financial data, health/HIPAA, industry-specific?
> 5. **Brand:** Existing design system, guidelines, visual identity?
> 6. **IP:** Who owns the codebase after delivery?
> 7. **Access:** What credentials and APIs are needed and when?

Flag anything that affects architecture immediately:
- Tech mandates → feeds directly into architect:
- Integrations → significant complexity risk
- Compliance → affects data model, auth, hosting
- Access timeline unconfirmed → Phase 1 delay risk

---

## Step 11C — UI direction

Same as Step 7P, plus brand constraints:
Questions 1-4 from Step 7P, plus:
> 5. [If brand constraints exist] Brand guidelines to reference?

---

## Step 12C — Tech and stack

Discovery first, recommendation second:
> Constraints described: [summarise mandates]
> Given these, my recommended stack is: [with reasoning — note mandated vs recommended]
> Does this fit?

Apply same breadth of stack options as Step 8P.

---

## Step 13C — Risks and delivery

**Product risks** — same as Step 9P.

**Client/process risks — always flag whichever apply:**
- **Scope creep:** Informal mid-build requests are the most common cost overrun source.
  Formal change process recommended before build starts.
- **Approval delays:** Agree on review turnaround times upfront.
- **Access delays:** Request all credentials before Phase 1.
- **Stakeholder misalignment:** Single sign-off point strongly recommended.
- **"Done" redefined at delivery:** Delivery criteria must be in the formal agreement.

Note which risks acknowledged vs dismissed.

**Delivery definition:**
> 1. Handoff: documentation, training, support period expected?
> 2. Acceptance testing: client tests before sign-off, or spec completion sign-off?
> 3. Post-delivery: who handles maintenance and hosting?

**Complexity estimate (internal — for the brief):**
Read `references/BRIEF_MD.md` — Complexity sizing guide.
Assign S / M / L / XL. Add delivery risk rating for client projects.

→ Run **Agentic Detection** then proceed to **Pre-write quality check**

---

# AGENTIC DETECTION

Run after features are locked — before the pre-write check.

Read `references/BRIEF_QUALITY_CHECK.md` — Agentic detection section.

If 2+ signals detected:
> "This project involves AI agent logic — I can see [signal A] and [signal B]
> in what you've described.
>
> Before `architect:`, I'd strongly recommend running `agent:` first.
> Agent architecture affects your data model, error handling, cost structure,
> and how the whole system is wired together. Getting this wrong mid-build
> is expensive to undo.
>
> I'll flag this in the brief. After `architect:` reads the brief,
> it will remind you."

Set `agentic_flag: true` in the brief.

If 1 signal detected — ask:
> "Will [feature] involve an AI model making decisions or taking actions
> autonomously, or is it a simpler API call?"

If 0 signals — no flag.

---

# READINESS GATE (advisory — the user decides)

Reached two ways: (a) you've satisfied the question budget and have enough for a solid
brief, or (b) **the user says "let's build" / "start building" / "just proceed" /
"enough questions" at ANY point** — including mid-interview. Either way, stop asking
and show the readiness card. This is the anti-pester escape hatch.

Compute a quick **readiness read** — how complete the brief is against the P0
essentials (specific user, single core value, measurable success, non-goals, clear v1
boundary) plus any research risks still unaddressed. Express it simply and show what's
still soft. Do **not** turn this into more questions.

```
IDEA READINESS — [project name]

  Ready:  ~[N]%   [▓▓▓▓▓▓▓░░░]

  Solid:
    ✓ [thing that's well-defined]
    ✓ [thing that's well-defined]
  Still open (would be recorded as assumptions to validate):
    • [open item — e.g. pricing model not decided]
    • [open item — e.g. primary user is still two personas]
    • [research risk — e.g. competitor X already owns this wedge]

  You can keep sharpening, or build now and validate the open items as you go.
```

Then a single choice — never a wall of follow-ups:
> "Continue to build with these open items noted, or sharpen a bit more?
>  [Yes, continue] / [Keep sharpening]"

- **Yes, continue** → write BRIEF.md now, recording every open item in its
  **Open assumptions to validate** section (so nothing is lost), and hand off
  downstream. Do not re-litigate. The user chose; respect it fully.
- **Keep sharpening** → ask the *single* highest-value open question, then offer the
  card again. Still bounded — don't spiral.

A brief written this way is valid. Downstream skills read the open-assumptions section
and treat those items as things to confirm, not as blockers.

---

# PRE-WRITE QUALITY CHECK

> 🧠 **Effort:** synthesising the brief is a high-leverage, one-shot decision —
> every downstream skill treats BRIEF.md as fixed. Run this with adaptive
> thinking at high effort (`thinking: {type: "adaptive"}`, `output_config.effort:
> "high"`); reason through gaps and alternatives before writing, don't pattern-fill.

**Internal step — not shown to user.**

Read `references/BRIEF_QUALITY_CHECK.md` in full.
Run all P0 checks against the confirmed conversation answers.
Run applicable P1 checks.

If a P0 check fails **and the user has not chosen to proceed**: fold it into the
bounded question round (within the ≤3-per-round budget) — don't fire a fresh
follow-up for every failing check one at a time.

**If the user has chosen "Yes, continue" at the readiness gate:** do NOT block.
Record each unmet P0 as an entry in the brief's **Open assumptions to validate**
section and write BRIEF.md. The user's decision to build outranks a perfect P0 pass —
never trap them in the quality check.

Log the quality summary internally:
```
PRE-WRITE QUALITY CHECK
P0: [N/5] passing
  [results per check]
P1: [results per applicable check]
Agentic: [Detected / Not detected]
Proceeding to write BRIEF.md.
```

---

# GENERATING BRIEF.md

Read `references/BRIEF_MD.md` in full.
Use the personal or client template based on the path taken.
Fill every field — no placeholders left blank. No section omitted.

**Synthesise from confirmed answers only.**
Do NOT re-read the full conversation.
Use only what was explicitly confirmed at each step gate.
This ensures the brief reflects decisions made, not things mentioned in passing.

Fill the complexity estimate section from the internal sizing done in the risks step.
Fill the agentic flag section from the detection step.
Fill the open questions section with anything unresolved — delete it if none.

Save as `BRIEF.md` at the project root.

Present it:
> "Does this brief capture what you want to build? Anything to adjust?"

For client projects, one additional check:
> "Is there anything in the constraints or delivery definition that needs confirming
> with the client before the build starts? Resolve open questions now, not mid-Phase 1."

When approved:

---

# SPEC-REVIEW AND HANDOFF

**Announce:**
> "BRIEF.md written. Running spec-review to check quality before architect:..."

Invoke `vibe-spec-review`:
- Trigger source: `brainstorm`
- Scope: BRIEF.md only

After spec-review completes (pass or acknowledged):

---
> ✅ **Brief ready.**
>
> **Decisions locked:** [N]
> **Risks surfaced:** [N]
> **Features deferred:** [N]
> **Non-goals:** [N explicitly stated]
> **Complexity:** [S / M / L / XL] — [complexity driver]
> **Agentic:** [✅ detected — run agent: first / — not detected]
> [Client: stakeholders · success metrics · constraints · delivery terms captured]
> **Spec review:** [✅ clean / ⚠️ [N] warnings acknowledged / 🔴 [N] P0s fixed]
>
> **Next:**
> ```
> [If agentic:] agent: [project name]
> [Then:] architect: confirm
>
> [If not agentic:] architect: confirm
> ```
> Both skills read BRIEF.md automatically.
---

---

## How downstream skills use BRIEF.md

`architect:` reads BRIEF.md for platform, stack, constraints, open questions.
`new-app:` reads BRIEF.md to pre-populate spec — skips all answered questions.
`vibe-agent:` reads BRIEF.md for problem, users, constraints, integrations.
`change-spec:` reads BRIEF.md in Step 2 as the original intent baseline.
`review:` reads BRIEF.md for original problem and core value sanity check.

The structural consistency of BRIEF.md (from the template) means every
downstream skill finds the same field names in the same sections every time.
No parsing variation. No missing data.

---

## Conversation principles

**Bounded, not exhaustive.** ≤3 questions per round, ≤2 rounds, batched. Ask only what
would change the build. Stop at "good enough to build." Over-questioning is a failure.
**The user can build anytime.** "Let's build" → stop, show the readiness card, respect
the choice. Never pester, never squeeze in "one more question", never re-ask.
**Reflect and confirm.** Misunderstandings caught here are free. Mid-build they cost days.
**Push for specifics.** Vague answers produce vague briefs produce expensive surprises.
**Non-goals are not optional.** They protect the build. Always get at least 2 (personal) or 3 (client).
**The brief is opinionated.** Synthesise, recommend, take a position. Produce decisions, not options.
**Push back on scope creep.** "Does [feature] serve [core value], or is it nice-to-have?"
**Be honest about complexity.** "That's possible but adds backend complexity. Would [simpler] work?"
**For client work: never let undefined stakeholders stand.** Who specifically signs off.
**For client work: always capture the cost of the problem.** "Frustrating" is not a cost.

**Goal for personal:** smallest v1 that delivers the core value.
**Goal for client:** smallest v1 that hits the primary success metric, within constraints, no surprises at delivery.
