---
name: hashline
description: Hash-anchored file editing with hashline — read a file as line:hash anchors, then patch by anchor so an edit against drifted content is rejected instead of silently landing on the wrong line. Use whenever hashline is available, as a native MCP server or as a Prime Agent kernel skill, for reads, creates, patches, deletes, and renames.
---

# hashline

Every line carries an `xxh32` content hash. You target lines by `line:hash`
anchors instead of by line number or by matching a string. If the file drifted
since you read it, the hash no longer matches and the patch is rejected — you
never write to the wrong place, and you find out immediately rather than three
edits later.

Requires the `hashline` binary (developed against 0.9.1) on `PATH`, or
`HASHLINE_BIN` pointing at it.

## Getting the tools

**Any harness with native MCP support (Claude Code, Codex, …)** — register the
stdio server and call its tools directly:

```json
{ "mcpServers": { "hashline": { "command": "hashline", "args": ["mcp"] } } }
```

**Prime Agent** — this skill ships a Python package that speaks the same stdio
server from the IPython kernel. See
[`references/prime-agent-setup.md`](references/prime-agent-setup.md) for install
and the AGENTS.md rules; once loaded:

```python
import hashline
print(await hashline.read("src/auth.py"))
```

Every kernel call is `async` — always `await`. The rest of this skill applies to
both: same server, same tools, same patch syntax.

## Workflow

Always **read → patch → verify**. The read gives you the anchors; the patch
result is the re-read file, so it doubles as the verification.

```
[src/auth.py#1a2b]
1:4f|def verify_token(token):
2:a3|    decoded = jwt.decode(token, SECRET)
3:9c|    return decoded
```

`1a2b` is the whole-file hash; `2:a3` is the anchor for line 2. Copy anchors
verbatim from the read — never guess a hash.

```python
await hashline.patch("src/auth.py", """SWAP 2:a3:
+    decoded = jwt.decode(token, SECRET, algorithms=["HS256"])""")
```

## Operations

Each op is a line; content lines are prefixed with `+`. Ranges are `N..M`
(`N.=M` also accepted). The `:HH` hash is optional but **always include it** —
it is the whole point of the tool.

| Op | Effect |
|----|--------|
| `SWAP N:HH:` + `+lines` | Replace line N |
| `SWAP N:HH..M:HH:` + `+lines` | Replace lines N through M |
| `DEL N:HH` | Delete line N |
| `DEL N..M` | Delete lines N through M |
| `INS.PRE N:HH:` + `+lines` | Insert before line N |
| `INS.POST N:HH:` + `+lines` | Insert after line N |
| `INS.HEAD:` + `+lines` | Insert at start of file |
| `INS.TAIL:` + `+lines` | Insert at end of file |
| `SWAP.BLK N:HH:` + `+lines` | Replace the whole syntactic block around N |
| `DEL.BLK N:HH` | Delete the syntactic block around N |
| `INS.BLK.PRE` / `INS.BLK.POST N:HH:` + `+lines` | Insert before/after the block around N |

Multiple ops in one patch, wrapped in envelope markers:

```
*** Begin Patch
SWAP 5:1a:
+    decoded = jwt.decode(token, SECRET, algorithms=["HS256"])
DEL 9:c3
INS.POST 12:d4:
+    log.info("verified %s", decoded["sub"])
*** End Patch
```

**Ops within one patch address the ORIGINAL line numbers** — do not re-number
for earlier inserts or deletes in the same patch.

Use `dry_run=True` to validate anchors without writing.

## The other tools

| Tool | Arguments |
|------|-----------|
| `read` | `file`, `json=False` |
| `patch` | `file`, `patch`, `dry_run=False` |
| `write` | `file`, `content`, `force=False` (create; `force` to overwrite) |
| `find_block` | `file`, `anchor` — the structural block around a `line:hash` |
| `remove_file` | `file` |
| `rename_file` | `src`, `dst` |

The parameter is `file`, not `path`. Relative paths resolve against the working
directory. `list_tools()` discovers them at runtime if in doubt.

## Rules

- **Read before you patch, every time.** Anchors from an earlier turn may be stale.
- **Never invent an anchor.** Copy `line:hash` from the most recent read output.
- **Failures come back as text, not exceptions.** A rejected patch returns a
  string starting with `Error:` (e.g. `line 2 content changed since last read
  (expected hash ff, got bf)`) and the call still "succeeds". Read the returned
  text before assuming the edit landed.
- A rejected patch means the file changed under you. Re-read and rebuild the
  patch — do not retry with the hash stripped off.
- Prefer `SWAP.BLK` over a long `SWAP N..M` when replacing a whole function.
- Use this instead of string-replace edit tools, `open(...).write()`, `sed`, or
  shell heredocs. Those bypass the drift check that makes hashline worth using.

## Troubleshooting

- `RuntimeError: hashline binary not found` — install hashline, or set
  `HASHLINE_BIN` to its absolute path.
- `unknown operation` in the warnings — the op name or the `line:hash` is
  malformed. Re-read the file and rebuild the anchor from its output.
