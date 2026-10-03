---
name: docs-validation
description: Validate documentation against the current product by executing commands and flows, checking links, versions, screenshots, prerequisites, terminology, code examples, and claimed outcomes before publication.
---
# Documentation Validation

Use when documentation needs evidence that it still describes the supported product accurately.

## Procedure
1. Identify the product version, environment, audience, and supported path the document claims to describe.
2. Follow the instructions from the stated starting state rather than relying on author memory or an already configured machine.
3. Run commands and code examples exactly as written and compare actual output or behavior with the documented expectation.
4. Verify UI labels, navigation, options, file paths, environment variables, defaults, and version-specific behavior.
5. Check links, referenced files, downloads, screenshots, diagrams, and source citations for existence and current relevance.
6. Confirm prerequisites and permissions are complete and appear before they are needed.
7. Test recovery or troubleshooting steps where they protect readers from common failures.
8. Record exact validation environment and unresolved platform or version limitations, then correct the documentation before marking it current.

## Decision rules
- Documentation is executable product surface when users rely on its instructions.
- A command that once worked is not evidence it works now.
- Screenshots can become inaccurate even when prose remains valid.
- Validate from a clean or representative state where hidden setup would otherwise mask missing steps.

## Quality gate
The documentation is validated when the stated workflow succeeds from documented prerequisites on a representative current environment, commands and references are correct, expected results match reality, known limitations are visible, and no required step depends on undocumented author context.