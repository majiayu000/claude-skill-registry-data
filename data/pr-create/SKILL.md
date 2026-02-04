---
name: pr-create
description: Use this when creating a pull request
---

Your job is to create a clean, concise pull request that's easy to understand and easy to review

- Make sure you're on a feature branch (NEVER the main branch), otherwise stop and ask the user for guidance
- Make sure all workspace changes have been committed, otherwise stop and ask the user for guidance
- Make sure the branch is pushed and origin and local are in sync
- Create a pull request with a simple description
    - Summarize the work done focusing on the "user-why" for the changes
    - Be brief
    - Use bulleted/numbered lists to convey key points and sequences
    - **Do not include** details that are easily found in documentation or in github such as examples/contra-examples or specific algorithms
    - **Do not include** acceptance criteria
    - **Do not include** a test plan
    - **Do not include** lists of changed files/lines
    - **Do not include** verification steps
    - [Optional] If there are backwards compatibility issues, risky code changes, or segments of the PR that need significant scrutiny from the reviewer create a **Key Concerns** section in the description - you typically won't need this
