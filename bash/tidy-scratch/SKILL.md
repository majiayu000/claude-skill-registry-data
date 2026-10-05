---
name: tidy-scratch
description: >-
  Use when the scratch notebook has accumulated stale or finished threads and needs cleaning —
  "tidy scratch", "garbage collect scratch", "prune old notes", "what can I delete", "archive
  done threads".
allowed-tools: Bash(git *), Bash(gh *), Bash(bun *), Bash(find *), Bash(ls *), Bash(date *), Bash(mkdir *), Bash(mv *), Bash(rm *), Bash(printf *)
---

# Tidy scratch — date-aware GC for the scratch notebook

A **read → propose → execute** sweep. This is the *only* ccx skill that proposes destructive
actions; save-state stays a pure read-only dashboard. The sweep is **dry-run by default** — it
prints a plan and touches nothing until you confirm. If the scratch dir is not version-controlled
(the usual setup), a delete is **permanent**. When in doubt: archive (move), don't delete.

## Live data (injected at load)

**Project + config:**
!`bun "${CLAUDE_PLUGIN_ROOT}/scripts/where.ts"`

**Now:** !`date "+%Y-%m-%d %H:%M %Z"`

**Folder scan — date-aware, stalest first** (newest-file age per folder; `STATE=NO` = no handoff doc):
!`bun "${CLAUDE_PLUGIN_ROOT}/scripts/scan.ts"`

**Open PRs (a matching open PR keeps a thread alive):**
!`gh pr list --limit 30 2>/dev/null || echo "(gh unavailable / not a GitHub repo)"`

## Then do this

1. **Classify** every folder from the scan. With `ticket_system: none` there is **no external
   "closed" oracle** — only age + PR signals exist, so stay patient and conservative. `age` = the
   scan's `age_days`; thresholds are *defaults you may adjust per item* when presenting the plan:
   - **KEEP (active)** — `age < 3` (protects an active spike), OR an open PR that matches the
     thread's topic/branch.
   - **ARCHIVE (likely done)** — has a STATE doc AND `age > 30` AND no open PR. (Longer threshold
     than a ticket-oracle setup would use: age alone must be more patient.)
   - **ADOPT (unfiled work)** — `STATE = NO` AND `files > 3` — too much accumulated work to be
     throwaway; propose creating a STATE doc for it (offer /ccx:start-thread), never delete in
     this pass.
   - **DELETE (throwaway)** — `STATE = NO` AND `age > 14` AND `files ≤ 3` (no handoff value +
     cold + tiny).
   - **DELETE (empty)** — `files = 0`.
   - **FLAG → default KEEP (unsure)** — anything that fits no rule above, and every `kind: hub`
     reference note. **Never auto-propose deleting a folder that has a STATE doc.**
2. **Print the PLAN — execute NOTHING yet.** One table, stalest first:

   | item | class | proposed action | why | last edit (age) |
   |---|---|---|---|---|

   End with a one-line tally: `N delete · M archive · K adopt · rest keep`.
3. **Confirm.** Ask: apply **all**, a **subset** (named), or **none**. Wait for the answer.
4. **Execute only what was approved**, echoing each action (paths from the injected config block):
   - **archive:** `mkdir -p <scratch_root>/<archive_dir> && mv <scratch_root>/<slug> <scratch_root>/<archive_dir>/`,
     then date-stamp: `printf '\n_Archived %s by ccx tidy-scratch._\n' "$(date +%Y-%m-%d)" >> <scratch_root>/<archive_dir>/<slug>/<state_basename>`
   - **delete:** `rm -rf <scratch_root>/<slug>` — permanent if the notebook isn't version-controlled.
5. **Reindex.** Run /ccx:save-state so the INDEX reflects the cleanup. Then a ≤3-line summary:
   deleted / archived counts and the new active-thread count.

## Safety rails (non-negotiable)

- **Dry-run is mandatory** — never delete, move, or prune before the step-3 confirmation.
- **Hard `rm` is only ever proposed for folders with no STATE doc AND ≤3 files.** Anything
  carrying a STATE — or carrying real bulk (>3 files) — is *archived* or *adopted*, never
  deleted; its work survives.
- **When unsure, archive, don't delete** — without a ticket system there is no authoritative
  "this is finished" signal, only age.
- **Reads the clock every run** (`scan.ts` + `date`) — no date is ever hardcoded, not even the
  model's notion of "today". Run it next month and the ages come out next-month-correct.
- Archived threads drop off the save-state dashboard (scans skip the archive dir). A graph view
  may still show them until the archive dir is excluded from its filter — one-time setup, out of
  scope for this per-run GC.
