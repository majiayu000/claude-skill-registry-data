---
name: replica
description: >-
  Clean-room app cloning pipeline in eleven parts: reverse-engineer an app into a
  recon map, plan the stack and schema, rebuild the design system, build screens,
  add auth and payments, test the flows, score parity against the original, mine
  what its users hate, rebrand, then run the launch assets and deploy. Use when cloning or
  substantially re-implementing another app's features and flows — features and
  flows only, never its code, assets, logo or copy. One contract; the parts under
  parts/ carry the method and the tools.
---

# replica — clean-room cloning pipeline

> Upstream: [Jakeschincariol/replica-skill](https://github.com/Jakeschincariol/replica-skill),
> MIT, commit `77c9436`, installed 2026-10-22. License text: `LICENSE.txt`.
> Tools are standard-library Python, invoked as `python`. All eleven skills and their tools were verified at install
> time against the upstream test suite (57 tests, green); that suite asserts the
> upstream repository layout and is not shipped here.

## Choosing a part

| Stage | Part | It writes |
|---|---|---|
| 1. Reverse-engineer the target: screens, flows, components, inferred data model, feature matrix | `parts/replica-recon/` | `replica/recon.md`, `replica/features.csv` |
| 2. Stack, database schema, routes, build order | `parts/replica-architect/` | `replica/architecture.md` |
| 3. Design system as tokens and component specs, with original assets | `parts/replica-design/` | `replica/design/tokens.json` |
| 4. Rebuild screen by screen from the recon map | `parts/replica-build/` | the app itself |
| 5. Auth, migrations, payments, email, jobs, integrations | `parts/replica-backend/` | backend code + security checklist |
| 6. Test every flow, log bugs by severity | `parts/replica-test/` | `replica/test-plan.md`, `replica/bugs.md` |
| 7. Score parity and diff screenshots | `parts/replica-diff/` | parity score, missing list, `diff.png` |
| 8. Read real reviews, rank complaints, pick a positioning angle | `parts/replica-entrepreneur/` | `replica/reviews.csv`, fix plan |
| 9. New name, palette, logo brief, voice, sweep the old name out | `parts/replica-brand/` | brand kit, sweep report |
| 10. Landing page, pricing, store listing | `parts/replica-launch/` | `replica/launch/` |
| 11. Preflight, production, DNS, ship | `parts/replica-deploy/` | `replica/deploy/` |

## Order

`recon → architect → design → build → backend → test → diff → entrepreneur → brand → launch → deploy`

Each part reads the file the previous one wrote from `replica/` in the project root.
Any part also runs on its own: `replica-entrepreneur` on an app you have not started
is a cheap way to decide whether cloning it is worth it.

## Tools

```bash
python skills/replica/parts/replica-diff/imgdiff.py original.png clone.png --out diff.png
python skills/replica/parts/replica-diff/parity.py replica/features.csv
python skills/replica/parts/replica-entrepreneur/reviews.py replica/reviews.csv
python skills/replica/parts/replica-design/contrast.py replica/design/tokens.json
python skills/replica/parts/replica-brand/sweep.py . --avoid "Original App"
python skills/replica/parts/replica-launch/listing.py replica/launch/listing.json
```

`imgdiff.py` compares edge maps, so a rebrand's colours do not count as a diff; it
reports which regions moved, in the original's pixels. `parity.py` weights
must/should/could, counts partials as half, and refuses to call a clone shippable
while a must-have is missing. `sweep.py` blocks a deploy that still carries the
original's name, domain or colours — including inside identifiers.

## Rules

- **Features and flows, clean-room.** Never the target's source, proprietary assets,
  logo, trademark, copy or private APIs. Read the artifact; write everything fresh.
- **Only what you are allowed to read**: public pages, store listings, help docs and
  the owner's own account. No scraping behind a login, no paywalls, no one else's
  account. If the account's terms forbid building a competitor, stay on public sources.
- **Rebrand before launch.** New name, palette, logo, words; `sweep.py` must be clean
  before `replica-deploy` ships.
- **Numbers, not vibes.** Parity comes from `parity.py`, layout from `imgdiff.py`;
  reviews only from rows with links, and thin themes are labelled thin.
- **Sizing first.** `replica-recon` states honestly how big the clone is before the
  build starts; open-ended scope here is a fork worth `ask_questions`.
- **In this kit**, the visual and device sides stay with the existing skills:
  `reverse-engineering` for APK/decompilation work, `browser` for phone and panel
  capture, `design` for tokens, `ship` for deploys.

## Related

`reverse-engineering` (artifact analysis), `browser` (capture on device and panel),
`design` (design systems), `review` (critique), `ship` (release mechanics).
