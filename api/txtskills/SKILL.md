---
name: txtskills-llms-to-agent-skills
description: Convert docs base URLs, llms.txt, or llms-full.txt into installable Agent Skills with txtskills CLI. Use when a user asks to generate, publish, and optionally install a new skill from documentation.
compatibility: Requires Node.js 20+ and the latest txtskills CLI (`npx txtskills@latest`).
license: MIT
---

# txtskills: llms.txt → Agent Skills

Use this skill when you need to turn documentation into a reusable Agent Skill quickly.

## What this skill does

- Converts a docs URL into a published skill via `txtskills convert`
- Supports base URLs and explicit files:
  - `example.com`
  - `example.com/llms.txt`
  - `example.com/llms-full.txt`
  - `example.com/.well-known/llms.txt`
  - `example.com/.well-known/llms-full.txt`
- Can install immediately after conversion (interactive or auto)

## Quick start

```bash
npx txtskills@latest convert github.com/llms.txt
```

```bash
npx txtskills@latest convert docs.anthropic.com
```

## Recommended workflow

1. Convert from a docs URL.
2. Review generated skill name and GitHub URL.
3. Install immediately when prompted.
4. If content changed and skill exists, re-run with `--force`.

## Agent execution workflow (important)

When the user gives only a product name (for example: "Google AI Studio"), do this:

1. Discover candidate URLs by checking in this order:
   - `<domain>/llms.txt`
   - `<domain>/.well-known/llms.txt`
   - `<domain>/llms-full.txt`
   - `<domain>/.well-known/llms-full.txt`
2. If domain is unknown, search web for `"<product> llms.txt"` and `"<product> llms-full.txt"`.
3. Run conversion:
   - `npx txtskills@latest convert <best-url>`
4. If convert succeeds, offer immediate install.
5. If multiple valid sources exist, ask user to choose before publishing.

Example user intent this skill should handle:

- "Find Google AI Studio llms.txt and convert it to a txtskills skill"

## Command reference

```bash
npx txtskills@latest convert <url>
```

Options:

- `-n, --name <skill-name>`: set custom skill slug
- `-f, --force`: regenerate when skill already exists
- `--install`: auto-install after conversion
- `--skip-install`: skip install prompt
- `-g, --global`: install globally (when auto-installing)
- `-a, --agent <agents...>`: target specific agents
- `-y, --yes`: auto-confirm prompts
- `--json`: machine-readable output
- `--api <url>`: custom convert API base or full endpoint

## Naming guidelines

Use lowercase, hyphenated names (Agent Skills standard):

- ✅ `payment-docs`
- ✅ `ai-sdk`
- ❌ `PaymentDocs`
- ❌ `docs_skill`

## Troubleshooting

- If conversion fails, verify the docs site exposes `llms.txt` or `llms-full.txt`.
- If skill exists but docs changed, run with `--force`.
- If install is skipped, run:

```bash
npx txtskills@latest add <skill-name>
```

## Useful links

- txtskills web: https://txtskills.hari.works
- Skills registry: https://github.com/hk-vk/skills
- Agent Skills spec: https://agentskills.io/specification
- llms.txt spec: https://llmstxt.org
