---
name: database-standard
description: Database design standards defining primary keys, foreign keys, audit fields, soft delete, junction tables. PostgreSQL style preferred, SQL lowercase without comments.
---

## Database Preferences

- **Forbidden**: MySQL
- **Recommended**: PostgreSQL or other modern databases
- **Required**: Foreign key constraints for data integrity

## SQL Code Style

- All **lowercase**
- SQL files have **no comments**

## Primary Key Standard

| Field | Type | Description |
|-------|------|-------------|
| `id` | bigint | Primary key, required for all regular tables |

## Audit Fields

All tables except junction tables MUST include:

| Field | Full Name | Type | Default | Description |
|-------|-----------|------|---------|-------------|
| `crd` | create row datetime | timestamp | current_timestamp | Row creation time, timezone-independent |
| `mrd` | modify row datetime | timestamp | null | Last modification time, timezone-independent, nullable |
| `rlv` | row lock version | integer | 0 | Optimistic lock version |

## Soft Delete Field

| Field | Full Name | Type | Default | Description |
|-------|-----------|------|---------|-------------|
| `ldf` | logic delete field | timestamp | null | Soft delete time, timezone-independent, null means active |

## Junction Table Standard

Tables linking two entities:
- **No primary key**
- **No audit fields**
- **Only** foreign key IDs from both tables

## Tree Structure

Tables with upward lookup (e.g., address) use `pid` for parent link:

| Field | Type | Description |
|-------|------|-------------|
| `pid` | bigint | Parent primary key, nullable |

## Examples

### Regular Table

```sql
create table user (
    id bigint primary key,
    name varchar(255) not null,
    email varchar(255),
    ldf timestamp,
    crd timestamp not null default current_timestamp,
    mrd timestamp,
    rlv integer not null default 0
);
```

### Junction Table

```sql
create table user_role (
    user_id bigint not null references user(id),
    role_id bigint not null references role(id)
);
```

### Tree Table

```sql
create table address (
    id bigint primary key,
    pid bigint references address(id),
    name varchar(255) not null,
    crd timestamp not null default current_timestamp,
    mrd timestamp,
    rlv integer not null default 0
);
```
