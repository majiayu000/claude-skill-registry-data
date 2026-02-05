---
name: hypopg-help
description: used for preparing hypothetical indexes to be run in higher environments
---

# Building hypothetical indexes

Useful when a database includes the hypopg extension (for Postgres) to create and test hypothetical indexes.
The goal is to create a copy and pasteable set of commands that a user can run to create a hypothetical index for testing in a higher environment.

The final deliverable is a set of Ruby commands to copy/paste. Wrap them in code blocks.

## Instructions

1. Work with the user to determine the index design. Ask them about contents, which table, and any ordering or conditional concerns.
2. Use `connection = ::ActiveRecord::Base.lease_connection` to find an available connection
3. Create a temporary variable called `create_index_sql` using a `<<~SQL.squish` heredoc for the index creation.
4. Next, use string interpolation to create a new SQL string to create the hypopg index using `hypopg_create_index()`. Set this to `hypopg_sql`. Use `connection.quote(create_index_sql)` to properly handle nested quotes and SQL escaping when interpolating the SQL string into the hypopg function call
5. Provide the snippet for the end user to use `connection.execute hypopg_sql`. The result should be saved to `results` and we should instruct the user to output `results.to_a`.
6. To verify the hypothetical index is being used, instruct the user to use the same `connection` to call `.execute` with string interpolation to add "EXPLAIN " at the beginning of a `#to_sql` call on a chain of model code. For example: `connection.execute("EXPLAIN #{Model.where(...).to_sql}")`.
7. Provide follow-up instructions to the user on how to verify the new hypothetical index is being used. Provide context on how to clean up new hypothetical indexes if they need to try an alternative.
