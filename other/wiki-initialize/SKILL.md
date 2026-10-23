---
name: wiki-initialize
description: Create or adopt a user-controlled Yarbrain Markdown vault and configure lifecycle hooks to find it. Use when setting up Yarbrain, moving its vault, or repairing a missing vault structure; do not use for routine capture or maintenance.
---

# Initialize a Yarbrain Wiki

Create the canonical vault only at a location the user approves. Never initialize
or reconfigure a vault as an implicit side effect of installing the plugin.

## Workflow

1.  Confirm the vault path, whether it is personal or shared, and whether an
    existing directory must be adopted without overwriting content.
2.  Confirm authority to write the Yarbrain config. Its default location is
    ~/.config/yarbrain/config.json; YARBRAIN_CONFIG can select another file.
3.  Resolve ../../scripts/yarbrain.py relative to this SKILL.md and run:

        python3 <helper> init <vault-path>

    Use --config only for an explicitly selected config path. Use
    --no-write-config when the user wants a vault without automatic hooks.

4.  Verify that the command preserved existing files and created INDEX.md plus
    episodes/, notes/, skills/, inbox/, archive/, reports/, and .cache/.
5.  Run the helper's lint command against the configured vault.
6.  Report the vault and config paths, whether hooks can now find the vault, and
    any existing content that still needs adoption work.

The vault owns canonical Markdown. The config only locates it. Search indexes,
session queues, and plugin installation directories are not canonical knowledge.

Do not import transcripts, create semantic notes, enable network access, or
replace an existing index during initialization.
