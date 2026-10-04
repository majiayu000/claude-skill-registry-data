---
name: extract-automation-candidates
description: Mine Claude Code session transcripts, git commit history, and spec or PRD markdown files for recurring or high-cost manual workflows worth turning into a skill, slash command, or standing instruction, then write the real artifact (SKILL.md, command markdown, or an AGENTS.md line) with traceability back to its source. Use when user says "find things worth automating", "extract skills from our sessions", "what should be a command by now", "turn recurring patterns into skills", "audit our commits and conversations for automation opportunities", or "mine our history for repeatable workflows".
metadata:
  author: Ronnasayd Machado - github.com/Ronnasayd
  version: 1.0.0
---

# Extract Automation Candidates

Mines session transcripts, commit history, and formal specs for **recurring or high-cost manual patterns** worth turning into a skill, command, or instruction — then writes the real artifact, not a report about one.

A candidate qualifies only if: it appears **≥2 times across different sources/sessions** (recurrence), OR it appeared once but was an unusually long/painful manual process in a single session (high cost — e.g. 15+ manual steps, repeated trial-and-error, a workaround the user had to re-explain in detail). A single ordinary request is never a candidate.

Each of the 3 mining phases below is independent — run only the phase(s) the user asks for. Phase 4 (classify + write artifact) always runs last, once at least one phase produced candidates.

## Instructions

### Step 1: Mine session transcripts (if requested)

Session transcripts live at `~/.claude/projects/<url-encoded-cwd>/*.jsonl`, one file per session UUID.

1. Read one raw line where `type == "user"` from any `.jsonl` in the target project directory and inspect `message.content` and the `promptSource` field. **Do this every time before running the script** — schema can differ across Claude Code versions, and tool-result/system content is also stored under `role: "user"`, so `promptSource == "typed"` may not still isolate real human input without checking first.
2. Run `scripts/extract_user_prompts.py` against all session files for the project:
   ```
   python3 scripts/extract_user_prompts.py "$HOME/.claude/projects/<project-dir>/*.jsonl" --out /tmp/user_prompts_only.txt
   ```
3. Read the output file in full (paginate if needed) — do not sample. For each prompt, ask: is this a request the user has phrased before (same or near-same intent, different session/wording), or a task that took many manual back-and-forth turns to accomplish?
4. Cluster matches into candidate workflows. For each candidate, record: the recurring request pattern (paraphrase, not verbatim), how many times/sessions it showed up, and the rough sequence of steps that were manually repeated each time.
5. Discard anything that already has a matching skill/command in `agents/skills/` or `agents/commands/` (check first) — the point is to find _gaps_, not re-catalog what already exists.

Expected output: a list of candidate workflows with occurrence count/session refs and a rough step outline.

### Step 2: Mine git commit history (if requested)

1. Dump the full log, bypassing any shell hook or token-saving proxy that might silently truncate `git` output:
   ```
   bash scripts/dump_git_log.sh /tmp/commits_full.txt <repo-path>
   ```
   The script self-verifies commit count vs `===END===` marker count — **do not proceed past a warning without investigating**.
2. Read the dump in full, chronologically (`--reverse`, oldest first).
3. Look specifically for: repeated `fix:` commits addressing the same root cause across time (signals a manual step that keeps getting done wrong or forgotten), commit-body descriptions of a manual multi-step process ("had to manually update X, Y, Z"), and any commit that itself adds a script/tool clearly meant to replace a manual step (signals the pattern was already felt as painful once — check if it's fully automated or still needs a human to invoke it correctly).
4. Cluster into the same candidate list as Step 1, cross-referencing by topic — a transcript candidate and a commit-history candidate about the same workflow are the same candidate with two source tags, not two separate ones.

Expected output: candidate list extended/corroborated with commit evidence (dates, commit hashes as traceability).

### Step 3: Mine formal spec/PRD files (if requested)

1. Locate candidate files: `find <repo-root> -iname "*.md"`, excluding `node_modules`, build/tooling temp dirs, and existing `agents/skills/` or `agents/commands/` content itself.
2. Read every candidate document in full. Look for documented processes, runbooks, or "how to do X" sections written in prose — these are implicit skill/command candidates if they describe a repeatable procedure rather than a one-time decision.
3. Cross-check against Steps 1-2's candidate list: a documented runbook that also shows up as a repeated manual transcript pattern is strong evidence, not a duplicate to discard.

Expected output: candidate list extended with spec-sourced procedures, tagged with source doc path.

### Step 4: Classify and write the artifact

Only run this once at least one phase produced candidates.

1. Read `references/classify-and-write.md` now — it defines the skill/command/instruction decision heuristic, the exact target paths (`<workdir>/agents/skills/<name>/SKILL.md`, `<workdir>/agents/commands/<name>.md`, or an appended line in `AGENTS.md`), and the traceability footer format every written artifact must include.
2. For every surviving candidate (recurrence ≥2 OR high-cost single occurrence — reject and drop anything weaker, do not write an artifact "just in case"), classify it as skill / command / instruction per the heuristic.
3. Write the artifact to its real target path. Do not just describe what the artifact would contain — the file must exist on disk when this step finishes.
4. If a same-named skill/command/instruction already exists, treat this as an update: read it first, merge the new evidence in rather than overwriting blindly, per `references/classify-and-write.md`.

Expected output: one or more real files written under `agents/skills/`, `agents/commands/`, or an instruction line appended to `AGENTS.md`, each with a traceability footer.

## Delivery (all steps)

Keep the chat reply to 1-2 sentences: how many candidates were found, how many were classified as skill/command/instruction, and where each was written. Do not paste full artifact contents into chat — the file itself is the deliverable, point to its path (use SendUserFile only if the user asks to see it rendered).

## Examples

### Example 1: Single-source scan

User says: "olha nossas conversas recentes e vê se tem algo que devia virar um command"
Actions: Step 1 only, then Step 4 filtered to command-type candidates.
Result: zero or more `.md` files written under `agents/commands/`, each traced back to the transcript sessions that justified it.

### Example 2: Full audit

User says: "varre commits, specs e conversas e me diz o que vale virar skill"
Actions: Steps 1 → 2 → 3 → 4 in order.
Result: candidate list built from all three sources, deduplicated by topic, classified, artifacts written to their respective paths.

### Example 3: Nothing qualifies

User says: "tem algo pra automatizar aqui?"
Actions: run requested phases, find only single-occurrence ordinary requests with no evidence of pain or repetition.
Result: report that zero candidates cleared the threshold — do not force a weak candidate into an artifact just to have output.

## Troubleshooting

### Commit/line counts disagree after `dump_git_log.sh`

Cause: a shell hook or CLI proxy rewrote `git` transparently and truncated output. The script invokes `/usr/bin/git` directly to bypass this — double-check no wrapper sits even closer to the binary (`type git`, `alias git`) if the warning persists.

### `promptSource` field absent or all values differ from `"typed"`

Cause: transcript schema changed. Read 3-4 raw `type == "user"` lines across different timestamps and find whichever field currently discriminates real typed input from injected tool-result/system-reminder content, then adjust the filter accordingly.

### Same workflow shows up with conflicting step counts across sources

Do not guess. Use the most detailed/most recent account as the basis for the artifact, but note the discrepancy in the traceability footer rather than silently picking one.
