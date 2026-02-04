---
name: readme-creator
description: Guide for creating and updating README files following autonomous-bits development standards. Use this when asked to create or update README files, ensure documentation completeness, or review README quality.
license: MIT
---

# README Creator

This skill guides agents in creating and updating comprehensive README files that follow the autonomous-bits development standards.

## When to Use This Skill

Use this skill when:
- Creating a new project or repository
- Updating existing README files to meet current standards
- Reviewing README completeness and quality
- Ensuring consistent documentation across projects
- Asked to "create a README", "update docs", or "improve documentation"

## Prerequisites

- Access to the project repository
- Understanding of the project's purpose and architecture
- Knowledge of project dependencies and setup requirements
- Access to related documentation (CONTRIBUTING.md, CHANGELOG.md, etc.)

## Instructions

### 1. Assess Current State

**Check for existing README:**
- Read the current README.md if it exists
- Identify missing sections
- Note outdated information
- Review against the checklist below

### 2. Create README Structure

**Use this essential sections checklist:**

1. **Project Name and One-Line Description**
   - Clear, concise title at the top
   - Brief summary (1-2 sentences) of what the project does
   - Example: "A Nomos provider that reads Terraform/OpenTofu remote state files"

2. **Purpose and Overview**
   - Why does this project exist?
   - What problem does it solve?
   - High-level architecture or approach

3. **Prerequisites and Supported Platforms**
   - Required software with specific versions (e.g., "Go 1.25+")
   - Operating system requirements
   - Development tools (Docker, Make, etc.)
   - External dependencies

4. **Installation and Setup Steps**
   - Clone repository command
   - Dependency installation (e.g., `make deps`, `npm install`)
   - Initial configuration steps
   - Database/service setup if needed

5. **Configuration**
   - Environment variables with descriptions
   - Configuration files and their purposes
   - Secrets management (never include actual secrets)
   - Feature flags if applicable
   - Example: Create `.env.example` reference

6. **How to Run Locally**
   - Development server commands
   - Build commands (e.g., `make build`)
   - Run commands (e.g., `make run`, `npm start`)
   - Port information and access URLs

7. **How to Run Tests and Linters**
   - Unit test commands (e.g., `make test`, `go test ./...`)
   - Integration test commands with any required tags
   - Linting and formatting (e.g., `make verify`, `npm run lint`)
   - Coverage requirements (e.g., "80%+ coverage required")
   - Race detection commands (e.g., `go test -race`)

8. **Deployment Instructions**
   - Deployment process overview
   - CI/CD pipeline information
   - Environment-specific considerations
   - Release process and versioning

9. **Basic Usage Examples**
   - Common use cases with code examples
   - CLI command examples with expected output
   - API usage snippets
   - Configuration examples

10. **Links to Further Documentation**
    - Architecture decision records (ADRs)
    - API documentation
    - Design documents
    - Contributing guidelines (CONTRIBUTING.md)
    - Changelog (CHANGELOG.md)
    - Related repositories

11. **Contact/Owner Information**
    - Project maintainers or team name
    - How to get support
    - Issue tracker URL
    - Communication channels (Slack, Discord, etc.)

### 3. Apply Language-Specific Guidelines

**For Go Projects:**
```markdown
## Prerequisites

- Go 1.25+
- Make
- Docker (optional)

## Installation

\```bash
git clone <repository-url>
cd <project-name>
make deps && make tidy
\```

## Testing

\```bash
make test              # Unit tests (80%+ coverage required)
make verify            # fmt + vet + lint + test
go test -race ./...    # Run with race detection
\```
```

**For TypeScript/Node.js Projects:**
```markdown
## Prerequisites

- Node.js 20+
- npm or yarn

## Installation

\```bash
npm install
\```

## Development

\```bash
npm run dev          # Start dev server
npm run build        # Production build
npm test             # Run tests
npm run lint         # Run linter
\```
```

**For Python Projects:**
```markdown
## Prerequisites

- Python 3.11+
- pip or poetry

## Installation

\```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
\```

## Testing

\```bash
pytest                 # Run tests
pytest --cov          # With coverage
\```
```

### 4. Include Examples and Code Blocks

**Always provide:**
- Actual command examples users can copy-paste
- Expected output where helpful
- Configuration file snippets
- API usage examples

