---
name: Envelope
description: Classify any incoming directive as Ship / Ask one focused question / Propose first. Forces a sharp decision instead of a multi-option survey to the principal. The default failure mode for agents is treating ship-work as ask-work (over-surveying) or treating propose-work as ship-work (rushing irreversible changes). This skill prevents both.
---

# Envelope

Sort an incoming request into one of three envelopes — **A: Ship**, **B: Ask one focused question**, **C: Propose first** — and act accordingly.

## When to use

- The principal gives a directive and you're tempted to respond with multiple clarifying questions
- The work involves a fork in the road and you're tempted to present multiple options
- Before posting any "should I…?" question
- Triggered by Caddy on prompts like: "should I", "before I start", "is this clear", "is this OK", "couple options", "two paths", "ambiguous", "not sure if you want", "want me to", "ship vs ask", "decision tree", "fork in the road"

## The decision tree (run top-to-bottom)

```
1. Is the request unambiguous?
   YES → step 2
   NO  → can I resolve the ambiguity by reading code/data/docs?
         YES → resolve, then step 2
         NO  → ENVELOPE B: ask exactly one focused question with options spelled out

2. Is the change reversible?
   YES → step 3
   NO  → is the irreversibility expensive? (data loss, schema migration, deploy, broken contract)
         YES → ENVELOPE C: propose first, wait for sign-off
         NO  → step 3

3. Is the change bounded to a known surface area?
   YES → step 4
   NO  → can I re-scope to a bounded version?
         YES → propose the bounded version + ship that
         NO  → ENVELOPE C: propose first

4. Do I have full context to make the change correctly?
   YES → ENVELOPE A: SHIP
   NO  → load missing context (search/read/query); re-evaluate

5. After shipping: did verification pass?
   YES → declare done with summary
   NO  → loop back to step 4 (more context, different approach)
```

## Envelope rules

### Envelope A — Ship it
- Clear request, known surface, reversible, low rollback cost
- **Action: just do it.** Do not ask "should I proceed?" after permission was already given. Asking permission for things you've been authorized to do wastes the principal's attention.

### Envelope B — Ask exactly one focused question
- 2+ reasonable interpretations that produce **meaningfully different outcomes**
- Cannot resolve by reading code/data
- **Action: one surgical question with options spelled out.** Not "what do you want?" — "do you want X or Y? Consequences are A vs B."
- Never ask a question you can answer yourself by reading the code.

### Envelope C — Propose, don't act
- Irreversible OR expensive: data deletion, schema migration, dependency swap, broad refactor, deploy
- Implications across many files/systems
- Genuinely a product decision dressed up as technical
- **Action: describe what you'd do, what it costs, what it breaks, what you'd recommend.** Wait for the call.

## Escalation triggers (auto-bump from A → C)

- Change spans more than ~5 files → consider proposing first
- Touches a public API or shared type → consider proposing first
- Schema migration required → propose first by default
- Deleting/modifying user data → propose first, always
- Production-only code paths → propose first
- New paid dependency → mention it, ship if small

## The bias

- **Cheap and reversible** → ship.
- **Cheap and ambiguous** → one focused question.
- **Expensive or irreversible** → propose first.

## Output format

When triggered, output a one-line classification before acting:

```
[ENVELOPE A — SHIPPING] {1-line description}
```
or
```
[ENVELOPE B — ONE QUESTION] {the question, with X-or-Y options + consequences}
```
or
```
[ENVELOPE C — PROPOSAL] {what I'd do, cost, blast radius, recommendation}
```

Then execute. No second-line "is this OK?" — that defeats the entire purpose.

## Anti-patterns this prevents

- Multi-section essays asking 5 alignment questions when the spec is the answer
- "Two paths, A or B?" surveys when you can pick one and defend it
- Asking permission for an obvious, reversible edit
- Shipping irreversible work without proposing first
- Posting status updates as deliverables ("I'm reading the docs now…" — silence until state change)
