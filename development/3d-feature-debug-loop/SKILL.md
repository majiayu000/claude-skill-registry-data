---
name: 3d-feature-debug-loop
description: Use when iterating on a complex visual / 3D feature where user feedback keeps surfacing the same kind of bug after several "fix" attempts. The methodology is diagnostic-first — read the actual code paths, spawn research agents for ground truth, sim-validate before shipping, never claim "fixed" without observed evidence. Triggers on 3D bug iteration, visual feature stuck, user keeps reporting same issue, iteration discipline.
---

# 3D Feature Debug Loop — Diagnostic-First Discipline

## The pattern this skill prevents

You ship a fix. User reports it's still broken or worse. You ship another fix. User reports same thing. After 5 iterations, the user says "you're guessing and refusing to find improvements based on actual observation."

This is the trust death-spiral. The root cause is **shipping without observed evidence**. Each iteration is a hypothesis that LOOKS plausible but wasn't validated against the actual rendered output.

## When to invoke this skill

- A 3D / visual feature has been iterated on for 3+ rounds with the same user feedback returning
- A user explicitly says "you keep saying it's fixed and it isn't"
- You're about to make a change without first observing the current behavior
- You catch yourself describing what you INTENDED rather than what you SEE

## The discipline

### Rule 1: Read the actual code before changing it

When the urge to "fix" arrives, resist it. Open the file. Read the function. Trace the data path:

> What's the actual flow from texture URL → loaded UIImage → CGImage → TextureResource → Material binding → ModelEntity → RealityRenderer → CVPixelBuffer → post-process → output frame?

Each arrow is a potential bug site. Each parameter at each step affects the final pixels. Don't assume; grep, read, understand. Use the Read tool on every file in the chain.

### Rule 2: Spawn a research agent for ground truth

When you've been guessing for >2 iterations, the right move is to delegate research to a fresh agent:

```
Agent (general-purpose):
  Description: "Deep-dive [feature] rendering + diagnose [bug]"
  Prompt: [self-contained briefing including:
    - what the user reported
    - what you've tried + why it didn't work
    - exact files to read with line numbers
    - the specific question (e.g., "what does set_opacity() actually do
      in CustomMaterial premultiplied-alpha output?")
    - request: report findings with file:line citations, not guesses]
```

A research agent has no anchoring bias from your previous failed attempts. It reads the code fresh + searches docs + reports. The cost is 5-10 minutes of agent time vs. another failed iteration.

Real-world example from BOBA Playbook Hero Shot:

> User had reported "black specks moving across the card" for 4 iterations. Each fix attempt failed. I spawned a research agent to investigate. It found in 10 minutes: RealityKit CustomMaterial output is premultiplied-alpha → `base_color=(0,0,0)` + `opacity=1` premultiplies to BLACK opaque at the sparkle pixels. That's the bug. Documented with Apple Developer Forum citation. Fix was one line. Without the agent, I would have continued guessing for hours.

### Rule 3: Sim-validate BEFORE shipping to device

If the feature renders an image / video, build an offline sim that mirrors the iOS scene graph. Render the same scene to a PNG. Inspect via Read tool. **Always** look at the output before claiming fix.

See [[3d-feature-sim-validation]] for the full pattern. Key points:

- Compile macOS RealityFoundation sim via `DEVELOPER_DIR=/Applications/Xcode.app/Contents/Developer xcrun -sdk macosx swiftc`
- Render at multiple keyframes (12 yaw angles, camera arc waypoints, etc.) — single hero pose hides edge-case bugs
- Composite into a contact sheet PNG
- Read tool decodes PNG as multimodal image → you can SEE the output

### Rule 4: Describe what you see, not what you intended

Catch yourself in the act. When writing a status update for the user, ask: am I describing the rendered output or the code I wrote?

**Wrong**: "I switched to UnlitMaterial which should give vivid pigment with no washout."

**Right**: "In the rotation strip render, yaw=0° shows the Bojax card with clear purple/black art and no obvious washout. yaw=180° shows the back as a solid white rectangle with no logo visible — this is a back-plane PBR bug, see frame ../v68_rotation_bojax.png."

The first is hope. The second is evidence.

### Rule 5: Track iteration history honestly

Each commit message should:

1. Quote the user feedback in question marks
2. State the specific change (file:line + diff intent)
3. Describe what you OBSERVED in the sim render to confirm the fix
4. Acknowledge what's NOT verified (e.g., "Sim-validated. Not yet device-tested.")

When a fix fails, the next commit should reference the prior commit and explain why the hypothesis was wrong. Lying about progress (e.g., calling something "fixed" without observed evidence) compounds the trust deficit.

