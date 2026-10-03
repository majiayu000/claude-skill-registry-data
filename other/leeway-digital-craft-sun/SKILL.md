---
name: leeway-digital-craft-sun
description: Evidence-bound four-ray digital craft evaluation for design/accessibility, motion/interaction, graphics/runtime and performance/hardware, with normative accessibility hard gates and project-specific elite targets.
license: MIT
---
# LeeWay Digital Craft Sun

## Four rays
1 DESIGN_SYSTEMS — token/component consistency, typography/color intent, applicable accessibility.
2 MOTION_INTERACTION — target state, velocity/phase continuity, interruption, gesture/state correctness, reduced-motion behavior.
3 GRAPHICS_RUNTIME — shader/geometry correctness where applicable, resource/batching/pipeline profile, visual artifact state.
4 PERFORMANCE_HARDWARE — frame pacing, interaction/loading/stability metrics, memory/VRAM, network and energy/thermal profile.

For evidence-bound x_j,W_j,theta_j: r_j=sqrt(x_j^T W_j x_j); b_j=1 iff r_j<=theta_j. Omega=sum(b_j*2^(4-j)); Omega_max=15; Phi=product(b_j).

## Standards hierarchy
Normative accessibility requirements and essential functional correctness are hard gates. APCA, damping ratio, modular scales, 120Hz, INP<50ms, LCP<1.5s and similar elite targets are versioned project profiles unless/until they become applicable standards.

## SDF boundary
The Eikonal |grad f|=1 expectation applies to true signed-distance representations in valid regions; procedural shader effects are not rejected merely because they are not exact SDFs.

## Performance boundary
Core Web Vitals baseline and LeeWay elite targets are separate. Frame period is not identical to application CPU/GPU work budget. Claims require device/browser/network/percentile context.
