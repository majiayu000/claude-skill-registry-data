---
name: fundamental-coding-principles
description: Apply SOLID, DRY, KISS, YAGNI, and SSOT principles when writing, reviewing, or refactoring code to ensure maintainability and quality.
---

# Fundamental Coding Principles

Apply this skill to keep code changes focused, testable, and maintainable.

## Quick Checklist
- Confirm each edit has a single purpose before coding.
- Ruthlessly remove duplication or dead paths you touch.
- Only add behavior backed by an explicit requirement.
- Prefer simple, composable solutions over clever ones.
- Keep truthy data and decisions in one authoritative place.

## Principle Guardrails

### SOLID
- `S`: Validate the change impacts one reason to vary; split helpers if mixed concerns appear.
- `O`: Extend behavior through new types or functions rather than rewriting stable code paths.
- `L`: Ensure new subtype logic preserves caller expectations (inputs, return contracts, exceptions).
- `I`: Create targeted interfaces; avoid forcing consumers to implement unused members.
- `D`: Depend on abstractions or injected collaborators; eliminate hardwired globals where possible.

### DRY
- Scan for repeated logic, constants, or schemas; consolidate into shared utilities before finishing.
- Prefer extracting reusable modules over copy-pasting even inside the same file.

### KISS
- Trim optional branches, flags, and polymorphism unless they solve today’s requirement.
- Keep functions short and state minimal; decompose complex flows into readable steps.

### YAGNI
- Challenge every new feature, parameter, or hook: is there a verified need right now?
- Defer premature abstractions until duplication or clear requirements emerge.

### SSOT
- Update or create the canonical definition (config, schema, doc) when data models change.
- Remove divergent caches or mirrors unless you enforce sync in the same change.

## Reference Playbooks
- [Splunk: "SOLID Design Principles – Hands-On Examples"](https://www.splunk.com/en_us/blog/learn/solid-design-principle.html) – success/failure code walkthroughs for each letter.
- [PullRequest.com: "7 Clean Coding Principles"](https://www.pullrequest.com/blog/7-clean-coding-principles/) – DRY-focused review prompts.
- [MIT 6.031: Code Review Guide](https://web.mit.edu/6.031/www/fa20/classes/03-code-review/) – DRY and simplification questions to ask.
- [Baeldung: KISS Software Design Principle](https://www.baeldung.com/cs/kiss-software-design-principle) – tactics for keeping solutions lightweight.
- [TechTarget: YAGNI Explainer](https://www.techtarget.com/whatis/definition/You-arent-gonna-need-it) – decision tests and risk scenarios.
- [Atlassian Workstream: Building an SSOT](https://www.atlassian.com/work-management/knowledge-sharing/documentation/building-a-single-source-of-truth-ssot-for-your-team) – practices for maintaining canonical sources.
