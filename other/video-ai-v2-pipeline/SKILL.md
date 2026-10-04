---
name: video-ai-v2-pipeline
description: >-
  Kiến trúc + interface pipeline SEOSONA Video AI V2 (SẢN PHẨM RIÊNG, ngoài extension Flow): audio/TTS/
  ASR/caption/reframe/render chạy LOCAL qua sidecar mcp/CLI. Dùng khi lên kế hoạch/thiết kế phần video
  nặng (TTS, caption word-level, reframe 9:16, ghép), định nghĩa hợp đồng script.json, hoặc chọn tool
  sidecar. LƯU Ý: đây là PLAN/interface — binary (audio.cpp C++/whisperX Python) build ở repo sidecar
  riêng, KHÔNG trong extension JS này.
---

# SEOSONA Video AI V2 — Pipeline (sidecar local, ngoài Flow)

**Ranh giới rõ:** SEOSONA **Flow** (extension) = gen ẢNH/VIDEO qua web-UI, KHÔNG audio. **Video AI V2** =
sản phẩm RIÊNG: dựng video hoàn chỉnh (TTS/ASR/caption/reframe/render) chạy LOCAL qua **sidecar** (mcp/CLI),
extension chỉ điều phối. Nguyên tắc: **AI quyết nội dung · code deterministic dựng pixel/audio**.

## Hợp đồng script.json (từ huytranvan) — 1 nguồn sự thật
```
{ version, renderer, aspect, metadata,
  voice:{provider,speed},
  scenes:[{ id, type:'hook|body|outro', voiceText, templateId, inputs }] }  // 3-12 scene
```
Extension/agent sinh script.json (skill video-production) → sidecar render.

## Sidecar (build ở REPO RIÊNG, không phải extension)
| Bước | Tool đề xuất | Ghi chú |
|---|---|---|
| **TTS** | audio.cpp (ggml, offline, 1 binary) | thay cloud edge-tts (violate local-first). Verify tiếng Việt trước. |
| **ASR + word-timestamp** | whisperX (BSD-2, CPU-able) hoặc audio.cpp forced-align | caption karaoke cần word-level. |
| **Caption render** | TextOverlay (đã có, extension) / sidecar canvas | chữ vector đúng chính tả (Reserve→Overlay). |
| **Reframe 9:16** | openshorts pattern (MediaPipe/YOLO track vs blur GENERAL) + PySceneDetect | sidecar Python/native. |
| **Mix/SFX/BGM** | audio.cpp (mix/denoise/SFX) | duck BGM dưới VO. |
| **Ghép/mux** | ffmpeg | concat + mux. |

## Interface V2 ↔ Flow (MCP) — ĐÃ DỰNG
- V2 lấy visual/b-roll từ Flow qua **Local MCP server** `seosona-flow/mcp-local/server.mjs` (15 tool).
  Xem skill [flow-mcp]. Quy trình: `list_capabilities` → `gen_image`/`gen_video`(câm)/`run_workflow` → `assets[]`.
- **Hợp đồng 1 nguồn**: resource `seosona://contract` = `FlowAsset`/`FlowResult`/`SceneInput`/`script.json`
  (`mcp-local/contracts/flow-asset.schema.json`). Validate: `node contracts/validate.mjs script|result <file>`.
- `SceneInput.source` ∈ `flow_gen_image|flow_gen_video|flow_run_workflow|flow_asset|local` — V2 resolve qua MCP,
  điền `scene.asset`. Flow KHÔNG đọc `voiceText` (V2 giữ giọng khớp kịch bản).
- **MCP tùy chọn**: có Flow-MCP → kéo b-roll; không → V2 vẫn chạy độc lập (degrade).
- Idempotent per-scene: xoá file trung gian 1 scene → regen scene đó (không dựng lại cả video).

## Quality gate
- skill mllm-judge (rubric adherence/motion/temporal/aesthetic) + text-qa (caption đúng chữ) trước khi xuất.

## Trạng thái / việc còn
- Phần Flow-side ĐÃ XONG: MCP server đầy đủ (15 tool) + hợp đồng + validator + skill [flow-mcp] (`npm test` xanh).
- Còn ở **repo V2 riêng** (binary — KHÔNG build từ đây): (1) chọn+verify audio.cpp tiếng Việt, (2) dựng CLI TTS/ASR/reframe/mux, (3) V2 gọi Flow-MCP lấy b-roll rồi mux. Contract + validator đã sẵn ở `mcp-local/contracts/`.
