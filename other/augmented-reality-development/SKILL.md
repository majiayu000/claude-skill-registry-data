---
name: augmented-reality-development
description: "Use when building or modifying an augmented-reality experience that aligns digital content with camera imagery, tracked devices, or physical surfaces to define coordinate spaces, tracking inputs, permission boundaries, and a safe test method before adding interaction. Trigger for AR scene placement, anchors, pose tracking, or camera-based overlays."
---

# Augmented Reality Development

## Overview

This skill applies when building or modifying an augmented-reality experience that aligns digital content with camera imagery, tracked devices, or physical surfaces. Its intended outcome is to define coordinate spaces, tracking inputs, permission boundaries, and a safe test method before adding interaction.

## When to Use

### Preserved source section: When to Use

Use for an application that combines a live or recorded view of the physical world with spatially anchored digital content. Distinguish marker-based, plane/anchor-based, and location-based behavior because their sensors and failure modes differ.

## Scope

**Does:** Follow the task boundary stated under When to Use and Instructions.

**Does not:** See the preserved source boundaries below and under Stop Conditions.

### Preserved source section: Safety and Privacy

Request camera and location access only when needed, explain the purpose, and minimize capture and retention. Do not record or upload surroundings by default. Avoid instructions that require users to move while looking only at a screen; provide a safe pause or exit state.

### Source boundary statements from: Procedure

4. **Control timing and anchors.** Use timestamped pose data, keep image and pose timing aligned, and define anchor lifetime and relocalization behavior. Avoid claiming world stability that the selected platform cannot guarantee.

## Inputs

**Required:** See the preserved source input guidance below.

**Optional:** Not specified in source skill.

**Prerequisites:** Not specified in source skill.

### Preserved source section: Inputs

- Supported device, operating system, AR runtime, camera, and tracking capabilities.
- Coordinate frames, expected environment, target interactions, and latency requirements.
- Permission, privacy, retention, and physical safety requirements.

## Instructions

### Preserved source section: Procedure

1. **Define the spatial contract.** Document world, camera, device, and content coordinate frames, units, handedness, and transform direction. Test conversion with known poses.
2. **Build a non-interactive placement slice.** Display one object from a recorded or simulated pose source before adding persistence, gestures, or networking.
3. **Handle tracking state explicitly.** Model unavailable, initializing, limited, relocalizing, and stable tracking. Hide, freeze, or fade content according to a deliberate loss-of-tracking policy.
4. **Control timing and anchors.** Use timestamped pose data, keep image and pose timing aligned, and define anchor lifetime and relocalization behavior. Avoid claiming world stability that the selected platform cannot guarantee.
5. **Add interaction and accessibility.** Make selection, placement, reset, and exit discoverable. Provide non-AR alternatives where practical and avoid visual effects that obscure hazards or essential surroundings.
6. **Test safely.** Prefer prerecorded sessions and a controlled space. Check drift, occlusion assumptions, lighting variation, camera movement, interruption, and permission denial on supported devices.

## Decision Rules

The following source conditional guidance is preserved verbatim; no unstated action is inferred.

### Source conditional guidance from: Safety and Privacy

Request camera and location access only when needed, explain the purpose, and minimize capture and retention. Do not record or upload surroundings by default. Avoid instructions that require users to move while looking only at a screen; provide a safe pause or exit state.

### Source conditional guidance from: Output and Acceptance

Describe supported devices, spatial assumptions, tracking-loss behavior, data handling, and test conditions. Accept only when object placement is coherent in the defined coordinate frame, tracking failure is handled visibly, and permissions and safety behavior are verified.

## Output Format

### Preserved source section: Output and Acceptance

Describe supported devices, spatial assumptions, tracking-loss behavior, data handling, and test conditions. Accept only when object placement is coherent in the defined coordinate frame, tracking failure is handled visibly, and permissions and safety behavior are verified.

## Validation Checklist

- [ ] Verify the source-defined success criteria above.

## Edge Cases and Recovery

### Source edge/failure guidance from: Output and Acceptance

Describe supported devices, spatial assumptions, tracking-loss behavior, data handling, and test conditions. Accept only when object placement is coherent in the defined coordinate frame, tracking failure is handled visibly, and permissions and safety behavior are verified.

## Stop Conditions

### Source stop-related guidance from: Safety and Privacy

Request camera and location access only when needed, explain the purpose, and minimize capture and retention. Do not record or upload surroundings by default. Avoid instructions that require users to move while looking only at a screen; provide a safe pause or exit state.

## Examples

Not specified in source skill. The original provided no input/output example, and none has been invented.

## Success Criteria

### Acceptance criteria from source: Output and Acceptance

Describe supported devices, spatial assumptions, tracking-loss behavior, data handling, and test conditions. Accept only when object placement is coherent in the defined coordinate frame, tracking failure is handled visibly, and permissions and safety behavior are verified.
