---
name: snaap-release
description: >
  Use before opening any PR or deploying. The pre-flight checklist — build, budget, Lighthouse,
  axe, curl raw-HTML checks, sitemap/robots, zero 404s, migration dry-run and rollback note.
---
# Release pre-flight

Run before every PR / deploy. "Done" means all of these pass:

- `npm run build` passes (build on Windows — the Linux SWC binary can't be fetched in a container).
- Initial JS ≤ 200KB gzipped; note before/after.
- Lighthouse mobile run; axe clean on every touched UI surface.
- SEO work verified with **curl against raw HTML** (paste the command + output). `sitemap.xml` and
  `robots.txt` still return 200.
- Zero internal 404s; no internal link lands on a zero-result listing.
- No retired WhatsApp number, no "free delivery" claim, no fake ratings/stock, no committed secret:

  ```
  git grep -n "wa\.me/"                 # only src/constants/business.js
  git grep -ni "free delivery"          # nothing
  # and confirm no retired WhatsApp number appears in src/ (the two old values are kept out of the repo by policy)
  ```

- DB migrations: dry-run first, reversible, references checked, rollback note in the PR.
- Conventional commit, one concern per PR, on a `feat/pX-...` branch — never push to `main`.
- End with: what changed, what's still broken, what needs the owner's decision.
