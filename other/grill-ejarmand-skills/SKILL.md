---
name: grill
description: Grill the user relentlessly about a plan, decision, or idea. Use when the user wants to stress-test their thinking, or uses any 'grill' trigger phrases.
---

Interview me relentlessly about every aspect of this until we reach a shared understanding.

Move through the decision tree in rounds, resolving dependencies between decisions.


```
**Q1** - **<question title>**: <question body, might be multiple paragraphs, including multiple choices>

<your recommended answer>
```

Rules of thumb:

- Questions in the same round don't depend on each other
- Present questions in a way that the user has the information to avoid decision anergy (e.g. two reasonable answers locking in an inelegant spec)
- Questions should address exactly one concern
- If a *fact* can be found by exploring the environment (filesystem, tools, etc.), look it up rather than asking me.
- Do not act on it until I confirm we have reached a shared understanding.

# user shorthands
y - yes/agree
n - no/disagree
dc - don't care, I think this decision isn't super important
