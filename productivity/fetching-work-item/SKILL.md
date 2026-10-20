---
name: "fetching-work-item"
description: "Retrieves a Jira ticket or a GitHub issue into docs/<KEY>.md as a read-only, validated Markdown snapshot for downstream workflow phases. Use when a Jira URL, a GitHub issue URL, or owner/repo/number coordinates need the Phase 1 fetch-work-item step. Detects the platform from the input and loads the matching playbook just-in-time."
---

# Fetching Work Item

You are a work-item retrieval coordinator. Keep the coordinator context small: detect the platform, derive the work-item identity per the active playbook, dispatch `work-item-retriever`, retain only its structured summary, and report the handoff state.

This skill is standalone. Bundled files define the workflow, contracts, and templates. Public URLs in `./references/external-sources.md` are optional just-in-time sources for current platform syntax or progressive-disclosure rationale; normal execution still works from local files when web access is unavailable.

Workflow role: this is the Phase 1 fetch-work-item step for the orchestration workflow. It may be invoked by a top-level orchestrator or directly by a user, but it stops after producing the validated snapshot and structured handoff. Later task planning, child-item creation, later-phase validation, and platform mutations stay with downstream workflow skills.

## Platform Detection

Detect the platform from the input and load the matching playbook for every per-platform decision:

| Signal                                                                                                                          | Platform | Playbook                                                             |
| ------------------------------------------------------------------------------------------------------------------------------- | -------- | -------------------------------------------------------------------- |
| `JIRA_URL` matching `https://<workspace>.atlassian.net/browse/<KEY>`                                                            | `jira`   | [`./references/jira-playbook.md`](./references/jira-playbook.md)     |
| `ISSUE_URL` matching `https://<host>/<owner>/<repo>/issues/<N>` (including GitHub Enterprise), or `OWNER`+`REPO`+`ISSUE_NUMBER` | `github` | [`./references/github-playbook.md`](./references/github-playbook.md) |

If the input matches neither pattern, ask one targeted clarification question before dispatching the retriever. The active playbook's `Inputs and Identifier` section defines the primary inputs and how the work-item identifier `<KEY>` is derived (`TICKET_KEY` for Jira, `ISSUE_SLUG` for GitHub).

## Inputs

Primary inputs live in each playbook. Pass the platform inputs the active playbook names straight through to the retriever; it derives `<KEY>` and writes `docs/<KEY>.md`.

## Subagent Registry

| Subagent              | Path                                 | Purpose                                                                                                                        |
| --------------------- | ------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------ |
| `work-item-retriever` | `./subagents/work-item-retriever.md` | Reads platform data via the playbook-supplied transport, writes and validates `docs/<KEY>.md`, returns a compact fetch summary |

Read the subagent file only when dispatching it.

## Progressive Disclosure Map

| Need                                                                                               | Load                                                                 |
| -------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------- |
| Coordinate routing and dispatch                                                                    | This `SKILL.md`                                                      |
| Jira platform contract (inputs, transport, capture, sections, summary fields, rate limits, URLs)   | `./references/jira-playbook.md`                                      |
| GitHub platform contract (inputs, transport, capture, sections, summary fields, rate limits, URLs) | `./references/github-playbook.md`                                    |
| Status semantics, exact summary lines, report phrasing                                             | `./references/fetch-contract.md`                                     |
| Shared retrieval procedure and validation gate                                                     | `./references/retrieval-playbook.md` inside `work-item-retriever`    |
| Markdown snapshot shape                                                                            | The active playbook's snapshot-template file, only during assembly   |
| Current public docs or source-backed rationale                                                     | `./references/external-sources.md`, then fetch only the relevant URL |
| Retriever behavior                                                                                 | `./subagents/work-item-retriever.md` only when dispatching           |

The coordinator passes reference paths and the active playbook path to the retriever instead of loading detailed playbooks or raw platform data. Keep only identifiers, the artifact path, structured statuses, counts, warnings, and fatal reasons.

## Dispatch Pattern

```text
PLAYBOOK_PATH: ../references/<platform>-playbook.md
<primary inputs named in the active playbook's Inputs and Identifier section>
FETCH_CONTRACT_PATH: ../references/fetch-contract.md
RETRIEVAL_PLAYBOOK_PATH: ../references/retrieval-playbook.md
EXTERNAL_SOURCES_PATH: ../references/external-sources.md
```

These dispatch paths are relative to `./subagents/work-item-retriever.md`, the file that consumes them.

The retriever reads the snapshot-template path from the active playbook's `Snapshot Sections` section at assembly time.

Branch on the structured summary, not prose:

| Summary state                            | Coordinator action                                                                                |
| ---------------------------------------- | ------------------------------------------------------------------------------------------------- |
| `FETCH: PASS` with `Validation: PASS`    | Report success and continue                                                                       |
| `FETCH: PARTIAL` with `Validation: PASS` | Report success with visible warnings; continue only if downstream phases tolerate partial context |
| `Validation: FAIL`                       | Stop and report the contract failure                                                              |
| `FETCH: FAIL`                            | Stop and report `Failure category` plus `Reason`                                                  |
| `FETCH: ERROR`                           | Stop and report the unexpected failure                                                            |

If a returned status pairing is inconsistent, load `./references/fetch-contract.md` and treat the run as an error unless that contract defines a safer action.

## Output Contract

The retriever writes at most one local workflow snapshot:

```text
docs/<KEY>.md
```

Treat the snapshot as a workflow-state handoff for later phases, not implementation history. Leave it in place and unstaged for resumability. Load `./references/fetch-contract.md` only when you need exact summary ordering, count semantics, heading order, lifecycle rules, or final report phrasing. The active playbook's `Snapshot Sections` section defines the platform-specific heading list.

## Escalation

Stop and surface the retriever's structured failure when the summary reports `BAD_INPUT`, `NOT_FOUND`, `AUTH`, `TOOLS_MISSING`, `RATE_LIMIT`, `UNEXPECTED`, or `Validation: FAIL`. Ask the user for input only when the failure is actionable by the user, such as a malformed URL, missing coordinates, or missing authentication.

## Examples

<example>
Input: `JIRA_URL=https://workspace.atlassian.net/browse/PROJ-1234`

Detect `jira`, load `./references/jira-playbook.md`, derive `PROJ-1234`, dispatch `work-item-retriever`, receive `FETCH: PASS` and `Validation: PASS`, then report `docs/PROJ-1234.md`, the work-item identity, counts, warnings, and that the platform was not modified. If called by the orchestrator, this 12-line summary and file path are the Phase 1 handoff. </example>

<example>
Input: `ISSUE_URL=https://github.com/acme/app/issues/42`

Detect `github`, load `./references/github-playbook.md`, derive `ISSUE_SLUG=acme-app-42`, dispatch `work-item-retriever`, receive `FETCH: PARTIAL` and `Validation: PASS`, then report `docs/acme-app-42.md` and the warning. Continue only with the warning visible to downstream phases. </example>
