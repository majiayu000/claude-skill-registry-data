---
name: callesnikov-understand-anything-forked
description: Codex App adapter for the Understand Anything fork. Use when Codex needs to analyze, explain, onboard, chat with, diff-review, visualize, research external technical or domain context for, or build knowledge graphs from a codebase, docs repository, wiki, or knowledge base using the bundled Understand Anything architecture, agents, scripts, dashboard, and prompts.
---

# Callesnikov-Understand-Anything-Forked

Use this as the Codex App entrypoint for the bundled upstream Understand Anything plugin.

The upstream project is preserved inside this skill folder. Do not rewrite or simplify the internal prompts, agents, scripts, package layout, hooks, or dashboard architecture unless the user explicitly asks to modify the fork. Treat this file and `agents/openai.yaml` as the Codex compatibility layer.

## Upstream Layout

- Original plugin root: `understand-anything-plugin/`
- Original Claude skill prompts: `understand-anything-plugin/skills/*/SKILL.md`
- Original agent prompts: `understand-anything-plugin/agents/*.md`
- Original hooks: `understand-anything-plugin/hooks/`
- Original source packages: `understand-anything-plugin/packages/`
- Original top-level docs, tests, install scripts, and homepage are kept at this skill root.

When an upstream prompt mentions Claude plugin paths, `~/.agents/skills/understand`, slash commands, or Claude-specific plugin caches, translate that operationally for Codex by resolving paths under this skill directory. The plugin root is:

```text
<this skill>/understand-anything-plugin
```

## Route Requests

Before acting, read the matching upstream `SKILL.md` and follow it as the source of truth:

| User intent | Read this upstream prompt |
| --- | --- |
| Analyze a codebase and build a structural knowledge graph | `understand-anything-plugin/skills/understand/SKILL.md` |
| Ask questions against an existing graph | `understand-anything-plugin/skills/understand-chat/SKILL.md` |
| Launch or explain the dashboard workflow | `understand-anything-plugin/skills/understand-dashboard/SKILL.md` |
| Review git diffs, PRs, affected components, and risks | `understand-anything-plugin/skills/understand-diff/SKILL.md` |
| Extract business-domain knowledge from a codebase | `understand-anything-plugin/skills/understand-domain/SKILL.md` |
| Explain a file, function, module, or subsystem | `understand-anything-plugin/skills/understand-explain/SKILL.md` |
| Analyze a Karpathy-pattern LLM wiki or knowledge base | `understand-anything-plugin/skills/understand-knowledge/SKILL.md` |
| Generate onboarding material for a project | `understand-anything-plugin/skills/understand-onboard/SKILL.md` |
| Research external technical or domain context needed to understand the project | `understand-anything-plugin/skills/understand-research/SKILL.md` |

If the user gives a slash command such as `/understand`, `/understand-dashboard`, `/understand-chat`, `/understand-diff`, `/understand-domain`, `/understand-explain`, `/understand-knowledge`, `/understand-onboard`, or `/understand-research`, map it to the corresponding prompt above and treat the rest of the line as the command arguments.

When another mode reaches a material uncertainty that requires current external evidence, read `understand-research/SKILL.md` in addition to the primary mode. Keep local analysis in the primary mode and apply the research mode only to the unresolved external questions.

## Codex Execution Notes

- Preserve upstream artifacts and outputs such as `.understand-anything/knowledge-graph.json`.
- Use Codex shell tools for the deterministic Node and Python scripts referenced by upstream prompts.
- Use Codex subagents or parallel work only when available and appropriate; otherwise perform the same analysis directly while preserving the upstream phase structure and output contracts.
- Use `understand-research` only for external evidence that materially improves understanding of the current codebase, dependency, standard, architecture decision, or domain. Do not turn unrelated general-interest research into a repository workflow.
- Prefer bundled upstream prompts over summaries in this adapter. This file exists to route and adapt paths, not to replace the original behavior.
- The upstream project expects Node.js >= 22 and pnpm >= 10 for full build and dashboard workflows.

## Validation

For skill-format validation, this top-level `SKILL.md` is the Codex-discoverable skill. Nested upstream `SKILL.md` files remain original Claude prompts and are loaded on demand as bundled resources.
