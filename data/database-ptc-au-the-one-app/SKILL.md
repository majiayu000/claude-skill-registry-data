---
name: database
description: Read before writing an app that keeps data or has scheduled jobs, which it keeps in a database with this app.
metadata:
  title: "Database"
  subtitle: "Where apps keep their data"
  about: "Gives every app here a database of its own, so what it keeps for you is yours, and what it keeps for a group is the group's."
  category: Admin
---

An app keeps its data in a database by requiring this app. The database is SQLite, kept in the app's own
artifact for whoever it runs for, so each user and each group has their own.

Its words:

- **Lease**: the record of which server writes a database for now. One server holds it at a time. Part of the database
  app.

    def requires, do: %{"database" => "to keep your notes"}

    @schema ["create table notes (id integer primary key, text text not null, at text not null)"]

    def call("add", %{"text" => text}, call) do
      database = OneCore.Call.app(call, "database")
      at = DateTime.to_iso8601(DateTime.utc_now(:second))

      database.transaction(call, @schema, fn db ->
        [%{"id" => id}] =
          database.query(db, "insert into notes (text, at) values (?, ?) returning id", [text, at])

        "Added note #{id}."
      end)
    end

- `transaction(call, schema, fun)` runs `fun` with the database and gives what it returns. What `fun` writes
  is kept all together or not at all: raise to keep none of it. Once it returns, what was written is safe in
  the bucket, and losing the server loses none of it.
- `query(db, sql, values)` runs one SQL statement with a `?` for each value, and gives its rows, each a map
  from a column's name to its value. `returning` gives back what an insert or an update made. A value is a
  number, text, `nil`, a boolean (kept as 1 or 0) or `{:blob, binary}`.
- `schema` is the statements that make the tables, in the order they were added. Each runs once on each
  database. To change the tables, add statements to the end, and leave the ones already deployed as they are.
- The database is the blobs under `log/` and `snapshot/` in the app's own artifact. Every other name there
  is the app's, for what isn't rows: a photo, a file.
- One server at a time writes a database, and a call that reaches another is passed on to it. So the tool may
  start again on another server, and `fun` may run more than once. Do everything that touches the database
  inside `fun`, and what reaches outside, such as sending a message, after `transaction` returns.
- An app's scheduled jobs (its `jobs/0`) are called by the server writing its database, and when each last
  ran is kept there too, in the table `database_scheduled`. A job's call marks that it ran in its own first
  transaction, so what it wrote and its having run are kept together or not at all: a server that takes over
  makes the call again only if neither was. So a job does its work in one transaction, in the process its
  tool is called in, and what reaches outside after `transaction` returns, which then happens at most once.
  A job that makes no transaction is marked when its call ends, and may be called again after a failover.
