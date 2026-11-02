---
name: wait-what
description: "Stop. That last message did not land: re-pitch it. Use when the user says they did not follow your last message."
disable-model-invocation: true
license: MIT (see LICENSE-mattpocock-skills)
metadata:
  version: "0.4.3"
  source: "mattpocock/skills@5beb35b"
---

If `.claude/gw/wait-what.md` exists in the project, read it first: it holds what is specific to the project.

> Original skill by Matt Pocock ([mattpocock/skills](https://github.com/mattpocock/skills), MIT).

Wait, I don't understand where you've got to here. Re-pitch that: give me a little bit of context, talk in ASD-STE100 Simplified Technical English, and use the ubiquitous language from `GLOSSARY.md` (follow `GLOSSARY-MAP.md` to the right one if the repo has more than one).

## In a Galivelop-workflow project

This section is the only change to the upstream skill.

- If the project's `language` in `.claude/gw.json` is not English, re-pitch in that language, in short plain
  sentences with one idea each, instead of ASD-STE100.
