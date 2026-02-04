---
name: cui-documentation
description: General documentation standards for README, AsciiDoc, and technical documentation
allowed-tools: [Read, Edit, Write, Bash, Grep, Glob]
---

# CUI Documentation Skill

Standards for writing clear, maintainable technical documentation in CUI projects.

**Note**: This skill covers general documentation. For code documentation, use:
- `cui-javadoc` for Java code documentation
- `cui-frontend-development/jsdoc-standards.md` for JavaScript documentation

## Workflow

### Step 1: Load Applicable Documentation Standards

**CRITICAL**: Load current documentation standards based on context.

1. **Always load core documentation standards**:
   ```
   Read: standards/documentation-core.md
   ```

2. **Conditional loading based on context**:

   - If creating or editing README files:
     ```
     Read: standards/readme-structure.md
     ```

   - If working with AsciiDoc files:
     ```
     Read: standards/asciidoc-formatting.md
     ```

   - If reviewing tone, style, or language (or comprehensive reviews):
     ```
     Read: standards/tone-and-style.md
     ```

   - If organizing, restructuring, or reviewing documentation structure:
     ```
     Read: standards/organization-standards.md
     ```

3. **Extract key requirements from all loaded standards**

4. **Store in working memory** for use during task execution

### Step 2: Analyze Existing Documentation

**When to Execute**: After loading standards

**What to Analyze**:

1. **General Documentation Quality**:
   - Check tone and style (see documentation-core.md for requirements)
   - Verify no marketing language or promotional wording
   - Validate factual descriptions with sources
   - Review technical precision
   - Check for conciseness and clarity

2. **Tone and Style** (if tone-and-style.md loaded):
   - Identify marketing language and subjective claims
   - Check for qualification patterns ("production-proven", "extensively tested")
   - Verify no transitional markers (status indicators, TODO items)
   - Ensure objective vs subjective language compliance
   - Review for promotional wording and self-praise
   - Validate all claims are verifiable or attributed

3. **Organization and Structure** (if organization-standards.md loaded):
   - Verify document follows single-aspect principle
   - Check document size (50-400 lines)
   - Validate file naming (kebab-case)
   - Identify duplicate content across documents
   - Check for transitional/status markers
   - Assess cross-reference integrity
   - Review logical document organization

4. **AsciiDoc Format** (if .adoc files):
   - Verify document header with required attributes
   - Check cross-reference syntax (`xref:` format)
   - **CRITICAL**: Validate blank lines before all lists
   - Review code block formatting with language specification
   - Check section hierarchy and numbering

5. **README Structure** (if README files):
   - Verify title and description
   - Check Maven coordinates placement
   - Review core concepts section
   - Validate usage examples completeness
   - Check configuration documentation
   - Review best practices section

6. **Content Quality**:
   - Only existing code/features documented
   - All references verified to exist
   - RFC references must be relevant (see documentation-core.md for verification requirements)
   - Consistent terminology used
   - Code examples from unit tests
   - All public APIs documented

### Step 3: Apply Documentation Standards

**When to Execute**: During documentation creation or review

**What to Apply**:

1. **Core Documentation Principles**:
   - Professional, neutral, objective tone
   - No marketing or promotional language
   - Technical precision with verifiable sources
   - Concise, clear language
   - Document only existing features
   - Use linking instead of duplication

2. **AsciiDoc Formatting** (if .adoc files):

   **README Files** (README.adoc, */README.adoc):
   - Use `:toc: macro` (NOT `:toc: left`)
   - Place `toc::[]` manually where TOC should appear
   - Example header:
     ```asciidoc
     = Module Name
     :toc: macro
     :toclevels: 3
     :sectnums:
     :source-highlighter: highlight.js

     Brief module description.

     toc::[]

     == Core Concepts
     ```

   **General Documentation Files** (not READMEs):
   - Use `:toc: left` for automatic left sidebar TOC
   - Do NOT use `:toc: macro`
   - Example header:
     ```asciidoc
     = Document Title
     :toc: left
     :toclevels: 3
     :toc-title: Table of Contents
     :sectnums:
     :source-highlighter: highlight.js
     ```

   **All AsciiDoc Files**:
   - Use `xref:path/to/file.adoc[Link Text]` for cross-references
   - **ALWAYS** add blank line before lists
   - Specify language in code blocks
   - Follow proper section hierarchy

3. **README Structure** (if README files):
   - Title and brief description
   - Maven coordinates immediately after description
   - Core Concepts section
   - Detailed Component Documentation with links to source
   - Usage Examples (complete, working code)
   - Configuration section
   - Best Practices
   - Technical Details
   - Related Documentation

4. **Code Examples**:
   - Must be complete and compilable (see documentation-core.md for requirements)
   - Include all necessary imports
   - Show proper error handling
   - Follow project coding standards
   - Be verified by unit tests
   - Use clear variable names
   - Include comments for complex steps
   - Configuration placeholders must be clearly identified

### Step 4: Verify Documentation Quality

**When to Execute**: After creating or updating documentation

**Quality Checks**:

1. **Tone and Style Verification**:
   - [ ] Professional, neutral tone
   - [ ] No marketing language
   - [ ] Factual descriptions
   - [ ] Technical precision
   - [ ] Concise language

2. **AsciiDoc Format Verification** (if .adoc):
   - [ ] Document header complete
   - [ ] Cross-references use `xref:` syntax
   - [ ] Blank lines before all lists
   - [ ] Code blocks have language specification
   - [ ] Section hierarchy correct

