---
name: triage-route
description: >-
  Triage and routing of a reverse-engineering task: by signal (what the target is,
  what material exists, what result is wanted) choose which reverse-engineering
  skill to load first. Use ALWAYS at the start of any RE task — before reading
  other skills. Not for ordinary coding.
license: Proprietary
---

# Triage & route

> Home branch in Memora: `root/skill/triage-route`.

The first thing a reverse-engineer does: 4 questions and a route. Don't read all
skills at once — only the route.

## 4 questions (always)

1. **What is the target:** website / API / JS bundle / extension / binary /
   protocol / black box?
2. **What action matters:** launch, login, search, request, encryption,
   validation, data exchange?
3. **What material already exists:** file, URL, HAR/PCAP, log, screenshot, dump,
   source — or only a description?
4. **What result is wanted:** explain behavior, find the entry point,
   intercept/substitute, reconstruct a request, a report?

If there is no material — first a plan to collect artifacts, not an "analysis"
of an invisible target.

## Choosing a route (signal → load first)

This router owns no parts: the choice below is which *other* skill to load first.

| Signal (target/material) | Skill to load first |
|---|---|
| Website, web app, "how does this work" | `reverse-engineering` (black-box recon first) |
| API, "what requests", contract | `reverse-engineering` → `protocol-reverse` (contract from traffic) |
| Minified JS, bundle, obfuscation | `js-reverse` → `reverse-engineering` |
| Signature/token/encrypted param (x-s, x-bogus, _abck...) | `js-reverse` (find the signer) — no dedicated signature skill; if the signing logic is server-side, report what is observable |
| Binary body (protobuf/grpc/msgpack), PCAP, WebSocket | `protocol-reverse` |
| "Intercept/substitute/mock/redirect" | `reverse-engineering` (traffic via a local proxy) |
| Extension, content script | `reverse-engineering` → `js-reverse` |
| Logs, errors, "why doesn't it work" | `dev` part `systematic-debugging` (first separate your own side from theirs) |
| Native binary (EXE/ELF/Mach-O), .so/.dll, crack, malware | `ida-reverse`/`ghidra-reverse`/`radare2` (triage → static → dynamic → patch); malware → `malware-analysis` |
| File of unknown format, firmware, save, dump | `binary-diff` (signature → structure → extraction); firmware → `firmware-pentest` |
| Game: Unity/Unreal/Cocos, assets, saves, mechanics | `reverse-engineering` (engine → code → resources → patch); assets via `binary-diff` |
| Mobile app (APK/IPA), Frida, TLS-pinning | `apk-reverse` / `mobile-reverse` (decompile → dynamic → traffic) |
| Encrypted: traffic/file/field, signature, hash, keys | `protocol-reverse` (recognize → key → decrypt) |
| Recover a function/algorithm | `binary-diff` / `ida-reverse` / `ghidra-reverse` |

Skill names follow the workspace's actual inventory — resolve the canonical name
from `skills/` before loading; do not invent skills.

## Rules

- **Order:** understand (blueprint) → redirect (intercept) → recover
  (reconstruction). You cannot intercept what you do not understand.
- **One route at a time** — don't drag in all skills at once.
- **Unknown target type** — start with `reverse-engineering` (recon).
- **No material** — a collection plan, not an analysis.
- **Findings go into Memora** under `root/skill/triage-route` (or the project
  branch when the work belongs to a project), one node per finding with what was
  observed and how it was verified. There is no local findings database.
- **Forks go to `ask_questions`**: whose system is being touched, whether an
  action could break someone else's service, and what counts as out of scope.

## Related

`reverse-engineering`, `protocol-reverse`, `js-reverse`, `binary-diff`,
`security`, `research`.
