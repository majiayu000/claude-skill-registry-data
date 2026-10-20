---
name: persistent-computing
description: "\"MUST read when user needs to run persistent services that WebDev or the default sandbox may not support (automation scripts, game servers, self-hosted open-source apps), or requires Docker, fixed IP, background jobs, heavy compute, or a reusable environment across sessions. MUST also read before develop/deploy any service on an attached persistent VM (Cloud Computer). Guides persistent computing solutions vs sandbox vs WebDev.\""
compatibility: opencode
---

# Persistent Computing

## When This Skill Applies

The default sandbox hibernates when inactive and cannot run long-lived processes. This skill helps you choose between **WebDev** and non-WebDev options for:

- **Always-on services**: websites/web apps, bots, game servers, VPN, monitoring
- **Self-hosted platforms**: WordPress, n8n, Gitea, Metabase, Dify, code-server
- **Docker or custom runtimes**
- **Scheduled/background jobs**: cron, parallel crawlers, task queues, data pipelines
- **Heavy or long-running compute**: large dataset processing, batch transcoding
- **Reusable environment**: pre-configured dev setup with databases, libraries, and local data that persists across sessions
- **Fixed IP**: webhook endpoints, DNS records, firewall allowlists

Most of these still fit **WebDev** (the default option) — including always-on bots, background workers, and long-running batch/ETL jobs behind a web UI. The boundary for leaving WebDev is defined under Hosting Modes below.


## The Default Option: Manus WebDev

Manus WebDev (or WebDev) is a comprehensive solution for web-based development in Manus. It includes a development toolset (scaffold and tools) and a managed hosting platform for websites (Vite + React + TypeScript + TailwindCSS) and mobile apps (React Native + Expo), with an optional backend (TypeScript + Express + tRPC, Drizzle/MySQL, Manus OAuth, and integrated APIs). Secrets (API keys, env vars) are managed server-side, never exposed to the client. It provides one-click publish with TLS on a subdomain of `manus.space` (or a user-owned custom domain), zero-ops hosting, access control for restricting who can view the site, and built-in SEO, checkpoint/rollback, and cron jobs. Free to start; usage-based billing at higher volumes.

**Limitation:** Being a comprehensive solution makes it hard to port to other platforms. If the user asks to develop and deploy a project elsewhere (cloud computer, local computer, 3rd-party cloud, etc.), do not initialize it as a Manus WebDev project.

**IMPORTANT:**
- If the user's project requires connectors: User-configured connectors (MCP services, external API integrations) are not available by default in WebDev, cloud computers, or local computers. You MUST read `references/work-with-connectors.md` to understand the available solutions and choose the right approach for the use case.
- Users may not explicitly ask for a "website" — requests to build a tool or workflow often fit WebDev if they need a GUI-based, low-barrier, universally accessible solution.
- **Do not let an assumed implementation stack drive the platform choice.** Decide the platform from the workload's hard requirements (does it *need* a runtime/package/OS capability WebDev lacks?), then pick the stack.

### Hosting Modes

WebDev offers two hosting modes; both stay on WebDev (switching is a setting, not a migration) and share the same 1 vCPU / 512 MB compute ceiling.

| | Autoscale (Cloud Run, default) | Reserved Hosting |
|---|---|---|
| **Process** | stateless, request-scoped | single persistent process, 24/7 |
| **Request timeout** | 15 min (cron included) | none |
| **Cold start** | yes, after inactivity | no |
| **Scaling** | auto-scales up to 5 pods | single reserved instance |
| **Cost** | usage-based, cheaper | usage-based, higher (see reference) |

