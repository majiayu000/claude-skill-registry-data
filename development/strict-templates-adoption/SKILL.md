---
id: angular.templates.strict-templates-adoption
name: Angular Strict Templates Adoption
description: >
  Guides progressive adoption of Angular strictTemplates so teams can enable template type checking without turning legacy codebases into upgrade-blocking refactor projects.
stack:
  - Angular
  - TypeScript
category: templates
status: stable
version: 0.10.0
owner: NgAutoPilot
triggers:
  - strictTemplates adoption
  - strict templates adoption
  - template type checking
  - angular template strictness
  - strict template rollout
compatibility:
  angular:
    min: "17"
    recommendedModern: "17+"
---

# Angular Strict Templates Adoption

## Purpose

Use this skill to adopt `strictTemplates` progressively in Angular codebases.

This skill is for teams that are not yet stabilized on strict template checking but want to move toward it safely.

The core rule is simple:

```txt
Adopt strictTemplates in bounded steps, not as a big-bang switch.
```

## When to Use

Use this skill when:

- `strictTemplates` is currently off
- the team wants to enable stronger template checking
- the repo has legacy templates
- diagnostics need to be introduced progressively

## Do

Use a staged rollout:

```txt
1. Enable strictTemplates in discovery mode
2. Observe diagnostics
3. Fix high-confidence issues
4. Keep lower-confidence diagnostics as warnings temporarily
5. Promote selected checks later
```

Start with a non-brittle policy:

```json
{
  "angularCompilerOptions": {
    "strictTemplates": true,
    "extendedDiagnostics": {
      "defaultCategory": "warning"
    }
  }
}
```

Track the baseline and convert it into a backlog.

## Do Not

Avoid flipping strictTemplates on and blocking the entire repo without a plan.

Avoid mixing strict template adoption with broad modernization in the same hop.

Avoid silencing all diagnostics to get a green build.

## Review Checklist

- [ ] Strict template adoption is phased.
- [ ] The baseline is recorded.
- [ ] Diagnostics are triaged.
- [ ] The rollout is bounded.

## Expected Output

1. Assess readiness for strictTemplates.
2. Recommend a staged rollout.
3. Record the baseline diagnostics.
4. Keep the adoption bounded.
5. Produce a safe adoption plan.
