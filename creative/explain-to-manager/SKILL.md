---
name: explain-to-manager
description: "Interview an engineer about the gap between what their non-technical manager expects and the actual state of the work, then produce a business-friendly status update that preserves trust. Use when the user needs to deliver bad news upward — work isn't ready, a deadline will slip, AI or a technology under-delivered — or asks anything like \"how do I explain this to my boss / manager / management\". Also use for justifying a cost, tooling spend, or risk-closure proposal to management, and for defending existing spend or invisible engineering work under scrutiny."
compatibility: Pure conversational skill; no scripts, network, or repo access required.
---

# Explain to Manager

## Purpose

Turn "it's not ready and I dread saying so" — or "they'll never approve this spend" — into a brief the manager can trust, and repeat upward, without the engineer losing credibility.

The skill has two jobs, in order:

1. **Extract the real picture** from the engineer with a structured interview. The engineer's first framing is almost never the full story; the specifics you pull out are the entire value of the final brief.
2. **Translate** engineering reality into managerial language: dates, risk, customer impact, decisions — not implementation detail.

Do not skip to writing. A polished brief built on a one-line problem statement is fiction with good grammar.

## Operating principles

Hold these through every phase:

- **Trust is built on forecast accuracy, not optimism.** A dependable "March 15, with these two risks" beats a hopeful "couple of weeks" every time. Never optimize the brief to sound better than the engineer's actual confidence.
- **Bad news early is a gift; bad news late is a betrayal.** If the interview reveals the manager should hear this today, say so explicitly.
- **Managers don't fear delays — they fear surprises and losing the ability to plan.** Every deliverable must restore their ability to plan and to explain the situation to *their* boss.
- **Scout, not victim.** The engineer must never sound like the work happened to them ("it turned out harder than I thought"). They sound like a scout reporting terrain: "here's what we've now confirmed is in the way, and the corrected route."
- **The manager must leave with three things:** a headline they can repeat verbatim, a date or checkpoint, and a decision that is theirs to make (or an explicit "nothing needed from you").

## Phase 0 — Intake

