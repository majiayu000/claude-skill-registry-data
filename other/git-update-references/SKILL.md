---
description: Update references in other Git repos to files moved, renamed, or deleted here
model: haiku
---

# Goal
- Find files moved, renamed, updated, or deleted in the current repo and
  update all references to them in the other Git repos

# Workflow

## Find Changed Files
- Find all files moved, renamed, updated, or deleted in the current repo:
  ```bash
  > invoke git_files --branch --only-print-files
  ```

- Print the files that are moved, renamed, or deleted
  - Print the main functions changed

## Search for References
- For each file `<FILE>`, search for its references in these repos:
  - `helper`: the current repo
  - `umd_classes`: located at `~/src/umd_classes1`
  - `csfy`: located at `~/src/csfy1`
  - `orange`: located at `~/src/orange1`
  - `lemonade`: located at `~/src/lemonade1`

- You must:
  - Skip the Git sub repos of each repo (e.g., `helpers_root`)
  - Search only files under Git control
  - Skip symlinks (e.g., `.claude`) using an approach like:
  ```bash
  search_repo() {
    local repo_path=$1
    local search_term=$2

    (cd "$repo_path" && {
      # Get submodule paths to exclude
      submodules=$(git config --file .gitmodules --name-only --get-regexp path 2>/dev/null | sed 's/.*path=//' | tr '\n' '|' | sed 's/|$//')

      if [ -n "$submodules" ]; then
        git ls-files | grep -v "^($submodules)" | while read -r file; do
          [ ! -L "$file" ] && echo "$file"
        done | xargs grep "$search_term" 2>/dev/null
      else
        git ls-files | while read -r file; do
          [ ! -L "$file" ] && echo "$file"
        done | xargs grep "$search_term" 2>/dev/null
      fi
    })
  }
  ```

- Print the references in a table organized by:
  - Repos
  - Files

- Create a vim quickfile cfile for the locations using the conventions in
  `.claude/skills/cfile.rules.md`

- Pause and ask the user to continue

## Update References
- Update the references in all the repos

# Verification
- [ ] Confirm every reference to each moved, renamed, or deleted file was
      updated in every repo
- [ ] Re-run the search and confirm no stale reference remains
