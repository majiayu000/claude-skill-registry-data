---
name: recon
description: Run the DigitalOcean ephemeral-droplet recon pipeline over a list of IPs, CIDRs, or wildcard domains. Use when target-init has produced http.md scope but recon (port scan, subdomain enum, httpx, feroxbuster) is missing. Spawns droplets, runs in parallel, tears down. Optional multi-region for geo-block detection.
---

# recon

Front-door for the `recon` MCP server.

## When to invoke

- New target where `targets/<name>/recon/` is empty.
- User asks for "recon", "port scan", "subdomain enum", "ferox" on a target.
- Multi-region geo check requested.

## Inputs (from `targets/<name>/http.md`)

Parse the scope section. Build a `targets` list:
- IPs and CIDRs go through verbatim.
- Wildcard apex domains become `*.<apex>`.
- Bare domains MUST be promoted to `*.<domain>` (the parser will refuse otherwise).

### Picking `scan_region`

Match `scan_region` to the geography implied by the scope. Geo-fenced or
country-coded apex TLDs (`.au`, `.uk`, `.de`, `.in`, `.sg`, `.ca`, `.nl`)
must scan from the matching DO region, or banners and CDN edges will be
wrong. Default `nyc1` only when scope is US-centric or generic gTLD.

| TLD / hint                  | scan_region |
| --------------------------- | ----------- |
| `.au`, `.com.au`            | `syd1`      |
| `.uk`, `.co.uk`             | `lon1`      |
| `.de`, `.eu`, EU hosts      | `fra1`      |
| `.nl`                       | `ams3`      |
| `.sg`, `.asia`              | `sgp1`      |
| `.in`                       | `blr1`      |
| `.ca`                       | `tor1`      |
| US / generic gTLD (default) | `nyc1`      |

Mixed scopes (e.g. `.com` + `.com.au`): pick the region matching the
country-coded TLD and add the US region to `probe_regions` so both
edges are sampled. Confirm region choice with the user before launch
when the scope spans multiple country TLDs.

## How to call

```
recon_start({
  "targets": ["1.2.3.4", "10.0.0.0/24", "*.acme.io"],
  "target_name": "acme",
  "scan_region": "nyc1",
  "probe_regions": [],
  "max_droplets": 10
})
```

Poll with `recon_status({"job_id": ...})` every 30–60 s until `status == "done"` or `"failed"`.
Then `recon_results({"job_id": ...})` for the structured summary.
Persist into `targets/<name>/status.json.recon = {job_id, summary_path, finished_at}`.

## Hard rules

- Never start a recon job whose `targets` include hosts outside `targets/<name>/http.md` scope. (2026-05 — scope-discipline rule; load-bearing for H1/Synack ToS compliance.)
- Confirm with the user before `probe_regions` longer than 3 (cost).
- If `recon_cancel` is invoked, also verify droplet count is 0 via `recon_list_jobs`.

## Failure handling

- `status == "failed"` → inspect `error`; surface to user; do not retry automatically.
- Stuck `running` past `RECON_MAX_RUNTIME_MIN` → call `recon_cancel`, surface, suggest splitting CIDR.
