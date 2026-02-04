---
name: log-file-use
description: When a mode needs to read, create, or write (log progress) to a log file.
---

# Log file use instructions

## Comstants
**Logging format**:
- `date + time; action summary` (semicolon separated).
    - Ex: `"2026-02-14 07:23; Approved to begin"`.
    - Ex: `"2026-02-14 07:25; Task completed: Added update_query() to utils_sql.py, refactored utils_sql.py, junk.py"`.
**Plans folder**: `.roo/docs/plans/`

## Initialization tasks

Do in order:

### 1 Determine **User query**:
Determine `user_query` value from current context or other input.
- If still not known: consult user.

### 2 Determine **Plan name**:
Do in order:
a) Determine `short plan name` value from current context, current task, or other input.
- If still not known: consult user. 
b) Create `short_2_word_description` of current task based on current context.
c) `short plan name`: `yymmdd_{short_2_word_description}`.

### 3 Determine **Log file name and path**:
- `log file`: `{plans folder}_[short plan name]_log.md`.

## Log file use instructions

### Reading a log file
- Use the `read_file` tool to read `log file`.

### Creating a log file
- Use the `write_to_file` tool to create fresh (or modify existing) `log file` in the `{plans folder}`.

### Writing to a log file
- Use the `apply_diff` tool to modify existing `log file` in the `{plans folder}`.
