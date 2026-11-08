---
name: simplify
description: review the current changes and simplify the code where possible.
disable-model-invocation: true
---

Think from first principles about what we're trying to achieve here. Interrogate what you built before calling it done:

1. is anything here unnecessary, overly complicated, or based on weak assumptions? Challenge them.
2. What can be deleted entirely?
3. What can be simplified now that unnecessary pieces are gone?

Then make the changes. Prefer deleting over simplifying, simplifying over optimizing, and optimizing over automating.

It might be done too - you dont HAVE to go and make changes. if its good, leave it alone