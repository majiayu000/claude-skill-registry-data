---
name: buildkite
description: Use this skill when working with Buildkite CI/CD pipelines, agents, builds, test analytics, or package registries. Covers pipeline configuration, YAML syntax, agent setup, build steps, plugins, and API usage.
---

# Buildkite Skill

Comprehensive assistance with Buildkite development, generated from official documentation.

## When to Use This Skill

This skill should be triggered when:
- Creating or modifying Buildkite pipeline YAML configurations
- Setting up or troubleshooting Buildkite agents
- Working with build artifacts (upload/download)
- Implementing dynamic pipelines or conditional builds
- Configuring agent hooks or plugins
- Managing build dependencies and step ordering
- Using `buildkite-agent` CLI commands
- Setting up input/block steps for manual approvals
- Troubleshooting agent connectivity or build failures
- Configuring artifact storage (S3, GCS, Azure, Artifactory)
- Working with build metadata and environment variables
- Implementing deployment workflows with Buildkite

## Key Concepts

### Agent
A small, reliable build runner that polls Buildkite for work and executes jobs on your infrastructure. Agents can run on local machines, cloud servers, or containerized environments.

### Pipeline
A container for modeling workflows. Pipelines define a series of steps (commands, waits, blocks, inputs, triggers) to achieve goals like building, testing, and deploying.

### Step Types
- **Command step**: Runs shell commands on agents
- **Wait step**: Pauses until all previous jobs complete
- **Block step**: Pauses until manually unblocked
- **Input step**: Collects user information without blocking other steps
- **Trigger step**: Creates a build on another pipeline
- **Group step**: Displays multiple sub-steps as one logical unit

### Artifact
Files generated during a build, stored in Buildkite-managed storage or custom storage (S3/GCS/Azure). Used to pass data between steps or store build outputs.

### Queue
Defines agents on which pipeline builds run. Queues isolate groups of agents for specific pipelines, teams, or purposes (e.g., deployment agents).

### Cluster
Groups queues and pipelines together, allowing teams to self-manage agent pools and create isolated sets within an organization.

## Quick Reference

### Example 1: Basic Pipeline with Multiple Steps

```yaml
steps:
  - label: ":hammer: Tests"
    command: "npm install && npm test"

  - wait

  - label: ":package: Build"
    command: "npm run build"
    artifact_paths: "dist/**/*"
```

**Description**: Simple pipeline with tests, a wait step, and a build step that uploads artifacts.

---

### Example 2: Uploading Artifacts

```bash
# Upload specific file
buildkite-agent artifact upload log/test.log

# Upload all logs
buildkite-agent artifact upload "log/*.log"

# Upload with glob pattern for multiple file types
buildkite-agent artifact upload "*/**/*.jpg;*/**/*.jpeg;*/**/*.png"

# Upload entire directory
buildkite-agent artifact upload "coverage/**/*"
```

**Description**: Various ways to upload build artifacts using the Buildkite agent CLI.

---

### Example 3: Downloading Artifacts

```bash
# Download specific artifact
buildkite-agent artifact download build.zip .

# Download from specific step
buildkite-agent artifact download "pkg/*.tar.gz" . --step "build"

# Download all logs
buildkite-agent artifact download "log/*" .

# Download from triggering build
buildkite-agent artifact download "*.jpg" images/ --build $BUILDKITE_TRIGGERED_FROM_BUILD_ID
```

**Description**: Download artifacts from current or previous build steps.

---

### Example 4: Input Step for User Input

```yaml
steps:
  - input: "Who is running this script?"
    fields:
      - text: "Your name"
        key: "name"

  - label: "Run script"
    command: |
      NAME=$(buildkite-agent meta-data get name)
      echo "Hello, $NAME!"
```

**Description**: Collect user input and use it in subsequent steps via meta-data.

---

### Example 5: Conditional Steps with Dependencies

```yaml
steps:
  - label: "Tests"
    key: "tests"
    command: "npm test"

  - label: "Deploy"
    command: "deploy.sh"
    depends_on: "tests"
    if: build.branch == "main"
```

**Description**: Step that only runs on main branch and depends on tests passing.

---

### Example 6: Group Step for Organization

```yaml
steps:
  - group: ":lock_with_ink_pen: Security Audits"
    key: "audits"
    steps:
      - label: ":brakeman: Brakeman"
        command: ".buildkite/steps/brakeman"
      - label: ":bundleaudit: Bundle Audit"
        command: ".buildkite/steps/bundleaudit"
      - label: ":yarn: Yarn Audit"
        command: ".buildkite/steps/yarn"
```

**Description**: Group related steps together for better visual organization in the UI.

---

### Example 7: Custom S3 Artifact Storage

```bash
# Set environment variables for custom S3 bucket
export BUILDKITE_ARTIFACT_UPLOAD_DESTINATION="s3://my-bucket/$BUILDKITE_JOB_ID"
export BUILDKITE_S3_DEFAULT_REGION="us-west-2"
export BUILDKITE_S3_ACL="private"

# Upload artifact to custom S3 bucket
buildkite-agent artifact upload "build.tar.gz"
```

**Description**: Configure custom S3 bucket for artifact storage instead of Buildkite-managed storage.

---

### Example 8: Agent Configuration

