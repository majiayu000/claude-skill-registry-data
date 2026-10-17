---
name: aiwf-field-pilot-readiness
description: Use for robotics, embedded AI, automation, or customer-site pilots that need safety gates, site constraints, operator handoff, rollback, data handling, and success criteria.
---

# AIWF Field Pilot Readiness

## Core Rule

Do not treat a demo, outdoor test, or customer-site automation as ready until the pilot has a job, site constraints, safety boundary, operator handoff, rollback plan, data plan, success criteria, and stop conditions.

## Workflow

1. Define the pilot job: task, location, users, operator, bystanders, equipment, environment, and expected duration.
2. Inventory hazards and constraints: motion, pinch/crush zones, electrical, network loss, weather, terrain, lighting, privacy, data handling, and human override.
3. Set gates: preflight, go/no-go, live monitoring, emergency stop, rollback, incident logging, and post-run review.
4. Define success metrics: task completion, latency, autonomy level, intervention count, reliability, operator workload, safety events, and customer-visible value.
5. Require a written pilot brief before field work or partner review.

## Guardrails

- Do not infer safety compliance from general robotics confidence. Use official safety, risk, and test-method references as guidance and identify where professional review is needed.
- Keep first pilots narrow. One site, one job, one fallback, one review path.
- Do not collect customer or bystander data without an explicit data-handling plan.
- Add `aiwf-robotics-systems` for robot architecture, control, ROS, sensors, or logs.
- Add `aiwf-networking-iot` for site connectivity, telemetry, or remote support.
- Add `aiwf-service-intake` when a pilot request arrives as a website lead and still needs business scoping.

## Output Shape

For a pilot plan, return:

- pilot job and site assumptions
- required preflight checks
- hazards and mitigations
- operator handoff and stop plan
- data/logging plan
- success metrics and stop conditions
- open approvals or missing evidence

## Primary Source Anchors

- NIST AI Risk Management Framework: https://www.nist.gov/itl/ai-risk-management-framework
- OSHA robotics overview: https://www.osha.gov/robotics
- NIST mobile robotics test-method work: https://www.nist.gov/el/intelligent-systems-division-73500/mobile-robotics-systems-research-and-standard-test-methods

Use these as planning and risk anchors, not as a substitute for legal, safety, or compliance review.
