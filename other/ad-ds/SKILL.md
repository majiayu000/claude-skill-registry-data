---
name: ad-ds
description: "Expert agent for Active Directory Domain Services across all versions. Provides deep expertise in AD architecture, replication, FSMO roles, Group Policy, Kerberos, LDAP, tiered administration, and AD hardening. WHEN: \"Active Directory\", \"AD DS\", \"domain controller\", \"FSMO\", \"Group Policy\", \"GPO\", \"replication\", \"dcdiag\", \"repadmin\", \"NTDS\", \"Kerberos\", \"LDAP\", \"trust\", \"LAPS\", \"gMSA\", \"AD hardening\"."
license: MIT
---

# Active Directory Domain Services

This skill covers Active Directory Domain Services (AD DS) across all supported Windows Server versions (2016 through 2025). It has deep knowledge of:

- AD DS architecture (NTDS.dit, replication, sites and subnets, partitions)
- FSMO roles and their operational impact
- Multi-master replication topology and troubleshooting
- Group Policy processing, inheritance, and troubleshooting
- Kerberos and NTLM authentication
- Trust types and cross-forest authentication
- AD hardening and tiered administration model
- LAPS, gMSA, Protected Users, Authentication Policies/Silos
- AD recycle bin, fine-grained password policies, managed service accounts

This skill's coverage spans AD DS holistically. When a question is version-specific, read the matching file in `references/versions/`. When the version is unknown, apply general guidance and note where behavior differs across versions.

## How to Approach Tasks

When you receive a request:

1. **Classify** the request type:
   - **Troubleshooting** -- Load `references/diagnostics.md` for repadmin, dcdiag, event ID reference
   - **Architecture** -- Load `references/architecture.md` for AD DS internals
   - **Hardening / Security** -- Load `references/best-practices.md` for tiered admin, GPO hardening
   - **Administration** -- Apply AD DS expertise directly
   - **Migration / Upgrade** -- Load the relevant `references/versions/<v>.md` files for source and target versions

2. **Identify version** -- Determine the forest/domain functional level and Windows Server version. If unclear, ask. Functional level determines available features.

3. **Load context** -- Read the relevant reference file for deep knowledge.

4. **Analyze** -- Apply AD DS-specific reasoning, not generic directory advice.

5. **Recommend** -- Provide actionable, specific guidance with PowerShell examples where applicable.

6. **Verify** -- Suggest validation steps (dcdiag, repadmin, event log checks).

## Core Expertise

### AD DS Architecture

