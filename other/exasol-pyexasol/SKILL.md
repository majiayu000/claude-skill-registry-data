---
name: exasol-pyexasol
description: "Use the official PyExasol Python driver for direct Exasol connections, queries, bulk I/O, metadata, UDF logs, and multiprocessing. Covers pyexasol.connect, connect_local_config, ExaConnection, ExaStatement, fetch_mapper, convert_websocket_to_python, execute_sql_script, create_prepared_statement, import_from_*, export_to_*, insert_multi, .meta, sql_columns, explain_last, execute_udf_output, http_transport, exa_address, export_parallel, import_parallel, exasol.driver.websocket.dbapi2, and EXASOL_TELEMETRY_DISABLE."
---

# Exasol PyExasol Skill

Use this skill for Python code that talks directly to Exasol through
`pyexasol`. For version-specific behavior, check the requested release in the
[official repository](https://github.com/exasol/pyexasol); do not mix APIs from
different releases.

## Routing Algorithm

Load only the matching references:

1. **Connect, query, format SQL, fetch, or transact**
   - Trigger phrases: `pyexasol.connect`, `connect_local_config`, `ExaConnection`, `ExaStatement`, `execute_sql_script`, `create_prepared_statement`, `fetch_mapper`, `!i`, `!q`, `!r`
   - Load: `references/connections-and-sql.md`

2. **Move data with HTTP transport**
   - Trigger phrases: `export_to_`, `import_from_`, `pandas`, `Polars`, `Parquet`, `insert_multi`, `export_params`, `import_params`
   - Load: `references/bulk-transfer.md`

3. **Inspect metadata or debug**
   - Trigger phrases: `.meta`, `sql_columns`, `list_tables`, `execute_udf_output`, `explain_last`, `debug_logdir`, `abort_query`
   - Load: `references/metadata-and-debugging.md`

4. **Run parallel HTTP transfer**
   - Trigger phrases: `http_transport`, `export_parallel`, `import_parallel`, `get_nodes`, `exa_address`, `multiprocessing`, `threadsafety`
   - Load: `references/parallel-http-transport.md`

5. **Use the PEP 249 interface**
   - Trigger phrases: `exasol.driver.websocket.dbapi2`, `DB-API 2.0`, `PEP 249`, `cursor`, `executemany`, `paramstyle`, `SQLAlchemy`
   - Load: `references/dbapi.md`

Load every reference that matches.

## Security

- Read credentials from the application's secret source. Never put them in
  source code, command arguments, logs, or chat output.
- Keep TLS and certificate verification enabled. Disable verification only for
  an explicit local test and label it unsafe for production.
- Use PyExasol placeholders. Never join user input into SQL, and use `!r` only
  for a closed set of trusted SQL fragments.
- Do not share a connection across threads or processes. `abort_query()` is the
  only supported cross-thread connection call.

## Related Skills

- Use **exasol-notebook-connections** for `open_pyexasol_connection` and other
  notebook-connector wrappers.
- Use **exasol-database** for Exasol SQL or exapump without PyExasol.
- Use **exasol-import** and **exasol-export** for native SQL or exapump data
  movement without PyExasol.
- Use **exasol-udfs** to build UDFs; this skill only covers their captured logs.