## The "I don't know what I'm looking at" red flag

When debugging a visual bug, ask yourself: can I describe, in concrete terms, what the current rendered output looks like? Not "the card art" — "the card is showing as a solid magenta rectangle with no Bojax player visible, surrounded by an orange rim at the edges."

If you CAN'T describe the output that specifically, you don't know what you're looking at. Stop. Instrument. Render the sim. Read the PNG.

A symptom of this failure: you describe the BUG ("the card disappears partially as it rotates") in the same language the user used, without ever having seen it yourself. That means you're working from a verbal report, not from observation. The next step is to OBSERVE, not to guess at the cause.

## The interrupt pattern when the user pushes back

If a user says any of:
- "You keep saying it's fixed and it isn't."
- "You're guessing."
- "Refusing to find improvements based on actual observation."
- "You introduced this bug."

That's the signal to stop the current iteration loop and reset. Concrete actions:

1. **Don't** immediately ship another hypothesis
2. **Do** spawn a research agent with the user's exact quote in the briefing
3. **Do** acknowledge in the next message that you've been guessing + state the new methodology
4. **Do** render the sim BEFORE the next commit

The user is the most expensive review surface in the loop. Their pushback is concentrated signal that the cheap reviewers (agent, sim, code-reading) have been skipped.

## Common debug-loop failure modes

### Failure: hypothesis × hypothesis stack

You ship fix A. Bug returns. You assume A worked + ship fix B for a "different" cause. But A didn't actually fix anything; you've now compounded two unverified hypotheses. Untangling requires reverting.

**Prevention**: every shipped fix must have observed evidence (sim render or device test) BEFORE the next change.

### Failure: changing one thing means rechecking everything

A 3D scene has interlocking parameters: light intensity × IBL exponent × material clearcoat × post-process EV all contribute to perceived brightness. Changing any one without re-validating the whole scene means a "fix" can introduce a regression elsewhere.

**Prevention**: after every change, re-render the FULL sim contact sheet (all 12 yaw angles, all camera waypoints). Look at every cell. Bugs hide in cells you didn't expect to be affected.

### Failure: "the agent said X" doesn't mean X is right

Research agents are tools, not authorities. Their findings are starting points to verify. If an agent says "set_opacity() works in premultiplied alpha pipeline," check the docs URL the agent cited. If the citation supports the claim, you're good. If the agent invented the URL or misread it, you're back to guessing.

**Prevention**: always verify the agent's specific claim has a citation you can read.

### Failure: shipping at midnight expecting things to work

After many hours of debugging, the temptation to "ship one more fix and hope" is strong. This is usually the last fix that breaks the most.

**Prevention**: at 3+ failed iterations in a session, stop. Document what you've tried. Pick up fresh tomorrow with the research agent + sim-validation discipline from the start.

## Working backward from a bug report

When a user reports a specific visual bug:

1. **Reproduce the exact frame** in the sim (or get a screenshot from the user)
2. **Describe the bug in pixel-level terms**: "I see X at coordinates Y, surrounded by Z"
3. **Form a hypothesis** about which step in the data path produces it
4. **Test the hypothesis** by changing ONE parameter and re-rendering
5. **If the hypothesis was wrong**, document that as a NEGATIVE finding (so you don't retest it later) and form a new hypothesis

A negative finding has just as much value as a positive one. Both shrink the search space.

## Real-world example: BOBA Playbook Hero Shot

Iteration history (50+ commits, 15+ user pushback rounds):

- **v6.5–v6.9**: shipped 4 sparkle-overlay fixes, each producing a different artifact. Each shipped without sim validation.
- **v6.9 research agent**: identified premultiplied-alpha trap + over-resolved camera framing. First evidence-based diagnosis.
- **v7.0**: shipped the agent's recommendations (pull camera back, drop overlay) BUT skipped sim validation. User: "card is too small, still washed out."
- **v7.0 → v7.1 reset**: spawned second research agent. Identified that the v6.0 ERA's PBR pipeline didn't have these bugs (Lambert softening masks pixelation; clearcoat-free back doesn't wash). Restored that pipeline with the bugs fixed.
- **v7.1 → v7.2 → v7.3**: sim-validated each ship. Each iteration small (one or two parameters). User confirmed "very close to shipping version" at v7.3.

The turning point was the research-agent + sim-validation pair at v6.9 and v7.1. Before that, every iteration was a guess. After that, every iteration was an observation.

## See also

- [[3d-feature-sim-validation]] — the offline-sim methodology this discipline depends on
- [[realitykit-3d-card-rendering]] — RealityKit patterns this discipline is most often applied to
