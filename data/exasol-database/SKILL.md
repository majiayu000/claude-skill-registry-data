---
name: exasol-database
description: "Exasol database interaction via the exapump CLI and Exasol SQL. Covers SQL queries and DML/DDL such as `SELECT`, `INSERT`, `UPDATE`, `DELETE`, `MERGE`, `CREATE TABLE`, `ALTER TABLE`, and `DROP TABLE`, `CREATE CONNECTION` connection objects without import or export intent, schema inspection, table design, `exapump sql` and `exapump profile`, query profiling, analytics, and Exasol-specific SQL behavior outside exasol-import and exasol-export."
---

# Exasol Database Skill

Trigger when the user asks for **Exasol database interaction**, **exapump**, **Exasol SQL**, **EXA_** system views, schemas, tables, or query execution outside **exasol-import** and **exasol-export**.

## Step 0: Establish Connection

Ensure a working exapump profile before proceeding:

1. If the user names a profile, test it with `exapump sql --profile <name> "SELECT 1"`; always place `--profile` after the subcommand. Otherwise test the default profile with `exapump sql "SELECT 1"`.
2. On success, proceed — and keep the same `--profile <name>` after the subcommand on every later `exapump` command.
3. On failure, run `exapump profile list` to see which profiles exist.
4. If profiles exist, present them and ask which to use, then inspect that one with `exapump profile show <name>` — it masks credentials — to confirm the required fields are set. **Never read, `cat`, or print `~/.exapump/config.toml`; it stores credentials in clear text.** If a credential value does appear in any command output, do not repeat it in the conversation.
5. If no usable profile exists, have the user create one locally with `exapump profile add <name>` (omit `--password` and exapump prompts on a hidden line) or `exapump profile init`, then retry step 1. Never ask the user to paste a password into the conversation, and never pass one as a command-line argument.

## Routing Algorithm

After the connection is established, determine the task type and load **only** the references needed:

1. **SQL execution** (queries, DDL, DML, schema inspection):
   - Load: `references/exapump-reference.md` (CLI usage)
   - Load: `references/exasol-sql.md` (core SQL behavior)
   - Load: `references/exasol-grammar.md` for the **exact statement syntax** (SELECT/DQL, DDL, DML, DCL, session & admin) — the EBNF the docs.exasol.com syntax diagrams are generated from. Consult it before inventing syntax or when unsure a clause exists. **Read only the section you need** — it is large.
   - Load: `references/exasol-grammar-functions.md` for **built-in function, operator, predicate, literal, and data-type syntax** (e.g. the exact argument order of a function). Same EBNF source, split out so statement lookups don't pull in the full function catalog.
   - Load: `references/exasol-reserved-keywords.md` and **ingest the full list before designing queries** — every reserved word (pinned to Exasol 2026.1.0) must be double-quoted when used as an identifier. On a keyword-related syntax error, re-query the running DB as described in **Before writing any SQL** in case the file has drifted from the DB version.

2. **Table design** (DISTRIBUTE BY, PARTITION BY, CREATE TABLE layout):
   - Load: `references/table-design.md`

3. **Query profiling / performance** (slow queries, data skew, REORGANIZE):
   - Load: `references/query-profiling.md`

4. **Analytics / window functions** (ROW_NUMBER, RANK, LAG/LEAD, QUALIFY, GROUPING SETS):
   - Load: `references/analytics-qualify.md`
   - Load: `references/exasol-grammar-functions.md` for exact analytic-function and `OVER (…)` window-clause syntax

5. **BucketFS file management** (upload/download/list/delete files in BucketFS, bfsdefault, bucket paths):
   - Activate the **exasol-bucketfs** skill for guidance

6. **UDF development** (CREATE SCRIPT, ExaIterator, SCALAR/SET, Script Language Containers, SLC, exaslct):
   - Activate the **exasol-udfs** skill for guidance

Multiple routes can apply — load all that match.

7. **Before writing any SQL** (applies to routes 1–4):
   - **Ingest `references/exasol-reserved-keywords.md` before designing queries** — load the reserved-word list (pinned to Exasol 2026.1.0) up front so you quote reserved identifiers from the start rather than discovering them through errors
   - **Always double-quote every identifier** (column names, table names, schema names) in SELECT, FROM, WHERE, GROUP BY, ORDER BY, and JOIN clauses — without exception
   - This preserves mixed-case names and prevents reserved-keyword errors in a single rule
   - Do NOT quote SQL keywords, functions, or aliases — only object identifiers
   - If a query fails with a syntax error that looks like an unquoted reserved word, do **not** trust the pinned file blindly — the DB may be newer or older than 2026.1.0 and the list can drift either way. Fetch the authoritative list for the running version and reconcile: `exapump sql "SELECT KEYWORD FROM EXA_SQL_KEYWORDS WHERE RESERVED ORDER BY KEYWORD"`
   - For the exact shape of any clause (optional parts, ordering, comma-lists), consult `references/exasol-grammar.md` (statements) or `references/exasol-grammar-functions.md` (functions / predicates / literals / data types) rather than guessing from examples.

## Related Skills

This skill handles core database interaction: connecting, SQL execution, schema inspection, and table design.
For direct native `IMPORT` and local file movement into Exasol, use **exasol-import**.
For direct native `EXPORT` and local file movement out of Exasol, use **exasol-export**.
For broad extension, connector, or federation selection, use **exasol-extension-catalog**.
For BucketFS file management (upload, download, list, delete), the **exasol-bucketfs** skill provides specialized guidance and will activate automatically when relevant.
For UDF development and Script Language Containers, the **exasol-udfs** skill provides specialized guidance and will activate automatically when relevant.
