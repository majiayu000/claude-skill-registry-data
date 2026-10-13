---
name: privesc-enumeration
description: >
  Systematic post-foothold host enumeration and credential/loot hunting on Linux and Windows —
  build situational awareness and find the lead that escalates or moves laterally. Load the moment
  you land a shell and think "now what?". Signals: fresh foothold, low-priv user, "enumerate the
  box", "situational awareness", hunting configs/history/creds, before running exploit tooling.
domain: privesc
type: methodology
stability: learning
modes: [pentest]
severity: info
mitre: [T1082, T1083, T1552, T1555]
cwe: [CWE-522, CWE-200]
tools: [linpeas, winpeas, pspy, seatbelt]
schema_version: 1
---

# Post-foothold enumeration & credential hunting

## When it applies
You have a shell as a low-privileged user and need to know what you're standing on and where to go
next. This is the situational-awareness pass that *precedes* escalation: it surfaces the leads that
`privesc-arsenal` (local privesc vectors) and `ad-pivot-arsenal` (domain) then exploit. On Windows
run `whoami /priv` and on Linux `sudo -l` first — an enabled privilege or sudo rule is a shortcut
past all of this.

## Why it works
Machines leak their own secrets: config files hold DB and service passwords, history files record
typed credentials, home directories and shares carry keys, and the OS records who runs what. A
methodical sweep — then a targeted grep for secrets — finds the reused password or private key that
turns one foothold into root/SYSTEM or the next host. Enumerate before you exploit; noise and dead
ends come from skipping this.

## Method
Work top-down; note every lead in `notes.md` and follow the strongest one.

**1 · Who/where am I** — `id`/`whoami /all`, groups (a `docker`/`lxd`/`adm` group or
`SeImpersonate`/`SeBackup` privilege is often the whole game), hostname, OS/kernel/patch level
(`uname -a` / `systeminfo`), and am-I-in-a-container (`/proc/1/cgroup`, `/.dockerenv`).

**2 · Automated first pass** (then read the output, don't scroll it):
`linpeas.sh > lp.txt` / `winPEASx64.exe`, plus `pspy64` (Linux, catches root cron without root) and
`Seatbelt.exe -group=all` / PowerUp (Windows). Treat highlights as leads to verify.

**3 · Users, processes, services, scheduled jobs** — other users (`/etc/passwd`, `net user`),
running processes and their owners (`ps auxf` / `tasklist /v`), services (esp. unquoted paths / weak
perms on Windows), and cron/systemd-timers / scheduled tasks. A privileged process reading a file
you can write is a lead.

**4 · Network & internal reach** — listeners bound to `127.0.0.1` (`ss -tulnp` / `netstat -ano`)
are internal services to port-forward to; ARP/routes/extra NICs reveal a pivot
(`network-pivoting-tunneling`).

**5 · Hunt credentials & loot — the highest-yield step:**
- **Config files:** web roots and app configs (`grep -ri "password\|DB_PASS\|secret" /var/www /opt 2>/dev/null`),
  `.env`, `wp-config.php`, `web.config`, `*.conf`, connection strings.
- **History:** `~/.bash_history`, `~/.mysql_history`, `~/.psql_history`; Windows PowerShell history
  (`ConsoleHost_history.txt`).
- **Keys & secrets:** `find / -name id_rsa -o -name "*.pem" -o -name "*.key" 2>/dev/null`,
  `~/.ssh/`, cloud creds (`~/.aws/credentials`), Kubernetes `~/.kube/config`, tokens.
- **Windows stores:** `cmdkey /list` (+ `runas /savecred`), autologon/PuTTY/VNC in the registry,
  `unattend.xml`/`sysprep.inf`/GPP `Groups.xml`, `netsh wlan show profile name=* key=clear`,
  DPAPI/browser creds, and `C:\Windows\System32\config\RegBack\` (SAM/SYSTEM copies).
- **Databases:** local DB running as root/SYSTEM you can log into with found creds.

**6 · Files of interest** — recently modified files (`find / -mmin -10`), backups (`*.bak`/`*.old`),
readable `/etc/shadow`, writable files/dirs in privileged paths, and Windows Alternate Data Streams
(`dir /r`).

**7 · Route the lead** — cracked/found password → try it everywhere (reuse is rampant;
`network-password-spraying`); crackable hash/keyfile → `network-credential-cracking`; escalation
vector → `privesc-arsenal`; domain context → `ad-pivot-arsenal`.

## Gotchas
- **Read linpeas/winPEAS output, don't drown in it** — pipe to a file and grep the red/yellow flags.
- **Password reuse is the #1 pivot** — always retry a found secret as other users/services/root
  (`su`, WinRM, SMB) before hunting harder.
- **`noexec`/`nosuid` mounts** change what works — check `mount` before dropping a binary.
- **Enumerate quietly on a live/bounty-adjacent host** — heavy `find /` and linpeas are noisy; pace
  them and stay in RoE.
- **Don't hoard** — pull the one cred/keyfile that advances you into `engagements/<target>/loot/`,
  not whole home directories.

## Verify success
A concrete next-step lead in hand — a working credential, a private key, an internal service to
tunnel to, or a confirmed escalation vector — recorded with where it came from.

## References
HackTricks (Linux/Windows local privesc checklists); PEASS-ng; `pspy`, `Seatbelt`.
Exploit the leads with `privesc-arsenal`; domain leads with `ad-pivot-arsenal`.
