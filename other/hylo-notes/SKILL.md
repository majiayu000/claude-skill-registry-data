---
name: hylo-notes
description: "Guide for working with Hylo, an AI-native personal note-taking system. Use this skill whenever the user wants to search, find, read, write, save, create, modify, delete, or capture notes — including journal entries, research notes, quick thoughts, knowledge retrieval, or any note-taking task. Trigger when the user says things like 'save this as a note', 'find my notes about X', 'create a note', 'look up my notes on X', 'read my note about Y', 'delete a note', 'quick note', 'short note', 'what do I know about X', or any variation of managing notes in Hylo."
---

# Hylo Notes — Router

## Environment check

```bash
hylo --help
```

If `hylo` is not found, inform the user and stop.

---

## Identify intent → load sub-skill

| Scenario          | Trigger signals                                                                                        | Sub-skill       |
| ----------------- | ------------------------------------------------------------------------------------------------------ | --------------- |
| **Regular notes** | create / read / modify / delete / list / search notes; journal entries; research notes; markdown files | @notes-crud.md  |
| **Short notes**   | quick capture, fleeting thought, short note, daily log, "jot down"                                     | @short-notes.md |
| **Knowledge**     | "what do I know about", knowledge base, compiled knowledge, index notes                                | @knowledge.md   |

Load the matching sub-skill. If the request spans multiple scenarios, handle them sequentially.
