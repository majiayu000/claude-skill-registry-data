---
name: toolchain-router
description: "Route an offensive or security-testing task to the one tool skill that fits it — Active Directory, web, reconnaissance, JavaScript reversing, credentials, pivoting, C2, AI/LLM testing or shell plumbing. Use at the start of any engagement step when the right tool is not already named. Not for choosing between libraries inside a single tool."
---

# Toolchain router

One task, one tool skill. Read this table, open the matching skill, follow it. Do not load several tool skills "just in case": each carries its own OPSEC notes and flag sets, and mixing them produces commands nobody verified.

## Route by intent

| If the task is… | Open | Why that one |
| --- | --- | --- |
| validate credentials, enumerate shares/sessions, dump SAM/LSA/NTDS | [netexec](../netexec/SKILL.md) | one binary, every protocol, fastest triage |
| relay NTLM, forge tickets, run a per-service script, dump secrets surgically | [impacket](../impacket/SKILL.md) | fine-grained control NetExec does not expose |
| attack AD CS, ESC1-ESC8, request and abuse certificates | [certipy](../certipy/SKILL.md) | purpose-built for certificate templates |
| map the domain graph (users, groups, ACLs, sessions) | [bloodhound-python](../bloodhound-python/SKILL.md) | collector for BloodHound analysis |
| first look at an unknown SMB/LDAP host, no credentials | [enum4linux-ng](../enum4linux-ng/SKILL.md) | null-session enumeration without touching auth |
| interactive shell on a Windows host with WinRM | [evil-winrm](../evil-winrm/SKILL.md) | pass-the-hash, file transfer, PowerShell |
| capture NetNTLM hashes from the wire | [responder](../responder/SKILL.md) | LLMNR/NBT-NS/mDNS poisoning |
| get IPv6 hosts to authenticate to you | [mitm6](../mitm6/SKILL.md) | DHCPv6 + WPAD takeover |
| enumerate or spray usernames through Kerberos pre-auth | [kerbrute](../kerbrute/SKILL.md) | no lockout on user enumeration |
| coerce a machine account to authenticate (PetitPotam style) | [coercer](../coercer/SKILL.md) | automated coercion method sweep |
| port and service discovery | [nmap](../nmap/SKILL.md) | the reference scanner |
| directory and parameter fuzzing | [ffuf](../feroxbuster/SKILL.md) or [feroxbuster](../feroxbuster/SKILL.md) | ffuf for crafted requests, feroxbuster for recursive brute force |
| template-based vulnerability scanning | [nuclei](../nuclei/SKILL.md) | 10k+ maintained templates |
| subdomain enumeration | [subfinder](../subfinder/SKILL.md) | passive sources |
| probe HTTP services at scale | [httpx](../httpx/SKILL.md) | status, title, tech, TLS |
| fingerprint a web stack | [whatweb](../whatweb/SKILL.md) | CMS and framework signatures |
| SQL injection | [sqlmap](../sqlmap/SKILL.md) | detection through exploitation |
| crack hashes offline | [hashcat](../hashcat/SKILL.md) (GPU) or [john](../john/SKILL.md) (CPU, formats) | mode coverage vs format coverage |
| online password spraying against a service | [hydra](../hydra/SKILL.md) | protocol-aware brute force |
| extract endpoints and secrets from JavaScript | [jsluice](../jsluice/SKILL.md) | AST-based, not regex |
| deobfuscate or unbundle JavaScript | [webcrack](../webcrack/SKILL.md) | obfuscator.io, webpack, browserify |
| capture, replay and diff HTTP(S) traffic | [mitmproxy](../mitmproxy/SKILL.md) | scriptable proxy plus MCP control |
| drive a real browser and read its network/CDP data | [chrome-devtools](../chrome-devtools/SKILL.md) | DevTools protocol for agents |
| tunnel TCP over HTTP or a firewall | [chisel](../chisel/SKILL.md) | single binary, SOCKS5 |
| build a routed pivot with a TUN interface | [ligolo-ng](../ligolo-ng/SKILL.md) | real routing, no proxychains |
| send existing traffic through a SOCKS chain | [proxychains](../proxychains/SKILL.md) | wraps any TCP client |
| implant-based C2 with mTLS and per-session SOCKS | [sliver](../sliver/SKILL.md) | open-source C2 |
| exploitation framework, payload generation, sessions | [metasploit](../metasploit/SKILL.md) | msfconsole and msfvenom |
| test an LLM endpoint for jailbreaks, leakage, injection | [garak](../garak/SKILL.md) | probe catalogue |
| audit a model file for malicious pickle code | [model-file-audit](../model-file-audit/SKILL.md) | picklescan + fickling |
| map what an agentic app can reach before running it | [agentic-radar](../agentic-radar/SKILL.md) | static analysis |
| inventory installed MCP servers, skills, agent configs | [snyk-agent-scan](../snyk-agent-scan/SKILL.md) | local surface discovery |
| find which wordlist to use | [wordlists](../wordlists/SKILL.md) | paths and trade-offs |
| fix the shell itself (zsh, PATH, completions, history) | [shell-environment](../shell-environment/SKILL.md) | this machine's shell setup |
| use the segfault-derived helpers (`crt`, `asnl`, `io`, `gssec`, `sshj`) | [segfault-cli](../segfault-cli/SKILL.md) | small single-purpose CLIs |
| check what is installed and whether it works | [redteam-toolchain](../redteam-toolchain/SKILL.md) | inventory, install, verification |
| end-to-end web traffic → JS → API workflow | [web-traffic-js-reversing](../web-traffic-js-reversing/SKILL.md) | cross-tool sequence |
| end-to-end AI/LLM target testing | [ai-security-testing](../ai-security-testing/SKILL.md) | cross-tool sequence |

