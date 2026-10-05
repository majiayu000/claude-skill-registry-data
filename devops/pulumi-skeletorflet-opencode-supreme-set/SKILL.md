---
name: pulumi
description: Infrastructure as code in TS/Python/Go, resources, stacks, state, config, secrets, automation API, providers.
---

## pulumi

Modern infrastructure as code with Pulumi.

### Language support
- TypeScript/JavaScript: full type safety
- Python: native dicts and loops
- Go: strong typing, compile-time checks
- C#, Java, YAML

### Resources and stacks
- Resource registration: new Resource(name, args, opts)
- Stack references for cross-stack values
- Stack outputs and exports
- Stack config: pulumi config set, get

### State and secrets
- Service-managed backend (Pulumi Cloud)
- Self-managed backends: S3, Azure, GCS
- Secret encryption with pulumi config set --secret
- State import for existing resources

### Automation API
- Programmatic infrastructure deployment
- Inline programs within applications
- CI/CD integration without CLI
- Custom deployment workflows
