---
name: project-orchestrator
description: Setup project repositories with industry-standard structure, configuration, and documentation for Rust, Python, or TypeScript/Vite/Astro projects. Use when users explicitly request to orchestrate, setup, or initialize a project with proper tooling, Docker configs, pre-commit hooks, linting, and README documentation. Creates complete project scaffolding with appropriate directory structure, configuration files, and deployment setup.
---

# Project Orchestrator

Set up project repositories following industry standards for Rust, Python, and TypeScript projects. Creates directory structure, configuration files, Docker setup, pre-commit hooks, and comprehensive README documentation.

## When to Use This Skill

Trigger this skill when the user explicitly requests to:
- "Orchestrate a project for [description] using [language/framework]"
- "Setup a [project type] project in [language]"
- "Initialize a [language] project with proper tooling"

## Workflow

### 1. Determine Project Type and Requirements

Ask the user:
- What language/framework? (Rust, Python, TypeScript/Vite/Astro)
- What type of project? (API, CLI tool, web app, data pipeline)
- Is Docker needed?
- Any specific deployment target? (GitHub Pages, Vercel, self-hosted)

### 2. Read Language-Specific Conventions

Based on project type, read the appropriate reference:
- Python: `references/python-conventions.md`
- Rust: `references/rust-conventions.md`
- TypeScript/Vite/Astro: `references/typescript-conventions.md`

### 3. Create Project Structure

Create the directory structure following language conventions from the reference file.

**Critical: Create in user's current working directory or ask where to create it.**

### 4. Generate Configuration Files

Use assets from `assets/` directory:

**For all projects:**
- `.gitignore` - Copy from `assets/gitignore-{language}.txt`
- `.pre-commit-config.yaml` - Copy from `assets/pre-commit-{language}.yaml`

**For Python:**
- `pyproject.toml` - Define project metadata, dependencies, and tool configs
- `Dockerfile` - Use `assets/Dockerfile-python.txt` as template if Docker needed
- `docker-compose.yml` - Use `assets/docker-compose.yaml` if Docker needed

**For Rust:**
- `Cargo.toml` - Define package metadata and dependencies
- `Dockerfile` - Use `assets/Dockerfile-rust.txt` as template if Docker needed
- `docker-compose.yml` - Use `assets/docker-compose.yaml` if Docker needed

**For TypeScript/Vite/Astro:**
- `package.json` - Define project metadata and scripts
- `tsconfig.json` - TypeScript configuration
- `vite.config.ts` or `astro.config.mjs` - Build tool configuration
- `.github/workflows/deploy.yml` - Use appropriate template from assets if deploying to GitHub Pages

### 5. Add Minimal Starter Code

Create basic starter files with minimal but functional code:
- Python: `src/project_name/main.py` with basic structure
- Rust: `src/main.rs` or `src/lib.rs` with basic structure  
- TypeScript: Appropriate entry files based on framework

**Do not implement full business logic** - just enough to demonstrate the structure.

### 6. Generate README

Read `references/readme-structure.md` for README guidelines, then create a comprehensive README following this structure:

1. **Title & Brief Description** (2-3 sentences)
2. **Context & Rationale** - Why this project exists, what problem it solves
3. **Installation** - Prerequisites and setup steps
4. **Running the Project** - How to start it
5. **API Endpoints / Interface** - Document the interface (API routes, CLI commands)
6. **Architecture & Technology Choices** - Stack and design decisions with rationale
7. **Configuration** - Environment variables, config options

**Style:**
- Direct and clear, no marketing language
- Explain actual tradeoffs in technology choices
- Provide concrete examples and commands
- Keep it scannable with headers and code blocks

## Configuration File Details

### Pre-commit Hooks

All projects get pre-commit hooks for:
- Trailing whitespace removal
- End of file fixing
- YAML validation
- Large file checking
- Language-specific linting and formatting

### Docker Files

When Docker is needed:
- Use multi-stage builds (especially Rust)
- Non-root user for security
- Optimize layer caching
- Keep final images small
- Include health checks for APIs

### Deployment Configs

For web projects deploying to GitHub Pages:
- Use appropriate workflow from assets
- Configure build command
- Set up artifact upload
- Configure Pages deployment

## Output

After creating the project structure, provide:
1. Brief summary of what was created
2. Next steps for the user:
   - How to install pre-commit: `pre-commit install`
   - How to run the project
   - Any environment variables to set
3. Link to created files if in outputs directory

## Examples

**Example 1: Python API**
```
User: "Orchestrate a REST API project using Python with FastAPI for a todo app"
Claude: [Creates Python project with FastAPI structure, Docker, pre-commit, README explaining todo API endpoints]
```

**Example 2: Rust CLI Tool**
```
User: "Setup a Rust project for a CLI tool that processes log files"
Claude: [Creates Rust project with clap for CLI, appropriate Cargo.toml, README explaining usage]
```

**Example 3: Astro Website**
```
User: "Initialize an Astro project for a portfolio site with GitHub Pages deployment"
Claude: [Creates Astro project with Tailwind, GitHub Actions workflow, README with deployment instructions]
```
