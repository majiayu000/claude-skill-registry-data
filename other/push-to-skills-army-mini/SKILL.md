---
name: push-to-skills-army-mini
description: >-
  Publish the parent-managed Skills Army HQ package from landed XYZ Forge into the generated
  HiQS-Labs/XYZ-skills-army-mini child repository. Trigger on "publish Skills Army mini",
  "sync Skills Army mini", or "push Skills Army mini".
---

# Push to XYZ Skills Army mini

XYZ Forge is authoritative; the child is generated. Run from a clean landed `development` checkout
with a clean `main` checkout of `HiQS-Labs/XYZ-skills-army-mini` at the sibling path or at
`$XYZ_SKILLS_ARMY_MINI_REPO`.

1. Preview: `python3 utils/py/xyz_mini_sync.py --target skills-army-mini`.
2. Read the copy/delete plan. Refusals must be fixed at the source or destination; never hand-edit
   managed child files.
3. With operator authorization, publish and verify:
   `python3 utils/py/xyz_mini_sync.py --target skills-army-mini --push`.
4. Read back child `origin/main`, `MANIFEST.txt`, and `.xyz-forge-revision`; report the child SHA.

The publisher refuses dirty source/destination state, a destination branch other than `main`, and
unrelated ahead/behind/divergent history. It permits an unborn `main`, an exact origin/main checkout,
or one exact retained publisher commit so a failed push can be retried. It never force-pushes or
schedules itself. See `docs/SPIN-OFF-REPOSITORY-PLAYBOOK.md` for the reusable recipe.
