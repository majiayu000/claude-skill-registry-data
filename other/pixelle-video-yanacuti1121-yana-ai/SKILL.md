---
name: pixelle-video
description: "Use when asked to create or generate a video automatically from a topic, text, or idea. Triggers on: 'tạo video', 'generate video', 'make a video about', 'video từ chủ đề', 'short video', 'create reel', 'pixelle', 'video tự động', 'video AI'. Requires Pixelle-Video server running locally (docker-compose or pip install)."
---

# Pixelle-Video Skill

Tự động tạo video AI từ một chủ đề hoặc đoạn văn bản — script → ảnh AI → voice → BGM → video hoàn chỉnh.
Dùng [AIDC-AI/Pixelle-Video](https://github.com/AIDC-AI/Pixelle-Video) (REST API, FastAPI, ComfyUI backend).

## Prerequisites

Pixelle-Video phải đang chạy trước khi gọi skill này:

```bash
# Kiểm tra server có đang chạy không
curl -s http://localhost:8000/api/health | jq .

# Nếu chưa chạy — khởi động bằng Docker
docker compose up -d    # trong thư mục Pixelle-Video

# Hoặc chạy thẳng
pip install -e .
pixelle-video start
```

## Workflow

### Step 1 — Xác nhận input từ user

Thu thập 3 thông tin:
- **text**: Chủ đề hoặc đoạn văn bản nguồn (vd: "Atomic Habits dạy chúng ta thay đổi thói quen nhỏ")
- **mode**: `generate` (AI tự viết lời) hoặc `fixed` (dùng text nguyên)
- **n_scenes**: Số cảnh, mặc định 5 (1–20)

Nếu user chỉ cung cấp chủ đề ngắn → dùng `mode: generate`.
Nếu user cung cấp script đầy đủ → dùng `mode: fixed`.

### Step 2 — Kiểm tra server health

```bash
curl -s http://localhost:8000/api/health
```

Nếu server không phản hồi → báo user khởi động server, dừng.

### Step 3 — Tạo video (async)

```bash
curl -s -X POST http://localhost:8000/api/video/async \
  -H "Content-Type: application/json" \
  -d '{
    "text": "<user_text>",
    "mode": "generate",
    "n_scenes": 5,
    "frame_template": "1080x1920/image_default.html",
    "video_fps": 30,
    "bgm_volume": 0.3
  }' | jq .
```

Ghi lại `task_id` từ response.

### Step 4 — Poll task status

```bash
TASK_ID="<task_id_from_step3>"
while true; do
  STATUS=$(curl -s "http://localhost:8000/api/tasks/$TASK_ID" | jq -r '.status')
  echo "Status: $STATUS"
  if [[ "$STATUS" == "completed" || "$STATUS" == "failed" ]]; then break; fi
  sleep 5
done
curl -s "http://localhost:8000/api/tasks/$TASK_ID" | jq .
```

### Step 5 — Lấy kết quả

Khi status = `completed`, response chứa `video_url`:

```bash
curl -s "http://localhost:8000/api/tasks/$TASK_ID" | jq '{
  video_url: .result.video_url,
  duration: .result.duration,
  file_size: .result.file_size
}'
```

Download video:
```bash
VIDEO_URL=$(curl -s "http://localhost:8000/api/tasks/$TASK_ID" | jq -r '.result.video_url')
curl -L "$VIDEO_URL" -o output_video.mp4
echo "Video saved → output_video.mp4"
```

### Step 6 — Báo cáo kết quả

Trả về cho user:
- Đường dẫn file video đã download
- Thời lượng (duration) + kích thước file
- URL nếu user muốn xem trực tiếp qua browser (`http://localhost:8000` + video_url)

## Options nâng cao

| Param | Mặc định | Mô tả |
|-------|---------|--------|
| `frame_template` | `1080x1920/image_default.html` | Template kích thước + layout (portrait/landscape) |
| `tts_workflow` | default config | Workflow TTS (giọng đọc) |
| `ref_audio` | none | Audio mẫu để clone giọng |
| `bgm_path` | none | Đường dẫn file nhạc nền tuỳ chỉnh |
| `bgm_volume` | `0.3` | Âm lượng nhạc nền (0.0–1.0) |
| `prompt_prefix` | none | Style prefix cho ảnh AI (vd: "cinematic, 4K") |
| `template_params` | none | Màu sắc, background tuỳ chỉnh cho template |

## Ví dụ nhanh

```bash
# Video 5 cảnh về thói quen tốt
curl -X POST http://localhost:8000/api/video/async \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Thói quen nhỏ mỗi ngày tạo nên sự khác biệt lớn trong cuộc đời bạn.",
    "mode": "generate",
    "n_scenes": 5,
    "title": "Sức mạnh của thói quen nhỏ"
  }'
```

## Xử lý lỗi

| Lỗi | Nguyên nhân | Fix |
|-----|------------|-----|
| `Connection refused` | Server chưa chạy | `docker compose up -d` |
| `task status: failed` | ComfyUI chưa start / thiếu model | Xem log: `docker compose logs` |
| Video trống / âm thanh không có | TTS workflow chưa config | Kiểm tra `config.yaml` → `tts_workflow` |
| Ảnh không generate | ComfyUI API key / model chưa cài | Xem README → Image Generation Setup |
