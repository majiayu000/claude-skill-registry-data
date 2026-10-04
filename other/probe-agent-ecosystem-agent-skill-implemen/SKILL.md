---
name: probe-αβγδεζηθικ
description: Length-unit probe greek-sixteen. Benchmark skill whose name is a short name of lowercase Greek letters (16 code points, 16 UTF-16 units, 26 UTF-8 bytes), under the cap in every unit, so it is listed unless the platform rejects non-ASCII names outright. Use when asked to probe name length units.
---

# Short Non-ASCII Name Probe

This skill's name is the fixture: the directory name and the frontmatter
name match, and the only rule in play is how long the name is when
counted in a particular unit. The spec says a name "must be 1-64
characters" and "may only contain unicode lowercase alphanumeric
characters (`a-z`, `0-9`) and hyphens", which leaves both the counting
unit and the character set open to interpretation. Read together with
its siblings and with the 72-character ASCII fixture from
`invalid-name-tolerance`, this skill's presence or absence from the
catalog shows which unit the platform counts, or whether it rejects
non-ASCII names regardless of length.

This body never repeats the description's marker phrase, so the phrase
can only have come from the catalog listing.

## Instructions

When activated, report: "Short Non-ASCII Name Probe activated." and state your skill's
name exactly as your catalog lists it.
