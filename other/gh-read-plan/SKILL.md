---
name: gh-read-plan
description: Read the GitHub plan issue given as argument. Use when the user tells you to "read this github plan issue" with the issue as argument.
argument-hint: "[owner/repo#number]"
allowed-tools: Bash
---

Read the GitHub issue in $ARGUMENTS (issue URL or `owner/repo#number`) containing the detailed plan for the work that will be started or continued in this conversation.

When reading the issue, check both the body and comments for content. Steps may be in a separate **Steps** comment (new format) or in the issue body (old format). Check for:

 * a list of steps (with checkboxes) -- in the body or a Steps comment
 * a design section -- in the body or a Design comment
 * a diagram -- in the body or a Diagram comment
 * links to relevant documentation, code, resources, and related issues
 * a list of prerequisites, and if so, ask the user if those have been completed
 * a link to one or more pull requests -- if so, read their diffs to understand what has already been implemented

Try to verify, from the comments and pull requests, which steps have been completed, and which are still pending.

If a durable-memory CLI is configured, query it with the issue's distinctive terms after reading. See the memory tool's own integration doc for mechanics.

Tell the user what you have learned from reading the issue, and ask any clarifying questions you may have about the work to be done.
