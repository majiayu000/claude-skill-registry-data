---
name: spec
layer: stack
description: Capture a POC's signed-off behaviour into its spec ledger (`<poc>/spec.json`) — the structured, walkable behaviour contract graduation freezes as authoritative. Run at the moment a behaviour gets signed off ("ok, this works"), while it's fresh — the same trigger as the HANDOFF.md update, but capturing the *behaviour as a testable entry* rather than the *decision as prose*. Use when a POC behaviour is approved, or asked to "capture this spec", "write the spec entry", "log this to the ledger".
argument-hint: "<poc-path> [behaviour summary]"
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Spec Skill — capture a signed-off POC behaviour into the ledger

A POC discovers its spec one behaviour at a time. This skill writes that discovery down as a
**structured entry** in `<poc>/spec.json` — the third leg beside `HANDOFF.md` (prose / architecture)
and `changelog.json` (chronological / archaeology). The spec ledger is the one **graduation freezes
as authoritative** and the **side-by-side comparison gate walks** (`/graduate` A0/C1). Without it,
"rebuild the experience" has no checkable contract and the rebuild drifts into a different UX (#988).

**The schema is owned by `pocs/CLAUDE.md`** ("Capture the spec ledger") — that's the single source
of truth for the field list. This skill is the *capture mechanic*; it does not redefine the schema.

## When to run

**The trigger is a sign-off:** a behaviour gets approved ("ok, this works") → capture it **now,
while it's fresh**, not at the end and not at graduation. Same moment you'd update `HANDOFF.md` — do
both. Reconstructing the ledger after the fact (the `/graduate` retrofit path) is the *lossy
fallback*, never the goal: an after-the-fact list can't be certified exhaustive.

If the behaviour is still being explored (not signed off), it's **too early** — capture it as
`status: "stopgap"` or `"new"`, never `"settled"`.

## The capture flow

1. **Locate the ledger.** `<poc>/spec.json` (next to `changelog.json` / `HANDOFF.md`). If absent,
   create it as an empty array `[]`. Confirm the poc path with Glob if not given.

2. **Draft the entry** from the signed-off behaviour. Fill every field the schema in `pocs/CLAUDE.md`
   lists — at minimum `id` (kebab, stable), `behaviour`, `when`→`expect`, `howToTest` (numbered, with
   before/after), and `status`. Two fields carry the method's weight:
   - **`hook`** — the `data-handoff`/`data-testid` selector that locates this state on the running
     page, so the *same walk* runs on POC **and** the graduated app. Plant one if the state has no
     stable anchor yet (see the `data-handoff` convention in `pocs/CLAUDE.md`).
   - **`status`** — `settled` (the contract, preserve — needs `signedOff`) · `stopgap` (known-temporary
     fake, replace at graduation) · `new` (an addition the POC left open) · `proposed` (drafted but not
     yet signed off — captured from artifacts at A0 retrofit, or proposed ahead of confirmation; flips
     to `settled` once a human reconciles it). Pick honestly; `stopgap`/`new`/`proposed` are not
     lesser — they tell graduation which gate governs the behaviour and whether it's confirmed yet.

3. **`settled` requires a recorded sign-off.** Only set `status: "settled"` with `signedOff`
   populated by the approval token (`lgtm vNN` / a comment ref). **Done is derived from this, never
   self-asserted** — and it's *enforced*: `.claude/hooks/gate-spec-signoff.mjs` blocks a `settled`
   entry with an empty `signedOff`. If you have the sign-off, record it; if not, keep it `stopgap`/`new`.

4. **Supersede, don't append blindly.** Specs evolve like `HANDOFF.md` (newest wins), *not* like the
   append-only changelog. If this behaviour replaces an earlier entry, set `supersedes` to its `id`
   and **edit/remove the stale one** — a ledger must read as "this is how it behaves now", never "here
   is everything we tried". Capture any rejected alternative in `consideredRejected` (`option → ❌ why`).

5. **Validate before writing.** The whole file stays a JSON array; every entry has a unique `id`; every
   `status` is one of `settled|stopgap|new`; every `settled` has a non-empty `signedOff`; every
   `supersedes` points at a real (or just-removed) `id`. Quick check:
   ```bash
   node -e 'const s=require("./<poc>/spec.json"); if(!Array.isArray(s))throw"not array";
     const ids=new Set(); for(const e of s){ if(ids.has(e.id))throw"dup id "+e.id; ids.add(e.id);
       if(!["settled","stopgap","new","proposed"].includes(e.status))throw"bad status "+e.id;
       if(e.status==="settled"&&!(e.signedOff||"").trim())throw"settled w/o signoff "+e.id; }
     console.log("spec ok:",s.length,"entries")'
   ```

6. **Surface it in-app** (if the POC has the changelog chip pattern) so a reviewer can walk and sign
   off entries against the running preview — the spec is the *walk script*, the live POC is the
   *expected result*. The builder POC shows a `vNN` chip; add the spec entries beside it.

## What you hand back

The updated `<poc>/spec.json` (valid, deduped, stale entries pruned), committed via `/commit` with
the same scope as the POC. If a behaviour was signed off, its entry exists — that's the acceptance.

## Conventions

Schema + the capture trigger live in **`pocs/CLAUDE.md`** (this skill defers to it). The `settled`
sign-off rule is the **done-rule** (`AGENTS.md`), enforced by `gate-spec-signoff.mjs`. Consumed by
`/graduate` at stage A0 (the frozen spec) and C1 (the walk). Pairs with the `HANDOFF.md` /
`changelog.json` updates — capture all three at sign-off.
