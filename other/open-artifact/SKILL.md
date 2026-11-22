---
name: open-artifact
description: Make a new artifact of one Open Artifact type (design, slides, whiteboard, sheets, data, docs, motion, design-system, …) with the Artifact tool. The person types `/open-artifact <type> <what to make>`.
---

# Make an artifact: `/open-artifact <type> <what to make>`

The person started this message with `/open-artifact`. The first word after it is the **type id** of the artifact to make
(`design`, `slides`, `whiteboard`, `sheets`, `data`, `docs`, `motion`, `design-system`, …); the rest of the message is what they want in it.

1. Take the type id from the first word. If there is none, or it is not one of the installed types listed below, ask
   which type they want (list the installed ones) and stop until they answer. Words like "deck" or "presentation"
   mean `slides`; "canvas", "UI" or "mockup" mean `design`; "board" means `whiteboard`; "dashboard", "report",
   "metrics" or "chart" mean `data`; "spreadsheet", "workbook" or "budget" mean `sheets`; "doc", "document", "write-up", "proposal", "memo" or "notes" mean `docs`; "animation", "video", "motion graphics" or "explainer video" mean `motion`; "brand", "tokens" or "design system" mean `design-system`.
2. If the request needs details only the person has (the topic, the content, the brand) and the message gives none,
   ask in one short question. Otherwise go ahead.
3. Create it: `Artifact {action: "publish", type_url: "open-artifact://type/<type id>", title: "<a short title>", open: "after_first_write"}`.
   Do not call `quickstart` first: the type is already chosen.
4. The result carries the artifact's `url`, its `root` folder and the type's own instructions. Follow those
   instructions exactly: they say which files to write into `root`, how to check them, and how the page opens.
5. When it is done, tell the person in a sentence or two what you made. The page shows in the session's Browser, where
   they can comment on it (their comments come back to you), share it and export it.

To share it, call `Artifact {action: "open", url, panel: "share"}`, which opens its share panel for the person; never
make links yourself.
