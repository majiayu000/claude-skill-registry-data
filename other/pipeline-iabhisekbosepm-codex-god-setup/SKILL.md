---
name: pipeline
description: "Run the full feature development pipeline: explore → architect → plan → build → review → security → test → docs."
argument-hint: "[feature-description]"
allowed-tools: Read Write Edit Bash Grep Glob
model: gpt-5.4
---

# /pipeline — Full Feature Pipeline

Build: **$ARGUMENTS**

1. **Understand** — `agents/code-explorer.md`: trace related code, map architecture, identify patterns
2. **Design** — `agents/architect.md`: trade-offs, component structure, architecture decisions
3. **Plan** — `agents/planner.md`: phased steps, dependencies, risks, success criteria
4. **Build** — Implement the plan following existing patterns. Handle all states.
5. **Fix build** — `agents/build-error-resolver.md`: fix type/build errors, minimal diffs
6. **Review** — `agents/code-reviewer.md` + language-specific reviewer
7. **Security** — `agents/security-reviewer.md`: OWASP, secrets, input validation
8. **Test** — `agents/e2e-runner.md`: E2E tests for critical paths
9. **Document** — `agents/doc-updater.md`: update codemaps and README
