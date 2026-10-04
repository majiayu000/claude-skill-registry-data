---
name: record-security
description: >
    Configure record-level security (RLS) per record type on Frontline objects
    using the Frontline CLI. Use when the user wants to enable/disable RLS,
    set virtual owner columns, or manage who can see and edit records based on
    User-relation fields.
allowed-tools: Bash(frontline:*)
---

# Record-level security (RLS)

**Record-level security** (also referred to as **RLS**; legacy docs may say "FLS") restricts which users can view or edit individual records within a record type.

> **Config lives on the record type**, not on the object. Two record types on the same object can have different RLS settings.

When enabled, access is driven by **virtual owner columns**: User-relation fields on the record type (e.g. a `Users` column). Users referenced in those fields become virtual owners of the record.

> RLS is different from **record sharing** (per-record `_grants`) and **resource sharing** (who can access the object schema). See the `sharing` skill for those.

## Prerequisites

- Authenticate with `frontline auth login <api-key>`.
- Requires a **USER API key** with **ADMIN** or **OWNER** role.
- Know the object name and record type ID (`frontline object record-type list <object>`).
- Know field IDs for User-relation columns (`frontline object get <object>` or `frontline object field list <object>`).

## Get security config

```bash
frontline object record-type security get <object-name> <record-type-id>
```

Example:

```bash
frontline object record-type security get people 3
```

Output:

```json
{
    "ok": true,
    "data": {
        "enabled": false,
        "workspace": "FULL_ACCESS",
        "virtual_owner_column_ids": [42],
        "virtual_owner_columns": [{ "id": 42, "name": "Users", "key": "users" }]
    }
}
```

Scripting: `jq '.data.enabled'`, `jq '.data.workspace'`, `jq '.data.virtual_owner_column_ids[]'`.

If no config has been saved yet, returns in-memory defaults (`enabled: false`, auto-detected `Users` column if present). Nothing is written to the database until you run `update`.

## Update security config

```bash
frontline object record-type security update <object-name> <record-type-id> --data '<json>'
```

Example — enable RLS with a Users column:

```bash
frontline object record-type security update people 3 --data '{
  "enabled": true,
  "virtual_owner_column_ids": [42]
}'
```

Example — set workspace default to read-only (account can view new records, not edit):

```bash
frontline object record-type security update people 3 --data '{
  "enabled": true,
  "virtual_owner_column_ids": [42],
  "workspace": "READ_ONLY"
}'
```

Supported keys in `--data` JSON:

| Key                        | Type     | Notes                                                                                                                                                                       |
| -------------------------- | -------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `enabled`                  | boolean  | Turn RLS on/off for this record type                                                                                                                                        |
| `virtual_owner_column_ids` | number[] | User-relation field IDs (aliases: `virtualOwnerColumnIds`)                                                                                                                  |
| `workspace`                | enum     | `FULL_ACCESS`, `READ_ONLY`, or `NO_ACCESS` — default for **new** records when RLS is on. Aliases: `default_workspace_record_permission`, `defaultWorkspaceRecordPermission` |

All body fields are optional (partial update). **Unknown keys return `400`** (strict validation).

When you **enable** RLS for the first time **without** setting `workspace`:

- If the record type workspace default is still `FULL_ACCESS`, it is automatically set to `NO_ACCESS` (owner-only by default).
- Existing rows with no `_grants` are backfilled to private when workspace ends up `NO_ACCESS`.

Set `workspace` explicitly to `READ_ONLY` or `FULL_ACCESS` before or while enabling to avoid the auto `NO_ACCESS` default.

## Rules

- Config is **per record type** — not per object.
- `virtual_owner_column_ids` must reference **User-relation fields** assigned to the record type. Other field types return `400`.
- RLS enforcement only activates after an admin saves config. Until then, all account users retain normal access.
- Admins and owners always bypass RLS restrictions.
- There is **no CLI grant** to give a non-owner read/list access except: make them a **virtual owner** (User-relation column), add **per-record sharing** (`_grants`), or set workspace default to `FULL_ACCESS` / `READ_ONLY` on the record type.

## Public API / CLI enforcement (expected behavior)

Applies to `object record list`, `get`, `update` (and the app UI — same backend).

Distinguish two response fields:

| Field                | Meaning                                                       |
| -------------------- | ------------------------------------------------------------- |
| `_recordAccess`      | Record-type CRUD flags (account/team permissions on the type) |
| `_recordShareAccess` | Per-record RLS/share level (`FULL`, `EDIT`, `VIEW`, `NONE`)   |

### RLS OFF (`enabled: false`)

| Operation  | Non-admin USER                    | Admin   |
| ---------- | --------------------------------- | ------- |
| **list**   | All rows of readable record types | All     |
| **get**    | Allowed if record-type `read`     | Allowed |
| **update** | Allowed if record-type `update`   | Allowed |

### RLS ON + workspace `NO_ACCESS` (default after first enable)

| Operation  | Owner (manual or virtual)         | Non-owner USER | Admin   |
| ---------- | --------------------------------- | -------------- | ------- |
| **list**   | Own rows (+ shared grants if any) | Hidden         | All     |
| **get**    | Allowed                           | `404` / denied | Allowed |
| **update** | Allowed                           | `403`          | Allowed |

### RLS ON + workspace `READ_ONLY`

New records get account-wide **view** access (`_grants: [{ scope: "account", level: "VIEW" }]`).

| Operation          | Non-owner USER                         | Owner   |
| ------------------ | -------------------------------------- | ------- |
| **list** / **get** | Allowed (`_recordShareAccess`: `VIEW`) | Allowed |
| **update**         | `403`                                  | Allowed |

### RLS ON + workspace `FULL_ACCESS`

New records are **open** to the whole account (`_grants` empty). Non-owners can read and edit unless the record is made private via sharing.

| Operation            | Non-owner USER                                      |
| -------------------- | --------------------------------------------------- |
| **list**             | All open rows + granted rows                        |
| **get** / **update** | Allowed on open rows (`_recordShareAccess`: `EDIT`) |

## Output notes

- SOR endpoints return `{ ok: true, data: … }` on success (same as other `object` / `table` commands).
- `--pretty` is not supported on `record-type security` commands; use default JSON + `jq`.

## Troubleshooting

| Error                                | Cause                                                                               |
| ------------------------------------ | ----------------------------------------------------------------------------------- |
| `403 Forbidden`                      | API key user is not ADMIN or OWNER                                                  |
| `400 Bad Request`                    | Invalid `virtual_owner_column_ids`, invalid `workspace` value, or unknown body keys |
| `404 Not Found`                      | Object or record type ID doesn't exist                                              |
| list returns 0 for USER with RLS OFF | Usually record-type read permissions; verify with an admin key                      |

## See also

- [Record Types concept](https://docs.getfrontline.ai/docs/concepts/record-types) — record type operations and RLS overview
- `record-type-management` skill — create/update record types and assign fields
- `sharing` skill — per-record and per-resource sharing permissions
