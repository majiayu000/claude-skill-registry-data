---
name: gitlab-usecase
description: Use before GitLab, glab, GitLab MCP, IssueOps remote issue/MR, linked-item, child-item, work-item, Kody/Kodus review, issue-body update, branch-target, or cleanup work. Prevents repeated GitLab mistakes by distinguishing native linked items from child items, enforcing body-of-record rules, authenticated CLI/MCP fallback, labels/assignee/target-branch checks, and review-thread verification.
---

# GitLab Usecase

Use this skill before GitLab work starts. It is a guardrail for repeated mistakes in GitLab IssueOps, MRs, work items, review feedback, and cleanup.

## Start Protocol

1. Identify the exact GitLab object type before acting. **The URL path does not tell you whether an object is a plain Issue or a Task.**
   - `/-/issues/:iid` and `/-/work_items/:iid` are two aliases of one issue identity. GitLab 18.10+ renders plain issues at `/-/work_items/:iid` as well. Verified 2026-08-27 on 19.2.4-ee: in a sampled project every plain issue (`issue_type: issue`) and every Task (`issue_type: task`) returned a `/-/work_items/` `web_url`, and not one returned `/-/issues/`. Never infer the type from the path.
   - Read the type from the payload instead: REST `issue_type` (`issue` / `task`) or `type` (`ISSUE` / `TASK`), or GraphQL `workItemType.name` (`Issue` / `Task`).
   - MR: `/merge_requests/:iid`
   - Native linked item: non-hierarchical relation such as `relates_to`, `blocks`, `is_blocked_by`
   - Child item: parent-child hierarchy, not a link relation
2. Fetch work items through the issues endpoint. **There is no REST `projects/:id/work_items/:iid`**; it answers `404 Not Found` (verified 2026-08-27 on 19.2.4-ee). Read any work item, Task included, through `projects/:id/issues/:iid` and confirm the type from `issue_type` / `type`, or through the GraphQL work-item API. If a `/-/work_items/` URL is all you have, resolve it against `issues/:iid` with the same project path and IID.
3. Pick the authenticated surface whose credentials and scope match the target GitLab host and project before the first call: generic `glab` CLI, or a configured GitLab MCP tool discovered by capability.
4. Do not report completion from local state alone. Re-read the remote issue/MR/work item after mutation.

## Portable VCS Recipe Discovery

GitLab issue 본문을 읽는 provider recipe가 필요할 때는 다음 순서를 지킨다.

1. canonical worktree가 있으면 먼저 선택 문서 `.issueops/VCS.md`를
   `project_docs_read`로 읽는다. 문서가 없거나 해당 provider recipe가 없으면 현재
   host에 등록된 trusted tool을 탐색한다.
2. GitLab MCP는 서버 이름이 아니라 semantic leaf `glab_api`와 실제 input schema로
   식별한다. server namespace는 등록 세부사항이지 capability identity가 아니다.
   같은 leaf와 호환 schema를 노출하는 개인 wrapper도 지원한다. 특정 wrapper 이름,
   설치 경로, profile, token을 코드나 공용 문서에 고정하지 않는다.
3. 실제 schema에 맞춰 `projects/<URL-escaped-project>/issues/<iid>`를 읽고,
   schema가 지원하면 `flags.hostname`으로 target host를 명시해 `web_url`,
   `description`, `state`를 받는다. 여러 후보가 있으면 target host/project 권한과
   schema가 맞는 후보만 사용한다.
4. 응답의 HTTPS authority(명시 port 포함), project path, IID를 linked issue와 정확히
   대조한다. `/issues/:iid`와 `/work_items/:iid`는 이 세 값이 모두 같을 때만 같은
   identity다.
5. 후보 부재뿐 아니라 auth/permission/transport/schema 호출 실패 뒤에도
   exact-identity MCP 응답을 얻지 못했으면 일반 `glab api` CLI를 사용한다.
   이미 받은 응답이 identity 대조에 실패했으면 CLI로 대체하지 않고 멈춘다.
6. 실제로 성공한 provider recipe는 canonical worktree에서 `project_docs_read`로
   최신 content/SHA를 다시 읽고 `project_docs_revise`의 SHA-CAS로
   `.issueops/VCS.md`에 기록한다. tool leaf, 관찰한 schema, endpoint/필드,
   CLI fallback만 남기고 secret과 개인 server namespace는 남기지 않는다.
   canonical worktree가 아직 없으면 생성 뒤로 기록을 미룬다.
7. `.issueops/VCS.md`는 provider-neutral하다. GitHub repo에서는 검증된
   `gh issue view <url> --json url,body,state`를 기록하거나 실제로 관찰한 MCP
   schema만 기록한다. 존재하지 않는 GitHub MCP 이름을 추측해서 만들지 않는다.

## Profile-Scoped glab MCP Servers (when configured)

