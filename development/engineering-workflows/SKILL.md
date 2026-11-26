---
name: engineering-workflows
description: Implement, debug, review, and release software using Kernel’s engineering procedures. Covers API, authentication, databases, React, native apps, builds, tests, and repository maintenance.
license: MIT
---

# Engineering Workflows

Select the procedure matching the user's task from the index below. Read only that procedure and any resources it explicitly needs. Resource paths in a procedure are relative to that procedure's folder; run bundled scripts from that folder when its commands assume a working directory.

Follow the user's current instructions and the target repository's conventions before Kernel defaults. Treat examples, framework choices, and project adapters as conditional guidance. Match validation to the actual change. Existing authorization persists; ask only when a required decision or permission is missing. Loading a procedure does not authorize publishing, deployment, or other external changes.

- [API routes and validation](references/kernel-dev-api/WORKFLOW.md): adding or changing an HTTP route, handler or request schema
- [Better Auth integration](references/kernel-dev-auth/WORKFLOW.md): sign-in, sessions or migration in a Better Auth project
- [Build and CI failures](references/kernel-dev-build/WORKFLOW.md): typecheck, lint, build or CI is red
- [Production database changes](references/kernel-dev-database/WORKFLOW.md): schema migrations, expand/contract, live data operations
- [Docker and Compose](references/kernel-dev-docker/WORKFLOW.md): writing or fixing Dockerfiles and Compose services
- [React components and state](references/kernel-dev-react/WORKFLOW.md): web React components, state ownership, data fetching
- [React Native boundaries and performance](references/kernel-dev-react-native/WORKFLOW.md): Expo/RN screens, native deps, mobile performance
- [Test design and flaky tests](references/kernel-dev-testing/WORKFLOW.md): choosing a test layer, mocks, coverage floors, flaky tests
- [TypeScript contracts and types](references/kernel-dev-typescript/WORKFLOW.md): type ownership, strictness, schema/type drift
- [Branches and commit messages](references/kernel-git-commit/WORKFLOW.md): staging and writing a commit under the repo's rules
- [Code health cleanup](references/kernel-clean-code/WORKFLOW.md): deslop, code smells, or a tech-debt audit
- [Monorepo architecture audit](references/kernel-audit-monorepo/WORKFLOW.md): auditing or refactoring monorepo package boundaries
- [Review completed work](references/kernel-audit-review/WORKFLOW.md): reviewing a finished task, PR or directory before sign-off
- [Trace a feature across boundaries](references/kernel-audit-trace/WORKFLOW.md): following one feature end to end through layers
- [Deep repo code scan](references/deep-repo-code-scan/WORKFLOW.md): read-only deletion and consolidation inventory
- [Dependabot batch updates](references/dependabot-batch/WORKFLOW.md): folding all pending Dependabot updates into one PR
- [PR comment triage](references/pr-comments/WORKFLOW.md): working through review comments on a PR
- [React Doctor](references/react-doctor/WORKFLOW.md): React health score, regression check, rule tuning
- [Configure project quality checks](references/project-quality-gates/WORKFLOW.md): setting up lint, coverage, security and CI gates
- [Deployment readiness and execution](references/kernel-ops-ship/WORKFLOW.md): preflight, deploy, verify and roll back a release
- [Agent knowledge loops](references/agent-knowledge-loops/WORKFLOW.md): turning agent task evidence into checked repo rules
- [LLM-based structured data extraction](references/llm-structured-extraction/WORKFLOW.md): designing LLM extraction of memories, entities and relationships into a validated store

For root-cause debugging, use systematic-debugging. For test-first implementation, use test-driven-development. For iOS releases and TestFlight, use ship-ios. For the engineering laws behind Charles's code, use ponti-principles; they take precedence over defaults here.

For Apple platform apps — iOS, macOS, watchOS, Swift and SwiftUI — use apple-workflows. For security audits, use security-workflows. For interface design and motion, use design-workflows. Writing and revising documents, scripts and interface copy uses writing-workflows.
