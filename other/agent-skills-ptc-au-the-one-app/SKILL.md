---
name: agent-skills
description: Read before giving a device the network's skills, so its agent tools (Claude Code, Codex, OpenCode, Amp) have them without connecting, or when a skill there named for the network looks wrong or is missing.
metadata:
  title: "Agent Skills"
  subtitle: "Your AI's skills, on every device"
  about: "Gives the AI tools on your devices, like Claude Code and Codex, what they need to use your apps here, even when they aren't connected. It keeps them up to date as your apps change."
  category: AI
---

It puts a skill for each app its person can use, and One Core's own, where every agent tool on a device reads
skills: `~/.claude/skills` and `~/.agents/skills`, wherever the tool's folder is there. Each is named for the
network and the app, `<network>-<app>`, the network being its address in kebab case (`one-example-com-gmail`),
and one named for the network alone lists them. It's what an app's skill says, as `skill://` serves it, so it's
changed where the app is.

A device gets them once its service is installed there: `install_service --app agent-skills --service
AgentSkills.Writer --server <key>`. Installed for a person, it writes theirs into the home folder of the user that
device's server runs as, as it starts and every minute: an app installed, updated or removed, or an agent tool
installed later, is there within the minute.

Each folder it writes has a `.agent-skills` file in it, saying which network's it is; it rewrites only those, and
removes one whose app is gone. A folder without it is left alone: delete that file to take a folder over.
