---
name: firm-moscow-scope
description: Sorts every item from the brief and the call into must, should, could or won't for this engagement, with the won't list written out with reasons, the effort split on your own estimates, what moves if budget or time changes, and items the client could do well with their own AI named as such. Use for "run firm-moscow-scope", "MoSCoW this scope", "the brief asks for everything", "what fits inside this fee", "cut the scope to the budget", "write the won't list", "must should could won't for this engagement", part of the Claude for Consultants · Team in Claude Pack by Polar Bear.
---

# MoSCoW Scope

## When To Use
The brief lists far more workstreams than any budget would cover, because a model was asked to be thorough. If you price all of them you lose; if you quietly drop most you will be reminded of each one in month two. Run this after the call, to decide in writing what this engagement guarantees, what it attempts and what it will not do this time.

## When Not To Use
Before the call, to find what the brief left unsaid, use AI-Written Brief Review. For three versions of different size, use Good-Better-Best Options. Once the scope is agreed, Statement of Work makes it contract-ready.

## Inputs
- The client's brief in full, and your call record
- What the client said matters most, their budget and their deadline if given
- Your effort estimate per item, in whatever unit you use
If you have none of this, I start from the brief by itself, write [your estimate] for effort and mark the scope as a first draft.

## Approach
MoSCoW prioritisation comes from DSDM, now maintained by the Agile Business Consortium (agilebusiness.org): Must have, Should have, Could have, Won't have this time. Its strength is the last category. Without a written won't list everything drifts into must, and the scope you priced becomes the scope the client remembers. The method keeps the musts well under the full effort so that there is room for surprises; you set the share you will allow.

## Workflow
1. Ask, in one go: which single outcome would make this engagement worth it if nothing else were done? What budget or time limit are you fitting? What share of total effort will you allow the musts to take?
2. List every item the brief and the call asked for, one per line, numbered, with its source. Nothing from the brief may vanish; this list is what you reconcile against at the end.
3. Sort each item. Must: without it the result is unusable and there is no workaround. Should: important, with a workaround. Could: wanted, first to go. Won't this time: written out with its reason. Test each must with "if only this were missing, would we still call it delivered?" If yes, it is a should.
4. Put your effort against each item and display the split. If the musts exceed the share you set, the scope is unsafe: move items down or raise the budget with the client. I only add up your estimates; I never supply one.
5. Give each won't an honest reason: beyond the budget, belongs in a later phase, not needed for the outcome, or something the client can do themselves. Where their own AI would handle an item well, say exactly that and leave it with them.
6. Plan the moves in advance: if budget or time shrinks, which shoulds become coulds and which coulds go; if it grows, which won'ts return first. Then check that the client's top priority sits in must. If it does not, stop and rethink.

## Output Format
```markdown
# Scope by MoSCoW
Outcome this engagement guarantees: [one line, their words where you have them]
| # | Item | Source (brief / call) | Category | Effort [your unit] | Reason |
|---|---|---|---|---|---|
| 1 | [item] | [source] | [must / should / could / won't] | [your estimate] | [why this category] |
## Effort split
| Category | Effort | Share | Your limit |
|---|---|---|---|
| Must | [sum] | [share] | [your limit] |
| Should · Could | [sum] | [share] | [n/a] |
## Won't this time
- [Item]: [reason; who could do it, or when; "the client's own AI can do this well" where true]
## If budget or time changes
| Change | Items that move | From | To |
|---|---|---|---|
| [less budget / more time] | [items] | [category] | [category] |
## Decision
[Your name] confirms the scope and the won't list by [date]; [client role] agrees both before the statement of work is drafted.
```

## Done When
- Every item from the brief and the call sits in exactly one category, with its source
- Each won't has a written reason
- The must share is within your limit, or the gap is raised with the client
- The moves for a budget or time change are written before work starts

## Quality Bar
- Musts are tested one by one; "they asked for it" is not a reason
- "Out of scope" alone is never a reason; say why
- Items the client's own AI could do well are named as such, not kept to pad the fee
- Effort figures are yours; shares are calculated from them
- Nothing from the brief disappears silently; I invent no estimate, and you decide the scope and put it to the client yourself.

## Next
Run firm-consulting-proposal (Consulting Proposal) to write the proposal around this scope.

## About the makers

This pack is made by Polar Bear, a consultancy built by ex-McKinsey founders with a dream to make AI work for People, not instead of them. We help our clients build people systems and AI-first ways of working, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
