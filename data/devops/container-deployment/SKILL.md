---
name: container-deployment
description: Container strategies for .NET libraries and test environments. Use when working with Docker test environments, container-based integration testing, or NuGet package container builds. Not typically for production deployment of libraries.
---

# Container & Deployment Engineer

## Mission
Implement containerized test environments and integration test infrastructure for the Lidarr.Plugin.Common shared library.

## Expertise Areas

### 1. Container-Based Testing
- Docker containers for integration tests
- Test environment isolation
- Multi-version testing (different Lidarr versions)
- Clean test environment setup/teardown

### 2. CI Container Integration
- GitHub Actions container services
- Docker-in-Docker for CI
- Test container orchestration
- Performance optimization for CI

### 3. Development Containers
- devcontainer.json for VS Code
- Codespaces configuration
- Consistent development environments
- Pre-configured tooling

## Current Context

### Lidarr.Plugin.Common Status
- **Library Type**: NuGet package (not deployed, consumed)
- **Container Usage**: ❌ Not currently using containers
- **Testing**: ⚠️ Tests run on host, not in containers
- **DevContainers**: ❌ Not configured

### Enhancement Opportunities
1. **Container Test Environments**: Test against multiple Lidarr versions
2. **Dev Containers**: VS Code devcontainer for contributors
3. **CI Container Services**: Use containers for integration tests
4. **Example Containers**: Sample environments for plugin developers

## Best Practices

### Dev Container Configuration
```json
// .devcontainer/devcontainer.json
{
  "name": "Lidarr Plugin Development",
  "image": "mcr.microsoft.com/devcontainers/dotnet:6.0",
  "features": {
    "ghcr.io/devcontainers/features/docker-in-docker:2": {},
    "ghcr.io/devcontainers/features/github-cli:1": {}
  },
  "customizations": {
    "vscode": {
      "extensions": [
        "ms-dotnettools.csharp",
        "ms-dotnettools.csdevkit"
      ]
    }
  },
  "postCreateCommand": "dotnet restore",
  "forwardPorts": [8686]
}
```

### Container-Based Integration Tests
```yaml
# .github/workflows/integration-tests.yml
jobs:
  test-with-lidarr:
    runs-on: ubuntu-latest
    services:
      lidarr:
        image: ghcr.io/hotio/lidarr:pr-plugins-2.14.2.4786
        ports:
          - 8686:8686
        env:
          PUID: 1000
          PGID: 1000
    steps:
      - name: Run integration tests against Lidarr
        run: dotnet test --filter Category=Integration
```

## Related Skills
- `integration-testing` - Leverage containers for integration tests
- `code-quality` - Consistent environments improve quality

## Examples

### Example 1: Create Dev Container
**User**: "Set up a development container for contributors"
**Action**: Create .devcontainer/devcontainer.json with .NET 6/8 SDKs, extensions, and Lidarr test instance

### Example 2: Container-Based Tests
**User**: "Run integration tests against real Lidarr in container"
**Action**: Create Docker Compose with Lidarr service, configure test project to connect, run tests in CI
