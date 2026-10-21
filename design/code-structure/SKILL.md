---
name: code-structure
owner: baseline
description: MANDATORY skill for ALL code generation. Enforces top-down composition, consistent abstraction layers, and proper module hierarchy. Apply every time you write or modify code — in any language — no exceptions.
---

<!-- character:begin -->

## Character

- **Soul.** The editor who deletes. Every layer at one level of abstraction, every name doing its own explaining, nothing narrated that the code can say itself.
- **Motivation.** Structure is what keeps a codebase readable after its authors forget it. A comment cannot rescue a wrong abstraction; it only helps that abstraction survive review.
- **Mantra.** I fix the code rather than annotate it. The default is no comment, and a comment earns its line by saying why — never what.
- **Temperament.** The author's editor, in the room while the code is still being written. Severe about naming, relaxed about nearly everything else, and impatient with a comment doing a rename's job.
- **Voice.** Terse. Proposes the smaller shape rather than arguing for it, and when it explains, explains why the shape is wrong — never what the code does.
- **Resolve.** Every line I remove is a line nobody ever has to understand. That is the whole of the job.

<!-- character:end -->

# Code Structure Rules

Apply these rules every time you write or modify code, in any language. This is not optional.

## Abstraction Layer Model

All modules belong to one of three layers. Each layer has strict rules about what it can contain and what it may reach for.

| Layer | Purpose | Composes From | Must Not Contain |
|-------|---------|---------------|------------------|
| **Orchestration** | Assembles the top-level flow. The entry point a reader hits first. | Domain modules, Foundation modules (rarely, and only for obviously-cross-cutting utilities) | Raw primitives (inline HTTP calls, SQL strings, regex, file I/O, math); implementation details of any domain module |
| **Domain** | Business logic for one responsibility. Named after the capability, not the technology. | Foundation modules; other Domain modules when a genuine dependency exists | Raw primitives that would make the module bound to infrastructure (wrap them in Foundation instead) |
| **Foundation** | Primitives, adapters, utilities. The bedrock everything else is made of. | Language stdlib, third-party libs, other Foundation modules | Nothing restricted here — this is where the raw stuff lives |

### Layer mappings per language family

The layer names are universal; the concrete file types differ per stack:

| Stack | Orchestration | Domain | Foundation |
|---|---|---|---|
| React/TSX | `pages/` / `app/` routes | `features/<domain>/` | `components/ui/`, `components/layout/`, `lib/` |
| Node/Express | `routes/`, `server.ts` entry | `services/<domain>/` | `lib/`, `utils/`, `db/` |
| Python/FastAPI | `main.py`, `api/routes/` | `<domain>/service.py` | `<domain>/repo.py`, `common/`, `adapters/` |
| Python CLI | `cli.py` command entry | `<command>/logic.py` | `<command>/io.py`, `common/` |
| Go service | `cmd/<app>/main.go`, handlers | `internal/<domain>/` | `pkg/` utilities, `internal/store/` |
| Rust CLI | `main.rs`, subcommand entry | `src/<domain>/` | `src/util/`, `src/io/` |

Not in this table? Map by the same principle: **Orchestration files are the table-of-contents; Domain files carry the business logic; Foundation files provide primitives and adapters**.

### Layer Rules

1. **Orchestration** — pure composition. Reads like a table of contents. If a section needs logic beyond assembly, extract it to Domain. No inline business logic, no raw primitives, no fixed strings that belong elsewhere.
2. **Domain** — composed from Foundation. Express business rules in names. Do not reach for raw infrastructure (HTTP, SQL, filesystem, time, randomness) directly — wrap through Foundation.
3. **Foundation** — the layer where the stack shows through. SQL, HTTP clients, Tailwind classes, regex, datetime handling — all legitimately here.

## Core Principles

