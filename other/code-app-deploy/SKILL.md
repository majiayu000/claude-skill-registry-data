---
name: code-app-deploy
description: "Deploy and operate a Power Apps code app: build/push, solutions, Pipelines, CSP, SDK migration, App Insights, PAC CLI failures (fetch failed, UNABLE_TO_VERIFY_LEAF_SIGNATURE, Zscaler). Use for pac code push, npx power-apps push, ALM, security, monitoring."
---

# Power Apps Code App — Deploy & Operate

Guide developers through deployment, ALM, security configuration, monitoring, and troubleshooting.

- For deployment, ALM, security, and monitoring: [references/deployment-and-alm.md](references/deployment-and-alm.md)
- For diagnostic workflows and troubleshooting: [references/troubleshooting-guide.md](references/troubleshooting-guide.md)

## Deployment Workflow

### Build & Push

**npm CLI (recommended):**
```bash
npm run build
npx power-apps push
```

**PAC CLI (legacy):**
```bash
npm run build | pac code push
# Target a specific solution:
npm run build | pac code push --solutionName <solutionName>
```

### Add to a Solution

Apps are automatically saved to the **preferred solution** when using `pac code push`.
To add manually: Power Apps portal > Solutions > [solution] > Add existing > App > Code app.

### Multi-Environment Deployment

Use **Power Platform Pipelines** to promote through dev → test → prod:
- Pipelines run preflight checks (dependencies, connection references)
- Connection references decouple data connections from environment-specific settings
- Each environment can have its own connection configurations

## Security — Content Security Policy

CSP controls which content sources are allowed. Configure at environment level:

**UI path:** Power Platform Admin Center > Environments > Settings > Product > Privacy + Security > App (CSP tab)

**Key directives:** `connect-src` (API endpoints), `script-src` (JavaScript sources), `style-src` (CSS), `img-src`, `font-src`

For programmatic configuration (CI/CD), use PowerShell or REST API — see the deployment reference.

## Monitoring — Azure App Insights

```typescript
import { ApplicationInsights } from '@microsoft/applicationinsights-web';
import { setConfig } from '@microsoft/power-apps/app';

const appInsights = new ApplicationInsights({
  config: { connectionString: '<your-connection-string>' }
});
appInsights.loadAppInsights();

setConfig({
  logger: {
    logMetric: (value) => {
      appInsights.trackEvent({ name: value.type }, value.data);
    }
  }
});
```

Built-in metrics: `sessionLoadSummary` (app load performance), `networkRequest` (API call timing).

## SDK v1.0 Migration

If migrating from SDK v0.3.21:
1. Remove all `initialize()` imports and calls
2. Remove initialization state management (`isInitialized` flags, `useEffect` guards)
3. Use SDK methods directly — no async initialization needed
4. Optionally configure `setConfig({ logger: ... })` for observability

## Quick Troubleshooting

| Symptom | Likely Cause | Action |
|---------|-------------|--------|
| `TypeError: fetch failed` | SSL proxy (Zscaler) intercepting | Export proxy CA cert, set `NODE_EXTRA_CA_CERTS` |
| `ETIMEDOUT` / `ECONNRESET` | Network/DNS issue | Check connectivity, firewall rules |
| Wrong schema / data source not found | Wrong environment in config | Run `pac env who`, compare with `power.config.json` |
| `401` / `403` on data requests | Auth/permissions issue | Re-authenticate: `pac auth create` |
| CSP violation in console | Missing allowed source | Add URL to CSP directive in admin center |

For detailed diagnostic workflows, see the [troubleshooting reference](references/troubleshooting-guide.md).

## ALM Limitations

Code apps currently do **not** support:
- Solution Packager tool
- Power Platform Git integration (source control)

## What NOT to Do

- Do not use `NODE_TLS_REJECT_UNAUTHORIZED=0` in production — it disables all SSL validation
- Do not skip CSP configuration when using external APIs or CDNs
- Do not store App Insights connection strings in app code — use Dataverse settings or environment detection
- Do not ignore preflight check failures in pipelines — they indicate missing dependencies
