---
name: extraction-append
description: >-
  TEST-ONLY. Never shipped in the plugin. Extracts FamilySearch records the
  user names by calling extraction_append once, and returns its summary. Use
  when the message asks to extract, analyze or process FamilySearch records by
  record id or ARK, or to record people a search did not find.
allowed-tools:
  - extraction_append
---

# extraction-append (test-only)

Make exactly one `extraction_append` call, then stop.

- `projectPath`: the working folder.
- `recordIds`: every FamilySearch record id or ARK the message names, in order.
- `questionIds`: the question ids the message names, if any.
- `absentPersons`: each person the message says was expected on one of those records and is not there, with that record's `recordId`.
- For people a search did not find, with no record to extract, send `absences` instead of `recordIds`: `collection`, `place`, `name`, and the nil search's `logEntryId` from the message.

If `extraction_append` is not immediately available, call ToolSearch with `query: "+extraction_append"`.

Reply with each record's `summary`, verbatim, one after another, and nothing else.
