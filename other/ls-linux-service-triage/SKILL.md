---
name: ls-linux-service-triage
description: Diagnoses common Linux service issues using logs, systemd/PM2, file permissions, Nginx reverse proxy checks, and DNS sanity checks. Use when a server app is failing, unreachable, or misconfigured.
metadata:
  version: "1.1"
compatibility: "Linux hosts. Uses systemd, PM2, Nginx, ss, journalctl, and dig only when those tools are present in the target stack; verify the service manager, proxy, DNS, and privilege model before suggesting commands."
---

# Linux & service basics: logs, systemd/PM2, permissions, Nginx reverse proxy, DNS checks

Source note: imported from `linux-service-triage` by kowl64, with provenance previously recorded in release-only `_meta.json` metadata.

## PURPOSE
Diagnoses common Linux service issues using logs, systemd/PM2, file permissions, Nginx reverse proxy checks, and DNS sanity checks.

## WHEN TO USE
- TRIGGERS:
  - Show me why this service is failing using logs, then give the exact fix commands.
  - Restart this app cleanly and confirm it is listening on the right port.
  - Fix the permissions on this folder so the service can read and write safely.
  - Set up Nginx reverse proxy for this port and verify DNS and TLS are sane.
  - Create a systemd service for this script and make it survive reboots.
- DO NOT USE WHEN...
  - You need kernel debugging or deep performance profiling.
  - You want to exploit systems or bypass access controls.

## INPUTS
- REQUIRED:
  - Service type: systemd unit name or PM2 process name.
  - Observed symptom: error message, status output, or logs (pasted by user).
- OPTIONAL:
  - Nginx config snippet, domain name, expected upstream port.
  - Filesystem paths used by the service.
- EXAMPLES:
  - `systemctl status myapp` output + `journalctl` excerpt
  - Nginx server block + domain + upstream port

## OUTPUTS
- Default: triage report (likely cause, evidence from logs, minimal fix plan).
- If explicitly requested and safe: exact shell commands to apply the fix.
Success = service runs, listens on expected port, and reverse proxy/DNS path is correct.


## WORKFLOW
1. Confirm scope and safety:
   - identify the host OS, service manager, process runner, reverse proxy, and whether changes are permitted.
   - do not assume systemd, PM2, Nginx, DNS control, or TLS tooling until the user confirms they apply.
2. Gather evidence:
   - status output + recent logs (see `references/triage-commands.md`).
3. Classify failure:
   - config error, dependency missing, permission denied, port conflict, upstream unreachable, DNS mismatch.
4. Propose minimal fix + verification steps.
5. Validate network path (if web service):
   - app listens -> Nginx proxies -> DNS resolves -> (TLS sanity if applicable).
6. Provide restart/reload plan and confirm health checks.
7. STOP AND ASK THE USER if:
   - logs/status output are missing,
   - actions require privileged access not confirmed,
   - TLS/cert management is required but setup is unknown.


## OUTPUT FORMAT
```text
TRIAGE REPORT
- Symptom:
- Evidence (what you provided):
- Most likely cause:
- Fix plan (minimal steps):
- Exact commands (ONLY if user approved changes):
- Verification:
- Rollback:
```


## SAFETY & EDGE CASES
- Read-only by default: diagnose from provided outputs; do not assume you can run commands.
- Treat systemd, PM2, and Nginx commands as stack-specific examples; adapt for other Linux init systems, process managers, or proxies.
- Avoid destructive changes; require explicit confirmation for anything risky.
- Prefer `nginx -t` before reload and verify ports with `ss`.


## EXAMPLES
- Input: "journal shows permission denied on /var/app/uploads."
  Output: path permission analysis + safe chown/chmod plan + verification.

- Input: "App works locally but domain returns 502."
  Output: upstream port checks + nginx error log interpretation + proxy_pass fix plan.
