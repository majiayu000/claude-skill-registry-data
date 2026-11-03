---
name: issue
description: Sends a report of a celis fault to the celis team. Use when the celis command, its hooks or the plugin fails, or when the person asks to report a celis problem.
---

You send a report of a celis fault, only the way the person chooses.

1. Write what went wrong in the person's words: what they did, what they expected, and what happened.
   Copy each error text exactly.
2. Ask the person whether to add the trail where the fault occurred. A trail holds their prompts, proofs
   and file names. Add its id only when they agree.
3. Run `celis issue [<id>]... -- "<what went wrong>"`. When the `celis` command is missing, write the
   OS, the agent and the error yourself.
4. Show the full report to the person. Tell them that it can hold paths, commands and words from their
   work, and remove each part they name.
5. Ask the person how to send it:
   - a public GitHub issue: write the report to a file, and run
     `gh issue create -R celishq/trails --title "<the heading>" --body-file <the file>`;
   - in private: write the report to a file, and give the person its path to send themselves.
6. Send nothing before the person says yes. Then give them the issue's URL or the file's path.
