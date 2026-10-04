---
name: jade-recipe-dummy
description: >-
  E2E test recipe. Appends // E2E TEST comment to matched line.
  Returns success immediately. Invoked by jade-core-rule-dispatcher.
arguments: [file_path, line]
---
# jade-recipe-dummy — E2E Test Recipe

Appends `// E2E TEST` comment to the flagged line. Does not alter
Java semantics. Used to validate the full pipeline end-to-end.
