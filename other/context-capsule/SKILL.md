---
name: context-capsule
description: The capsule verb, invoked explicitly — reconcile from the live memory, write a resume-ready capsule, then stop. Mid-session checkpoint or completion capsule; a rolling best-effort version of the same write also runs automatically on every Stop event via daemons/stop-capsule-writer.mjs.
trigger: /context-capsule
status: Two-verb lifecycle — supersedes the v1 capsule skill and absorbs /close (there is no separate close ceremony).
related:
  - "docs/two-verb-lifecycle.md (design doc — schema, content gate, sovereignty rules)"
  - "daemons/capsule-verb.mjs (validateCapsuleText — required fields + content gate)"
  - "daemons/capsule-content-gate.mjs (content gate; shared with the stop-writer)"
  - "skills/resume/SKILL.md (the mirror verb)"
---

# /context-capsule — the capsule verb

**The entire job: reconcile → write the capsule → confirm it → chronicle → sync the vault → STOP.** The capsule absorbs `/close`: there is no separate close ceremony, and no separate stamping step — writing a valid capsule (content gate passes, required fields non-empty) and folding the session into durable memory is the capsule contract.

## When this skill fires vs the automatic verb

A rolling, best-effort version of this write already runs on every `Stop` event via `daemons/stop-capsule-writer.mjs` — you don't need this skill for ordinary turn-by-turn capture. Invoke `/context-capsule` for the explicit cases: a mid-session checkpoint before risky work, a completion capsule when a thread ships, or a handoff.

## Operator sovereignty (never violate)

- The capsule is **best-effort autosave, never a gate**. An operator `/clear` passes through whether or not a capsule landed; never tell the operator to wait on capsule machinery.

## Fences (never cross)

- **Do NOT write a narration capsule.** Reconcile-from-memory is the value: a capsule that restates the transcript instead of the live memory/git state is the trap this verb exists to prevent.

## Steps (tight + terminal)

1. **RECONCILE from live memory** — re-read the session log, active priorities, and this session's git commits. Record what happened, not what was said. Budget: **2–4 reads, no more**.
2. **WRITE** `vault/memory/capsules/<YYYY-MM-DD>-<slug>.md`:
   - Frontmatter — all four REQUIRED fields non-empty, no inline `#` comments on them, `waiting_on` quoted (never bare `null`): `id`, `objective`, `waiting_on`, `next_valid_action`; plus `parent_capsule_id`, `status: active`, `trigger`, `expires`, `tags`, `created_at`. Stamp `created_at` with the real current date-time at this write, **ISO-8601 with offset** (e.g. `2026-07-25T11:12:04-07:00`) — the selector parses this field, and a date-only stamp backdates the capsule to midnight UTC where it loses to every same-day autosave. `resume_trigger` and `success_criteria` are OPTIONAL — include them when they add real signal, omit otherwise.
   - Body — `[REFERENCE ONLY]` banner, then: `Done (don't redo)` · `Historical-Errors → Resolutions` · `Historical-Rejected-Approaches` · `Files-Read / Files-Modified` · `Operating-Facts` · `Pending-Gates` · `Claimed-Rows`. Historical- prefixes and latest-wins stay (anti-zombie).
   - `waiting_on` is the resume contract: write it so a fresh session can act from it alone — concrete items, owners, gates.
3. **CONFIRM the write.** Re-read the exact file you just wrote: it landed at the path you think it did, `id` matches the filename, and every required field is populated. Self-check the frontmatter against the field list and the content gate (injection echo / ceremony action, `daemons/capsule-content-gate.mjs`). There is no separate trusted-writer pass to catch a mistake after the fact, so an unread write is an unverified one. Repair before continuing.
4. **CHRONICLE — the close-parity pass.** This verb absorbed `/close`, so it has to absorb what `/close` actually did, or the durable record stops growing the moment you stop running the old verb:
   - **Memory-delta pass** — fold this session's real changes into the durable notes that changed (typically 2 to 6 files under `vault/memory/`). Precise edits, not a transcript dump.
   - **Stage directives** — anything decision-shaped or instruction-shaped that isn't already banked goes to `vault/memory/MEMORY_CANDIDATES.md`. A directive that exists only inside a capsule dies with that capsule: the capsule is spent on the next resume, and the directive is not meant to be.
   - **One `vault/memory/SESSION_LOG.md` line**, newest first: `- <YYYY-MM-DD> <capsule-id>: <one-line summary>`.
