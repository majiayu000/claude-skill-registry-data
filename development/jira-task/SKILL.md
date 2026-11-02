---
name: jira-task
description: Draft a Jira task (title + description) from a work item, change, or conversation context, formatted for manual copy-paste into Jira. Use when the user asks to create/draft/write a Jira task, issue, or ticket.
---

# Jira task drafter

Produce a Jira-ready task from the user's input (`$ARGUMENTS`) and/or the current conversation context. The user pastes the output into Jira manually — do NOT attempt any Jira API/MCP calls.

## Input

- If `$ARGUMENTS` describes the work, use it as the primary source.
- If arguments are empty or thin, derive the task from recent conversation context (the change just made, bug just found, plan just discussed).
- If neither gives enough substance, ask one concise question instead of inventing details.

## Output format

Return exactly two copy-paste blocks, nothing else:

```
TO5.D2.4 - <title>
```

```
<description>
```

## Never use the em dash

The character `—` is banned from the title and the description. Use a comma, a
colon, parentheses, or two sentences.

## Title rules

- Always prefixed `TO6.D2.4 - ` (prefix, space, hyphen, space).
- Short and imperative, no trailing period.
- Example: `TO6.D2.4 - Align Node version across the app`

## Description rules

- As concise as possible by default. Say WHAT needs to be done, never HOW.
- Concise, direct, informal language. Avoid technical jargon and implementation detail.
- Plain prose paragraphs — no headings, bullets only if they genuinely help.
- Simple task → one or two sentences. Example:

  > Make the Node.js version consistent wherever possible, including psps-deploy, the app, the UI library, .nvmrc, and related tooling and build processes.

- Complex task → more paragraphs describing the requirements and expected behavior, still WHAT-not-HOW, same tone. Behavioral contracts (e.g. an assumed API shape, statuses, polling expectations) belong in the description when the task can't be done without them; code-level choices do not. Example:

  > We will eventually want the user to be able to trigger validation on the server side. For this task, consider the trigger to be a manual click of the Validate button which already exists in the application.
  >
  > When the user triggers this validation, the current state of the pulse schedule (which may not match the latest saved state) will be sent to the server and the server will execute the validation asynchronously. The web app will indicate to the user that a validation is in progress and check, periodically, whether it has finished. When it has finished, the new pulse schedule (or a portion of it) will be fetched from the server (this is to reflect any transformations that were performed as part of the validation).
  >
  > The server-side API for this does not exist yet, so we will assume it takes the following form and stub out the API calls for the moment. [... assumed request/response behavior, statuses, polling interval ...]

- No invented estimates, assignees, sprints, labels, or acceptance-criteria boilerplate unless the user provides them.
- Never open by describing the current state as a gap ("X can do A, but there is no way to B"). State the work to do, nothing else. If the missing thing were not missing there would be no task — saying so is bloat.
- Do not explain or justify a requirement. Name it with the shortest term that carries it and stop — e.g. "must keep round-trip fidelity", not "must be in the same format the editor reads, so anything saved can be loaded again without conversion".
- References to existing behavior are a pointer, not a comparison. "Use the PSPS editor's Export Dataset as reference, keep the PCS architecture" — never spell out that one should not be copied over the other.
- Before returning the draft, check it for repeated words/phrases and bloated sentences (e.g. restating the same qualifier or clause more than once). Cut repetition and tighten wording — every sentence should add new information.
