---
name: reverse-eng-macos
description: >
  Reverse macOS Mach-O binaries and .app bundles — codesign/notarization state, entitlements,
  Objective-C/Swift symbol recovery, and lldb/Frida dynamic analysis. Load when the target is a
  Mach-O executable/dylib/framework, an .app bundle, a LaunchAgent/Daemon plist, or Apple-platform
  malware. Signals: "Mach-O 64-bit executable", codesign/spctl output, hardened runtime,
  objc_msgSend, mangled _ZN/_$s symbols, XPC service names, TCC prompts.
domain: reverse-engineering
type: technique
stability: learning
modes: [pentest, bugbounty]
severity: medium
tools: [codesign, spctl, otool, jtool2, class-dump, dsdump, swift-demangle, hopper, ghidra, lldb, frida]
schema_version: 1
---

# macOS / Mach-O reversing

## When it applies
The target is a Mach-O binary, dylib, framework, or `.app` bundle on macOS (or a sample you can
read offline), and it is in scope (`tradecraft-scope-roe`, `scope.txt`). iOS IPAs are a different
surface — treat them with the iOS assessment flow (`mobile-ios-assessment`). Typical jobs:
understand a thick client, audit a persistence item (LaunchAgent/Daemon), or analyze Apple-platform
malware.

## Why it works
Mach-O carries its trust model in-band: the code signature, entitlements, and load commands say
what the binary may do before you read a single instruction. Objective-C keeps class and selector
names in `__objc_*` sections and Swift symbols demangle to full signatures, so static recovery is
cheap — and Apple's own tools (`codesign`, `otool`, `lldb`, `log`) cover most of the workflow.

## Method
1. **Trust posture first.**
   ```bash
   file target.app/Contents/MacOS/target
   codesign -dv --verbose=4 target.app          # signer, team ID, hardened-runtime flags
   codesign -d --entitlements :- target.app     # com.apple.security.* capabilities
   spctl -a -vv target.app 2>&1                 # Gatekeeper/notarization verdict
   otool -L target                              # linked dylibs + rpath entries
   ```
   Record: signed vs ad-hoc, notarized or not, hardened runtime, library validation, and any
   powerful entitlements (`get-task-allow`, `disable-library-validation`, TCC-related).
2. **Static.** `class-dump`/`dsdump` for Objective-C headers, `swift-demangle` for Swift symbols,
   then Hopper/Ghidra/IDA (jtool2 for deep Mach-O structure). Grep strings for XPC service names,
   TCC-sensitive APIs, URLs, and keys. Objective-C calls go through `objc_msgSend` — follow
   *selector* cross-references, not direct calls.
3. **Dependencies.** Audit `LC_LOAD_DYLIB` and `@rpath` entries — a writable rpath search dir is
   a dylib-hijack primitive; note it for privesc/attack-path mapping.
4. **Dynamic.** `lldb` for debugging, Frida for instrumentation. Watch behavior with
   `fs_usage -w -f filesystem <pid>` and `log stream --predicate 'process == "target"'` — file,
   network, and XPC activity show up without a single breakpoint. Proxy or hook for the network side.
5. **Persistence & malware checks.** For a suspicious sample: enumerate its LaunchAgents/Daemons
   plist, install receipts, and `AuthorizationExecuteWithPrivileges` / SMJobBless usage, then
   confirm the behavior dynamically before calling it malicious.

## Gotchas
- **Universal (fat) binaries** carry arm64 + x86_64 slices — `lipo -info`, and analyze the slice
  matching your analysis host.
- **Hardened runtime + library validation blocks dylib injection and Frida** — you need a copy
  re-signed (or the target built) with `com.apple.security.cs.disable-library-validation` /
  `get-task-allow`. SIP-protected platform binaries can't be attached at all.
- **Ad-hoc or revoked signatures change the verdict** — `spctl` failing doesn't mean malicious;
  correlate with entitlements and behavior.
- **Swift UI/AppKit binaries look sparse statically** — the real flow lives in closures and
  protocol witnesses; dynamic observation beats static here.
- **`objc_msgSend` hides call graphs** in decompilers — resolve selectors via the `__objc_selrefs`
  / `__objc_msgrefs` sections.

## Verify success
You can state the signature/notarization/entitlement posture, name the entry points and the
interesting logic at symbol or address level, and back the claim with a dynamic observation
(debugger state, `fs_usage`/`log stream` trace).

## References
Apple codesign/entitlement documentation; `otool`/`jtool2` Mach-O references; Hopper & Ghidra docs.

---
_Portions adapted from [reverse-skill](https://github.com/zhaoxuya520/reverse-skill) by zhaoxuya520, MIT License._
