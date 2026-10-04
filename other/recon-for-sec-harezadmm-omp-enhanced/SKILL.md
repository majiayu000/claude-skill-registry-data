---
name: recon-for-sec
description: >-
  Entry P1 category router for reconnaissance and methodology. Use when mapping
  scope, discovering assets, fingerprinting technology, building endpoint
  inventory, and choosing the first high-value security testing path.
---

# Recon and Methodology Router

This is the starting router for new targets and unknown attack surfaces.

## When to Use

- You just received a new target and do not yet know what to test first
- You need to begin with asset discovery, tech fingerprinting, endpoint inventory, and test-route planning
- You want to build follow-up testing on structured methodology instead of random payload enumeration

## Skill Map

- [Recon and Methodology](../recon-and-methodology/SKILL.md)
- [Insecure Source Code Management](../insecure-source-code-management/SKILL.md) — .git/.svn/.hg exposure detection
- [Dependency Confusion](../dependency-confusion/SKILL.md) — Supply chain reconnaissance for internal package names

## Recommended Flow

1. First confirm in-scope assets and target type
2. Then perform asset discovery, port/service identification, technology fingerprinting, and endpoint collection
3. Route based on collected findings to [api-sec](../api-sec/SKILL.md), [auth-sec](../auth-sec/SKILL.md), [injection-checking](../injection-checking/SKILL.md), or [business-logic-vuln](../business-logic-vuln/SKILL.md)
## 1. CONFIRMING THE ROUTE

A router produces **one** artefact: the correct destination for an observed behaviour. Confirming a route
means the destination was reached by a **resolved link** and that the destination's own dispatch table was
then consulted - never that a technique was recalled from memory.

| Step | Question | What it proves |
|---|---|---|
| 1 | Is the **observed behaviour** recorded before the route is chosen? | routing is decided by the sink, not by the parameter's name |
| 2 | Is there a **negative control**: a benign value leaving the response unchanged? | the difference is caused by your input, not application noise |
| 3 | Was the destination **loaded by resolving its link**, and did the load succeed? | a route that 404s makes the agent proceed from memory |
| 4 | Was the destination's **own dispatch table** then applied? | the destination re-decides the vantage (passive, active, internal) before a technique is chosen |
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
| The probe that **distinguished** the chosen sink from the neighbouring candidates | the probe that establishes the vantage the observation came from |
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

This is the default first router for an unknown target, which makes it the easiest one to
enter by mistake and the most damaging one to *stay* in. Verify that scanning is still the
right activity before you spend the session on it.

| Step | Question | What it proves |
|---|---|---|
| 1 | Is the in-scope asset list confirmed in writing (scope file, program brief, engagement letter)? | Recon findings belong to a defined surface; unscoped discovery produces reportable-invalid work |
| 2 | Do you have more than one hostname, service, or endpoint to compare? | A single endpoint is not a recon problem — it is a single-target test, and a category router applies instead |
| 3 | Has the inventory stopped producing *new* items in the last pass? | Recon has a completion condition; unbounded enumeration is how engagements silently lose days |
| 4 | Do discovered endpoints already suggest identity, object references, or injected input? | Enumeration is done for now → dispatch to [api-sec](../api-sec/SKILL.md), [auth-sec](../auth-sec/SKILL.md), or [injection-checking](../injection-checking/SKILL.md) |
| 5 | Does the scope include downloadable source, `.git`/`.svn`/`.env`, source maps, or package manifests? | Two more routes exist here → [insecure-source-code-management](../insecure-source-code-management/SKILL.md) and [dependency-confusion](../dependency-confusion/SKILL.md) |
| 6 | Does the target involve coupons, pricing, inventory, invites, or multi-step state? | The highest-impact class for this target is elsewhere → [business-logic-vuln](../business-logic-vuln/SKILL.md) |
| 7 | Are you blocked by a WAF/CDN, or re-running the same tools for a third time? | The route is a bypass/scale question, not a discovery question — escalate to [hack](../hack/SKILL.md) for the phase-1 alternatives |
| 8 | Can you name the *next* skill you will load once recon ends? | If you cannot, the recon has no exit condition and will not end |

**Discovery without a stopping rule is not methodology.** The value of this router is that it
tells you when to leave it. Recon output that never feeds a category router is inventory kept
for its own sake.

## 4. OUTPUT STANDARD

