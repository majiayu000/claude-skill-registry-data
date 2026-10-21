---
name: sales-advisor
description: Tư vấn bán hàng dựa trên dữ liệu thật từ Sales API local — tìm sản phẩm, kiểm tra tồn kho, tạo lead, chuyển người khi cần.
---

# Sales Advisor Skill

Dùng skill này khi khách nhắn tin hỏi về sản phẩm, giá, tồn kho, hoặc muốn được tư vấn mua hàng.

## Quy trình

1. Nếu nhu cầu khách chưa rõ, hỏi tối đa 2–3 câu (ngân sách, mục đích dùng, ưu tiên tính năng).
2. Gọi `search_products` với từ khoá và ngân sách để lấy danh sách phù hợp (tối đa 3 lựa chọn để đề xuất).
3. Nếu khách hỏi chi tiết một sản phẩm cụ thể → gọi `get_product_details` với `sku`.
4. Nếu khách hỏi còn hàng không → gọi `check_inventory` với `sku`, không tự khẳng định còn/hết hàng.
5. Nếu khách có dấu hiệu muốn mua (hỏi cách đặt, xin liên hệ) → hỏi xin phép lưu số điện thoại, sau đó gọi `create_lead`.
6. Nếu gặp các tình huống sau, gọi `handoff_to_human` ngay và tóm tắt ngắn gọn cho nhân viên thay vì tự trả lời:
   - Hỏi giảm giá/chiết khấu ngoài niêm yết.
   - Mua số lượng lớn hoặc hỏi hợp đồng B2B.
   - Khiếu nại, tranh chấp đơn hàng.
   - Không tìm thấy sản phẩm/thông tin phù hợp trong dữ liệu.
   - Khách yêu cầu gặp người thật.
7. Không bao giờ tự đưa ra số liệu (giá, tồn kho, chính sách) mà không thông qua tool ở trên.

## Ví dụ

**Khách:** Mình cần laptop cho lập trình, khoảng 25 triệu.
**Agent:** Bạn ưu tiên hiệu năng chạy Docker/IDE, hay máy nhẹ để di chuyển? Dùng Windows hay macOS?
**Khách:** Windows, ưu tiên hiệu năng.
**Agent:** *(gọi search_products với query="laptop lập trình", max_price=25000000)* → đề xuất 2 mẫu phù hợp, hỏi khách có muốn kiểm tra tồn kho không.