Some environments expose `glab` through profile-scoped MCP servers, where each server pins one GitLab host, one token, and one default project workdir (server selection = target project + credential declaration). In that setup:

- Before any call, confirm the server profile matches the task's target project. A wrong-profile call is not always an error — it can silently succeed against the wrong project or fail with a misleading 404.
- Do not rely on repo autodetection. Without an explicit `-R <group/project>` or explicit API endpoint, `glab` resolves the repo from the current session's working directory, not the profile workdir — in a non-GitLab checkout it errors ("None of the git remotes configured for this repository point to a known GitLab host", verified 2026-08-27), and in a different GitLab checkout it silently targets that repo. Verified 2026-07-09 against profile-scoped servers.
- Profile tokens are often project-scoped bot tokens. A 404 on another project usually means token scope, not a missing project; switch to the matching profile instead of forcing `-R`.
- Do not switch profiles mid-task without re-verifying the target object (issue/MR/work item) on the new profile.
- These MCP tools run the same `glab` CLI under the profile's credentials; CLI-vs-MCP is a credential/scope choice, not a capability fallback order.

## Non-Negotiable Distinctions

| Need | Correct GitLab surface | Wrong surface |
| --- | --- | --- |
| Related issue | Native linked item through issue links API | Body-only URL, child item |
| Work breakdown | Child `Task` work item through work-item hierarchy | `relates_to`, issue link, sibling issue |
| Parent task index | Parent issue body `## 하위 Task` plus real hierarchy | Comments-only checklist |
| Existing child proof | Work-item hierarchy / parent widget | REST `has_tasks`, body reference, linked item |

`has_tasks` is never child proof. Verified 2026-08-27 on 19.2.4-ee: a parent issue that held a real child Task still reported `has_tasks: false`, while its `task_completion_status` counted unrelated markdown checkboxes in the body. Prove children through the work-item hierarchy only.

For IssueOps child tasks, use `issueops remote create-child --confirm --json` when creating new children. It must create a GitLab `Task` work item, attach it with `workItemHierarchyAddChildrenItems`, verify hierarchy/labels/assignees, and record the child. Use `link-child` only for an already existing provider-native child that was verified separately.

Do not create child work by calling `glab api projects/:id/issues/:iid/links`, `glab issue link`, or `issueops link-related`. Those create or record linked items, not child items.

If a Task is already a linked item and must become a child item, remove the linked relation first, then set/attach the parent hierarchy, then verify by GraphQL/work-item hierarchy.

## Remote Artifact Rules

- GitLab related issues belong in native linked items, not a `Related Issues` body section.
- The GitLab issue body is the source of truth for scope, acceptance criteria, child task list, and durable evidence. If the user says not to comment, update the issue body.
- For long issue-body updates, fetch the current description, patch it additively, submit with file-backed description input when possible, then re-read and verify.
- Remote issue/MR text should stay Korean-centered except code identifiers, branch names, commands, and URLs. Before any remote write — issue body, MR body, note, or thread reply — invoke the `fluent-korean` skill and apply it to the draft.
- Inside an IssueOps cycle, never create or edit an issue, child, or MR body through `glab` or a glab MCP tool. Use `issueops remote create-issue|create-child|create-pr|sync-issue|sync-pr`: they run the body contract and readability check and record the write, and a direct write skips both.

## Branch And MR Rules

- Treat user-named branches such as `release/stg`, `development`, parent issue branches, and child branches as part of the contract.
- Child MR targets the parent issue branch, not the default branch, unless the user explicitly says otherwise.
- Copy or pass labels and assign the MR/issue to the concrete current user. Do not use `@me`.
- `glab mr for` is deprecated: glab answers `Command "for" is deprecated, use 'glab mr create --related-issue <issueID>'` (verified 2026-08-27). Use `glab mr create --related-issue <issueID>` instead, and pass a numeric assignee id wherever that path takes an assignee.

## Review And Cleanup Rules

- Automated-reviewer threads (Kody/Kodus, CodeRabbit, Copilot, Gemini, `pr-review`) are owned by the `review-agent-feedback` skill. Route there instead of hand-rolling the triage; this skill only fixes the GitLab-side rule that skill must satisfy: inspect the real discussion thread, reply in-thread with evidence, then re-fetch discussions and resolve every remaining `resolvable=true` and `resolved=false` note.
- A merged MR does not prove the child Task is closed. Verify the Task state after merge and close it explicitly when needed.
- Cleanup sequence: verify MR merged, verify remote/source branch state, verify child Task state, verify worktree cleanliness, then remove worktree/local branch.

## Stop Conditions

Stop and ask or switch to GitLab MCP/API when:

- local `glab` or a glab MCP profile returns `401`, `404`, missing scope, or permission errors;
- the resolved project of the auth surface does not match the task's target project (wrong profile/workdir/token);
- linked item and child item state disagree;
- target/base branch does not match the recorded parent branch;
- issue body update would overwrite unknown current content;
- review thread state cannot be re-read after a reply.
