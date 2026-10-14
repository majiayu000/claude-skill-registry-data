---
name: implement
description: "Implement a prepared spec or set of tickets. Use when the user asks to implement one, or when an orchestrating skill runs it as its implementation subloop."
---

Implement the work described by the user in the spec or tickets.

Write against the unified code standard in
[`../codebase-design/STANDARD.md`](../codebase-design/STANDARD.md) as you go;
independent review happens outside this session. Follow this sequence:

1. Use `/tdd`, working in red → green slices. Choose the seams under test per
   its seam doctrine — prefer seams the spec establishes — and note them.
2. Run focused typechecking and tests for the touched behavior.
3. Run the full typecheck and test suite once at the end.
4. Commit the verified work to the current branch. Declare the tested seams in
   the PR description (or the final report when no PR exists) so reviewers can
   validate the seam choice.

Do not commit while accepted review findings or failing checks remain.
