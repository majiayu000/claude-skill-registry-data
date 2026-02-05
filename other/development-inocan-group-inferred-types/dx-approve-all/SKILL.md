---
name: dx approve all
description: use to approve all builds in a tagged buildkite link using the dx command
---

# DX approve all

## Instructions
- dx command is available in the global node_modules folder, add it to the path before executing dx-infrastructure-approve-all.js.
- if user doesn't have dx installed in global, use `npx @siteminder/dx` to execute the command instead of `dx`.
- before executing, please add all user bash environment variables to the command.
- ensure that the buildkite build URL/path is provided.
- required arguments: build_path (the buildkite build URL to approve)
- before executing, give an outline of what is about to proceed and ask user to approve with all relevant details shown.
- command for executing the script:
```bash
npx @siteminder/dx infrastructure approve-all --tagged-build-url <build_path>
```
- present all stdout and stderr output to the user.
- then wait for user to approve for further actions.
- print a list of all the files pending for approval, also count the total file number

## Examples

#### Example for user asking to approve all builds in a buildkite link
- user request: "approve all builds for https://buildkite.com/siteminder/my-project/builds/12345"
- then the command should be:
```bash
npx @siteminder/dx infrastructure approve-all --tagged-build-url https://buildkite.com/siteminder/my-project/builds/12345
```

## Usage Notes
- This tool will approve all pending builds in the provided tagged buildkite link automatically
- Make sure you have the necessary permissions to approve builds in buildkite
- The build_path should be the full URL to the buildkite build
