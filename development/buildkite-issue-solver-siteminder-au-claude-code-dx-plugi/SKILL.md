---
name: Buildkite issue solver
description: Will utilise buildkite read only mcp server to solve specific buildkite issues encountered
---

# Buildkite issue solver

## Instructions
- When provided with buildkite instructions ALWAYS utilise the buildkite-read-only-toolsets mcp server
- When provided with a buildkite url will determine if there's any issues in any of the builds or jobs using the MCP server
- If there are issues, utilise the Atlassian MCP server to fetch the confluence documentation on how to resolve Terraform Errors in buildkite deploy below.
  - https://siteminder.atlassian.net/wiki/spaces/IOPS/pages/1820000809/Terraform+Errors+in+Buildkite+Deploy
  - note:
    - `-s` is an argument to provide `system`
    - `-e` is an argument to provide `environment`
    - `-c` is an argument to provide `component`
    - `-r` is an argument to provide `realm`
- Go through the errors found via the buildkite mcp server and check if they are present within the confluence documentation
  - NOTE: Never perform any modifications on confluence
- Accumulate the issues and go through one by one asking user to approve the fixes needed based on the confluence documentation, replacing `system`, `component`, `realm`, `config_branch`, `environment` as needed based on original buildkite deployment and component that has the issue.
  - Display the fix to the user and ask for approval to run fix
  - After fix has run and error is resolved then retry the failed job in the original buildkite link.
  - Validate the job runs correctly and if not try to resolve again
  - If runs successfully then proceed to next issue (if there are any).

## Examples
- Buildkite link provided has a build with error `Error: another operation (install/upgrade/rollback) is in progress` for the job `Deploy notifications-beef to prod`. `notifications-beef` is the component, `prod` is the `environment`
- Should visit confluence and find the fix that's appropriate for that component
- Ask the user to approve running the suggested fix