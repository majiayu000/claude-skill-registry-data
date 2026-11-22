---
name: "milestone-tagging"
description: "How EISS's GitHub milestones are structured: the version-tied SemVer set and its backlog catch-all, why conference-phase milestones were tried and reverted, due dates tracking the roadmap timeline, and when to create a new one. Use when creating or re-milestoning an issue or PR, when the roadmap shifts a planned release, or when a milestone title or due date is in question."
---

# Milestone tagging

The always-loaded rule is CLAUDE.md §10: every open issue and every
pull request belongs to exactly one milestone, set in the `gh` command
that creates it, and when the answer is not obvious you ask rather than
guess. This is the rest, which is consulted rather than carried.

### The milestone set (version-tied, SemVer)

EISS uses **version-numbered milestones** matching the planned
releases on the roadmap, plus a single catch-all for uncommitted
work. This mirrors the sister NetSec site. EISS switched from
thematic milestones to this scheme after v2.24.0, so the milestone
now answers "which release is this for?" rather than "what kind of
work is this?". The set:

- **One milestone per planned release** (`v2.25.0`, `v2.26.0`,
  `v2.27.0`, …), created from the version-tagged rows of the roadmap
  (the *At a glance* timeline in [`docs/roadmap-2026.md`](docs/roadmap-2026.md),
  surfaced publicly on `/roadmap.html`). A patch milestone
  (`v2.24.1`) exists only when a reactive patch is anticipated, such
  as the post-conference cut.
- **`Backlog — Under watch`**: items waiting on an external trigger
  (Indico write-API access, NetSec coordination, source research) or
  with no committed release. Mirrors the *Under watch* section of the
  roadmap.

**Every milestone title is a SemVer version, or the backlog.** No
sentence-titled milestones. A conference cycle has phases with their own
deadlines (*save the date*, *call for papers*, *selection and
notifications*, *programme and logistics*, *conference*), and those are
real, but they are named in the roadmap and in the issues rather than
minted as milestones. The prep work rides whichever release is open when
its deadline falls, which is what NetSec does and says in its own §10.

This was tried the other way in August 2026 and reverted the same month:
five `ESSC 2027: <phase>` milestones existed briefly, and the reason
against them is that they answer a different question from the rest of
the set. A milestone here answers "which release is this for?", and a
board where some rows answer that and others answer "which phase of a
conference is this?" cannot be read as one queue. The phase rows live in
[`docs/roadmap-2026.md`](docs/roadmap-2026.md) beside the release
timeline, which is where a date owned by somebody else belongs.

Due dates on the version milestones come from the roadmap timeline.
When the roadmap shifts a planned release, **bump the milestone's due
date in the same commit that updates the roadmap row**: they are two
views of one schedule. A conference deadline that lands between releases
moves the nearest release's date or waits for it, and the roadmap says
which.

Create a new version milestone when the roadmap gains a release row.
Don't pre-create far-future majors.
