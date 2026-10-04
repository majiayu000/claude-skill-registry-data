---
name: video-production
description: >-
  Dựng video nhiều cảnh có kỷ luật cho SEOSONA — VO-first (đo giọng trước làm nhịp), style-anchor
  frame (1 keyframe neo palette/texture cho mọi cảnh), resumable per-beat state (mỗi cảnh regen độc
  lập). Dùng khi lên kế hoạch 1 video/reel nhiều scene, cần nhất quán hình + nhịp khớp giọng đọc, hoặc
  chia nhỏ để sửa/tạo-lại từng cảnh không phá cả bài. Học vox-explainer + huytranvan.
---

# SEOSONA — Video Production (VO-first, resumable)

Kỷ luật sản xuất video nhiều cảnh: **AI quyết nội dung · code dựng pixel**, giọng làm nhịp, mỗi cảnh độc lập.

## 3 nguyên tắc lõi

### 1. VO-FIRST — giọng làm master clock
- Viết + **đo thời lượng narration TỪNG beat TRƯỚC** khi có hình nào. Beat durations = đồng hồ chủ.
- Hình/motion dựng theo nhịp giọng (không ngược lại) → khỏi lệch tiếng-hình.

### 2. STYLE-ANCHOR frame — nhất quán
- Sinh 1 keyframe "anchor" được duyệt → khoá palette/texture/framing.
- Mọi cảnh sau tái dùng anchor đó (xem skill character-consistency / StyleAnchor) → không "trôi" phong cách.

### 3. RESUMABLE per-beat state
- Lưu state MỖI beat riêng: `script.json` (nội dung), `vo_durations.json` (thời lượng), asset/beat.
- Sửa 1 cảnh → chỉ regen cảnh đó (không dựng lại cả bài). Idempotent.

## Quy trình
1. Script → tách beats (skill prompt-sequence / node prompt_sequence).
2. VO per beat + đo thời lượng → master clock.
3. Style-anchor keyframe (duyệt) → khoá look.
4. Per-beat: image (bám anchor) → motion (khớp thời lượng VO) → caption.
5. **Chữ trên hình**: Reserve→Overlay (skill text-in-image), KHÔNG bake.
6. QA từng beat (skill image-qa / mllm-judge) → beat fail thì regen riêng.
7. Ghép theo master clock.

## Output contract
1. **Beat list**: | beat | VO ({language}) | thời-lượng | image prompt | motion |.
2. **Style-anchor** block (tái dùng mọi beat).
3. **State files** gợi ý (script.json / vo_durations.json / per-beat).
4. Ghi rõ cảnh nào cần regen (nếu QA fail).

## Lưu ý scope
- Đây là **kỷ luật lập kế hoạch + prompt** cho video. Phần AUDIO thật (TTS/mix) là **SEOSONA Video AI V2** (sidecar riêng, ngoài extension Flow) — xem skill video-ai-v2-pipeline. Skill này lo nội dung/nhịp/nhất quán, không tự render audio.
