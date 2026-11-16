---
name: naming
description: Use when deciding what something is called — what should I call this module or class, this name is vague, rename this, re-derive a ported or generated name. Owns the derivation procedure, the six naming tests, the `I` prefix on ports, the error-class and repository-class identifier forms, the vague-noun replacements, and the role suffixes (`Handler`, `Result`, `Payload`, `Service`) an architecture defines that are exempt from them. The mechanics around a name are `python-packaging`. - Naming a variable, parameter, enum member or constant; choosing between `fetch_`, `build_` and `get_by_`; standardising a term the repository already spells two ways.
---

# Naming — deriving a name instead of recalling one

A name is the first thing a reader sees and usually the only thing they read before deciding what
something does. The cost of getting it wrong is asymmetric: **wrong code fails loudly, a wrong name
misleads quietly for as long as it survives** — through every review, every search, and every later
change made on the strength of what it seemed to promise.

This skill owns the choice of the name itself. It is architecture-neutral and project-neutral, and
is loaded alongside whichever skill owns the artifact being named.

It holds in any Python project — a single package, a service, a library, a workspace of several.
Examples use this set's placeholder vocabulary (`myapp`, `foos`/`bars`, `Foo`/`Bar`) with real
technology names (`redis`, `s3`, `stripe`) kept concrete; substitute your project's own concepts,
never its layout.

## When to use vs. neighbours

- Choosing or judging any identifier — package, module, class, function, method, parameter, variable,
  enum, constant → this skill, before writing the line.
- Porting or generating code and keeping the names that came with it → this skill, first; that is its
  primary case.
- One class per module, `__all__`, the `__init__.py` re-export contract, import spelling, a circular
  import → `python-packaging`. It owns the *mechanics* around a name; this skill owns the name, so
  "name this module" is a request for this skill and not for that one.
- Which package a module belongs in → `flat-layered` (in the `pyhouse-flat` plugin) or
  `hex-architecture` (in `pyhouse-hex`), whichever style the project uses.
- Where the boundary between two components goes at all → `coupling`. A name cannot rescue a wrong
  boundary; if a thing resists naming, suspect the split before the vocabulary.
- Log event names, exception `code` values, job or task names registered by string, database
  constraint names → those are *frozen external contracts*, owned by `python-logging`,
  `exception-catalog` and whichever skill owns that artifact. See **Renaming** below.
- A test builder, fixture or failure-injection subclass needs a name → this skill for the name;
  `test-principles` for whether it should be a fixture at all.
- A test *function* or test *file* name → `test-principles`, which owns the `test_` file mirror and the
  `test_<rule_being_pinned>` function pattern. This skill names the identifiers inside the test, not
  the test.
- Deriving a concrete *file path* for an artifact in a hexagonal project, rather than its name →
  `hex-conventions`, in the `pyhouse-hex` plugin.

## The two ways a name goes wrong

Both are the same failure — the name was never actually chosen — and they need different fixes.

**Inertia.** The name arrived with the code: copied from the project it was ported from, from a
template, from a sibling service, or from whatever the generator's training data called this shape of
class. It described something in *that* context and is now describing something else. `CheckResult`
was unambiguous in a codebase that performed exactly one kind of check; moved into one that performs
five, it names nothing — because the two words a reader now needs, *which* check and *what* the
result asserts, are precisely the two the source could afford to leave out.

**Category.** The name says what *kind* of thing it is rather than what it does: `manager`, `worker`,
`handler`, `processor`, `service`, `utils`, `data`, `info`, `item`. Anything can be filed under a
category, which is why nothing can be found in it, and why the same word ends up on five unrelated
components. The fix is never a longer generic name (`worker_manager`, `data_service`) — it is the
specific one.

## Derive the name — four steps

Do not retrieve a name from memory of similar code. Derive it from this thing, here.

1. **Say what it is in one sentence**, out loud or in the scratch buffer, with no pronouns and no
   filler verbs (`handle`, `manage`, `process`, `do`). If the sentence needs an "and", the thing may
   be two things — check `coupling` before naming it.
2. **Take the head noun** of that sentence (for a function, the verb phrase). That is the name's
   head — the last word of a class name, the first word of a function name.
3. **Add the qualifiers that separate it from its siblings**, in the order *subject → aspect*.
   Usually the subject (what it is about) and the answer it carries (what it asserts).
4. **Delete every word that would still be true of half the project.** A word the enclosing package
   already supplies is noise: `Db` inside a `db` package, `Foo` inside `foos/`, `Service` on anything
   that is not the domain service the architecture defines (**Role suffixes the architecture
   defines**, below).

