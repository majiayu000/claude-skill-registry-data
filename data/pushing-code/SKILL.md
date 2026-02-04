---
name: pushing-code
description: Commits and pushes code changes. Used when work should be committed and/or pushed to Git.
color: purple
---

# Committing code
Create a git commit message which summarises the changes being committed. Include what was changed and why the changes were made, using the conversation history to determine the why if possible.

## Challenge your "why"
After drafting a "why" part, challenge yourself: would a reader be able to easily determine this themselves from the "what"? If so, don't include the "why", since it is superfluous.

# Pushing code
After committing, push code to the git remote, creating and tracking if necessary, unless asked not to.

# GitHub Integration
- Always use gh CLI for GitHub operations when possible. Authentication is automatically taken care of by the GH_TOKEN environment variable.
- Fall back to GitHub API when gh CLI isn't suitable

# Improvements
- If you solve any problems with pushing code, for example with gh authentication not working out of the box, summarise for the user what problem you solved and how after you finish the task. This information will be used to improve the skill in future.
