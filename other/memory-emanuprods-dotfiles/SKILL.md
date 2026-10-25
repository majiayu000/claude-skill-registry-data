---
name: memory"
description: Persistent memory across OpenCode sessions. Stores facts, decisions, and session checkpoints in SQLite so a later session can recover context the conversation no longer holds.
---

# Memory

Durable facts and session checkpoints live in SQLite at `~/.opencode/memory.db`, exposed by the local plugin `~/.config/opencode/plugins/memory-store.ts`. This replaces the old JSON store (`~/.opencode/memory/global.json`, `~/.opencode/memory/projects/*.json` and `~/.opencode/checkpoints/*.json`, all archived on 2026-09-28).

| Tool                        | Purpose                                                                                                                                     |
| --------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------- |
| `memory_store`              | Save a fact. Refuses to overwrite a divergent existing value without `overwrite: true`; reports `conflict` and shows both values otherwise. |
| `memory_recall`             | Retrieve facts by text, namespace, or both.                                                                                                 |
| `memory_forget`             | Delete a fact. Requires approval.                                                                                                           |
| `memory_checkpoint_save`    | Persist a session checkpoint.                                                                                                               |
| `memory_checkpoint_list`    | List checkpoints, newest first.                                                                                                             |
| `memory_checkpoint_restore` | Retrieve a full checkpoint payload.                                                                                                         |

Use `memory_recall` at the start of a task to recover prior decisions instead of re-asking. `memory_forget` is the only tool that asks for approval — it destroys data.

SQLite gotcha that cost us a bug: a contentless FTS5 table (`content=''`) silently ignores the `'delete'` command on SQLite 3.53, leaving orphan index rows that make `recall` return deleted memories. The plugin uses a plain FTS5 table with explicit `DELETE FROM memories_fts WHERE rowid = ?` instead. Do not "optimize" it back to a contentless table.

## Storing a fact

Key format is `domain:subject:detail`, lowercase, colon-separated: `opencode:plugins:session-anchor`.

```ts
memory_store({
  key: "opencode:plugins:session-anchor",
  value:
    "Plugin que preserva os pedidos literais do usuário através da compactação da sessão, injetando um bloco <session_anchor> em event.system via ctx.session.hook('context').",
  namespace: "global", // 'global' is the default
  tags: ["opencode", "plugins"],
  confidence: 0.95, // 0.0 to 1.0
});
```

`store` is intentionally hard to misuse: it will not clobber a recorded decision by accident. If you get a `conflict` back, the response carries both the existing and the proposed value — that is a decision for the human, not something to resolve by re-issuing with `overwrite: true`. Show both and ask.

Store the **conclusion**, not the artifact. A fact is "auth uses RS256 with 15min access tokens", not "`~/.project/src/auth.ts` line 42". Paths and terminal output belong in a checkpoint payload, not in a memory value.

## Recalling

```ts
memory_recall({ query: "session anchor", limit: 20 }); // free text
memory_recall({ query: "auth", namespace: "global" }); // scoped
memory_recall({ limit: 20 }); // most recent
```

Search matches on both key and value, folds accents in both directions ("validação" finds "validacao"), and matches on stems. A zero-hit result means no match for that query, not an empty store — widen the search before concluding the memory is gone.

## Checkpoints

A checkpoint is session state, not a fact. Use it to resume work; use a memory for knowledge that outlives the session.

```ts
memory_checkpoint_save({
  name: "opencode-plugins-anchor-20260928",
  summary:
    "session-anchor injetando bloco via context hook; filtro de scaffolding do host aplicado",
  payload: {
    objetivo: "Preservar pedidos do usuário através da compactação",
    situacao:
      "Plugin instalado, 115 testes verdes, injeção verificada em runtime",
    proximo_passo:
      "Testar o filtro contra um checkpoint do host em sessão nova",
    arquivos: ["~/.config/opencode/plugins/session-anchor.ts"],
  },
});
```

`memory_checkpoint_list({ limit: 20 })` returns newest first. `memory_checkpoint_restore({ name })` returns the full payload, or `checkpoint not found: <name>` — it does not throw on a missing name.

**The name is a plain key.** No `.json` extension, and no date suffix: the date is stored in its own column. The old JSON store used `name-20260924.json`; SQLite stores the same checkpoint as `name-20260924` with a `created_at` field. Passing the old filename gets a not-found error for a checkpoint that exists, so strip the extension before restoring.

Every checkpoint should carry `proximo_passo`. A checkpoint without it records state but gives no way to resume.

## Slash commands

`/lembrar`, `/recordar` and `/checkpoint` wrap the six tools above and encode the conflict, accent and name-normalization rules. Prefer them over calling the tools directly when the user's phrasing is a plain request to remember, recall, or save a checkpoint — they are discoverable in the UI, which tool names are not.

## What does not exist

The old JSON store had `memory_list`, `memory_delete` and `memory_clear`, and accepted `--tags`, `topic` and `expiresAt` parameters. None of those exist. Filtering happens through `recall`'s `query` and `namespace`; the only delete is `memory_forget({ key, namespace })`. Do not write code or instructions against that older surface.