AD DS is a multi-master replicated directory built on the Extensible Storage Engine (ESE). The database file is `NTDS.dit`, stored by default at `C:\Windows\NTDS\`.

**Directory partitions:**

| Partition | Replication Scope | Contents |
|---|---|---|
| Schema | Forest-wide | Object class and attribute definitions |
| Configuration | Forest-wide | Sites, subnets, services, replication topology |
| Domain | Domain-wide | Users, groups, computers, OUs, GPOs |
| Application | Configurable | DNS zones (ForestDnsZones, DomainDnsZones), custom |

**Object model:** Every AD object has a globally unique `objectGUID`, a security-aware `objectSid` (for security principals), and a `distinguishedName` (DN) reflecting its position in the hierarchy.

### FSMO Roles

Five Flexible Single Master Operations roles that break the multi-master model for specific operations:

| Role | Scope | Hosted On | Purpose | Impact if Unavailable |
|---|---|---|---|---|
| **Schema Master** | Forest | One DC | Schema modifications | Cannot extend schema (rare operation) |
| **Domain Naming Master** | Forest | One DC | Add/remove domains | Cannot add/remove domains (rare) |
| **PDC Emulator** | Domain | One DC per domain | Password changes, time sync, GPO editor, account lockout | Authentication failures, time drift, GPO edit issues |
| **RID Master** | Domain | One DC per domain | Allocates RID pools for SID creation | Cannot create new objects when RID pool exhausted |
| **Infrastructure Master** | Domain | One DC per domain | Cross-domain reference updates | Stale group membership display (multi-domain only) |

**Operational guidance:**
- PDC Emulator is the most operationally critical role -- place it on your strongest DC
- Schema Master and Domain Naming Master can co-exist on the same DC
- Infrastructure Master should NOT be on a Global Catalog server (unless all DCs are GCs)
- Use `netdom query fsmo` or `Get-ADForest`/`Get-ADDomain` to identify role holders
- Seize roles only when the original holder is permanently offline

### Replication

AD DS uses multi-master replication with a pull model. The Knowledge Consistency Checker (KCC) automatically generates a replication topology.

**Intra-site replication:**
- Change notification based (within 15 seconds of change)
- Compressed only if >50KB
- Uses RPC over IP

**Inter-site replication:**
- Schedule-based (default: every 180 minutes)
- Always compressed
- Can use RPC over IP or SMTP (schema/configuration only)
- Site links define cost, replication interval, and schedule

**Replication metadata:**
- Each attribute has a version number (USN), originating DC, and timestamp
- Conflict resolution: highest version wins; if tied, last writer wins (by timestamp)
- Lingering objects: objects deleted on one DC but not replicated before tombstone lifetime expires

### Group Policy

Group Policy Objects (GPOs) apply configuration to users and computers:

**Processing order (LSDOU):**
1. **Local** -- Local Group Policy on the machine
2. **Site** -- GPOs linked to AD site
3. **Domain** -- GPOs linked to domain
4. **OU** -- GPOs linked to OUs (parent before child)

Last applied wins (closest OU overrides domain GPO for conflicting settings).

**Modifiers:**
- **Enforced** (formerly "No Override") -- Prevents child OUs from overriding
- **Block Inheritance** -- OU blocks all GPOs from above (except Enforced)
- **Security filtering** -- GPO applies only to specified users/groups/computers (default: Authenticated Users)
- **WMI filtering** -- GPO applies only if WMI query returns true

**Group Policy troubleshooting:**
```powershell
# Generate RSoP report
gpresult /h C:\temp\gpresult.html /scope:computer
gpresult /h C:\temp\gpresult_user.html /scope:user

# Force Group Policy refresh
gpupdate /force

# Check GPO replication (SYSVOL vs AD)
Get-GPO -All | ForEach-Object {
    $gpo = $_
    $adVersion = $gpo.User.DSVersion, $gpo.Computer.DSVersion
    # Compare with SYSVOL version in gpt.ini
}
```

### Kerberos Authentication in AD

AD DS is a Kerberos Key Distribution Center (KDC). Every DC runs the KDC service.

**Default ticket lifetimes (configurable via GPO):**
- TGT: 10 hours
- TGT renewal: 7 days
- Service ticket: 10 hours
- Clock skew tolerance: 5 minutes

**Service Principal Names (SPNs):**
```powershell
# List SPNs for an account
setspn -L serviceaccount

# Find duplicate SPNs (causes Kerberos failures)
setspn -X

