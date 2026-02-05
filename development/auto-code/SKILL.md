---
name: auto-code
description: Run an autonomous coding agent that builds applications from specifications. Use when asked to "build an app autonomously", "run autonomous agent", or "create application from spec".
allowed-tools: Bash(python*), Bash(pip*), Read, Glob
---

# Autonomous Coding Agent Skill

Build complete applications from specification files using a multi-session autonomous agent.

## Usage

Invoke with a spec file path:
```
/auto-code --spec ./path/to/spec.txt
```

With additional options:
```
/auto-code --spec ./spec.txt --project-dir ./output --max-iterations 10
```

## How It Works

This skill invokes the `auto-code` Python package to:
1. Read your application specification
2. Create a feature list with 200+ test cases
3. Implement features one by one with browser-based verification
4. Continue across sessions until all features pass

## Prerequisites

The package must be installed from source:
```bash
# Clone and install
git clone https://github.com/AhamSammich/auto-code.git
cd auto-code
pip install -e .
```

Authentication is required - set one of:
- `ANTHROPIC_API_KEY` - API key from console.anthropic.com
- `CLAUDE_CODE_OAUTH_TOKEN` - OAuth token (run `claude setup-token`)

## Invocation

When this skill is triggered, run the following command:

```bash
auto-code --spec <spec_path> --project-dir <project_dir>
```

Replace `<spec_path>` with the user's specification file path.
Replace `<project_dir>` with the desired output directory (default: ./autonomous_project).

## Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `--spec` | Yes | Path to the application specification file |
| `--project-dir` | No | Output directory for the project (default: `./autonomous_project`) |
| `--max-iterations` | No | Maximum agent iterations (default: unlimited) |
| `--model` | No | Claude model to use (default: `claude-sonnet-4-5-20250929`) |

## Security

The agent runs in a sandboxed environment with:
- Filesystem access restricted to the project directory
- Bash commands limited to a safe allowlist
- No ability to modify security settings
