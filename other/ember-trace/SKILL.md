---
name: ember-trace
description: Zuko's ember trace for runtime forensics. Follow the embers back to the fire that started them. Use for runtime-forensics or trace-forensics, a memory leak, an idle CPU spin, a visual glitch, a hang, or a captured cpuprofile, trace, spindump, or heap snapshot handed over after the fact. The deliverable is a cited diagnosis, not a fix.
---

# Zuko's ember trace

When Zuko tracked the Avatar, he did not guess where the fire started. He read the scorch marks and followed the embers back to their source. Forensics is the same. You do not theorize from source code. You read the evidence the running system left behind and follow it to the line that lit it.

You own the diagnosis. The deliverable is a cited diagnosis, not a fix. Fix only when asked. Once the cause is known, hand it to `healing-water` for a defect or `breath-of-fire` for slowness.

On Codex, read [avatar-mode/references/codex.md](../avatar-mode/references/codex.md) for tool equivalents.

## Pick the mode

| You have | Mode | Steps |
|----------|------|-------|
| A live process showing the symptom now | Live | [references/live.md](references/live.md) |
| A captured artifact (cpuprofile, `.json.gz` trace, spindump, heap snapshot) and no live process, or one you must not disturb | Artifact | [references/artifact.md](references/artifact.md) |

If you have both, start from the artifact and use the live process to prove the mechanism.

## Rules for both modes

- A real artifact, not a guess. The evidence is what the system recorded, not what the source suggests.
- Parse large artifacts away from the main thread. When the top-level session runs this skill, dispatch the parsing to `team-avatar:zuko` on Zuko's model from the avatar-setup sheet, with an effort level that fits the job, and keep only the reduced finding in the main thread (Guard the Context Window, Fire in `four-elements`). When you are already a dispatched character, reduce it yourself with a script and read only the script's output.
- Map every finding to source: file, symbol, and the line that allocates, schedules, or blocks. A frame with no source location is not yet a diagnosis.
- Label confidence. A mechanism you proved is a cause. One the evidence only supports is the strongest hypothesis, and you say so.
- No change set ships from this skill, so there is no throughput or PR step.

## Reply

The signal or artifact and its format, the reduced finding, how you proved the mechanism (or that it is the strongest hypothesis), the source location, and the artifact paths. No fix unless asked.
