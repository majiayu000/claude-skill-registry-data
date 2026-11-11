---
name: tools
description: Which tool to reach for and in what order. Code navigation (repomap, ripgrep, ast-grep, Serena, language servers), the lookup ladder for facts and docs (own knowledge only for things that can't change, then Context7, then Exa), notes and memory in Basic Memory for Jason's own projects and setup, tasks in Linear, and compressed output. Use when you need to find or understand code, for a fact or doc you can't answer from knowledge, and before reading or writing notes. Not needed to answer a chat question you already know.
---

# Using the tools

Your tools are part of the answer, not a fallback. Check what this session actually has (MCP servers, connectors, skills, subagents) and use them before guessing. When a tool you'd expect is missing or fails to connect, say so in one line instead of quietly working around it.

## Finding code

Prefer cheap, precise lookups to reading whole files:

1. **Orient.** Without a map of the repo in context, run `repomap -root . -max 80` (when installed) for the most-referenced files and their top-level symbols.
2. **Symbols:** Serena (`find_symbol`, `find_referencing_symbols`, `get_symbols_overview`) or a language-server MCP for definitions, references, callers and types. Check references before calling anything unused. Use only their read-only tools unless you're asked to edit.
3. **"Where's the code that does X":** a semantic code search (cocoindex-code) when connected.
4. **Text:** `rg -n 'pattern'`, narrowed with `-t go`, `-g '*.md'`, `-F` for literal strings. `ast-grep run -p 'PATTERN' -l LANG` when the shape matters more than the text (`fmt.Errorf($$$)`), search only, never `--rewrite`.
5. Read only the part of a file you need.

## Facts, docs and anything current: the ladder

Go down one rung at a time and stop at the first that answers. Every tool call resends the whole conversation, so a quick question gets at most one lookup, and one it can answer from knowledge gets none.

1. **What you already know**, only for things that can't change: language semantics, algorithms, maths, protocols by RFC, history, general concepts. Anything versioned, priced, released, scheduled, or about who runs what skips this rung. If you can't say why the fact couldn't have changed since your training, it isn't rung 1.
2. **Basic Memory**, only when the question is about Jason's own projects, setup or past work (the section below). Don't check it for a general fact or a library question.
3. **Context7** for anything about a library, framework, SDK, CLI or service, even ones you know well: `resolve-library-id`, then `query-docs` with one concept per query. Name the version the answer is for.
4. **Exa** (or the built-in web search) for everything else current, or when Context7 has nothing: search describing the page you want, then fetch the one or two best results.

If a rung's tools aren't connected, say so in one line and go to the next.

After rung 3 or 4, don't write to Basic Memory unasked. For a one-off question just answer. When the answer looks worth keeping (he's researching a topic, or he'll plainly ask again), offer in one line to cache it, and write it only if he says yes; the format is in [cache-note.md](cache-note.md). Never cache secrets, private code, or anything from a work codebase or Linear.

End an answer that needed a lookup with one source line:

- `◇ known` (rung 1)
- `◇ memory cache/neovim/vim-pack-lockfile (verified 2026-10-20)`, when you did use a note
- `◇ context7 /neovim/neovim`
- `◇ exa <url>`

Add `· cached → cache/<topic>/<slug>` when he said yes to caching.

Lookups in the middle of a task don't need the line.

## Notes and memory (Basic Memory)

- Basic Memory is the long-term store: decisions, project status, research, reference material. The app's built-in memory is the short-term cache.
- Before answering about Jason's own projects, setup or past work (and only then), check Basic Memory first: `search_notes` with a few keywords (not the whole question), `page_size` 3 to 5, text output; if the hits look off, retry once with `search_type="vector"`; `read_note` only the one or two you need. Use `build_context` only when relationships matter, and `recent_activity` only when the topic is recent work.
- Write at checkpoints, not every turn: a real decision, or when he says "save that" or "wrap up". Do it at the end of the reply, after the answer.
- Search before writing and update the existing note rather than adding another. Folders: `projects/`, `decisions/`, `reference/`, `learning/`, `cache/`. Record decisions with the reason, use `[category]` observations and `[[wiki links]]`.
- Freshness: every note has `last_verified` and `stale_after_days`. Use a stale note but say "as of <date>" and that it may have changed, and confirm with him before acting on it. Reading never refreshes a note; only his confirmation does.
- When a fact changes, don't delete it: `- [superseded YYYY-MM-DD] Was: X. Now: Y, because Z.`

## Everything else

- **Tasks:** Linear, following the `bud:planning` skill.
- **Documents:** Claude Docs, only when he asks for a doc.
- **Compressed output:** when a result says it was compressed (Headroom) and gives a way to fetch the original, retrieve the detail you need instead of working from the summary.
- **Skills:** load one only when the task is writing code, planning or filing issues, or cutting a release (`bud:code-style`, `bud:planning`, `bud:release`), or when he asks for it. A chat question doesn't need one.
