---
name: dong-bo-thiet-ke-mockdata
description: "Quy trình đồng bộ khi thiết kế lại 1 trang Website cần hiển thị trường dữ liệu mới (rating, mô tả dài, bảng thông số, đánh giá khách hàng...) chưa có trong response API JGameApi. Dùng khi: redesign trang chi tiết/danh sách kiểu Shopee, thêm field mới vào type, phát hiện API đã trả field mà UI đang bỏ qua, cần test Website với BE local thay vì mock nội bộ."
---

# Đồng bộ Thiết kế UI ↔ MockData Backend — phía Website

> Backend hiện chỉ trả mock data (chưa có DB thật). Khi 1 trang Website cần hiển thị thêm thông
> tin mà API JGameApi CHƯA trả — **PHẢI sửa Backend trước** (xem
> `Backend/.claude/skills/dong-bo-thiet-ke-mockdata/SKILL.md`), không tự bịa dữ liệu ở tầng
> Website (kiểu field UI-only cũ `art`/`MockAccessoryArt` — BE thật không trả, chỉ dùng làm
> fallback khi thiếu ảnh, không phải nguồn dữ liệu chính).

## Quy trình phía Website (sau khi Backend đã trả field mới)

1. **TS type** (`features/<Module>/<feature>/types/<x>.types.ts`) — thêm field vào interface.
   JSON key từ BE là camelCase (System.Text.Json mặc định) — field TS đặt ĐÚNG tên đó, không cần
   tầng mapping riêng vì `ApiService` chỉ `return response.json()` thẳng (xem
   `AccessoryApiService.ts`).
2. **Component/Page hiển thị** — cập nhật trang/card liên quan. Ảnh: dùng component `<X>Art.tsx`
   có sẵn (VD: `AccessoryArt`, `CardArt`) — nếu `art?: Mock<X>Art` là field UI-only cũ, giữ nguyên
   làm fallback khi ảnh lỗi, KHÔNG xoá.
3. `npx tsc -b` trong `Website/` — lọc lỗi liên quan file mình sửa (`grep -i "<feature-keyword>"`
   trên output); dự án hiện có 1 số lỗi TS tồn đọng ở module khác (Admin dashboard, ShopOwner,
   Order/Playtime/Card services) — KHÔNG phải do thay đổi của mình thì không cần sửa cùng lúc,
   nhưng phải xác nhận field/file mình vừa sửa không sinh thêm lỗi mới.
4. Kiểm tra thật bằng Playwright hoặc mở tay: Website mặc định `VITE_JGAME_USE_MOCK=true` (đọc
   mock nội bộ, KHÔNG gọi BE thật) — để test với Backend local đang chạy, tạo file
   `Website/.env.local` (gitignore, KHÔNG commit, xoá sau khi test xong):
   ```
   VITE_JGAME_API_URL=http://localhost:<port-backend>
   VITE_JGAME_USE_MOCK=false
   ```
   Chạy `npm run dev`, Website dùng **HashRouter** nên URL truy cập trực tiếp phải có `#`, ví dụ
   `http://localhost:<port-vite>/#/jgame/phu-kien/<id>` — quên `#` sẽ bị điều hướng sai (redirect
   về trang chủ).

## Bẫy hay gặp

- Field optional ở TS (`originalPrice?: number | null`) nhưng render không check `!!product.originalPrice`
  trước khi tính discount % → lỗi runtime khi field null.
- Quên xoá `Website/.env.local` sau khi test xong — không ảnh hưởng git (đã gitignore) nhưng dễ
  quên là máy đang trỏ BE local thay vì mock khi debug việc khác sau này.

## Ví dụ đã làm (tham khảo khi cần pattern tương tự)

Redesign `AccessoryDetailPage.tsx` kiểu Shopee (2026-08-30):
`features/Public/accessories/types/accessory.types.ts` (thêm `AccessorySpecItem`,
`AccessoryReview`, field `originalPrice/rating/reviewCount/soldCount/warrantyMonths/description/
highlights/specifications/reviews`), `pages/AccessoryDetailPage.tsx` — rating/đã bán, giá + giảm
giá, điểm nổi bật, chính sách bảo hành/vận chuyển/đổi trả, mô tả, bảng thông số, đánh giá khách
hàng. Backend tương ứng: `Backend/JGameApi/DTOs/Accessories/Responses/AccessoryProductResponse.cs`
+ `MockData/MockAccessoryData.cs`. App tương ứng:
`App/.claude/skills/dong-bo-thiet-ke-mockdata/SKILL.md`.