3. **README Structure Verification** (if README):
   - [ ] Title and description present
   - [ ] Maven coordinates included
   - [ ] Core concepts documented
   - [ ] Usage examples complete
   - [ ] Configuration documented
   - [ ] Best practices included

4. **Content Quality Verification**:
   - [ ] Only existing features documented
   - [ ] All references verified
   - [ ] Consistent terminology
   - [ ] Code examples from tests
   - [ ] All public APIs documented

5. **Build Verification** (if applicable):
   ```bash
   # Verify documentation builds successfully
   mvn clean install -DskipTests
   ```

### Step 5: Automated Validation (AsciiDoc)

**When to Execute**: After creating or updating AsciiDoc files

**Available Validation Scripts**:

This skill includes two validation scripts in the `scripts/` directory:

1. **`asciidoc-validator.sh`** - Format validation script
   - Validates AsciiDoc format compliance
   - Checks for blank lines before lists
   - Verifies section header formatting
   - Detects list syntax issues

   Usage:
   ```bash
   # Validate a single file
   scripts/asciidoc-validator.sh path/to/file.adoc

   # Validate all files in a directory
   scripts/asciidoc-validator.sh directory/
   ```

2. **`verify-adoc-links.py`** - Link verification script
   - Validates cross-reference links
   - Checks for broken file references
   - Verifies anchor existence
   - Detects deprecated syntax

   Usage:
   ```bash
   # Verify links in a single file
   python3 scripts/verify-adoc-links.py --file path/to/file.adoc --report target/links.md

   # Verify links in directory (non-recursive)
   python3 scripts/verify-adoc-links.py --directory directory/ --report target/links.md

   # Verify links recursively
   python3 scripts/verify-adoc-links.py --directory directory/ --recursive --report target/links.md
   ```

**Validation Workflow**:

1. Run format validation:
   ```bash
   scripts/asciidoc-validator.sh target_file_or_directory 2>&1
   ```

2. Run link verification:
   ```bash
   mkdir -p target/asciidoc-reviewer
   python3 scripts/verify-adoc-links.py --file target.adoc --report target/asciidoc-reviewer/links.md 2>&1
   ```

3. **Distinguish link validation results**:
   - **Syntax Valid + Target Exists**: ✅ Link is correct
   - **Syntax Valid + Target Missing**: ❌ Reference to non-existent file
     - Common cause: Documentation for planned/future features
     - Action: Either create the target document or remove the reference
     - Do NOT leave references to non-existent files
   - **Syntax Invalid**: ❌ Malformed cross-reference
     - Fix syntax to use proper `xref:path[text]` format

4. Review validation output and fix issues

5. Re-run validation to confirm fixes

**Script Paths**:
- Scripts are located in the skill directory at: `scripts/asciidoc-validator.sh` and `scripts/verify-adoc-links.py`
- When running from project root, use relative path from current working directory
- Scripts require execution from a location where relative paths to AsciiDoc files are correct

### Step 6: Document Changes and Commit

**When to Execute**: After verification passes

**Commit Standards**:
- Follow standard commit message format
- Reference related issues
- Document significant documentation changes
- Add co-authored-by line for Claude Code

## Common Documentation Patterns

### AsciiDoc Document Header
```asciidoc
= Document Title
:toc: left
:toclevels: 3
:toc-title: Table of Contents
:sectnums:
:source-highlighter: highlight.js

== Purpose
Brief description of the document's purpose.

== Related Documentation
* xref:other-document.adoc[Other Document]
* xref:../category/document.adoc[Category Document]
```

### README Structure Example
```asciidoc
= Module Name

Concise description of the module's purpose and key features.

== Maven Coordinates

[source, xml]
----
<dependency>
    <groupId>group.id</groupId>
    <artifactId>artifact-id</artifactId>
</dependency>
----

== Core Concepts

=== Feature One

* Capability details
* Integration points
* Key benefits

== Usage Examples

=== Basic Usage
[source,java]
----
// Complete code example
----

== Configuration

=== Property Configuration
[source,properties]
----
# Configuration examples
----
```

### Code Block with Language
```asciidoc
[source,java]
----
@Test
void shouldValidateToken() {
    // Test implementation
}
----
```

## Error Prevention

### Common Documentation Issues

1. **Missing Blank Line Before List**: AsciiDoc grammar requires blank line
2. **Wrong Cross-Reference Syntax**: Use `xref:` not `link:`
3. **Missing Language Specification**: Always specify language in code blocks
4. **Marketing Language**: Use neutral, factual descriptions
5. **Incomplete Code Examples**: Provide complete, compilable examples

### Quality Violations

1. **Promotional Tone**: "Our amazing feature" → "Feature X provides..."
2. **Incomplete Header**: Missing required document attributes
3. **Invalid References**: Links to non-existent files
4. **Speculative Documentation**: Documenting planned features
5. **Duplicate Content**: Copy-paste instead of cross-reference

## Quality Verification

All documentation must pass:
- [x] Professional, neutral tone
- [x] Proper AsciiDoc formatting
- [x] Complete code examples
- [x] Verified references
- [x] Consistent terminology
- [x] No marketing language
- [x] Documents only existing features

## References

All documentation standards are located in the `standards/` directory:

* **Core documentation principles**: [standards/documentation-core.md](standards/documentation-core.md)
* **Tone and style requirements**: [standards/tone-and-style.md](standards/tone-and-style.md)
* **Organization and structure**: [standards/organization-standards.md](standards/organization-standards.md)
* **AsciiDoc formatting guidelines**: [standards/asciidoc-formatting.md](standards/asciidoc-formatting.md)
* **README structure patterns**: [standards/readme-structure.md](standards/readme-structure.md)
