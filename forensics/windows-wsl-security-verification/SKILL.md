---
name: windows-wsl-security-verification
description: >-
  Am I compromised? After supply-chain news — a poisoned npm/PyPI package, a
  malicious VS Code extension, a backdoored dep that ran as you — this runs a
  guided IOC triage of a Windows + WSL2 dev box, then trims the attack surface
  the next compromise would use. WSL side: known-bad package versions,
  ld.so.preload, persistence (systemd/cron/autostart), planted SSH keys,
  shell-rc injection, executable .pth. Windows side: full AV scan (a
  third-party AV makes Defender passive — one scan, not two), second-opinion
  scan, Sysinternals Autoruns with VirusTotal, code --list-extensions,
  scheduled tasks, BYOVD-class drivers. Carries the discriminators that stop
  false alarms: filename IOCs via find not grep, VT named-family verdicts over
  aggregate labels, web-filter blocks vs infections. Fires on "am I hacked",
  "did I get owned", a named bad package or CVE in your dependency chain, or
  an AV detection you're unsure how to read. Windows/WSL-specific; verifies —
  does not harden. A clean result raises confidence, never proves.
---

# Verify a Windows + WSL Dev Box After a Supply-Chain Scare

**Seed question:** *A dependency that ran as me may have been malicious — did anything take hold, is anything still resident, and what surface should I close while I'm looking?*

## Core Capability

Supply-chain compromise — a poisoned npm/PyPI release, a trojaned VS Code extension, a backdoored CI dependency — runs with *your* permissions the moment you install it. Its real prizes are **credential theft and network exfiltration**, not vandalizing your filesystem. This skill turns "am I compromised?" from an anxiety spiral into a finite procedure: a worst-first IOC sweep of both halves of a Windows + WSL2 box, a set of discriminators that keep ambiguous evidence from being misread in either direction, and a surface-reduction pass so the time spent looking also shrinks the next attack's room to move.

The discriminators are the value. Anyone can paste a checklist; what wrecks a triage is misreading the output — a content-grep "finding" your own research notes, a VirusTotal aggregate label screaming trojan at grayware, a web-filter popup read as an infection. Each step below carries the reading rule next to the check.

## Scope

**Windows host + WSL2, specifically.** The checks are tool-concrete — Sysinternals Autoruns, Defender/third-party AV interplay, Task Scheduler, `code --list-extensions`, `wsl.conf`-era WSL2 — and tool-concrete is what makes them runnable rather than aspirational. macOS and bare-Linux boxes need sibling skills with their own tools (see Integration); this one does not pretend to cover them.

**Verification, not hardening.** This skill answers "did I get hit, and what can I close right now?" Hardening — sandbox distros, secrets isolation, egress control, container/microVM tiers — answers "make this box safer going forward": a different trigger, a different working mode (interactive, system-specific), a different job. This skill hands off to that track at the end; it does not bundle it.

**The honest ceiling, stated up front:** you cannot *prove* a machine clean — a good rootkit's job is to hide from exactly these checks. IOC triage is asymmetric: a **hit is meaningful**; a **clean result raises confidence without being proof**. Every verdict this skill produces says so.

## When This Applies

**TRIGGER** (offer the triage — the user may not know to ask):
- "Am I hacked / compromised / owned?", "did that package do something to me?", "is this malware?" — in any phrasing.
- A named bad package, version, or CVE appears in the user's dependency chain — supply-chain incident news (a LiteLLM/TeamPCP-class event, an npm worm, a trojaned extension) where the user *ran* the ecosystem in question, **even if they never ask about their own box**.
- An AV detection, VirusTotal score, or web-filter block the user is unsure how to read.
- An unfamiliar autostart, scheduled task, service, or driver was noticed and "should I worry?" is in the air.

**DO NOT TRIGGER / skip quietly:**
- General hardening intent ("make my machine safer", "sandbox my agents") with no compromise question attached → that's the hardening track, not this skill; point there in one line.
- The box is macOS or Linux-without-Windows → say so and name the gap; do not run Windows steps that can't apply.
- Abstract security discussion, CTF/coursework, or analysis of *someone else's* incident with no live "is THIS box clean?" question.

---

## Step 0 — Frame: what you're defending, worst-first

Before any command, fix the mental model — wrong models misallocate the whole triage:

