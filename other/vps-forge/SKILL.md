---
name: vps-forge
description: Set up, harden, audit and polish a Linux VPS (Debian/Ubuntu) to production grade without ever losing access — SSH keys and crypto, firewall, fail2ban/CrowdSec, automatic security updates, kernel hardening, Docker, Caddy/nginx with TLS, WireGuard/Tailscale, restic backups, phone alerts, monitoring and a final verified score. Use this skill whenever the user mentions a VPS, VDS, cloud server, droplet, Hetzner/DigitalOcean/Vultr/Linode/OVH/Oracle Cloud/AWS EC2 or Lightsail box (x86 or ARM), a "fresh server", "secure/harden/lock down my server", SSH hardening, ufw, fail2ban, "set up Docker/Caddy/nginx on my server", preparing a server for Coolify, Dokploy, CapRover or Kamal, server backups or monitoring, or asks to audit or check an existing server — even if they don't say "harden". Not for RHEL/Fedora-family servers, Kubernetes nodes (k3s, kubeadm), Proxmox or other hypervisor hosts, managed or shared hosting without root, or the user's own desktop.
license: MIT
compatibility: Debian 12/13 and Ubuntu 22.04/24.04/26.04 servers, reached over SSH from the agent's machine. Server scripts are bash and run with root or sudo.
---

# VPS Forge

Take a fresh or existing Debian/Ubuntu VPS to a state the user will be proud of: locked down, observable, backed up, documented, reproducible and pleasant to live on. Do it with a safety net under every risky step, so access to the server is never lost.

Speak the user's language. Before every change, say in one line what you are changing and why. When the user asks "why?", answer properly: the reasoning matters more than the command.

## 1. Rules that keep the user safe

These exist because one wrong `sshd` or `ufw` change can make a server unreachable, and the user may have no idea how to use the provider's rescue console.

1. **Never cut off access.** Every SSH, firewall, sudo or PAM change goes inside a dead-man switch: `scripts/deadman.sh arm` → change → validate → test from a **new, unmultiplexed** connection → disarm. If the new connection fails, do nothing and let the timer roll back (default 5 min). Arm longer (`arm 10`) when the change needs several edits or a package install, and if it runs late, `vps-forge-deadman extend <min>` moves the rollback while the snapshot stays the same. Never extend after a failed test login.
   - **Before the first risky step,** make sure the user knows where the provider's web console (VNC/serial) is. Keep the existing session open throughout.
   - **The test must be a new connection.** A plain `ssh host` reuses the live ControlMaster, which never touches the new sshd, port or firewall. Always test with `-o ControlPath=none`.
   - **Disarming.** With NOPASSWD sudo (or the temporary grant) the test is the disarm: `ssh -o ControlPath=none -o BatchMode=yes -p <port> <admin>@<host> 'sudo -n vps-forge-deadman disarm'`. Under password sudo, `sudo -n -v` must fail with `a password is required`, and you disarm from the root session (ssh.md "Test and disarm").
   - **What it covers:** sshd, ufw/nftables/iptables, sudoers and PAM files. It doesn't snapshot WireGuard, Tailscale or netplan config (vpn.md), and it can't undo anything outside the server, such as a provider firewall. There, add the new rule first, prove a new login, and remove the old rule last (firewall.md).
2. **Never ban yourself.** Every test login that might fail counts against fail2ban and ufw `limit`, and a ban on the admin's IP looks exactly like a lockout. The admin's IP goes on every exemption list before anything can count it: fail2ban's `ignoreip`, a ufw allow rule ahead of `limit`, and sshd's `PerSourcePenaltyExemptList` (firewall.md, ssh.md).
   - **The admin's IP** is `$(sudo vps-forge-deadman client-ip)`, because `$SSH_CLIENT` is empty under sudo. Stop if it's empty or not an IP. If you aren't on the user's own machine (cloud sandbox, CI), it's *your* IP: mark every entry (ufw, `ignoreip`, sshd's exempt list) `agent session <date>`, ask for the user's real IP or range, and remove your entries in phase 12.
   - It goes into fail2ban's `ignoreip` **before fail2ban can first start**. Debian 13 and Ubuntu 24.04 start it on install, and on start it re-reads recent journal lines, so your earlier test logins ban the user at once. So: `systemctl mask fail2ban` and write the jail before the phase-2 install, then unmask and enable it in phase 5 (base.md). A runtime `addignoreip` is lost on every restart, and the deadman can't undo a ban (firewall.md).
