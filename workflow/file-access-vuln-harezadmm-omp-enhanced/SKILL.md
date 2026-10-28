---
name: file-access-vuln
description: >-
  Entry P1 category router for file access and upload workflows. Use when
  testing download endpoints, file paths, local file inclusion, upload flows,
  preview pipelines, archive extraction, or storage and sharing boundaries.
---

# File Access Router

This is the routing entry point for filesystem paths, download endpoints, upload pipelines, and file preview handling.

## When to Use

- Parameters, filenames, download endpoints, or import flows influence file paths
- The target supports upload, preview, transcoding, extraction, sharing, download, or proxied file access
- You need to decide whether this is path traversal/LFI or an upload-validation/processing-chain issue

## Skill Map

- [Path Traversal LFI](../path-traversal-lfi/SKILL.md): path traversal, file read, wrapper abuse, include chains
- [Upload Insecure Files](../upload-insecure-files/SKILL.md): upload validation, storage paths, processing chains, overwrite risk, preview/share boundaries

## Recommended Flow

1. First identify whether the entry point is a path parameter, download endpoint, or upload workflow
2. Then locate whether the issue appears in accept, store, process, or serve stages
3. Small path-chain and upload-bypass samples are merged into the main topic skills; no separate payload entry is needed

## Related Categories

- [injection-checking](../injection-checking/SKILL.md)
- [business-logic-vuln](../business-logic-vuln/SKILL.md)
## 1. CONFIRMING THE ROUTE

A router produces **one** artefact: the correct destination for an observed behaviour. Confirming a route
means the destination was reached by a **resolved link** and that the destination's own dispatch table was
then consulted - never that a technique was recalled from memory.

| Step | Question | What it proves |
|---|---|---|
| 1 | Is the **observed behaviour** recorded before the route is chosen? | routing is decided by the sink, not by the parameter's name |
| 2 | Is there a **negative control**: a benign value leaving the response unchanged? | the difference is caused by your input, not application noise |
| 3 | Was the destination **loaded by resolving its link**, and did the load succeed? | a route that 404s makes the agent proceed from memory |
| 4 | Was the destination's **own dispatch table** then applied? | the destination re-decides between traversal, inclusion, and upload before a technique is chosen |
| 5 | Is the **interpreter/sink named**, not the payload family? | the technique, severity, and fix all follow from the interpreter |
| 6 | Is **one interpreter at a time** observed, with a probe that distinguishes it? | probing the wrong sink burns the endpoint's error budget and teaches nothing |
| 7 | If no row matches, was the **non-coverage statement** followed? | absence of a route is information |

**A resolved link, a named sink, and a negative control.** A route chosen from the input's appearance rather
than its sink is the single most expensive mistake in this domain, because the wrong subtree is probed, comes
back clean, and the finding is recorded as "no issue".

---

## 2. EVIDENCE STANDARD

The router's evidence is **the route and the observation that justifies it**, plus the dispatch trail.

| Item | Why |
|---|---|
| The observed behaviour, verbatim, before any routing decision | The route is a conclusion about this observation; record the premise |
| The benign request and the probe request, both verbatim, plus both responses | Routing on a difference requires both sides of the difference |
| The negative control value and its unchanged response | Separates your input's effect from "this endpoint fails on everything" |
| The **sink/interpreter identified**, with the observation that established it | The destination is derived from the sink, so the sink is the load-bearing fact |
| The destination domain **actually loaded**, and that its link resolved | A resolved link is the router's own correctness condition |
| The probe that **distinguished** the chosen sink from the neighbouring candidates | the probe that separates a path-traversal read from a local file inclusion |
| Any route **not taken** and why it was excluded | The eliminated branches are half the routing argument |
| The return path when nothing matched | the instruction to return to the parent router is present and followed |

### Route failures - how they mislead

| Route failure | How it misleads |
|---|---|
| Routed on the parameter's **name** rather than the sink | The wrong subtree is probed, returns clean, and a real finding is closed as "no issue" |
| Routed on a **500 or an error page** | Many parsers fail on any malformed value; an error is not a reachable sink |
| **Two plausible interpreters**, only one row taken | The untested one is silently marked clean and coverage is claimed for a sink never reached |
| Route followed **from memory** after a dead link | The agent believes it loaded doctrine while proceeding without it |
| **No negative control** | Application noise is reported as input-coupled behaviour |
| **In-band assumption on a blind sink** | Timing and out-of-band channels are never attempted, so a real vulnerability is reported as not reproducible |
| A **destination consolidated away** while its row survives | The router looks complete while dispatching into nothing |
| A **workflow-only domain** routed as a technique | Phantom coverage: the file loaded never describes a testing procedure |