Before interviewing, establish from what the user already said (ask only for what's missing):

1. **What format is the deliverable?** Slack message, email, 1:1 talking points, standup blurb, or a slide's worth of bullets. Default to 1:1 talking points + a short written follow-up if unspecified.
2. **Who is the manager?** Direct engineering manager, non-technical founder/CEO, product/business stakeholder, or a skip-level. How technical are they, really?
3. **When is the conversation?** In an hour vs. next week changes how much interview depth is affordable. If it's imminent, compress Phase 1 to the questions marked ★.
4. **Which shape is the conversation?**
   - **Reset** — bad news about existing work: not ready, slipping, un-integrated, under-delivering.
   - **Proposal** — creating a new expectation: spend, tooling, headcount, proactive risk closure.
   - **Defense** — justifying existing spend or invisible work under scrutiny: maintenance capacity, reliability work, a license or platform bill someone circled.

   The shape selects the interview set (Phase 1), the applicable gap types (Phase 2), and the brief skeleton (Phase 4).

Calibrate every later phase to the audience answer:

| Audience | Calibration |
|----------|-------------|
| Non-technical manager / founder | Zero mechanism; one analogy allowed; every impact in customer, money, or date terms. |
| Technical manager, cost-skeptic | One sentence of mechanism is fine; drop the analogy (it reads as condescension); lead with trade-off numbers. |
| Finance / budget owner | Denominator first ("X% of the cloud bill"), risk second, mechanism never. |
| Skip-level / exec | Hard cap ~120 words; optimize for forwardability — assume every sentence may be pasted upward verbatim. |

## Phase 1 — The interview

Interview the engineer before writing anything. Rules of engagement:

- Batch 3–4 questions at a time (use AskUserQuestion when available; otherwise ask in plain prose). Never dump all dimensions at once.
- Never ask what the user already told you.
- Push back on vagueness. "It's mostly done" gets "what specifically works end-to-end today, and what breaks if I try it?" Vague inputs produce the exact vague reassurances that caused this situation.
- When an answer is "I don't know," route it before moving on: drop it if the brief doesn't need it, give it to the manager as something only they can answer, or hand the engineer a named task to check before the conversation. Never close the gap yourself.
- Two to three rounds is typical. Stop when you can answer every checklist item in Phase 4 from interview material alone.

For the **reset** shape cover dimensions A–E. For the **proposal** shape cover P1–P4 plus E. For the **defense** shape use P1–P4 with the substitutions at the end of this phase.

### A. The expectation
- ★ What exactly does the manager currently believe? (A date? "It's basically done"? "AI makes this fast now"?)
- Where did that belief come from — the engineer's own earlier estimate, a demo, a sales promise, AI hype, an assumption nobody corrected?
- How public is it? Has the manager already committed it to their boss or a customer? (This changes the stakes and the tone.)
- What's the real drop-dead date vs. the aspirational one?

### B. The reality
- ★ What works end-to-end today? What could be demoed right now without hand-holding?
- What's honestly left — enumerated, not as a percentage?
- What is currently blocking, and since when?

### C. The why (root cause)
- ★ What specifically was discovered that wasn't known when the expectation was set?
- Was the original estimate ever realistic, or under-scoped from day one?
- If AI/tooling was expected to accelerate this: where did it actually help, where did it not, and why? Get specifics — review burden, integration work, hallucinated output, the part that was never automatable.

### D. History and trust balance
- Is this the first reset on this work, or the second or third? (A third reset needs a fundamentally more conservative new date and an explicit acknowledgment of the pattern.)
- Were early warnings given, or is this landing cold?

### E. The path forward
- ★ What is the credible next milestone, and what date does the engineer actually believe at ≥80% confidence — not the date they think the manager wants?
  - Elicitation technique: ask "what date would you bet your weekend on?" — use that one, not the first date offered.
- What are the realistic options with trade-offs: cut scope, move the date, add help, de-risk with a spike? Managers respond far better to a menu than to a verdict.
- ★ What faster route has already been ruled out, and what does it miss? "Can't we buy our way out of this?" is the first question back. If nothing was evaluated, the brief says so rather than implying a comparison.
- What does the engineer need from the manager — a decision, an escalation, air cover, or nothing?
- What will be *demonstrably true* at the next checkpoint? ("You'll see it process a real customer file on the 15th" beats "it'll be further along.")

### P1. Stakes of inaction (proposal shape)
- ★ What breaks, costs, or embarrasses if this isn't done — in business terms (customer trust, audit exposure, unexplained spend, outage hours)?
- Has a small version of it already happened — a near-miss, a question that took hours to half-answer?

### P2. Cost and its denominator (proposal shape)
- ★ The exact number, and what it's relative to — "under X% of our cloud bill" does more persuasion work than the number itself.
- Flat or usage-scaled? If usage-scaled, the manager must see the growth expectation and a review point, not a fake flat figure.

### P3. Alternatives ruled out (proposal shape)
- ★ What cheaper or free options were evaluated, and what does each one miss?
- If the answer is a gut call, the brief must not claim a full evaluation — and tell the engineer to verify before sending. "Can't we do this cheaper?" is always the first question back.

### P4. The ask type (proposal shape)
- ★ Approve now, budget line for next period, direction before investing, or awareness with default-yes (proceeding unless veto)?
- For dimension E in this shape: the checkpoint is an enablement date plus a first review point ("actual cost, and one thing it caught, after month one").

### Defense shape: P1–P4, substituted
- P1 → What does this work or spend *quietly prevent*? ★ Best evidence: what happened the last time it lapsed, or the nearest near-miss.
- P2 → What it costs today (with denominator) vs. what cutting it would save — and expose.
- P3 → What the cheaper version looks like, and the specific risk it accepts.
- P4 → The ask is usually "keep as is" or an informed-cut menu with named risks — never a bare defense of the status quo.

## Phase 2 — Diagnose the gap type

Classify the gap; it drives the reframe and the analogy. Full analogy bank and worked examples: [references/playbook.md](references/playbook.md).

| # | Gap type | The manager thinks… | The reframe |
|---|----------|--------------------|-------------|
| 1 | **Iceberg** (hidden complexity) | "The feature works, I saw it." | The visible part is done; the invisible majority — rare-but-real situations, failure handling, security, scale — is the remaining work, and it was always the majority. |
| 2 | **Last-mile integration** | "The tech exists, so plug it in." | Each system works alone; making them work *together, reliably* is a project of its own, and it's the one we're in. |
| 3 | **Demo vs. product** | "I saw it working in the demo." | A demo proves the idea; a product survives real users, bad inputs, and Monday mornings. The distance between them is the plan I'm presenting. |
| 4 | **Dependency drag** | "Why is your thing late?" | Our part is on track/done; we're gated on X. Here's what we're doing to unblock and what escalation would help. (State facts; never assign blame.) |
| 5 | **Quality bar** | "It works, ship it." | It works in the happy path; shipping below the bar converts one late feature into weeks of customer-visible failures. Here's the cost of each option. |
| 6 | **AI reality check** | "AI should make this 10–100x faster." | AI genuinely accelerated X (say what, quantified). Drafting got faster; verifying, integrating, and owning correctness did not — and for this task, that was always most of the work. |
| 7 | **Moving target** | "You've had plenty of time." | The thing we're building today is materially bigger than what was scoped — here's the delta, and the date that matches the current scope. |
| 8 | **Estimate miss** | "You said two weeks." | The estimate was wrong; here's specifically what I mis-sized, the corrected number, and what I've changed so the new number is trustworthy. Own it in one clean sentence — no cushioning, no groveling. |
| 9 | **Insurance ask** (proposal shape) | "Nothing's broken — why pay?" | After the incident is the expensive time to buy this — and the evidence or protection can't be backfilled to cover the past. Small known cost now vs. unbounded unknown cost later. |
| 10 | **Invisible work** (defense shape) | "What am I even paying for? Why so little feature progress?" | The success of this work looks like nothing happening. Here's what "nothing" prevented — with last-lapse evidence — and what cutting it would save vs. expose. |

Real situations often combine two (AI reality check sitting on top of an iceberg is the classic). Name the dominant one; mention the second only if it changes the plan.

## Phase 3 — Translation rules

Apply these when drafting. The full engineer-speak → business-speak dictionary is in [references/playbook.md](references/playbook.md).

1. **Headline first.** The first sentence carries the state and the new checkpoint. Never make the manager read the explanation to find out how bad it is.
2. **Business units only.** Dates, money, risk, customer impact, scope. Translate or delete every internal term — "refactor," "tech debt," "flaky," "staging," "edge cases," "CI" all have plain-language equivalents in the dictionary.
3. **Separate facts / assessment / plan / ask.** Never blend "what happened" with "what I think it means" — blended updates read as spin.
4. **One analogy, maximum.** Chosen from the gap type. Analogies are seasoning; a brief that's all analogy reads as evasion.
5. **No naked dates or numbers.** Every date ships with its confidence and the one risk that would move it: "the 15th; the one thing that moves it is X, and I'll know by Tuesday." Every number ships with its denominator or comparison: "2 of 12 modules," "under 1% of the storage bill" — a bare number forces the manager to guess whether it's big.
6. **Own without groveling.** One sentence of ownership. Zero sentences of self-flagellation. Zero blame of teammates, vendors, or tools — blaming the AI tool reads exactly like blaming the compiler.
7. **Discovery framing.** Replace "it's harder than I thought" with what specifically is now known that wasn't: "we've confirmed the vendor's API drops connections under load — that's the work."
8. **Hand them the upward line.** Include one quotable sentence the manager can forward to *their* boss verbatim. If you don't write it, they'll improvise it — badly.
9. **Commit to a cadence.** "Next update Friday, or immediately if X changes." A promised cadence rebuilds trust mechanically; it converts "waiting and worrying" into "scheduled and handled."
10. **Banned phrases:** "basically done," "should be ready soon," "just needs testing," "one small thing left," "99% done," "hopefully," "fingers crossed." Each one is a future credibility invoice.

## Phase 4 — Produce the deliverables

Produce, in the requested format:

1. **The headline** — ≤25 words. State + new checkpoint + tone of control.
2. **The brief** — skeleton by shape. **Reset:** Headline → What's solid → What we learned / what changed → New plan with checkpoint dates → Risks and what would move the date → Options + the ask (or "nothing needed") → Next update. **Proposal:** Headline → What → Why now (stakes of inaction) → Cost with its denominator → Plan + review checkpoint → The ask or veto window → Next update. **Defense:** Headline → What it quietly prevents (last-lapse evidence) → Cost vs. exposure of cutting → Informed-cut menu with named risks → The ask, with a review point attached to any cut taken. Length caps by format: email ≤250 words, Slack ≤150, slide = headline + 5 bullets, 1:1 talking points ≤6 lines (they must survive being remembered under stress). Managers skim; brevity reads as control. When the cap and the skeleton collide, cut the analogy first. Then cut the separate upward line if the manager forwards or presents the brief itself, since its first sentence already does that job — and the next-update line if they don't. Cutting an element waives its checklist item below. The anchor and the ask are never what gets cut.
3. **Hard-questions prep** — the 3–5 toughest questions *this* manager will ask, with suggested answers built from interview material. Always consider: "Why am I only hearing this now?", "Can't we add people?", "I thought AI made this fast?", "What can you give me by <earlier date>?", "How sure are you about the new date?" Answer patterns are in the playbook.
4. **Personal do-not-say list** — 3–5 lines the engineer is most likely to blurt under pressure, given how they talked during the interview, with the replacement phrasing.
5. **The promised follow-up (offer it)** — a pre-structured skeleton of the next update the brief commits to (the Friday status line, the month-one cost review). The cadence promise is what rebuilds trust; this makes it get kept.

Before delivering, verify every item:

- [ ] A non-engineer could read the brief aloud to a CEO without stumbling on a single term.
- [ ] One primary anchor, matched to the shape: a delivery date the engineer stated ≥80% confidence in (reset), an enablement date plus first review point (proposal), or a cost-vs-exposure comparison (defense). Tiered delivery has two dates — the anchor is the one that completes the work; the earlier date is scope.
- [ ] The "why" reads as discovery/scouting, not excuse.
- [ ] There's an explicit ask, or an explicit "nothing needed from you."
- [ ] Contains the quotable upward line; reset and proposal briefs also commit to a next-update cadence, and a defense brief offering a cut names when it will report what the accepted risk actually cost.
- [ ] No sentence blames a person, a team, or a tool.
- [ ] Every claim, number, and date traces to an interview answer — nothing invented, and every unknown was dropped, handed to the manager, or assigned as a check before the conversation.

Then offer one iteration pass: read the draft *as the manager* and report what it triggers — alarm, confusion, or confidence — and adjust.

## What NOT to do

- **Don't write the brief from the initial request alone.** The interview is the skill.
- **Don't soften into vagueness.** Vague reassurance is what created this situation; the fix is specific honesty, kindly worded.
- **Don't narrate effort.** Lists of hours worked and obstacles fought read as defensiveness. Show state and plan, not struggle.
- **Don't invent numbers.** No completion percentages, dates, or impact figures the engineer didn't give you.
- **Don't promise on the engineer's behalf.** Every commitment in the brief must be one the engineer explicitly made, at a confidence they explicitly stated.
- **Don't help spin.** If the engineer asks you to hide a known risk or imply a date they don't believe, decline that part: the skill protects trust, and trust doesn't survive discovered spin. Offer the honest framing that costs the least instead.

## References

- [references/playbook.md](references/playbook.md) — translation dictionary, analogy bank, hard-question answer patterns, and four worked before/after examples (feature slip, un-integrated tech, AI reality check, insurance ask).
