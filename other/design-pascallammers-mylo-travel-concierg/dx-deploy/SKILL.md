---
name: dx deploy
description: use to deploy a siteminder component using the dx command
---

# Siteminder DX deploy

## Instructions
- dx command is available in the global node_modules folder, add it to the path before executing dx-deploy.js.
- if user dosn't have dx installed in global, use `npx @siteminder/dx` to execute the command instead of `dx`.
- before executing, please add all user bash environment variables to the command.
- When asking for arguments, provide the user the ability to select from a dropdown or if requires typing allow the user to address each argument independantly 
- required arguments: system, environment, component, workspace
  - `environment` can be typically `platform-dev` `tpi` `shared` `prod`, but can be something else
  - `workspace` is the folder that contains all cloned repositories, each repository is a `system`, the folder name is usually also the system name but not always
- Ask user to provide the workspace, and remember it for future use.
- optional arguments: region, build version, realm, config branch, infrastructure branch
  - `region` can be as of right now only `apac` or `emea`
  - `realm` can either be `dev` `pciprod` or `preprod`. This can be determined through the `environment` selected
    - if environment is `platform-dev` or `shared` realm will be `dev`
    - if environment is `prod`, realm will be `pciprod`
    - if environment is `tpi` or `demo` realm will be `preprod`
- always asking user to provide config-branch and infrastructure-branch, if not provided, then use default values, options while asking is: master or provided your branch name.
- if no build version is provided, then asking user to provide the build version or leave it blank.
- before executing, change executing directory to the workspace that user has provided.
- before executing, give an outline of what is about to proceed and ask user to approve with all relevant details shown.
- command for executing the script:
- componentTerraformConfigPath is the path to the terraform config file for the component.
  - If region IS NOT provided this will be <workspace>/<system>-config-<realm>/<component>/<environment>/terraform.tfvars
  - If region IS provided this will be <workspace>/<system>-config-<realm>/<component>/<environment>/<region>terraform.tfvars
  - check <component> is existing under <system>-config-<realm>, if not, try find <component>-inf or <component>-app, if not found, error out.
- configBranch is the branch to checkout in the config repo, if it exists. default: master
- infrastructureBranch is the branch to checkout in the app infrastructure repo, if it exists. default: master
- buildVersion is the build version to deploy.
  - if no build version is provided, then don't have to provide the argument in the command.
```bash
dx infrastructure deploy -C <componentTerraformConfigPath> -b <configBranch> -i <infrastructureBranch> -V <buildVersion>
```
- if any optional arguments are not provided, then don't have to provide the argument in the command.
- present all stdout and stderr output to the user.
- then wait for user to approve for further actions.

## Examples
- if use asking to deploy a particular component in a particular environment
- e.g: "deploy google-gha provider-api to platform-dev"
- this means:
  - `system` -> google-gha
  - `component` -> provider-api
  - `environment` -> platform-dev
- then the command should be:
```bash
dx infrastructure deploy -C google-gha-config-dev/provider-api/platform-dev/terraform.tfvars -b master -i master
```

- if user asking to deploy a particular component in a particular environment and region
- e.g: "deploy tbb-google pricing-bridge to platform-dev apac"
- this means:
  - `system` -> tbb-google
  - `component` -> pricing-bridge
  - `environment` -> platform-dev
  - `region` -> apac
- then the command should be:
```bash
dx infrastructure deploy -C tbb-google-config-dev/pricing-bridge/platform-dev/apac/terraform.tfvars -b master -i master
```

## Examples

#### Example for user asking to deploy a particular component in a particular environment
- user request: "deploy tbb-google pricing-bridge apac to platform-dev"
- this means:
  - `system` -> tbb-google
  - `component` -> pricing-bridge
  - `region` -> apac
  - `environment` -> platform-dev
- should change to the workspace directory before executing the command.
- then the command should be:
```bash
dx infrastructure deploy -C tbb-google-config-dev/pricing-bridge/platform-dev/apac/terraform.tfvars -b master -i master
```

#### Example for user asking to deploy a particular component in a particular environment and region
- user request: "deploy tbb-google content-handler to platform-dev"
- this means:
  - `system` -> tbb-google
  - `component` -> content-handler
  - `environment` -> platform-dev
- should change to the workspace directory before executing the command.
- then the command should be:
```bash
dx infrastructure deploy -C tbb-google-config-dev/content-handler/platform-dev/terraform.tfvars -b master -i master
```

#### Example for user who dosn't have dx installed in global
- user request: "deploy tbb-google pricing-bridge apac to platform-dev"
- this means:
  - `system` -> tbb-google
  - `component` -> pricing-bridge
  - `region` -> apac
  - `environment` -> platform-dev
- then the command should be:
```bash
npx @siteminder/dx infrastructure deploy -C tbb-google-config-dev/pricing-bridge/platform-dev/apac/terraform.tfvars -b master -i master
```