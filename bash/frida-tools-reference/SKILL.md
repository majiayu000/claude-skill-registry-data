---
name: frida-tools-reference
description: Pick and run the right Frida CLI tool, including frida, frida-ps, frida-ls-devices, frida-trace, frida-discover, frida-kill, and frida-create.
---

# Frida Tools Reference

Use this skill when choosing a Frida command-line tool or building a command from scratch.

## Tool Picker

- `frida`: interactive REPL, load scripts, spawn or attach to a target.
- `frida-ps`: list processes and installed apps.
- `frida-ls-devices`: list local, USB, and remote devices.
- `frida-trace`: generate temporary handlers for matching functions, ObjC methods, Java methods, or modules.
- `frida-discover`: discover internal functions by observing activity.
- `frida-kill`: kill a process on a selected device by PID.
- `frida-create`: scaffold an agent project when TypeScript or packaging is needed.

## Target Selectors

```bash
frida-ls-devices
frida-ps -Uai
frida -U -f com.example.app -l agent.js --no-pause
frida -U -n "App Name" -l agent.js
frida -p 1234 -l agent.js
frida -H 127.0.0.1:27042 -n target -l agent.js
```

Prefer package/bundle identifiers for mobile spawn commands and PID when process names are ambiguous.

## Trace Examples

```bash
frida-trace -U -f com.example.app -j '*!*certificate*/isu' --no-pause
frida-trace -U -f com.example.app -i 'Java_*' --no-pause
frida-trace -p 1234 -i '*open*' -x 'libSystem*!*open*'
frida-trace -U -f com.example.ios -m '-[NSURLSession *]' --no-pause
```

Option order matters for include and exclude filters: build the working set with includes, then remove noise with excludes.

## Direct CodeShare

```bash
frida -U --codeshare author/project-slug -f com.example.app --no-pause
```

Prefer `frida-codeshare-search` when the script must be fetched, reviewed, and saved locally first.

## Proof To Report

- Exact command used.
- Device selector and target selector.
- Frida version.
- Whether the command attaches, spawns, traces, or kills.
- First useful output or full error.

## References

Read `references/tool-docs.md` for official Frida tool documentation links and option notes.
