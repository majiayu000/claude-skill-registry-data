---
name: creating-plans
description: Creates summary for human review - and comprehensive implementation plan for LLM, complete code examples, and verification steps
---

# Creating Plans

## Overview

Write plans optimized for human review:

## Plan Document Structure

A plan has two sections:

### Plan summary for human review at the top

The summary tells a story the reviewer can follow in <150 lines. Not a file list - show the *shape* of the change to review the plan and spot issues early.

**Structure:**
1. **Requirements** - Brief restatement with enough precision to be clear
2. **How it works today** - Diagram showing current flow (builds shared context)
3. **The change** - Diagram showing new flow + code in context. Present code changes outside-in, showing new code **in context** with surrounding existing code:

1. **Usage & Signature** - reveal the API shape, types, and ergonomics
2. **Flow** - show where new code lands relative to existing code

Example - adding a `formatCurrency` utility:

```ts
// Usage
function formatCurrency(cents: number, currency: 'USD' | 'EUR' | 'GBP'): string

formatCurrency(1999, 'USD');  // "$19.99"
formatCurrency(1999, 'EUR');  // "€19.99"

// Flow - where it lands in existing code
// src/components/ProductCard.tsx
export function ProductCard({ product }: Props) {
  const store = useStore();                          // existing
  const price = formatCurrency(product.cents, ...);  // ← new

  return (
    <div className="card">                           {/* existing */}
      <span className="price">{price}</span>         {/* ← new */}
      <span className="name">{product.name}</span>   {/* existing */}
    </div>
  );
}
```

The reviewer should see what already exists around the new code, not just the new code in isolation.

4. **Verification** - Always include `local-ci.sh` + manual testing steps
5. **Testing** - Match existing test patterns. List test files to add/update, then key cases to cover (edge cases, error states, happy path). Give confidence the plan has testing covered.

**Guidelines:**
- Show code in context - what's above and below, not floating snippets
- Only mention alternatives if they were genuinely considered and could have gone either way
- Don't pad with fake tradeoffs or invented alternatives
- Don't list files separately if the diagram already shows them
- Don't condescend ("Clarified with user:") - just state the decisions

### Plan implementation details

```
## Plan implementation instructions

- Which files will be affected and how.
- Include all files to change with line numbers:
- The code that will go in that file
- Each step is one bite sized action (2-3 minutes)
- Structure your plan as a check list using [ ]
- Complete code in plan (not "add validation")

Document everything they need to know: which files to touch for each task, code, testing, docs they might need to check, how to test it. Give them the whole plan as bite-sized tasks. DRY. YAGNI. TDD.

```


## Making your plan

**Announce at start:** "I'm using the creating-plans skill to create the implementation plan."

**Save plans to:** `scratch/plans/YYYY-MM-DD-plan-<feature-name>.md`  (separate from research or design docs)

You must surface any genuine / important questions you have using multichoice questions.

- Prefer multiple choice questions when possible, but open-ended is fine too
- Only one question per message - if a topic needs more exploration, break it into multiple questions

Start by creating a planning todo list:

Collect context information:

- [ ] Read any provided documents / context & Explore the relevant code
- [ ] Search for similar patterns in the codebase
- [ ] If you have questions or are unsure about anything please ask for clarification until everything is resolved

Draft the plan and iterate:

- [ ] Draft a full plan (summary + implementation) and write it to disk
- [ ] Read the plan again and review it based on the plan criteria laid out here. Focus on how easy it is for human to digest and review the plan so they can give feedback on any potential issues early on.
- [ ] Review this plan and the code within it. Use the feedback to improve the plan. If necessary go back to the previous todo and continue iterating on the plan.

- [ ] Reply to user with the plan summary section and the implement command

**End with:** The plan summary directly in the chat, always tell the user the exact command to run:
`$implementing-plans scratch/plans/YYYY-MM-DD-<feature-name>.md`
