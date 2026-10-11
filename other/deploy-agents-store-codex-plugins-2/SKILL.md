---
name: deploy
description: 'Deploy Trigger.dev tasks to an environment Arguments: [staging|prod] [--profile <name>].'
---

# Deploy Tasks

1. Determine target environment from arguments (default: prod; `production` is accepted and means `prod`)
2. Verify `trigger.config.ts` exists
3. Build the deploy command:
   - Base: `npx trigger.dev@<version> deploy --env <environment>`, where `<version>` is the installed `@trigger.dev/sdk` version from `package.json` (for self-hosted, the server's version); `@latest` only when the project has no pinned version
   - If `--profile` argument: add `--profile <name>`
   - If monorepo: add `--config <path>`
   - A CLI that differs from the installed `@trigger.dev/*` packages makes `deploy` fail in CI; prefer the project's `trigger.dev` devDependency
4. Run the deploy command
5. Report the deployment status and version
6. Suggest: "Check deployment with `list_deploys(environment='<env>', limit=1)` or in the dashboard"