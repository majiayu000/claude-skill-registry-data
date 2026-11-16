---
name: video-linggo
description: "Video translation, dubbing and subtitle generation pipeline — WhisperX speech recognition, LLM translation (Claude/GPT/DeepSeek), multi-voice TTS, Netflix-standard single-line subtitles. Triggers on: 'video translation', 'dịch video', 'thuyết minh video', 'video dubbing', 'tạo phụ đề', 'subtitle generation', 'videolinggo', 'video linggo', 'dịch phụ đề youtube', 'whisperx subtitle', 'tts dubbing video', 'lồng tiếng video AI', 'translate youtube video'."
origin: skyconnfig/VideoLinggo (MIT)
license: MIT
version: "1.0.0"
compatibility: "yana-ai >= 0.41.0"
allowed-tools: Bash, Read, Write
---

# VideoLinggo — Video Translation & Dubbing
# Source: skyconnfig/VideoLinggo (MIT)
# Tier: TIER 3 — PRODUCTIVITY

Dịch + lồng tiếng video tự động: tải YouTube → nhận dạng giọng nói → dịch AI → TTS → video hoàn chỉnh.

**Do NOT use for:** `terminal--whisper` (chỉ transcript, không dịch/TTS).

---

## Pipeline tổng thể

```
YouTube URL / file local
        ↓  yt-dlp
Audio extraction (.wav)
        ↓  WhisperX
Word-level transcript (timestamps chính xác từng từ)
        ↓  NLP segmentation
Subtitle segments (chuẩn Netflix: ≤ 1 dòng, ≤ 42 ký tự)
        ↓  LLM (Claude / GPT-4 / DeepSeek / Gemini)
Translated subtitles (3-step refinement + custom terminology)
        ↓  TTS (Azure / OpenAI / Edge-TTS / Fish-TTS / GPT-SoVITS)
Dubbed audio track
        ↓  ffmpeg mux
Video đầu ra với phụ đề + tiếng lồng
```

---

## Cài đặt

```bash
git clone https://github.com/skyconnfig/VideoLinggo
cd VideoLinggo
pip install -r requirements.txt

# WhisperX cần CUDA hoặc CPU (chậm hơn)
pip install whisperx

# Chạy UI Streamlit
streamlit run app.py
```

---

## Sử dụng — CLI

```bash
# Bước 1: Tải video + extract audio
yt-dlp -x --audio-format wav "https://youtube.com/watch?v=VIDEO_ID" -o audio.wav

# Bước 2: Transcript với WhisperX (word-level timestamps)
whisperx audio.wav --model large-v2 --language en --output_format srt

# Bước 3: Dịch với LLM (Claude)
python translate.py \
  --input audio.srt \
  --target-lang vi \
  --model claude-sonnet-4-6 \
  --terminology terms.json   # custom terminology để nhất quán

# Bước 4: TTS lồng tiếng (Edge-TTS free)
python tts.py \
  --input translated.srt \
  --voice vi-VN-HoaiMyNeural \
  --output dubbed.wav

# Bước 5: Ghép video
ffmpeg -i original.mp4 -i dubbed.wav -c:v copy -c:a aac \
  -map 0:v:0 -map 1:a:0 output.mp4
```

---

## Ngôn ngữ hỗ trợ

```
Input (nhận dạng):   EN, RU, FR, DE, IT, ES, JA, ZH
Output (dịch):       Tất cả ngôn ngữ (qua LLM)
TTS (lồng tiếng):   Phụ thuộc engine chọn:
  Edge-TTS (free):  100+ giọng, bao gồm VI
  Azure TTS:        Neural voices, chất lượng cao
  OpenAI TTS:       alloy, echo, nova, shimmer
  GPT-SoVITS:       Clone giọng custom (cần GPU)
  Fish-TTS:         Streaming, latency thấp
```

---

## Custom terminology

```json
// terms.json — đảm bảo nhất quán thuật ngữ chuyên ngành
{
  "AI agent": "AI agent",
  "retrieval-augmented generation": "RAG",
  "fine-tuning": "fine-tuning",
  "Yana AI": "Yana AI"
}
```

LLM sẽ ưu tiên dùng đúng thuật ngữ trong file này thay vì dịch tự do.

---

## TTS Engine so sánh

| Engine | Chi phí | Chất lượng | Tiếng Việt | Ghi chú |
|--------|---------|------------|------------|---------|
| Edge-TTS | Free | Tốt | ✅ | Khuyến nghị bắt đầu |
| OpenAI TTS | $15/1M chars | Rất tốt | ❌ | Không có VI |
| Azure TTS | $16/1M chars | Xuất sắc | ✅ | Neural, nhiều giọng VI |
| GPT-SoVITS | Free (local) | Clone giọng | ✅ | Cần GPU + training data |
| Fish-TTS | Free tier | Tốt | Hạn chế | Streaming tốt |

---

## Anti-Fake-Pass Checks

```
❌ FAIL nếu subtitle > 1 dòng (vi phạm Netflix standard)
❌ FAIL nếu TTS audio desync > 200ms so với subtitle timestamp
❌ FAIL nếu WhisperX không có word-level timestamps (dùng --word_timestamps True)
✅ PASS khi: video output có đúng 1 audio track mới + subtitle track
✅ PASS khi: terminology check — custom terms xuất hiện đúng trong output
```

## See also

- `terminal--whisper` — chỉ transcript, không dịch/TTS
- `agent-reach` — tải nội dung từ YouTube (transcript có sẵn qua yt-dlp)
