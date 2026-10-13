---
name: instagram-video-workflow
description: Download Instagram videos + transcribe with faster-whisper + extract content automatically.
---

# Instagram Video Workflow

Complete pipeline: download Instagram video → transcribe audio → extract useful content.

## Tools

- **parth-dl**: CLI Instagram downloader (installed via pipx) — downloads Reels, posts, carrousels, profile pics
- **ig-download MCP server**: Node.js MCP server at `/home/keila/ig-download-mcp-server/` with a `download` tool (url + path params)
- **faster-whisper**: Python library for transcription (installed via pipx)
- **transcribe.py**: `/home/keila/ig-download-mcp-server/transcribe.py` — CLI script that extracts audio with ffmpeg + transcribes with faster-whisper

## Workflow Steps

### 1. Download video

**Option A — via MCP tool** (uses `download` tool from ig-download MCP server):
- Tool name: `download`
- Params: `url` (Instagram URL), `path` (where to save)
- ⚠️ This MCP server may fail (`Instagram download error`); fall back to parth-dl if so.

**Option B — via parth-dl CLI**:
```bash
parth-dl "https://www.instagram.com/reel/ABC123/" -o /path/to/output.mp4
```
- ⚠️ `-o` requires a full file path (e.g. `/path/to/reel.mp4`), NOT just a directory.
- 🔍 **Dica:** Mesmo quando o download falha (ex: caminho errado), o parth-dl imprime o **título e uploader** do Reel no erro. Capture essas infos antes de corrigir o caminho — elas já dão contexto sobre o conteúdo.

### 2. Check for audio track

Before transcribing, verify the video has an audio stream:

```bash
ffprobe -v quiet -show_entries stream=codec_type /path/to/video.mp4 | grep -q audio && echo "✅ Has audio" || echo "❌ No audio (silent video)"
```

If only `video` appears (no `audio`), the Reel is silent — skip transcription entirely and go straight to caption scraping.

### 3. Transcribe audio (skip if silent)

```bash
python3 /home/keila/ig-download-mcp-server/transcribe.py /path/to/video.mp4 --model base --output transcript.json
```

Models: tiny (fastest) < base < small < medium < large-v3 (most accurate)

If HF_UNUTHENTICATED warning appears, it's harmless — transcription still works.

### 4. Extract content

**Option A — from transcript** (if audio was present): use the LLM to analyze the transcript and extract:
- Key topics / summary
- Action items
- Useful information
- Quotes

**Option B — from Instagram post caption** (if video is silent, OR as supplementary source): Use `browser_navigate` to open the Instagram URL and scrape the caption text from the page.

- 📝 **A caption pode estar visível mesmo com o login dialog aberto.** O `browser_snapshot` retorna a árvore de acessibilidade completa — procure por `StaticText` dentro de `dialog` ou `generic` containers. A legenda geralmente aparece como múltiplos `StaticText` nodes com o texto completo do post.
- Se o snapshot mostrar um modal de login, role (ou clique "Close" se houver) para revelar mais conteúdo.
- O título e uploader também aparecem no snapshot como `link` com `StaticText` — colete tudo junto.

## Config

The MCP server is registered in `~/.hermes/config.yaml` as `ig-download`:
```yaml
mcp_servers:
  ig-download:
    command: node
    args:
      - /home/keila/ig-download-mcp-server/index.js
```

## Pitfalls

- Only works with PUBLIC Instagram content
- Stories and Highlights require authentication (not supported)
- `parth-dl -o` requires a full file path (e.g. `/path/to/reel.mp4`), not just a directory — passing a directory gives `[Errno 21] Is a directory`
- Some Reels have **no audio track** (silent video-only posts). Always check with `ffprobe` before running transcription
- If transcription returns empty segments but the video has an audio stream, try a larger whisper model (e.g. `small` or `medium`)
- transcribe.py uses CPU by default — large models may be slow on CPU
- The ig-download MCP server uses `btch-downloader` npm package which may break if Instagram API changes; parth-dl is the more reliable fallback
- The provider (DeepSeek/OpenCode Zen) does NOT support vision — `vision_analyze` will fail with `unknown variant image_url`. Use browser_navigate to scrape captions instead
- To reload MCP servers in Hermes after adding to config: restart session or `/reload`
