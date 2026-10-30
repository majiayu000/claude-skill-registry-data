---
name: windows-ad
description: Use for authorized Active Directory and Windows identity attacks including Kerberos, AD CS, BloodHound paths, NTLM relay, and domain privilege escalation research.
---

# Windows / Active Directory Security

## Authorization preamble

1. **Domain/AD testing requires explicit written scope** — including DCs, and whether poisoning/relay is allowed.
2. Open a case; write the network profile and prohibited actions down clearly.
3. Tools: impacket / certipy / bloodhound are often manual installs — verify first.
4. Start from identity enumeration and the BloodHound graph; **no destructive exploitation first**.

## Scope

- Domain pentest, Kerberoasting, AS-REP, delegation
- AD CS certificate attacks (ESC1–ESC8 etc.)
- BloodHound / SharpHound attack paths
- NTLM relay / Coercer forced authentication
- Local-to-domain escalation paths (Potato family as stepping stones)

## Relationship to attack-chain

- **Multi-stage from external to DC** → PRIMARY stays `attack-chain/`; this skill is the **AD specialist**
- **Already inside the domain, identity focus** → PRIMARY = this skill

## Workflow

### 1. Enumeration

```bash
# Impacket / built-in examples (need credentials and authorization)
nxc smb <range> -u user -p pass
bloodhound-python -d domain.local -u user -p pass -c All -ns <DC>
```

### 2. Common paths (graph before guns)

```text
□ Kerberoast / AS-REP → offline cracking
□ ACL abuse (GenericAll / WriteDacl)
□ Delegation (unconstrained / constrained / resource-based)
□ AD CS template misconfigs → Certipy
□ Relay: LLMNR/NBT-NS + ntlmrelayx (confirm authorization)
```

### 3. Credentials and lateral movement

```text
□ secretsdump / lsassy / mimikatz (strict authorization and cleanup)
□ PtH / PtT / golden ticket only within authorized red-team scope
□ Write Evidence at every step; confirm with the user for high-impact actions
```

## Toolchain

| Tool | Purpose |
|------|---------|
| BloodHound / SharpHound | path graphs |
| Certipy | AD CS |
| Impacket / NetExec | lateral movement and enumeration |
| Rubeus / Mimikatz | tickets and credentials (authorized) |
| Coercer / Responder | forced auth / poisoning |

## References

- `references/ad-attack-paths.md`
- `../pentest-tools/references/network-attack-defense.md`
- `security/parts/attack-chain/`

## MUST NOT

- Unauthorized DCSync / golden tickets against production.

## Completion self-check

- [ ] Graph/enumeration before exploitation?
- [ ] Reproducible commands recorded and sanitized?
- [ ] Scope prohibitions respected?
- [ ] Checklist written?