---

---

## 3. DISPATCH VERIFICATION

This router has two routes and they are decided by **where the file boundary is crossed**,
not by whether the word "file" or "upload" appears in the URL.

| Step | Question | What it proves |
|---|---|---|
| 1 | Is there a parameter, filename, template name, or download path whose value the client controls? | A path is addressable → [path-traversal-lfi](../path-traversal-lfi/SKILL.md) |
| 2 | Does the value reach a filesystem read whose result is returned (body, status code, error text, timing)? | You have an observable read channel; without one this is not yet a finding |
| 3 | Is there an upload, import, archive-extract, preview, or transcode stage? | A write/process pipeline exists → [upload-insecure-files](../upload-insecure-files/SKILL.md) |
| 4 | Does the stored file get served back, and from a path you can influence? | Traversal and upload compose here; test both directions on the same endpoint |
| 5 | Can a benign value and a traversing value be compared on the *same* endpoint? | Establishes input-coupled behaviour rather than a generic 500 |
| 6 | Is the path accepted only after normalisation (`../`, encoded `%2e%2e`, double-encoding, unicode)? | Distinguishes a real filter from a filter you have not yet shaped input around |
| 7 | Does the download response come from an object store/CDN URL rather than the app? | The app may be clean while the storage policy is the actual boundary — note it, then test the URL's own authorization |
| 8 | If neither route matches (no path control, no upload/process stage) | The domain does not apply — return to [injection-checking](../injection-checking/SKILL.md) or [business-logic-vuln](../business-logic-vuln/SKILL.md) |

**A file download is not automatically a traversal.** Signed URLs, object-store redirects,
and fixed storage paths are all correct designs. The route applies when *the client's value
selects the file*, which is a claim you must prove with two different values.

## 4. OUTPUT STANDARD

| Item | Why |
|---|---|
| Which stage was reached: accept, store, process, or serve | The four have different owners and different fixes; "file upload bug" is not actionable |
| The exact request, the exact file/path value used, and the exact response | Path findings are value-specific; paraphrasing loses the bypass that worked |
| The benign value and the traversing value, both, with responses | Proves the file returned is selected by the input and is not a default asset |
| Whether the file that came back is *outside* the intended root, stated as an absolute path | "It returned a file" is not a finding; "it returned `/etc/passwd`" is |
| For uploads: whether the file executes, is served as a different content type, or overwrites an existing object | Converts an upload-validation gap into a severity claim |
| For archives: whether entries escape the extraction root | Zip-slip is a write primitive, not a validation nicety |
| Whether the pipeline is asynchronous, and how the processed artefact is retrieved | Async processing means the vulnerable stage is often not the one you first touched |
| The authorization model of the served file (anonymous, session, signed URL) | A traversal to a file you were already entitled to read is not a finding |

### Routing failures — how they mislead

| Routing failure | How it misleads |
|---|---|
| Upload endpoint routed to path traversal | Validation bypass, content-type confusion, and processing chains are never tested; the write primitive is missed while read paths are probed |
| Download endpoint routed to upload validation | Traversal out of the storage root is never attempted, so the classic high-severity read is replaced by a low-severity validation note |
| A preview/transcode stage routed to neither route | The processing chain — the actual attack surface — is never touched; the report covers only the accept stage |
| Filename control treated as a naming issue rather than a path issue | A filename that is later concatenated into a path and served is never tested with a traversal payload |
| An object-store redirect treated as an application path bug | The app-level filter is tested against a request the app never handles; the storage policy that actually decides access is never examined |
| CDN-cached download treated as an authorization boundary | Cache key confusion is filed as a file-access issue, and a genuine shared-cache leak is misdiagnosed |
| Archive extraction treated as pure validation | Entry-name traversal (zip-slip) and symlink entries are never tried, so a remote write primitive is reported as "accepts .zip" |
| A signed URL treated as no test needed | Expiry, scope binding, and path binding of the signature are never verified; a re-usable signature for arbitrary objects goes unreported |

## 5. MAINTENANCE REFERENCE — KEEPING THIS ROUTER CORRECT

A router is a **map**, and a map is wrong the moment the terrain moves. Every item below is
a concrete, checkable fix — not advice. Run them after any edit under `skills/impl/`.

1. **Every link resolves.** A route that 404s is worse than no route: the agent believes it
   has loaded doctrine and proceeds from memory, which is precisely what the skill-invocation
   rule forbids. Assert this with a link check, not by reading.
