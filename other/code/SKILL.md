---
description: Review code through the lens of a senior engineer
---

# Code Coaching

Review "$ARGUMENTS" through the lens of a senior software engineer. Provide mentorship feedback on code quality, architecture patterns, security, performance, and testing.

## Prerequisites

None — this is a utility skill that can run anytime.

## Process

1. **Read the target:**
   - Read the source code files specified in "$ARGUMENTS"
   - If it's a directory, read the key files
   - Understand the context: what does this code do?

2. **Read reference material:**
   - Read `plugins/coaching/shared/code-principles.md` for engineering principles
   - Read `plugins/coaching/shared/feedback-format.md` for output structure

3. **Evaluate against engineering principles:**
   - **SOLID:** Single responsibility, open/closed, Liskov, interface segregation, dependency inversion
   - **Clean code:** Naming clarity, function size, abstraction levels, self-documenting code
   - **DRY/YAGNI/KISS:** Appropriate abstraction level, no premature optimization
   - **Security:** Input validation, injection prevention, secrets management, auth patterns
   - **Performance:** N+1 queries, appropriate data structures, caching, lazy loading
   - **Database:** Normalization, indexing, query patterns, transactions
   - **Testing:** Coverage, behavior vs. implementation testing, test quality
   - **Error handling:** Appropriate error types, no swallowed errors, graceful degradation

4. **Write the coaching report** to `.metapowers/coaching/$ARGUMENTS/code-review.md` following the feedback format.

## Output

The code coaching report written to `.metapowers/coaching/$ARGUMENTS/code-review.md`. Present the score and top 3 suggestions to the user.
