---
name: memory-promote
disable-model-invocation: true
description: Audit this repo's auto-memory files and suggest promoting each one to a more persistent layer — user or repo CLAUDE.md, an existing or new skill, a settings.json hook, or a checked-in reference doc. Use when the user says "audit memory", "promote memory", "clean up memories", "memory-promote", or wants to move ephemeral memory into durable config.
allowed-tools: Bash(ls:*), Bash(find:*), Bash(grep:*), Bash(cat:*), Bash(realpath:*), Bash(pwd:*), Read, Edit, Write
---

# Memory Promote

Auto-memory under `<config-dir>/projects/<encoded-cwd>/memory/` is per-conversation context, not durable config. Many memories belong in a more persistent layer where they apply consistently and survive memory pruning. This skill scans memories and proposes a target layer for each.

`<config-dir>` is `$CLAUDE_CONFIG_DIR` when set, otherwise `~/.claude`. Resolve it once at the start and use it everywhere below.

## Scope

The current repo. Memory dirs encode the absolute cwd with `/` replaced by `-`:

- `/home/alex/work/api` → `<config-dir>/projects/-home-alex-work-api/memory/`

Compute `MEM_DIR="$CONFIG_DIR/projects/$(pwd | tr / -)/memory"`. If it doesn't exist, report "no memories for this repo" and stop.

If the user asks for something wider or narrower in their own words — another repo, every project, only the cross-cutting ones, just list them without suggestions — honor it using the same encoding. Don't invent flags for it; the report-then-confirm loop below already gives them control.

## Steps

1. **List memories.** `find "$MEM_DIR" -type f -name '*.md' ! -name 'MEMORY.md'`. For each file, read the frontmatter and body. Memory frontmatter looks like:

   ```yaml
   ---
   name: coolify-deploy
   description: Deployment coordinates for the app
   metadata:
     node_type: memory
     type: project
     originSessionId: <uuid>
   ---
   ```

   The classification key is `metadata.type` (commonly `user`, `project`, `feedback`, `reference`). If it is absent, infer the type from the body.

2. **Classify each memory** using the table below.
3. **Render report** — one row per memory: file, type, current content (1-line summary), → suggested target, rationale, concrete action.
4. **Wait for user confirmation** before changing anything — promotion is a judgment call, so confirm per-item even when the user asked to just apply everything.
5. **On confirm:** perform the action (edit CLAUDE.md, invoke `/cc:skill-creator`, add the hook to `settings.json`, write a reference doc), then **delete the memory file and its line in `MEMORY.md`**.

## Promotion targets

| Memory pattern                                                   | Promote to                                  | Why                                                  |
| ---------------------------------------------------------------- | ------------------------------------------- | ---------------------------------------------------- |
| `type: user` (role, stack, voice, naming)                        | user-level `CLAUDE.md`                      | Applies across all projects, not just one            |
| `type: feedback` — stable preference, repo-specific              | repo `CLAUDE.md`                            | Survives memory pruning, visible to teammates        |
| `type: feedback` — "never run X" / "X is human-only"             | `settings.json` PreToolUse deny hook        | Harness enforces; can't be forgotten                 |
| `type: feedback` — repeatable workflow ("always do X before Y")  | new skill (via `/cc:skill-creator`) or hook | Skill makes it discoverable; hook makes it automatic |
| `type: project` — durable fact (versioning scheme, release flow) | repo `CLAUDE.md`                            | Onboarding context, not session state                |
| `type: project` — current sprint/incident/deadline               | **keep in memory**                          | Genuinely ephemeral — memory is the right layer      |
| `type: reference` — internal URL, dashboard, doc page            | repo `CLAUDE.md` "References" section       | Checked in, shared with team                         |
| Pattern already covered by an installed skill                    | point to that skill, delete memory          | The skill already encodes it                         |
| Build/test command quirks                                        | repo `CLAUDE.md` "Development Workflow"     | Lives next to the code that needs it                 |

## Heuristics

- **Cross-repo applicability test:** would this memory be useful in any other repo? → user-level `CLAUDE.md`. Only this one? → repo `CLAUDE.md`.
- **Enforcement test:** is the memory a _prohibition_ ("never run X")? → hook beats prose. Memory/CLAUDE.md is a request; a hook is a guarantee.
- **Existing-skill test:** before suggesting a new skill, look for overlap in `<config-dir>/skills/`, the repo's `.claude/skills/`, and installed plugin skills. Prefer pointing at an existing skill over creating another one.
- **Ephemeral test:** does it name a person, sprint, date, or in-flight ticket? → leave it in memory.

## Output format

Print a numbered list. Per item:

```
[N] <memory-file> (type: <type>)
    Current: "<one-line summary of body>"
    → Promote to: <target>
    Why: <one sentence>
    Action: <exact edit / command to run>
```

After the list, ask "Which to promote? (numbers, `all`, or `none`)". Then act on the selected items one at a time.

## Notes

- Don't auto-delete a memory unless its content is fully captured at the new location.
- When editing a `CLAUDE.md`, append under an existing relevant section if one exists; only create new sections when needed.
- For hook proposals, defer to the built-in `/update-config` skill when it is available — it knows the settings schema. Otherwise edit `settings.json` directly and show the diff before writing.
- For skill proposals, defer to `/cc:skill-creator` — it knows the SKILL.md format.
- After promotion, also remove the entry from the `MEMORY.md` index in the same memory dir.
