---
name: az-ado
description: Operate the Azure DevOps CLI extension through native az devops, boards, repos, pipelines, and artifacts commands. Use for ADO board inventories, work-item mapping and assignment, hierarchy changes, PRs, pipeline runs, service connections, permissions, wikis, packages, and diagnosing authentication or empty CLI output. Discover exact syntax from installed -h manuals before operations.
---

# Azure DevOps CLI

`az-ado` is this skill's name. The installed extension has no `az ado` command.
Use `az devops` and its related top-level groups. This skill does not install a shell alias.

## Start here

1. Read the active repository's identity, transport, deployment and approval rules. For Wholesale work, read [wholesale.md](references/wholesale.md).
2. Resolve the actual Azure CLI executable with `command -v az` and inspect a wrapper before relying on its profile selection. Record `az version --output json`. Do not install, upgrade, log in, log out, switch identity, change proxies or set global defaults merely to discover commands.
3. Run `az devops -h`, then the appropriate related group's `-h`. Follow its advertised subgroups to the leaf. Read that leaf's current `-h` immediately before an operation. Reference snapshots are navigation aids, not substitutes for current syntax.
4. Select explicit organization and project where supported. Separate the organization origin from the project path. Pass the project as one argument. Never append unsupported `--project` to a leaf that only accepts organization.
5. Classify the operation's effects, confirm authority, execute bounded requests, validate the response and read back writes. Report exact scope, observed result and remaining gaps.

## Command routing

| Need | Start | Reference to load |
| --- | --- | --- |
| Organization, project, team, users, extensions, wikis, service endpoints, security, generic API | `az devops -h` | [devops.md](references/devops.md) |
| Work items, relations, queries, area/iteration paths | `az boards -h` | [boards.md](references/boards.md) |
| Repositories, PRs, branch policies, reviewers | `az repos -h` | [repos.md](references/repos.md) |
| Definitions, runs, builds, releases, variables, variable groups, pools | `az pipelines -h` | [pipelines.md](references/pipelines.md) |
| Universal package upload/download | `az artifacts -h` | [artifacts.md](references/artifacts.md) |

The references cover 269 help pages, including paths five tokens deep after `az`.
They include every child advertised by those five roots on the captured extension version.
[coverage.json](references/coverage.json) records paths and flags. It does not claim coverage of every ADO REST API.

## Response contract

Use `--output json` for machine reads and parse the response before making claims.
Capture exit status, stdout and stderr separately. A nonzero exit, malformed JSON,
empty stdout or wrong JSON shape is inconclusive, not a verified empty result.
Even exit zero with no output is not `[]`. Inspect documented null/empty semantics
and confirm against another scoped read before classifying no matches.

For collections, inspect documented page sizes and continuation behavior. Report a
partial inventory if you cannot prove all pages were retrieved. Do not silently
truncate a hierarchy or interpret a filtered view as the whole project.

For writes, read back the exact item and relevant fields/relations. A queued run
is not a successful deployment. A returned item ID is not proof that its parent,
assignee or final state matches the request.

## Board and identity workflow

- `az boards query` accepts WIQL through `--wiql`, or a saved query ID/path. It supports flat queries only. `--query` is output filtering with JMESPath, not WIQL.
- Extension 1.0.8 does not pass project context to `query_by_wiql`. Use an explicit escaped project-name literal in WIQL rather than `@project` for this path, even with `--project`. Verified against Wholesale on 2026-09-08: the macro returned no output, the literal returned 872 items. Empty matches return Python None and hence empty stdout. The implementation caps detail retrieval at 1,000 items; partition large inventories by ordered ID bounds and verify exhaustion.
- Discover the process's actual types, states, fields and backlog settings before mapping Epic, Feature, Story, Task or Bug. Do not assume Bug placement or state names.
- Inventory first, deduplicate second, propose changes third, write only within approved scope. Preserve IDs and history. Read exact work items and relations to build hierarchy. Do not use flat-query output as proof of every relationship.
- Resolve assignees to an exact verified identity. `az devops user show --user` accepts email or user ID. `user list` defaults to 100, supports `--top`/`--skip`, and excludes users added through AAD groups. A missing user in that list is not proof the identity does not exist.
- Authentication identity and `System.AssignedTo` are separate. Approval to inventory multiple profiles does not authorize reassignment.
- Preview exact IDs, types, parents, assignees and state transitions for a mapping proposal. Do not manufacture IDs or choose a parent from title similarity alone. Unmapped updates stop for resolution.
- Check `work-item relation list-type -h`, `relation show -h`, and the intended mutation help. Confirm relation direction before adding or removing a parent. Detect cycles and conflicting parents. Record partial success if a multi-step reparent fails.
- Creation and discussion comments can duplicate on retries. Re-read after an uncertain write before retrying. The native work-item update help exposes no revision precondition flag. Do not promise atomic compare-and-swap from a read-then-update sequence.

## Effects and authorization

Help discovery executes only `-h` and version reads. Never execute a sample mutation to learn syntax.

Read operations may still expose confidential data. Retain only necessary fields,
keep private evidence in protected scratch files, and avoid raw `--debug` logs,
which may contain credentials or private request/response bodies.

Treat creates, updates, assignments, relations, comments, wiki edits, uploads,
pipeline queues, installs and permission changes as writes. Queueing can deploy.
Downloads and checkouts write local files. Login/logout/configure affect local
credentials or defaults. Inspect command-specific behavior instead of assuming
that every `show` is harmless or every POST is a mutation.

Require explicit authority for deletion, access-policy changes, production,
merging/completing PRs, publishing and irreversible operations. Repository guards
remain controlling. Do not grant escalation roles or reset passwords.
Never put PATs, passwords, secret variables or tokens in argv, files under version
control, output or examples. Use an approved secure credential mechanism.

## Native API escape hatch

When a typed command cannot express the required read, inspect `az devops invoke -h`.
It is part of this extension, not a reason to invent a new REST client. Discover
area/resource and route/query parameters before use. Pin the supported API version
rather than assuming the help's default 5.0 matches the resource.

Use explicit `--http-method` and JSON output. Some APIs use POST for read-only
queries, so classify by documented endpoint semantics as well as HTTP method.
Writes require an approved plan and any necessary concurrency precondition.
Keep payload files private and scrub outputs. Missing resource documentation,
permission or transport is a blocker, not permission to guess an API call.

## Failures and recovery

- Missing credentials: name the selected profile and failed read, request restoration through the approved login path. Do not enumerate token stores or switch to another identity to bypass failure.
- Empty output: compare a harmless version/help response, validate the requested endpoint and profile, and inspect bounded non-secret diagnostics. Stop after three unsuccessful attempts without new evidence.
- Authorization error: distinguish authentication, project visibility, object permission and pipeline service-connection RBAC. Local user access is not the deploy identity's access.
- Unknown subcommand: re-walk installed help. `az ado` is not native syntax on the captured version.
- Unsupported atomicity or bulk operations: state the limit and use a documented native API with the required guards, or stop. Do not claim a script creates a transaction across independent writes.

## Completion

Report CLI/extension versions, organization/project, exact read or approved write
scope, pagination coverage, response validation, write read-back and blockers.
Help-only verification proves command availability, not live ADO access.
For skill maintenance, run `python3 scripts/validate.py` from this skill directory.
