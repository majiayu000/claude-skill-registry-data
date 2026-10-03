---
name: mermate-tab-idea
description: Stage 1 tab (Simple Idea) of the Mermate pipeline — raw idea intake, AI enhancement, voice transcription, and the Idea → Markdown transition. Use when editing idea-stage UI, the enhance/copilot path, voice input, or the /api/analyze and /api/copilot/enhance endpoints.
---

# Mermate Tab 1 · Simple Idea (idea)

Operates under `mermate` master invariants; Lamport standards via `specification-master-agent`.

## Stage Identity (from `STAGE_REGISTRY.idea`, public/js/mermaid-gpt-app.js)
- Label: **Simple Idea** · reveal: `STAGE 1 · IDEA` · color `#fbbf24`
- Expected duration: ≈5–15s · enhance default: ON · no file upload
- **IPO contract**:
  - Input: raw text dump — ideas, notes, speech
  - Process: copilot profile analysis + AI enhancement
  - Output: refined idea, ready for Markdown structuring

## Owning Code
- Frontend: `public/js/mermaid-gpt-app.js` (idea input config, ⌘⏎ enhance, tab-completion suggestion)
- Backend: `server/routes/render.js` — `POST /api/analyze` (input profile), `POST /api/copilot/enhance` (enhance proxy, lines 188–231), `GET /api/copilot/health`
- Voice: `server/routes/transcribe.js` — `POST /api/transcribe` (OpenAI Whisper, requires `MERMATE_AI_API_KEY`)
- Classification: `server/services/input-router.js` → content_state `text | hybrid`

## Stage Invariants
1. Idea input never blocks on enhancement — enhance failure degrades to raw text, never to a stuck tab.
2. Enhancement is advisory: the user's original text remains recoverable (animate/transition only when `data.enhanced && data.compiled_source`).
3. Voice input lands as plain idea text; transcription failure surfaces as an error toast, not silent loss.

## Anti-Patterns (Reject)
- Inventing client-side classification that duplicates `input-router.js` / `MermaidClassifier`.
- Letting the enhancer proxy's latency or failure gate the render path.
- Adding upload UI to this tab (registry says `showUpload: false` — deliberate).

## Verification
- `npm run test:fast`; touch classifier logic → `node --test test/test-classifier.js`
