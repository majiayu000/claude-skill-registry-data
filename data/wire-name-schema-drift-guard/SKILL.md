---
name: wire-name-schema-drift-guard
description: "Prove a client's serialization names, RPC argument names, and field-length limits still match the database/API schema they read — kotlinx @SerialName and take(N) caps vs Postgres/Supabase migrations — catching silent-default failures where a renamed column decodes as 0/null or a tightened CHECK makes one row's push fail forever inside runCatching. Use when DTOs carry hand-written wire names, after any column rename or constraint change, or when server-side SQL tests exist but nothing checks the client."
---

# Wire contract drift guard

Client and server duplicate a contract in two languages. Nothing fails loudly when
they drift: kotlinx decodes a missing key as the **default** (0/null), PostgREST
404s a renamed RPC parameter, and a tightened `CHECK` rejects one row forever
inside a `runCatching`. All three read as "the feature is quietly wrong", never as
an error.

Guard all three axes in ONE unit test that reads the migrations.

## What to pin

1. **Serial names** — `Dto.serializer().descriptor.elementNames` ⊆ the columns of
   the table/view it reads.
2. **RPC argument names** — declare args as a `@Serializable` shape, not a
   hand-built `JsonObject`; compare `elementNames` to the `create function`
   signature, and assert the **encoded body** too (a right descriptor with a
   broken encoder still sends the wrong JSON).
3. **Length/bounds limits** — put `take(N)` caps and `min..max` in one
   `WireLimits` object; compare to `char_length(col) <= N` and
   `char_length(trim(col)) between LOW and HIGH`.

## Locating the migrations from a test

Walk up from the module CWD until `supabase/migrations` exists; read every `.sql`.

## Parser traps (each cost a real debugging cycle)

- One `alter table` may carry **several** `add column` clauses — scan the whole
  statement, not the first match.
- A view's select list ends at its **own** `from`, at paren depth 0; a correlated
  sub-select carries its own `from` and must not terminate the scan.
- Views get redefined by later migrations — take the **last** definition.
- Assert the parser found something (`columns.size > 2`). A schema-parsing test
  that silently parses nothing passes forever.

## Prove it both ways

Mutate the **client** (rename a `@SerialName`, drop an arg, change a limit) and
the **server** (drop a column from a view, tighten a `CHECK`). Each must fail with
the column named. Removing an RPC argument should stop **compiling** once the args
are a typed shape — better than a test.

Beware no-op mutations: adding a comment or an unused `val` changes nothing and
"passes" while proving nothing.

## Library contract

Verify the client call signature against the artifact, not memory. Example: pinned
`postgrest-kt` `rpc` takes only `(String, JsonObject)` — the typed
`rpc(function, T)` overload does not exist; encode the shape into a `JsonObject`.

## Before claiming a mismatch

Confirm the client field actually reaches that column. Two similarly-named fields
(a device-local profile name vs a cloud handle) can look like a violated
constraint and be unrelated.
