---
name: azure-static-web-apps
description: Use when hosting a static front end on Azure Static Web Apps — deploying a local build with the SWA CLI, routing and fallback rules in staticwebapp.config.json, custom domains, managing the resource with Terraform, and keeping the Azure bill at zero by removing unused companions. Also use when deep links return 404, a deployment token expired, or a resource group keeps charging money after the app stopped needing it.
---

# Azure Static Web Apps

Default: Free plan, build locally, deploy with the SWA CLI from one script on the production branch, routing in `staticwebapp.config.json`, the resource and custom domain declared in Terraform.

## Deploy

```bash
npm ci && npm run build && npm test
npx @azure/static-web-apps-cli deploy ./dist --env production \
  --deployment-token "$SWA_DEPLOYMENT_TOKEN"
```

- Provide the deployment token from the environment (or fetch it at deploy time with `az staticwebapp secrets list`); never commit it.
- Without `--env production` the CLI deploys to a preview environment.
- Run the deploy only from the main branch with a clean working tree, as with any manual production deploy.

## Routing

```json
{
  "navigationFallback": { "rewrite": "/index.html", "exclude": ["/assets/*", "/*.{png,svg,css,js}"] },
  "routes": [{ "route": "/blog/*", "headers": { "cache-control": "public, max-age=3600" } }],
  "globalHeaders": { "x-content-type-options": "nosniff" },
  "responseOverrides": { "404": { "rewrite": "/404.html" } }
}
```

- The fallback makes client-side routes work on refresh and deep links; exclude real files so missing assets still 404.
- Static pages (articles, policy pages) are served as files; keep them as real HTML for crawlers.

## Infrastructure as code

- Declare `azurerm_static_web_app` and the custom domain in Terraform. If the resources already exist, `import` them into state and run `plan` until it shows no changes before editing anything.
- DNS: a CNAME (subdomain) pointing to the app's default host name; validation can take time — Terraform may need a retry.

## Cost hygiene

- The Free plan costs nothing, but companions created during experiments (container registries, container apps, log workspaces with high retention) do. List every resource in the resource group and the cost per resource; delete what the front end does not call.
- Removing a backend the front end never calls can be done without downtime — verify by checking the built JavaScript for its URL before deleting.

## Verification loop

1. Deploy, then `curl -sI https://<domain>/` (200) and a deep link (200 via fallback) and a missing asset (404).
2. Check headers from `globalHeaders` are present.
3. `terraform plan` shows no drift after any portal change.

## Pitfalls

- **Stuck custom domains** can block deleting an app; remove the domain first (via CLI or REST) and then the resource.
- **Region and plan limits:** the Free plan has size and custom-domain limits; check them before adding content.
- **Build in CI vs locally:** the default GitHub integration builds in Actions on every push; if you deploy locally, remove that workflow so the two do not race.
- **Case sensitivity:** routes are case-insensitive but file systems used in builds may not be; keep file names lowercase.
