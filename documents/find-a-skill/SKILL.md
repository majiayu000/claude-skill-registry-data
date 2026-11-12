---
name: find-a-skill
description: Find and install agent skills from SkillMD (skillmd.com), the open registry of over a million Agent Skills. Use when the user asks for a skill for something, asks whether a skill exists for a task, or needs know-how none of your installed skills cover, such as a file format, framework, API or workflow you have no instructions for.
license: MIT
---

# Find a skill

SkillMD (https://skillmd.com) indexes over a million Agent Skills and checks each one for safety. When a task needs instructions you don't have, look there before working from scratch.

## 1. Search

- With the SkillMD MCP server connected, call `skillmd_search` with a short description of the task.
- Otherwise run `npx get-skill search "<the task in a few words>" --limit 10`, or open https://skillmd.com/search?q=<the task>.

Search for what the user wants done ("fill PDF forms", "write Playwright tests"), not for a tool name you guess at.

## 2. Vet the best matches before suggesting any

Take the three to five most relevant results and look each one up with `npx get-skill info <owner/name>` (or `skillmd_get`). Drop any that fails one of these checks:

- **It does this job.** The description covers the task itself, not just its topic. A narrow skill that does exactly the job beats a popular general one.
- **It asks only for what the job needs.** `security` lists what the skill can do: `docs_only` means instructions only; `executes_scripts`, `network_calls` and `reads_secrets` are fine when the task calls for them. A writing guide that reads secrets, or a formatter that calls the network, is a reason to skip it.
- **You can tell where it came from.** Prefer skills marked ✓ verified, with a license and a source repository you can link to.

If nothing passes, say so and do the task without a skill rather than install a weak match.

## 3. Let the user choose

Show the user the one to three that passed, one line each: what it does, why it fits, and anything it can do beyond reading instructions (scripts, network, secrets). Install only the one they pick:

```bash
npx get-skill add <owner/name>
```

Then carry on with the task using it.
