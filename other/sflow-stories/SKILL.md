---
name: sflow-stories
description: List Story candidates and their progress, then ask which exact Story to make active through /sf-session.
disable-model-invocation: true

---
# Choose a Story from durable state

<!-- sflow-output-contract: explicit-selection -->
**Output contract:** Collect every required choice explicitly; never infer or preselect; preserve errors, artifacts, and next actions.
<!-- sflow-execution-boundary -->
**Boundary:** machine-local; no repository or Story required. Use explicit arguments or SFlow-returned paths; never search `$HOME` or infer a repository.

1. Preserve explicit `--workspace <WORKSPACE> --repository <REPOSITORY-ID>` selectors. Partial selectors: resolve only within the explicit workspace or ask; never fill from active workspace/cwd. With none supplied, run `singularity-flow workspace current --json`; when active, capture its exact `workspacePath` and `repositoryId` and pass both as selectors. Never let an old host cwd override that selected workspace. With no active workspace, an opened Git root is a valid discovery scope; if unresolved, ask for `/sf-workspace` and stop. Never guess URLs or use a planned checkout as cwd.
2. Run `singularity-flow session candidates --table` with that scope. Relay the complete CLI table, progress, active markers, scope, warnings, and errors verbatim. Do not hide inactive Stories, invent progress, make per-Story status calls, or use Home headings. Candidate `repositoryPath` is only the discovery source, not the destination. For an explicit list-only request, end here without selection.
3. Ask with `ask_user` or plain chat for an exact Story ID or row number. Map a row only to the exact ID in that returned table. Preserve the table's workspace/repository selectors. Never auto-attach the first or current Story; ambiguous, absent, or unavailable choices require clarification, not attachment.
4. After the contributor explicitly chooses, invoke and complete existing `/sf-session <WORK-ID>` with those exact selectors in this flow, not merely display its route. It tries a managed local checkout first and permits verified remote attachment only on its specified unavailable-local refusals. Verify the returned checkout and session status `ready`, `workId`, and `activeAgent`; do not assume attachment has `activeAgent` or run a second attachment sequence here.
5. Stop after session setup. Discovery alone changes no active Story. Do not create, advance, begin, submit, approve, merge, publish, or execute Story work.
