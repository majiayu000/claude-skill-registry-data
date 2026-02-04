---
name: commitlint-config
description: Commitlint configuration and GitHub Copilot commit message instruction templates with validation logic for conventional commit enforcement. Includes 6 required standards (conventional format, relaxed subject rules for Copilot compatibility, optional scope, Husky integration, required dependencies, Copilot instruction consistency). Use when creating or auditing commitlint.config.js and .copilot-commit-message-instructions.md files.
---

# Commitlint Configuration Skill

This skill provides commitlint.config.js and .copilot-commit-message-instructions.md templates and validation logic for conventional commit message enforcement.

## Purpose

Manage commitlint configuration to:

- Enforce conventional commit message format (type(scope): subject)
- Configure relaxed rules for GitHub Copilot compatibility
- Integrate with Husky pre-commit hooks
- Ensure consistency between commitlint rules and AI-generated messages
- Support subject length limits and formatting standards
- Guide GitHub Copilot to generate compliant commit messages

## Usage

This skill is invoked by the `commitlint-agent` when:

- Creating new commitlint.config.js files
- Creating GitHub Copilot instruction files
- Auditing existing commit message configurations
- Validating commitlint against standards

## Templates

Standard templates are located at:

```
templates/commitlint.config.template.js          # Commitlint validation rules (relaxed for Copilot)
templates/.copilot-commit-message-instructions.template.md  # GitHub Copilot guidance
```

## The 6 Commitlint Standards

### Rule 1: Conventional Commits Format (CRITICAL)

MUST enforce conventional commit message structure:

```
type(scope?): subject

body?

footer?
```

**Valid types:** feat, fix, docs, style, refactor, perf, test, chore, ci, build, revert

**Validation:**

- Check `type-enum` rule has all 11 standard types
- Verify error level (2 = error)

### Rule 2: Relaxed Subject Rules for GitHub Copilot Compatibility

**IMPORTANT:** GitHub Copilot currently does NOT honor commitlint configuration files. MetaSaver uses RELAXED RULES for Copilot compatibility.

**Requirements:**

- Subject must always be present - STRICT
- Can use any case (sentence-case, start-case, lowercase all acceptable) - RELAXED
- Avoid ending with a period, or end with any character acceptable (warning only, not blocking) - RELAXED
- Maximum length: 120 characters (warning only, not blocking) - RELAXED

**Validation:**

```javascript
// Verify relaxed rules configuration
config.rules["subject-case"] === [0]; // DISABLED (allows any case)
config.rules["subject-empty"] === [2, "never"]; // STRICT
config.rules["subject-full-stop"] === [1, "never", "."]; // WARNING
config.rules["header-max-length"] === [1, "always", 120]; // WARNING
config.rules["body-max-line-length"] === [0]; // DISABLED
```

### Rule 3: Optional Scope Support

Scope is optional but useful for monorepos:

```
✅ CORRECT:
feat(auth): add JWT middleware
fix(database): resolve connection pooling
docs(readme): update installation steps
```

**Validation:**

- No specific scope validation required (optional by design)
- Scope must be lowercase if present

### Rule 4: Husky Integration (CRITICAL)

Commitlint MUST be integrated with Husky for pre-commit enforcement:

**File structure:**

```
repo-root/
├── commitlint.config.js  ← Commitlint rules
├── .husky/
│   └── commit-msg        ← Hook that runs commitlint
└── package.json          ← Dependencies
```

**Validation:**

- Check `.husky/commit-msg` hook exists
- Verify hook calls `commitlint --edit`
- Confirm dependencies in package.json

### Rule 5: Required Dependencies

```json
{
  "devDependencies": {
    "@commitlint/cli": "^19.0.0",
    "@commitlint/config-conventional": "^19.0.0",
    "husky": "^9.0.0"
  }
}
```

**Validation:**

- Read package.json
- Verify all 3 dependencies present
- Check versions meet minimum requirements

### Rule 6: GitHub Copilot Instructions Consistency

GitHub Copilot commit message instructions MUST be consistent with commitlint rules:

**File:** `.copilot-commit-message-instructions.md`

**Requirements:**

1. Same commit types as commitlint.config.js type-enum
2. Same subject case rules documented (relaxed for Copilot)
3. Same length limits (120 char header)
4. Same punctuation rules (no period at end - warning)
5. Clear examples showing correct and incorrect formats
6. AI-specific guidance for generating compliant messages

**Validation:**

```typescript
function validateConsistency(commitlintConfig, copilotInstructions) {
  const errors = [];

  // Check types match
  const commitlintTypes = commitlintConfig.rules["type-enum"][2];
  const copilotTypes = extractTypesFromMarkdown(copilotInstructions);
  if (!arraysEqual(commitlintTypes, copilotTypes)) {
    errors.push("Types mismatch between commitlint and copilot instructions");
  }

  // Check relaxed rules documented
  if (
    !copilotInstructions.includes("sentence-case") &&
    !copilotInstructions.includes("any case")
  ) {
    errors.push("Copilot instructions missing relaxed case requirement");
  }

  // Check length limits documented
  if (!copilotInstructions.includes("120 characters")) {
    errors.push("Copilot instructions missing header length limit");
  }

  return errors;
}
```

## Validation

To validate commitlint configuration:

1. Check that commitlint.config.js exists at repository root
2. Check that .copilot-commit-message-instructions.md exists at root
3. Parse commitlint config and extract rules
4. Read copilot instructions markdown
5. Validate against 6 standards
6. Test configuration with sample commits
7. Report violations

### Validation Approach

```bash
# Rule 1: Check type-enum rule
node -e "const config = require('./commitlint.config.js'); console.log(config.default.rules['type-enum'])"

# Rule 2: Check relaxed rules
grep -q "subject-case.*\[0\]" commitlint.config.js || echo "VIOLATION: subject-case not disabled"
grep -q "subject-empty.*\[2" commitlint.config.js || echo "VIOLATION: subject-empty not strict"

# Rule 4: Check Husky integration
[ -f ".husky/commit-msg" ] || echo "VIOLATION: Missing commit-msg hook"
grep -q "commitlint" .husky/commit-msg || echo "VIOLATION: Hook doesn't call commitlint"

# Rule 5: Check dependencies
jq '.devDependencies | has("@commitlint/cli")' package.json
jq '.devDependencies | has("@commitlint/config-conventional")' package.json

# Rule 6: Check copilot instructions consistency
[ -f ".copilot-commit-message-instructions.md" ] || echo "VIOLATION: Missing copilot instructions"
```

## Repository Type Considerations

- **Consumer Repos**: Strict enforcement of all 6 standards
- **Library Repos**: May have additional commit types or custom rules
- **All Repos**: Must have both commitlint.config.js AND .copilot-commit-message-instructions.md

## Best Practices

1. Always create both files (commitlint.config.js and .copilot-commit-message-instructions.md)
2. Verify consistency between commitlint rules and copilot instructions
3. Use relaxed rules to accommodate GitHub Copilot's natural style
4. Integrate with Husky for automated enforcement
5. Test configuration with sample commits
6. Keep types consistent across both files
7. Re-audit after making changes

## Integration

This skill integrates with:

- Repository type provided via `scope` parameter. If not provided, use `/skill scope-check`
- `/skill audit-workflow` - Bi-directional comparison workflow
- `/skill remediation-options` - Conform/Update/Ignore choices
- `husky-agent` - For commit-msg hook integration