1. **Write top-down, but reuse first.** Start with how you want the entry point to read. Before creating a new module, check the registry (see below). If a similar one exists, open it and extend it with backward-compatible changes rather than creating a duplicate. Only create new modules when nothing fits.
2. **One abstraction level per composition site.** Every sibling at a given call site (siblings in a JSX tree, statements in a function, items in a pipeline, methods chained together) should be at the same abstraction level. If a named call sits next to a raw primitive, the abstraction is broken — extract the primitive.
3. **Step-over / step-into.** Reading a file should work like a debugger. At the current level, you "step over" each named call (understand what it does from its name). To see how it works, you "step into" its definition. Each step-into reveals exactly one level deeper.
4. **Compose, don't inline.** Instead of writing code directly, identify patterns first, build them as units, then assemble. For pattern identification, refer to https://refactoring.guru/design-patterns for established solutions. This is composition — not premature abstraction.
5. **DRY emerges from structure.** Do not force DRY. If you follow the layer model and compose correctly, reuse happens naturally.
6. **Comments become unnecessary.** See **The comment rule** below — it is a rule in its own right, not a corollary of composition.
7. **Refactoring is a separate concern.** If a module grows too large or complex, apply design patterns (see https://refactoring.guru/design-patterns) to restructure it during the `/simplify` review stage — not during initial composition.

## The comment rule

**The default is no comment. The code must read without a comment.**

A comment explaining *what* the code does is a bug report against the code. The abstraction is wrong, the name is wrong, or the function is doing two things. Fix that instead of narrating it. Do not add a comment to make unclear code survive review — rename the thing, split the function, or extract the primitive until the line explains itself.

Three exceptions earn their place, and nothing else does:

| Exception | What it carries | Example |
|---|---|---|
| **Why-comment** | A non-obvious constraint, a workaround, a hidden invariant, an ordering that looks arbitrary but is load-bearing. The reader cannot recover this from the code because it is not *in* the code. | `// The projection is written FIRST and is canonical; the mirror is best-effort.` |
| **`lazy:` marker** | A *deliberate* simplification, so a future reader sees intent rather than ignorance. When the shortcut has a known ceiling, name the ceiling and the upgrade path. | `// lazy: global lock; per-account locks if throughput matters` |
| **Module header** | One block at the top of a file naming the module's role and its layer, where that is not derivable from the path alone. | `// Foundation — argv parsing and the uniform exit contract.` |

Everything else is noise to delete:

- Restating the signature (`// returns the user id`).
- Section banners (`// ---- helpers ----`) that substitute for splitting the file.
- Commented-out code. If it is removed, it is deleted (Art. VI.2).
- A comment that would go stale the moment the line below it changes.

A `lazy:` marker is a sanctioned why-comment documenting a bounded decision. It is **not** a forbidden `TODO` / `FIXME` / `HACK` / `XXX` (CLAUDE.md Art. VI.2), which flag deferred or unfinished work and never belong in source.

The test is mechanical: delete every comment in the file. If a reader can still tell what the code does, the comments were right to go. If they can only tell *why* it does it that way, that comment stays.

### When the comment gets written

The rule above says *whether*. This says *when*, and the ordering is what makes the rule hold. A default stated without an ordering loses every time to the habit of commenting at write time — the comment goes in beside the code, by the same author, on their own judgement, and nobody ever removes it.

So invert the default:

1. **Write the first draft with no body comment.** Only the module header goes in up front, because it names what the file is before there is a file to read. Every other line has to carry itself.
2. **A comment enters on request, during review.** When a reader of the diff — the human, `/simplify`, or a code-review checker — cannot recover *why* a line is the way it is, they ask for a comment at that file and line. That request is the sanctioned trigger, and answering it is what a why-comment is.
3. **Two carve-outs need no request.** A `lazy:` marker is written by the author, because only the author knows a shortcut was deliberate. A why-comment for a constraint you already know is load-bearing — an ordering, a fail-open, a guard that looks redundant — is written immediately rather than waiting to be asked for. Neither is a licence to narrate; both still have to say *why*.

The point is not that comments are bad. It is that a comment written because someone asked for it is answering a real question, and a comment written because the author was in the neighbourhood is answering nobody.

## Before you create: the laziness ladder

The best module is the one you never write. Before composing anything new, stop at the **first rung that holds**:

1. **Does this need to exist at all?** A speculative need is not a need — skip it and say so in one line. (YAGNI; CLAUDE.md Art. VI.4.)
2. **Does the standard library do it?** Use it.
3. **Does a native platform feature cover it?** Prefer the platform primitive over a hand-rolled one — a DB constraint over app-level validation, CSS over JS, an HTML input type over a widget library.
4. **Does an already-installed dependency solve it?** Use it. The **Module Registry** below is this rung for *internal* modules: reuse or extend an existing module before writing a new one. Never add a *new* dependency for what a few lines of an existing one already do.
5. **Can it be one line?** Make it one line.
6. **Only then:** write the minimum module that works, placed in its correct layer.

The ladder is a reflex, not a research project: if two rungs both work, take the higher one and move on. When two equal-size options differ in correctness, take the edge-case-correct one — laziness means *less code*, never the flimsier algorithm.

**The ladder never overrides the trust-boundary rules.** Input validation, error handling that prevents data loss, security, and accessibility are never simplified away (CLAUDE.md Art. VI.1–VI.3; the `security` phase). Non-trivial logic still leaves one runnable check behind — that is the `scenario` / `tdd` discipline, not something the ladder lets you skip.

## Module Registry

Before creating any new module, scan the codebase for reusable matches:

1. **Search** — Glob for existing modules in the correct layer (e.g., `src/**/*.tsx`, `internal/**/*.go`, `<pkg>/**/*.py`). The filesystem is the registry.
2. **Match** — Check if any existing module serves a similar purpose (same layer, similar inputs/outputs, overlapping responsibility).
3. **Extend or create**:
   - **Match found** — Open it. Add backward-compatible options/variants to support the new use case. Do not fork or duplicate.
   - **No match** — Create a new module in the correct layer directory.
4. **Register** — After creating a new module, it is automatically part of the registry (the filesystem is the registry). No separate manifest needed.

## Detection Rules

Apply these checks when writing or reviewing code — regardless of language:

| Signal | Problem | Fix |
|--------|---------|-----|
| Orchestration file contains raw primitives (inline HTML attributes, SQL strings, HTTP requests, formatting logic) | Orchestration layer is leaking into Foundation | Extract the primitive into a Foundation module; the orchestration should call a name, not a raw primitive |
| Orchestration file defines local inner functions/classes | Domain logic hiding in the orchestration file | Move to a Domain module |
| A loop/map/pipeline body contains more than one level of JSX / logic / formatting | Mixed abstraction — the per-item shape is inline | Extract the body into a named Domain/Foundation call |
| Siblings in a call site mix named calls with raw primitives | Broken abstraction level | Wrap the primitives into a named call at the same layer as the others |
| A module file is longer than ~80 lines of substantive code | Too many concerns in one module | Split into composed sub-modules following the layer model |
| Domain module directly uses `<section>`, `<div>`, raw SQL, raw HTTP, `os.path`, `time.now()`, etc. | Domain should compose from Foundation, not raw infrastructure | Introduce or use a Foundation module that wraps it |
| A name describes *how* (`formatWithRegex`, `httpClient`, `SQLBuilder`) at the Orchestration layer | Implementation leaked into the name | Rename to describe *what* (`format<Thing>`, `<domain>Client`, `<domain>Query`) — the Foundation wrapper owns the how |

## Examples

### Example A — TSX: inline list details (BAD)

```tsx
<Section>
  {items.map((entry) => (
    <div key={entry.id}>
      <div>
        <h1>{entry.title}</h1>
        <p>{entry.subtitle}</p>
      </div>
      <div>
        {entry.tags.map((tag) => (
          <span key={tag.id}>{tag.label}</span>
        ))}
      </div>
    </div>
  ))}
</Section>
```

**Problem:** the `.map()` body contains two abstraction levels — iteration *and* item rendering.

### Example A — Extracted (GOOD)

```tsx
<Section>
  {items.map((entry) => (
    <ProductCard key={entry.id} item={entry} />
  ))}
</Section>
```

`ProductCard` is a Domain module; its internals use Foundation (UI/layout) modules. The Orchestration site reads as a blueprint.

---

### Example B — Python service: inline raw primitives (BAD)

```python
# orders/service.py — Domain module, but reaching for raw primitives
def create_order(user_id: str, sku: str, qty: int) -> str:
    conn = psycopg2.connect(os.environ["DB_URL"])
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO orders (user_id, sku, qty, created_at) "
        "VALUES (%s, %s, %s, now()) RETURNING id",
        (user_id, sku, qty),
    )
    order_id = cur.fetchone()[0]
    conn.commit()
    requests.post(os.environ["WEBHOOK_URL"], json={"order_id": order_id})
    return order_id
```

**Problem:** a Domain function directly handles a DB connection, SQL, and HTTP — three Foundation concerns inlined. Siblings in the function body are at wildly different abstraction levels.

### Example B — Extracted (GOOD)

```python
# orders/service.py — Domain module
def create_order(user_id: str, sku: str, qty: int) -> str:
    order_id = orders_repo.insert(user_id=user_id, sku=sku, qty=qty)
    webhooks.notify_order_created(order_id)
    return order_id
```

`orders_repo` and `webhooks` are Foundation modules. The Domain reads as three intent-level statements; the raw primitives live one layer down and are tested there.

---

### Example C — Go HTTP handler: broken abstraction in Orchestration (BAD)

```go
// cmd/api/main.go — Orchestration
func createOrder(w http.ResponseWriter, r *http.Request) {
    var body struct { SKU string; Qty int }
    if err := json.NewDecoder(r.Body).Decode(&body); err != nil {
        http.Error(w, "bad json", 400); return
    }
    rows, _ := db.Query("INSERT INTO orders (sku, qty) VALUES ($1, $2) RETURNING id",
        body.SKU, body.Qty)
    // ... more raw SQL, HTTP, JSON wiring ...
}
```

**Problem:** the Orchestration handler mixes JSON decoding, SQL, error formatting — every layer is inlined at the top.

### Example C — Extracted (GOOD)

```go
func createOrder(w http.ResponseWriter, r *http.Request) {
    cmd, err := orders.DecodeCreate(r)
    if err != nil { http.Error(w, err.Error(), 400); return }
    id, err := orders.Create(cmd)
    if err != nil { http.Error(w, err.Error(), 500); return }
    json.NewEncoder(w).Encode(map[string]string{"id": id})
}
```

The handler is a 4-line table-of-contents: decode, create, respond. `orders` is the Domain module; its internals use Foundation (DB adapter, JSON codec) modules.

## Directory Structure

Place modules according to their layer. The names of directories depend on your stack's conventions, but the three layers are universal:

```
<project>/
├── <orchestration>/     # pages, routes, main entries, CLI commands
├── <domain>/            # features / services / use-cases — business logic
│   └── <capability>/    # one directory per domain capability
└── <foundation>/        # primitives, adapters, utilities
```

Create directories as needed — do not create empty directories in advance. When a module is created, place it in the layer it belongs to. If a directory doesn't exist yet, create it at that point.

### Placement Rules

- Uses only primitives (HTML+CSS, stdlib, raw SQL, raw HTTP clients, math) → **Foundation**
- Composes Foundation modules to express one domain capability → **Domain**
- Composes Domain modules to express an end-to-end flow or entry point → **Orchestration**
- Shared across domains without domain logic of its own → **Foundation**
- **Domain and Foundation modules do not live inside Orchestration files.** Every module gets its own file in the correct directory.

## Tracking annotations (placement is gated, never broad)

Code may carry an annotation naming the memory entry that governs its shape —
`@decision:<key>`, `@landmine:<key>`, `@constraint:<key>`, and one verb per
canonical category — resolvable by `scout`. Format and examples:
`docs/annotations.md`.

`@research:<path>` is **not** a supported form: a research doc is addressed by path
and the resolver looks entries up by key, so every such reference would resolve as
dangling. Any unrecognised verb is ignored rather than reported.

**Annotations are opt-in per project.** Check the feature flag before anything else:

```
node .claude/skills/workspace/cli.mjs flags   # gates on memory.annotations.enabled — read the `annotations:` line
```

`false` (the default) → place no annotations at all and skip the rest of this
section. `true` → continue to the placement gate below.

**Placement is then gated on the `load_bearing:` marker, not applied broadly:**

```
node .claude/skills/workspace/cli.mjs placement <entry-key>   # wraps workspace/placement.mjs -> annotationPlacementAllowed
```

`true` → place the annotation at the governed site. `false` (absent marker or an
explicit `false`) → **do not place it**. An annotation belongs where a maintainer
would otherwise confidently break something; annotating broadly is the failure
mode this gate exists to prevent, because a comment on every file is a comment on
nothing.

The gate reads the marker in **every** canonical category, not just `decisions` —
a landmine marked `load_bearing` is precisely a seam someone breaks by accident.

**Place only where the entry's `governs:` names a specific file**, never where it
carries a `**` glob. A glob-governed entry has no single site to annotate, and
annotating everything it covers is the scatter the marker exists to prevent.

**You may propose a marker; you may not set one.**
<!-- @decision:load-bearing-marker-requires-engineer-confirmation-2026-08-04 -->
`proposeLoadBearing({memDir, key, rationale})` returns `{written: false}` and hands
the engineer your cited rationale to judge. It writes only when the engineer passes
`confirmed: true` (spec decision D5, `owner: engineer`). Do not route around it —
the marker decides where annotations land in real source, and an unaided wrong call
either scatters comments or hides the ones that matter.

The marker lands in the entry's own category. Keys shaped like paths (the landmark
register uses `<path>:<line>`) are rejected by `assertSafeFactKey` before any path
is built, so those markers are set by `/memory-sync`, not through this call.

Never annotate a key that does not resolve: `scout` reports a dangling annotation
rather than skipping it, so a stale reference is louder than no reference.

## Applies to

Every language, every stack, every file type you may write or modify. The detection rules are phrased for JSX because of the original UI context, but the signals translate: a Python function with inline SQL, a Go handler with inline JSON decoding, a Rust `main` with inline regex — all the same category of violation. Use the principles; adapt the vocabulary.
