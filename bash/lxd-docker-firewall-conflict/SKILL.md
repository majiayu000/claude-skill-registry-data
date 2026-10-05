---
name: lxd-docker-firewall-conflict
description: 'Diagnose and fix the well-known Docker/LXD firewall conflict on a host running both. Docker sets the iptables FORWARD chain policy to DROP and accepts only its own bridges, so forwarded traffic from the LXD bridge (lxdbr0) is silently dropped and LXD containers/VMs get no outbound internet (the host itself is fine). Fix: accept the LXD bridge in the DOCKER-USER chain, then persist it with a systemd unit ordered after docker.service. Use when an LXD container has no internet or cannot reach archive.ubuntu.com, when "apt update"/"apt-get"/"curl" inside an LXD container times out or reports "Network is unreachable" / "connection timed out" / "Failed to fetch" (but the same works on the host), when a packer-lxd image build fails during "apt update", when LXD container networking breaks right after installing Docker, or when iptables shows "policy DROP" on FORWARD with an empty DOCKER-USER chain. The LXD bridge already has ipv4.nat=true and net.ipv4.ip_forward=1 — it is purely a FORWARD-chain drop, not a NAT or DNS problem.'
---

# LXD ↔ Docker firewall conflict (FORWARD DROP)

When Docker and LXD share a host, **Docker sets the iptables `FORWARD` chain policy to `DROP`** and only
ACCEPTs traffic for its own bridges. Forwarded packets from the LXD bridge (`lxdbr0`) match nothing and fall
through to the DROP policy, so **LXD containers/VMs lose all outbound internet** — even though the host itself
is fine and the LXD bridge has `ipv4.nat=true`. The fix is to ACCEPT the LXD bridge in Docker's `DOCKER-USER`
chain and persist it.

⚠️ This is **not** a NAT, DNS, or LXD-config problem. The bridge's `ipv4.nat=true` and `net.ipv4.ip_forward=1`
are already correct — packets are dropped at the `FORWARD` hook before NAT ever applies. Don't waste time
reconfiguring the bridge, DNS, or `lxd init`.

## Quick start

```bash
# Detects managed LXD bridges, adds DOCKER-USER ACCEPT rules, and installs a
# systemd unit so they survive reboots + docker restarts. Idempotent; re-runnable.
bash scripts/fix-lxd-docker-forward.sh
```

## Symptoms

- Inside an LXD container, `apt update` / `apt-get` / `curl` **times out** on IPv4 (`connection timed out`,
  `Failed to fetch`) and/or instantly says `Network is unreachable` on IPv6.
- The **exact same request works on the host.**
- A `packer-lxd` image build errors in its first shell provisioner at `apt update` → `Failed to fetch ...
  Could not connect ... connection timed out`.
- It began right after **Docker was installed** on the LXD host (or after a Docker upgrade re-applied rules).

## Diagnose (3 checks)

```bash
# 1. Host reaches the internet but the container does not -> forwarding/firewall, not DNS/NAT.
curl -4 -sI http://archive.ubuntu.com | head -1            # host: "HTTP/1.1 200 OK"

# 2. The smoking gun: FORWARD policy DROP + Docker jumps, and DOCKER-USER does NOT accept the LXD bridge.
sudo iptables -S FORWARD            # -> "-P FORWARD DROP"  and  "-A FORWARD -j DOCKER-USER"
sudo iptables -S DOCKER-USER        # -> only "-N DOCKER-USER" (empty): nothing accepts lxdbr0
sudo iptables -L FORWARD -n -v | head -3   # the "policy DROP" pkt/byte counter climbs while a container retries

# 3. Prove the bridge is fine (rules out the usual red herrings).
lxc network get lxdbr0 ipv4.nat     # -> true
sysctl net.ipv4.ip_forward          # -> net.ipv4.ip_forward = 1
```

If `FORWARD` is `policy DROP` with Docker jumps and `DOCKER-USER` has no `lxdbr0` ACCEPT, it's this bug.

## Fix

Docker reserves the `DOCKER-USER` chain — evaluated **first** in `FORWARD` and **never flushed by Docker** —
for exactly this. Accept the LXD bridge in both directions:

