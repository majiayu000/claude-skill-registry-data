---
name: migration
description: Creating and applying an EF Core database migration in any backend microservice. Triggers when a new Entity is added, a column is added/renamed/removed, a DbSet is added to ApplicationDbContext, or after any Domain model change that requires schema update.
---

## Nguyên tắc bắt buộc

1. **Tuân thủ tuyệt đối** quy trình và checklist được định nghĩa trong skill này — không bỏ qua bước rollback test, không dùng `DROP TABLE` trong `Up()`.
2. **Hỏi trước khi chạy** nếu bất kỳ yêu cầu nào chưa rõ (tên migration, có data cần seed không, bảng nào đang có data production). Không đoán mò — một câu hỏi ngắn tốt hơn một migration phá data.

---

# BE Migration Pattern

## Create migration

```bash
# Run from Api project directory
dotnet ef migrations add {MigrationName} -p ../ServiceName.Infrastructure -s .
```

Migration name must describe the change:
- `AddBatteryTable`
- `AddBatteryStatusColumn`
- `CreateTicketTable`
- `RenameLocationCodeColumn`

## Apply migration

```bash
dotnet ef database update -p ../ServiceName.Infrastructure -s .
```

## Rollback test (required when schema changes)

```bash
dotnet ef database update {PreviousMigrationName} -p ../ServiceName.Infrastructure -s .
dotnet ef database update -p ../ServiceName.Infrastructure -s .  # re-apply
```

## NOT NULL column on existing table — seed first

```csharp
// In Up() — populate before adding constraint
migrationBuilder.Sql("UPDATE batteries SET status = 1 WHERE status IS NULL");
migrationBuilder.AlterColumn<int>("status", "batteries", nullable: false, defaultValue: 1);
```

## Checklist before commit

- [ ] Migration name clearly describes the change
- [ ] `Down()` method exists and works
- [ ] NOT NULL columns have `defaultValue` or data seeding
- [ ] Rename uses `RenameColumn`, not drop + recreate
- [ ] Rollback tested: `update [prev]` → `update` succeeds
- [ ] No `DROP TABLE` or `TRUNCATE` in `Up()` / `Down()`

## TimescaleDB vs PostgreSQL

- Sensor readings, time-series → **TimescaleDB** (hypertable)
- Users, tickets, configs, battery configs → **PostgreSQL**
