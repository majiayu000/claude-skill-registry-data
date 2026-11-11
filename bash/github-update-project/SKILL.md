---
description: Rename the issues of a GitHub project to start with a tag, after review
model: haiku
---

# Goal
- Given a `<TAG>` (e.g., `Noesis`) and a `<PROJECT_URL>` (e.g.,
  `https://github.com/users/gpsaggese/projects/2`), rename every issue in the GitHub
  project so its title starts with `<TAG>: `
- Propose first, apply only after the user approves
- Follow the rules in `.claude/skills/github.rules.md`

# Inputs
- `<TAG>`: the prefix word, without colon (e.g., `Noesis`)
- `<PROJECT_URL>`: the project URL in one of these forms
  - `https://github.com/users/<OWNER>/projects/<NUM>`
  - `https://github.com/orgs/<OWNER>/projects/<NUM>`
- If either input is missing, ask the user for it

# Workflow

## Parse the Project URL
- Extract `<OWNER>` and `<NUM>` from `<PROJECT_URL>`
- Use `<OWNER>` and `<NUM>` in all `gh project` commands

## Check Access
- Private and public user projects need the `read:project` scope
- Test access:
  ```bash
  > gh project view <NUM> --owner <OWNER> --format json
  ```
- If it fails with `missing required scopes [read:project]`, ask the user to run
  this command in the prompt, since it needs a browser and a device code
  ```
  ! gh auth refresh -h github.com -s read:project
  ```
  - Do not run it with the Bash tool: it waits for the browser and times out
  - `-h github.com` is required in a non-interactive shell
  - Wait for the user to confirm before continuing

## Read the Items
- Save the items to a file in the scratchpad directory, not in the repo:
  ```bash
  > gh project item-list <NUM> --owner <OWNER> --limit 500 --format json \
      > <SCRATCHPAD>/items.json
  ```
  - The default limit is 30: always pass `--limit`
  - Compare the saved item count with `items.totalCount` from `gh project view`
- For each item, read these fields: `content.number`, `content.type`,
  `content.repository`, `title`
- Treat items by `content.type`:
  - `Issue`: rename
  - `PullRequest`: keep unchanged (PR titles follow the `UmdTask<N>_` convention)
  - `DraftIssue`: no issue number exists, so list it and skip it

## Propose the New Titles
- Apply these rules in order, per issue
  - Title already starts with `<TAG>:`: keep unchanged
  - Title starts with `<TAG>_` (roadmap ID): replace `_` with `: `
    - **Bad**: `Noesis_PR_M12 Add tables`
    - **Good**: `Noesis: PR_M12 Add tables`
  - Title contains `<TAG>` elsewhere: move the tag to the front and drop the
    redundant word
    - **Bad**: `Organize Noesis codebase into components`
    - **Good**: `Noesis: Organize codebase into components`
    - **Bad**: `Noesis MVP: checker foundation`
    - **Good**: `Noesis: MVP checker foundation`
  - Any other title: prepend `<TAG>: `
    - **Good**: `Get the team gelled together` becomes
      `Noesis: Get the team gelled together`
- Drop redundant information in the new title
  - A second `<TAG>` word that repeats the prefix
  - A branch ID like `UmdTask639_` when the issue number already identifies it
    - **Bad**: `Noesis: Follow up to UmdTask639_Noesis_PR_S11`
    - **Good**: `Noesis: Follow up to PR_S11`
- Keep an existing second `<TAG>` mention when it is the subject of the sentence
  - **Good**: `Noesis: Prove that Noesis improves over a single-sided market`
- Do not change anything else in the title: keep the roadmap IDs, the wording, and
  the case
- Do not edit labels, status, body, or project fields

## Write the Plan Files
- Write a table with columns `#`, `Before`, `After` into
  `plan-github.update_project.md`
  - Include only the issues that change
  - Below the table, list the unchanged items by number with the reason (already
    prefixed, PR, draft issue)
- Write the commands into `plan-github.update_project.sh`
  - One line per changed issue, using the `content.repository` of that item:
    ```bash
    gh issue edit <ISSUE_NUM> --repo <OWNER>/<REPO> --title '<NEW_TITLE>'
    ```
  - Escape a single quote in a title as `'\''`
  - Start the file with the comment `# NOT RUN. Review first.`
- Build both files with a script saved in a different directory than the downloaded
  JSON, and run it with `python3 -I`

## Get Approval
- Show the user the before / after table and the counts: changed, already OK,
  skipped
- State the open decisions: the ID format, whether PRs are renamed, redundancy
  dropped
- Do not run any `gh issue edit` before the user answers with a clear "go"
  - An answer to a decision question is not a "go"
  - An earlier "do not change the names" stays in force until the "go"
- If the user changes a rule, regenerate both plan files and show the table again

## Apply the Renames
- Run the script after the "go":
  ```bash
  > bash plan-github.update_project.sh
  ```
- Each command prints the issue URL on success
- If a command fails, stop, report the failing issue number and the error line,
  and do not retry silently

# Constraints
- Never rename without approval of the exact before / after table
- Never rename a PR unless the user asks for it
- Never change anything but the title
- Keep scratch files (`items.json`, plan files) out of the Git repo or delete them
  at the end

# Verification
- [ ] Re-read the project items with the same `gh project item-list` command
- [ ] Confirm the item count equals the count before the renames
- [ ] Confirm every item with `content.type` equal to `Issue` has a title that starts
      with `<TAG>:`
  ```bash
  > gh project item-list <NUM> --owner <OWNER> --limit 500 --format json \
      | python3 -I -c "
  import json, sys
  d = json.load(sys.stdin)
  bad = [(i['content']['number'], i['title']) for i in d['items']
         if i['content']['type'] == 'Issue' and not i['title'].startswith('<TAG>:')]
  print(len(d['items']), 'items; issues without prefix:', bad)"
  ```
- [ ] Confirm PRs and draft issues are unchanged
- [ ] Report to the user: number renamed, number unchanged, any failures

# Example
- Invoke with:
  ```
  /github.update_project Noesis https://github.com/users/gpsaggese/projects/2
  ```
- Result on that project: 41 items, 30 issues renamed, 10 issues already prefixed,
  1 PR left unchanged
