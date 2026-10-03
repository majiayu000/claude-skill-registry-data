---
name: ad-methodology
description: >
  The order of operations for an Active Directory penetration test: setup, collection,
  exploitation, post-processing. Use this whenever you are planning or driving an AD
  assessment and need to know what to run before what and why (map before you exploit;
  harvest easy credentials before spraying to avoid lockouts; collect the graph before
  you reason about paths). Covers phase sequencing with standard tooling: netexec/nxc,
  impacket, certipy, bloodyAD, kerbrute, BloodHound CE. Invoke it at the start of an
  engagement, when deciding the next phase, or when a step feels out of order.
---

# AD Pentest Methodology: Phase Order

A domain assessment is not a bag of tricks you run in random order. The order is the
craft. Enumeration feeds exploitation; a credential harvested cheaply saves you a spray
that locks accounts; a graph collected once tells you which of a hundred possible attacks
actually reaches Domain Admin. Run the phases in order and each one narrows the next.

Four phases, in sequence:

1. **Setup**: reachability, name resolution, environment posture, first credentials.
2. **Collection**: topology, trusts, directory objects, hosts, shares. Read, do not touch.
3. **Exploitation**: attack-path discovery, then cheap wins, then spraying, then hunting.
4. **Post-processing**: consolidate loot, re-collect as the owned set grows, report.

The rest of this skill is what happens inside each phase and why that order holds.

---

## Phase 1: Setup

You cannot attack a DC you cannot reach, resolve, or authenticate against. Get these
four things straight before anything else.

### 1.1 Reachability and DNS

The DC is the DNS server for the domain. If your resolver does not point at it,
`corp.local`, `dc01.corp.local` and SRV records will not resolve, and half your tools
fail with confusing errors that look like auth problems.

```bash
# Point resolution at the DC, confirm the domain answers
nslookup -type=SRV _ldap._tcp.dc._msdcs.corp.local <dc_ip>
nxc smb <dc_ip>                      # confirms host up + prints domain/hostname/OS
```

Kerberos also needs FQDNs. Add the DC to `/etc/hosts` (`<dc_ip> dc01.corp.local dc01`)
so short names and IPs both resolve to the canonical FQDN. This one step prevents a
whole class of Kerberos SPN failures later (see `ad-environment-constraints`).

### 1.2 Clock sync

Kerberos rejects tickets when client and DC differ by more than five minutes
(`KRB_AP_ERR_SKEW`). Sync before you touch Kerberos.

```bash
sudo ntpdate <dc_ip>        # or: sudo rdate -n <dc_ip>
```

### 1.3 Environment posture: detect before you authenticate

Fingerprint the environment's hardening before you pick an auth path. Whether NTLM is
disabled, whether the KDC is AES-only, whether LDAP signing / channel binding is
required, whether LDAPS is even listening. Every one of these changes which command
will work and which will silently fail. Probe it first, then choose Kerberos vs NTLM,
LDAPS vs LDAP, RC4 vs AES accordingly. The full catalogue of constraints and how to
read them lives in `ad-environment-constraints`; the point here is that posture
detection belongs in setup, not as an afterthought when a bind fails.

```bash
# Cheap unauthenticated fingerprint of the target surface
nxc smb <dc_ip> --gen-relay-list relaytargets.txt   # SMB signing posture across hosts
nxc ldap <dc_ip>                                     # LDAP/LDAPS reachability + null bind behaviour
```

### 1.4 First credentials

Everything downstream is gated on having *a* foothold identity. Before you assume you
have none, try the credential-free vectors that frequently yield one:

- **Anonymous / null-session enumeration** of users (RID cycling) to build a username list.
- **AS-REP roasting** against accounts with pre-auth disabled: no password needed.
- **Responder / LLMNR-NBNS poisoning** to capture a NetNTLM hash.

```bash
# RID-cycle a user list from a null session, then feed AS-REP roasting
nxc smb <dc_ip> -u '' -p '' --rid-brute > rids.txt
GetNPUsers.py corp.local/ -usersfile users.txt -dc-ip <dc_ip> -no-pass -format hashcat
```

You leave setup with: reachable DC, working resolution, clock in sync, a read on the
posture, and ideally one credential or hash to work with.

---

## Phase 2: Collection

Map before you exploit. This is the rule that separates a professional assessment from
flailing. You collect the entire directory and network picture *first*, reason over it,
and only then act, because the graph tells you which attacks are worth attempting and
which lead nowhere. Collection is read-only: LDAP queries, SAMR lookups, share listings.
Nothing here changes state on the target.

### 2.1 Topology and trusts

Before enumerating one domain, learn the shape of the forest. A trust can make a
credential from domain A the key to domain B, and a path that looks blocked inside one
domain is trivial across a trust.

```bash
nxc ldap <dc_ip> -u user -p pass -M enum_trusts
nxc ldap <dc_ip> -u user -p pass --dc-list      # enumerate DCs in the domain
```

### 2.2 Directory collection: the BloodHound graph

Collect the object graph once, in full. Users, groups, computers, ACLs, sessions, GPOs,
delegation: this is the single most valuable artifact of the engagement, because attack
paths are computed *from* it. BloodHound CE (Apache-2.0, genuinely open source) ingests
the collector output and lets you query low-priv → Domain Admin routes.

