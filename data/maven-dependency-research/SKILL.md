---
name: maven-dependency-research
description: Research Maven dependency updates with breaking changes, release notes, and security information
tags: [maven, dependencies, research, security, breaking-changes]
triggers: [maven dependency update, dependency research, version upgrade]
tools: [bash, curl, grep, jq, web_search]
prerequisites:
  - curl command available
  - jq for JSON parsing
  - Internet access for Maven Central and GitHub APIs
version: 1.0.0
---

# Maven Dependency Research Skill

A comprehensive skill for researching Maven dependency updates, identifying breaking changes, security vulnerabilities, and migration requirements.

## Overview

This skill automates the research process for Maven dependency updates by:
1. Discovering all versions between current and available versions
2. Finding and verifying release notes and changelogs
3. Extracting breaking changes, security issues, and major features
4. Providing structured reports for decision-making

## When to Use This Skill

Use this skill when:
- Updating Maven dependencies in `pom.xml`
- Investigating available dependency updates
- Assessing migration complexity for dependency upgrades
- Reviewing security implications of dependency changes
- Planning dependency update strategies

## Five-Phase Workflow

### Phase 1: Identification

Identify the defining attributes of the dependency group:
- **GroupId**: The common group identifier (e.g., `org.springframework.boot`)
- **ArtifactIds**: List of artifacts in the group
- **Current Version**: Version currently in use
- **Available Version**: Target version to upgrade to

**Example:**
```bash
# Extract from pom.xml
grep -A 3 "<groupId>org.apache.commons</groupId>" pom.xml
```

### Phase 2: Version Scope Definition

Identify all versions between current and available versions.

**Script:** `scripts/fetch-maven-versions.sh`

**Usage:**
```bash
./scripts/fetch-maven-versions.sh org.apache.commons commons-lang3 3.12.0 3.14.0
```

**Output:** List of applicable versions (excluding pre-release versions)

**Strategy:**
- ≤5 versions: Research each version individually
- >5 versions: Aggregate findings with note "N versions behind"

### Phase 3: Release Notes Discovery & Verification

Find and verify documentation for each applicable version.

**Scripts:**
- `scripts/extract-project-urls.sh` - Extract project URLs from Maven POM
- `scripts/query-github-releases.sh` - Query GitHub releases API
- `scripts/verify-url.sh` - Verify URL returns relevant content

**Discovery Priority:**
1. Check previous reports in current directory
2. Query Maven Central POM for project URLs
3. Use GitHub Releases API (if GitHub project)
4. Web search as last resort

**Example:**
```bash
# Extract project URLs
./scripts/extract-project-urls.sh org.apache.commons commons-lang3 3.14.0

# Query GitHub releases
./scripts/query-github-releases.sh apache commons-lang "v?3\\.1[234]\\."

# Verify URL
./scripts/verify-url.sh "https://github.com/apache/commons-lang/releases/tag/rel/commons-lang-3.14.0" "3.14.0"
```

### Phase 4: Content Extraction

Analyze release notes to extract:
- **Security**: CVEs and security issues (only if explicitly mentioned)
- **Breaking Changes**: API removals, signature changes, behavior modifications
- **Major Features**: Transformative capabilities only
- **Critical Fixes**: Data corruption, security hardening, crash/hang fixes

**Omit**: Routine bug fixes, minor enhancements, performance tweaks

### Phase 5: Reporting

Generate structured report using the template.

**Template:** `templates/dependency-report-template.md`

**Example:** `examples/sample-research-output.md`

## Scripts Reference

### fetch-maven-versions.sh

Queries Maven Central for version history and filters for applicable versions.

**Parameters:**
1. `groupId` - Maven group ID
2. `artifactId` - Maven artifact ID
3. `currentVersion` - Current version in use
4. `availableVersion` - Target version

**Example:**
```bash
./scripts/fetch-maven-versions.sh com.google.guava guava 31.0-jre 33.0-jre
```

### extract-project-urls.sh

