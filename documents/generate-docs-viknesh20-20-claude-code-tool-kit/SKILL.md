---
name: generate-docs
description: "Generates documentation matching the project's style — README files, API docs, inline documentation, or architecture docs. Auto-detects the documentation format in use."
argument-hint: "[file, module, 'readme', or 'api']"
allowed-tools: Read, Grep, Glob, Bash, Write
---

# Generate Documentation

## Detect Documentation Style
!`find . -name "README*" -o -name "CONTRIBUTING*" -o -name "CHANGELOG*" -o -name "docs" -type d 2>/dev/null | grep -v node_modules | grep -v .git | head -10`
!`ls docs/ doc/ documentation/ wiki/ 2>/dev/null`

## Detect Code Documentation Format
!`grep -r "\/\*\*" --include="*.ts" --include="*.js" --include="*.java" -l 2>/dev/null | head -3`
!`grep -r '"""' --include="*.py" -l 2>/dev/null | head -3`
!`grep -r "\/\/\/" --include="*.rs" --include="*.cs" --include="*.go" -l 2>/dev/null | head -3`

---

## Documentation Types

### Type 1: README Generation
If "readme" is specified, generate a complete README.md with:
- Project name and one-line description
- Badges (build status, coverage, version — if CI is configured)
- Table of contents
- Features list
- Prerequisites and installation
- Quick start / usage examples
- Configuration options
- API reference (if applicable)
- Contributing guidelines
- License

### Type 2: API Documentation
If "api" is specified:
- Find all public endpoints/routes/handlers
- Document each with: method, path, description, parameters, request body, response body, error codes
- Generate in the format matching existing docs (OpenAPI, Markdown, or inline)

### Type 3: Module/File Documentation
If a file or module is specified:
- Read the code completely
- Add inline documentation following the project's convention:
  - **JavaScript/TypeScript**: JSDoc (`/** ... */`)
  - **Python**: Docstrings (`"""..."""`)
  - **Go**: GoDoc comments (`// FunctionName ...`)
  - **Rust**: Doc comments (`/// ...`)
  - **Java**: Javadoc (`/** ... */`)
  - **C#**: XML comments (`/// <summary>`)
  - **Ruby**: YARD (`# @param`, `# @return`)

For each public function/method/class, document:
- Brief description of what it does
- Parameters with types and descriptions
- Return value with type and description
- Exceptions/errors that can be thrown
- Usage example (for complex APIs)

### Type 4: Architecture Documentation
If "architecture" is specified:
- Map the high-level system components
- Create ASCII or Mermaid diagrams
- Document data flow between components
- List external dependencies and integrations
- Note key design decisions and trade-offs

---

## Rules
- **Match existing style** — if the project uses JSDoc, don't add Python docstrings
- **Don't over-document** — skip obvious getters/setters/constructors
- **Document the why** — explain intent and gotchas, not just parameters
- **Keep it current** — documentation that lies is worse than no documentation
- **Show don't tell** — include usage examples for complex APIs
