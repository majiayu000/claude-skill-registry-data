---
name: skill-resolver
description: Resolve Claude/Codex skill files by name when neither the user nor the current session catalog identifies the artifact. Use for unresolved name-only lookup or resolver ambiguity; not when an exact path or a catalog root-alias mapping already identifies the requested skill.
---

# Skill Resolver

Use the resolver for name-only lookup when the requested file is not already
identified. Honor an exact path or the current session's supplied skill catalog,
including its root-alias mapping; do not replace that identity with a same-named
file found elsewhere. The resolver locates and prints skill files; it does not
install, edit, or synchronize skills.

## Workflow

1. Skip the resolver when an exact `SKILL.md` path is already supplied by the user or session catalog. Expand catalog aliases using that catalog's mapping.
2. Choose the lookup scope: use `--tool codex` in Codex, `--tool claude` in Claude Code, and `--tool any` only when comparing paired copies or debugging tool-agnostic ambiguity.
3. Choose the lookup directory. Use the current working directory for the active project; pass `--cwd /path/to/project` when resolving a project-local skill for another workspace.
4. Run `path` to get the file path, `cat` to read the skill, `list` to inventory discovered files, `duplicates` to expose same-name copies, or `roots` to inspect the helper's search order. Check exit status before using stdout as a path or instruction body. Read the complete body before applying it.
5. If the resolver reports ambiguity or no match, inspect `list` and `roots` before continuing; do not substitute a likely-looking path.
6. For edits, resolve symlinks and use the canonical tracked source in the requested scope. Global dotfiles skills live under `claude/skills/<name>/` or `codex/skills/<name>/`; a project-local skill stays in that project's skill tree. Do not migrate a local skill globally or edit a managed plugin cache merely because a matching file was found. Keep intended Claude/Codex pairs synchronized except for intentional tool metadata or manifest-recorded divergences.

Command:

```bash
/Users/pablostafforini/My\ Drive/dotfiles/bin/agent-skill
```

Common operations:

```bash
/Users/pablostafforini/My\ Drive/dotfiles/bin/agent-skill path diagnose --tool codex
/Users/pablostafforini/My\ Drive/dotfiles/bin/agent-skill cat diagnose --tool codex
/Users/pablostafforini/My\ Drive/dotfiles/bin/agent-skill path diagnose --tool claude
/Users/pablostafforini/My\ Drive/dotfiles/bin/agent-skill list --tool codex
/Users/pablostafforini/My\ Drive/dotfiles/bin/agent-skill roots --tool codex
/Users/pablostafforini/My\ Drive/dotfiles/bin/agent-skill duplicates --tool codex
/Users/pablostafforini/My\ Drive/dotfiles/bin/agent-skill path skill-resolver --tool codex --cwd "/Users/pablostafforini/My Drive/dotfiles"
```

Rules:

- If neither the user nor session catalog identifies the file, resolve the name with `agent-skill` before guessing a path.
- Use `--tool claude` when operating in Claude Code and `--tool codex` when operating in Codex.
- The resolver's precedence is a lookup convenience, not a claim about either runtime's loading order or enabled skill catalog. It includes local compatibility/workspace sources; a discovered file may be disabled or unavailable in this session. Use the supplied session catalog or runtime inspection to establish availability.
- Honor `CODEX_HOME` and Claude's `CLAUDE_CONFIG_DIR` for the active account. Do not silently switch to another account to make a lookup succeed.
  `CLAUDE_HOME` is a legacy helper-only option, honored only when
  `CLAUDE_CONFIG_DIR` is unset.
- Codex lookup includes native `.agents/skills` project/user roots and
  `/etc/codex/skills`, alongside the local `.codex/skills` compatibility
  sources. Project-native roots stop at the nearest Git root.
- Claude plugin lookup uses enabled-plugin and installed-version records, not
  every directory left in a cache. A failed or malformed plugin inventory is
  incomplete discovery, not proof that no matching plugin is installed.
  Its enablement input is the account's `settings.json`; it does not reconstruct
  merged project/local/managed enablement policy. Project-scoped installation
  paths are filtered against `--cwd`.
- If the resolver reports ambiguity or no match, stop and investigate the skill inventory instead of substituting a likely-looking path.
- A successful lookup authorizes reading the requested artifact, not executing its workflow. Preserve explicit-only invocation policies while inspecting or auditing skills.

Native Codex locations were checked against the
[OpenAI skills documentation](https://learn.chatgpt.com/docs/build-skills)
on 2026-09-05. Local compatibility roots and lookup precedence remain specific
to this helper; check `roots` instead of assuming native runtime equivalence.
