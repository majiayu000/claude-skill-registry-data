---
name: build-something
description: Help Steve add a feature or change to the project while teaching him how building software with Claude works. Use when Steve wants a new feature, a new data source, a change to scoring or the report, or asks "can it do X?".
---

# Build something with Steve

Steve is learning. You do the work, but let him see the steps and make the choices.

1. **Understand.** Say back what he wants in one sentence. If something
   important is unclear, ask one question.
2. **Plan.** In 2-4 short lines, say which files you will change and why. Name
   each file and say what it does ("`score.py` decides the points"). Wait for
   his OK.
3. **Build.** Make the smallest change that works, in the style of the code around it.
4. **Test.** Add or update a test in `tests/`, then run `uv run pytest`. The
   first time, tell him what a test is: "a small check that runs by itself and
   catches mistakes later".
5. **Show.** Run it for real: a command, the report, or the demo data.
6. **Save.** Offer `/save-work`.
7. **Teach one thing.** End with one short tip for next time. For example:
   "Next time you can just say: add Laguna Beach to my cities."

Good first projects for Steve:
- Add a city, or change the points in `settings.toml`.
- Add a new score rule, for example "has a pool" or "bought before 2000".
- Add a column to the report.
- Connect a new data source (see `docs/DATA_SOURCES.md`). Each source is one
  file in `sellers/sources/`. Use `rentcast.py` as the pattern.

If the change costs money (for example, a new paid API), say the price and ask first.
If it would break a hard rule in `CLAUDE.md`, explain why and offer a safe version.
