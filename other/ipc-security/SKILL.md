---
name: ipc-security
description: Detects IPC receivers that accept input without verifying caller identity. Use
  when writing URL scheme handlers, Android intent receivers or exported
  activities, named pipe or socket listeners, XPC service handlers, or any IPC
  endpoint that processes caller-supplied input without validating the
  caller's identity or origin.
---

# IPC Security (A01:2025)

## What this checks

Detects IPC receivers that accept input without verifying the caller's identity. Open
IPC channels let malicious apps hijack URL schemes, trigger exported components, or
inject data through shared channels.

## Vulnerable patterns

- URL scheme handler that runs an action without validating the incoming scheme, host, and path against a static allowlist
- Exported mobile component (Android activity, service, or broadcast receiver) with no signature-level permission or caller-package check guarding a sensitive action
- Network listener bound to a public interface for what is logically same-host IPC, with no auth token or peer-credential check before the handler acts
- Named pipe, XPC service, or desktop-renderer IPC handler that processes a privileged request without verifying caller identity, code signature, or sender origin
- IPC-supplied value flowing into a process-execution or dynamic-evaluation sink without validation

## Fix immediately

Flag the vulnerable code and explain the risk. Then suggest a fix that establishes
these properties:

1. **URL scheme handlers validate scheme, host, and path against a static allowlist**
   before running any action. A custom scheme is invokable by any app on the device;
   only the handler decides what's legitimate.
2. **Exported components require a signature-level permission** or verify the caller
   package explicitly. An exported component with no permission gate is callable by
   anything on the device. Intent extras and equivalent caller-supplied payloads are
   validated against a schema before use.
3. **Network listeners bind to the narrowest interface that works.** Use a Unix
   domain socket or loopback address, never a public-facing bind, when the listener
   is for same-host IPC. An auth token or peer-credential check runs before the
   handler acts on any command.
4. **Named pipes, XPC services, and desktop-renderer IPC handlers verify caller
   identity** — effective user ID, code-signing requirement, pipe ACL, or sender
   origin against an allowlist — before any privileged action. Renderer-to-main
   channels run with context isolation enabled and node integration disabled.
5. **No IPC-supplied value reaches a process-execution or dynamic-evaluation sink
   unvalidated.** The channel is an attacker-reachable surface; treat its payloads
   like network input.

Translate each principle to the language, platform, and IPC mechanism of the audited
file. Use the platform's documented identity-verification and binding APIs — do not
invent your own.

## Verification

Confirm the following *properties* hold for every IPC surface present in the change (criteria only apply when the relevant pattern exists):

- [ ] Every URL scheme handler validates scheme, host, and path against a static allowlist before any action runs
- [ ] Every exported mobile component is protected by a signature-level permission or explicitly verifies the caller package, and caller-supplied payload fields are validated against a schema before use
- [ ] Every same-host IPC socket binds to a Unix domain socket or loopback address — never a public interface — and requires an auth token or peer-credential check before handling commands
- [ ] Every renderer-to-main or cross-process IPC handler verifies sender origin or caller identity against an allowlist and runs with context isolation enabled
- [ ] Every named pipe or platform RPC handler verifies caller identity (effective user id, code-signing requirement, or ACL) before privileged actions run
- [ ] No process-execution or dynamic-evaluation sink is called with unvalidated IPC-supplied input on any of the above surfaces

## References

- CWE-926 ([Improper Export of Android Application Components](https://cwe.mitre.org/data/definitions/926.html))
- CWE-441 ([Unintended Proxy/Intermediary](https://cwe.mitre.org/data/definitions/441.html))
- [OWASP A01:2025 Broken Access Control](https://owasp.org/Top10/A01_2021-Broken_Access_Control/)
- [OWASP Mobile M4:2024](https://owasp.org/www-project-mobile-top-10/)
