---
name: db-migrate
description: Safely modify the Drizzle schema and create a migration for FixNow Postgres. Validates the change against docs/database-schema.md, runs drizzle-kit generate then migrate, and updates the schema doc. Use when user says "thêm field X vào users", "đổi enum status", "add Review table", "tạo migration".
---

# db-migrate

Thay đổi schema Drizzle + tạo migration an toàn.

## Trước khi chạy

1. **Đọc** `db/schema.ts` hiện tại + `docs/database-schema.md`.
2. **Hỏi user**: thay đổi cụ thể là gì? (thêm cột / đổi type / thêm table / drop / thêm index).
3. **Đánh giá rủi ro**:
   - Drop column → mất data. WARNING.
   - Rename column → drizzle-kit không detect rename, sẽ drop+add (mất data). Phải edit SQL tay.
   - Đổi field nullable → required → cần default cho row cũ.
   - Đổi enum → ALTER TYPE trong Postgres phức tạp.
   - Đổi index → an toàn.

Nếu rủi ro cao → **STOP, xin xác nhận từ user**.

## Workflow

### 1. Sửa `db/schema.ts`

Tuân thủ:
- snake_case ở DB, camelCase ở TS.
- Mọi table có `id`, `createdAt`, `updatedAt`.
- Index explicit qua extra config arg thứ 2.
- Định nghĩa `relations()` nếu có FK.

### 2. Generate migration

```bash
npx drizzle-kit generate
```

File SQL xuất ở `drizzle/<timestamp>_<auto_name>.sql`. Đọc kỹ trước khi apply.

### 3. Đọc + verify SQL

Kiểm tra:
- `CREATE TABLE` đúng các column + type.
- `ALTER TABLE ... ADD COLUMN` có `DEFAULT` nếu NOT NULL.
- Không có `DROP COLUMN` / `DROP TABLE` ngoài ý muốn.
- Index name + columns đúng.

Nếu phát hiện rename bị nhầm thành drop+add → **sửa file SQL tay** thành `ALTER TABLE ... RENAME COLUMN ...`.

### 4. Apply migration

```bash
npx drizzle-kit migrate
```

Hoặc test trước trên DB scratch:
```bash
# Tạo tạm DB test
# psql -c "CREATE DATABASE fixnow_test;"
# DATABASE_URL=postgresql://...fixnow_test npx drizzle-kit migrate
```

### 5. Update docs

Sửa `docs/database-schema.md`:
- Thêm table/column mới vào schema mẫu.
- Cập nhật phần "Giải thích quyết định" nếu non-trivial.

### 6. Verify TypeScript

```bash
npx tsc --noEmit
```

Schema thay đổi sẽ phản ánh ngay ở types.

### 7. Update seed nếu cần

Nếu table mới hoặc column NOT NULL mới → cập nhật `db/seed.ts`. Xem skill `seed-fixtures`.

## Migration không an toàn (cần confirm)

- **Drop column với data**: generate, mở SQL, confirm với user. Nếu đồng ý → apply.
- **Rename column**: edit SQL tay sau khi generate (drizzle-kit chỉ drop+add).
- **Đổi enum value đã dùng**: dùng `ALTER TYPE ... ADD VALUE` thủ công, không drop enum.
- **Đổi PK type**: gần như không thể không reset. Cảnh báo user.

## Đã commit → không sửa migration cũ

Migration history phải immutable trong git. Cần đổi → tạo migration mới revert + apply lại.

## Checklist

- [ ] Schema cập nhật trong `docs/database-schema.md`.
- [ ] Migration tạo bằng `drizzle-kit generate`, không `push` (trừ prototype).
- [ ] SQL được đọc trước khi `migrate`.
- [ ] `npx tsc --noEmit` pass.
- [ ] `db/seed.ts` đã update nếu cần.
- [ ] Commit cả `db/schema.ts` + `drizzle/<new>.sql` + `drizzle/meta/_journal.json`.

## Liên kết

- Complex schema design → spawn agent `fixnow-drizzle-modeler`.
- Sau migration → skill `seed-fixtures` để có data demo.
