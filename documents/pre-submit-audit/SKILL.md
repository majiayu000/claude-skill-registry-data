---
name: pre-submit-audit
description: Final audit before submitting the challenge. Checks every deliverable, runs all agents, a clean-clone test and a full-history secrets scan. Use once, in Stage 9.
---

# Pre-submit audit

1. Walk the submission checklist in `docs/brief.md` section 8 and record evidence (command output or URL) for each
   item. An item without evidence is not done.
2. Run all six project agents on the full codebase and the production URL.
3. Clean clone from the remote into a new folder, use `.nvmrc`, follow only the README, and run every command in
   its checks table exactly as written.
4. Scan the full git history for secrets (`gitleaks detect --log-opts="--all"`) and confirm `private/` was never
   committed (`git log --all -- private`).
5. Check every Markdown table renders with the right column count (markdownlint).
6. Confirm the live URL, the public repo and the docs links work from a logged-out browser.
7. List anything the checks wrote to production (test users, events) and confirm it is tagged and excluded.
8. Write the result into `docs/ai-log.md` and report blockers to the owner before anything is submitted.
