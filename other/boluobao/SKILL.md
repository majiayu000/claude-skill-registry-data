---
name: boluobao
description: Plan and create warm-paper, ink-and-colored-pencil editorial illustrations, social covers, creator-introduction cards, multilingual handwritten notes, identity-preserving pet portraits, image reconstructions, food, people, scenes, landscapes, landmarks, charts, and compact tables. Use when a user asks for boluobao, article illustrations, a social cover, a creator profile visual, a handwritten visual, a pet-photo reconstruction, a warm journal-like redesign, or phrases such as “为我的内容进行配图”, “为这篇文章生成封面”, “做一张个人介绍图”, or “帮我将这个图片用 boluobao 进行设计”.
---

# Boluobao for Claude Code

This file is the Claude Code project bridge. The repository root remains the single source of truth so Codex and Claude Code cannot drift into different visual systems.

1. Read the canonical [SKILL.md](../../../SKILL.md) completely before acting.
2. Resolve every relative link in the canonical file against the repository root, then read only the references required for the active mode.
3. Follow the canonical planning, generation, correction, quality-scoring, naming, and final-only delivery contract without weakening it.

## Claude Code runtime adaptation

- Use an image-generation or image-editing tool configured in the current Claude Code environment when the task requires pixels.
- If no compatible image tool is available, complete the content map, composition brief, locked text, production prompt, and verification plan, then clearly state that image execution was not performed. Never invent a generated file or path.
- Treat `agents/openai.yaml` as Codex-only interface metadata. It does not modify the visual rules.
- Keep accepted final artwork outside the installed Skill directory and do not retain candidate or correction images.

Invoke explicitly with `/boluobao`, or let Claude Code select the Skill automatically from the description above.
