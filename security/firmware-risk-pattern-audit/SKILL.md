---
name: firmware-risk-pattern-audit
description: Use when auditing embedded firmware source, object files, or extracted rootfs content for risky C/web-backend patterns such as system(), _eval(), exec wrappers, sprintf/strcpy/strcat, user-controlled path construction, /tmp usage, unlink(), mktemp(), firmware/config upload handlers, NVRAM backup/upload/download, restore/default reset paths, WPS handlers, nvram flows, and suspicious hidden CGI endpoints.
metadata:
  short-description: Audit risky firmware web/backend patterns
---

# Firmware Risk Pattern Audit

Use this skill for conservative static security triage of firmware web/backend code. It is intended for candidate issue discovery, not exploit confirmation.

## Search Surface

Prioritize these sinks and patterns:

- Command execution: `system`, `popen`, `_eval`, `eval`, `execv`, `execvp`, `execve`, `/bin/sh`, `kill`.
- Unsafe string/file construction: `sprintf`, `vsprintf`, `strcpy`, `strcat`, `gets`, fixed stack buffers.
- Path and temp file handling: `/tmp`, `mktemp`, `tmpnam`, `unlink`, `rename`, `fopen`, `open`, upload file names, symlink-sensitive cleanup.
- Firmware/config flows: upgrade, restore, backup, defaults, NVRAM download/upload/import/export, checksum/decrypt/constraint validation, reboot exceptions.
- Router-specific web routes: WPS, `dev.cgi`, `proxy.cgi`, `get.cgi`, `set.cgi`, `twonky_cmd.cgi`, SKU/model handlers.

## Workflow

1. Harvest candidate sinks with `rg`, `strings`, `nm`, dynamic symbols, and relocation tables. If `rg` is unavailable, use `grep -RniE`.
2. For each sink, identify caller, input source, transformations, and sink type.
3. Classify data-flow confidence:
   - `confirmed`: source-to-sink path is visible and artifact linkage is clear.
   - `candidate`: suspicious construction exists, but source or reachability is incomplete.
   - `hypothesis`: plausible based on names/strings/layout, but needs manual validation.
4. Rank risk by impact and confidence:
   - High: reachable command execution, auth bypass, firmware write, config restore with weak validation.
   - Medium: path traversal, arbitrary file delete/write candidates, unsafe upload/temp-file handling.
   - Low: crash-only buffer risks, dead-code candidates, unreachable diagnostics.
5. State required validation steps before claiming exploitability.

## Useful Commands

```sh
rg -n "system\(|popen\(|_eval\(|execv|execvp|execve|sprintf\(|vsprintf\(|strcpy\(|strcat\(|unlink\(|mktemp|tmpnam|/tmp|upgrade|restore|upload|download|backup|checksum|constraint|wps|nvram|dev\.cgi|proxy\.cgi|get\.cgi|set\.cgi|twonky|SKU" src /tmp/rootfs 2>/dev/null
# Fallback when rg is unavailable:
grep -RniE "system\(|popen\(|_eval\(|execv|execvp|execve|sprintf\(|vsprintf\(|strcpy\(|strcat\(|unlink\(|mktemp|tmpnam|/tmp|upgrade|restore|upload|download|backup|checksum|constraint|wps|nvram|dev\.cgi|proxy\.cgi|get\.cgi|set\.cgi|twonky|SKU" src /tmp/rootfs 2>/dev/null
strings -td artifact | grep -Ei "system|_eval|exec|/tmp|upgrade|restore|upload|download|backup|checksum|constraint|wps|nvram|\.cgi|cgi-bin"
nm -A objects/*.o | rg "system|_eval|exec|unlink|sprintf|strcpy|strcat|upload|restore|upgrade|wps"
readelf -r object.o | rg "system|_eval|exec|unlink|sprintf|strcpy|strcat"
```

## Reporting Rules

- Keep confirmed findings separate from hypotheses.
- Do not turn path control into command injection unless the sink is shell-string based or another shell boundary is shown.
- Call out when command execution is argv-based but still risky because arguments, paths, environment, or executable names are controlled.
- Include artifact names and offsets/addresses when available.
