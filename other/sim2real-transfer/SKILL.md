---
name: sim2real-transfer
description: Use when a policy or controller trained/tuned in simulation must run on the real robot — close the gap with domain randomization for what you can't measure and system identification for what you can.
stacks: [python]
domains: [hardware]
phases: [dev, gate]
tags: [sim-to-real, domain-randomization, system-identification, rl, robustness]
scope: kit
---
**When to use.** Before any sim-trained behavior touches hardware. *Why:* the sim-to-real gap fails
policies silently; randomize what you can't identify, identify what you can.

**Procedure.**
1. System-ID measurable params (joint friction, rotor inertia, actuator delay) against real logs so the nominal sim is correct.
2. Domain-randomize the rest (mass, friction, latency, lighting, textures) — tune ranges (too wide is unlearnable, too narrow overfits).
3. Validate across engines (dual-sim) before hardware.
4. **Done when:** the policy holds up in a held-out randomized sim *and* a supervised real-robot trial, with the gap quantified.

**Knowledge:** KNOWLEDGE-LIBRARY.md §B3.