3. **Look before you touch.** Check the current state first and make each step idempotent. On an existing server, run the read-only audit and get approval before changing anything (see `references/audit-mode.md`).
4. **Every change is recoverable.** Install `etckeeper` early so `/etc` is under git with an auto-commit per change, and commit after each phase with a message (`etckeeper commit "vps-forge: ssh hardening"`). Prefer drop-in files over editing main configs.
5. **Ask before anything irreversible or disruptive**: deleting data or users, removing packages, rebooting, changing the SSH port, disabling password login, enabling auto-reboots, restricting SSH to a VPN. If the user said they are offline or told you to decide yourself, their request is the approval for the standard steps of the chosen level, including turning off password and root login once the admin key login is proven (not root login when root holds deploy keys, ssh.md). Still never delete data or users. Leave anything you skipped as a clear item in the final report.
6. **Secrets never travel through chat.** Generate passwords, keys and tokens on the server, store them with mode 600, and tell the user where they are. If the user pastes a secret anyway, use it, don't repeat it back, and suggest rotating it later.
7. **Don't guess versions.** Behaviour differs between Ubuntu 22.04/24.04 and Debian 12/13 (socket-activated SSH, OpenSSH algorithms, fail2ban backends). Check `/etc/os-release`, `ssh -V`, `ssh -Q kex` and `systemd-detect-virt`, and read `references/distro-notes.md` when anything is unusual.
8. **Stop if the box looks compromised.** Unknown UID-0 accounts, unknown `authorized_keys`, `/etc/ld.so.preload`, miners, `curl | sh` cron entries: stop hardening and follow the compromise section of `references/audit-mode.md`. You can't harden your way out of a breach.

## 2. Operating modes

Pick the mode from what you can actually do in this session:

| Mode | When | How |
|---|---|---|
| **Direct** | You have a shell that can `ssh` to the server | Run commands over SSH with multiplexing (below). This is the best mode. |
| **Script** | No SSH access from here (a chat app) | Recon first, then one small script per stage that the user runs and pastes back; every risky step pauses for a test login from the user's second terminal. Follow `references/script-mode.md`. |
| **Audit** | The user wants a check, not changes, or the server is already in production | Run `scripts/audit.sh` read-only, then produce the findings report. Change nothing until asked. |

**Direct-mode mechanics**
- Multiplex so you don't pay for a handshake per command, and so ufw `limit` won't throttle you: `-o ControlMaster=auto -o ControlPath=~/.ssh/cm-%r@%h:%p -o ControlPersist=10m`. The master outlives sshd and ufw changes, so it never counts as a login test; that always takes `-o ControlPath=none` (rule 1).
- Never run anything that can prompt. Use `export DEBIAN_FRONTEND=noninteractive NEEDRESTART_MODE=a` and `apt-get -y -o Dpkg::Options::=--force-confdef -o Dpkg::Options::=--force-confold`. Use `adduser --disabled-password --gecos ""`. Don't use `dpkg-reconfigure`; write the config files directly.
- Run bundled scripts without copying them by hand: `ssh host 'sudo bash -s -- --flags' < scripts/audit.sh`. Install the helpers that must stay on the server (deadman, alerts) into `/usr/local/sbin/` with `install -m 755`.
- Write files with a heredoc, then validate them (`sshd -t`, `visudo -cf`, `nft -c -f`, `caddy validate`, `nginx -t`, `python3 -m json.tool`).

