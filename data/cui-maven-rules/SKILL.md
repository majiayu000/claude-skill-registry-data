---
name: cui-maven-rules
description: Complete Maven standards covering build processes, POM maintenance, dependency management, and Maven integration for CUI projects
allowed-tools: Read, Grep
---

# CUI Maven Rules

Comprehensive Maven standards for CUI projects covering build verification, POM maintenance, dependency management, Maven wrapper updates, and integration with build tools.

## What This Skill Provides

### Maven Build Standards
- Pre-commit profile configuration and execution
- Build success criteria and verification
- Quality gate enforcement
- Execution time tracking and optimization
- Error and warning analysis
- OpenRewrite marker handling

### POM Maintenance Standards
- BOM (Bill of Materials) management
- Dependency management with properties
- Version naming conventions (version.*, maven.*.plugin.version)
- Scope optimization (compile, provided, runtime, test)
- OpenRewrite integration for automated cleanup
- Maven wrapper updates and maintenance

### Maven Integration Standards
- Frontend-maven-plugin configuration for JavaScript
- Node.js and npm version management
- Maven phase integration (validate, compile, test, etc.)
- SonarQube integration and coverage reporting
- CI/CD build environment standards

### Quality Standards
- Compilation error resolution
- Test failure handling
- Code warning fixes
- JavaDoc mandatory fixes
- Dependency analysis
- Acceptable warning management

## When to Activate This Skill

Activate this skill when:
- Building Maven projects with quality checks
- Analyzing Maven build output
- Fixing Maven build errors or warnings
- Maintaining POM files
- Managing dependencies or BOMs
- Updating Maven wrappers
- Integrating JavaScript tooling with Maven
- Setting up CI/CD Maven builds
- Troubleshooting Maven issues

## Workflow

### Step 1: Load Maven Standards

**CRITICAL**: Load Maven standards based on the task context.

1. **For POM maintenance tasks** (editing POM files, managing dependencies, updating BOMs):
   ```
   Read: standards/pom-maintenance.md
   ```

2. **For Maven integration tasks** (JavaScript/frontend integration, SonarQube setup):
   ```
   Read: standards/maven-integration.md
   ```

3. **For comprehensive Maven work** (build verification, complete project setup):
   ```
   Read: standards/pom-maintenance.md
   Read: standards/maven-integration.md
   ```

### Step 2: Apply Standards to Task

After loading the appropriate standards:

1. Extract key requirements relevant to your specific task
2. Follow the patterns and guidelines from the loaded standards
3. Apply quality gates and verification criteria as specified
4. Ensure all changes align with CUI Maven best practices

## Standards Organization

All standards are organized in the `standards/` directory:

- `pom-maintenance.md` - Comprehensive POM maintenance process, BOM management, dependency management, scope optimization
- `maven-integration.md` - Maven integration with JavaScript, frontend-maven-plugin, SonarQube integration

## Tool Access

This skill requires:
- **Read**: To load standards files
- **Grep**: To search for patterns in standards

## Usage Pattern

When this skill is activated, it loads all Maven-related standards into the agent's context. Agents can then reference these standards when:

1. **Executing builds**: Understanding build success criteria, quality gates
2. **Fixing issues**: Knowing how to handle errors, warnings, JavaDoc issues, OpenRewrite markers
3. **Maintaining POMs**: Following BOM patterns, property naming, dependency management rules
4. **Optimizing dependencies**: Applying scope rules, consolidation criteria
5. **Integrating tools**: Configuring frontend-maven-plugin, SonarQube properties
6. **Updating wrappers**: Following Maven wrapper update procedures

## Integration with Agents

### maven-project-builder Agent

The `maven-project-builder` agent activates this skill at workflow start (Step 0) to:
- Load build verification standards
- Understand quality gate criteria
- Know how to handle OpenRewrite markers
- Follow JavaDoc fix requirements
- Apply acceptable warning rules
- Track execution duration properly

The skill provides the authoritative standards that guide all build-related decisions and fixes.

## Standards Coverage

### Build Process
- ✅ Pre-commit profile execution
- ✅ Build success criteria (exit code, BUILD SUCCESS text, no ERROR lines)
- ✅ Timeout calculation (duration * 1.25 safety margin)
- ✅ Output analysis patterns
- ✅ Iteration workflow

### Issue Handling
- ✅ Compilation error fixes
- ✅ Test failure resolution
- ✅ Code warning handling
- ✅ JavaDoc mandatory fixes (NEVER optional)
- ✅ OpenRewrite marker auto-suppression (LogRecord, Exception)
- ✅ Acceptable warning management

### POM Maintenance
- ✅ BOM implementation patterns
- ✅ Property naming conventions
- ✅ Dependency aggregation rules
- ✅ Scope optimization guidelines
- ✅ Version management (handled by Dependabot)
- ✅ OpenRewrite recipe execution

### Maven Integration
- ✅ Frontend-maven-plugin configuration
- ✅ Node.js version management (v20.12.2)
- ✅ Maven phase mapping
- ✅ SonarQube properties
- ✅ CI/CD integration

## Related Skills

- **cui-javadoc**: JavaDoc standards used for mandatory JavaDoc fixes
- **cui-java-unit-testing**: Testing standards referenced in build verification
- **cui-frontend-development**: JavaScript standards for Maven integration

## Maintenance Notes

Standards in this skill are authoritative for:
- All Maven build processes in CUI projects
- All POM maintenance activities
- All Maven-related quality checks
- All Maven integration configurations

When standards need updates, modify the files in the `standards/` directory and the skill will automatically reflect the changes when next activated.

## Version

Version: 0.1.0 (Initial release)

Part of: cui-maven bundle

---

*This skill consolidates Maven standards from multiple sources into a single, comprehensive knowledge base for CUI Maven workflows.*