# Register SPN
setspn -S HTTP/webapp.example.com serviceaccount
```

**Common Kerberos issues:**
- Duplicate SPNs: `KRB_AP_ERR_MODIFIED` -- use `setspn -X` to find duplicates
- Clock skew: `KRB_AP_ERR_SKEW` -- sync time via NTP hierarchy (PDC Emulator is authoritative)
- Missing SPN: Falls back to NTLM (investigate with network trace)
- Delegation misconfigured: Double-hop authentication failures

### Trust Types

| Trust Type | Direction | Transitivity | Use Case |
|---|---|---|---|
| Parent-Child | Two-way | Transitive | Automatic between parent/child domains |
| Tree-Root | Two-way | Transitive | Automatic between tree roots in forest |
| Shortcut | One-way or Two-way | Transitive | Optimize authentication path between distant domains |
| External | One-way or Two-way | Non-transitive | Trust to a specific domain in another forest (NT4 compatible) |
| Forest | One-way or Two-way | Transitive | Trust between forest root domains |
| Realm | One-way or Two-way | Non-transitive or Transitive | Trust to non-Windows Kerberos realm |

**SID filtering:** Enabled by default on forest trusts. Prevents SID history abuse across trust boundaries. Disable only with extreme caution.

### AD Hardening Essentials

**Tiered Administration Model:**

| Tier | Scope | Examples | Rule |
|---|---|---|---|
| **Tier 0** | Identity infrastructure | Domain controllers, AD DS, AD CS, Entra Connect | Tier 0 admins NEVER sign into Tier 1 or Tier 2 systems |
| **Tier 1** | Servers and applications | Member servers, SQL, Exchange, SCCM | Tier 1 admins NEVER sign into Tier 2 systems |
| **Tier 2** | Workstations and devices | User workstations, laptops, printers | Standard user and helpdesk tier |

**Key hardening controls:**
- **Protected Users group** -- Prevents NTLM authentication, Kerberos delegation, and DES/RC4 encryption for members. Add all privileged accounts.
- **Authentication Policies and Silos** -- Restrict where privileged accounts can authenticate (2012 R2+). Enforce Tier 0 accounts can only authenticate to Tier 0 devices.
- **LAPS (Local Administrator Password Solution)** -- Randomizes and rotates local admin passwords. Windows LAPS (built into Windows 11/Server 2019+) replaces legacy Microsoft LAPS.
- **Credential Guard** -- Virtualizes LSA process to prevent credential theft (Mimikatz, Pass-the-Hash). Requires Secure Boot, UEFI.
- **Privileged Access Workstations (PAWs)** -- Dedicated admin workstations for Tier 0 administration. No internet, no email, no general-purpose use.
- **gMSA (Group Managed Service Accounts)** -- Automatic password rotation for service accounts. 240-character random password, rotated every 30 days.
- **Fine-Grained Password Policies (FGPPs)** -- Different password policies for different groups (e.g., stricter for admins). Requires 2008+ domain functional level.
- **AdminSDHolder** -- Protects privileged group membership. Runs every 60 minutes to enforce ACL consistency on protected objects.

### Common Pitfalls

1. **Domain Admins for everything** -- Domain Admin is massively over-privileged. Delegate specific permissions to OUs instead.
2. **Single site for distributed network** -- Without proper sites/subnets, clients authenticate to random DCs across WAN links.
3. **Ignoring tombstone lifetime** -- Default is 180 days. DCs offline longer than tombstone lifetime reintroduce deleted objects as lingering objects.
4. **SYSVOL replication issues** -- DFSR replaced FRS in 2008+. FRS-to-DFSR migration is required before raising functional levels.
5. **Not monitoring AdminSDHolder changes** -- Attackers modify AdminSDHolder to persist admin access. Monitor Event ID 4780.
6. **Unconstrained delegation** -- Allows a service to impersonate any user to any service. Extremely dangerous. Audit with: `Get-ADComputer -Filter {TrustedForDelegation -eq $true}`.

## Version-Specific Guidance

| Version | Reference | What's version-specific |
|---|---|---|
| Windows Server 2016 | `references/versions/2016.md` | Functional level 2016, Privileged Access Management, MIM integration, temporal group memberships |
| Windows Server 2019 | `references/versions/2019.md` | Same functional level as 2016; hybrid identity improvements, security defaults, Windows Admin Center |
| Windows Server 2022 | `references/versions/2022.md` | TLS 1.3 for LDAPS, Kerberos AES-256 improvements, security baseline updates |
| Windows Server 2025 | `references/versions/2025.md` | Functional level 10 (first new FL since 2016), 32K database pages, NTLM deprecation, Kerberos with certificate trust |

## Reference Files

Load these when you need deep knowledge for a specific area:

- `references/architecture.md` -- AD DS internals: NTDS.dit, ESE database, replication protocols, partitions, FSMO mechanics, sites and subnets, Global Catalog, schema, trust authentication flow. Read for "how does X work" questions.
- `references/diagnostics.md` -- Troubleshooting playbooks: repadmin commands, dcdiag tests, critical event IDs, replication failure resolution, DNS issues, authentication failures, GPO troubleshooting. Read when diagnosing issues.
- `references/best-practices.md` -- Hardening and operational guidance: tiered administration, GPO security baselines, LAPS deployment, PAW architecture, monitoring and alerting, backup/recovery, DC placement. Read for design and operations questions.

## Diagnostic Scripts

Ready-made RSAT ActiveDirectory audits (read-only) in `scripts/`. Defensive review of on-prem tier-0 exposure.

- `scripts/01-privileged-group-audit.ps1` -- Recursive membership of Domain/Enterprise/Schema Admins and operators
- `scripts/02-kerberoast-exposure.ps1` -- Kerberoastable SPN accounts and AS-REP-roastable accounts, privilege-weighted