- **WSL is not a security boundary.** Every WSL↔Windows feature exists for seamless integration, the opposite of isolation. All WSL2 distros share one kernel, one utility VM, one network namespace.
- **The bridges, worst-first:** (1) **interop** — WSL can launch Windows executables that run as your Windows user, direct cross-OS code execution; (2) **drive mounts** — `/mnt/c` write access; (3) **`\\wsl$`** — Windows reading the Linux filesystem, secondary because it needs a Windows-side trigger.
- **The prizes are credentials and egress.** A supply-chain payload's first move is harvest-and-phone-home. So the triage weights credential stores and persistence over "did it write to C:".

## Step 1 — WSL/Linux IOC sweep

Run the checklist in `reference/wsl-linux-ioc-checklist.md` — known-bad package versions, rootkit preload, persistence vectors, planted SSH keys, shell-rc injection, executable `.pth` files, plus a secrets-exposure inventory. Each check there carries its command *and* what a hit means. Work through all of them even after an early "clean" — the vectors are independent; a clean `ld.so.preload` says nothing about cron.

## Step 2 — The filename-IOC discriminator (before you declare a hit)

For an IOC that is a **named file**, search with `find -name` (or hashes) — **never content-grep**. The moment you research an IOC, its name enters your shell history, session transcripts, and notes; `grep -rl` will then "find" it everywhere and the hits are *your own research*, not the artifact. A filename IOC exists as a *file*; test for the file. (Lived false alarm: four content-grep hits on a backdoor's `.pth` filename — all four were session transcripts discussing it; `find -name` came back empty.)

## Step 3 — Windows-side checklist

Run `reference/windows-checklist.md`: full AV scan, second-opinion on-demand scanner, Sysinternals Autoruns review (with its red/yellow/VT reading legend), `code --list-extensions` against verified-publisher *namespaces*, scheduled tasks. Two interplay rules from that pack worth knowing before you start:

- **A third-party AV (Bitdefender, etc.) is the *active* engine and pushes Defender to *passive*.** Its full scan covers the "full AV scan" item — running `Start-MpScan` on top duplicates hours of I/O for no added coverage.
- **Autoruns is the hub.** Its Scheduled Tasks tab subsumes `Get-ScheduledTask`; its Drivers tab is where BYOVD-class leftovers surface. One tool, several checklist lines.

Most Windows steps are GUI- or host-side and can't be run from inside WSL — drive them as instructions to the user, and record their reported results in the output.

## Step 4 — Read detections without panic (or false comfort)

Every non-zero scan result goes through `reference/interpreting-detections.md` before it becomes a verdict. The two discriminators that pack carries:

- **VirusTotal: named-family verdicts over the aggregate label.** "14/70, popular threat label: trojan.X" can still be grayware: when the *named-family* engines (ESET, Malwarebytes, Fortinet, Ikarus…) all say `PUA/PUP/Riskware` with `family: <the app itself>`, and the "trojan" rows are generic ML/heuristic engines tripping on `upx` + `persistence` + `detect-debug` tags — the substance is "the app is junkware," not "a trojan is wearing its name." Those are different verdicts with different responses.
- **A web-filter block is a *destination-reputation* event, not an infection finding.** A browser can re-touch a stored URL with zero clicks (new-tab tile favicon/preconnect); the AV flags the destination's category. The confirming field is the **process** that made the request — a browser process is consistent with benign. Check whether the popup even exposes the process before promising that check.

## Step 5 — Surface reduction (the "while I'm here" pass)

Walk the Autoruns/extensions/tasks inventory once more with a different question: not "is this malicious?" but **"do I actually use this?"** Every autostart, service, and driver is attack surface + persistence real-estate + patch liability, *whatever* its intent. The pack's reduction list flags the special cases — BYOVD-class low-level drivers (hardware-monitor leftovers attackers bring *in* by name), remote-access tools, idle-compute rental agents, stale unquoted-path tasks. Uninstall/disable what isn't used; record what was removed and why.

## Output format

```
BOX: <host / role>
THREAT CONTEXT: <what prompted this — package/CVE/detection/routine>
WSL-LINUX IOCs: <per-vector: HIT / clean / not-checked>
WINDOWS CHECKS: <AV / second-opinion / Autoruns / extensions / tasks: verdicts>
DETECTIONS READ: <each alert → malware / grayware / false-positive, with the named-family or process basis>
SURFACE REMOVED: <what was uninstalled or disabled, and why>
RESIDUAL GAPS: <what was not checked, plus the standing evasion ceiling>
VERDICT: CLEAN-SO-FAR (confidence raised, not proof) / COMPROMISED (→ contain: isolate, rotate credentials from a clean device, rebuild) / INCONCLUSIVE (name what would resolve it)
NEXT: <the hardening track, if wanted>
```

Keep RESIDUAL GAPS and the verdict's parenthetical always — they are what keeps the output honest about the ceiling.

## Worked examples

**The grep false alarm.** During a triage for a backdoored PyPI release, `grep -rl` on the dropper's filename returned four hits — heart-rate moment. All four were the session's own transcripts and notes, which contained the string *because the IOC had just been researched*. `find -name` across the filesystem: empty; the installed versions predated/postdated the bad releases. Verdict: clean on that vector. The lesson is Step 2 — a filename IOC is a file, so test for the file.

**The 14/70 "trojan" that was grayware.** Autoruns + VirusTotal flagged a torrent client at 14/70 with aggregate label "trojan.<appname>". Reading the engine rows: every named-family verdict said PUA/Riskware with the app itself as the family; the "trojan" rows were generic ML engines reacting to the packer and autostart behavior. Verdict: the real app, classified as junkware — uninstall because it's junk you don't use (Step 5), not because a trojan was found (Step 4). Same action, different verdict — and the difference matters for whether you must now rotate credentials.

**The web-filter popup at 2am.** An AV web-filter block fired while opening a *new browser tab* — no link clicked. Cause: the new-tab page's "top sites" tile re-requested a stored historical URL (favicon fetch), and the AV flagged that destination's reputation category. A page-load block of a remembered URL, originating from the browser, is not a malware finding; the box's verdict didn't change. Follow-up was privacy hygiene (remove the tile, clear the history entry), not incident response.

## Integration

| Skill / component | Relationship |
|-------------------|-------------|
| **security-toolkit hooks** (prompt-injection detection, dangerous-git blocking, PR-merge guard) | The *prevention* layer of the same plugin — they reduce the chance an agent-driven compromise happens. This skill is the *detection/recovery* layer for when prevention may have already failed. Same threat lens, different moment. |
| **research-toolkit / iterative-verification** | The evidence-honesty discipline this skill borrows: no confirmation = UNVERIFIED, not DISCONFIRMED. A vector you didn't check is "not-checked", never silently "clean". |
| **macOS / bare-Linux verification siblings** *(not built yet)* | The same "am I compromised?" trigger needs OS-specific tools elsewhere. Sibling skills, not a bloated cross-OS version of this one — they'll be built when those workflows are lived. |
| **Hardening track** *(separate concern; skill-set to follow)* | Where NEXT points: hardened sandbox distro (interop/automount off) → secrets out of the blast radius → default-deny egress → throwaway containers → gVisor → microVM, in reward-per-effort order. Kept out of this skill because its workflow is interactive, system-specific, and only a skill once it has been fully lived. |

**Workflow position:** fires on a compromise question or an unread detection → frame (Step 0) → sweep both sides (Steps 1, 3) with the discriminators (Steps 2, 4) → reduce surface (Step 5) → verdict with gaps stated → hand off to hardening if the user wants the forward-looking half.

## Self-Reflexivity

- **The known-bad list is a snapshot.** Named bad versions and campaigns in the reference pack are worked examples of the *class*, not an exhaustive feed; absence from the list is not cleanliness. For a current incident, fetch the advisory's own IOC list and apply the same discriminators.
- **A clean verdict can be wrong.** The evasion ceiling is structural — state it every time rather than letting a tidy CLEAN-SO-FAR read as proof. If the user needs proof-grade assurance, the honest answer is rebuild-from-known-good, not more scanning.
- **The skill can manufacture panic.** Checklists amplify ambiguity into dread; the discriminators (Steps 2 and 4) exist to push back in *both* directions. If a finding survives a discriminator, escalate calmly; if it doesn't, close it and say why.
- **Windows/WSL vantage only.** Run on the wrong OS, the tool names stop being load-bearing and the skill degrades into generic advice — better to say "wrong skill for this box" than to improvise coverage.

## Vasana

A vasana is a pattern that persists across unrelated contexts. If during
this task you notice such a pattern emerging, it may be worth capturing.
This skill works best alongside the `vasana` skill and `vasana` hook
from the Vasana System plugin.

Modify freely. Keep this section intact.