```bash
sudo iptables -I DOCKER-USER -i lxdbr0 -j ACCEPT   # container -> internet
sudo iptables -I DOCKER-USER -o lxdbr0 -j ACCEPT   # replies   -> container
```

Replace `lxdbr0` with your managed bridge name if different (`lxc network list` shows `MANAGED=YES` bridges).

## Persist across reboots

Manually-added rules are **lost on reboot** (Docker recreates `DOCKER-USER` empty at boot). **Do not reach for
`iptables-persistent` / `netfilter-persistent` here** — it snapshots Docker's volatile per-container rules and
races Docker's own boot-time setup. Instead use a tiny oneshot unit ordered **after** `docker.service` that
idempotently re-inserts only our rules (this is what the Quick-start script installs):

```ini
# /etc/systemd/system/lxd-docker-forward.service
[Unit]
Description=Persist LXD bridge ACCEPT rules in Docker's DOCKER-USER chain
After=docker.service
Wants=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
ExecStart=-/usr/sbin/iptables -N DOCKER-USER
ExecStart=/bin/sh -c '/usr/sbin/iptables -C DOCKER-USER -i lxdbr0 -j ACCEPT 2>/dev/null || /usr/sbin/iptables -I DOCKER-USER -i lxdbr0 -j ACCEPT'
ExecStart=/bin/sh -c '/usr/sbin/iptables -C DOCKER-USER -o lxdbr0 -j ACCEPT 2>/dev/null || /usr/sbin/iptables -I DOCKER-USER -o lxdbr0 -j ACCEPT'

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload && sudo systemctl enable --now lxd-docker-forward.service
```

## Verify

```bash
lxc launch ubuntu:24.04 nettest
lxc exec nettest -- curl -4 -sI http://archive.ubuntu.com | head -1   # "HTTP/1.1 200 OK"
lxc delete -f nettest
```

Prove persistence actually rebuilds the rules (simulates a fresh boot's empty chain). ⚠️ Briefly drops LXD
container connectivity — run only when no LXD instances need the network:

```bash
sudo iptables -F DOCKER-USER                            # empty it, as at boot
sudo systemctl restart lxd-docker-forward.service
sudo iptables -S DOCKER-USER                            # the two ACCEPT rules are back
```

## Why (nftables semantics)

On modern Ubuntu both Docker (`iptables-nft`) and LXD (its own `inet lxd` table) attach base chains to the
kernel's `forward` netfilter hook. A packet must survive **every** base chain at that hook: LXD can `accept`
in its own table, but Docker's `ip filter` `FORWARD` chain with `policy drop` then drops it anyway (in
nftables, one chain's `accept` does not override another chain's `drop` at the same hook). Placing an `ACCEPT`
in `DOCKER-USER` (part of the `ip filter` table) resolves *that* table's verdict to accept, so the packet is
no longer dropped. NAT (`ipv4.nat=true`) lives in the `nat` table at a *different* hook and never runs because
the packet is already gone at `forward`.

## Notes & gotchas

- **IPv6 noise:** `lxdbr0` defaults to `ipv6.address=none`, so the instant `Network is unreachable` on IPv6
  in logs is harmless — the real failure is the IPv4 timeout. If you enable IPv6 on the bridge, the same rules
  apply (the script covers every managed bridge, both directions).
- **Renamed / multiple bridges:** the script auto-detects all `MANAGED=YES` bridges; override with
  `BRIDGES="lxdbr0 lxdbr1" bash scripts/fix-lxd-docker-forward.sh`.
- **Docker restarts** preserve `DOCKER-USER` contents, so the rules survive `systemctl restart docker`; only a
  reboot empties the chain — which the systemd unit handles.
- **Same class of bug** hits *any* non-Docker bridge on a Docker host (libvirt `virbr0`, Incus, plain
  `brctl`/netplan bridges): same `DOCKER-USER` fix, just a different interface name.
- **Alternative (not recommended):** `"iptables": false` in `/etc/docker/daemon.json` stops Docker managing
  the firewall entirely, but then you own all of Docker's NAT/port rules yourself. The `DOCKER-USER` approach
  is the supported one.