## 3. Intake (ask at most 4 questions at a time)

You need four answers before starting. Infer whatever you can from the conversation and from the server itself.

1. **Purpose → profile(s):** `web`, `docker`, `vpn`, `db`, `worker` (bots, cron jobs, outbound only), `game`. Profiles combine. For `docker` or `web`, ask whether a deploy panel or tool (Coolify, Dokploy, CapRover, Kamal, Dokku) runs or will run here: it changes root login, the proxy and the firewall (paas.md).
   - **worker** has no inbound ports besides SSH. Run each bot or job as its own unprivileged user under a systemd unit with `Restart=on-failure`, keep its secrets in a 600 env file, and cap its logs.
   - **game** opens exactly the game's ports, often UDP (`ufw allow <port>/udp comment '<game>'`). Run the server as a dedicated non-root user under systemd, and back up its world directory.
2. **Level:** `baseline`, `hardened` (recommend this by default), or `paranoid`. Explain the difference in one sentence each (see §5).
3. **Access today:** host/IP, user (root?), password or key, provider. Does the user have an ed25519 key? If not, have them run `ssh-keygen -t ed25519` locally; FIDO2 is `-t ed25519-sk` if they own a hardware key.
4. **Extras:** domain and DNS (Cloudflare proxied?), where alerts should go (ntfy / Telegram / webhook / none), where backups should go (S3/B2/R2/Storage Box/none yet), timezone (servers default to UTC).

## 4. Workflow

**Match the work to the request.**
- **The whole server** ("set up / secure / harden my server", "make it production-ready", a fresh box with no narrower ask): the full workflow below at the chosen level, `hardened` by default.
- **A narrow request** (move SSH, add fail2ban, create a sudo user, a short checklist of such items): do exactly that, under every safety rule. Making the request safe is part of it, not extra: the admin's IP goes on fail2ban's ignore list before fail2ban starts, and every SSH or firewall change runs inside the deadman. Then offer the rest in one line, naming the concrete gaps the audit found ("SSH crypto fails ssh-audit and there is no firewall: want the hardened baseline too?"). Don't apply it unasked.
- **"I'm offline, decide yourself"** settles questions inside the request. It doesn't widen a narrow request: put the offer in the final report instead.

Create a task list from the phases below, trimmed to the chosen profile and level. Show the user a short plan, then go. After each phase, append a line to `/var/lib/vps-forge/progress.log` (`date phase=ssh status=done`) and commit with etckeeper, so an interrupted run can resume where it stopped.

