---
name: proof-of-done-lite
description: Use before saying work is done, fixed, or complete after changing code. Run the project's checks, show their results, and end with a short verification receipt.
---

# Proof of Done (lite)

This is the instructions-only version. For enforcement that blocks the agent until
checks pass, install the `proof-of-done` plugin from the claude-code-skills marketplace.

1. After your last code change, run the checks that prove it works: typecheck, lint,
   tests and build.
2. Run each check plainly. Do not pipe it into `tail`, `head` or `Select-Object`, and
   do not add `|| true`. A hidden exit code is not proof.
3. If a check fails, fix it and run it again. If you cannot fix it, say so plainly.
4. End your message with a receipt:

   Verified:
   - npm run lint ✓
   - npm test ✓ (42 passed)

5. If no check can run, end with one line that states why:

   Verification: skipped — <the specific reason>

---

Made by **Wageesha Tripathi** · [LinkedIn](https://www.linkedin.com/in/wst2002/) · [Email](mailto:tripathiwageesha2002@gmail.com) · [More skills](https://github.com/WST2002/claude-code-skills)
