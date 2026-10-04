---
name: cortex-query
description: >
  Search and retrieve content from the cortexes vault — the user's external
  memory. Use when the user explicitly asks to search or recall the vault
  ("查 cortex", "之前有記過", "cortex 裡有沒有", "check my notes", "what did
  I write about", `/cortexes:query`), or when the using-cortex skill routes a
  request here after one of its four prior-context signals. Do not use for
  general questions, for fresh work with no prior-context signal, because a
  question is merely hard or technical, or after the user has opted out of
  the vault.
---

# Cortex Query — Search the Vault

Search the cortexes Obsidian vault using semantic search.

## When to Run This Skill

Run it in exactly two cases:

1. **The user explicitly asks.** "查 cortex", "之前有記過嗎", "cortex 裡有沒有",
   "check my notes", "what did I write about X", or the `/cortexes:query`
   command. An explicit request is always sufficient on its own.
2. **`using-cortex` routes the request here** after one of its four concrete
   signals fired (explicit request, reference to prior work, a topic the
   SessionStart hook actually listed, or resuming a previous session). That
   skill owns the decision; this one owns the search.

### Do not run it

- For general questions, or for fresh work with no prior-context signal.
- Because a question is difficult, technical, open-ended, or touches
  infrastructure or internal tooling. **Difficulty is not a signal.**
- When the user picked option 4 ("直接開始工作") from the SessionStart menu,
  skipped the menu, or said "don't check cortex" — that opt-out holds for
  the rest of the session until the user explicitly asks (case 1).
- When the conversation, the current repo, or the current turn already
  supplies the answer.

An unprompted search costs the user tokens and latency, and unrelated notes
pollute the answer. When no case applies, answer directly and do not mention
the vault.

## Resolve Vault Path

Read `~/.cortex/config.json` and take `vault_path`. If the file is missing or
has no usable `vault_path`, tell the user to run `/cortexes:genesis` first.

Do **not** read `CORTEX_VAULT_PATH` here. Only the SessionStart injection
script and the `takeoff.sh` helper honour it; the write side — the SessionEnd
recorder, `evolve`, `distill`, `broadcast` — resolves the vault from
`config.json` alone, and the BM25/vector indexes live at a single fixed
`~/.cortex/` location regardless. Honouring it on the read side would split
reads and writes across two vaults while both shared one index. `config.json`
is the one source of truth until a real multi-vault design lands.

## Search Strategy (Layered)

### Layer 1: Vector Search (primary)

Use `cortex-vec` for semantic search:

```bash
cortex-vec search "<query>" --n 5
```

`cortex-vec` is installed as a CLI tool (from PyPI via `uv tool install
cortex-vec` or pip — see the README's Quick Start; `/cortexes:genesis` offers
the install when it is missing).

**Context-aware filtering:** If the current session is inside a git repo,
detect the repo name and add `--repo` filter as default scope:

```bash
cortex-vec search "<query>" --repo <detected-repo> --n 5
```

`--repo` narrows the `Projects/` partition only; cross-repo `Notes/` always
appear in results regardless of the filter, and a page listing several repos
passes a filter naming any of them. Scoping therefore hides other repos'
`Projects/` pages, never the shared notes. All three retrieval streams
(vector, BM25, wikilink graph) honour the filter.

The user can override this by saying "search all" or "search across everything".

**Additional filters:** Apply when the user specifies:
- `--type note|project` — filter by content type
- `--category Nginx|Linux|...` — filter by category

**Interpreting `score`:**

`score` is the **vector cosine similarity only** — how close the query is to
that page's embedding. It is **not overall hybrid confidence**: it says
nothing about the BM25 or graph streams that also produced this result set,
and it is not what ordered the list.

So read the number only as a band of **semantic overlap**, never as a verdict
on relevance:

- `> 0.80` — strong semantic overlap with the embedding
- `0.60–0.80` — moderate semantic overlap
- non-zero `< 0.60` — little semantic overlap *on the embedding*, which is
  not by itself a verdict on whether the page answers the question. This band
  now means a measured low overlap even for a keyword or wikilink hit, not an
  unmeasured one
- `0.0` — ambiguous in the current CLI output; see below

**Relevance follows the returned order, not the number.** The list comes back
already fused across every active stream, and reranked when `--rerank` is on,
so its order is the retrieval system's own verdict. Judge each hit from that
position plus the fields the CLI actually returns — `title`, `category`,
`tags`, `summary` — and from exact lexical evidence where you have it. Layer 1
returns no excerpt; matched text comes from the Layer 2 grep supplement.

**Never demote a high-ranked BM25 or graph result solely because its cosine is
low or zero.** Fusion routinely places such a hit above a higher-cosine one on
purpose, and an exact match on an identifier, command or error string is
usually the strongest evidence available even when the embedding scores it
low. The number is comparable across hits — a hit that arrived through the
keyword or wikilink stream is backfilled with its real cosine from the
collection, so it is scored on the same scale as a vector hit — but a
comparable number is still only the semantic band, not the verdict.

**What `0.0` means.** The backfill needs a live vector stream, so it does not
remove the ambiguity, it narrows it. The CLI emits `0.0` when the vector
stream is unavailable (no `OPENAI_API_KEY`, or vector retrieval switched
off — the score is then missing for every non-vector hit), when the backfill
query itself failed, and when an actual cosine is zero or rounds to zero at
four decimal places. The implication runs one way only: a result with no vector
score always prints `0.0`, but a printed `0.0` does not tell you which of
those produced it.

So `0.0` establishes none of the following: whether the document took part in
the vector result stream, whether it exists in the vector index at all, or
which retrieval mode produced the result set. Treat the vector evidence as
unavailable or indeterminate, and rely on the returned order and the result
fields instead.

**Do not infer BM25-only mode from `0.0` alone.** Say retrieval ran without a
vector stream only when you know that independently — the user has established
that `OPENAI_API_KEY` is unset, or `cortex-vec status` reports no embedded
entries. Otherwise present the results without asserting a mode.

### Layer 2: Exact Match (supplement)

If Layer 1 returns no *relevant* results, if `cortex-vec` is unavailable, or
if the user is searching for an exact string (command, config path, error
message), search the text directly. Judge "no relevant results" from the
returned hits and their order — never from the score column alone.

```bash
grep -ri "<query>" <vault_path>/Notes/ <vault_path>/Projects/
```

Use `grep` through Bash rather than the Grep tool: the vault normally lives
outside the session's working directory, and the file tools are confined to
the workspace, so the Grep tool cannot reach it. `/cortexes:query`
pre-approves exactly this `grep` (and nothing else beyond `cortex-vec` and
repo detection) for that reason.

**If the grep is refused because the vault is outside the working
directory**, do not report the search as failed. Say precisely that: Layer 1
is unavailable and the fallback cannot reach the vault, and the fix is either
to install `cortex-vec` (Layer 1 takes no path argument, so it is unaffected
by the workspace boundary) or to add the vault to the session with
`/add-dir <vault_path>`. Never imply the vault has no matching content when
the search never ran.

Show matching files with brief excerpts.

### Layer 3: Raw Search (archive, on request)

Only when the user specifically asks about recent sessions or raw data:

```bash
grep -ri "<query>" <vault_path>/Raw/
```

Show matches with date and repo context.

## Response Format

Present results to the user:

```
Found N results for "<query>":

1. [score] Title (Type, Category/Repo)
   → one-line summary

2. [score] Title (Type, Category/Repo)
   → one-line summary
```

- Use wikilink format when referencing notes: `[[note-name]]`
- If multiple matches, list them and ask which one to read
- If user wants details → read the full file
