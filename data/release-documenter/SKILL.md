---
name: Release documenter
description: Will handle creation of Atlassian Confluence release documentation creation
---

# Release documenter

## Instructions
- Should always use Atlassian MCP server to perform actions on confluence
  - If not authenticated with MCP server ask user to Authenticate
- `workspace` should be determined or provided
  - It is the directory that holds all cloned repositories (system's) will most likely be a parent directory from where claude has been called from, can be verified by finding the `.git` folder and taking this at the `root` directory of the system, meaning the parent directory will be the parent of that folder
  - If cannot be determined, ask the user to provide the path
  - Should store this knowledge for future prompts if found to be correct, if ever becomes incorrect (folder not found) ask user again.
- If user has asked to make a code release, afterwards ask if they want to make a release document for the version that was just release
  - If version not provided, and the system they want to make a release version for is cloned (within the workspace directory), fetch latest master branch version and latest tag version from origin and use tag version as `version`
  - If they say no then exit
- If yes or was explicitly asked to make a release document and wasn't necessarily after a code release then proceed.
- `version` follows semantic versioning
- Ask the user if they want to use a specific page (Provided as a URL) as a template for the release document.
  - Have a default value of: `https://siteminder.atlassian.net/wiki/spaces/AProg/pages/4311810049/v+version`
  - Asks the user if they want to provide a template for the release document (can be remembered for later and mapped differently for each system, saved for future prompts)
  - The template provided may have variables defined in the format [[<variable name>]]
  - When replacing values look for `[[system]]`, `[[version]]`, `[[deploymentDate]]`, `[[userMakingRelease]]`
- For the system the release document is being made for, ask the user to provide the parent folder that holds the systems releases manually
  - If provided then continue, if asked to try find it then use the MCP server to find the location where release documentation is kept for that system
    - page is normally labeled as `v<version>`
- Use the template to create a new release document on the new version specified and update all relevant fields in the document to reflect the new version number
  - Be sure to not alter any formatting / layout of the original template being used
- If there any any jql queries (Used by Jira Legacy / Insert Jira Issue modal) it should be updated also with the relevant fixVersion (`version`) and project (`system`)
- If PVT tests are provided in a table, check diff between tag of version provided and the tag before and populate the PVT table appropriate, if not found then keep empty PVT table.
- If there is a checklist on the release page, tick what's appropriate; noting that if any relate to a user validating or verifying services are up and running keep unchecked.
- Output the link to the new page along with all relevant information


## Examples
User provides, "Make a release document for demand-manager"
  - `system` would be `demand-manager`
  - using `workspace` location, fetch latest git changes for the system on `master` branch and determine the latest tag
  - Ask the user if tag `version` found is the version that they want to make the release document for
  - If not then let user provide `version`
  - Asks the user if they want to provide a template for the release document
  - Use Atlassian MCP server to determine where the release documents for the `system` are kept
    - if not found ask user to provide URL to parent directory that holds all release document pages
  - Uses Atlassian MCP server to create the release document by duplicating the release document template in the same directory but renaming the page name to be the `version` we're making the release document for.
  - Updates relevant details of new release document correctly


User provides, "Make a v1.0.0 release document for demand-manager"
  - `system` would be `demand-manager`
  - `version` would be `v1.0.0`
  - As above