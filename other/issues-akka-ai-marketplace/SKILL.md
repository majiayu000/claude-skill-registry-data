---
name: issues
description: "Convert existing tasks into actionable, dependency-ordered GitHub issues for the feature based on available design artifacts."
---

## User Input

You **MUST** consider the user input before proceeding (if not empty).

## Outline

1. **Locate the feature**: Call the `akka_sdd_list_specs` MCP tool to find features. Verify that `tasks.md` exists for the target feature (`has_tasks` must be true). If `tasks.md` is missing, instruct the user to run `/akka:tasks` first. Read the `tasks.md` content from FEATURE_DIR.

2. **Build the task-ID set**: Scan `tasks.md` for every task line — each starts with `- [ ]` followed by a task ID matching `T` and three digits (e.g. `T001`). Collect the set of task IDs you are about to process.

3. **Determine the GitHub repository from the git remote**:

   ```bash
   git config --get remote.origin.url
   ```

   > [!CAUTION]
   > ONLY PROCEED TO THE NEXT STEPS IF THE REMOTE IS A GITHUB URL

4. **Fetch existing issues for deduplication**: Before creating anything, use the GitHub MCP server's `list_issues` tool to find issues that already cover the task IDs from step 2.
   - Do **not** pass a `state` value — omitting it returns both open and closed issues.
   - Request `perPage: 100` to minimize calls.
   - The tool uses cursor-based pagination: request further pages with the `after` parameter using the `endCursor` from the previous response.
   - For each issue title, match against the pattern `\bT\d{3}\b` (word boundaries so `ST001` and `T0010` do not false-match). This recognizes titles written as `T001 ...`, `T001: ...`, or `[T001] ...`. When it matches one of your task IDs, mark that ID as already having an issue.
   - **Stop paginating** as soon as every task ID has been matched, or when there are no more pages. This bounds the number of calls on repos with large issue histories.

5. **Create issues for tasks that don't have one yet**: For each task in `tasks.md`:
   - Strip the leading `- [ ]` and any `[P]` / `[US#]` markers to recover the task ID and description. Example: `- [ ] T001 [P] [US1] Create User model in src/models/user.py` → ID `T001`, description `Create User model in src/models/user.py`.
   - If the ID is in the "already has an issue" set from step 4: **skip** it and report `T001 already has an issue, skipping`.
   - Otherwise, use the GitHub MCP server's `issue_write` tool to create a new issue in the repository derived from the git remote. Use the canonical title format:

     ```text
     T001: Create User model in src/models/user.py
     ```

   > [!CAUTION]
   > UNDER NO CIRCUMSTANCES EVER CREATE ISSUES IN REPOSITORIES THAT DO NOT MATCH THE REMOTE URL

6. **Report**: Summarize the run — total task IDs found, existing issues detected (skipped), new issues created, and the target repository URL.

## Done When

- [ ] FEATURE_DIR and `tasks.md` were resolved via `akka_sdd_list_specs` with `has_tasks == true`.
- [ ] The full set of task IDs (`T\d{3}` matches in `tasks.md`) was collected before any GitHub calls were made.
- [ ] The git remote was inspected and confirmed to point at a GitHub repository — for any non-GitHub remote the command stopped without creating issues.
- [ ] `list_issues` was called with `perPage: 100`, both open and closed issues (no `state` filter), and cursor-based pagination via `after`; pagination stopped as soon as every task ID was matched or the pages ran out.
- [ ] Titles were matched against `\bT\d{3}\b` with word boundaries, so tokens like `ST001` or `T0010` were not false-matched.
- [ ] Every new issue used the canonical title format `T###: <description>`, built by stripping `- [ ]`, `[P]`, and `[US#]` markers from the source task line.
- [ ] Tasks whose IDs already had an existing issue were skipped and each skip was reported (e.g. `T001 already has an issue, skipping`).
- [ ] Every created issue lives in the repository derived from the git remote and in no other repository.
- [ ] The report includes the total task count, count of skipped-because-already-exists, count of newly created issues, and the target repository URL.
