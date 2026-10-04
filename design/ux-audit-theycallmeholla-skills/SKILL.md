---
name: ux-audit
description: >
  Reconstruct a product flow, then audit how usable it is — whether it makes sense, where users
  get confused or stuck, whether the copy and instructions are clear, and where friction causes
  drop-off. Produces a prioritized, severity-weighted findings report. Works from three inputs:
  frontend code in a repo, a live running app driven via a browser, or a written flow / spec /
  screenshots. Use this skill whenever the user asks for a UX review, usability audit, "is this
  flow confusing", "does this signup/onboarding/checkout make sense", "why are people dropping
  off", "audit this form", "where's the friction", or hands over a flow and asks whether it's
  user-friendly. Trigger even on casual phrasings ("is my checkout any good?") — it imposes the
  structure ad-hoc UX opinions miss. Audits flow usability and friction; for visual polish and
  interface quality the impeccable audit/critique skills apply instead.
---

# UX Audit

A structured methodology for auditing a product flow end-to-end from a *user's* point of view. The goal is not to redesign the product — it's to **find the moments where a real user hesitates, misunderstands, gets stuck, or gives up**, and present them in a form the owner can act on.

A UX audit answers three questions the owner usually can't answer about their own product, because they're too close to it:

1. **Does the flow make sense?** Is the order of steps logical, is anything asked too early, are there dead ends?
2. **Will users understand it?** Are the instructions, labels, and copy clear at the moment they're needed?
3. **Where's the friction?** What costs effort, attention, or trust — and where does that cause people to bail?

## When to use this skill

- "Audit the UX of this flow" / "usability review of the signup" / "is this onboarding any good?"
- "Does this checkout make sense?" / "why are people dropping off at step 3?"
- "Review this form" / "is this confusing?"
- Pre-launch usability check on a new flow
- Diagnosing a conversion or completion-rate problem
- Periodic UX health check on a live funnel or app

If the user wants a single button restyled or a one-line copy tweak, that's a design suggestion, not an audit — answer directly without this skill.

## Operating principles

These mirror a code audit's discipline, applied to experience instead of code.

1. **Map before you judge.** You cannot audit a flow you haven't reconstructed. Establish the actual step-by-step journey first; opinions come after.
2. **Be the user, not the builder.** Audit from the perspective of someone seeing this for the first time, on a phone, in a hurry, who did not read the docs. The builder's mental model is the enemy.
3. **Severity by drop-off, not by taste.** A dead end that blocks task completion matters more than a slightly-off button color. Sort findings by how much they cost the user (and the business).
4. **Evidence over opinion.** Every finding points at something concrete — a file:line, a screen, a quoted step, a specific label. "This feels clunky" without a pointer is noise.
5. **Actionable remediation.** Each finding ends with a specific fix, not "improve UX."
6. **No false alarms.** If something looks wrong but might be fine in context you can't see (e.g., a field that's pre-filled in production), say so rather than asserting it. Crying wolf destroys the report's credibility.
7. **Code complexity is not user complexity.** Developer confusion — tangled components, duplicated logic, a flow that's hard to read in source — is a *signal*, not proof. Messy code can produce a fine experience, and clean code can produce a baffling one. Always translate a code smell into the *likely* user consequence, and mark it likely (not certain) until you've confirmed it from the user's side. The thing you're auditing is the experience, not the source.
8. **Earn the negatives.** Name what's genuinely good. An audit that only criticizes gets tuned out, and calling out strengths proves you actually went through the flow.

## Step 0: Pick the input mode

The methodology is the same regardless of input; only *how you reconstruct the flow* differs. Determine which mode you're in and read the matching reference file before mapping:

- **Code mode** — you have the frontend source (a repo, a directory, uploaded files). Read `references/code-mode.md`. This is the richest mode: you can see every branch, every validation rule, every copy string, including paths a manual walkthrough would miss.
- **Browser mode** — you have a live, running app and a browser automation tool (Playwright, Claude in Chrome, etc.). Read `references/browser-mode.md`. This is the truest mode: you experience the flow as a user does, including real latency and real feedback.
- **Spec mode** — you have a written description of the flow, a PRD/spec, a Figma export, or screenshots. Read `references/spec-mode.md`. Audit what's described; flag what the artifact leaves unspecified, since gaps in a spec are often gaps in the real thing.

If you have more than one input (e.g., the repo *and* the running app), use them together: walk it in the browser to feel it, read the code to confirm *why* it behaves that way and to catch the branches you didn't trigger. Note in the report which inputs you used.

### Asking for more evidence (only when it changes the answer)

Whatever mode you're in, audit as far as you can with what you have before asking for more. Then escalate to another input *only when the missing evidence would actually change a recommendation* — not as a reflex. A partial audit with marked uncertainties beats stalling for perfect context.

