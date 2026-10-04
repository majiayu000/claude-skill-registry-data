---
name: character-consistency
description: >-
  Giữ NHÂN VẬT / PHONG CÁCH nhất quán qua nhiều ảnh khi gen loạt trong SEOSONA Flow — định nghĩa 1
  khối CHARACTER/STYLE tái dùng verbatim, dựng bộ góc chuẩn, và chèn khối đó vào MỌI prompt cảnh sau.
  Dùng khi user muốn 1 nhân vật/KOC/mascot giữ y hệt diện mạo qua các scene, làm reference sheet, hoặc
  chống "trôi mặt/wardrobe" giữa các lần sinh.
---

# SEOSONA Flow — Character / Style Consistency

Bạn giữ **nhất quán nhân vật & phong cách** khi gen loạt ảnh. Pain-point lớn nhất của AI image: mỗi
lần sinh mặt/wardrobe/style "trôi" một chút. Nguyên tắc (agnes/arcads/vox): **định nghĩa MỘT LẦN,
tái dùng NGUYÊN VĂN.**

## Quy trình

### 1. Tạo khối CHARACTER (hoặc STYLE) tái dùng
Viết 1 block cô đọng, pasteable, mô tả BẤT BIẾN:
- **CHARACTER**: face shape, age range, skin tone, hair, eye color, distinctive features, build, default wardrobe.
- **STYLE**: medium, palette, lighting, texture, era, render look (khi cần nhất quán phong cách thay vì 1 nhân vật).
Nếu có ảnh ref → phân tích ảnh thành block này trước (prompt `img_person_to_charblock` / `img_extract_tokens`).

### 2. Bộ góc chuẩn (reference set)
Sinh {N} góc canonical: hero front, three-quarter left, three-quarter right, side profile, full-body.
Mỗi prompt kèm: *"keep identity, facial proportions and wardrobe IDENTICAL across all — no morphing, no beautifying."* (Workflow mẫu: template "Character sheet (nhất quán nhân vật)".)

### 3. Tái dùng verbatim ở mọi cảnh
Với mỗi cảnh mới: **chèn NGUYÊN VĂN** khối CHARACTER/STYLE vào đầu prompt, chỉ đổi pose/action/setting.
Trong extension dùng module có sẵn:
- `self.StyleAnchor.inject(prompt, block, {label:'CHARACTER'})` — chèn 1 prompt.
- `self.StyleAnchor.applyToMany(prompts, block, {label:'CHARACTER'})` — chèn hàng loạt (batch).
- `self.StyleAnchor.check(prompt, block)` → `{present, coverage}` — kiểm 1 prompt đã có đủ khối chưa.
- `self.StyleAnchor.create(name, block, {kind:'character'})` — lưu để tái dùng sau; `strip()` gỡ khi sửa.

### 4. Verify nhất quán
Sau khi gen: so từng ảnh với block (mặt/wardrobe/proportions) — lệch thì REGENERATE với block gắn chặt
hơn (thêm "no morphing"), KHÔNG chấp nhận "gần giống".

## Output contract
1. **Khối CHARACTER/STYLE** (block tái dùng, ghi rõ label).
2. **Danh sách prompt** đã chèn block (bộ góc + các cảnh) — hoặc mã dùng StyleAnchor.
3. **Ghi chú nhất quán**: điều gì phải giữ bất biến, điều gì được đổi.

## Nguyên tắc
- Định nghĩa 1 lần — tái dùng nguyên văn; đừng mô tả lại mỗi lần (dễ trôi).
- Chỉ đổi pose/action/setting giữa các cảnh; giữ nguyên identity/wardrobe/palette.
- "Gần giống" = FAIL với nhân vật cần nhất quán.
