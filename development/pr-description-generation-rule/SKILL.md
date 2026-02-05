---
name: pr-description-generation-rule
description: Rule for creating PR (pull request) description
---

# PR Description Generation Rule

This rule helps generate PR descriptions by comprehensively utilizing changes between the current branch and a specified branch, contents of changed files, current conversation content, and the `.github/PULL_REQUEST_TEMPLATE.md` file.

## How to Use

1. Ask the AI "Generate PR description with context" or use the "generate_pr_description_contextual" command.
2. The AI will ask which branch to compare against (e.g., `upstream/main`, `origin/develop`).
3. The AI will perform the following steps to generate the PR description:
  * Fetch the latest information for the specified branch (`git fetch`).
  * Analyze `git diff` between the current branch and specified branch to identify the list of changed files, commit summaries, and **key code changes**.
  * **Reference current conversation content or additional context provided by the user**.
  * Read the `.github/PULL_REQUEST_TEMPLATE.md` file.
  * Synthesize all collected information to create the PR description.
4. Review the generated description, modify as needed, and use it for your pull request.

## Rule Logic (Guidelines for AI)

### Step 1: Get Comparison Branch Information from User
  - Clearly ask the user for the name of the branch to compare against.
  - Example prompt: "Which branch would you like to compare against? Please enter something like `origin/main` or `upstream/develop`."

### Step 2: Fetch Git Information and In-depth Analysis
  - **Fetch**: Retrieve the latest changes from the remote repository containing the branch provided by the user.
    - `print(default_api.run_terminal_cmd(command='git fetch <remote_name> <branch_name_without_remote_prefix>', is_background=False))`
      (e.g., `git fetch origin main`)
  - **Log**: Get the commit list for the "What's changed?" section.
    - `print(default_api.run_terminal_cmd(command='git log <full_branch_name>..HEAD --pretty=format:"- %s (%h)" --abbrev-commit', is_background=False))`
      (e.g., `git log origin/main..HEAD --pretty=format:"- %s (%h)" --abbrev-commit`)
  - **Diff (Attempt to Identify Detailed Changes)**: Try to identify the list of changed files and key changes in each file.
    - First, get the list of changed files:
      `print(default_api.run_terminal_cmd(command='git diff HEAD...<full_branch_name> --name-only', is_background=False))`
    - (Optional, at AI's discretion) For some important files, execute `git diff HEAD...<full_branch_name> -- <file_path>` to check and summarize actual changes. Don't read all files if there are many.
    - Or get overall change statistics with `git diff HEAD...<full_branch_name> --shortstat`.
    - **AI Judgment**: Decide which files to examine in more detail based on the number and size of files and importance of changes. May ask the user for explanations about specific files.

### Step 3: Collect Additional Context
  - **Review Conversation Content**: Check if the user has mentioned anything about the PR's purpose, key changes, problems to solve, etc., in the conversation so far, and prepare to reflect this in the PR description if available.
  - **Provided Context**: If the user has explicitly provided additional information (e.g., specific issue numbers, related document links, etc.), include this in the "Reference" or "Details" section.

### Step 4: Read PULL_REQUEST_TEMPLATE.md
  - Read the contents of the `.github/PULL_REQUEST_TEMPLATE.md` file.
  - `print(default_api.read_file(target_file='.github/PULL_REQUEST_TEMPLATE.md', should_read_entire_file=True, start_line_one_indexed=1))`

### Step 5: Generate PR Description (Comprehensive)
  - **"What's changed?" Section**: Summarize the changes resulting from `git diff` analysis into no more than 3 items. Summarize so that the overall modifications and purpose are clearly evident.
  - **"Details" Section**: Write as detailed as possible based on the `git diff` analysis results (file change summary) from Step 2 and conversation content/user-provided context from Step 3.
  - **"Reference" Section**: Include related issue numbers, document links, etc., collected in Step 3.
  - **Other Template Sections**: Fill as needed or guide the user to fill them.
  - **Checklist**: Maintain the template's checklist as is.
  - Ensure the final output follows the structure of PULL_REQUEST_TEMPLATE.md.

### Step 6: Present Results to User
  - Provide the generated PR description to the user and may ask about parts that need additional modification.
