---
name: augmented-reality-from-scratch
description: "Use when implementing the core AR pipeline (camera pose estimation, marker tracking, projection overlay) from first principles — not when just using ARKit/ARCore/Unity's AR framework as a black box. Triggers on: 'build augmented reality from scratch', 'marker-based AR tracking', 'camera pose estimation', 'implement fiducial marker detection', 'AR projection matrix math', 'markerless AR tracking'. Covers marker-based vs markerless tracking, pose estimation, and the projection math to overlay 3D content on a camera feed."
origin: yana-ai — synthesized from public computer-vision literature on fiducial markers (ArUco) and SLAM fundamentals, plus community from-scratch tutorials indexed in codecrafters-io/build-your-own-x
license: Apache-2.0
version: 1.0.0
compatibility: yana-ai >= 0.43.2
---

# /augmented-reality-from-scratch

## When to Use

- Understanding or implementing the core AR pipeline (detect real-world reference → estimate camera pose → project virtual content) without a high-level AR SDK doing it for you.
- Choosing between marker-based and markerless tracking for a project, with the actual tradeoffs.
- Implementing fiducial marker detection (ArUco-style) or the projection math to draw a 3D object aligned with a live camera feed.

## Do NOT use for

- Shipping a real product AR feature — use ARKit (iOS), ARCore (Android), or a Unity/Unreal AR plugin; these handle sensor fusion, drift correction, and device-specific calibration far better than a from-scratch implementation should attempt to.
- General 3D rendering unrelated to camera-feed overlay — see `threejs-skills`/`spline-3d-integration` for that.
- Object recognition/classification (what is this object) as opposed to pose tracking (where is the camera relative to a known reference) — those are different computer-vision problems; see `vision-*`/OCR-related skills for recognition tasks.

---

## Marker-Based vs Markerless — Decide First

```
Need reliable tracking with minimal compute, willing to place a printed marker
in the scene?
  → Marker-based (Step 1-3) — detect a known pattern, pose is a direct
    geometric solve, robust and fast even on weak hardware

Need tracking without placing anything in the environment (point phone at
any room/surface)?
  → Markerless / SLAM-based (Step 4) — much harder: track arbitrary visual
    features frame-to-frame, no known reference geometry to solve against
```

Build the marker-based path first even if markerless is the end goal — it isolates and teaches the pose-estimation and projection math (Steps 2-3) without also solving the much harder "which features are reliable to track" problem markerless AR requires.

## Step 1: Fiducial Marker Detection

A fiducial marker (ArUco-style) is a square black-and-white pattern designed to be reliably detected and uniquely identified:

```
1. Convert frame to grayscale, threshold to pure black/white (adaptive
   thresholding handles uneven lighting better than a single global cutoff)
2. Find contours (connected boundary shapes) in the thresholded image
3. Filter to quadrilateral contours (4 corners, roughly convex) — most
   contours in a real scene aren't marker candidates, this filters fast
4. For each quad candidate: perspective-warp it to a flat square, sample
   the interior grid cells, decode the black/white pattern against your
   known marker dictionary (a fixed set of valid bit patterns with error
   correction, so partial occlusion/noise doesn't cause a misread)
```

## Step 2: Camera Pose Estimation (from a detected marker)

Once you know the marker's 4 corners in the 2D image AND you know the marker's real-world size (you printed it, so you know it's e.g. exactly 10cm square), you have a classic **Perspective-n-Point (PnP)** problem: given N known 3D points (the marker's corners in its own coordinate frame) and their corresponding 2D image projections, solve for the camera's rotation and translation relative to the marker.

This requires the camera's **intrinsic parameters** (focal length, optical center, lens distortion) — obtained via a one-time **camera calibration** step (photograph a known checkerboard pattern from multiple angles, a calibration algorithm solves for the intrinsics; OpenCV's `calibrateCamera` is the standard tool for this, don't hand-derive it). Without calibration, pose estimates will be systematically wrong in a way that's hard to diagnose (looks "close but off" rather than obviously broken).

The PnP solve itself outputs a rotation matrix + translation vector — together, the camera's full pose (position + orientation) relative to the marker's coordinate frame.

## Step 3: Projection — Overlaying 3D Content

With the camera pose from Step 2, overlaying a virtual object aligned to the marker is a standard 3D graphics projection, using the SAME camera intrinsics from calibration:

```
screen_point = Intrinsics × [Rotation | Translation] × world_point
```

Where `world_point` is a point on your virtual 3D object (defined in the marker's coordinate frame, so placing it "on top of the marker" is just world coordinates near the origin), `[Rotation | Translation]` is the camera pose solved in Step 2 (this is what makes the virtual object appear to stay locked to the marker as the camera moves), and `Intrinsics` is the same 3×3 calibration matrix from Step 2 (this is what makes the projected size/perspective match the real camera's actual lens).

Render the virtual object with this projection matrix on top of the live camera frame — every frame, re-detect the marker (Step 1) and re-solve pose (Step 2), so the overlay tracks marker movement in real time.

## Step 4: Markerless Tracking (SLAM fundamentals, high-level only)

Without a known marker, pose must come from tracking arbitrary visual features frame-to-frame:

```
1. Detect distinctive image features (corners/blobs — ORB or FAST detectors
   are the standard fast-enough-for-real-time choices)
2. Match features between consecutive frames (which feature in frame N
   corresponds to which feature in frame N+1)
3. Estimate camera motion from how matched features shifted (essential
   matrix / visual odometry — the 2D-to-2D analog of Step 2's PnP)
4. Maintain a map of triangulated 3D feature positions as the camera moves,
   and correct accumulated drift when previously-seen areas are re-observed
   (loop closure) — this is what separates full SLAM from simple visual
   odometry, which drifts unboundedly without it
```

This is a genuinely hard, research-grade problem (this is why ARKit/ARCore exist as heavily-engineered platform SDKs) — implementing a robust markerless tracker from scratch is a multi-month undertaking, not a weekend project. Understand the pipeline conceptually; don't expect a from-scratch implementation to match platform SDK robustness.

## What NOT to Do

- Don't skip camera calibration "to save time" — an uncalibrated projection produces overlays that are subtly, confusingly wrong (drifting scale/position) rather than obviously broken, which is much harder to debug than a missing feature.
- Don't attempt markerless tracking before marker-based tracking works end-to-end — Step 4 depends on understanding pose estimation and projection (Steps 2-3) which are far easier to validate against a known, controllable marker first.
- Don't re-derive PnP or camera calibration math by hand for a real project — use OpenCV's `solvePnP`/`calibrateCamera` (or platform equivalents); this skill is for understanding what those functions actually do, not replacing well-tested numerical implementations.
- Don't ignore lens distortion in the intrinsics — most cameras (especially wide-angle phone cameras) have noticeable distortion; skipping distortion correction produces overlay errors that get worse toward the edges of the frame.