```bash
# Python collector (bloodhound-ce-py): LDAP + SMB collection into JSON for BloodHound CE
bloodhound-ce-python -u user -p pass -d corp.local -ns <dc_ip> -c All --zip

# or netexec's built-in BloodHound module
nxc ldap <dc_ip> -u user -p pass --bloodhound --collection All --dns-server <dc_ip>
```

Request only the attributes you need and spread queries over time. BloodHound-style
collection has a well-known LDAP signature that MDI and ATA detect (see
`ad-opsec-telemetry`).

### 2.3 LDAP / SAMR / shares

Fill in the detail the graph does not capture on its own:

```bash
# Users, descriptions (passwords are routinely left in the description field), pwd policy
nxc smb <dc_ip> -u user -p pass --users
nxc ldap <dc_ip> -u user -p pass -M get-desc-users
nxc smb <dc_ip> -u user -p pass --pass-pol            # read lockout threshold BEFORE spraying

# Share inventory across the estate
nxc smb <targets> -u user -p pass --shares
```

Reading the password policy here is not optional. The lockout threshold you learn in
this phase is what makes spraying safe in the next one.

### 2.4 Host and identity inventory

Port-scan the in-scope range, inventory which hosts run SMB/WinRM/RDP/MSSQL, and record
reachability so the exploitation phase does not waste workers on dead hosts.

```bash
nxc smb <cidr> --gen-relay-list live.txt      # live SMB hosts
nxc smb <targets> -u user -p pass             # OS/signing/domain per host, one pass
```

You leave collection with: the trust map, a full BloodHound graph, user/share
inventories, the password policy, and a live-host list.

---

## Phase 3: Exploitation

Now you act, and the order inside this phase matters as much as the phase order itself.

### 3.1 Attack-path discovery first

Before running a single exploit, ask the graph what is reachable. Mark the identities you
already control as owned in BloodHound and query shortest paths to Domain Admins, to
Tier-0 assets, and to any high-value target. This turns "try everything" into "run the
three techniques that are actually on a path to DA." Reasoning over the graph before
touching a DC is the whole reason collection came first.

### 3.2 Cheap credential wins before spraying

Harvest credentials that cost nothing and lock nothing before you ever send a spray.
These read from data you already collected or query the DC gently:

- **Timeroast**: recover machine-account hashes via NTP (no auth, no lockout risk).
- **LDAP descriptions / userPassword**: passwords left in object attributes.
- **GPP passwords**: the cPassword in `Groups.xml` on SYSVOL, AES-decryptable with a
  published key.
- **GPP autologin**: plaintext autologon creds in registry.pol / SYSVOL.

```bash
# GPP cPassword from SYSVOL: read-only, no lockout risk
Get-GPPPassword.py -no-pass corp.local/ -dc-ip <dc_ip>
nxc smb <dc_ip> -u user -p pass -M gpp_password -M gpp_autologin
```

Every credential you win here is one you did not have to guess, and none of them can
lock an account. Do this before spraying, always.

### 3.3 Spraying: measured, after you know the policy

Only now do you spray, and only because you read the lockout policy in collection.
Spraying blind is how you lock out real accounts and burn the engagement. Try, in order
of decreasing safety:

- **pre2k**: pre-Windows-2000 computer accounts whose password equals the lowercased
  hostname (no user lockout at stake).
- **blank passwords**: accounts with an empty password.
- **username-as-password**: the account name as its own password.
- **credential reuse**: a password you already recovered, sprayed across other accounts.

```bash
# ONE password across all users, staying under the lockout threshold you read earlier
nxc smb <dc_ip> -u users.txt -p 'Winter2026!' --continue-on-success
# check pre2k accounts specifically
nxc smb <dc_ip> -u computers.txt -p '' --pre2k
```

Cap attempts per account below the threshold, and leave a window before lockout resets.
Spraying is a controlled action, not a brute-force.

### 3.4 Share and credential hunting

With more identities in hand, spider the shares you inventoried for secrets: config files
with connection strings, scripts with embedded passwords, KeePass databases, private keys.
Bound the spider by depth, time, and file count per share so you do not run for hours or
trip DLP.

```bash
nxc smb <targets> -u user -p pass -M spider_plus       # controlled recursive share hunt
```

Each new credential feeds back to 3.1: mark it owned, re-query the graph, repeat. The
exploitation phase is a loop, not a straight line: collect, reason, act, re-collect.

---

## Phase 4: Post-processing

- **Consolidate loot**: every credential, hash, ticket, and secret in one place, tagged
  with where it came from and what it unlocks.
- **Re-collect as ownership grows**: a credential that gives you a new session changes the
  graph. Re-run collection so path discovery sees the new reality.
- **Verify the path end-to-end**: confirm the low-priv → Domain Admin route actually
  works, rather than assuming the graph edge is exploitable.
- **Report**: findings, the proven path, evidence, and remediation. Map each technique to
  the compliance controls it touches (see `compliance-mapping`), and document the
  telemetry each step generated so the client can correlate with their own logs (see
  `ad-opsec-telemetry`).

---

## Why this order, in one paragraph

Setup makes the target reachable and gives you a foothold identity. Collection turns the
domain into a graph you can reason over, and reading the password policy here is what
makes later spraying safe. Exploitation starts by asking the graph what is worth doing,
then takes the credentials that cost nothing before the ones that risk lockout, then
sprays only within the known policy, then hunts with every identity gained, looping back
to re-reason each time ownership grows. Post-processing proves the path and writes it up.
Skip a phase or run one out of order and you either miss the path that was in front of
you or lock out the accounts that would have led you to it.
