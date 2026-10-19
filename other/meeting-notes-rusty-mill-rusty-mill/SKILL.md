---
name: meeting-notes
description: Turn a meeting transcript or raw notes into a structured summary with action items.
tags: [meetings, summary, writing]
source: rusty_mill:crates/apps/nexus/crates/nexus-skills/builtins/meeting-notes.skill.md (converted; template fields became <placeholders>)
---
Produce meeting notes from the supplied content with this shape:

## Attendees
Bullet list. If unknown, write `(not captured)`.

## Topics
One `###` heading per topic. Under each heading, 2-5 bullets of the
key points discussed. Quote short phrases directly when they capture
something non-obvious; paraphrase otherwise.

## Decisions
Numbered list of things that were explicitly decided. If nothing was
decided, omit this section rather than writing "no decisions".

## Action items
Bulleted `- [ ] {owner}: {task} (due: {date})`. Owner must be a named
person — not a team — so accountability is unambiguous. Use `TBD` for
dates that weren't given. Group by owner if the list exceeds six items.

## Open questions
Anything raised but not resolved. These become the seed for next time.
