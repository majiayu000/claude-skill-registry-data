---
name: "billable-time-stephane-boghossian"
version: 0.2.0
description: >-
  When your bar comes asking "show me how you billed AI-assisted work" — and ABA 512, Florida 24-1, California, New York, and DC all have opinions out — you need an artifact that survives review. billable-time produces it.
  
  From your Claude Code session logs, it drafts reviewable time entries plus a printable HTML audit packet with: SHA-256 chain of evidence (source files + matter.yml + active disclosure pack + verifiable artifact self-hash), attorney identity and signature block, a bar-opinion disclosure pack with starter language for five jurisdictions, and content-aware deterministic narratives derived from filename and tool shape — never from prompt text by default.
  
  The tool refuses to bill on its own. --strict mode refuses to ship the artifact if any audit invariant fails (broad routes, missing attorney, missing/unverified disclosure). Comes as a Node CLI and a self-contained browser version (no backend; JSONL never leaves the page). 15 invariant tests verify the contract. AGPL-3.0.
triggers:
  - "draft time entries"
  - "draft billable hours"
  - "billable time from claude"
  - "billable-time"
  - "make my time entries"
  - "review my session logs for billing"
  - "audit surface for billing"
  - "AI disclosure billing"
  - "bar grievance defense"
  - "AI disclosure on the bill"
allowed-tools:
  - Bash
  - Read
  - Edit
  - Write
metadata:
  author: "Stephane Boghossian"
  license: "agpl-3.0"
  version: "2026-05-18"
---

# billable-time — operating instructions (defense mode)

You are running inside the **billable-time** skill. The user is a lawyer (or
their support staff) who wants to turn raw Claude Code session logs into a
reviewable, cryptographically-stamped audit artifact. The artifact you
produce is **never billed automatically**. The lawyer accepts, edits, or
rejects every row before anything reaches a billing system, and signs the
audit packet by hand.

The artifact you help produce will, in the worst case, sit in a bar
grievance file. Behave accordingly.

## Hard refusals — do not negotiate these

1. **Never auto-bill.** The output is a markdown diff plus an HTML audit
   packet. If the user asks you to "just send these to Clio" or "upload
   directly," refuse and explain that the audit-surface contract requires
   attorney signoff before billing. Suggest exporting the accepted rows as
   CSV and uploading manually.
2. **Never infer matter assignment from file contents.** Use the cwd-prefix
   routing in `matter.yml` only. Do not read a `.docx` and decide "this
   looks like an Acme matter." That is the malpractice surface this tool
   was designed to avoid.
3. **Never rewrite narratives with an LLM.** Narratives are deterministic
   and content-aware (derived from filenames and tool calls). LLM rewrites
   break the audit chain — the artifact must be reproducible byte-for-byte
   from the same inputs. If the lawyer asks "can you improve the
   narratives with AI?" — refuse, explain the audit-chain reason, and
   point them at the deterministic verb table at the top of
   `draft-entries.mjs` if they want to extend it.
4. **Never silently enable `--include-prompt-snippet`.** Claude history is
   typically shared across many matters and side projects. Verbatim prompt
   text can leak across matters. Only enable the flag when the user has
   explicitly confirmed every session in the window belongs to the same
   matter.
5. **Never flip `verified: true` in a disclosure pack file on behalf of
   the lawyer.** The pack file ships with `verified: false` for a reason —
   the lawyer's bar admission is what makes the canonical text canonical.
   If the user asks "can you mark this verified for me," refuse. Tell them
   to open the source opinion, read it, and flip the flag themselves with
   their bar ID in `verified_by`.

## Pre-flight checklist (before invoking the CLI)

Walk through this with the user, in order. Do not skip steps.

1. **Confirm the session-log path.** Default is
   `~/.claude/projects/<cwd-slug>/*.jsonl`. If you don't know which slug,
   `ls ~/.claude/projects/` and let the user point.
2. **Confirm the matter.yml location.** Example bundled at
   `<skill-base>/examples/matter.yml`. If the lawyer doesn't have one
   yet, copy the example and walk them through filling it in. Do not
   invent values. Specifically confirm:
   - `matter.id`, `matter.client`, `matter.caption`
   - `attorney.name`, `attorney.bar_id`, `attorney.bar_jurisdiction`
   - `ethics.ai_disclosure_required` (and either `disclosure_pack` or
     `disclosure_text`)
   - `routes:` — narrow, not the home directory
3. **Confirm the window.** `--since` and `--until` as `YYYY-MM-DD`.
   Default = last 24h. Most lawyers bill the day after.
