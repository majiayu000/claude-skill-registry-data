---
name: docs-ship-check
description: The pre-share gate for a Superhuman Docs (Coda) document. Before a doc reaches a reader, run the QA checklist, choose the interaction mode, set the publish frame, and confirm the share. Catches the broken formula, the wall of text, the orphaned bullet, the missing cover, the wrong audience. Trigger on "is this doc ready to share", "publish this doc", "QA this doc", "ship-check", "final pass before I send", "which interaction mode", or any moment a Superhuman Doc is about to leave the building.
---

# Ship-check a Superhuman Doc

The last gate before a doc reaches a reader. A great draft and a shipped product differ mostly in the frame and the finish, not the words. Run this after the build (superhuman-docs-builder) and the design pass (superhuman-docs-design).

## The QA checklist (pass / warn / block)
- **Structure:** every section, table, and view renders; no TBD or placeholder text left.
- **Formulas:** run formula_execute on every live formula; confirm counts, percents, and rollups compute.
- **Hierarchy:** one focal point per screen; the first screen is not a wall of text; the outline reads sensibly.
- **Color budget:** one accent, rationed; semantic color only for status; pale fills; no colored body text.
- **Anti-bullet:** no orphaned bullet lists carrying attributes; comparisons are tables, arguments are cards.
- **Links:** every external link resolves; every claim has a source.
- **Header:** cover set and crop-tested; subtitle written (it is the unfurl); byline on.
- **Render:** open the doc in Chrome from the owning account and look at it; fix what the MCP can, list the UI items.

## Choose the interaction mode
- **View:** articles, reports, manuals. Controls are read-only. The default for a finished artifact.
- **Play:** calculators, quizzes, interactive demos. Readers can click; changes are not saved.
- **Edit:** voting, brainstorms, add-a-row. Contributions are saved.

## Set the publish frame
Cover, subtitle, and byline on. Organize with nested pages; collapse the extraneous. Turn on discoverability with a category and audience only for public docs; leave it off for shared-but-unlisted. Clean the URL, or a custom domain for brand-facing docs. Allow copy only for templates. Preview, then share. The live doc is the deliverable; never print or PDF it.

## Confirm the share
State the recipient, the mode, the access level, and the deadline before you send. For a doc that must reach someone by a date, share by link at least 24 hours ahead and confirm the link opens for them.

## Make it yours
Fork it. Add your org's QA items and publish defaults. The point is that no doc reaches a reader without the gate. Built by an operator. Customize it, break it, make it better.
