---
name: privilege-handling
description: Detects unsafe privilege handling in SUID/SGID binaries, environment-variable trust in privileged code, insecure umask, temp-file races, and symlink-follow bugs in /tmp. Use when writing or modifying SUID/SGID-installed code, code that drops or elevates privileges via setuid/setgid/seteuid/seteuid_r, anything that reads PATH/LD_*/IFS environment variables, code that creates files in /tmp or other world-writable directories, or anything that opens a file whose path may contain a symlink controlled by a less-privileged user.
---

# Privilege Handling (CWE-271, CWE-426, CWE-377, CWE-61)

## What this checks

Privileged programs (SUID/SGID, root daemons, container init) operate with a
credentials gap. Classic mistakes: privileges dropped in the wrong order, environment
variables trusted from an attacker-controlled shell, temp files where an attacker can
symlink-swap before write. Local pattern, cross-trust-boundary consequence. LSMs
provide defense in depth; this catches the source-level mistake.

## Vulnerable patterns

- Privileged process drops the effective UID only, leaving the saved set-user-ID intact so the process can regain root later.
- Privileged exec resolves the program name via `PATH`, letting the attacker plant a lookalike earlier in the search path.
- Privileged code inherits `LD_PRELOAD`, `LD_LIBRARY_PATH`, or `IFS` from the calling environment without scrubbing them.
- Process runs with no umask call (or an explicit zero umask), leaving created files world-writable.
- Temp file created via a "generate name then open" pattern (non-atomic), allowing an attacker to symlink the name in between.
- File opened in a world-writable directory without the no-follow flag, letting the attacker pre-create the path as a symlink to a privileged target.
- Multi-call binary that picks behavior based on `argv[0]` without canonicalizing — the caller chooses the name via `execve`'s second argument.

## Fix immediately

Flag the vulnerable code and explain the risk. Then suggest a fix that establishes
these properties. Translate each property into the audited file's language and
operating-system API — use the platform's documented privilege, environment, and
filesystem calls.

1. **Privilege drops set all three credential IDs explicitly and check the return.** Use the call that sets real, effective, and saved IDs in one operation; verify by re-reading afterwards. Any failure is fatal — abort rather than continue with ambiguous credentials.
2. **Privileged execs pass an absolute path and a known environment.** Do not inherit `PATH`, `LD_*`, or `IFS` from the caller. Never use exec variants that resolve via `PATH` in privileged code.
3. **Temp files are created with an atomic open-and-create primitive** that returns a file descriptor in one call — never "make a name, then open". Atomic creation closes the symlink-swap window.
4. **Files opened in world-writable directories pass a no-follow flag** so the open fails if the final path component is a symlink. Combine with exclusive-create when the file should not pre-exist.
5. **The umask is set explicitly at process start** to a restrictive value matching the intended file-mode policy. Do not rely on the inherited umask.

## Verification

After rewriting, confirm:

- [ ] Every privilege drop sets real, effective, and saved IDs explicitly and checks the return values
- [ ] Every exec from privileged code passes an absolute path and a sanitized environment, never the inherited environment
- [ ] No path-searching exec variant (the family that resolves via `PATH`) is used in privileged code paths
- [ ] Every temp-file creation uses an atomic open-and-create primitive — never a name-then-open pattern
- [ ] Every file open in a world-writable directory passes a no-follow flag, plus exclusive-create when the file should not pre-exist
- [ ] The umask is set explicitly at process start to a restrictive value

## References

- CWE-271 ([Privilege Dropping / Lowering Errors](https://cwe.mitre.org/data/definitions/271.html))
- CWE-426 ([Untrusted Search Path](https://cwe.mitre.org/data/definitions/426.html))
- CWE-377 ([Insecure Temporary File](https://cwe.mitre.org/data/definitions/377.html))
- CWE-61 ([UNIX Symbolic Link Following](https://cwe.mitre.org/data/definitions/61.html))
