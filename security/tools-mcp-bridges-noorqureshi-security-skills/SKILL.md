---
name: tools-mcp-bridges
description: >
  Expose CLI security tools to an AI agent through MCP servers — mcp-kali-server generic terminal
  bridge, MetasploitMCP, pentestMCP Docker bundle, mcp-security-hub, single-tool nmap/nuclei
  servers. Load when setting up agent-driven tooling on Kali or wiring a new tool into MCP.
  Signals: mcpServers config, kali-server-mcp, metasploitmcp, pentestmcp, "MCP server for nmap",
  stdio transport, port 5000/8080/8085.
domain: tools
type: arsenal
stability: learning
modes: [pentest, bugbounty]
severity: info
tools: [mcp-kali-server, metasploitmcp, pentestmcp, mcp-security-hub, hexstrike-ai]
schema_version: 1
---

# MCP bridges for security tools

## When it applies
You're setting up an agent-driven workflow and need CLI tools (nmap, nuclei, sqlmap, hashcat,
gobuster, Metasploit…) callable as MCP tools instead of raw shell. This is *infrastructure*, not
authorization: registering a tool over MCP never widens scope — `tradecraft-scope-roe` and
`scope.txt` still gate every call. For Burp specifically, see `tools-burp-suite`; for attacking MCP
servers themselves, `ai-mcp-security`.

## Why it works
MCP wraps a tool's CLI behind typed tool definitions, so the agent gets structured parameters and
output instead of scraping terminal text. A generic terminal bridge (mcp-kali-server) covers
everything but is unstructured; per-tool servers give safer, typed interfaces at the cost of setup.

## Options (pick one per need)

| Option | Install | Tools covered | Best for |
|--------|---------|---------------|----------|
| **mcp-kali-server** (Kali-official) | `apt install mcp-kali-server` | Any terminal command (nmap, nxc, curl, gobuster…) | General-purpose; CTF/labs |
| **MetasploitMCP** (Kali-official) | `apt install metasploitmcp` | MSF modules/payloads/sessions | MSF-heavy exploitation (`tools-metasploit`) |
| **pentestMCP** (Docker bundle) | `docker run -d -p 8080:8080 ramkansal/pentestmcp` | 20+: nmap, nuclei, ZAP, sqlmap, ffuf, nikto, gobuster, subfinder, httpx | One-container everything |
| **mcp-security-hub** (modular) | per-module pip installs | nmap, Ghidra, nuclei, sqlmap, hashcat | Enable only what you need |
| **hexstrike-ai** (Kali-official) | `apt install hexstrike-ai` | 150+ tools, multi-agent orchestration | Large-scale automation |
| **Single-tool servers** | npm/pip per project | one tool each (e.g. nmap-mcp-server, nuclei-mcp) | Minimal footprint |

## Method
1. **Generic terminal bridge (start here on Kali):**
   ```bash
   kali-server-mcp --port 5000        # API side; runs any terminal command
   mcp-server --server http://localhost:5000   # MCP client-facing side
   ```
2. **Metasploit:** `metasploitmcp --transport stdio` (preferred) or
   `--transport http --port 8085`. The invocation discipline in `tools-metasploit` still applies
   underneath (one-shot `-x`, `;exit`, port checks).
3. **Docker bundle:** `docker pull ramkansal/pentestmcp && docker run -d -p 8080:8080 ramkansal/pentestmcp`,
   then register `{"url": "http://localhost:8080/mcp"}` in the client's `mcpServers`.
4. **Register stdio servers** in the client config, e.g.:
   ```json
   {
     "mcpServers": {
       "kali-server": { "command": "kali-server-mcp", "args": ["--port", "5000"] },
       "metasploit-mcp": { "command": "metasploitmcp", "args": ["--transport", "stdio"] }
     }
   }
   ```
5. **Verify before relying on it:** list the exposed tools and run one harmless call (e.g. a
   version check) against a lab target before pointing anything at a real engagement.

## Gotchas
- **A terminal bridge is arbitrary command execution** — bind to localhost only, never expose the
  port on a network interface, and treat the bridge host as compromised-adjacent.
- **Community MCP servers are supply chain** — audit or pin versions before installing; a malicious
  tool server sees every command and result. Prefer Kali-official packages when they exist.
- **Scope still applies** — a registered scanner makes it *easier* to fire out-of-scope requests,
  not more allowed. Keep `scope.txt` loaded and check targets against it before every call.
- **Container bundles run as root with mounted sockets** — pentestMCP's Docker has full tool
  capability; don't mount engagement data you can't afford to leak into it.
- **Tool availability ≠ tool correctness** — the server reports what its manifest claims; confirm
  the underlying binary exists and is the expected version (`nmap --version`, etc.).

## Verify success
The MCP client lists the server's tools, a harmless invocation returns sane structured output, and
every subsequent call is logged against an in-scope target in the engagement workspace.

## References
Kali blog on MCP/LLM integration; Wh0am123/MCP-Kali-Server; GH05TCREW/MetasploitMCP;
ramkansal/pentestMCP; FuzzingLabs/mcp-security-hub; 0x4m4/hexstrike-ai.

---
_Portions adapted from [reverse-skill](https://github.com/zhaoxuya520/reverse-skill) by zhaoxuya520, MIT License._