5. **SYNC fail-soft.** After the capsule and memory edits land, run `node daemons/vault-sync.mjs`. The helper requires the operator to approve every effective push URL in repository-local `aigent.vaultSyncPushUrl` before staging or publishing memory. A clone's `origin` is not approval. Never add that approval yourself to bypass a refusal; see `docs/vault-sync.md`. No remote remains a silent no-op. Unapproved destinations and Git failures are recorded in the memory root's `.daemon-errors.log`; the CLI remains silent and exits 0, which is not proof of sync. Note the byte position of the resolved memory root's `.daemon-errors.log` before the call and inspect new `tag="vault-sync"` records afterward; an old last line is not this call's outcome. Keep any unsynced or unverified status in the durable record before step 7, without blocking the acknowledgement or clear. Local capsules remain on disk whether or not a remote backup succeeds.
6. **EXTENSION ACK, only if this install declares one.** Run this and act on what it prints:

   ```
   node daemons/lifecycle-extension.mjs render capsule_ack --capsule-id <the confirmed capsule id> --root <the installed root>
   ```

   If it prints a line, do exactly what that line says, now, before step 7. If it prints nothing and stderr is empty, there is no declaration to run and this step is over: that is the ordinary standalone install. If stderr carries a line beginning `LIFECYCLE-EXTENSION:`, a declaration exists but is not being run, either refused whole (`declaration ignored:`) or held because its field could not be rendered truthfully (`capsule_ack not rendered:`), so report that line and improvise no substitute. It always exits 0, so a bad declaration can never fail the capsule. Do not open `.aigent/lifecycle-extension.json` yourself: this command is the only reader, which is what keeps a declaration refused on resume refused here too, by the same validator.

   **Why it runs HERE and not after step 7**, even though an extension otherwise follows the core acknowledgement: step 7's literal IS the acknowledgement the supervising machinery watches for, and the clear is gated on that acknowledgement and on nothing after it. The moment the literal is observed the clear can be minted, mid-turn, without waiting for anything else this turn does. A step placed after the literal therefore runs inside a window the core already treats as closed, and races the clear it is meant to precede. Running the extension one step earlier costs nothing and removes the race.

7. **STOP. Emit this EXACT line, nothing else, and then be silent:**

   ```
   Capsule Complete, Ready For Clear
   ```

   Not a summary. Not the capsule path. Not what shipped, not what is ready, not
   what comes next. **This literal string and nothing more.** If you have
   something to say, it belonged in the capsule.

   **Why it is a fixed literal and not "keep it short":** every word after the
   capsule is a NEW assistant turn appended to the transcript, and the auto-clear
   checkpoint compares the captured offset against the transcript size. A turn
   landing after the capture makes the capsule read as stale, and the cycle holds
   on `checkpoint-transcript-short` — **the seat cannot clear, because it
   announced that it was ready to.**

   A fixed string makes the trailing bytes ARITHMETIC instead of a guess, which
   is what lets `CHECKPOINT_TAIL_TOLERANCE_BYTES` (auto-clear-transport.mjs) be
   derived rather than invented: entry-envelope max 1,361 bytes (measured over 72
   real short assistant entries) + a 120-char ceiling + 5% margin. Anything
   bigger than that budget is a second turn or real work, and must still hold.
   **Free-form prose here re-breaks the cycle silently** — it will look like it
   worked and the seat will simply never clear.

   Measured on a live standalone seat 2026-08-04: the capsule wrote correctly,
   the seat then said "Capsule saved: … Research session complete. 40
   production-quality documents delivered … Ready for next phase.", and the cycle
   stalled behind exactly those bytes. The instruction that used to sit on this
   line — "one line acknowledging the capsule path" — is what produced it.

## Lifecycle

`active → resumed → resolved`. The resume RUNTIME marks the capsule `resumed` mechanically at load (`daemons/resume-verb.mjs` via `markCapsuleConsumed`) — never edit a capsule's status by hand, and never expect the same capsule to be silently re-resumed on a later clear. A capsule superseded by a newer one, or `resumed` >30 days, resolves. `/open`/`/close` are retired — resume absorbs open, this verb absorbs close.

## When NOT to capsule

- Mid-thought (finish the thought).
- Trivial sessions a fresh session could reconstruct from memory alone.
- Inside a dispatched sub-agent (the dispatch brief IS the capsule).

**Declining still ends at Step 7.** If this invocation is an **injected**
`/context-capsule` from the auto-clear cycle (not the operator's own),
"trivial" only excuses the WRITE — steps 2–5 — never step 6 and never the
ack. Before going
quiet: (a) confirm a valid prior capsule already exists on disk for this
session — `daemons/stop-capsule-writer.mjs` wrote one on the last `Stop`
event, and the checkpoint's capsule-exists gate feeds on it being there,
so verify rather than assume; (b) still emit the exact literal from Step 7,
`Capsule Complete, Ready For Clear`, as the final act, then go silent. The
cycle is waiting on that literal alone — "nothing to capsule" is not an
exemption from producing it. The completion acknowledgement is still required when an existing valid capsule is reused. The injected cycle waits on that exact literal; "nothing to capsule" is not a completion signal.