```ini
# /etc/buildkite-agent/buildkite-agent.cfg
token="YOUR_AGENT_TOKEN"
name="my-agent-%n"
tags="queue=deploy,os=linux"
priority=5
build-path="/var/buildkite/builds"
hooks-path="/etc/buildkite-agent/hooks"
```

**Description**: Basic agent configuration file with token, name, tags, and paths.

---

### Example 9: Dynamic Pipeline Upload

```yaml
steps:
  - label: "Generate pipeline"
    command: |
      echo "steps:" > pipeline.yml
      for service in api web worker; do
        echo "  - label: \"Test $service\"" >> pipeline.yml
        echo "    command: \"test-$service.sh\"" >> pipeline.yml
      done
      buildkite-agent pipeline upload pipeline.yml
```

**Description**: Generate and upload a dynamic pipeline at runtime based on conditions.

---

### Example 10: Block Step for Manual Approval

```yaml
steps:
  - label: "Build"
    command: "make build"

  - block: ":rocket: Deploy to production?"
    prompt: "Ready to deploy?"
    fields:
      - select: "Environment"
        key: "environment"
        options:
          - label: "Staging"
            value: "staging"
          - label: "Production"
            value: "production"

  - label: "Deploy"
    command: |
      ENV=$(buildkite-agent meta-data get environment)
      ./deploy.sh $ENV
```

**Description**: Pause build for manual approval with environment selection.

## Reference Files

This skill includes comprehensive documentation in `references/`:

### agents.md (118 pages)
Complete agent documentation including:
- Installation on various platforms (Ubuntu, Debian, Red Hat, macOS, Windows, Docker, Kubernetes)
- Agent configuration and command-line reference
- Security best practices and securing agents
- SSH key configuration and Git mirrors
- Agent hooks (environment, pre-command, post-command, pre-exit)
- Running agents on AWS, Google Cloud, and Kubernetes
- Troubleshooting agent connectivity and performance issues

### pipelines.md
Pipeline configuration and step definitions:
- All step types (command, wait, block, input, trigger, group)
- Dynamic pipelines and conditionals
- Step dependencies and build matrix
- Environment variables and secrets management
- Pipeline templates and YAML syntax
- Branch configuration and scheduled builds

### builds.md
Build management and artifacts:
- Build artifacts (upload, download, search)
- Build metadata and environment variables
- Build timeouts and retention
- Managing log output
- Build status and notifications

### getting_started.md
Getting started guides:
- Setting up your first pipeline
- Understanding Buildkite architecture
- Creating hosted or self-hosted agents
- Basic workflow examples

## Working with This Skill

### For Beginners
Start with `getting_started.md` to understand Buildkite's architecture and create your first pipeline. Focus on:
- Basic pipeline YAML structure
- Simple command steps
- Agent setup and configuration

### For Pipeline Development
Use `pipelines.md` for:
- Step type references (command, wait, block, input, trigger, group)
- Conditional logic and dependencies
- Dynamic pipeline patterns
- Environment variable usage

### For Agent Management
Consult `agents.md` for:
- Installation on your platform
- Configuration options
- Security hardening
- Hook customization
- Troubleshooting connectivity issues

### For Artifact Management
Reference `builds.md` for:
- Uploading and downloading artifacts
- Custom storage configuration (S3, GCS, Azure, Artifactory)
- Artifact glob patterns
- Cross-step data sharing

### Common Patterns

**Pattern: Pass data between steps**
```yaml
steps:
  - label: "Build"
    command: |
      make build
      buildkite-agent artifact upload "dist/**/*"

  - wait

  - label: "Test"
    command: |
      buildkite-agent artifact download "dist/**/*" .
      make test
```

**Pattern: Parallel tests with dependencies**
```yaml
steps:
  - label: "Setup"
    key: "setup"
    command: "npm install"

  - wait

  - label: "Unit tests"
    command: "npm run test:unit"
    parallelism: 3
    depends_on: "setup"

  - label: "Integration tests"
    command: "npm run test:integration"
    depends_on: "setup"
```

**Pattern: Deploy only from main**
```yaml
steps:
  - label: "Deploy"
    command: "./deploy.sh"
    if: build.branch == "main" && build.state == "passed"
    branches: "main"
```

## Tips and Best Practices

1. **Use artifact_paths in steps** for automatic artifact upload after command completion
2. **Quote glob patterns** in artifact commands to prevent shell expansion
3. **Use step keys** for explicit dependencies instead of implicit ordering
4. **Tag agents** with queue names for proper job routing
5. **Store secrets in environment hooks** rather than in pipeline YAML
6. **Use wait steps** to control parallelization and ensure prerequisites
7. **Group related steps** to keep the build UI organized
8. **Use input steps** instead of block steps when you don't want to block parallel steps
9. **Set artifact retention** based on compliance and storage requirements
10. **Use dynamic pipelines** for complex conditional logic and matrix builds

## Resources

For detailed information on any topic:
1. Use the `references/` directory for comprehensive documentation
2. Each reference file contains detailed explanations, examples, and links
3. Code examples include language annotations for syntax highlighting
4. Search within reference files for specific commands, attributes, or patterns

## Notes

- This skill was automatically generated from official Buildkite documentation
- Reference files preserve structure and examples from source docs
- All examples are tested and validated from official documentation
- Quick reference patterns are extracted from real-world usage examples

## Updating

To refresh this skill with updated documentation:
1. Re-run the documentation scraper with the same configuration
2. The skill will be rebuilt with the latest information from Buildkite docs
