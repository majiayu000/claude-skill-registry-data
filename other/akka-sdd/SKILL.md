---
name: akka-sdd
description: Use when working on Akka SDK projects, Akka Spec-Driven Development, or when the user asks for workflows equivalent to Claude commands such as /akka:specify, /akka:plan, /akka:tasks, /akka:implement, /akka:review, /akka:build, /akka:deploy, /akka:analyze, /akka:clarify, /akka:checklist, or /akka:issues.
---

# Akka Spec-Driven Development For Codex

Use the Akka CLI MCP server whenever its tools are available. The plugin registers the server with:

```json
{
  "command": "akka",
  "args": ["mcp", "serve", "--disable-prompt"]
}
```

Before using an Akka SDD workflow, verify the MCP server is available by listing MCP tools/resources. If Akka MCP tools are unavailable, tell the user to confirm the plugin is installed/enabled and that `akka mcp serve --disable-prompt` starts from the repo root.

## Project Rules

- Follow the repository `AGENTS.md` instructions for Akka SDK component architecture, package layout, tests, and documentation reads.
- Prefer Akka MCP tools for spec files, task generation, branch helpers, and Akka CLI operations.
- Use local `akka-context/` documentation before coding first-time Akka component types.
- For CLI commands run directly from Codex, use non-interactive flags where available: `--disable-prompt`, `--output json`, and explicit context/config options when relevant.

## Claude Command Mapping

- `/akka.specify`: create or update a feature specification. Use Akka MCP spec tools first, then create or update `specs/<number>-<short-name>/spec.md`.
- `/akka.plan`: create the technical plan from the selected spec. Use Akka MCP template/spec tools, then produce `plan.md`, `research.md`, `data-model.md`, contracts, and quickstart artifacts as needed.
- `/akka.tasks`: derive actionable tasks from the plan and write `tasks.md`.
- `/akka.implement`: execute `tasks.md` on the feature branch, preserving user changes and verifying with Maven tests.
- `/akka.review`: review implementation against the spec, plan, tasks, and Akka SDK rules.
- `/akka.build`: build, test, and run the Akka service locally.
- `/akka.deploy`: use Akka CLI deployment commands only after confirming target project, region, service name, and credentials.
- `/akka.analyze`: inspect an existing Akka project and report architecture, components, gaps, and risks.
- `/akka.clarify`: identify unresolved requirements and update the spec only after user answers.
- `/akka.checklist`: create or update quality checklists for the active spec.
- `/akka.issues`: summarize open spec, plan, task, build, and review issues.

## MCP Usage Expectations

When MCP tools exist, prefer typed MCP calls over shelling out to `akka` for the same operation. When shelling out is required:

```powershell
akka --disable-prompt --output json <command>
```

Use text output only when the user asks to see human-readable CLI output.
