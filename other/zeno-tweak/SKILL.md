---
name: zeno-tweak
description: "Add or remove zeno.zsh snippet shortcuts in $HOME/.config/zeno/config.yml. Use when: (1) User says 'zeno-tweak', (2) User wants to add or remove a zeno snippet shortcut."
user-invocable: true
argument-hint: <keyword> -> <command>  OR  del|remove <keyword>
---

# Zeno Tweak

Manage zeno.zsh snippet shortcuts in `$HOME/.config/zeno/config.yml`.

## Parse argument

- **Add mode**: `<keyword> -> <snippet command>` (e.g., `gst -> git status`)
- **Remove mode**: `del <keyword>` or `remove <keyword>` (e.g., `del gst`)

## Add mode

1. Read `$HOME/.config/zeno/config.yml`
2. If keyword already exists, ask user whether to overwrite
3. **Safety check**: Run `which <keyword>` and `type <keyword>` in Bash. If either finds a real binary, builtin, alias, or function, warn user with what it conflicts (e.g., "`cc` is `/usr/bin/cc` (C compiler)") and ask for confirmation before proceeding
4. Append new entry to `snippets:` list:

```yaml
  - name: <short description derived from the command>
    keyword: <keyword>
    snippet: <command>
```

5. Show the added entry

## Remove mode

1. Read `$HOME/.config/zeno/config.yml`
2. Find entry with matching keyword. If not found, report error
3. Remove the entry (the `- name:`, `keyword:`, and `snippet:` lines)
4. Show what was removed

## After modification

1. `cd $HOME/repos/p/dotconfigetc`
2. Run `/co push`
