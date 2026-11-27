---
name: gitignore
description: Creates or refreshes .gitignore from gitignore.io templates and keeps the project block. Use when the user asks for a .gitignore, or the stack of the repository changes.
---

# .gitignore from gitignore.io

gitignore.io keeps the standard ignore rules for each language, editor, and operating system. Rules that people
write by hand become out of date and miss files.

The project-specific rules are different. They protect secrets and local state, and a careless regeneration can
delete them without a sign. Thus this skill never writes the whole file. It replaces one marked block and keeps
all other lines.

## File shape

```gitignore
# >>> gitignore.io generated — do not edit by hand >>>
...rules from gitignore.io...
# <<< gitignore.io generated <<<

# === project-specific — never regenerated, must stay last ===
.local-state/
!.env.example
```

**The project block must be last.** git uses the last rule that matches. The templates contain their own `.env`
rules. If the generated block came after a `!.env.example` rule, git ignores `.env.example` again. The order is a
correctness rule.

## Usage

The template list is a **parameter**: a comma-separated list of gitignore.io template names. Choose it from the
tools that the repository uses (examples: `python,macos,visualstudiocode`; `node,macos,jetbrains`; `go,linux`).
Ask the project: look at the files in the repository, and read the last list in the project block comment or in
`AGENTS.md` if it records one. If you cannot decide, ask the user once.

```bash
"${CLAUDE_PLUGIN_ROOT:-<directory of this skill>/../..}/skills/gitignore/scripts/sync-gitignore.sh" "<templates>" [path-to-.gitignore]
```

Find the script relative to the directory of this skill (the harness gives the base directory when it loads the
skill). `CLAUDE_PLUGIN_ROOT` is set when the skill is part of a plugin.

To find a template name, search the list:

```bash
curl -s https://www.toptal.com/developers/gitignore/api/list | tr ',' '\n' | grep -i <term>
```

Add a template only for a tool that the repository or the team uses. Each unused template adds lines that a
reader must read. Write the chosen list in the report, so that the next refresh uses the same list.

## Rules

1. **Do not write the whole file.** The script replaces only the marked generated block.
2. **Do not remove a project rule.** If a project rule is the same as a generated rule, keep it. An explicit rule
   is documentation.
3. **The script fails without a write.** A network error or a truncated response does not change the file. The
   script checks that the response starts with the gitignore.io header.
4. **Put negations (`!` rules) in the project block.** They depend on the order, and the order is fixed there.
5. **A slash that is not at the end anchors the rule to the root.** `.tool/cache` matches only `./.tool/cache`.
   Write `**/.tool/cache` for any depth.
6. **A second run changes nothing** when the templates did not change. Check this with a second run and
   `git diff`.

## After a run

Check that the important rules still work. Do not assume it. The project `AGENTS.md` section `## Secrets` names
the files that tools must never read. If a guard refuses a command that names an env file, check the other paths
yourself and ask the user to run the env checks:

```bash
git status --short --ignored -- <local state folders>   # agent: !! means ignored
git check-ignore -v <secret file>                        # user: expect the secret rule
git status --short --ignored -- <env example file>       # user: expect ?? (not ignored)
```

`git check-ignore` exits with 0 when any pattern matches, also a negation. Read the rule that it shows, or use
`git status` as above.
