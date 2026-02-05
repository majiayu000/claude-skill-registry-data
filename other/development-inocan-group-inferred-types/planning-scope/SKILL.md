---
name: planning-scope
description: Mycelia-specific scope for planning document audits
---

# Mycelia Planning Document Scope

When auditing planning documents in Mycelia, use this specific scope.

## Planning Documents Location

Primary: `planning-docs/` (all files)

## Cross-Reference Scope

**Source Code:**
- `src/Mycelia.jl` - Main module
- `src/` - All source files

**Tests:**
- `test/runtests.jl` - Test entry point
- `test/` - All staged test directories

**Documentation:**
- `docs/src/` - Key documentation pages
- `README.md`

**CI/Infrastructure (context only):**
- `.github/workflows/ci.yml`
- `ci/hpc/README.md`

## Mycelia-Specific Priorities

When prioritizing actions, consider:

1. **Correctness** - Scientific validity, algorithm correctness
2. **Scalability** - HPC performance, large dataset handling
3. **Speed** - Assembly algorithm efficiency
4. **Onboarding** - Contributor setup, tutorials

## Known Planning Documents

Typical Mycelia planning docs include:
- Development triage and status
- Test templates and coverage plans
- Benchmark planning
- Release roadmaps
- API design documents

## Cross-Verification Checklist

When verifying planning claims:
- [ ] Do claimed modules exist in `src/`?
- [ ] Are claimed tests in the appropriate stage directory?
- [ ] Do documented APIs match function signatures?
- [ ] Are external tool requirements documented?
- [ ] Are benchmark claims backed by `benchmarking/` results?
