---
name: tech-stack
description: Describes the primary technologies, frameworks, libraries, and language conventions used in this codebase.
---

# Tech Stack Overview

## Primary Languages
- Backend: [e.g., TypeScript / Node.js]
- Frontend: [e.g., React / TypeScript]
- Infrastructure: [e.g., Terraform / YAML]
- Other: [e.g., Python for data tasks]

## Frameworks & Libraries
- Backend framework(s): [e.g., NestJS, Express]
- Frontend framework(s): [e.g., Next.js, Redux, React Query]
- Database: [e.g., PostgreSQL + Prisma, MongoDB]
- Messaging / queues: [e.g., Kafka, RabbitMQ]
- Observability: [e.g., OpenTelemetry, Prometheus, Grafana]

## Language Conventions

### General
- Prefer [functional / OO / mixed] style for [language].
- Follow [link to style guide] for formatting and structure when possible.

### Naming
- Types / classes: [e.g., PascalCase]
- Functions: [e.g., camelCase verbs]
- Constants: [e.g., UPPER_SNAKE_CASE]
- Files: [e.g., kebab-case.ts, PascalCase.tsx]

### Error Handling
- Use [custom error types / Result types / exceptions] with:
  - Consistent error codes
  - User- vs system-facing messages

### Dependency Management
- Use [npm / yarn / pnpm / pip / etc.] with:
  - Lockfiles committed
  - Reproducible installs in CI

## Project-Specific Notes
- [Any special constraints, e.g., "no experimental language features" or "avoid reflection."]
