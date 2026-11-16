---
name: content-platform-team
description: One brief → platform-native content for TikTok, Xiaohongshu (小红书), X/Twitter thread, LinkedIn — simultaneously. Each platform gets a specialist with native format, tone, and hooks. No generic copy-paste. Inspired by msitarzewski/agency-agents marketing division (MIT).
origin: yana-ai — inspired by msitarzewski/agency-agents (MIT)
license: MIT
version: 1.0.0
triggers:
  - /content-platform-team
  - /cpt
  - viết content đa nền tảng
  - content cho nhiều nền tảng
  - content platform
  - tiktok xiaohongshu linkedin twitter
  - viết content marketing
---

# /content-platform-team

Một brief. Bốn nền tảng. Bốn chuyên gia viết song song — mỗi người native với thuật toán, format, và văn hóa của nền tảng mình. Không copy-paste chéo.

```
/content-platform-team "Ra mắt sản phẩm X"
/cpt "Chia sẻ kinh nghiệm học lập trình từ 0"
/cpt "Review laptop Macbook M4" --platforms tiktok,xhs
/cpt --brief-only   → chỉ hỏi thông tin brief, chưa viết
```

---

## Khi nào dùng

- Có một chủ đề/sản phẩm/câu chuyện muốn đẩy lên nhiều nền tảng cùng lúc
- Muốn nội dung thực sự native với từng platform, không giống nhau
- Đang làm content marketing, personal brand, hoặc product launch

## Khi nào KHÔNG dùng

- Chỉ cần nội dung cho 1 platform (yêu cầu platform cụ thể trực tiếp)
- Cần ảnh/video thực sự (skill này viết script và caption, không tạo media)
- Nội dung quá nhạy cảm/chính trị

---

## Brief cần trước khi viết

Nếu brief chưa đủ, hỏi đúng 4 câu này:

```
1. Chủ đề / sản phẩm là gì? (1 câu)
2. Đối tượng mục tiêu là ai? (tuổi, mối quan tâm, level)
3. Tone muốn: chuyên nghiệp / thân thiện / hài hước / inspiring / educational?
4. CTA (call to action) mong muốn: follow / comment / click link / mua hàng?
```

---

## 4 Platform Specialist

### 🎵 TikTok Specialist

**Thuật toán TikTok ưu tiên:**
- 3 giây đầu quyết định tất cả (hook rate)
- Watch time > completion rate > comments > shares
- Trending audio/sound tăng reach 2-3x
- Caption ngắn, text overlay quan trọng hơn caption

**Format script TikTok:**
```
[0s–3s] HOOK — câu mở đầu gây sốc/tò mò/controversial
  Kiểu: "90% người [X] không biết điều này"
        "Lý do tôi [hành động bất ngờ]"
        "POV: [tình huống relatable]"

[3s–15s] SETUP — context ngắn, build tension
[15s–45s] PAYOFF — giá trị thực, thực tế, không đủ thời gian lý thuyết
[45s–60s] CTA + hook cho comment ("Bình luận nếu bạn cũng...")

Text overlay: 3-5 dòng, mỗi dòng max 7 từ
Caption: max 150 ký tự + 3-5 hashtag trending
```

---

### 📕 Xiaohongshu (小红书/XHS) Specialist

**Thuật toán XHS ưu tiên:**
- Keywords trong title và body (SEO nội bộ mạnh)
- Ảnh đẹp, aesthetic — người dùng lưu (save) quan trọng hơn like
- Nội dung "dry goods" (干货 — giá trị thực tế) được yêu thích
- Comment hỏi đáp giữ engagement
- Dùng bullet points và emoji structure

**Format XHS:**
```
TITLE: [keyword chính] + [lợi ích cụ thể] (max 20 ký tự)
  Kiểu: "学编程3个月，我的真实经历🔥"
        "MacBook M4 深度使用 | 值得买吗"
        "[sản phẩm]避坑指南✅"

BODY (800-1500 ký tự):
  📌 [Điểm 1] — mô tả
  📌 [Điểm 2] — mô tả
  📌 [Điểm 3] — mô tả
  
  [Đoạn kết với CTA: "你们有什么想了解的可以评论⬇️"]

TAGS: #[topic] #[niche keyword] #[trending hashtag] (5-10 tags)
```

---

### 🐦 X/Twitter Thread Specialist

**Thuật toán X ưu tiên:**
- Tweet 1 (hook) quyết định toàn bộ thread có được đọc không
- Bookmarks > replies > reposts (reach)
- Thread 5-15 tweets sweet spot
- Cliffhanger giữa mỗi tweet giữ người đọc cuộn
- Số liệu + opinionated statements viral tốt

