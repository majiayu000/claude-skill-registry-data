---
name: code releaser
description: To initiate a release by executing the dx release command with appropriate parameters.
---

# Code releaser

## Instructions
- Before executing, give an outline of what is about to proceed and ask user to approve with all relevant details shown.
- DO NOT update package.json version number.
- DO NOT execute 'git push' or 'git tag' commands, these are handled by `dx release` command.
- Ensure that the version provided follows semantic versioning (e.g., 1.0.0, 2.1.3) and does not contain the prefix 'v'.
- If version is not provided then:
  - Ensure current branch is on master
    - If not on master, ask user if they want to switch to master branch.
  - Fetch latest changes from origin before:
    - Checking what the latest tag is
  - When latest tag is found, set version appropriately based on whether user has specified major, minor, or patch increment.
    - If user has not specified increment type, then ask user to provide increment type (major, minor, patch).
- `systemPath` is root folder path of the system we want to release:
  - root folder path being the folder that contains the system's .git folder
  - e.g. if the user says they want to release channels-plus, channels-plus is the system name and the path to the channels-plus folder should be the root directory that holds the .git folder related to the channels-plus git repository.
  - if the current working directory is something like ".../<parent-folder>/demand-manager/" then to release channels-plus there should be a folder for the channels-plus system under ".../<parent-folder>/channels-plus/" which holds the .git folder for channels-plus. If it doesn't exist tell the user and exit.
- Ensure that the systemPath provided is correct and contains the .git folder.
- `system` is the name of the system that can be found at the root package.json file, if it exists
  - if package.json does not exist it will take the directory name of the git repository in question.
- Ensure that the system name provided matches the name in the root package.json file, if it exists.
- If there is no package.json file at root then DO NOT proceed and exit.
- Once all parameters are validated:
  - cd to `systemPath` directory
  - display a summary of the release prep details including current working directory and prompt user for approval.
- When approval is given, execute dx release command with relevant parameters, and return the output in a user friendly format with relevant release details and links if any.
- command to execute dx release should be run in the intended system's project root directory, and should have the latest master checked out and up to date. Command is as below
```bash
npx @siteminder/dx github release --do-not-push --new-version <version>
```

## Examples
If user asks for a code release and the pwd is at the root of the git repository and it has a package.json with name property "channels-plus" system should be "channels-plus" and systemPath could be "~/system-repositories/channels-plus"
latest git tag on origin master should be found and version parameter should be incremented approriately using semantic versioning based on user input (if not specified then ask if patch, minor or major release)
e.g. latest tag found is 1.0.2
minor release would be 1.1.0
dx release command will then be used to make the release and called within the root folder of channels-plus cloned repository under master branch.