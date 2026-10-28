---
name: mobile-security-skill
description: Run a complete mobile application security assessment of an Android APK/AAB, iOS IPA, or their source, covering manifest/plist/entitlements misconfiguration, insecure local storage and weak crypto, taint analysis from attacker-controlled sources to dangerous sinks, WebView/OAuth/OIDC/deep-link flaws, Android IPC and iOS platform attack surface, anti-tamper/root-jailbreak/pinning resilience, network and backend API weaknesses (BOLA, JWT, secrets), supply-chain and framework-specific issues (Flutter/React Native/Xamarin/Unity/Cordova), and business-logic abuse. Then it adversarially confirms exploitability before anything is reported as Confirmed. Use this whenever the user asks for a mobile app security audit, pentest, or MASVS/MASTG assessment; mentions an APK, AAB, IPA, or mobile app source tree they want reviewed for vulnerabilities; asks to check a mobile app for hardcoded secrets, insecure storage, SSL pinning, WebView/JS-bridge issues, OAuth or deep-link flaws, root/jailbreak detection bypass, or OWASP Mobile Top 10 issues; or wants to know whether a specific mobile finding is actually exploitable. Always run the Step 0 authorization check before touching any target.
compatibility: Requires Claude Code (or an SDK agent harness) with the Agent/Task tool to spawn subagents from agents/*.md. Static analysis needs standard Android/iOS reverse-engineering tooling on PATH (apktool, jadx/aapt2, plutil, codesign, otool, strings) for best results but degrades gracefully without it. Dynamic phases require a connected device/emulator/simulator with Frida/objection; skipped (and reported as skipped) otherwise.
---

# Mobile Application Security Audit

A pipeline of specialist subagents that performs an OWASP MASTG-aligned mobile security assessment. The part that matters most: it does not let a finding call itself "Confirmed" until an adversarial prosecutor/skeptic panel has actually tried to break it. The 18 subagents this pipeline spawns by name below (`mobile-recon-triage`, `android-manifest-auditor`, etc.) are installed alongside this skill. See the project's README on GitHub for the full architecture diagram and agent roster if you want the human-readable version.

## Step 0: Authorization & scope (mandatory, do this before anything else)

Do not run any phase of this skill, not even recon, against a target until you can state in your own words, back to the user, one of:
1. **Own app**: the user owns this app or its source, or it's an internal app at their employer and they're the engineer/security team assigned to it.
2. **Authorized engagement**: a pentest/bug-bounty engagement with documented scope that covers this target (ask for the scope doc or program rules if not already provided).
3. **CTF / training target**: a deliberately vulnerable app built for practice (e.g. DVIA, InsecureBankv2, OWASP MSTG crackmes).

If none of these is clearly true, stop and ask. Do not proceed on an assumption of authorization. Write a one-line record to `engagement-<slug>/scope.md`:
```markdown
# Scope
- Target: <app name / package id / bundle id>
- Authorization: <own-app | engagement | ctf>, <one line of detail the user gave>
- In scope: <what the user wants covered, e.g. full MASVS sweep, or a specific concern>
- Out of scope: <anything explicitly excluded, e.g. "don't touch the production backend, static APK only">
- Date: <today>
```
`<slug>` = a short kebab-case identifier for this engagement (app name + date is fine). Everything below writes into `engagement-<slug>/` relative to the current working directory.

This mirrors the reference material's own stance: `advanced-attacks.md` frames every check as "test your own app for exposure," and the parent system instructions require clear authorization context for dual-use security testing. This skill is read-and-report by design: specialist agents get `Read, Grep, Glob, Bash` for inspection/instrumentation, never blanket `Edit` on the target's source, and nothing here attempts to weaponize a finding beyond what's needed to prove it's real.

## Resolving reference-doc paths for spawned agents

Every phase below spawns agents that need one or more files from this skill's own `references/` folder (the directory next to this SKILL.md). Resolve the absolute path to that folder yourself before spawning anyone. You can do this reliably, since you loaded this very file, and a skill's bundled resources are always installed together with it, whatever the install method (Claude Code plugin, global `~/.claude/skills/mobile-security-skill/`, or project-scoped `.claude/skills/mobile-security-skill/`). Then give each spawned agent either that reference file's full content inline in its prompt, or the resolved absolute path to it, whichever is more convenient at the point you're spawning it.

Don't assume a spawned agent can find its own reference doc by a bare relative path. The 18 agent definitions in `agents/` are commonly installed in a *different* location than this skill bundle (for example, a global `~/.claude/agents/` sitting alongside a skill installed at `~/.claude/skills/mobile-security-skill/`), so a relative path inside an agent's own prompt has nothing reliable to resolve against unless you hand it one explicitly. Each agent file's own instructions note this and fall back to a Glob search if you forget, but passing the path (or content) directly is one Read call for you and saves every agent a guess.

## Pipeline

```
Phase 0  Authorization & scope                         (you, above)
Phase 1  Recon & triage                                  mobile-recon-triage
Phase 2  Static specialists (parallel, scoped by Phase 1 output)
Phase 3  Dynamic confirmation (if device/emulator connected)  dynamic-runtime-verifier
Phase 4  Adversarial exploitation panel (per candidate finding)
Phase 5  Report synthesis                                 report-synthesizer
```

### Phase 1: Recon & triage
Spawn `mobile-recon-triage` (Agent tool, `subagent_type: mobile-recon-triage`) with the target path/artifact. It identifies platform (Android/iOS/both), framework (native, Flutter, React Native, Xamarin/MAUI, Cordova/Ionic, Unity, Kotlin Multiplatform), extracts the manifest/plist/entitlements, and writes `engagement-<slug>/target-profile.md` with an attack-surface inventory (exported components, URL schemes/App Links/Universal Links, WebViews found, network endpoints seen in strings, permissions/entitlements, embedded SDKs, whether a device/emulator is available for Phase 3). Read this before deciding which Phase 2 specialists to run. Don't run `ios-platform-attack-auditor` on an Android-only APK, don't run the Flutter/RN-specific parts of `supply-chain-framework-auditor` on a pure-native app, etc. Scope to what's actually relevant; it's fine to skip an agent entirely and say so in the report's Appendix C.

### Phase 2: Static specialists (parallel)
Spawn the applicable subset of these as concurrent Agent-tool calls (they're independent, no reason to serialize them). Each is grounded in its own reference-doc section and writes findings per `references/finding-schema.md` into `engagement-<slug>/findings/findings.jsonl`:

| Agent | Primary reference | Covers |
|---|---|---|
| `android-manifest-auditor` | `manifest-plist.md` §A | MAN-01..21 |
| `ios-plist-entitlements-auditor` | `manifest-plist.md` §B | PLS-01..18 |
| `storage-crypto-auditor` | `storage-crypto.md` | STO-*, CRY-* (both platforms + native + cross-platform) |
| `taint-flow-analyst` | `taint-analysis.md` | Full source->sink->sanitizer methodology, TNT-01..20 |
| `webview-security-auditor` | `clipboard-webview-oauth.md` §B | WEB-01..44 |
| `oauth-oidc-auditor` | `clipboard-webview-oauth.md` §C | OAU-01..26 |
| `deeplink-clipboard-auditor` | `clipboard-webview-oauth.md` §A, §D | CLP-01..14, DLK-01..08 |
| `android-ipc-ui-auditor` | `advanced-attacks.md` §A | ADV-01..25 |
| `ios-platform-attack-auditor` | `advanced-attacks.md` §B | ADV-40..54 |
| `resilience-anti-tamper-auditor` | `advanced-attacks.md` §C | ADV-60..72 |
| `network-backend-auditor` | `advanced-attacks.md` §D | ADV-80..90 |
| `supply-chain-framework-auditor` | `advanced-attacks.md` §E | ADV-100..110 |
| `business-logic-auditor` | `advanced-attacks.md` §F | Logic/business-flow abuse |

Each agent prompt should include: the target artifact/source path, the `target-profile.md` attack-surface summary, the path to write findings to, and its reference doc's content or resolved absolute path from the table above (see "Resolving reference-doc paths for spawned agents"). They work from static artifacts (decompiled code, manifest/plist, strings, binaries). No device required for this phase.

### Phase 3: Dynamic confirmation
If `target-profile.md` says a device/emulator/simulator is connected, spawn `dynamic-runtime-verifier` with the full `findings.jsonl` so far, plus the content or resolved path of the reference docs it needs (`advanced-attacks.md`, `taint-analysis.md`, `storage-crypto.md`; see "Resolving reference-doc paths for spawned agents" above). It follows `advanced-attacks.md` §G (baseline, exercise flows, hook sinks, fuzz exported components/deep links, MITM with/without pinning bypass, background/logout/reinstall residue) and the taint doc's dynamic-confirmation step (marker strings through sources, grep at sinks with stack traces). It appends `type: "dynamic"` evidence to existing findings rather than creating new ones where possible, and may add new findings runtime-only static analysis would miss (e.g. ADV-60..72 resilience checks are inherently dynamic).

If no device is available, skip this phase and say so explicitly in the report (Appendix C). Don't silently under-cover STO/CRY runtime verification and the ADV-60..72 resilience block, which the reference docs call out as needing a connected device.

### Phase 4: Adversarial exploitation panel
This is the centerpiece: no finding becomes **Confirmed** without surviving it. Full decision rules live in `references/severity-rating.md`. Read that yourself before running this phase (you apply its rule in step 3 below), and pass its content or resolved absolute path to the prosecutor and every skeptic instance when you spawn them (see "Resolving reference-doc paths for spawned agents" above). Don't assume they can find it on their own.

For every finding with `status: "candidate"`:
0. You (the orchestrating session) set that finding's `status` to `"under-review"` in `findings.jsonl` the moment you hand it to the prosecutor. This is the only `findings.jsonl` write in this phase that happens before a verdict exists, so the file always reflects what's actively in flight.
1. Spawn `exploit-verifier-prosecutor` on that finding (and any related findings merged into it per the dedup rule in `references/report-template.md`). It writes the strongest honest exploitability case into `exploitation/<finding_id>.md`. Note it does **not** write to `findings.jsonl`. Neither it nor the skeptics do, by design (see their "Discipline" sections); that keeps their tool grant read-mostly and keeps one single place (here) responsible for the central file.
2. Spawn 2 independent `exploitability-skeptic` instances in parallel on the prosecutor's case (3 if the prosecutor rated it critical/high). Each is blind to the others' verdicts, each tries to refute, each writes its verdict to its **own** file, `exploitation/<finding_id>.skeptic-<label>.md` (e.g. `.skeptic-1.md`, `.skeptic-2.md`), never to the prosecutor's file or to each other's files. Having every parallel skeptic instance append to one shared file is a real Read-then-Write race, confirmed by an actual occurrence during this skill's own reproduction walkthrough (see `examples/steps-to-reproduce.md`), not a hypothetical worry: two instances can both read the file before either writes, then the second append silently overwrites the first. Separate files make the collision structurally impossible instead of relying on timing.
3. **You** read the prosecutor's file and every skeptic's separate verdict file, then apply the evidence-primacy decision rule from `severity-rating.md` to the complete set. In short: any single *well-evidenced* `refuted` wins regardless of how many skeptics said `stands` (-> `false-positive` or `potential` depending on whether the path is fully closed); otherwise `stands` + the evidence bar -> `confirmed`; unresolved -> `potential`. Read the full rule before applying it, especially its definition of "well-evidenced," which is what actually resolves the hard case of a well-evidenced minority refutation against a well-evidenced majority stands. Then consolidate everything, the prosecutor's case, every skeptic verdict in full, and your own decision and reasoning, into the single canonical `exploitation/<finding_id>.md` file, in that order. You are the only writer of this consolidated file and you write it only after every skeptic for this finding has finished, so this step has no concurrent-write risk even though the skeptics' own writes did. Finally, write `status` and `final_severity` (not `severity_initial`, which is never overwritten) into that finding's record in `findings.jsonl`, per `finding-schema.md`.

This is naturally a **pipeline**: each finding moves through prosecutor -> skeptic-panel independently of the others, so don't serialize across findings. Run as many finding-pipelines concurrently as your harness allows. If you have the Workflow tool available *and the user has explicitly opted into multi-agent orchestration* (an "ultracode" session, or they asked for it directly), this phase maps cleanly onto `pipeline()` with a `parallel()` skeptic stage per item. See this repo's `agents/exploit-verifier-prosecutor.md` and `agents/exploitability-skeptic.md` for prompts to drop straight into `agent()` calls. Otherwise, drive the same logic with sequential Agent-tool calls per finding; correctness matters far more than parallelism here.

Low-severity/purely-informational findings (resilience gaps on apps with no high-value asset, cosmetic best-practice deviations) can skip the full panel and go straight to `informational`. Don't spend a 3-skeptic panel on "no `FLAG_SECURE` on a non-sensitive screen." Use judgment; the panel exists to protect against over- and under-claiming on findings that actually matter.

### Phase 5: Report synthesis
Spawn `report-synthesizer` with the complete `findings.jsonl`, all `exploitation/*.md` transcripts, `target-profile.md`, and the content or resolved path of both `references/report-template.md` and `references/report-template.html`. It dedupes, fills both templates, and writes `engagement-<slug>/report/final-report.md` and `engagement-<slug>/report/final-report.html`: a well-formed, self-contained, color-coded HTML report, not just a markdown-to-HTML conversion. The HTML file is the primary deliverable; lead with it when you hand this back to the user, and if they're working in an environment with the Artifact tool, offer to publish it there too, since a MASVS report is exactly the kind of deliverable meant to be shared, not left in a terminal.

## Scaling to the ask
- "Quick check for X" (e.g. "does this app pin certs?"): skip the full pipeline, run only the relevant specialist (likely `resilience-anti-tamper-auditor` or `network-backend-auditor`) plus a focused prosecutor/skeptic pass on anything it finds. No need for recon-triage's full attack-surface inventory or a full report.
- "Full audit" / "MASVS assessment" / "pentest this app": run the whole pipeline as described.
- "Is this specific finding actually exploitable?" (user already has a candidate issue): skip straight to Phase 4 on that one finding; still write it into `findings.jsonl` first so it's in the schema the panel expects.

## What this skill will not do
It will not attempt to weaponize a confirmed finding beyond what's needed to prove exploitability (no building a working malware sample, no mass-exploitation tooling, no bypassing anti-abuse controls on a system the user doesn't own/control). It will not run against a target without a satisfied Step 0. It will not report a finding as Confirmed on vibes. That's the entire point of Phase 4.
