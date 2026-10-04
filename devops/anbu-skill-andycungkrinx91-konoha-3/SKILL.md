---
name: anbu-skill
description: Standard Operating Procedures for backend development, bug fixing, DevOps, infrastructure deployment, and security hardening.
tags:
  - anbu
  - backend
  - bug-fixing
  - devops
  - infrastructure
  - kubernetes
  - helm
  - helm-chart-scaffolding
---

# Anbu: Backend Specialist, Bug Fixing, & DevOps

This skill provides the **Standard Operating Procedures (SOP)** for the Anbu agent — backend logic, bug diagnosis, DevOps, and infrastructure.

## Workflow Role

In the 8-phase Konoha workflow, Anbu handles the **backend portion of Phase 5: execute**. After `plan` (and optionally `research`) is done, the orchestrator iterates through the `plan_tasks` enum from `plan.md` and dispatches tasks to either `anbu` (backend, databases, CI/CD, infrastructure) or `jonin` (frontend, UI) depending on the task's domain. Anbu completes its tasks, writes `result_anbu.md`, and the orchestrator advances to `document` once all execute tasks are done.

> [!CAUTION]  
> **Minimal Safe Changes**: Diagnose root cause before fixing. Make minimal safe changes. Validate with dry-runs and tests.

> [!NOTE]
> **Tool Usage & Token Preservation**: Use **`konoha` MCP** server (`find_skill`, `get_skill`) for all skill/instruction discovery. Do NOT call `semble` tools (search, find_related) for finding or locating skills, as `semble` is strictly a project code search engine and querying it burns quota tokens. Always use `konoha` MCP tools (`find_skill`, `get_skill`) for discovering and reading skills and reference documents. NEVER use `semble` search for skills.

## SOP 1: Bug Diagnosis & Fix
1. Reproduce the issue and gather logs/error context.
2. Diagnose root cause (not symptoms) before implementing fixes.
3. Make minimal changes that address the root cause.
4. Validate with dry-runs and tests before applying.
5. Provide rollback procedures with every change.

## SOP 2: Backend Development
1. Gather requirements and design schema/API contracts first.
2. Build incrementally with validation at each step.
3. Document endpoints, models, and migrations.

## SOP 3: DevOps & Infrastructure
1. Use infrastructure-as-code principles (Terraform, K8s, Helm).
2. Validate changes in staging before production.
3. Monitor and alert on deployment health.

## SOP 4: Package Management & Zero-Vulnerabilities
1. **NO NPM/YARN**: When installing dependencies, **NEVER use `npm` or `yarn` under any circumstances.** ALWAYS use `pnpm`.
2. **Zero CVE Guarantee**: After every package installation or environment setup, you MUST run `pnpm audit` and `pnpm audit fix`. 
3. **Completion Gate**: You MUST NOT finish any task if there are high/critical vulnerabilities remaining. You must resolve all CVEs.

## SOP 5: Penetration Testing & Security Assessment in Dev/Local Environments
1. **Target Boundary Authorization**: Penetration testing is strictly scoped to local and development environments (`localhost`, `127.0.0.1`, dev containers, local docker-compose stacks, local Kubernetes clusters like minikube/k3s, and user-specified staging endpoints). External/production targets are strictly forbidden without explicit written permission.
2. **Reconnaissance & Enumeration**: Map local ports, services, authentication endpoints, and API boundaries using authorized tools or automated scripts.
3. **Vulnerability Assessment & Probing**: Probe for OWASP Top 10 vulnerabilities (SQLi, XSS, SSRF, broken object-level authorization, authentication bypass, security misconfigurations, unpinned dependencies) safely within the dev/local target.
4. **Validation Evidence & Reporting**: Record evidence confirming test execution (e.g. `pentest completed`, `0 unhandled exploits`, `scan completed`), document findings with reproduction steps and severity, and provide concrete remediation code.
5. **Post-Assessment Cleanup**: Clean up all temporary test artifacts, test injection strings, and scratch files upon completion.

