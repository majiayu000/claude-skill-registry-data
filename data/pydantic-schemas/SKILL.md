---
name: pydantic-schemas
description: ALWAYS USE when working with Pydantic models, BaseModel, Field, validators, or data contracts. MUST be loaded before creating any Pydantic schemas, configuration classes, or API contracts. Provides v2 syntax validation and SDK research steps.
---

# Pydantic Schema Development (Research-Driven)

## Philosophy

This skill does NOT prescribe specific patterns. Instead, it guides you to:
1. **Research** the current Pydantic version and capabilities
2. **Discover** existing patterns in the codebase
3. **Validate** your implementations against SDK documentation
4. **Verify** backward compatibility and contract stability

## Pre-Implementation Research Protocol

### Step 1: Verify Runtime Environment

**ALWAYS run this first**:
```bash
python -c "import pydantic; print(f'Pydantic {pydantic.__version__}')"
```

**Critical Questions to Answer**:
- What version is installed? (v1 or v2?)
- Does it match the documented requirements?
- Are there breaking changes from the docs?

### Step 2: Research SDK State (if unfamiliar)

**When to research**: If you encounter unfamiliar Pydantic features or need to validate syntax

**Research queries** (use WebSearch):
- "Pydantic v2 [feature] documentation 2025"
- "Pydantic v2 breaking changes from v1"
- "Pydantic v2 best practices [specific use case]"

**SDK documentation**: https://docs.pydantic.dev/latest/

### Step 3: Discover Existing Patterns

**BEFORE creating new schemas**, search for existing implementations:

```bash
# Find existing Pydantic models
rg "class.*\(BaseModel\)" --type py

# Find field validators
rg "@field_validator|@model_validator" --type py

# Find ConfigDict usage
rg "model_config.*ConfigDict" --type py
```

**Key questions**:
- What patterns are already in use?
- Are they using v1 or v2 syntax?
- What validation patterns exist?

### Step 4: Validate Against Requirements

Check [API-REFERENCE.md](API-REFERENCE.md) for known v2 patterns, then verify:
- Are you using v2 syntax (`@field_validator`, NOT `@validator`)?
- Are you using `model_config = ConfigDict(...)`, NOT `class Config:`?
- Are type hints present on ALL fields and methods?
- Are secrets using `SecretStr` (not `str`)?

## Implementation Guidance (Not Prescriptive)

### Contract Design Principles

When designing contract schemas (like CompiledArtifacts):
- Consider immutability: `frozen=True` prevents accidental mutations
- Consider strict validation: `extra="forbid"` rejects unknown fields
- Consider versioning: Use semantic versioning for contract changes
- Consider backward compatibility: Only add optional fields in minor versions

**Research questions**:
- What are the actual integration points? (Read architecture docs)
- Who are the consumers of this contract?
- What changes would break compatibility?

### Security Considerations

When handling sensitive data:
- Research: What fields contain secrets? (passwords, API keys, tokens)
- Validate: Are you using `SecretStr` for sensitive fields?
- Verify: Are secrets excluded from logs and error messages?

**SDK feature to research**: `pydantic.SecretStr` usage and `.get_secret_value()` pattern

### Configuration Models

When building configuration from environment variables:
- Research: `pydantic-settings` package (separate from core Pydantic)
- Discover: What env var naming conventions exist in the codebase?
- Validate: Are you using `SettingsConfigDict` with appropriate `env_prefix`?

**SDK feature to research**: `pydantic_settings.BaseSettings` and `SettingsConfigDict`

## Validation Workflow

### Before Implementation
1. ✅ Verified Pydantic version
2. ✅ Searched for existing patterns in codebase
3. ✅ Read architecture docs to understand requirements
4. ✅ Identified security requirements (secrets, PII)
5. ✅ Researched unfamiliar Pydantic features

### During Implementation
1. ✅ Using `from __future__ import annotations`
2. ✅ Type hints on ALL fields and methods
3. ✅ Using v2 syntax (`@field_validator`, `model_config`)
4. ✅ Secrets using `SecretStr` (not `str`)
5. ✅ Contract models using `frozen=True` and `extra="forbid"`

### After Implementation
1. ✅ Run type checker: `mypy --strict [file]`
2. ✅ Verify JSON schema export works: `Model.model_json_schema()`
3. ✅ Test validation with invalid data
4. ✅ Test serialization/deserialization
5. ✅ Check backward compatibility if modifying existing contracts

## Context Injection (For Future Claude Instances)

When this skill is invoked, you should:

1. **Verify runtime state** (don't assume):
   ```bash
   python -c "import pydantic; print(pydantic.__version__)"
   ```

2. **Discover existing patterns** (don't invent):
   ```bash
   rg "class.*\(BaseModel\)" --type py
   ```

3. **Research when uncertain** (don't guess):
   - Use WebSearch for "Pydantic v2 [feature] documentation 2025"
   - Check official docs: https://docs.pydantic.dev/latest/

4. **Validate against architecture** (don't assume requirements):
   - Read relevant architecture docs in `/docs/`
   - Understand the actual contract requirements
   - Check for existing schema definitions

## Quick Reference: Common Research Queries

Use these WebSearch queries when encountering specific needs:

- **Field validation**: "Pydantic v2 field_validator examples 2025"
- **Model validation**: "Pydantic v2 model_validator cross-field validation"
- **Settings**: "pydantic-settings BaseSettings environment variables 2025"
- **Secrets**: "Pydantic v2 SecretStr SecretBytes best practices"
- **JSON Schema**: "Pydantic v2 model_json_schema custom schema"
- **Performance**: "Pydantic v2 performance optimization tips 2025"
- **Migration**: "Pydantic v1 to v2 migration guide breaking changes"

## References

- [API-REFERENCE.md](API-REFERENCE.md): Curated v2 API changes and migration patterns
- [Pydantic Documentation](https://docs.pydantic.dev/latest/): Official SDK documentation
- [pydantic-settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/): Environment variable configuration

---

**Remember**: This skill provides research guidance, NOT prescriptive patterns. Always:
1. Verify the runtime environment
2. Discover existing codebase patterns
3. Research SDK capabilities when needed
4. Validate against actual requirements
