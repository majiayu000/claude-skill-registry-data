---
name: star-tracker
description: "Use when the task is star identification, boresight and field of view selection, lost in space versus tracking mode, cross-boresight versus roll pointing accuracy, or star tracker update rate. Determine star tracker attitude determination for spacecraft ADCS: identify measured star centroids against an onboard star catalog, compute the angular separation between each measured centroid and its catalog star, and return the best match inside the field of view. The logic normalizes unit vectors, finds the nearest catalog star within the field of view radius, returns the matched star id plus boresight error in arcseconds, and selects lost in space or tracking mode from a prior attitude. Trigger: star identification, star catalog, boresight, field of view, lost in space, tracking mode, angular separation, pointing accuracy, attitude determination."
license: Apache-2.0
compliance: STANDARDS-REF
standards:
  - id: ecss
    reference-only: true
gated: false
domain: space-systems
pack: space-systems
compatibility: "agentskills.io SKILL.md; any SKILL.md host (Claude Code, Hermes, OpenClaw)"
metadata:
  domain: space-systems
  subdomain: adcs
  tags: [adcs, star-tracker, star-identification, star-catalog, boresight, attitude-determination, lost-in-space, field-of-view]
  version: 0.1.0
  author: Aero Agent Skills
---

# Star Tracker Attitude Determination (space-systems/adcs/star-tracker)

Use when the task is star tracker attitude determination: matching
measured star centroids to a star catalog, computing the angular
separation between a measured centroid and its catalog star, choosing
the boresight and field of view, or deciding between lost in space and
tracking mode.

## Domain quick reference

- A star tracker is the ADCS attitude reference with the highest
  pointing accuracy: it images stars, measures their centroid
  positions on the focal plane, and matches the pattern against an
  onboard star catalog to recover the instrument attitude.
- Star identification is the matching step: each measured centroid is
  compared against catalog stars by angular separation
  theta = acos(dot(u_meas, u_cat)) between unit vectors, and the best
  match inside the field of view is accepted.
- The boresight is the tracker optical axis, the center of the field
  of view. The field of view (FOV) is the angular window the sensor
  sees; a square FOV of half-angle fov/2 accepts catalog stars within
  that radius of the boresight.
- Lost in space mode identifies stars with no prior attitude by
  searching the full star catalog; tracking mode uses the prior
  attitude to predict which catalog stars should appear and matches
  within a small tracking radius.
- Pointing accuracy is anisotropic: cross-boresight error is set by
  centroid noise relative to focal length, while roll error about the
  boresight is larger because star positions on the focal plane barely
  change under roll.
- Update rate: a star tracker produces attitude at rates from a few
  Hz to tens of Hz; the ADCS uses the matched-star angular separation
  as the pointing error bound between updates.

## Workflow

1. Normalize the catalog star unit vectors and the measured centroid
   unit vector.
2. Compute the angular separation between each measured centroid and
   every candidate catalog star: acos of the dot product, clamped to
   [-1, 1] before the acos call.
3. Accept the nearest catalog star when its separation is within the
   FOV half-angle; return the matched star id and the separation as
   the boresight error.
4. Select the mode: tracking when a prior attitude exists and the
   nearest match is within the tracking radius, otherwise lost in
   space against the full catalog.
5. Report the boresight error in arcseconds and compare the achieved
   pointing accuracy against the requirement.

## Pitfalls

- Comparing unnormalized vectors: the dot product must use unit
  vectors or the acos separation is meaningless.
- Letting floating point round-off push the dot product outside
  [-1, 1], which makes acos return nan; clamp first.
- Accepting a match outside the FOV: the nearest catalog star is not
  a valid identification when its separation exceeds the FOV
  half-angle.
- Choosing lost in space when a valid prior attitude exists: tracking
  mode is cheaper and more robust.
- Reporting roll accuracy as if it equaled cross-boresight accuracy.
- Confusing the field of view (angular window, half-angle fov/2) with
  the boresight (its center direction).

## Behavior contract (gate 3)

The star identification, boresight, and mode logic is exercised by the
gate 3 contract test: scripts/test_star_tracker.py against
scripts/star_tracker_logic.py (stdlib unittest, offline). Run:
python3 scripts/test_star_tracker.py

## Compliance

- ECSS (European Cooperation for Space Standardization) standards are
  freely downloadable, copyright ESA; cite the source and paraphrase.
  This leaf cites ECSS as reference only per standards-map.yaml; the
  logic here is generic star tracker geometry, not ECSS text.
- compliance: STANDARDS-REF, gated: false.