Extracts project homepage and SCM URLs from Maven POM.

**Parameters:**
1. `groupId` - Maven group ID
2. `artifactId` - Maven artifact ID
3. `version` - Version to query

**Example:**
```bash
./scripts/extract-project-urls.sh org.springframework.boot spring-boot-starter-web 3.2.0
```

### query-github-releases.sh

Queries GitHub Releases API for version information.

**Parameters:**
1. `org` - GitHub organization
2. `repo` - GitHub repository
3. `versionPattern` - Grep pattern for version filtering

**Example:**
```bash
./scripts/query-github-releases.sh spring-projects spring-boot "v?3\\.2\\."
```

### verify-url.sh

Verifies URL returns 200 OK and contains relevant content.

**Parameters:**
1. `url` - URL to verify
2. `expectedContent` - Content that should be present (e.g., version number)

**Example:**
```bash
./scripts/verify-url.sh "https://github.com/spring-projects/spring-boot/releases/tag/v3.2.0" "3.2.0"
```

## Integration Patterns

### Standalone Usage

Research a single dependency:
```bash
cd .github/skills/maven-dependency-research
./scripts/fetch-maven-versions.sh org.apache.commons commons-lang3 3.12.0 3.14.0
./scripts/extract-project-urls.sh org.apache.commons commons-lang3 3.14.0
# ... continue with other scripts
```

### Agent Integration

Use from a custom agent or workflow:
```markdown
Use the maven-dependency-research skill to investigate:
- groupId: org.springframework.boot
- artifactId: spring-boot-starter-web
- currentVersion: 3.1.0
- availableVersion: 3.2.0

Follow the five-phase workflow and return structured findings.
```

### Batch Processing

Research multiple dependencies:
```bash
# Create dependency list file
cat > dependencies.txt << 'EOF'
org.apache.commons:commons-lang3:3.12.0:3.14.0
com.google.guava:guava:31.0-jre:33.0-jre
EOF

# Process each line
while IFS=: read -r groupId artifactId currentVer availableVer; do
  echo "Researching $groupId:$artifactId"
  ./scripts/fetch-maven-versions.sh "$groupId" "$artifactId" "$currentVer" "$availableVer"
done < dependencies.txt
```

## Quality Standards

All research outputs must include:
1. ✅ CVEs/Security section (state "None found in release notes" if none)
2. ✅ Breaking Changes section (even if empty)
3. ✅ Version numbers prefixed to changes (when gap >2 versions)
4. ✅ Only significant items (no routine maintenance)
5. ✅ Migration concerns in Notes section
6. ✅ Project retirement/EOL status checked
7. ✅ For ≤5 versions, all intermediate versions listed in Release Notes
8. ✅ All URLs verified (200 OK with relevant content)

## Boundaries

**Do:**
- Use the scripts to automate research
- Verify all URLs before including in reports
- Focus on breaking changes and security issues
- Keep descriptions concise (one line per item)
- Document research methodology

**Don't:**
- Include unverified URLs in reports
- Research CVEs beyond what's in release notes
- Include routine bug fixes or minor enhancements
- Skip intermediate versions when ≤5 versions apart
- Make assumptions about breaking changes without evidence

## Error Handling

Scripts include proper error handling:
- Retry logic for network calls (2 retries, 5s timeout)
- Fallback strategies when primary methods fail
- Clear error messages for debugging
- Exit codes for automation

## Examples

See `examples/sample-research-output.md` for a complete example of expected output format.

## Maintenance

**Version History:**
- 1.0.0 (2025-12-20): Initial release

**Future Enhancements:**
- Automated CVE database integration
- Parallel processing for batch research
- Caching layer for repeated queries
- Integration with Maven version plugins

## References

- [Maven Central Repository](https://repo1.maven.org/maven2/)
- [Maven Central Search](https://search.maven.org/)
- [GitHub Releases API](https://docs.github.com/en/rest/releases)
- [Agent Skills Specification](https://agentskills.io/what-are-skills)
