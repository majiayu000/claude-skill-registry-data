---
name: db
description: "Skill for the DB area of Securacy. 25 symbols across 5 files."
---

# DB

25 symbols | 5 files | Cohesion: 75%

## When to Use

- Working with code in `backend/`
- Understanding how test_db_operations, get_user, update_user work
- Modifying db-related functionality

## Key Files

| File | Symbols |
|------|---------|
| `backend/buddlyai/DB/DBservice.py` | get_user, update_user, delete_user, insert_threat_run, insert_threat_data (+10) |
| `backend/buddlyai/Routes/UserController.py` | get_user, update_user, delete_user, create_user |
| `backend/buddlyai/Routes/ThreatsController.py` | save_threats, delete_threat, update_threat, get_threat_data |
| `backend/buddlyai/tests/test_dbservice_crud.py` | test_db_operations |
| `backend/buddlyai/tests/test_controller.py` | setup_module |

## Entry Points

Start here when exploring this area:

- **`test_db_operations`** (Function) — `backend/buddlyai/tests/test_dbservice_crud.py:11`
- **`get_user`** (Function) — `backend/buddlyai/Routes/UserController.py:50`
- **`update_user`** (Function) — `backend/buddlyai/Routes/UserController.py:67`
- **`delete_user`** (Function) — `backend/buddlyai/Routes/UserController.py:84`
- **`save_threats`** (Function) — `backend/buddlyai/Routes/ThreatsController.py:62`

## Key Symbols

| Symbol | Type | File | Line |
|--------|------|------|------|
| `test_db_operations` | Function | `backend/buddlyai/tests/test_dbservice_crud.py` | 11 |
| `get_user` | Function | `backend/buddlyai/Routes/UserController.py` | 50 |
| `update_user` | Function | `backend/buddlyai/Routes/UserController.py` | 67 |
| `delete_user` | Function | `backend/buddlyai/Routes/UserController.py` | 84 |
| `save_threats` | Function | `backend/buddlyai/Routes/ThreatsController.py` | 62 |
| `delete_threat` | Function | `backend/buddlyai/Routes/ThreatsController.py` | 129 |
| `update_threat` | Function | `backend/buddlyai/Routes/ThreatsController.py` | 150 |
| `get_threat_data` | Function | `backend/buddlyai/Routes/ThreatsController.py` | 231 |
| `get_user` | Function | `backend/buddlyai/DB/DBservice.py` | 95 |
| `update_user` | Function | `backend/buddlyai/DB/DBservice.py` | 107 |
| `delete_user` | Function | `backend/buddlyai/DB/DBservice.py` | 129 |
| `insert_threat_run` | Function | `backend/buddlyai/DB/DBservice.py` | 149 |
| `insert_threat_data` | Function | `backend/buddlyai/DB/DBservice.py` | 234 |
| `get_threat_runs` | Function | `backend/buddlyai/DB/DBservice.py` | 246 |
| `get_threat_data` | Function | `backend/buddlyai/DB/DBservice.py` | 257 |
| `update_threat_run` | Function | `backend/buddlyai/DB/DBservice.py` | 389 |
| `delete_threat_run` | Function | `backend/buddlyai/DB/DBservice.py` | 415 |
| `close` | Function | `backend/buddlyai/DB/DBservice.py` | 434 |
| `main` | Function | `backend/buddlyai/DB/DBservice.py` | 441 |
| `setup_module` | Function | `backend/buddlyai/tests/test_controller.py` | 19 |

## Execution Flows

| Flow | Type | Steps |
|------|------|-------|
| `Main → Connect` | cross_community | 4 |
| `Create_user → Connect` | intra_community | 4 |
| `Main → Commit` | cross_community | 3 |
| `Save_threats → Commit` | cross_community | 3 |

## Connected Areas

| Area | Connections |
|------|-------------|
| Securacymcp | 7 calls |

## How to Explore

1. `gitnexus_context({name: "test_db_operations"})` — see callers and callees
2. `gitnexus_query({query: "db"})` — find related execution flows
3. Read key files listed above for implementation details
