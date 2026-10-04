---
name: cross-camera-metric-calibration
description: Use when relating two cameras' views metrically (projecting one camera's 3D into another, borrowed-depth supervision, multi-view rigs) — lock consumer-camera auto modes, checkerboard-calibrate intrinsics, solve the extrinsic from stereo-3D↔2D correspondences, and validate end-to-end with class-agnostic geometry.
stacks: [python]
domains: [hardware]
phases: [dev]
tags: [calibration, stereo, extrinsics, intrinsics, opencv, pnp, webcam]
scope: kit
---
**When to use.** Any two-camera (or camera+sensor) metric relationship. *Why:* every failure mode
here was silent — spec-sheet FOVs that match no runtime mode, autofocus drifting the focal length,
PnP that is right only up-to-scale, and detector labels that alias across views.

**Procedure.**
1. Kill the auto modes first (auto-framing, autofocus, FOV) in the vendor tool; recapture working
   frames immediately before calibrating. Measure the printed checkerboard square — printers rescale.
2. Calibrate intrinsics per camera (`findChessboardCornersSB` for low-contrast boards); a spec FOV is
   a candidate, never a calibration. Single-view PnP without calibrated intrinsics is scale-ambiguous.
3. Solve the extrinsic: 3D points from the metric camera (stereo/depth) ↔ 2D features in the other;
   seeded `solvePnPRansac` + `solvePnPRefineLM`. Record which physical act invalidates what
   (re-aiming kills extrinsics; intrinsics survive if FOV/focus untouched).
4. Validate end-to-end, class-agnostically: project detections across cameras and match by geometry
   (center distance / box containment) — labels alias across views (the same figurine read "person"
   and "teddy bear"). Save the overlay as evidence.
5. **Done when:** feature reprojection ~1 px, cross-projected items land on their counterparts
   (~10 px), and the invalidation rules are written into the resume surface.

**Knowledge:** FIELD-KNOWLEDGE-GILBERT.md §G2.
