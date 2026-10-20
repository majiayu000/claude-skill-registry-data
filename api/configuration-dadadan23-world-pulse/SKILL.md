---
name: "configuration"
description: 'Implement configuration management patterns including environment variables, secrets, feature flags, and validation strategies. Use when setting up app configuration, managing environment-specific settings, implementing feature flags, storing secrets securely, or validating configuration at startup.'
metadata:
 author: "AgentX"
 version: "1.0.0"
 created: "2025-01-15"
 updated: "2025-01-15"
---

# Configuration Management

> **Purpose**: Manage application configuration securely across environments. 
> **Goal**: Externalized config, no hardcoded secrets, fail-fast validation. 
> **Note**: For implementation, see [C# Development](../csharp/SKILL.md) or [Python Development](../python/SKILL.md).

---

## Prerequisites

- Understanding of environment variables
- Access to a secrets manager for production

## Decision Tree

```
Configuration concern?
+- Where to store?
| +- Secrets (passwords, API keys) -> Vault / secrets manager
| +- Environment-specific -> Environment variables
| +- App defaults -> Config file (appsettings.json, .env.example)
| - Feature flags -> Remote config service
+- How to validate?
| +- Required values? -> Fail fast at startup (not at first use)
| +- Typed values? -> Parse + validate on load
| - Schema validation? -> Use config class / Pydantic model
- Multiple environments?
 +- Use layered config: base + environment override
 - NEVER commit .env files (use .env.example as template)
```

## Configuration Hierarchy

```
Priority (highest to lowest):
 1. Command-line arguments
 2. Environment variables
 3. Environment-specific config files
 4. Base config files
 5. Default values in code
```

**Principle**: Higher priority sources override lower ones.

---

## Environment Variables

### When to Use

**Environment Variables For:**
- Secrets (API keys, passwords, connection strings)
- Environment-specific URLs (API endpoints)
- Feature toggles that change per environment
- Cloud provider credentials

**Config Files For:**
- Structured configuration (nested settings)
- Default values
- Non-sensitive settings
- Documentation of available options

### Best Practices

```
[PASS] DO:
 - Use descriptive names: DATABASE_URL, API_KEY, FEATURE_NEW_UI_ENABLED
 - Prefix with app name for namespacing: MYAPP_DATABASE_URL
 - Document all required environment variables
 - Provide sensible defaults where safe
 - Validate on startup (fail fast)

[FAIL] DON'T:
 - Hardcode secrets in code or config files
 - Commit .env files to version control
 - Use environment variables for complex nested config
 - Leave required variables undocumented
```

---

## Best Practices Summary

| Practice | Description |
|----------|-------------|
| **Externalize config** | No config in code, all external |
| **Fail fast** | Validate all required config at startup |
| **Use secrets manager** | Never commit secrets to version control |
| **Type safety** | Use strongly-typed config classes |
| **Default values** | Provide sensible defaults where safe |
| **Document** | List all config options and their purpose |
| **Environment parity** | Same config structure across all environments |
| **Immutable config** | Don't change config at runtime |

---

## Configuration Libraries

| Language | Libraries |
|----------|-----------|
| **.NET** | IConfiguration, IOptions<T>, Azure Key Vault SDK |
| **Python** | python-dotenv, pydantic-settings, boto3 (AWS) |
| **Node.js** | dotenv, convict, config |
| **Java** | Spring Config, Apache Commons Configuration |
| **Go** | viper, envconfig |

---

**See Also**: [Security](../../architecture/security/SKILL.md) - [C# Development](../csharp/SKILL.md) - [Python Development](../python/SKILL.md)

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Config not loading in production | Check environment variable names match, verify config file is deployed |
| Secrets exposed in config files | Use secrets manager or user-secrets for development, never commit secrets |
| Feature flag not toggling | Check flag evaluation context, verify flag provider connection |

## References

- [Typed Config Secrets Flags](references/typed-config-secrets-flags.md)
- [Config Files And Anti Patterns](references/config-files-and-anti-patterns.md)