## Operating rules

1. **Confirm the tool exists before promising output.** Run `redteam-check` (or `<tool> --version`). A skill describes behaviour that requires the binary.
2. **Read the skill's OPSEC section before the first command.** Each one names the events its actions generate.
3. **Stay inside the authorised scope.** Example IPs, hostnames and credentials in these skills are placeholders. Scope comes from the engagement, not from documentation.
4. **Prefer read-only collection first.** Enumeration, then authentication, then execution, then persistence.
5. **Record the command, timestamp and raw output** for every step that changes a target's state.
6. **Do not chain tools the skill did not sanction.** If two skills disagree, the more specific one wins; if neither covers the case, stop and ask.

## Specialist agents

These are `task` agents from `~/.omp/agent/agents/`, not skills. Dispatch one when the work should run with its own tool allowlist and prompt:

| Delegate when… | Agent |
| --- | --- |
| the objective is an AD path, not a single command | `ad-specialist` |
| the target is a SPA, API capture, or obfuscated bundle | `web-reverser` |
| the surface is unmapped and scope is fixed | `recon-specialist` |
| a suspected bug needs a deterministic repro | `exploit-dev` |
| a plan is noisy, irreversible, or near the scope edge | `opsec-reviewer` |
| the target is only reachable from a foothold | `pivot-engineer` |
| hashes or passwords must turn into access | `credential-operator` |
| an implant or channel is the objective, not a tunnel | `c2-operator` |
| the blocker is conceptual and no tool fixes it | `consultant` |

## Ambiguous cases

- **"Get domain admin"** — not a tool. Route to [bloodhound-python](../bloodhound-python/SKILL.md) for the map, then the tool the path needs (certipy, impacket, netexec).
- **"Scan the web app"** — [nuclei](../nuclei/SKILL.md) for known CVEs, [ffuf](../ffuf/SKILL.md) for content discovery, [sqlmap](../sqlmap/SKILL.md) for injection. Run them in that order.
- **"Analyse this JS"** — [webcrack](../webcrack/SKILL.md) to make it readable, [jsluice](../jsluice/SKILL.md) to extract from it. Never the reverse.
- **"Test our chatbot"** — [ai-security-testing](../ai-security-testing/SKILL.md), which dispatches to garak or the agentic tools depending on whether the target is a model endpoint or an agent.

## Verification

```sh
redteam-check | tail -3        # ok=N missing=0
```

If a skill's tool is missing, [redteam-toolchain](../redteam-toolchain/SKILL.md) has the install command. Do not improvise an install mid-engagement.