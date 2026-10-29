---
name: checkpoint-list
description: "Lists all saved checkpoints for the current project. Usage: /checkpoint-list"
---

# List Saved Sessions

1. Determine the current project: the basename of the git repository root (`git rev-parse --show-toplevel`), or of the working directory outside a repo, so subfolders of one repo share state.
2. Read the contents of the `~/.claude_states/<project>/` directory.
3. If the directory does not exist or is empty, output: "No session checkpoints found for this project."
4. If files exist, list them clearly as a bulleted list, stripping out the `.md` extension so only the session name is visible.
5. Ask me: "Which session would you like to load?"
6. Wait for my response. When I reply with a name, silently read that specific `~/.claude_states/<project>/<session_name>.md` file to restore your context, then confirm you are ready.