Worked, on a `CheckResult` inherited from a ported module:

| Step | |
|---|---|
| Sentence | "the outcome of one request to an upstream dependency, and whether it answered in time" |
| Head noun | *availability* — this is a verdict, not a bag of fields |
| Qualifiers | subject = the upstream dependency; aspect = whether it is reachable |
| Delete implied | inside a `health/` package, `Health…` is already said; drop it |
| **Result** | `UpstreamAvailability` — or `UpstreamProbe` if it carries timings rather than a verdict |

Not `CheckResult`, and not `UpstreamCheckResultData` either — step 4 removes `Data`, and step 2
rejects `Result` as a head, because "result" names the fact that something returned rather than what
it says. This record is no handler's or run's return value, so the role suffix below does not reach it.

## The six tests

Run these against the candidate before writing it. A name that fails one is not a near-miss; it is
the next `worker.py`.

1. **Predictability.** Can a reader say what is inside from the name alone, without opening it?
2. **The sentence test.** Read the call site aloud as English. `if check(x).result:` says nothing;
   `if upstream_availability.is_reachable:` says the thing.
3. **Identity over mechanism.** Does it say what the thing *is*, not how it currently happens to be
   built? `redis_cache`, `celery_task`, `csv_loader` must change when the mechanism does, or they
   start lying. Name the job: `session_store`, `nightly_rebuild`, `catalog_import`.
4. **Distinctness from siblings.** Two names differing only by a qualifier — `handler` / `handler2`,
   `client` / `new_client`, `service` / `core_service` — mean either the split is wrong or one of the
   two was never named.
5. **Exclusivity.** Would this same word be defensible for anything *else* in the project? If yes, it
   is too generic for both.
6. **The grep test.** Searching the name finds this thing and its uses — not two hundred incidental
   hits. A name you cannot search for is a name no one will maintain.

## Porting names in from another project

This is where names rot fastest, because the code already works and the name looks like it was
decided by someone.

- **A name that arrived with copied code is unnamed until re-derived.** Treat every identifier in a
  ported file as a placeholder. Run the four steps on the classes, the module, and every function on
  its public surface, in the destination's context — not the source's.
- **Re-derive against the destination's vocabulary, not the source's.** Whatever the shared packages
  and sibling components here already call this concept is the word to use. Introducing a synonym
  (`candidate` here, `entry` there, `record` in the third place, for one row of the same table) is a
  more expensive mistake than a clumsy name, because it hides the fact that they are the same thing.
- **Two invariants hold across the whole repository:** one concept, one word; one word, one concept. When a
  port breaks either, the port fixes it — not a later cleanup.
- **A qualifier that was implicit at the source is usually mandatory at the destination.** The source
  integrated one provider and could say `Client`; a codebase integrating three needs `StripeClient`.
  Conversely a qualifier the destination package already supplies gets dropped (step 4).
- **Rename in the porting commit, before anything imports the new name.** A rename is cheap while the
  file has one caller and expensive once it has thirty. If the port is large, the rename is still its
  own commit, so it cannot hide a behaviour change.
- **Do not port a name that is frozen at the source** — its log event names, exception codes and
  registration strings are *that* system's contracts, not this one's. Re-derive them under this
  project's own catalogs.

## Kind by kind

