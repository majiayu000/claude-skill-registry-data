---
name: vn-law-check
description: "Rà soát/audit một website hoặc mobile app theo pháp luật Việt Nam về bảo vệ dữ liệu cá nhân, thương mại điện tử, an ninh mạng, bảo vệ người tiêu dùng, quảng cáo trực tuyến, giao dịch điện tử và minh bạch AI. Dùng khi người dùng yêu cầu audit/kiểm tra/rà soát pháp lý website theo luật VN, hỏi về tuân thủ NĐ 356/2025, Luật Bảo vệ dữ liệu cá nhân, Luật Thương mại điện tử 2025, hoặc cần checklist compliance cho site Việt Nam. Cũng dùng khi người dùng muốn soạn chính sách bảo mật/chính sách bảo vệ dữ liệu cá nhân, form đồng ý, banner cookie đúng luật VN cho dự án. Also use for English requests: Vietnam legal compliance audit, Vietnamese privacy law (PDPL), Decree 356/2025, Vietnam e-commerce law, Vietnam cybersecurity law, website or mobile app compliance check for Vietnamese users."
---

# VN Web Compliance Audit

Rà soát (audit) một website theo quy định pháp luật Việt Nam hiện hành liên quan đến: bảo vệ dữ liệu cá nhân, thương mại điện tử, an ninh mạng/lưu trữ dữ liệu, bảo vệ người tiêu dùng, quảng cáo trực tuyến, giao dịch điện tử, và minh bạch AI (nếu áp dụng).

## Nguyên tắc bắt buộc

1. **Không khẳng định dứt khoát** "website này vi phạm/không vi phạm pháp luật". Đây là công cụ hỗ trợ rà soát ban đầu, không phải tư vấn pháp lý chính thức.
2. **Luôn trích dẫn số hiệu văn bản pháp luật cụ thể** (số văn bản, ngày ban hành/hiệu lực, điều khoản nếu biết) cho mỗi mục kiểm tra. Không bịa số hiệu. Nếu không chắc, nói rõ "cần tra cứu lại".
3. Luật Việt Nam về dữ liệu cá nhân, TMĐT, an ninh mạng đang trong giai đoạn chuyển tiếp mạnh (nhiều luật mới 2025 có hiệu lực trong 2026, một số nghị định xử phạt chưa ban hành hoặc chưa xác minh được). Mục nào checklist ghi "CHƯA XÁC MINH" thì chỉ dẫn tên văn bản, không tự điền số điều hay mức phạt. Luôn khuyến nghị người dùng xác minh lại văn bản còn hiệu lực tại thuvienphapluat.vn hoặc vbpl.vn. Đọc ngày "Cập nhật" ở đầu `sources/legal-references.md`: nếu cách ngày audit hơn 3 tháng, ghi một dòng cảnh báo ở đầu báo cáo rằng dữ liệu luật của bộ checklist có thể đã cũ.
4. Mỗi phát hiện phân loại mức độ: 🔴 Cần xử lý ngay / 🟡 Nên cải thiện / 🟢 Đạt yêu cầu / ⚪ Không áp dụng. Với site nhỏ, nghĩa vụ giấy tờ, thủ tục chỉ xếp tối đa 🟡 và gom ở cuối báo cáo; 🔴 dành cho lỗi sửa được trong code (xem "Mức ưu tiên" trong `references/00-triage.md`).
5. Luôn khuyến nghị tham vấn luật sư cho quyết định cuối cùng, đặc biệt với mục 🔴.
6. Tự xác định loại hình website bằng cách quét code/nội dung thực tế (xem `references/00-triage.md`). Không đoán bừa, nhưng cũng không hỏi người dùng nếu quét được. Chỉ hỏi lại khi quét xong vẫn không xác định được.
7. **Mức phạt chỉ lấy từ `references/08-penalties-reference.md`.** Hành vi nào bảng đó không có mức cụ thể thì ghi "mức phạt: CHƯA XÁC MINH", không tự đưa con số từ trí nhớ, không cộng dồn, không suy từ mức trần (ví dụ không ghi "tới 5% doanh thu" cho lỗi không phải chuyển dữ liệu xuyên biên giới). Không viết "sẽ bị đình chỉ/tạm dừng hoạt động" nếu checklist không dẫn căn cứ cụ thể.
8. Chỉ báo cáo những gì nằm trong phạm vi các checklist. Vấn đề ngoài phạm vi (bản quyền hình ảnh, file LICENSE, lỗi bảo mật code, thuế...) nếu thấy thì ghi một dòng "ngoài phạm vi, nên kiểm tra riêng", không xếp mức 🔴 và không gán điều luật hay mức phạt. Chỉ dùng thang 🔴🟡🟢⚪, không tự đặt nhãn khác (P0, Critical...).

## Quy trình

1. **Luôn bắt đầu bằng `references/00-triage.md`**: phân loại mức độ phức tạp (tĩnh/thu thập nhẹ/bán hàng/nền tảng quy mô) trước khi mở checklist nào. Chạy `bash scripts/scan.sh <thư-mục-code>`, hoặc `bash scripts/scan.sh <URL>` nếu chỉ có địa chỉ website, để quét tự động, rồi xem lại bằng chứng script in ra. Site tĩnh không form, không script theo dõi, không bán hàng thì KHÔNG audit đủ bộ checklist.
2. Theo bảng phân loại ở bước 1, chỉ mở checklist thực sự áp dụng tại `references/`: 01-personal-data-protection, 02-ecommerce, 03-cybersecurity, 04-consumer-protection, 05-advertising, 06-electronic-transactions, 07-ai-transparency (luôn thêm nếu có chatbot/nội dung AI), 08-penalties-reference, 09-mobile-app (luôn thêm nếu là mobile app), 10-generate-policy (khi người dùng yêu cầu soạn chính sách bảo mật/form đồng ý).
3. Đọc code/nội dung website thực tế (footer, trang chính sách, cookie banner, form thu thập dữ liệu) để xác định trạng thái. Chưa kiểm tra thì không suy đoán.
4. Xuất báo cáo theo mẫu `examples/sample-audit-report.md`. Với site mức 0-1, dùng bản rút gọn, không liệt kê các checklist không áp dụng thành bảng dài.
5. Mở đầu báo cáo bằng dòng "🤖 Báo cáo do AI tạo..." theo `examples/sample-audit-report.md`, và đóng báo cáo bằng phần "Giới hạn & Khuyến nghị" (xem `DISCLAIMER.md`).
6. Site thu thập dữ liệu mà thiếu chính sách hoặc xin đồng ý sai: cuối báo cáo gợi ý người dùng có thể bảo "soạn chính sách bảo mật cho dự án này". Khi được yêu cầu, làm theo `references/10-generate-policy.md` với khung `examples/privacy-policy-template.md`.

Nguồn pháp luật đầy đủ: `sources/legal-references.md`.
