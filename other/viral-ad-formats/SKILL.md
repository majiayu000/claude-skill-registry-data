---
name: viral-ad-formats
description: >-
  Thư viện format video quảng cáo UGC/hài kiểu Việt Nam + preset ảnh sản phẩm cho SEOSONA Flow lái Veo
  dựng b-roll. Chưng cất TAXONOMY (concept + prompt scaffold + motion) — KHÔNG dùng API/paid nào, Flow tự
  gen bằng Veo của bạn. Dùng khi cần ý tưởng video ads viral, dựng b-roll quảng cáo nhiều cảnh, hoặc chọn
  bố cục ảnh sản phẩm (packshot/poster/infographic/composite). Ghép với interview-to-spec + anti-slop-visual.
---

# SEOSONA Flow — Viral Ad Formats (VN) cho Veo

Bộ **format nội dung** (ý tưởng, không phải công cụ trả phí) để Flow lái **Veo** dựng b-roll quảng cáo.
Mỗi format = concept + **prompt scaffold** (có `{placeholder}` → PromptSlots gợi ví dụ) + **motion** (cho Veo).
Ranh giới: gen video **CÂM** để [[flow-broll]] → V2 lồng tiếng; hoặc bake voice qua Veo nếu cố ý.

## 15 format video ads (chọn theo mục tiêu)

| Format | Concept (hook) | Prompt scaffold (rút gọn) | Motion (Veo) |
|---|---|---|---|
| **Đuổi bắt** | nhân vật bị `{thing}` rượt → sản phẩm cứu nguy | `{subject} chạy hoảng trên {location}, {product} phát sáng cứu nguy` | máy lia nhanh theo, rung nhẹ, tốc độ cao |
| **Đóng băng thời gian** | mọi thứ đứng hình, chỉ `{subject}` + sản phẩm động | `mọi người bất động, {subject} bước qua cầm {product}` | dolly chậm vòng quanh, nền freeze |
| **Review sập sàn** | KOL hô "sắp hết hàng" gấp gáp | `{subject} chỉ tay vào {product}, chữ SALE nhấp nháy` | zoom giật, cắt nhanh, tay chỉ |
| **Unbox bất ngờ** | mở hộp → phản ứng "wow" | `tay mở hộp {product}, mặt {subject} ngỡ ngàng` | cận tay mở, cắt sang mặt, push-in |
| **Bóc phốt / plot-twist** | tưởng xấu → lật ngược khen | `{subject} cau mày nghi ngờ {product}, rồi bật cười gật gù` | 2 nhịp: nghi ngờ → vỡ oà, cut khựng |
| **Bản tin (parody)** | MC "breaking news" về sản phẩm | `MC ngồi bàn tin, màn hình sau hiện {product}, chữ chạy dưới` | tĩnh kiểu studio, lower-third chạy |
| **Thảm đỏ** | sản phẩm ra mắt như sao | `{product} trên bục xoay, đèn flash, thảm đỏ` | bục xoay chậm, flash nhấp nháy |
| **Podcast clip** | talking-head cầm sản phẩm kể | `{subject} đeo tai nghe, mic, cầm {product} kể chuyện` | tĩnh 1 góc, cắt b-roll xen |
| **Phỏng vấn đường phố** | hỏi người qua đường về `{topic}` | `{subject} cầm mic phỏng vấn người đi đường phố cổ` | cầm tay lắc nhẹ, cận mặt trả lời |
| **Đi chợ flex** | mua sắm phô trương vui | `{subject} xách túi {brand}, bước tự tin qua chợ` | slow-mo bước đi, máy ngước |
| **Trà đá vỉa hè** | tám chuyện đời thường về sản phẩm | `2 người ngồi ghế nhựa trà đá, chỉ vào {product} bàn tán` | tĩnh, 2-shot, đời thường |
| **Gia đình review** | mẹ/bà thử → duyệt | `bà cầm {product} săm soi rồi gật đầu ưng ý` | cận tay + mặt, ấm áp |
| **Elevator pitch** | 8s chốt sản phẩm trong thang máy | `{subject} trong thang máy giơ {product} nói nhanh` | tĩnh chật, đèn thang máy |
| **Trước / Sau** | so sánh before-after | `chia đôi khung: trái {before}, phải sau khi dùng {product}` | wipe ngang giữa 2 nửa |
| **UGC cầm tay** | người thật quay tự sướng khen | `{subject} tự quay tay cầm {product}, cười nói vào máy` | tay cầm phone, cận mặt, rung UGC |

## 4 preset ảnh sản phẩm

| Preset | Dùng khi | Prompt scaffold |
|---|---|---|
| **Packshot** | ảnh sản phẩm sạch bán hàng | `{product} nền {bg_color} seamless, đèn softbox, đổ bóng nhẹ, 1:1` |
| **Poster** | banner khuyến mãi có chữ | `{product} lệch trái, chừa mảng phải cho chữ, tông {palette}, 9:16` |
| **Infographic** | nêu 3 tính năng | `{product} giữa, 3 icon + chú thích quanh, nền phẳng, gọn` |
| **Composite** | ghép cảnh đời sống | `{product} đặt trong {scene}, ánh sáng {time}, tự nhiên` |

## Cách dùng
1. Chọn format theo mục tiêu (hook mạnh → đuổi-bắt/unbox; tin cậy → phỏng vấn/UGC; bán gấp → review-sập-sàn).
2. Điền `{placeholder}` — PromptSlots gợi ví dụ; thiếu ý thì chạy [[interview-to-spec]].
3. Rà qua [[anti-slop-visual]] (bỏ cụm sáo), rồi gen: `/flow-broll <scaffold>` (video câm) hoặc node generate.
4. Chữ trên ảnh/video → node Text Overlay (vector, không bake) — xem [[text-in-image]].

## Lưu ý scope
- Đây là **taxonomy nội dung** chưng cất (không copy code/API, KHÔNG dùng dịch vụ trả phí). Flow dựng bằng
  **Veo** (quota Google của bạn). Phần tiếng/ghép là **V2** (xem [[video-ai-v2-pipeline]]).
- Model ảnh có thể từ chối "người thật" trong ref — với UGC/gia đình, dùng nhân vật AI hoặc ref được phép.
