---
name: fusionaly-deploy
description: Use ONLY when explicitly invoked. Puts Fusionaly on a Linux server you reach over SSH with a key. Optionally creates a Hetzner server and the Cloudflare DNS record. The user runs the one interactive install command; the agent prepares and checks everything around it.
---

# Deploy Fusionaly

Four steps: a server, a DNS record, one install command, a check. The agent does the setup and the checks. **The user runs the install command in their own terminal**, because the installer is interactive and needs a real terminal.

## Rules

- **SSH keys only.** Never ask for, type, or store a password. If the server takes only passwords, stop and help the user add a key (`ssh-copy-id`).
- **Ask before anything that costs money or changes DNS.** Show the exact command first.
- **Never disable host key checks.** Use `-o StrictHostKeyChecking=accept-new` for a new server.
- **No "analytics" in the hostname.** Blockers drop hostnames with `analytics`, `tracking`, `stats` or `telemetry`. Suggest `data.example.com` or a brand name.
- **Tokens stay in the user's shell.** Ask the user to export them. Do not paste them into files.

## 1. Server

Ask: "Do you have a Linux server you can SSH into with a key?" This is the default path.

**Existing server.** Ask for the IP and the SSH user, then check:

```bash
ssh -o BatchMode=yes -o ConnectTimeout=5 <user>@<ip> 'uname -s && (test "$(id -u)" = 0 || sudo -n true) && echo ready'
```

`ready` means SSH works and the user has root or passwordless sudo. Anything else: stop and fix that first.

**New Hetzner server (optional).** Needs the `hcloud` CLI and a read/write API token from the Hetzner console (Security > API Tokens).

```bash
hcloud context create fusionaly            # paste the token when it asks
hcloud server-type list -o columns=name,cores,memory,disk   # pick the smallest shared type
hcloud ssh-key list                         # or: hcloud ssh-key create --name me --public-key-from-file ~/.ssh/id_ed25519.pub
```

Show the plan and ask before creating it (it is billable):

```bash
hcloud server create --name fusionaly --type <type> --image ubuntu-24.04 --location <location> --ssh-key <key>
hcloud server ip fusionaly
ssh -o StrictHostKeyChecking=accept-new -o ConnectTimeout=5 root@<ip> 'echo ready'   # retry for ~60s while it boots
```

Fusionaly needs 1 vCPU, 512 MB RAM, 10 GB disk.

## 2. DNS

Ask for the domain. Then create an `A` record: `<domain>` → `<ip>`.

**Cloudflare (optional).** Ask the user to create a token with the "Edit zone DNS" template and `export CF_API_TOKEN=...` in their shell. Ask before creating the record:

```bash
zone=$(curl -s -H "Authorization: Bearer $CF_API_TOKEN" \
  "https://api.cloudflare.com/client/v4/zones?name=<apex-domain>" | jq -r '.result[0].id')
curl -s -X POST -H "Authorization: Bearer $CF_API_TOKEN" -H "Content-Type: application/json" \
  "https://api.cloudflare.com/client/v4/zones/$zone/dns_records" \
  -d '{"type":"A","name":"<domain>","content":"<ip>","proxied":false,"ttl":300}' | jq '.success'
```

Keep `proxied` false until the certificate exists.

**Any other DNS provider:** tell the user the exact record to add.

Then wait until the record resolves. The certificate cannot be issued before that:

```bash
dig +short <domain> @1.1.1.1     # repeat until it prints <ip>
```

## 3. Install (the user runs this)

Tell the user to run this in their own terminal:

```
ssh -t <user>@<ip> 'curl -fsSL https://fusionaly.com/install | sudo bash -s <domain>'
```

It installs Chasen (and Docker, when the server has none) and runs Fusionaly with HTTPS, live backups of the database, and an update each night. Wait until the user says it finished, then tell them to open https://<domain> and create the first account at once.

## 4. Check

```bash
curl -s -o /dev/null -w "%{http_code}\n" https://<domain>/up    # 200
```

Then the user opens `https://<domain>/setup` to create the admin account and add the first website.

## Done: tell the user

- Dashboard: `https://<domain>/admin`. Add the tracking script shown in the website settings.
- Updates and backups run every night. Keep a copy off the server too (VPS snapshots or rsync).
- Harden a new server: [server-hardener](https://github.com/karloscodes/server-hardener). Run it yourself: `ssh -t <user>@<ip> 'curl -fsSL https://raw.githubusercontent.com/karloscodes/server-hardener/main/harden.sh -o /tmp/harden.sh && sudo bash /tmp/harden.sh'`. If you pick Tailscale, SSH works only over Tailscale afterwards: connect this machine to your tailnet first.
- Ask your analytics from your AI client: https://fusionaly.com/agents/
