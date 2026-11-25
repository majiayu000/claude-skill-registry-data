---
name: ai-dna
description: Turn your own local ChatGPT, Claude Code, and Codex conversation history into a 4:5 AI DNA helix still and 12-second film. Use when someone asks to make or share their AI DNA from their chat history.
---

# Make my AI DNA

Edge turns your own AI conversations into a luminous helix: one rung per conversation and one dot per message. The default path uses only local files, Python packages, and ffmpeg. It makes no network or model call.

## Run

Install Python 3, ffmpeg, and the local Python packages:

```bash
python3 -m pip install numpy scipy pillow
ffmpeg -version
```

From this skill folder, pass every history source you have. ChatGPT accepts its export zip or `conversations.json`; Claude Code and Codex accept their session directory roots. Omit a source you do not have.

```bash
python3 scripts/make.py \
  --chatgpt ~/Downloads/chatgpt-export.zip \
  --claude-code ~/.claude/projects \
  --codex ~/.codex/sessions \
  --output ~/my-ai-dna
```

With no source flags, the script scans `~/.claude/projects` and `~/.codex/sessions`. ChatGPT exports need an explicit `--chatgpt` path. Repeat any source flag to include more paths. `--preview` creates a 540×675 still and the same 12-second film at 540×676 and 12 fps for a quicker review. The extra film pixel keeps H.264 dimensions even. Full output is 1080×1350 at 30 fps. Use a new or previously generated AI DNA output folder; the script refuses a nonempty folder it does not own. The still is `hero.png`; the film is `pure.mp4`. `dna.json`, frames, and a count/timing summary also stay in the chosen output folder.

For a quick first look:

```bash
python3 scripts/make.py --chatgpt ~/Downloads/conversations.json --preview --output ~/my-ai-dna-preview
```

The film features up to three of your longest conversations. To pick your own, create a local `stops.json` with one to three entries, each matching the start of a conversation title:

```json
[
  {"title":"My garden plan", "label":"The garden takes shape"},
  {"title":"Learning Spanish", "label":"A new language"}
]
```

Pass `--stops stops.json`. Labels and chronological era names are derived locally from your titles. No Federico-specific topic names or music are bundled.

## Privacy and extras

Titles can reveal private names, projects, and questions. Read the still and film before sharing them. `--hide-titles` replaces the visible stop and era labels with neutral labels; it is **off by default** so the personal story is visible. The local `dna.json` still contains titles, so do not publish that file unless you intend to share them. If you add a face, its raw frames are temporary and removed when the render ends. History text never leaves your laptop in the default workflow.

Add `--face ~/portrait.jpg` or `--face ~/short-face-video.mp4` for an optional 18-second `intro.mp4`. Center the face in a 4:5 crop; a simple oval mask draws it in message dots before they fly into the helix. Add `--music ~/music.mp3` to mix your own licensed audio into the films. Without it, films are silent. Add `--skip-film` to generate just data and a still. For existing locally extracted conversations, `--conversations-jsonl path` accepts the normalized format produced by `scripts/extract.py`.

A preview takes roughly 1–3 minutes for a few thousand messages on a normal laptop. Full 30 fps rendering is CPU and memory heavy; allow tens of minutes for a large history. Render time grows with message count, image size, and CPU speed. If an input is empty or absent, the script reports the condition rather than generating a generic DNA.
