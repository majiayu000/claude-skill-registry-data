---
name: dat-ten
description: 'Quy chuẩn đặt tên file trong dự án SASUCO InvoiceEasy. Dùng khi: đặt tên Page, Dialog, Component, Hook, Service, Types, Utils; xác định shortName từ tên feature; phân biệt Business Portal vs Admin portal (suffix Admin); tên thư mục feature kebab-case; ví dụ thực tế như SPAApiServiceAdmin, comSPAAdmin.page.Table.tsx.'
---

# Quy Chuẩn Đặt Tên File — SASUCO InvoiceEasy

## Xác định `shortName`

| Tên Page | Cách lấy shortName |
|----------|-------------------|
| ≥ 3 từ: `InvoiceIssuanceManagement` | Lấy chữ cái đầu → `IIM` |
| ≤ 2 từ: `CustomerPage` | Giữ nguyên → `Customer` |

---

## Quy Tắc Đặt Tên Theo Loại File

| Loại | Business / Partner | Admin |
|------|--------------------|-------|
| **Page** | `{Name}Page.tsx` | `{Name}PageAdmin.tsx` |
| **Dialog** | `{shortName}Dialog.tsx` | `{shortName}DialogAdmin.tsx` |
| **Component (page)** | `com{shortName}.page.{Name}.tsx` | `com{shortName}Admin.page.{Name}.tsx` |
| **Component (dialog)** | `com{shortName}.dlg.{Name}.tsx` | `com{shortName}Admin.dlg.{Name}.tsx` |
| **Hook (page)** | `use{shortName}.page.{name}.ts` | `use{shortName}Admin.page.{name}.ts` |
| **Hook (dialog)** | `use{shortName}.dlg.{name}.ts` | `use{shortName}Admin.dlg.{name}.ts` |
| **Service** | `{shortName}ApiService.ts` | `{shortName}ApiServiceAdmin.ts` |
| **Types** | `{shortName}.types.ts` / `.types.ui.ts` / `.types.api.ts` | Không cần suffix Admin |
| **Utils** | `{shortName}.util.ts` | Không cần suffix Admin |

> **Admin suffix** áp dụng cho: Pages, Components, Dialogs, Hooks, Services  
> **KHÔNG áp dụng** suffix Admin cho: Types, Utils, Docs

---

## Tên Thư Mục Feature

- Dùng `kebab-case`, phản ánh nghiệp vụ
- Ví dụ: `quan-ly-hoa-don`, `service-price-manage`, `invoice-template`

---

## Ví Dụ Thực Tế

Feature: `service-price-manage` → shortName = `SPA`

| File | Tên chuẩn |
|------|-----------|
| Page (Admin) | `ServicePriceAdminPage.tsx` |
| Dialog (Admin) | `SPADialogAdmin.tsx` |
| Hook page (Admin) | `useSPA.page.fetchData.ts` |
| Hook dialog (Admin) | `useSPA.dlg.form.ts` |
| Service (Admin) | `SPAApiServiceAdmin.ts` |
| Types | `service-price.types.ts` |
| Component table (Admin) | `comSPAAdmin.page.Table.tsx` |

---

## Lưu Ý Quan Trọng

> ⚠️ **File cũ đã tồn tại: KHÔNG đổi tên khi không có yêu cầu rõ ràng.**

---


