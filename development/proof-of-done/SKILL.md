---
name: proof-of-done
description: Use before saying work is done, fixed, or complete after changing code. Run the project's checks, show their results, and end with a short verification receipt.
---

# Proof of Done

Never say work is finished because the code looks right. Finish with evidence.

1. After your last code change, run the checks that prove it works: the project's
   typecheck, lint, tests and build, or the commands listed in
   `.claude/proof-of-done.json`.
2. Run each check plainly. Do not pipe it into `tail`, `head` or `Select-Object`,
   and do not add `|| true`. A hidden exit code is not proof.
3. If a check fails, fix it and run it again. If you cannot fix it, say so plainly.
4. End your message with a receipt:

   Verified:
   - npm run lint ✓
   - npm test ✓ (42 passed)

5. If no check can run (no test runner, missing credentials, hardware needed), end
   with one line that states why:

   Verification: skipped — <the specific reason>

Use `/proof` to see what has been recorded in this session.

---

Made by **Wageesha Tripathi** · [LinkedIn](https://www.linkedin.com/in/wst2002/) · [Email](mailto:tripathiwageesha2002@gmail.com) · [More skills](https://github.com/WST2002/claude-code-skills)