Escalate when, and only when:

- **Layout/visual weight decides the finding** (competing CTAs, above-the-fold priority, perceived density) → ask for **one screenshot of the specific screen**, not "some screenshots."
- **Timing/animation/progressive disclosure** is the issue → ask for **a short recording**.
- **The intended outcome is genuinely ambiguous** and two valid simplifications hinge on it → ask **"what's the single result this user should reach?"**
- **The user type changes the recommendation** (first-time vs returning vs admin) → ask **"who is this flow for?"**
- **A dynamic behavior can't be confirmed statically** → ask for the **live URL or the specific success/error component**.

Make the smallest useful request. Never send a generic "please provide more context." If the flow itself can't be identified at all, that's the one exception where a broad ask is fair.


## The audit workflow

Work through these phases in order. Phase 1 is non-negotiable — every later phase references the map you build here.

### Phase 1: Map the flow

Reconstruct the user journey as a sequence, using the technique from your input mode's reference file. Produce an explicit step list before judging anything:

- **Entry points.** How does a user arrive at step one? Ad, email link, nav click, deep link? First impressions are set before the flow "starts."
- **Steps.** Each distinct screen/state the user passes through, in order.
- **Decisions & branches.** Where the path forks (logged-in vs. not, plan A vs. B, validation pass vs. fail).
- **Inputs asked at each step.** What the user must provide or decide.
- **Exits.** Success state(s), and every way to fall out — abandon, error, dead end, back-button-to-nowhere.

Write this as a short numbered map. It anchors the whole report and is usually itself revealing — if *you* can't cleanly map the flow from the materials, a user can't hold it in their head either. That's finding #1.

### Phase 2: First impression & comprehension

The first few seconds decide whether users continue. Evaluate the entry point and first step:

1. **The "what is this / what do I do" test.** Within ~5 seconds, can a newcomer tell what this is, what they'll get, and what the next action is? If not, why not.
2. **Value before ask.** Is the user given a reason to proceed before being asked to spend effort (sign up, hand over an email, fill a form)? Asking for commitment before establishing value is a top drop-off cause.
3. **Visual hierarchy & the primary action.** Is the single most important next action obvious and prominent, or competing with secondary actions for attention?
4. **Trust at the door.** For anything asking sensitive info or money: are there credibility signals (who is this, why is it safe, social proof) at the moment of hesitation?

### Phase 3: Flow logic & coherence ("does it make sense?")

This is the heart of the audit. Walk the map from Phase 1 and interrogate the *sequence*:

1. **Step ordering.** Does each step logically precede the next? Is anything asked before the user has context to answer it (e.g., shipping options before they know the price)?
2. **Premature or misplaced asks.** Account creation gating access to value; long forms before any payoff; permissions requested before they're relevant.
3. **Redundancy.** Information asked twice; steps that could be merged; confirmation screens that confirm nothing.
4. **Dead ends & traps.** States with no forward path and no clear way out. Back button that loses progress or breaks. Modals with no visible close.
5. **Reversibility.** Can the user change an earlier choice without restarting? Edit a typo'd email at the confirmation step without losing the form?
6. **Branch coherence.** Do all branches (error, empty, logged-out, returning user) lead somewhere sensible, or do some just stop?
7. **Length vs. payoff.** Is the number of steps justified by what the user gets? A 6-step flow for a newsletter signup is a finding.
8. **Structural leakage.** Do any steps exist only because the *code* is organized that way rather than because the user needs them? Separate screens that map to separate modules/endpoints but represent one user task; admin and customer paths fused into one flow because they share a component; a step that's really just a developer's checkpoint. These are steps the user pays for and the architecture caused.

### Phase 4: Clarity, language & developer leakage

Users read less than builders think, and only at the moment of need. Evaluate the words — and watch for the product's internals bleeding into them:

1. **Labels & buttons describe the action/outcome.** "Submit" / "Continue" are weaker than "Create my account" / "See my results." Vague labels force users to guess.
2. **Jargon & internal language.** Terms only the team understands ("provision," "entity," "DCV"), acronyms unexpanded, feature names that mean nothing to outsiders.
3. **Instructions are present at the point of need** — not buried in a help doc, not above a field the user already scrolled past. If a field needs explanation, it's explained inline.
4. **Microcopy carries its weight.** Placeholder text used as a label (disappears on focus — bad), helper text that clarifies format, empty states that tell the user what to do next.
5. **Tone & length.** Walls of text at a decision point; legalese where plain language would do; or the opposite — too terse to be actionable.
6. **Internal state names exposed as UI.** Status enums straight from the code — `draft`, `pending`, `active`, `generated`, `enhanced`, `verified`, `provisioned` — shown to users with no explanation of what they mean or what to do about them. Either translate them to user language or explain them; don't ship the database's vocabulary as the interface.
7. **Implementation-driven categories.** Menu groupings, tabs, or filters that mirror how the data/code is structured rather than how the user thinks about the task. Categories named after tables, services, or modules are the tell.
8. **Admin/internal concepts shown to normal users.** Debug toggles, internal IDs, raw error codes, config that only the team should ever touch, leaking into the customer-facing surface.

