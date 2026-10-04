---
name: ik-solver-select
description: Use when the arm must reach a Cartesian pose — choose differential (Jacobian) IK for smooth servoing/teleop vs analytic/global IK for reaching a pose from scratch, and handle singularities and joint limits explicitly.
stacks: [python]
domains: [hardware]
phases: [dev]
tags: [kinematics, inverse-kinematics, pinocchio, pink, moveit, jacobian, singularity]
scope: kit
---
**When to use.** End-effector pose control. *Why:* the wrong IK class gives jerky motion or no
solution; differential vs global is the key fork, and singularity handling is non-optional.

**Procedure.**
1. Classify: continuous tracking/teleop → differential IK (Pink/Mink, per-tick QP); reach-a-pose → analytic/global (MoveIt/IKFast).
2. For differential IK, use damped least squares near singularities and cap joint velocities.
3. Respect joint limits as constraints, not afterthoughts.
4. **Done when:** the EE reaches targets within tolerance without limit violations or singularity blow-ups (test trajectory logged).

**Knowledge:** KNOWLEDGE-LIBRARY.md §B2. **Example:** the Pink differential-IK snippet there.
