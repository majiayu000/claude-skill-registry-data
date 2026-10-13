---
name: local-test-render
description: How to render MythiStone pages locally against a throwaway seeded MySQL. Use whenever you change a templates/*.html, a backend_scripts/generate*.py, pageGeneration.py/aggregateData.py/commonUtils.py, or page CSS/JS, and must verify the rendered page before handing it back.
kind: workflow
files:
  - templates/*
  - backend_scripts/generate*.py
  - backend_scripts/pageGeneration.py
  - backend_scripts/aggregateData.py
  - backend_scripts/commonUtils.py
  - assets/js/*
  - assets/css/*
  - backend_scripts/localDev/*
---

# Local test render workflow

Never hand back page work that was only reasoned about. Render it against the seeder in
`backend_scripts/localDev/` (options and coverage: `backend_scripts/localDev/README.md`).

1. **Seed:** `python backend_scripts/localDev/seed_test_db.py`. It needs Docker Desktop, starts the
   `mythistone-testdb` container and prints `DATABASE_*` exports. Point the generators at those.
2. **Render** the page with its generator and the arguments `buildPages.yml` uses (the page lookup
   of the kb prints them). For one spec add `--spec=252`: a numeric spec id, not a name. A name
   matches nothing and renders no page, without an error.
3. **Serve the repo root** on port 8099 (`.claude/launch.json`), because pages use root-absolute
   `/assets/` paths: `python -m http.server 8099 --bind 127.0.0.1`. Decline the cookie banner, then
   check that the cards you touched render with data and the console has no errors.
4. Optional teardown: `python backend_scripts/localDev/seed_test_db.py --teardown`.

Traps:

- **The Bash tool cannot reach Docker on Windows.** Its `npipe ... cannot find the file` error is
  the Bash docker client, not proof that Docker is down. Run docker and the seeder from the
  PowerShell tool and set the variables with `$env:`. If Docker Desktop really is not running,
  start it and wait until `docker version` reports a server. Never fall back to a hand-built test
  page.
- Every generator needs only the `DATABASE_*` exports. Without keystone.guru credentials a dungeon
  render fails fast on the route thumbnail and renders without the map image, which is what you
  want for seeded routes.

Related: [[add-database-table]], [[gear-and-talent-data-retention]].
