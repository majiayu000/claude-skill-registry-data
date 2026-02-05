---
name: dx list
description: Show list of available dx list commands and help users execute them with required parameters.
---

# dx list

## Instructions
This skill helps users discover and execute various dx list commands. When users type 'dx list' or ask to list resources, present them with available list command options organized by category.

## Available List Commands

### Infrastructure Commands (dx infrastructure list-*)

1. **list-artifact-versions**
   - Description: List recent artifact versions of the component/frontend
   - Required parameters:
     - `--system` or `-s`: System name (e.g., tbb)
     - `--component` or `-c`: Component name (e.g., core-api)
   - Optional parameters:
     - `--max` or `-m`: Max number of items in result (default: 30)
   - Command: `npx @siteminder/dx infrastructure list-artifact-versions -s <system> -c <component>`

2. **list-builds**
   - Description: List builds on infrastructure-deploy pipeline
   - Required parameters:
     - Either `--component` or `-c` OR `--config-file` or `-C`
     - `--env` or `-e`: Environment (when using --component)
     - `--realm` or `-r`: Deployment realm (dev, pciprod, preprod, bi, bidev, oldprod, test, stratops)
   - Optional parameters:
     - `--type` or `-t`: Deployment type (terraform, helm, frontend)
     - `--region` or `-R`: Region construct
     - `--config-branch` or `-b`: Branch to checkout in config repo
     - `--infrastructure-branch` or `-i`: Branch to checkout in app infrastructure repo
     - `--max-pages`: Max number of BuildKite build result pages (default: 10)
     - `--per-page`: Results per page (default: 100)
     - `--created-from`: Filter by builds created on or after (ISO 8601 format)
     - `--created-to`: Filter by builds created before (ISO 8601 format)
   - Command: `npx @siteminder/dx infrastructure list-builds -c <component> -e <env> -r <realm>`

3. **list-tagged-resources**
   - Description: List resources deployed to AWS and K8s
   - Optional parameters:
     - `--environment` or `-e`: Environment to list resources
     - `--system` or `-s`: System name(s) (comma separated)
     - `--component` or `-c`: Component name(s) (comma separated)
     - `--provider` or `-pr`: Provider (aws, k8s, all - default: all)
     - `--providerService` or `-ps`: Provider service(s) (default: compute)
     - `--sort`: Sort by comma separated parameters (default: environment,system,component,provider)
   - Command: `npx @siteminder/dx infrastructure list-tagged-resources -e <env> -s <system>`

4. **list-standard-terraform-modules**
   - Description: List all standard default terraform modules that should be used in infrastructure
   - No parameters required
   - Command: `npx @siteminder/dx infrastructure list-standard-terraform-modules`

### Overlord Commands (dx overlord list-*)

5. **list-non-standard-docker-images**
   - Description: List non standard docker images used in the system directory
   - Required parameters:
     - `--system`: Path to the system folder
   - Command: `npx @siteminder/dx overlord list-non-standard-docker-images --system <path>`

### Code Commands (dx code list-*)

6. **list-docker-image-versions**
   - Description: List all docker image versions used in the current dir and child dir
   - No parameters required (runs in current directory)
   - Command: `npx @siteminder/dx code list-docker-image-versions`

7. **list-standard-docker-images**
   - Description: List all standard default docker images that should be used in systems
   - No parameters required
   - Command: `npx @siteminder/dx code list-standard-docker-images`

8. **list-npm-pkg-differences**
   - Description: Compare all package.json files to list different versions being used between components
   - Optional parameters:
     - `--dir`: Path to the base directory (default: current directory)
   - Command: `npx @siteminder/dx code list-npm-pkg-differences`

## Execution Flow

1. When user requests 'dx list' or similar:
   - Present a categorized list of all available list commands with brief descriptions
   - Ask which command they want to execute

2. Once user selects a command:
   - Check if the command requires parameters
   - If parameters are required, ask the user to provide them
   - If optional parameters exist, ask if they want to specify any
   - Present default values where applicable

3. Before executing:
   - Show the complete command that will be executed
   - Ask for confirmation

4. Execute the command:
   - Check if dx is available globally, otherwise use `npx @siteminder/dx`
   - Run the command
   - Present all stdout and stderr output to the user

5. Handle errors:
   - If command fails, show the error message
   - Suggest common fixes or parameter adjustments

## Examples

### Example 1: User wants to see list options
```
User: "dx list"
Assistant: Presents categorized list of all 8 list commands
User: Selects "list-artifact-versions"
Assistant: Asks for required parameters (system, component)
User: Provides "tbb" and "core-api"
Assistant: Confirms and executes: `dx infrastructure list-artifact-versions -s tbb -c core-api`
```

### Example 2: User wants to list tagged resources
```
User: "show me list commands"
Assistant: Presents all list commands
User: "list tagged resources"
Assistant: Asks for optional parameters (environment, system, component, provider)
User: Provides "nxs-dev" for environment and "nxs" for system
Assistant: Executes: `dx infrastructure list-tagged-resources -e nxs-dev -s nxs`
```

### Example 3: User without global dx installation
```
User: "dx list"
Assistant: Checks dx availability, finds it's not globally installed
Assistant: Uses `npx @siteminder/dx` prefix for all commands
User: Selects "list-standard-docker-images"
Assistant: Executes: `npx @siteminder/dx code list-standard-docker-images`
```

### Example 4: Quick execution without menu
```
User: "list builds for my component in dev"
Assistant: Recognizes "list builds" command
Assistant: Asks for component path, environment, and realm
User: Provides details
Assistant: Executes: `dx infrastructure list-builds -c <component> -e dev -r <realm>`
```

## Notes
- Always verify dx is installed globally, otherwise fall back to `npx @siteminder/dx`
- For commands that require BUILDKITE_API_TOKEN or GITHUB_TOKEN, remind users to set them if errors occur
- Some commands (like list-builds) can take a component path relative to the repo root
- Commands that search the current directory will use the user's current working directory
