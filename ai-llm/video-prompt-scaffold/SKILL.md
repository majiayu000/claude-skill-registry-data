---
name: video-prompt-scaffold
description: >-
  Viết prompt VIDEO có kỷ luật cho SEOSONA Flow lái Veo (và Sora/Kling) — cấu trúc 7 phần cố định:
  Subject·Action·Shot·Camera·Setting/Light·Style/Lens·Duration/Audio. Dùng khi viết prompt gen video,
  dựng b-roll nhiều cảnh, hoặc chuẩn hoá prompt trong node. MỘT camera-move + MỘT action mỗi cảnh; cụ thể
  hơn hoa mỹ (qua anti-slop-visual). Kèm khác biệt model + kho "🎬 Video Prompting" mẫu.
---

# SEOSONA Flow — Video Prompt Scaffold (Veo/Sora/Kling)

Prompt video hay = **có kỷ luật**, không nhồi. Model (nhất là Veo) trả tốt khi mỗi cảnh có **1 chủ thể rõ,
1 hành động, 1 chuyển động máy**. Cấu trúc 7 phần — điền đủ, đúng thứ tự:

## 7 phần (điền theo thứ tự này)
1. **Subject** — ai/cái gì, cụ thể (tuổi/trang phục/số lượng/chất liệu). *"a young woman in a linen dress"*
2. **Action** — 1 hành động chính, thì tiếp diễn. *"slowly turning to look over her shoulder"*
3. **Shot & framing** — cỡ cảnh (wide / medium / close-up / extreme close-up) + góc (eye-level / low / high / overhead).
4. **Camera move** — **CHỈ 1**: static · pan · tilt · dolly-in/out · tracking · crane · handheld · orbit · push-in.
5. **Setting & light** — địa điểm + thời gian + hướng/chất sáng. *"sunlit kitchen, backlight, soft shadows"*
6. **Style & lens** — look (film 35mm / anime / 3D) + ống kính (85mm, wide) + DOF (shallow/deep).
7. **Duration & audio** — thời lượng (Veo ~4–8s) + âm thanh: **"no dialogue, ambient only"** cho b-roll (V2 lồng tiếng), hoặc lời thoại trong ngoặc nếu cố ý bake.

**Mẫu 1 dòng:** `[Subject] [action], [shot] [angle], [camera move]. [Setting], [light]. [style], [lens], [DOF]. ~[N]s, [audio].`

## Kỷ luật (bắt buộc)
- **1 move + 1 action / cảnh.** Nhiều chuyển động = model rối, méo. Chia thành nhiều cảnh (skill video-production).
- **Cụ thể > hoa mỹ.** Bỏ "cinematic/epic/8k" (qua [[anti-slop-visual]]) → dùng thông số ống kính/hướng sáng thật.
- **Nêu thời lượng + nhịp.** "~6s, slow" ổn định hơn để trống.
- **Giữ liên tục** giữa các cảnh: cùng nhân vật/trang phục/palette (skill video-production / style-anchor).

## Khác biệt model
| Model | Mạnh | Viết thế nào |
|---|---|---|
| **Veo (Flow)** | Vật lý/thực + **audio native** | Mô tả điện ảnh tự nhiên; **b-roll để CÂM** (`no dialogue, ambient only`) cho V2 lồng tiếng; ~8s |
| **Sora** | Cảnh dài, đa-shot, nhất quán thế giới | Kể theo **chuỗi/câu chuyện**, nhiều beat trong 1 prompt |
| **Kling** | **Image-to-video** (khung đầu) + motion | Cho ảnh start rồi tả **CHUYỂN ĐỘNG** từ ảnh đó (dùng node ảnh → video) |

## Cách dùng trong Flow
1. Thiếu ý → [[interview-to-spec]]; cần format ads → [[viral-ad-formats]].
2. Điền 7 phần (PromptSlots gợi `{placeholder}`), rà [[anti-slop-visual]].
3. Gen: node generate (video) hoặc `/flow-broll`. Chữ trên video → Text Overlay (không bake).
4. Nhiều cảnh → [[video-production]] (VO-first, style-anchor, resumable).

## Kho mẫu
Category **"🎬 Video Prompting"** trong gallery — ~24 scaffold điền sẵn (cinematic/product/food/character/aerial/
macro/abstract) theo đúng 7 phần, có `{placeholder}`. Copy → thay biến → gen.