2. **Every domain in the routing table exists on disk.** A domain can be renamed or
   consolidated away while its row survives, producing a dead route. Domains named here:
   `path-traversal-lfi` `upload-insecure-files`.

3. **No duplicate routes.** The same observed behaviour must not appear twice with two
   different destinations. Where two domains genuinely overlap (the short `attack-*`
   methodology files and their long-form playbooks), the row must say so and instruct the
   agent to load both, rather than leaving two identical-looking entries.
4. **Coverage counts stay accurate.** Any count stated here must match the number of distinct
   deep topic skills actually routed. Counting prose mentions inflates coverage; counting only
   links that resolve to an existing `SKILL.md` is the correct denominator.
5. **Re-verify when a domain is added or removed.** Adding a domain under `skills/impl/` is an
   incomplete change until this router routes it or records it as deliberately unrouted.
   Removal is the same change in reverse — prune the row *and* the count in one commit.
6. **Prune dead domains.** A scheduled or CI link check that resolves every destination here
   prevents the slow rot where routes point at skills that were consolidated away and the
   router looks complete while dispatching into nothing.
7. **Workflow-only domains stay excluded.** CORE.md records 36 of the 199 `impl/` domains as
   agent-workflow and meta-tooling skills (handoff, writing, TDD, setup) that are not
   kill-chain techniques. Routing them manufactures phantom coverage: the agent loads a file
   that never describes a testing procedure.
8. **Ordering and phase stay consistent with CORE.md.** This router is reached from the phase
   table and dispatch block in `CORE.md`. If phases are re-cut there, the recommended flow
   here must move with them, or the router will dispatch into a phase the kill chain no
   longer contains.
9. **A self-check script exists.** `sv_check.sh` at the repository root is the existing
   precedent: it asserts size, section count, a fenced block, link liveness, and topic
   keywords. A router check is the same shape — link resolution, domain existence, domain
   count, fence parity, and presence of the three closing sections.

    ```bash
    # router self-check — run from the repository root
    f=skills/impl/file-access-vuln/SKILL.md
    echo "bytes: $(wc -c <"$f")  numbered sections: $(grep -c '^## [0-9]' "$f")"
    d=$(dirname "$f")
    # 1. every relative link must resolve to a real file
    grep -oE '\]\(\.\./[^)]+\)' "$f" | tr -d '](' | sed 's/)$//' | sort -u |
      while read -r p; do [ -f "$d/$p" ] || echo "DEAD LINK $p"; done
    # 2. fence parity must be even
    n=$(grep -c '^\x60\x60\x60' "$f"); [ $((n % 2)) -eq 0 ] || echo "ODD FENCE COUNT: $n"
    # 3. the three closing sections must be present and numbered
    for s in 'DISPATCH VERIFICATION' 'OUTPUT STANDARD' 'MAINTENANCE REFERENCE'; do
      grep -q "^## [0-9]*\. $s" "$f" || echo "MISSING SECTION: $s"; done
    ```

10. **The router states what it does NOT cover.** Absence of a route is information; silence
    is not. A target that reaches this domain and matches no technique here must be told to
    return to the P0 router rather than told nothing. Update the non-coverage statement
    whenever the boundary moves.

---

## 6. REMEDIATION REFERENCE - CONFORMANCE OF THE ROUTE

1. **Fix the row when the read/write boundary moves.** A traversal read and a local file inclusion are
   different findings with different proofs, and a merged row cannot be verified.
2. **Require the distinguishing probe.** State which observation separates a path traversal from an LFI,
   because the same parameter frequently supports both.
3. **Route upload paths to their own row.** An upload flaw is not a read-through flaw, and merging them
   loses the write primitive entirely.
4. **Prune removed destinations with their counts.**
5. **Keep the return path to the P0 router current, and the non-coverage statement accurate.**
6. **Re-run the link check after any `skills/impl/` change.**

---

## 7. RELATED ROUTERS
- [path-traversal-lfi](../path-traversal-lfi/SKILL.md) — Client-controlled path reaching a filesystem read
- [upload-insecure-files](../upload-insecure-files/SKILL.md) — Accept, store, process, and serve stages of an upload pipeline
- [injection-checking](../injection-checking/SKILL.md) — When the file content itself reaches an interpreter
- [business-logic-vuln](../business-logic-vuln/SKILL.md) — When storage, quota, or sharing rules are the actual flaw
- [hack](../hack/SKILL.md) — the P0 master router; return here when no route above matches
- [CORE.md](../../../CORE.md) — the kill-chain phases this router dispatches into
