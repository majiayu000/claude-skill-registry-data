---
name: Cloudflare Workers Bindings
description: This skill should be used when the user asks about "KV namespace", "R2 bucket", "D1 database", "Hyperdrive", "create binding", "list workers", "worker code", "storage binding", "database query", "object storage", "key-value store", "connection pooling", or needs to manage Cloudflare Workers storage and compute resources.
version: 1.0.0
---

# Cloudflare Workers Bindings

Manage Cloudflare Workers storage and compute bindings using the Workers Bindings MCP server.

## Available Tools

### Account Management
| Tool | Purpose |
|------|---------|
| `accounts_list` | List all accounts |
| `set_active_account` | Set the active account for subsequent operations |

### Workers
| Tool | Purpose |
|------|---------|
| `workers_list` | List all Workers in the account |
| `workers_get_worker` | Get Worker details |
| `workers_get_worker_code` | Retrieve Worker source code |

### KV Namespaces
| Tool | Purpose |
|------|---------|
| `kv_namespaces_list` | List all KV namespaces |
| `kv_namespace_create` | Create a new KV namespace |
| `kv_namespace_get` | Get namespace details |
| `kv_namespace_update` | Update namespace settings |
| `kv_namespace_delete` | Delete a namespace |

### R2 Buckets
| Tool | Purpose |
|------|---------|
| `r2_buckets_list` | List all R2 buckets |
| `r2_bucket_create` | Create a new bucket |
| `r2_bucket_get` | Get bucket details |
| `r2_bucket_delete` | Delete a bucket |

### D1 Databases
| Tool | Purpose |
|------|---------|
| `d1_databases_list` | List all D1 databases |
| `d1_database_create` | Create a new database |
| `d1_database_get` | Get database details |
| `d1_database_query` | Execute SQL queries |
| `d1_database_delete` | Delete a database |

### Hyperdrive
| Tool | Purpose |
|------|---------|
| `hyperdrive_configs_list` | List Hyperdrive configurations |
| `hyperdrive_config_create` | Create new config |
| `hyperdrive_config_get` | Get config details |
| `hyperdrive_config_edit` | Modify config |
| `hyperdrive_config_delete` | Delete config |

## Common Workflows

### Set Up Account First
Always start by setting the active account:
1. Use `accounts_list` to see available accounts
2. Use `set_active_account` with the desired account ID

### Create Storage Binding
1. Create the resource (`kv_namespace_create`, `r2_bucket_create`, or `d1_database_create`)
2. Note the resource ID returned
3. Add binding to wrangler.toml (manual step)

### Inspect Worker
1. Use `workers_list` to find the worker
2. Use `workers_get_worker` for metadata
3. Use `workers_get_worker_code` to review source

### Query D1 Database
1. Use `d1_databases_list` to find database ID
2. Use `d1_database_query` with SQL statement

## Tips

- Always set the active account before other operations
- Resource creation returns IDs needed for wrangler.toml bindings
- D1 queries support standard SQLite syntax
- R2 is S3-compatible for object operations
