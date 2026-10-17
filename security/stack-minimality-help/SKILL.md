---
name: stack-minimality-help
description: Provide a quick reference for stack-minimality skills and scope without changing repository behavior.
license: MIT
---
# Stack Minimality Help

## Purpose
Provide a one-shot reference to the stack-minimality pack and its relationship to domain skills.

## Activate when
Use for minimality help, skill selection, pack usage, or a request for simplification commands.

## Repository inspection
No scan is required unless the user asks for a repository-specific example.

## Decision rules
Select the narrowest skill:
- stack-minimality: implementation discipline;
- stack-minimality-review: focused diff over-engineering review;
- stack-minimality-audit: whole-repository simplification audit;
- stack-minimality-debt: deliberate shortcut ledger;
- stack-minimality-evidence: observable measurement;
- stack-minimality-help: this reference.

The domain skill still owns the engineering contract. Minimality never overrides explicit requirements or required guarantees.

## Implementation procedure
Pair stack-minimality with the skill that owns the actual problem, such as Rails persistence, Rails jobs, React state, TypeScript runtime contracts, PostgreSQL schema engineering, security, or API design.

## Anti-patterns / failure modes
- Treating minimality as a replacement for correctness or security review.
- Optimizing for character count instead of smallest safe implementation.
- Publishing unmeasured benchmark results.
- Using review or audit skills to modify the repository.

## Reference example

```text
$ bin/stack-minimality help
Usage: bin/stack-minimality <command> [repository]

Commands:
  help       Show this reference.
  debt       List stack-minimality: shortcut markers.
  evidence   Report observable Git diff size for a repository.
```

Typical selection: implementing a change → `stack-minimality` with the owning domain skill; reviewing a diff for over-engineering → `stack-minimality-review`; listing deliberate shortcuts → `stack-minimality-debt` (`bin/stack-minimality debt`); measuring a simplification → `stack-minimality-evidence` (`bin/stack-minimality evidence`).

## Agent review checklist
- [ ] Correct minimality skill selected.
- [ ] Domain skill remains responsible for the contract.
- [ ] Non-negotiable guarantees preserved.
- [ ] Report-only skills did not modify source.

## Verification
Confirm that the requested skill operated at the correct scope and that report-only activity left files unchanged.

## Source foundation
- https://ponytail.dev/
- https://github.com/DietrichGebert/ponytail
- Repository routing and skill-pack conventions