| Item | Why |
|---|---|
| The confirmed scope, quoted from the source that defines it | Every later finding inherits its validity from this; an unquoted scope cannot be defended |
| The asset inventory as a table (host, service, technology, version, source of discovery, status) | The inventory *is* the deliverable; prose summaries cannot be de-duplicated or handed over |
| The provenance of each asset (DNS, certificate transparency, JS bundle, brute force, third-party dataset) | Provenance tells the reader how complete and how stale the list is |
| Which assets are live versus historical, with the check that established it | Dead hosts reported as live inflate scope and waste the next phase |
| The technology fingerprint *with the evidence* (header, cookie name, error signature, bundle marker) | "Looks like nginx" is not a fingerprint; a version-identifying artefact is |
| The endpoints/parameters discovered, and the ones deliberately not enumerated | Absence is information; an unstated gap reads as coverage |
| The named next router and the specific reason for that choice | Recon is judged by whether it produced a decision, not by how much it collected |
| Anything in scope that this router does not cover, stated explicitly | Prevents the engagement from assuming recon covers areas it structurally cannot |

### Routing failures — how they mislead

| Routing failure | How it misleads |
|---|---|
| An unknown single target routed here indefinitely | Enumeration runs for the whole session; no vulnerability class is ever tested and the report has inventory but no findings |
| A target whose scope is unconfirmed treated as fully in scope | Out-of-scope hosts are scanned and any resulting finding is invalid, no matter how severe |
| Recon findings dispatched without provenance | A stale asset inherited from a third-party dataset drives hours of work on a host that was decommissioned |
| A target already blocked by WAF/CDN kept on the discovery route | The same tooling is re-run against the same block page; the work is invisible in the report and the actual bypass route is never taken |
| Source-code exposure found but routed only as "interesting" | `.git`/`.env` and dependency manifests are treated as intel, not as their own two skill domains, and the leaked-secret route is never opened |
| Business-logic surface discovered but treated as recon output | Pricing, coupon, and state-machine flaws are the highest-impact class for such targets and are never tested |
| Recon output that names no next router | The agent returns to memory for exploitation, which is exactly what the skill-invocation rule forbids |
| A one-endpoint target routed here instead of to a category router | The correct skill is never loaded, and the single endpoint gets reconnaissance methodology applied to something that needed a decision between SQLi, authz, and logic |

## 5. MAINTENANCE REFERENCE — KEEPING THIS ROUTER CORRECT

A router is a **map**, and a map is wrong the moment the terrain moves. Every item below is
a concrete, checkable fix — not advice. Run them after any edit under `skills/impl/`.

1. **Every link resolves.** A route that 404s is worse than no route: the agent believes it
   has loaded doctrine and proceeds from memory, which is precisely what the skill-invocation
   rule forbids. Assert this with a link check, not by reading.
2. **Every domain in the routing table exists on disk.** A domain can be renamed or
   consolidated away while its row survives, producing a dead route. Domains named here:
   `recon-and-methodology` `insecure-source-code-management` `dependency-confusion`.

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
    f=skills/impl/recon-for-sec/SKILL.md
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

1. **Fix the row when the vantage changes.** A passive observation and an active probe are different
   findings, and a row that does not record the vantage produces evidence with no provenance.
2. **Require the vantage probe in the row.** State how the agent establishes where an observation came
   from, since the same data carries a different weight at a different vantage.
3. **Keep the wildcard caveat attached to every enumeration route.** A route to subdomain enumeration
   without the wildcard test produces a fabricated host list.
4. **Prune removed destinations with their counts.**
5. **Keep the return path to the P0 router current.**
6. **Re-run the link check after any `skills/impl/` edit.**

---

## 7. RELATED ROUTERS
- [recon-and-methodology](../recon-and-methodology/SKILL.md) — The long-form recon and methodology playbook
- [insecure-source-code-management](../insecure-source-code-management/SKILL.md) — .git/.svn/.hg exposure found during discovery
- [dependency-confusion](../dependency-confusion/SKILL.md) — Internal package names and supply-chain inventory
- [api-sec](../api-sec/SKILL.md) — Once endpoints and contracts are enumerated
- [auth-sec](../auth-sec/SKILL.md) — Once login, session, or token surfaces are found
- [injection-checking](../injection-checking/SKILL.md) — Once input reaches an interpreter
- [business-logic-vuln](../business-logic-vuln/SKILL.md) — Once workflow and state surfaces are visible
- [hack](../hack/SKILL.md) — the P0 master router; return here when no route above matches
- [CORE.md](../../../CORE.md) — the kill-chain phases this router dispatches into
