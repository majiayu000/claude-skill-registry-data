---
name: cf-cli
description: Use when the user asks for Cloudflare's `cf` CLI, `cf cli search`, or `cloudflare.config.ts` to inspect resources, manage zones or DNS, attach domains, or deploy. Existing Wrangler projects keep their configured workflow unless migration is requested.
---

# Cloudflare `cf` CLI

`cf` 命令与覆盖范围会变化。以已安装版本和命令帮助为准，不把 Wrangler 参数直接套用。

## Start with the installed CLI

1. Check `cf --version` and the project's package manager, scripts, config, and any local `cf` or Wrangler dependency. Run project commands through the project's pinned version when present. For account-level work, the installed global `cf` is fine. Cloudflare's [announcement](https://blog.cloudflare.com/cloudflare-cf-cli-launch/) documents `npm i -g cf` for installation.
2. Run `cf cli search "<action and resource type>"`. Keep the query anonymous: no domains, account or resource IDs, names, email addresses, or tokens. Pick the relevant result; search can rank a similarly named product above the intended one.
3. Read `cf <discovered command> --help`. For API request fields and response shape, run `cf schema <discovered command without cf>`. Read the specific [Cloudflare documentation](https://developers.cloudflare.com/) or API page when semantics or prerequisites matter. Do not infer flags from Wrangler.
4. If search misses a command, consult the official docs or inspect the exact command group once. Do not run a chain of nested `--help` calls or guess a similarly named command.

## Authenticate and select the target

- Check `cf auth whoami` before remote operations. A Wrangler login does not establish a `cf` login. Use `cf auth login` or an existing, appropriately scoped `CLOUDFLARE_API_TOKEN`; do not print, paste, log, or put token values in command arguments. If login opens a browser, follow the workspace's browser instructions.
- Resolve the intended account, zone, project, Worker, hostname, and environment from the request and existing configuration before changing anything. Use a named `cf` profile or account setting when several accounts are available.
- Read results are safe to inspect; for mutations, review the exact target and required permissions. Use a command's `--dry-run` when available, then verify the remote result separately. A dry run is not deployment or domain activation.

## Choose the right workflow

- **Existing Wrangler project:** keep its current build and deployment path unless migration is requested. `cf migrate` changes project configuration; inspect the diff and test before switching. 如 `cf` 当前版本将构建委托给 Wrangler，按已安装命令与项目脚本执行。 Use the installed Wrangler skill for commands that remain on Wrangler.
- **New `cf` project:** use `cf init` and the generated `cloudflare.config.ts`; read the generated config and framework integration before `cf dev`, `cf build`, or `cf deploy`. Do not manually copy a `wrangler.jsonc` shape into the TypeScript config.
- **Zone onboarding:** discover and inspect `cf zones list` and `cf zones create`. Zone creation returns a pending zone; activation still requires the domain's nameservers or the documented partial-zone verification. Check existing zones, DNSSEC, and account scope before creating one.
- **Pages custom domain:** discover and inspect `cf pages projects domains create` for the project/domain association. DNS and nameserver requirements depend on whether it is an apex domain, subdomain, and Cloudflare-managed zone. Association and DNS must both be verified. See [Pages custom domains](https://developers.cloudflare.com/pages/configuration/custom-domains/).
- **Worker custom domain:** inspect the project's current routing config. `cloudflare.config.ts` can declare a fetch trigger; existing Wrangler projects can use `routes` with `custom_domain: true`. An active Cloudflare zone and Worker are required, and a conflicting CNAME prevents attachment. Verify the deployed domain and live response. See [Worker custom domains](https://developers.cloudflare.com/workers/configuration/routing/custom-domains/).
- **DNS only:** discover `cf dns records` commands, inspect the exact record before a write, and read it back afterward. A DNS record alone does not attach a Pages or Worker project.

## Finish

Report the CLI version, account/resource/environment targeted, what changed, and what was actually checked. Keep CLI output and credentials separate; never turn a successful command, dry run, returned URL, or DNS record into a claim that the site works without a live readback.
