---
name: set-up-ionos-vps
description: Use when taking over or hardening a self-hosted IONOS VPS (Cloud Panel, not IONOS Cloud) on Debian — SSH keys, Cloud Panel firewall policy, updates, swap, backups — or pointing IONOS domains and subdomains at it with DNS records and TLS.
---

# Set up an IONOS VPS

An IONOS **VPS** is the flat-rate server managed in the IONOS Cloud Panel. It is a different product from **IONOS Cloud** (datacenters, LANs, ENTERPRISE servers, OpenTofu), which [deploy-to-ionos](../deploy-to-ionos/SKILL.md) covers. A VPS has no tofu provider and no cloud-init: it arrives with a root password, and the hardening runs over SSH. This skill makes a fresh VPS safe to expose, gives it a role that fits its size, and points domains at it. Rules and reasons: [vps-hardening-patterns.md](./vps-hardening-patterns.md), [dns-patterns.md](./dns-patterns.md).

## 1. Audit current state (change nothing)

```bash
cat .claude/stack-profile.md 2>/dev/null            # hosting, domains
ls ops/inventory.md infra/inventory.md 2>/dev/null  # the private host and domain list
ssh -o BatchMode=yes root@<ip> true 2>&1            # "Permission denied" = no key yet
ssh -o BatchMode=yes <admin>@<ip> 'sudo sshd -T | grep -E "^(permitrootlogin|passwordauthentication) "; swapon --show; systemctl is-active fail2ban unattended-upgrades'
dig +short A <domain>; dig +short CAA <domain>; dig +short TXT <domain>
```

Never ask for the root password and never type it into a command. The person runs `ssh-copy-id root@<ip>` and enters it themselves (in Claude Code: `! ssh-copy-id root@<ip>`). Check API keys by name only (`IONOS_API_KEY`), never print a value.

## 2. Decide

- `BatchMode` login as root fails → step 4 first: the key is missing.
- Admin login works, `permitrootlogin no`, `passwordauthentication no`, swap on, fail2ban and unattended-upgrades active → hardening is "already in place"; go to step 6 for DNS, or stop.
- Some of it present → run [harden-host.sh](./harden-host.sh) anyway: it is idempotent and only adds what is missing.
- DNS records and CAA match the inventory → "already in place".

## 3. Pick the role by size

The VPS size decides what it may run. Table and reasons in [vps-hardening-patterns.md](./vps-hardening-patterns.md#rule-the-size-decides-the-role):

| RAM | Fits | Does not fit |
|---|---|---|
| 1 GB | Outside watcher (uptime and TLS checks, status page, heartbeats, ntfy), WireGuard bastion, small reverse proxy, a static site | Telemetry backends (SigNoz, LGTM), Postgres for real load, CI runners, any LLM |
| 2–4 GB | One Compose app with Postgres and Traefik, light metrics and logs (VictoriaMetrics + VictoriaLogs + Grafana) | SigNoz/ClickHouse, a 7B+ model |
| 8 GB+ | The app stack of [deploy-to-hetzner](../deploy-to-hetzner/SKILL.md)'s Compose contract, SigNoz | Several environments on one box |

Put the monitor at a different provider from the thing it watches.

## 4. Get in with a key, then lock the door

1. Person: `ssh-copy-id -i ~/.ssh/<key>.pub root@<ip>`.
2. Run the hardening (admin user, sshd lock-down, unattended upgrades, fail2ban on the journal, swap, journal cap):
   ```bash
   ssh root@<ip> 'ADMIN_USER=admin SWAP_MB=2048 bash -s' < harden-host.sh
   ```
   For a deploy user with a forced command ([deploy-script.md](../_shared/deploy-script.md)), create it first and pass `EXTRA_SSH_USERS=deploy`.
3. **Keep the root session open** and prove the new door in a second terminal: `ssh admin@<ip> sudo true`. Only then close the first session. If it fails, the Cloud Panel's KVM console is the way back in.

## 5. Firewall: the Cloud Panel policy is the real one

In the Cloud Panel under Network → Firewall Policies, give each VPS a policy that allows only TCP 22, 80, 443 inbound (and 51820/UDP for WireGuard if used). Remove default rules you do not need. Docker publishes ports past ufw/nftables on the host; the panel policy sits in front of the server, so a container port cannot get past it. Details and the port 25 block: [vps-hardening-patterns.md](./vps-hardening-patterns.md#rule-the-cloud-panel-policy-is-the-firewall-docker-bypasses-the-host-one).

## 6. Domains and subdomains

A subdomain added in the IONOS panel comes with a parking `A`, an `AAAA`, two `MX` and an SPF record: delete them first. Then, per hostname in the inventory: one `A` record (plus `AAAA` if the VPS has IPv6) to the VPS, set in the IONOS DNS for the domain. Add `CAA`, and the null-mail records (`SPF -all`, `DMARC p=reject`, null `MX`) on every name that sends no mail. TLS through Traefik with HTTP-01 by default; DNS-01 through the IONOS Hosting API only for wildcards or hosts that are not public. All rules: [dns-patterns.md](./dns-patterns.md).

## 7. Verify

```bash
ssh -o PasswordAuthentication=no -o PubkeyAuthentication=no root@<ip>    # Permission denied (publickey).
ssh admin@<ip> 'sudo sshd -T | grep -E "^(permitrootlogin|passwordauthentication) "'  # no / no
ssh admin@<ip> 'sudo fail2ban-client status sshd; swapon --show; systemctl is-active unattended-upgrades'
nc -zv -w3 <ip> 5432 || echo "closed: good"                           # any port not in the policy
dig +short A <host>.<domain>                                           # the VPS IP
curl -sI https://<host>.<domain> | head -1                             # HTTP/2 200 (once a service runs)
```

**Exercised while writing this skill:** `harden-host.sh` ran twice in a `debian:trixie` container (openssh-server, fail2ban): second run changed nothing, `sshd -T` showed `permitrootlogin no` and `passwordauthentication no` although a `50-cloud-init.conf` set `PasswordAuthentication yes`; `fail2ban-client -t` passed; shellcheck clean. **Run on a live IONOS VPS (1 vCPU, 854 MB usable RAM, Debian 13, 2026-10-22):** the image shipped `50-cloud-init.conf` with `PasswordAuthentication yes`; after the script `sshd -T` showed `no`/`no`, root got refused, a password login got `Permission denied (publickey)`, `admin` had passwordless sudo, fail2ban and unattended-upgrades were active, 2 GB swap was on. **Not exercised:** the Cloud Panel policy, the KVM console, the IONOS DNS API.

## References
- [vps-hardening-patterns.md](./vps-hardening-patterns.md): SSH, firewall, updates, swap, logs, backups, sizing, inventory; when to deviate.
- [dns-patterns.md](./dns-patterns.md): records per subdomain, TTL, CAA, null mail, rDNS, ACME HTTP-01 vs DNS-01, the IONOS Hosting DNS API.
- [harden-host.sh](./harden-host.sh): the idempotent first-boot script.
- [deploy-to-hetzner](../deploy-to-hetzner/SKILL.md) and [compose-patterns.md](../deploy-to-hetzner/compose-patterns.md): the Compose stack and Traefik once the box runs an app; [deploy-script.md](../_shared/deploy-script.md), [manage-secrets](../manage-secrets/SKILL.md), [hosting-decision.md](../_shared/hosting-decision.md).
- [security-baseline.md](../../core/_shared/security-baseline.md).