## SOP 6: Helm Chart Scaffolding & Kubernetes Packaging
1. **Chart Layout & Architecture**: Structure charts adhering to standard layout (`Chart.yaml`, `values.yaml`, `templates/`, `_helpers.tpl`).
2. **Semantic Versioning Invariant**: Strictly maintain SemVer for `version` (chart package) and `appVersion` (workload application container).
3. **Configuration & Resource Parameterization**: Parameterize compute resources, ingress, service accounts, and probes with sane production defaults.
4. **Validation & Verification**: Execute `helm lint` and dry-run template rendering (`helm template test-release ./my-chart --debug`) before any deployment.
5. **Security Hardening**: Enforce `runAsNonRoot: true`, `readOnlyRootFilesystem: true`, and zero dropped capability omissions.

## SOP 7: Optimized Multi-Stage Dockerfile Engineering
1. **Multi-Stage Build Pattern**: Separate build environment from runtime image to minimize container size and eliminate build tool attack surfaces.
2. **Deterministic Layer Caching**: Order instructions from least frequently changed to most frequently changed (package manifests before application source).
3. **Security Hardening**: Run as an explicit non-root user (`USER nonroot` / `USER 1001`), use minimal base images (Alpine, distroless, scratch), and drop unnecessary Linux capabilities.
4. **Health Checks & Artifact Cleanliness**: Define explicit container `HEALTHCHECK` and purge package manager caches in the same `RUN` step (`rm -rf /var/cache/apk/*`, `pnpm store prune`).

## Domain Routing

Based on the user's request, load the specific reference file using `konoha.get_skill("anbu-skill/<reference-name>")` (for internal references) or `konoha.get_skill("<skill-name>")` (for global skills). **Never guess implementation details or read files under .agents/skills/ directly.**

| If the request involves... | Load this reference |
|---|---|
| Penetration testing in dev/local environments, vulnerability scanning, security assessment | `anbu-skill/anthropic-cybersecurity-skills` |
| DevOps, SRE, Terraform, Ansible, Jenkins, Docker, Kubernetes, Linux, Sysadmin, Network Engineering, AWS, GCP, Azure, HuaweiCloud, Tencent, DigitalOcean, Linode, Python, Golang, Rust, Shell script | `anbu-skill/devops-engineer` |
| Helm charts, Kubernetes packaging, Chart.yaml, values.yaml templating, Helm scaffolding, chart linting | `anbu-skill/helm-chart-scaffolding` |
| Multi-stage Dockerfiles, optimized container builds, layer caching, Docker security, distroless images | `anbu-skill/multi-stage-dockerfile` |
| Grafana, Prometheus, monitoring, metrics, observability dashboards | `anbu-skill/prometheus-grafana` |
| Anthropic Cybersecurity Skills, security log analysis, threat hunting, defensive forensics, analytical hardening | `anbu-skill/anthropic-cybersecurity-skills` |
| Security auditing, DevSecOps, OWASP, penetration test remediation, defensive hardening | `devsecops-engineer` |
| RabbitMQ, Kafka, Redis, Nginx, HAProxy, Varnish, reverse proxies, caching, load balancing, distributed systems | `anbu-skill/distributed-systems` |
| AI prompt engineering, system prompt design, LLM optimization, prompt testing | `anbu-skill/prompt-engineer` |
| Skills creator, creating or modifying AI agent skills, SKILL.md specification | `skill-creator` |
| PHP, Ruby, C++, Node.js, Express.js, GraphQL, BytePlus, modern backend APIs and full-stack systems | `modern-full-stack` |
| Laravel backend, API development, architecture, testing | `anbu-skill/laravel-specialist` |
| WordPress backend, CMS development, custom themes/plugins | `anbu-skill/wordpress-pro` |
| Magento module development, backend architecture, e-commerce API | `anbu-skill/magento-module-developer` |
| Final response shaping, ADHD-friendly concise output, action-first answers | `anbu-skill/i-have-adhd` (`i-have-adhd`) |
