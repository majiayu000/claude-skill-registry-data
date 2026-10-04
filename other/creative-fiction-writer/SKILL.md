---
name: creative-fiction-writer
description: Fiction writing workflow — novel, memoir, short story — vault files + Writing Engine visual UI + Claude as the drafting brain. Use when the user says "work on my novel", "draft a chapter", "fiction", "memoir", or continues an existing manuscript. NOT for non-fiction articles and posts (use the writing-editor app / eos-devlog-publish) or defining the target reader (use eos-communication-define-your-reader).
---

# Fiction Writer

Structured creative writing using **Obsidian files** (source of truth) + **Writing Engine UI** (visual workspace) + **Claude Code** (full-context AI) + **Voice API** (hands-free dictation & TTS).

## Reference files (read on demand)

`SKILL_DIR` = `{home}/.claude/skills/creative-fiction-writer/`. The harness loads only this file; read a sibling with the Read tool when you reach the step that needs it.

| File | Priority | Read when |
|---|---|---|
| `<SKILL_DIR>/fiction-memory.md` | Required | Always, first — active projects, last-session state, accumulated craft notes |
| `<SKILL_DIR>/templates.md` | Required | Scaffolding a project or writing any brief / outline / progress / scene / character / world / `_project.yml` file |
| `<SKILL_DIR>/writing-engine.md` | Optional | Launching or explaining the Writing Engine UI, or the tool architecture |
| `<SKILL_DIR>/voice-mode.md` | Optional | The user wants voice writing — dictation, command mode, conversation, or TTS proof-listening |

**Always read `<SKILL_DIR>/fiction-memory.md` first** — it holds active projects, last-session state, and accumulated craft notes.

## Reference

- **Memory**: `<SKILL_DIR>/fiction-memory.md`
- **Writing Engine**: `10_Projects/writing-engine/` (web UI on port 7800)
- **Projects**: `10_Projects/<Title>/` (each novel/memoir/story is a project folder)

### Three AI Brains, Three Strengths

| Tool | Best For | Context |
|------|----------|---------|
| **Claude Code** (terminal) | Full-context drafting, continuity checks, structural revision | Reads entire project |
| **Voice API** (mic button) | Hands-free scene generation, dictation, TTS proof-listening | UI packages context into system_prompt |
| **Writing Engine AI panel** (Ollama/OpenAI) | Quick in-editor actions: expand, compress, grammar | Current scene + codex selection |

Tool architecture + ASCII diagram: `<SKILL_DIR>/writing-engine.md`.

---

## Trigger Table

| User Says | Mode | Action |
|-----------|------|--------|
| "写小说" / "new novel" / "start a novel" | `new-project` | Scaffold novel project |
| "写回忆录" / "new memoir" | `new-project` | Scaffold memoir project |
| "写短篇" / "new short story" | `new-project` | Scaffold short story project |
| "写大纲" / "outline" / "plan the story" | `outline` | Create/refine story outline |
| "写场景" / "draft scene" / "write next scene" | `draft` | Write scene with full context |
| "扩展" / "expand this" | `revise:expand` | Expand passage with detail |
| "压缩" / "compress" | `revise:compress` | Tighten prose |
| "对话润色" / "dialogue pass" | `revise:dialogue` | Improve dialogue voice |
| "文风统一" / "voice pass" | `revise:voice` | Consistent narrative voice |
| "连续性检查" / "continuity check" | `continuity` | Check consistency |
| "角色档案" / "new character" | `character` | Create/update character |
| "世界设定" / "worldbuilding" | `world` | Create/update world note |
| "组装章节" / "assemble chapter" | `assemble` | Compile scenes → chapter |
| "项目状态" / "story status" | `status` | Progress report |
| "打开写作界面" / "open writer" / "writing UI" | `ui` | Launch Writing Engine |
| "语音写作" / "voice mode" / "talk to write" | `voice` | Activate voice mode in UI |
| "读给我听" / "read it back" / "TTS" | `voice:tts` | TTS playback of current scene/chapter |

Project scaffolds + all note templates: `<SKILL_DIR>/templates.md`.

---

## Core Workflow

```
new-project → outline → [DRAFT LOOP] → assemble → revision passes
```

### Draft Loop (per scene)

```
1. Claude reads context (see Context Loading Protocol)
2. Claude drafts scene → writes to manuscript/<path>.md
3. User reviews in Writing Engine UI or Obsidian
4. User annotates / requests changes via Claude Code
5. Claude revises
6. Every 3-5 scenes: continuity check
7. Update _progress.md
```

---

## Context Loading Protocol

**Before writing ANY scene**, Claude MUST read (in order):

