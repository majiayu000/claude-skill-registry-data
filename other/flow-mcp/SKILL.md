---
name: flow-mcp
description: >-
  Cách lái SEOSONA Flow (gen ẢNH/VIDEO/b-roll) qua Local MCP server (mcp-local/) — cho agent HOẶC
  SEOSONA Video AI V2 gọi. Dùng khi cần sinh visual asset từ ngoài extension (Claude Code/Cursor/V2),
  chọn tool đúng (discovery→gen/run_workflow), đọc envelope FlowResult, xử lý error_code, hoặc định
  nghĩa/validate hợp đồng script.json Flow↔V2. MCP là TÙY CHỌN: có → V2 kéo b-roll từ Flow; không →
  cả hai chạy độc lập.
---

# SEOSONA Flow — Local MCP (lái gen từ ngoài extension)

**Ranh giới:** Flow = dựng PIXEL (ảnh/video/b-roll), KHÔNG audio. Video AI V2 = kịch bản + voice + edit +
mux. V2 (hoặc agent) gọi Flow **qua MCP** để lấy asset, rồi V2 tự lo giọng → content↔voice khớp. Cầu ở
`seosona-flow/mcp-local/server.mjs` (MCP stdio + WS 127.0.0.1). Extension side panel phải mở trên tab
`labs.google/fx` (đã đăng nhập) = executor. Không nối → tool trả lỗi rõ "Extension not connected".

## Tool surface (20) — luôn trả envelope FlowResult (text + `structuredContent`)

`{ ok, tool, status, assets?[], data?, batch?, error_code?, error_message?, idempotent_hit? }`
Mỗi tool khai `outputSchema` → MCP client validate response native.

- **Gen** (→ `assets: FlowAsset[]`): `gen_image` · `gen_video` (b-roll; **bỏ `voice` = CÂM**, để V2 lồng giọng) ·
  `run_workflow(wf_id)` · `upload_ref(url)`. Cả 3 gen nhận **`client_ref`** (idempotency — xem dưới).
- **Export** (handoff file): `export_asset(url|video_url,file_name?,folder?)` → tải asset ra đĩa
  (`Downloads/<folder>/<file_name>`, xem `path_hint`). **BẮT BUỘC cho VIDEO** (URL cần session Google; ảnh
  đã có base64 inline nên chỉ export khi muốn re-download res cao).
- **Discovery** (read-only, gọi bất cứ lúc nào): `list_capabilities` (GỌI ĐẦU) · `list_models` · `list_voices` ·
  `list_workflows(flow_kind?)` · `list_projects` · `search_prompts(query?,tags?,limit?)` · `get_context` ·
  `get_provider_status` · `list_results`.
- **Control** (server trả, không round-trip extension): `health` (liveness + version + `extension_connected`) ·
  `cancel_job(job_id?)`.
- **Project/memory**: `create_project` · `open_project(project_id)` · `memory_search` · `memory_add`.

`FlowAsset` = `{ asset_id, kind:image|video, url, thumbnail_url, file_name, provider }`.

## Idempotency (pipeline resumable) & prompts
- Truyền **`client_ref`** (vd scene id) vào gen → gọi lại cùng `client_ref` trả cache (`idempotent_hit:true`),
  **KHÔNG gen lại/tốn quota**. Sống sót restart server (persist `.cache/`, đổi `SEOSONA_LOCAL_MCP_CACHE_DIR`).
- Kho prompt đóng gói còn lộ qua MCP **`prompts/list` + `prompts/get`** (nền `search_prompts`).
- **Progress streaming**: truyền `progressToken` (SDK: callback `onprogress`) vào gen/run_workflow → server phát
  `notifications/progress` khi chạy (gen multi-ảnh: `completed/total`; workflow: mỗi node xong 1 tick).

## Quy trình chuẩn (V2 / agent)
1. `health` → chắc `extension_connected` + `contract_version` khớp TRƯỚC khi chạy pipeline.
2. `list_capabilities` → biết model/ratio/voice (model nào bake voice — thường KHÔNG muốn).
3. Mỗi cảnh: `gen_image` / `gen_video` (câm) / `run_workflow` (**kèm `client_ref`=scene id** → resume khỏi gen lại) → lấy `assets[]`.
4. **Lấy file**: ảnh = base64 inline; **video → `export_asset(video_url)`** → đọc `Downloads/<folder>/<file_name>`.
5. V2 điền `scene.asset`, rồi TTS + caption + **mux** LOCAL (ngoài Flow). `cancel_job` nếu user huỷ.

## Xử lý error_code (đừng retry mù)
- `PROVIDER_NOT_LOGGED_IN` / `PROVIDER_TAB_NOT_READY` → bảo user mở/đăng nhập tab provider, KHÔNG retry ngay.
- `WRONG_PROJECT` → workflow thuộc project khác → hỏi user rồi `open_project(expected_id)` → `run_workflow` lại.
- `DAILY_QUOTA_EXCEEDED` → hết quota Google Flow của user → dừng, chờ reset.
- `EXTENSION_BUSY` → extension đang chạy job khác → chờ xong.
- `VALIDATION_ERROR` (voice/model) → dùng `list_capabilities`/`list_voices` lấy slug đúng rồi gọi lại.

## Hợp đồng script.json (Flow↔V2) — resource `seosona://contract`
V2 SỞ HỮU script.json; Flow chỉ fulfill `scene.inputs[]` (`SceneInput.source`: `flow_gen_image` |
`flow_gen_video` | `flow_run_workflow` | `flow_asset` | `local`). Flow KHÔNG đọc `voiceText`.
Validate: `node mcp-local/contracts/validate.mjs script <file>` | `result <file>` | `--self-test`.

## Nguyên tắc
- **Discovery-first**: hỏi năng lực TRƯỚC khi gen → tránh VALIDATION_ERROR giữa chừng.
- **B-roll câm mặc định**: voice là việc của V2 (khớp kịch bản). Chỉ truyền `voice` khi CỐ Ý để Veo bake.
- **MCP tùy chọn**: code V2 phải chạy được cả khi KHÔNG có Flow-MCP (degrade, không crash).
- **Bảo mật**: WS chỉ loopback + chặn origin web; đặt `SEOSONA_LOCAL_MCP_TOKEN` (khớp 2 phía) khi cần mutual-auth.
- Xem thêm skill [video-ai-v2-pipeline] (kiến trúc V2) + [video-production] (kỷ luật nội dung/nhịp).

## Tiện ích
- **Slash-command** (`.claude/commands/flow-*.md`): `/flow-health` · `/flow-gen` · `/flow-broll` (video câm) ·
  `/flow-run` · `/flow-prompts` — wrapper gọi nhanh tool MCP.
- **Tái lập**: ảnh export từ node Text Overlay được nhúng spec JSON vào PNG (`PngText`, tEXt chunk, UTF-8) —
  kéo ảnh lại là đọc được spec gen.

## Verify
`cd seosona-flow/mcp-local && npm test` → normalize + contract self-test + integration E2E (giả lập extension, không cần Chrome).
