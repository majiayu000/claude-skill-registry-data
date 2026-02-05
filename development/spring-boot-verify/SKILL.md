---
name: spring-boot-verify
description: Verify Spring Boot 4.x projects for correct dependencies, configuration, and migration readiness. Use when analyzing pom.xml, build.gradle, application.yml, discussing Spring Boot project setup, dependency versions, configuration validation, version compatibility, migration to Spring Boot 4, deprecated dependencies, or when user mentions "verify project", "check dependencies", "upgrade Spring Boot", "migration readiness", "Jackson 3", "@MockBean deprecated", or "Spring Security 7".
---

# Spring Boot 4.x Project Verification

Analyzes Spring Boot projects for dependency compatibility, configuration correctness, and migration readiness.

## Verification Workflow

1. **Detect Build System** → Find pom.xml or build.gradle, extract Spring Boot version
2. **Analyze Dependencies** → Check versions, find deprecated libraries, validate compatibility
3. **Validate Configuration** → Check application.yml/properties, security config, actuator settings
4. **Generate Report** → Structured markdown with severity levels and remediation code
5. **Lookup Docs** → Use Exa MCP to fetch latest Spring Boot 4.x documentation when needed

## Dependency Quick Reference

| Check | Severity | Action |
|-------|----------|--------|
| Spring Boot version < 4.0 | CRITICAL | Upgrade to 4.0.x |
| Jackson 2.x (`com.fasterxml`) | CRITICAL | Migrate to Jackson 3 (`tools.jackson`) |
| `@MockBean` in tests | ERROR | Replace with `@MockitoBean` |
| Undertow server | ERROR | Switch to Tomcat or Jetty |
| Java version < 17 | ERROR | Minimum Java 17 required |
| `spring-boot-starter-web` | WARNING | Use `spring-boot-starter-webmvc` |

## Configuration Quick Reference

| Check | Severity | Action |
|-------|----------|--------|
| Security `and()` chaining | CRITICAL | Convert to Lambda DSL closures |
| `antMatchers()` usage | ERROR | Replace with `requestMatchers()` |
| `authorizeRequests()` | ERROR | Replace with `authorizeHttpRequests()` |
| All actuator endpoints exposed | WARNING | Limit to health, info, metrics |
| 100% trace sampling | WARNING | Use 10% in production |

## Tools to Use

1. **Glob** → Find `**/pom.xml`, `**/build.gradle*`, `**/application.{yml,properties}`
2. **Grep** → Search for deprecated patterns (`@MockBean`, `com.fasterxml`, `.and()`)
3. **Read** → Inspect build files and configuration
4. **Exa MCP** → Fetch latest Spring Boot 4.x docs: `mcp__exa__web_search_exa`

## Output Format

Generate verification reports with this structure:

```markdown
## Spring Boot 4.x Verification Report

### Summary
- **Project**: {name}
- **Boot Version**: {detected version}
- **Issues Found**: {n} Critical, {n} Errors, {n} Warnings

### Critical Issues / Errors / Warnings
[Issue details with code remediation]
```

## Detailed References

- **Migration Guide**: See [MIGRATION_GUIDE.md](MIGRATION_GUIDE.md) for step-by-step migration from Boot 3.x to 4.0
- **Examples**: See [EXAMPLES.md](EXAMPLES.md) for sample verification outputs
- **Troubleshooting**: See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for detection issues
- **Dependencies**: See [references/dependencies.md](references/dependencies.md) for complete version matrix
- **Configuration**: See [references/configuration.md](references/configuration.md) for validation rules

## Critical Reminders

1. **Check Spring Boot version first** — Many issues are version-specific
2. **Jackson 3 namespace change** — `com.fasterxml.jackson` to `tools.jackson`
3. **Security 7 Lambda DSL** — `and()` method removed, closures required
4. **Testing annotations changed** — `@MockBean` to `@MockitoBean`
5. **Use official docs** — https://docs.spring.io/spring-boot/documentation.html

## Related Skills

- `spring-boot-security` — Deep security configuration verification
- `spring-boot-testing` — Testing patterns and coverage analysis
- `spring-boot-observability` — Actuator, metrics, and tracing setup
- `spring-boot-modulith` — Module structure verification
- `domain-driven-design` — DDD architecture patterns