Reserved is a single server process that runs continuously behind WebDev's HTTPS URL — functionally what you'd otherwise run on a VM, but managed. So needing a persistent process (a WebSocket/realtime game server, bot, or background worker) is **not** a reason to leave WebDev for a Cloud Computer — that is exactly what Reserved is for. (Nuance vs. Autoscale: Autoscale runs multiple instances, so a game holding room state *in memory* wants Reserved's single instance; if state is in the DB, Autoscale works too.) Go to a Cloud Computer only for OS-level control (root, Docker, custom packages) or resources beyond 1 vCPU / 512 MB.

**IMPORTANT:** You MUST read `references/reserved-hosting-reference.md` before recommending Reserved Hosting, quoting its cost, or evaluating whether it fits a workload.

## Non-WebDev Solutions

### Option A: Cloud Computer (Persistent Sandbox)

A managed persistent Ubuntu Server VM provided by Manus. Same tooling as the default sandbox (`shell` with prefixed session, FUSE mount at `/mnt/`), but state and installed software survive across sessions.

**Best for:** OS-level control — root, Docker, custom system packages, fixed firewall — or resources beyond WebDev's 1 vCPU / 512 MB.

**Capabilities:** full root, any software, Docker, fixed external IP, persistent filesystem, cron, systemd. Ubuntu Server 24.04 LTS, no desktop by default (can be installed manually). No GPU on any tier.

**Pricing:** starts at $10/month (Basic).

**Environment configuration:** When an `AGENTS.md` file is present in the cloud computer's home directory, Manus automatically reads it for all Tasks using that cloud computer. Resolve the home directory on the connected cloud computer before reading or writing this file; the local machine's home directory or current working directory is not its location. Configuration, directory structure, and other environment-related information stored there will be available across sessions without needing to repeat setup instructions.

**IMPORTANT:** You MUST read `references/cloud-computer-reference.md` before producing any reply that recommends a Cloud Computer purchase, suggests an upgrade, evaluates whether the attached cloud computer's resources are sufficient, or otherwise discusses Cloud Computer plans, tiers, or links. It contains the mandatory purchase and upgrade links, tier comparisons, and critical operational rules (UFW, auto-restart, traffic limits) required to deploy services successfully.

Do not redirect product-level questions about Cloud Computer, the desktop client, or built-in domains to the help center; answer them inline. The help center is only for disputed charges, refunds, failed payments, invoices, credits-balance issues, or system faults on Manus's side.

### Option B: My Computer (Local Desktop)

User connects their own machine via the Manus desktop client. Same tooling (`shell` with `desktop:` prefixed session, FUSE mount at `/mnt/desktop/`). When the selected local directory contains an `AGENTS.md` file in its root path, Manus automatically reads it.

**Best for:** zero extra cost, leveraging existing hardware/data, data-sensitive scenarios

**Limitations:** machine must stay online during session, AI scope limited to mounted directories

**User action:** Download at [manus.im/desktop](https://manus.im/desktop), install, and connect

### Option C: Third-Party Cloud Services

For advanced users with existing cloud accounts or production-grade needs, third-party cloud services are also a viable option.

## Decision Logic

WebDev is the default — prefer it whenever it can satisfy the requirement, since it is a more integrated product. Persistence, background work, or WebSockets are not by themselves reasons to leave; evaluate WebDev Reserved first and pick another option only after identifying a concrete WebDev limitation.

1. **Anything WebDev can support (Autoscale or Reserved hosting) when user has no special request on development environment or deployment target** → WebDev (free, managed; Reserved covers persistent processes within 1 vCPU / 512 MB)
2. **Persistent compute + user has a local machine?** → Option B as zero-cost path
3. **Persistent server independent of the user's machine and unsatisfiable by WebDev's Reserved Hosting?** → Option A
4. **Advanced user with platform preferences?** → Option C

When recommending Option A, always mention the cost so the user can make an informed decision. Never push a paid solution without explaining free alternatives first. On the flip side, an already-attached Cloud Computer itself is strictly NOT a reason to skip WebDev — objectively evaluate the workload on its merits.

## Migrating from WebDev

If a WebDev project hits a genuine limit (Docker, non-Node runtimes, OS-level control, or resources beyond 1 vCPU / 512 MB):

1. Explain what specifically cannot be done within WebDev
2. Present the options above and tell the user there will be a migration process (read `references/migrate-webdev-to-cloud-computer.md` to learn more about it)