1. **`_brief.md`** — premise, themes, tone, audience
2. **`_outline.md`** — find the current scene's beat/purpose
3. **`_progress.md`** — what's done, open threads, continuity flags
4. **Previous 2 scenes** — for continuity and flow
5. **POV character file** — voice, speech patterns, arc position
6. **Other characters in scene** — relationships, tensions
7. **Relevant world file** — if new setting introduced

This is what makes Claude Code superior to the Writing Engine's generic AI panel: **every scene is written with full project context**.

### Context Loading — Quick Reference

```
READ _brief.md          → tone, themes
READ _outline.md        → this scene's beat
READ _progress.md       → what's happened, open threads
READ prev 2 scenes      → continuity, voice
READ character files    → POV voice, relationships
READ world files        → setting details (if needed)
```

---

## Mode Details

### `new-project`

1. Ask user for: title, type (novel/memoir/short), premise, language
2. Create project folder in `10_Projects/<Title>/`
3. Scaffold all folders and template files
4. Create `_project.yml` for Writing Engine compatibility
5. Write initial `_brief.md` from user's premise
6. Update `fiction-memory.md` with new active project

### `outline`

1. Read `_brief.md` for premise and themes
2. Propose act/chapter structure with scene beats
3. Iterate with user until outline is solid
4. Write to `_outline.md`
5. Generate initial `_progress.md` scene table

### `draft`

1. **Execute full Context Loading Protocol** (see above)
2. Identify next scene from `_progress.md` (or user specifies)
3. Write scene matching: outline beat, character voice, tone, previous flow
4. Save to `manuscript/<path>/<scene>.md`
5. Update `_progress.md` (status → draft, word count)

### `revise:expand`

Read the scene, expand thin passages with:
- Sensory detail (sight, sound, smell, touch, taste)
- Internal thought (for POV character)
- Environmental texture
- Micro-actions and body language

### `revise:compress`

Read the scene, tighten by:
- Removing redundant descriptions
- Cutting filler words and phrases
- Combining sentences where possible
- Preserving voice and key imagery

### `revise:dialogue`

Read the scene + all character files for characters present:
- Make each character sound distinct
- Remove "said" synonyms overuse
- Add subtext (what's unsaid)
- Ensure dialogue advances plot or reveals character

### `revise:voice`

Read `_brief.md` tone notes + sample of earlier scenes:
- Flag voice inconsistencies
- Normalize POV distance
- Harmonize tense usage
- Suggest specific fixes

### `continuity`

Scan recent 3-5 scenes + character files + world files:
- **Character consistency**: behavior matches profile? contradictions?
- **Timeline**: chronological logic? impossible overlaps?
- **Plot threads**: which are open? any dropped?
- **Setting details**: physical descriptions consistent?
- **Tone/voice**: has narrative voice drifted?

Output: Update `_progress.md` with findings under "Continuity Flags"

### `character`

1. Ask: name, role, want/need/flaw/arc
2. Create file in `characters/` (or `people/` for memoir)
3. Link to relevant scenes in outline
4. If updating existing: read current file, preserve existing info, add new

### `world`

1. Ask: name, type, description, rules, significance
2. Create file in `world/` (or `places/` for memoir)
3. Link to scenes where it appears

### `assemble`

1. Read all scenes for target chapter (sorted by scene number)
2. Check transitions between scenes
3. Add chapter-level framing if needed
4. Calculate chapter word count
5. Write assembled chapter to `revisions/ch01-assembled.md`

### `status`

Report on demand:
- Total word count (by chapter/act)
- Scene completion status (draft/revised/final)
- Open plot threads
- Character appearance tracker
- Continuity flags
- Estimated completion %

### `ui`

Launch the Writing Engine:
```bash
cd "10_Projects/writing-engine" && python server.py &
```
Then open `http://localhost:7800` in browser.

**Note**: The Writing Engine reads from `10_Projects/` — it sees the same files Claude Code writes.

---

Writing Engine UI details: `<SKILL_DIR>/writing-engine.md`.
Voice mode (dictate / command / conversation + TTS): `<SKILL_DIR>/voice-mode.md`.

---

## Writing Principles

These guide Claude's drafting and revision:

1. **Show, don't tell** — action and sensory detail over abstract statements
2. **Character voice distinction** — each character sounds different
3. **Scene purpose** — every scene must advance plot OR reveal character (ideally both)
4. **Tension on every page** — conflict, mystery, or emotional stakes
5. **Specific over general** — "a cracked blue mug" not "a cup"
6. **Subtext in dialogue** — what's unsaid matters more
7. **End scenes with forward momentum** — reader wants to turn the page

---

## Post-Action

After any mode execution:
1. Update `_progress.md` if scene status changed
2. Update `<SKILL_DIR>/fiction-memory.md` whenever a project changes (new or active project, phase/status shift) or a significant craft insight emerges — it is the durable memory across sessions
3. Report what was written/changed and next suggested action
