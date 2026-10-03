---
name: scaffold-crud
description: Scaffold complete CRUD cho một entity — tạo tất cả files (Entity, Enum, DTOs, 4 Commands, 2 Queries, Controller, UoW update, Migration)
argument-hint: [ServiceName EntityName]
allowed-tools: Bash, Write, Read, Edit
---

# Scaffold Full CRUD `$ARGUMENTS`

Usage: `/scaffold-crud ServiceName EntityName`  
Example: `/scaffold-crud BatteryService Battery`

Skill này tạo **tất cả files** cho một CRUD feature hoàn chỉnh.

## Files sẽ tạo (16 files)

### Domain (2)
1. `Domain/Entities/{Entity}.cs`
2. `Domain/Enums/{Entity}StatusEnum.cs`

### Application (13)
3. `Application/DTOs/Response/{Entity}Response.cs` — DTO + nested DTOs + response wrappers
4. `Application/Commands/{Entity}Create/{Entity}CreateCommand.cs`
5. `Application/Commands/{Entity}Create/{Entity}CreateCommandHandler.cs`
6. `Application/Commands/{Entity}Update/{Entity}UpdateCommand.cs`
7. `Application/Commands/{Entity}Update/{Entity}UpdateCommandHandler.cs`
8. `Application/Commands/{Entity}Delete/{Entity}DeleteCommand.cs`
9. `Application/Commands/{Entity}Delete/{Entity}DeleteCommandHandler.cs`
10. `Application/Commands/{Entity}Restore/{Entity}RestoreCommand.cs`
11. `Application/Commands/{Entity}Restore/{Entity}RestoreCommandHandler.cs`
12. `Application/Queries/{Entity}GetList/{Entity}GetListQuery.cs`
13. `Application/Queries/{Entity}GetList/{Entity}GetListQueryHandler.cs`
14. `Application/Queries/{Entity}GetById/{Entity}GetByIdQuery.cs`
15. `Application/Queries/{Entity}GetById/{Entity}GetByIdQueryHandler.cs`

### Api (1)
16. `Api/Controllers/{Entity}Controller.cs`

### Files Updated (3)
- `Infrastructure/Persistence/ApplicationDbContext.cs` — add DbSet
- `Application/Interfaces/I{Service}UnitOfWork.cs` — add repository
- `Infrastructure/Implements/UnitOfWork.cs` — init repository

### Migration (1)
- `dotnet ef migrations add Add{Entity}`

## Thứ tự thực hiện

Chạy các skills theo thứ tự:

1. `/scaffold-entity {Service} {Entity}`
2. `/scaffold-dto {Service} {Entity}`
3. `/scaffold-cqrs-command {Service} {Entity} Create`
4. `/scaffold-cqrs-command {Service} {Entity} Update`
5. `/scaffold-cqrs-command {Service} {Entity} Delete`
6. `/scaffold-cqrs-command {Service} {Entity} Restore`
7. `/scaffold-cqrs-query {Service} {Entity} GetList`
8. `/scaffold-cqrs-query {Service} {Entity} GetById`
9. `/scaffold-controller {Service} {Entity}`
10. `/run-migration {Service} Add{Entity}`

## API Endpoints sau khi hoàn thành

| Method | Route | Auth | Handler |
|--------|-------|------|---------|
| GET | `/api/{entities}` | Public | {Entity}GetListQueryHandler |
| GET | `/api/{entities}/{id}` | Public | {Entity}GetByIdQueryHandler |
| POST | `/api/{entities}` | Auth | {Entity}CreateCommandHandler |
| PUT | `/api/{entities}/{id}` | Auth | {Entity}UpdateCommandHandler |
| DELETE | `/api/{entities}/{id}` | Admin | {Entity}DeleteCommandHandler |
| PATCH | `/api/{entities}/{id}` | Admin | {Entity}RestoreCommandHandler |

## Query Params cho GetList

- `?searchTerm=abc` — text search
- `?status=1` — enum filter
- `?parentId=guid` — FK filter
- `?isDeleted=false` — soft delete filter
- `?isDescending=true` — ordering
- `?fields=id,name,status` — data shaping
- `?hasParent=true` — conditional include
- `?pageNumber=1&pageSize=10` — pagination
