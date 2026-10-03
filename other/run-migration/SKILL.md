---
name: run-migration
description: Generate và apply EF Core migration cho một microservice
argument-hint: [ServiceName MigrationName]
allowed-tools: Bash, Read
---

# Run EF Core Migration `$ARGUMENTS`

Usage: `/run-migration ServiceName MigrationName`  
Example: `/run-migration BatteryService AddBattery`

## Generate Migration

```bash
cd services/{Service}/src/{Service}.Api
dotnet ef migrations add {MigrationName} -p ../{Service}.Infrastructure -s .
```

**Flags:**
- `-p` (project): Infrastructure project (nơi DbContext)
- `-s` (startup): Api project (nơi Program.cs)

## Apply Migration

```bash
dotnet ef database update -p ../{Service}.Infrastructure -s .
```

## Verify

```bash
ls -la ../{Service}.Infrastructure/Persistence/Migrations/
```

## Migration Name Convention

| Action | Pattern | Example |
|--------|---------|---------|
| Entity mới | `Add{Entity}` | `AddBattery` |
| Thêm field | `Add{Field}To{Entity}` | `AddVoltageThresholdToBattery` |
| Xóa field | `Remove{Field}From{Entity}` | `RemoveOldFieldFromBattery` |
| Schema ban đầu | `InitialCreate` | `InitialCreate` |
| Relationship | `Add{A}{B}Relation` | `AddBatteryTicketRelation` |

## Troubleshooting

```bash
# Xóa migration cuối (nếu chưa apply)
dotnet ef migrations remove -p ../{Service}.Infrastructure -s .

# Xem danh sách migrations
dotnet ef migrations list -p ../{Service}.Infrastructure -s .

# Generate SQL script để review
dotnet ef migrations script -p ../{Service}.Infrastructure -s .
```

## Rules
- LUÔN chạy từ Api project directory
- Migration name: PascalCase, mô tả rõ ràng
- Review migration file trước khi apply
- Auto-migrate on startup (`db.Database.Migrate()` trong Program.cs)
