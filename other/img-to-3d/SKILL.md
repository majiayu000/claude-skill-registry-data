---
name: img-to-3d
description: >-
  Dựng lại vật thể trong 1 ảnh tham chiếu thành model Three.js CODE-ONLY, procedural, animation-ready
  (không depth-map/point-cloud/photogrammetry). Dùng khi user muốn biến 1 ảnh sản phẩm/vật thể thành
  scene 3D web nhẹ, hoặc cần asset Three.js sinh bằng code. ADJACENT (ngoài core gen ảnh Flow) — dùng
  pattern spec→gate→build→visual-diff, tốn token CHỈ cho so-sánh-nhìn. Học img2threejs.
---

# SEOSONA — Image → Three.js (procedural, code-only)

Dựng model 3D từ ảnh bằng **CODE Three.js primitives**, KHÔNG reconstruct mesh/depth. Theo pattern lõi
spec→gate→build (xem skill spec-gate-build) — model chỉ tốn token cho phần **so ảnh render vs ảnh gốc**.

## 8-pass sculpting (từ img2threejs)
1. **Intake/analysis** — phân tích ảnh: hình khối chính, tỉ lệ, vật liệu, màu, phần động.
2. **ObjectSculptSpec (JSON)** — spec cấu trúc: các khối primitive (box/sphere/cylinder…), transform, material, hierarchy, socket/collider.
3. **Quality gate** — validate spec (đủ khối? tỉ lệ hợp lý?) trước khi build.
4. **Blockout** — dựng khối thô Three.js.
5. **Structural** — chi tiết cấu trúc + hierarchy.
6. **Material** — vật liệu PBS + màu bám ảnh.
7. **Lighting + interaction** — đèn + socket/animation group.
8. **Optimization** — gộp geometry, giảm draw-call.

## Vòng verify (token chỉ cho phần nhìn)
- **Browser screenshot** scene vs ảnh gốc → vision model chấm khác biệt (bố cục/tỉ lệ/màu) → feedback → sửa pass.
- Phần gate/validate/optimize = code deterministic (không tốn model).

## Output
- `ObjectSculptSpec` (JSON) + TS factory trả `THREE.Group` (có socket/collider nếu cần).
- Kết quả verify: diff vs ảnh gốc + verdict.

## Lưu ý scope
- ĐÂY LÀ ADJACENT — SEOSONA Flow core là gen ẢNH/VIDEO qua web-UI, không phải 3D. Dùng skill này khi thật sự cần asset Three.js; đừng ép vào luồng gen ảnh.
- Không depth-map/photogrammetry — chỉ primitive + procedural (nhẹ, animation-ready, git-diffable).