### Phase 5: Feedback & system status

Users need to always know what's happening and what just happened (Nielsen heuristic #1):

1. **Progress indication** on any multi-step flow — "Step 2 of 4," a progress bar. Without it, length feels infinite.
2. **Loading & latency feedback.** Spinners/skeletons on anything slow; disabled-and-labeled buttons during submit so users don't double-click or assume it's broken.
3. **Confirmation of actions.** After a meaningful action (saved, sent, purchased), is there unambiguous confirmation? What changed?
4. **Current location.** In a longer app, does the user know where they are and how to get back?

### Phase 6: Error prevention & recovery

How a flow handles mistakes is where good UX separates from bad (heuristics #5 and #9):

1. **Prevention beats correction.** Constrain inputs to valid options (date pickers, dropdowns, input masks) rather than letting users type something rejectable.
2. **Validation timing.** Inline/on-blur validation that catches problems as they happen vs. submit-then-fail that makes the user hunt for what went wrong.
3. **Error messages say what's wrong AND how to fix it.** "Invalid input" is useless; "Password needs at least one number" is actionable. Errors appear next to the offending field, not only in a banner.
4. **Forgiving input.** Accept phone numbers/dates/cards in multiple formats and normalize, rather than rejecting a space or dash.
5. **Destructive-action safety.** Confirmation or undo for anything irreversible (delete, cancel, leave-without-saving). Bonus for undo over a scary confirm dialog.

### Phase 7: Effort & cognitive load

Every unit of thinking or typing is a chance to quit:

1. **Field & step count.** Count required fields and steps. Each one is friction; challenge whether every field is truly needed *now* (or ever).
2. **Choice overload (Hick's law).** Too many options at one decision point paralyzes. Are choices grouped, defaulted sensibly, or progressively disclosed?
3. **Memory burden.** Does the flow make users remember something from an earlier step, re-enter data the system already has, or leave to find info (a code, a number) and come back?
4. **Smart defaults & autofill.** Sensible pre-selections, `autocomplete` attributes, detected values (country from locale) that save typing.
5. **Optional vs. required clarity.** Are optional fields marked, or does the user fill everything fearing it's all mandatory?

### Phase 8: Forms (when the flow contains one)

Forms are where most flows live and die — give them their own pass. See `references/heuristics.md` for the full forms checklist. High-leverage checks:

1. **Labels above or beside fields, persistent** — never placeholder-only.
2. **Correct input types** so mobile shows the right keyboard (`type="email"`, `inputmode="numeric"`), and pickers for dates.
3. **One-thing-per-line** for primary flows; logical grouping; sensible tab order.
4. **Validation & errors** per Phase 6, applied per field.
5. **Save / resume** for anything long, so a refresh or interruption doesn't wipe progress.

### Phase 9: Mobile & responsive

Most real users on a funnel are on a phone — audit as if mobile is primary unless told otherwise:

1. **Tap targets** large enough (~44px) and not crowded together.
2. **Thumb reach** — primary actions reachable, not stranded in a top corner.
3. **Keyboard overlap** — does the on-screen keyboard cover the field being typed or the submit button?
4. **Viewport & zoom** — content fits without horizontal scroll; text legible without pinch-zoom.
5. **Reflow** — multi-column layouts that collapse sensibly, not into overlap or tiny text.

### Phase 10: Accessibility (the UX-affecting essentials)

Not a full WCAG audit, but the accessibility gaps that are also usability gaps for everyone:

1. **Keyboard operability** — can the whole flow be completed without a mouse? Is focus visible?
2. **Focus management** in multi-step flows and modals — does focus move sensibly when content changes, or get lost?
3. **Labels & names** — every input has a programmatic label; icons-only buttons have accessible names.
4. **Contrast** — text and interactive elements meet contrast minimums; don't rely on color alone to signal state (e.g., red-only error).
5. **Motion** — does heavy animation respect `prefers-reduced-motion`? (Relevant to scramble/scroll effects.)

Read `references/heuristics.md` for the complete framework behind these phases (Nielsen's 10 heuristics plus the flow/form/conversion extensions used above).

### Phase 11: Compose the report

Use `assets/report-template.md` as the skeleton (it's the detailed default). For a fast read or a hand-off to engineers, use the concise or ticket-ready variants in `references/report-variants.md`. Structure of the default:

1. **Verdict** (one line, up top): **clear** / **mostly clear** / **confusing** / **broken**, plus 2–4 sentences. Clear = a first-timer finishes without help. Mostly clear = finishes despite a meaningful snag. Confusing = several issues or one ambiguity likely to derail or drop users. Broken = can't be completed, contradicts itself, or hides the essential next step. Lead with this — the owner reads it and skims the rest.
2. **Executive summary** (5–8 lines): what flow was audited, via which input(s), the top 3 issues by user cost.
3. **The flow map** from Phase 1, so the reader sees what you evaluated.
4. **Findings table.** Every finding: ID, severity, category (phase), title, location (file:line / step / screen), one-line description.
5. **Detailed findings.** Each expanded: what it is, the user impact (who hesitates/quits and why), evidence (the specific pointer), recommended fix, and effort estimate (S/M/L).
6. **What's good.** Genuine strengths — calibrates the report and earns trust on the criticism.
7. **Prioritized next steps.** A short ranked list. Do the prioritization for the owner.
8. **Suggested next pass.** Name the specific next file, route, screen, or screenshot worth inspecting — so the audit can iterate instead of ending flat.

**Recommend in subtraction-first order.** When you propose fixes, bias toward removing work before adding it — the cheapest, highest-clarity wins almost always come from the top of this list:

1. **Remove** an unnecessary step, field, or choice.
2. **Consolidate** duplicate screens, components, or repeated questions.
3. **Rename** a label or CTA so it describes the outcome.
4. **Reorder** so context arrives before the decision that needs it.
5. **Add feedback** (loading, progress, confirmation, error guidance).
6. **Add new UI** — only after 1–5 have been genuinely considered. New surface is the last resort, not the first idea.

If scoring would help (the user asks for it, or the flow is complex enough that structure sharpens judgment), apply the optional 1–5 rubric in `references/rubric.md` and derive the verdict from the scores.

### Severity guide

Severity tracks **user/business cost**, not how much it bugs you aesthetically:

- **Critical** — blocks task completion for many users or silently loses their data/progress. Examples: a dead end with no recovery, a form that fails silently, a required action impossible on mobile, a submit that double-charges.
- **High** — significant confusion or friction that drives measurable drop-off for a real subset. Examples: unclear primary action on the entry screen, account-creation gate before any value, errors with no guidance, no progress indicator on a long flow.
- **Medium** — friction or confusion that's surmountable but costs goodwill and some conversions. Examples: jargon labels, placeholder-as-label, validation only on submit, asking for optional info as if required.
- **Low** — polish and consistency. Examples: inconsistent button styling, slightly verbose copy, a redundant confirmation.
- **Info** — observation or opportunity, not a defect.

Don't inflate severity. If everything is Critical, nothing is — and the owner can't tell what to fix first.

## Working with what's available

The skill adapts to the environment:

- **Full tooling** (code execution and/or browser automation): run the inventory script in code mode, drive the live app in browser mode, capture screenshots as evidence.
- **Read-only / no shell / no browser**: do the mapping and all passes by reading the materials you were given. The methodology is unchanged; only the evidence-gathering becomes manual. Note in the report what you couldn't verify dynamically (e.g., "couldn't confirm real loading behavior — recommend checking against the running app").

If a tool fails, proceed without it and say so in the report rather than aborting.

## Reference files

Load as needed:

- `references/heuristics.md` — the full evaluation framework: Nielsen's 10 usability heuristics, plus the flow-logic, forms, conversion/trust, and mobile checklists that the phases draw on. Use it to *ground* findings (name the heuristic), not to lecture — keep findings practical.
- `references/rubric.md` — optional 1–5 scoring across the audit categories, with verdict rules. Use when the user wants a score or the flow is complex enough that structure helps.
- `references/report-variants.md` — concise and ticket-ready report formats for when the detailed default isn't the right shape.
- `references/code-mode.md` — reconstructing a flow from frontend source (routes, components, state machines, form libraries, copy strings, branch enumeration).
- `references/browser-mode.md` — walking a live app with browser automation; what to capture as evidence; triggering error/empty/edge states.
- `references/spec-mode.md` — auditing a written flow, PRD, or screenshots; flagging unspecified gaps.

## Scripts

- `scripts/ui_inventory.sh <path>` — best-effort inventory for code mode: lists route/page files, components, forms, and visible copy strings to orient the flow map. Optional — skip if no shell.

## Final reminders

- A UX audit is a service to the owner and, through them, to their users. Be honest, specific, and useful.
- The builder can't see their own flow clearly — that blind spot is exactly what you're being paid to cover. Stay in the newcomer's shoes the whole way.
- Findings without remediation are complaints. Findings without evidence are opinions. Give both.
- When you genuinely can't tell whether something's a problem without context you don't have, say so. Honest uncertainty beats confident wrongness.
