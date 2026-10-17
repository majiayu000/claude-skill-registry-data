---
name: definition-of-done
description: "Evaluate implementation, test, review, release and deployment evidence before completion claims; distinguish a reviewable change from a verified deployment."
---
# Definition of done

Bind every completion claim to its requested scope and exact candidate revision. Creating a PR, merging a PR, releasing an artifact and verifying deployment are separate outcomes.

1. **Scope:** Map every acceptance criterion to observed behavior. Mark unimplemented, blocked or unverified work explicitly. No stub or unwired configuration may satisfy a behavior requirement.
2. **Tests:** Run the full applicable required suite after the last relevant edit. Record commands, environment, collected counts and results. No unexplained skip, hidden failure, or zero-test success. Select checks according to risk and the repository's policy.
3. **CI:** If enabled, inspect current candidate checks. Pending, unavailable, cancelled and failed checks are not green. Local results do not override a required CI gate. If no CI applies, document the applicable local verification and its limits.
4. **Security and failure:** Validate trust boundaries, secret handling, authorization, errors and recovery for changed behavior. A checklist is not a security guarantee.
5. **Review:** Satisfy the repository's required independent reviews on the actual candidate. Authors cannot count self-review as independent approval.
6. **Distribution:** Inspect the consumed package, skill directory or hook configuration. Resolve every bundled dependency. Verify installation and an actual event/consumer path where that is the requested deliverable.
7. **Deployment, when requested:** Bind the immutable artifact and configuration to each intended consumer. Check running revision and user-facing behavior. Source merge alone is not deployment evidence. Do not deploy without existing authorization.
8. **Operations:** Check idempotence, observable failure, persistence and rollback where applicable. Elapsed quiet time alone is inconclusive; use deterministic tests as well as meaningful runtime observations.
9. **Documentation:** Keep installation, migration, limitations and ownership accurate. Link the issue, PR and verification evidence.

Report `IMPLEMENTED`, `REVIEW_PENDING`, `CI_PENDING`, `RELEASED`, `DEPLOYED`, `VERIFIED`, `PARTIAL` or `BLOCKED` only when evidence supports that scope. Mark genuinely inapplicable items N/A with a reason. Continue useful authorized work while a separate gate is unavailable.
