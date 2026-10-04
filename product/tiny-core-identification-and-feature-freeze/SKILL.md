---
name: tiny-core-identification-and-feature-freeze
description: "Isolates the one tiny interaction that is a product's actual superpower, stress-tests whether it's good enough to carry the product on its own, and enforces a 'no more features' veto until that core is obviously, unmistakably good. Use after an MVP direction is chosen and before or during scoping, as a discipline against the 'just one more feature' trap that AI-cheap building makes especially tempting."
---

# Tiny Core Identification and Feature Freeze

## Purpose

Because AI-assisted building makes adding a feature nearly free, the most
common trap for an AI-native product isn't building too little — it's
building too much, one plausible-sounding addition at a time, none of
which fixes the actual reason the product isn't yet great. This skill is
a discipline against that trap: identify the single, tiny interaction
that is the product's real reason to exist, and refuse to add anything
else until that one thing is unmistakably, obviously good.

## Anchored in

Notion product lead Max Schoening's account, supplied by the user from a
source video transcript, of what separates products that actually work:
*"all the great products have something tiny that is a superpower — one
tiny core that is so exceptionally good... one of the biggest pitfalls is
if you get into the loop of 'if I just add one more thing to the
product, it will finally be great' — that never works."* On what the
tiny core actually looked like for several well-known products:
*"GitHub is probably the pull request... at Notion it's the blocks and
the slash commands... Heroku for sure I think it was `git push heroku
master`... Dropbox was the little menu bar icon that was so good at
syncing — and then for years they tried to increase the surface area,
and I kept thinking: no, no, no, push it back."*

## Method

1. **List every feature the product currently has or plans to have** —
   the full surface area, without editing yet.
2. **Isolate the one interaction the product could not exist without.**
   Not the most-used feature, and not the most technically impressive
   one — the single interaction that, if it disappeared, would mean the
   product no longer solves the core problem at all. For reference,
   what this looked like elsewhere: GitHub's pull request, Notion's
   slash-command block conversion, Heroku's single `git push` deploy
   command, Dropbox's sync menu-bar icon. In each case the rest of a
   much larger product grew around this one thing — not the other way
   around.
3. **Stress-test the isolated core with one direct question.** "If this
   product had *only* this one feature and nothing else, would it still
   be genuinely useful and would it still delight the person using it?"
   If the honest answer is no, the candidate isn't actually the core
   yet — go back to step 2, because either the wrong interaction was
   isolated, or the right one hasn't been built well enough yet to
   stand alone.
4. **Enforce a "no more features" veto until the core passes step 3.**
   Once the tiny core is identified, block new feature work — including
   features that individually sound reasonable and low-cost to build —
   until the core interaction is obviously, unmistakably good on its
   own. The rationalization to watch for and explicitly name when it
   shows up: "if I just add this one more thing, it'll finally be
   great." That reasoning is the trap this skill exists to interrupt,
   not a legitimate scoping argument — treat it as a signal the core
   itself still isn't good enough, not as a case for expanding scope.
5. **Once the core passes, expand deliberately and slowly — resurface
   the veto whenever scope creep resumes.** Products that get this
   right (per the source example, Dropbox's years-long resistance to
   growing its surface area beyond the sync icon) treat feature
   expansion as something to actively hold back, not something that
   happens by default once the core works. Revisit this check whenever
   a new feature is proposed for a product whose core hasn't been
   explicitly re-validated recently.

## What this skill does NOT do

- Doesn't replace `../rice-scoring-and-mvp-synthesis/SKILL.md` — that
  skill chooses between multiple candidate solution *directions* before
  a product exists; this skill interrogates one already-chosen product
  (existing or in development) for its irreducible core and blocks
  scope creep afterward. Use RICE scoring first, this skill once a
  direction is being built.
- Doesn't guarantee the isolated interaction actually is the right one
  — step 3's stress test is a judgment call, not a formula; where
  possible validate it against real usage data rather than intuition
  alone.
- Doesn't mean a product should never grow — it delays and disciplines
  growth until the core has earned it, not forbid growth permanently.

## Refinement notes

The source attribution is drawn from a video transcript supplied by the
user and has not been independently cross-verified word-for-word
against a second source; the named product examples (GitHub, Notion,
Heroku, Dropbox) are consistent with each product's well-known public
identity but are the speaker's own characterization, not independently
re-confirmed against those companies' own statements.

## Continue from here

- Before this: `../rice-scoring-and-mvp-synthesis/SKILL.md` — chooses
  the solution direction this skill's core is drawn from.
- Feeds into: `../ai-buildable-prd-writing/SKILL.md` — the isolated
  core and the feature-freeze boundary become the PRD's "Core features"
  and "Out of scope" sections directly.
- Predicting whether the isolated core will actually land with the
  target in-group before investing further:
  `../../../../business-design-frameworks/skills/taste-emulation-heuristic/SKILL.md`
- The pack's shared guardrails: `../../CLAUDE.md`

## References

- `../../CLAUDE.md` — the pack's shared guardrails

---
**Reminder:** frontmatter has only `name` and `description`. Everything
else goes into `skills_index.json` (run `scripts/generate_index.py`).