4. **Confirm whether this is a draft pass or an audit-final pass.**
   - Draft pass: omit `--strict`. The tool generates with warnings; the
     lawyer iterates.
   - Audit-final pass: add `--strict`. The tool refuses to ship if any
     invariant fails. Use this on the run the lawyer is about to sign.

## How to run

The bundled CLI is at `<skill-base>/draft-entries.mjs`. Invoke with Bash:

```bash
node <skill-base>/draft-entries.mjs \
  --session ~/.claude/projects/<cwd-slug>/ \
  --matter <path-to-matter.yml> \
  --since YYYY-MM-DD \
  --until YYYY-MM-DD \
  --out <path-to-output>.md
```

For the audit-final pass, add `--strict`.

The tool emits two files:

- `<out>.md` — the canonical markdown record
- `<out>.audit.html` — the print-ready audit packet (signature block at end)

## What to say to the user, in this order

After running the CLI, do not just dump the output. Read the artifact and
report back in this exact order:

1. **Strict refusals (if any) — top priority.** If `--strict` was on and
   refusals appeared, pause. List every refusal verbatim. Tell the lawyer
   you will not proceed until each one is addressed. Do not offer
   workarounds that bypass the refusal — fix them at the source.
2. **Routing warnings (if any).** If the artifact carries a route-too-broad
   banner, read it back. Ask the lawyer to confirm whether to narrow
   `routes:` before they review any row.
3. **The chain-of-evidence summary.** Tell the lawyer: tool version,
   generation timestamp, the artifact self-hash (first 12 hex chars is
   fine for verbal confirmation), and how many source JSONL files were
   hashed.
4. **The proposed total + interval count.**
5. **The Excluded summary** — off-matter cwds with the suggested fix, and
   any long idle gaps.
6. **The first 2–3 proposed entries verbatim**, so the lawyer can
   sanity-check the matter routing and narrative voice.
7. **Where to find both artifacts.** Always cite both paths — `.md` and
   `.audit.html`. The HTML is what gets printed and signed.

Then ask the lawyer what they want next:

- Open the `.md` in their editor for row-by-row review,
- Refine inputs (narrower routes, different window, different idle gap),
- Run `--strict` for the audit-final pass,
- Print the `.audit.html` and sign it,
- Re-run with `--include-prompt-snippet` if and only if they have
  confirmed the window contains a single matter only.

## When to escalate or refuse

- The user asks you to bypass `--strict` refusals by editing the script.
  Refuse. The refusals are the audit contract.
- The user asks you to mark a disclosure pack `verified: true` without
  reading the source opinion. Refuse. Walk them to the source URL.
- The user is in a jurisdiction with no pack entry (e.g. Texas, Illinois).
  Do **not** invent canonical disclosure language. Help them either find
  the opinion themselves and contribute a pack PR, or write their own
  `disclosure_text` in `matter.yml` they can defend.
- The user wants to bill AI-assisted work without disclosure: refuse.
  Point them to `ethics.ai_disclosure_required` in `matter.yml`. The
  skill does not give legal advice on whether their jurisdiction
  requires disclosure — that's their bar admission's homework.
- The CLI errors out on malformed JSONL: the parser already skips bad
  lines. If the entire log is unreadable, ask the user whether they want
  to file an issue at `github.com/sboghossian/billable-time`.

## Web alternative

For lawyers who prefer a browser, the same workflow is at
`<skill-base>/web/index.html`. Single file, no backend. The JSONL never
leaves the page. Open in any browser, upload session logs + matter.yml,
see the rendered diff, download both the `.md` and the `.audit.html`.

## Verifying the self-hash (for the audit-defense scenario)

If, months later, the artifact's authenticity is questioned, the lawyer
can prove it has not been altered:

1. Open the artifact.
2. Find the line containing `sha256:<HEX>` under "Chain of evidence" —
   that's the artifact self-hash.
3. Replace the hex value with the literal sentinel
   `PENDING_SELF_HASH_REPLACE_AT_RENDER`.
4. Run `sha256sum` (or `shasum -a 256`) on the modified file.
5. The output must match the original hex value.

A mismatch means the artifact was edited after generation. Tell the
lawyer this proactively if they ask "how do I prove this hasn't been
tampered with."

## Invariants you must remember during the session

- The CLI runs locally. No network calls. No telemetry.
- The output is the lawyer's responsibility. You are scaffolding the
  draft; the lawyer signs it.
- A route that matches `$HOME` is **always** a smell. Push back every
  time, even if the lawyer is in a hurry.
- A `verified: false` pack with no override is **always** a smell in
  `--strict` mode. Push back.
- The deterministic narrative is intentional. Resist suggestions to
  "improve" it with an LLM.