**Format Thread:**
```
Tweet 1 — HOOK (max 280 ký tự):
  Bold claim hoặc counterintuitive insight
  Kết thúc bằng "Thread 🧵" hoặc "(1/N)"

Tweet 2-3 — CONTEXT:
  Tại sao nội dung này quan trọng với họ

Tweet 4-9 — MEAT:
  Mỗi tweet = 1 điểm rõ ràng + bằng chứng/ví dụ
  Câu cuối mỗi tweet = setup cho tweet tiếp theo

Tweet N-1 — SYNTHESIS:
  Tóm tắt 3 điểm cốt lõi

Tweet N — CTA:
  "Follow nếu muốn thêm về [topic]"
  Repost tweet đầu để tăng reach
```

---

### 💼 LinkedIn Specialist

**Thuật toán LinkedIn ưu tiên:**
- Dòng đầu (above the fold) trước "see more" → tỷ lệ click cao = reach cao
- Native text > link post (link giảm reach 50-70%)
- Personal story > corporate announcement
- Comment dài trong 30 phút đầu = tín hiệu mạnh cho thuật toán
- Hỏi câu hỏi cuối bài → tăng comment

**Format LinkedIn:**
```
LINE 1 (Hook — không quá 150 ký tự):
  Câu statement mạnh, không "Dear Network"
  Kiểu: "3 năm trước tôi từng..."
        "Điều tôi ước được biết khi..."

[dòng trống]

BODY (200-600 từ):
  - Paragraph ngắn (2-3 dòng)
  - Spacing rộng, dễ đọc trên mobile
  - Story arc: situation → complication → resolution
  - 1-2 con số cụ thể tăng credibility
  
[dòng trống]

CTA (1 câu):
  Câu hỏi mở để invite comment
  Hoặc: "Save lại bài này nếu có ích"

TAGS: 3-5 tags liên quan trực tiếp (không spam)
```

---

## Output chuẩn

```markdown
## Content Package: [Chủ đề]

*Brief: [tóm tắt 1 câu] | Audience: [target] | Tone: [X] | CTA: [Y]*

---

### 🎵 TikTok Script

**Hook (0–3s):**
[câu mở đầu]

**Script:**
[0s–3s] [hook text]
[3s–15s] [setup]
[15s–45s] [main content]
[45s–60s] [CTA]

**Text overlay:**
- [dòng 1]
- [dòng 2]
- [dòng 3]

**Caption:**
[caption ngắn] #[tag1] #[tag2] #[tag3]

**Gợi ý âm thanh:** [trending sound type]

---

### 📕 Xiaohongshu Post

**Title:** [title tiếng Trung/Việt]

**Body:**
[nội dung đầy đủ với emoji structure]

**Tags:** #[tag1] #[tag2] ...

**Gợi ý ảnh:** [mô tả concept ảnh đầu]

---

### 🐦 X Thread

**Tweet 1/[N] — Hook:**
[tweet hook]

**Tweet 2/[N]:**
[tweet 2]

[... tiếp theo]

**Tweet [N]/[N] — CTA:**
[tweet kết]

---

### 💼 LinkedIn Post

**[Dòng hook]**

[nội dung đầy đủ]

[CTA question]

#[tag1] #[tag2] #[tag3]

---

### Ghi chú phân tích

**Điểm khác nhau chính giữa 4 platform:**
- TikTok: [điểm đặc trưng]
- XHS: [điểm đặc trưng]
- X: [điểm đặc trưng]
- LinkedIn: [điểm đặc trưng]

**Đăng theo thứ tự:** [platform nào đăng trước để build momentum]
```

---

## Platform flags

```
--platforms tiktok,xhs          → chỉ 2 platform đó
--platforms twitter,linkedin    → chỉ 2 platform đó
--lang vi                       → tiếng Việt (default)
--lang en                       → tiếng Anh
--lang zh                       → tiếng Trung (XHS native)
--brief-only                    → chỉ hỏi brief, chưa viết
--repurpose [url]               → tóm tắt nội dung từ URL rồi viết
```

---

## Anti-patterns

```
❌ Copy y chang nội dung giữa các platform — thuật toán phạt, user nhận ra ngay
❌ Caption LinkedIn dài 1000 từ trên TikTok — platform mismatch
❌ Emoji spam trên LinkedIn (≤3 emoji/post)
❌ Thread Twitter 30 tweets — không ai đọc hết
❌ XHS title > 20 ký tự — bị cắt trong feed
❌ Hook TikTok mở đầu bằng "Xin chào mọi người" — tỷ lệ thoát cao
```

---

## Skills liên quan

- `copywriting` — copy dài form, landing page, email
- `storyteller` — narrative arc và storytelling
- `seo-geo-aeo-strategist` — SEO cho blog và web content