**Example:**
```markdown
## Usage

### Starting the Provider

\```bash
# Set environment variables
export BACKEND_TYPE=local
export STATE_FILE=/path/to/terraform.tfstate

# Run the provider
./bin/nomos-provider-terraform-remote-state
\```

The provider will print:
\```
PROVIDER_PORT=50051
\```
```

### 5. Add Best Practices Section

Include project-specific best practices:
```markdown
## Best Practices

- Always run `make verify` before committing
- Keep test coverage above 80%
- Update CHANGELOG.md with every release
- Follow conventional commit format (see commit-messages.md)
- Never commit secrets or credentials
```

### 6. Reference Related Standards

Link to other standard documents:
```markdown
## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md) for development guidelines.

- **Commit Messages**: Follow [commit message standards](./commit-messages.md)
- **Code Review**: See [development standards](./CONTRIBUTING.md#code-review)
- **Architecture**: Review [architecture docs](./docs/architecture/)
```

### 7. Validate README Completeness

**Quality checklist:**
- [ ] All 11 essential sections present
- [ ] Commands are tested and work correctly
- [ ] No hardcoded secrets or credentials
- [ ] Links are valid and up-to-date
- [ ] Code examples are accurate
- [ ] Platform-specific instructions included
- [ ] Prerequisites clearly listed with versions
- [ ] Troubleshooting section for common issues (if applicable)

### 8. Keep README Maintainable

**Best practices:**
- Keep it concise - link to detailed docs instead of duplicating
- Test all documented commands
- Update with breaking changes immediately
- Use relative links for repo files
- Include "Last Updated" date if helpful
- Place README at repository root

## Examples

### Minimal Go Project README

```markdown
# Project Name

Brief one-line description of what this project does.

## Prerequisites

- Go 1.25+
- Make

## Installation

\```bash
git clone <repo-url>
cd <project-name>
make deps
\```

## Running Tests

\```bash
make test              # 80%+ coverage required
make verify            # Complete validation
\```

## Usage

\```bash
make build
./bin/<binary-name>
\```

## Documentation

- [Architecture](./docs/architecture.md)
- [Contributing](./CONTRIBUTING.md)
- [Changelog](./CHANGELOG.md)

## Contact

- Team: [Team Name]
- Issues: [GitHub Issues URL]
```

### README with Configuration Example

```markdown
## Configuration

Create a `.env` file or set environment variables:

\```bash
# Backend Configuration
BACKEND_TYPE=azure           # Options: local, azure
STORAGE_ACCOUNT=myaccount    # Required for Azure
CONTAINER_NAME=tfstate       # Required for Azure
STATE_PATH=prod.tfstate      # Path within backend

# Optional Settings
LOG_LEVEL=info               # Options: debug, info, warn, error
PORT=50051                   # gRPC port (default: auto-assign)
\```

See [.env.example](./.env.example) for complete configuration options.
```

## Best Practices

### Do's ✅
- Start with the essential 11 sections
- Include working, tested commands
- Provide concrete examples
- Link to detailed documentation
- Keep it updated with code changes
- Use clear, imperative language
- Test all instructions as a new user would

### Don'ts ❌
- Don't include actual secrets or credentials
- Don't duplicate extensive documentation (link instead)
- Don't use vague instructions ("install dependencies")
- Don't forget to update after breaking changes
- Don't assume prior knowledge without prerequisites
- Don't leave outdated information
- Don't make it too verbose

## Troubleshooting

**Issue**: README is too long and overwhelming
**Solution**: Move detailed content to docs/ folder and link from README

**Issue**: Commands don't work on different platforms
**Solution**: Include platform-specific instructions or use cross-platform tools

**Issue**: README gets outdated quickly
**Solution**: Add README updates to your PR checklist and CI validation

## Resources

- [README Guidelines](https://github.com/autonomous-bits/development-standards/blob/main/readme-guidelines.md)
- [Project Structure Standards](https://github.com/autonomous-bits/development-standards/blob/main/project-structure.md)
- [Go Development Standards](https://github.com/autonomous-bits/development-standards/blob/main/go/general.md)
- [Commit Message Standards](https://github.com/autonomous-bits/development-standards/blob/main/commit-messages.md)