| Kind | Rule | Not | But |
|---|---|---|---|
| Package | the role it holds, one word where possible | `utils/`, `common/` | `billing/`, `pricing/` |
| Module | matches its class in snake_case (`python-packaging`) | `helpers.py` | `retry_policy.py` |
| Class | a noun phrase for the thing itself | `FooManager` | `FooValidator` |
| Protocol | a port takes the `I` prefix — see **Port names carry the `I` prefix** below; a published protocol of a distributed library follows `typing`'s naming | `FooRepository` as the port's own name | `IFooRepository`, `ICanExportFoos`; `SupportsFoo` in a library |
| Repository | the kind of stored record plus `Repository` (under hexagonal, the aggregate), whether or not a port stands in front; the `I` goes on the port where one exists, never on the class. The ban is on a second word for the class owning a record's data access — an adapter named for what its capability does (storing blobs) is not a repository | `FooRepositoryImpl`, `FooDao`, `FooStorage`, `FooStore` | `FooRepository` — implementing `IFooRepository` where there is a port |
| Exception class | the condition that was violated, suffixed `Error` (`exception-catalog` owns the class's `code` and the file it lives in) | `FooException`, `FooFailure`, `BadFoo` | `FooConflictError` |
| Type alias | the concept the composite stands for, PascalCase like a class (`python-style` decides *when* to introduce one) | `FooTuple`, `StrDict` | `FooKey`, `BarIdsByFooId` |
| Dataclass / DTO | the subject plus what it asserts | `CheckResult` | `UpstreamAvailability` |
| Enum | singular noun naming the axis it varies on | `Types` | `FooKind` |
| Enum member | the value, not its ordinal or encoding | `KIND_1` | `ARCHIVED` |
| Function | verb phrase, the specific verb | `process_foos()` | `archive_expired_foos()` |
| Fetch vs build | say which side the value comes from | `get_foo()` | `fetch_foo()` (IO) / `build_foo()` (pure) / `get_by_<field>()` |
| Method | drop what the class already says | `stripe_client.fetch_stripe_charge()` | `stripe_client.fetch_charge()` |
| Predicate | reads as a proposition; `is_`/`has_`/`can_` | `check_alive()` | `is_reachable` |
| Rule check | says what happens on failure | `check_limit()` | `assert_within_limit()` (raises) |
| Settings env prefix | the component that owns the settings class | one prefix shared by two components | `MYAPP_`, `MYAPP_FOO_`, `MYSCHEMA_` |
| Boolean variable | positive, never a negated negative | `not_disabled` | `is_enabled` |
| Collection | plural of the element name | `data`, `items`, `result_list` | `foos`, `pending_charges` |
| Mapping | `<key>_to_<value>`, or `<value>_by_<key>` | `mapping`, `d` | `foo_id_to_bar`, `bar_by_foo_id` |
| Count / index | `<noun>_count`, `<noun>_index` | `num`, `cnt`, `n` | `retry_count` |
| Duration / size | carry the unit | `timeout`, `limit` | `timeout_seconds`, `max_body_bytes` |
| Constant | the meaning, not the literal | `SIXTY` | `POLL_INTERVAL_SECONDS` |
| Parameter | names the role in *this* call, not the caller's variable | `x`, `obj` | `foo`, `session` |
| Loop variable | short is fine when the scope is two lines | — | `for row in rows:` |

**An unqualified `get_` is the banned form, not the word.** `get_foo()` hides the one thing the caller
has to know before writing the line — whether this call crosses the wire — so it is `fetch_foo()` when
it does and `build_foo()` when it does not. `get_by_<field>()` hides nothing: it names the key it looks
up by, and it appears on a port whose whole purpose is that lookup, so the IO is stated by where the
method lives. It is compliant as written and needs no exception.

**A method name states what happens on failure.** Three prefixes, and they are not interchangeable:
`assert_*` raises when the rule is broken and returns nothing, `is_*` / `has_*` / `can_*` returns a
boolean and raises nothing, and a bare verb computes and returns a value. The caller must be able to
tell which of the three it is getting **without opening the method**, because the choice decides whether
the call site needs a branch, a `try`, or neither. `check_*` fails this test twice over: it names no
verb and it answers the failure question not at all.

**One environment prefix per settings class, named after the component that owns it and disjoint from
every sibling's.** A distribution's own settings read `MYAPP_`, and a component inside it reads that
stem plus its own segment — `MYAPP_FOO_`. A library shared inside one repository reads its own
stem (`MYSCHEMA_`); a library published for importers the project does not know reads no environment at
all — its importer hands it values. Two components sharing one prefix read each other's variables: a field added
for one silently changes the other's configuration, and neither owner sees it in their own file.
**A nested prefix collides the same way** once the outer class declares a field beginning with the inner
segment — `postgres_host` under `MYAPP_` and `host` under `MYAPP_POSTGRES_` are one variable. Keep the stems
disjoint, or treat each inner segment as reserved in the outer class. A deployed prefix is a frozen
external contract — see **Renaming**.

**Port names carry the `I` prefix.** Repository protocols use `I<Aggregate>Repository`
(e.g. `IFooRepository`); capability protocols use `ICan<Verb>` (e.g. `ICanExportFoos`).
Their modules are `i_foo_repository.py` and `i_can_<verb>.py`, respectively.
Both prefixes are mandatory: `i_` marks a port, and `i_can_` distinguishes a
capability from a repository at a glance. A repository class with no port in front of it — a
flat-layered service's, say — carries no `I` and needs none: the prefix marks a port, and there is none.
Nor does a structural protocol a distributed library publishes for its users to satisfy: that is
`typing`'s own kind of protocol, named the way `typing` names them (`SupportsFoo`, `Sized`), because its
readers meet it beside those.

**This is a deliberate departure from PEP 8**, which carries no such prefix, and from the `typing`
documentation, whose own protocols are `Iterable`, `Sized`, `Hashable`. The departure buys something
PEP 8 never had to price: where a port and the adapter satisfying it are both in scope, the two want
the same noun, and one of them has to give it up. Without a prefix it is the adapter that has to
absorb a qualifier, and the qualifiers available say nothing — `FooRepositoryImpl`, `FooRepositoryBase`
— forms rejected outright further down this page. The prefix puts the mark on the abstraction, where
it is true of every implementation that will ever satisfy it, and leaves the adapter free to be named
for what it actually is.

## Vague-noun families — the fix is always the same

Each of these names a category. The fix is to name the *subject* and the *assertion* — unless the
suffix names a role the architecture defines, which the next section exempts.

| Suffix / prefix | Why it fails | Replace with |
|---|---|---|
| `…Result`, `…Response`, `…Output` | says something returned, not what it says | the verdict: `UpstreamAvailability`, `DeliveryReceipt`, `ImportSummary` |
| `…Data`, `…Info`, `…Details`, `…Payload` | every object is data | the entity: `FooRecord`, `ChargeAttempt` |
| `…Manager`, `…Processor`, `…Handler` | names an unbounded responsibility | the one job: `ScheduleBuilder`, `RetryPolicy` |
| `…Service` as a bare class name | a layer word, not a thing | what it talks to or does: `StripeClient`, `InvoiceRenderer` |
| `…Helper`, `…Utils`, `…Common`, `…Misc` | a bin, so it grows without limit | split by responsibility and name each part |
| `…Item`, `…Entry`, `…Object` | the element of *what*? | `CartLine`, `PriceChange` |
| `…Config`, `…Params`, `…Options` | fine for a settings class, wrong for arguments | `RetrySettings` if it *is* settings; otherwise pass the fields |
| `check_…`, `process_…`, `do_…`, `handle_…` | the verb is a placeholder | the real verb: `score_`, `resolve_`, `upsert_`, `fetch_` |
| `…2`, `…New`, `…V2`, `…Impl`, `…Base` with no subject | marks that the first one was never named | name both for what distinguishes them |

### Role suffixes the architecture defines

**A suffix that names a role the architecture defines is not a vague noun.** Where the project's
architecture gives a word one written meaning, the suffix says which role the class plays and the
subject in front of it says which one, so the name passes the six tests. The roles, and only these:

| Suffix | The role it names |
|---|---|
| `Handler` | a use case's handler |
| `Command`, `Query` | a handler's input |
| `Result` | the record a handler or a run returns |
| `Payload` | an external system's wire record |
| `Request`, `Response` | a transport's inbound and outbound models |
| `Service` | a domain service |
| `Repository` | the class that owns data access for one kind of stored record — an aggregate's, under hexagonal — with or without a port in front of it |
| `Settings` | a component's settings class |
| `Error` | an exception class (`exception-catalog`) |

`CreateFooHandler`, `FooPayload`, `ImportResult`, `FooUniquenessService` and `FooRepository` pass as
written. Two conditions keep the carve-out from swallowing the rule: **the subject is still there** — a
role suffix alone (`Handler`, `Result`, `Settings`, `Service`) names nothing, so a distribution's own
settings class takes the distribution's name (`MyappSettings`), and a store's takes its technology
(`PostgresSettings`, `RedisSettings`, never `DbSettings`, which names nothing once a second store
arrives; two stores on one technology each put the store's own name in front, `FooPostgresSettings`)
— and **the class actually plays that role** in this architecture. A `FooResult` that no handler or run
returns, a `FooService` that is a client, a `FooHandler` that is not a use case's handler is the vague
noun it looks like, and the table above applies to it. Conversely, `FooStorage`, `FooStore` or `FooDao` on
the class that owns a record's data access is a second word for the concept `Repository` already names —
one concept, one word (**Porting names in from another project**). The ban stops there: a class that is
not a repository but an adapter for one external capability takes the role noun of what that capability
does — under hexagonal, an adapter implementing a port for storing blobs (`ICanStoreFoos`) is named for
the storing — its technology token plus `FooStorage` — and owns no record's data access.

### Other exceptions

Two more. A category word is right when **a framework or library defines it and the thing genuinely is
that** (a `worker` that is the framework's own term for a queue-serving process; a `handler` in a
framework whose contract calls it one), and when **the project has deliberately established the term
with a written meaning** (a `shared` package defined in that repository's layout skill or README). Outside
these and the role suffixes, reaching for one of these words is the signal to spend another ten
seconds.

## Length, abbreviations, consistency

- **Name length tracks scope.** A two-line loop variable may be `row`; a module-level constant, a
  public class, or anything crossing a package boundary earns full words. The distance between
  definition and use is what decides, not a character budget.
- **No invented abbreviations.** Do not drop vowels (`cnt`, `msg`, `res`, `hdlr`) and do not truncate
  (`conf`, `req`). Four kinds are allowed, and the examples given for the first two name the kind
  rather than enumerate its members: acronyms the domain already writes that way (`http`, `url`, `id`,
  `db`, `io`, `csv`, `xml`), technology names (`postgres`, `redis`, `s3`), the names Python's own style
  gives — `self` and `cls` as a method's first parameter, `exc` for an exception in hand
  (`except … as exc`, a handler's parameter), and the standard library's own `exc_type` and `exc_info`
  (the data model's `__exit__` parameter, pytest's and logging's `exc_info`) — and the conventional
  single letters, the throwaways `i`, `j` and `_` and a type parameter (`T`, `S`), which carry no
  meaning to abbreviate and are bounded by the scope rule above rather than by this one.
  An acronym the domain genuinely writes that way qualifies whether or not it is printed here; a word
  you shortened yourself never does.
- **Acronym casing is a project-wide choice made once** — `HttpClient` everywhere or `HTTPClient`
  everywhere, never both. This set's default is the first: only the leading letter capitalises, which
  keeps mechanical renames and case-sensitive searches predictable. On a project that already has a
  consistent other form, follow it; on one that is inconsistent, standardise rather than add to it.
- **One concept, one word, repository-wide.** Before inventing a term, search for what the shared packages
  and sibling components already call it, and use that.

## Renaming

A module that started as one thing and became another keeps its old name only through neglect.
Renaming is cheap, mechanical and reviewable; a stale name is none of those. **Do it in its own
commit** so it cannot hide a behaviour change.

The exception is a name that has escaped the codebase and become an external contract. Those are
frozen and are **not** renamed in place: log event names, exception `code` values, job or
task names registered by string, queue and topic names, database table/column and constraint
names, Alembic revision identifiers, serialization aliases and published API fields,
environment-variable names and settings prefixes, CLI commands and flags. If one of those is wrong, add the new
name alongside it and retire the old one deliberately, with a migration.

## Rules

1. Run the four-step derivation on each candidate, using `coupling` when the responsibility will not fit
   one sentence.
2. Require the candidate to pass all six tests before using it.
3. Re-derive copied and generated identifiers against the destination's concepts and existing vocabulary.
4. Check names against both the kind-by-kind table and the vague-noun table, retaining category words
   only as a role suffix the architecture defines — with a subject in front, on a class that plays
   that role — or under the two other documented exceptions.
5. **Name a call for which side its value comes from.** An unqualified `get_` leaves the caller unable to
   tell whether the line crosses the wire; a name that states the key it looks up, or the word `fetch` or
   `build`, does not.
6. **Name a method for what happens on failure** — `assert_*` raises, `is_*`/`has_*`/`can_*` returns a
   bool, a bare verb computes — so the call site can be written without opening the method.
7. **Give each settings class its own environment prefix, named after the component that owns it**, and
   check it against every sibling's before using it — a nested prefix included, whose inner segment the
   outer class never begins a field with.
8. Apply the port prefixes in **Port names carry the `I` prefix** — `I<Aggregate>Repository`
   for a repository port, `ICan<Verb>` for a capability port, both mandatory. A published protocol of a
   distributed library follows `typing`'s naming instead.
9. Apply the scope, abbreviation and acronym-casing choices in **Length, abbreviations, consistency**.
10. Keep the repository's concept-to-word mapping unambiguous in both directions — one concept, one
    word; one word, one concept. A port that brings a second word for a concept the repository already names
    takes the existing word.
11. Perform renames separately from behaviour changes; complete port-time naming before callers spread.
    A module that has outgrown its name is renamed, in its own commit, before it is extended.
12. Check the frozen-contract list in **Renaming** before changing a published name; migrate those names
    instead of replacing them in place.

## Hard stops

- A thing resists every candidate name because no sentence describes it without "and" → stop, this is
  a boundary problem, not a vocabulary problem; load `coupling`.
- Asked about one class per module, `__all__`, the `__init__.py` re-exports or import spelling → stop,
  use `python-packaging`; this skill names the module, that one owns the mechanics around it.
- Asked which package a module belongs in → stop, use `flat-layered` (in `pyhouse-flat`) or
  `hex-architecture` (in `pyhouse-hex`), whichever the project uses, or the project's own layout where
  neither applies.
- Asked to name a test function or a test file → stop, use `test-principles`.