| # | Phase | Read | Key outcome |
|---|---|---|---|
| 0 | Recon | `scripts/audit.sh` | Facts, a baseline score, and red flags spotted before any change. Stop on a Kubernetes node, a hypervisor host or a non-Debian/Ubuntu system (distro-notes.md). Coolify, Dokploy, CapRover, Kamal or Dokku found or planned: read `references/paas.md` before phase 3 |
| 1 | Safety net | `references/base.md` §Safety net | Provider snapshot, console known, etckeeper on, deadman installed |
| 2 | Base system | `references/base.md` | Non-interactive full upgrade, unattended security updates, time sync, swap, journald limits, hostname that survives reboots |
| 3 | Admin user & SSH | `references/ssh.md` | Admin user with a key, sudo policy chosen, root login and passwords off, modern crypto, verified from a new session |
| 4 | Firewall | `references/firewall.md` | Default deny, only explained ports open, IPv6 matched, Docker gap closed, provider firewall considered |
| 5 | Brute-force defence | `references/firewall.md` §fail2ban | fail2ban unmasked and started with the systemd backend (or CrowdSec), detection and ban action proven |
| 6 | Kernel & OS hardening | `references/kernel.md` | sysctl set, AppArmor on, unused services off, BBR |
| 7 | Workload | `references/docker.md`, `web.md`, `vpn.md`, `databases.md` | Per profile |
| 8 | Backups | `references/backups.md` | restic on a timer, dumps first, protected against deletion, **restore tested** |
| 9 | Alerts & monitoring | `references/alerts-monitoring.md` | Phone alerts, heartbeat, external uptime check |
| 10 | Comfort | `references/comfort.md` | Status motd, sane shell, useful tools |
| 11 | Verify | `scripts/audit.sh`, `scripts/external-check.sh`, base.md §Reboot drill | Score before → after, external scan clean, every listening port explained, reboot drill passed (with the user's OK) |
| 12 | Document & hand off | `assets/SERVER.md`, `references/reproducibility.md`, ssh.md §Hand-off cleanup | `/root/SERVER.md` and the final report, agent-session entries and the temporary sudo grant removed; offer the cloud-init/Ansible export, and build it only if the user wants it |

Do the alerts phase near the end. Otherwise the SSH-login alert fires for every connection you make during setup.

**Keep it fast without skipping safety:**
- Install all packages for the chosen profiles in one `apt-get install` in phase 2 (base.md).
- Batch read-only checks into one SSH call.
- Read only the reference the current phase needs.

Never merge deadman windows across unrelated changes: when a combined change fails, you can't tell which part broke.

## 5. Levels

| | baseline | hardened (default) | paranoid |
|---|---|---|---|
| SSH | keys only, no root, `AllowGroups`, MaxAuthTries 5 | + modern KEX/ciphers/MACs, ed25519 host key only, ssh-audit clean | + FIDO2 keys or TOTP, SSH reachable only via WireGuard/Tailscale |
| Firewall | ufw default deny, needed ports only | + IPv6 parity, Docker DOCKER-USER rules, provider firewall as a second layer | + Cloudflare-only 80/443 or Cloudflare Tunnel, egress review |
| Intrusion | fail2ban sshd, incremental bans | + recidive jail (SSH port, 1 day) | CrowdSec with a firewall bouncer |
| Updates | unattended security updates | + needrestart auto, Livepatch (Ubuntu Pro) where supported | + scheduled auto-reboot window |
| OS | sysctl baseline, swap, journald cap | + etckeeper, AppArmor check, BBR, unused services off | + auditd, AIDE, `/dev/shm` noexec, core dumps off |
| Backups | restic daily + tested restore | + versioned or append-only repo, weekly `restic check` | + second off-site repo, quarterly restore drill |
| Alerts | external uptime check | + phone alerts: SSH login, failed units, disk, reboot needed; backup heartbeat | + fail2ban/CrowdSec digest |
| Proof | final audit | + Lynis, ssh-audit, testssl/securityheaders | + all of it, scores recorded in SERVER.md |

A level is a starting point. If the user wants "hardened, but keep password sudo", do exactly that.

## 6. Definition of done

Don't call the server done until every applicable item is true and you have shown the evidence:

- [ ] A new SSH session as the admin user works; `ssh root@host` and password login are rejected (shown by `external-check.sh --root-test`, run after whitelisting the user's IP in fail2ban: every probe counts as a failed login)
- [ ] `sshd -T` shows the intended values; nothing in `sshd_config.d/` overrides them
- [ ] The firewall is active with default deny; **every** port in `ss -tulpn` and in `docker ps` is listed in SERVER.md with a reason
- [ ] fail2ban (or CrowdSec) is running and its sshd jail is active
- [ ] Unattended upgrades are enabled; `unattended-upgrade --dry-run` runs without errors
- [ ] Backups run on a timer and a test restore succeeded (or the user knowingly postponed this, which is recorded in SERVER.md)
- [ ] Alerts reach the user's phone (a test message was received) and an external uptime check exists, or the user declined
- [ ] `audit.sh` has no FAIL; the score before → after is reported
- [ ] `/root/SERVER.md` is written and the user has a local copy; etckeeper holds the full history
- [ ] The deadman is disarmed and no temporary sudo or firewall exceptions are left behind

## 7. Final report

End with a short message in the user's language:

1. **Result:** the score before → after, and what changed, in 5–8 bullets.
2. **How to get in:** `ssh <admin>@<host> -p <port>`, the `~/.ssh/config` block with `IdentitiesOnly yes` (ssh.md), and where the provider console is.
3. **What only the user can do:** for example save the key, sudo and backup passwords offline, enable provider snapshots, confirm they received the test alert. Name anything you left on purpose, such as root login kept for a deploy key (ssh.md).
4. **Next 1–2 improvements** worth doing later.

Offer the export from `references/reproducibility.md` (cloud-init or Ansible) so the next server comes out identical.

## 8. Reference map

Read only what the current phase needs.

- `references/base.md`: packages, non-interactive apt, unattended-upgrades, needrestart, time, swap/zram, journald, hostname vs cloud-init, Ubuntu Pro/Livepatch, etckeeper, safety net
- `references/ssh.md`: admin user, sudo policy, the drop-in ordering trap, crypto, port change with socket activation, FIDO2/TOTP, cleanup of provider keys
- `references/firewall.md`: ufw, IPv6, Cloudflare allowlists, Docker vs ufw, provider firewalls, fail2ban, CrowdSec
- `references/kernel.md`: sysctl (and when not to), AppArmor, services, BBR, paranoid extras
- `references/docker.md`, `references/web.md`, `references/vpn.md`, `references/databases.md`: workload profiles
- `references/paas.md`: Coolify, Dokploy, CapRover, Kamal and Dokku: root key login, the panel's own SSH, its proxy and dashboard ports, what to back up
- `references/backups.md`: restic, DB dumps, deletion-resistant repos, restore drills
- `references/alerts-monitoring.md`: phone alerts, heartbeats, uptime checks, metrics
- `references/comfort.md`: motd, shell, tools
- `references/audit-mode.md`: read-only audits, severity rubric, findings format, compromise response
- `references/reproducibility.md`: SERVER.md, cloud-init and Ansible export
- `references/distro-notes.md`: Ubuntu 22.04/24.04, Debian 12/13 differences, containers (OpenVZ/LXC), ARM
- `references/script-mode.md`: no SSH from here: recon, stage scripts, the test-and-disarm pause
- `references/troubleshooting.md`: locked out, cloud-init overrides, fail2ban won't start, Docker ignores ufw, and more

**Scripts** (all idempotent; `--help` on each):
- `scripts/audit.sh`: read-only audit with PASS/WARN/FAIL, a score and optional `--json`; exits 1 on any FAIL. Used in phase 0 and phase 11.
- `scripts/deadman.sh`: `arm [minutes] [--ip addr]` / `extend <minutes>` / `disarm` / `status` / `restore` / `client-ip` (the calling SSH client's address, also under sudo). Snapshots SSH, firewall and sudoers config and rolls back automatically unless disarmed, also after a reboot. The rollback unbans the arming SSH client (or `--ip`) in fail2ban. `disarm` exits 3 with `ROLLED BACK` when the rollback already ran: the change was not kept.
- `scripts/external-check.sh`: runs on the **user's machine**. Checks open ports, offered SSH auth methods, admin login, TLS and headers for a domain; `--root-test` and `--ssh-audit` are opt-in because they add failed logins. They are harmless when the user's IP is in fail2ban's `ignoreip` (firewall.md); if it isn't, add it first.
- `scripts/install-alerts.sh`: installs `vps-notify` (ntfy/Telegram/webhook), SSH-login alerts, and a 5-minute health timer (failed units, disk, inodes, reboot-required, heartbeat).

**Assets:** config templates in `assets/` (sshd, sysctl, fail2ban, unattended-upgrades, needrestart, journald, docker, Caddyfile, restic units, motd, SERVER.md, cloud-init). Copy a template, fill in the `<placeholders>`, then validate it.
