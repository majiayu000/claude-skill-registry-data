---
name: repro-developer
description: Build a developer reproduction bundle for agent-review failures, missed-plan retrospectives, Claude/Codex transcript comparisons, or cases where Anthropic/OpenAI engineers need raw conversation JSONL, subagent state, repo evidence, hashes, and a concise replay guide.
---

# Repro Developer

Use this skill when a user wants a reproducible artifact bundle for an agent failure or cross-agent comparison, especially when raw Claude/Codex conversations, subagent transcripts, repo commits, and local state are needed.

## Workflow

1. Identify the incident and claim.
   - State the exact failure mode in one sentence.
   - Separate raw evidence from interpretation.
   - Prefer full transcript/session files over excerpts.

2. Collect artifacts with `scripts/collect_repro.py`.
   - Include Claude parent sessions and their session directories when present.
   - Include subagent JSONL/meta files and workflow journals.
   - Include Codex parent/subagent sessions that caught or analyzed the miss.
   - Include repo evidence files, bead snapshots, git status/log, and command/skill definitions.
   - Produce hashes and a manifest so a developer can verify integrity.

3. Write a replay guide.
   - Explain chronology: initial workflow, missed issue, later catching workflow, retrospective/fix.
   - Name the concrete files to inspect first.
   - Include exact local paths and, when available, GitHub commit URLs.
   - Mark any missing/private artifacts honestly.

4. Package, do not commit large raw transcripts to an ordinary repo by default.
   - Default output belongs under `/tmp/repro-developer-*`.
   - If long-term sharing is needed in git, publish only gitleaks-clean sanitized archives and encrypted raw archives through Git LFS.
   - Do not paste large transcript contents into prompts or PR bodies.

5. Check for sensitive material before sharing externally.
   - Do not delete raw files from the bundle, but add `SENSITIVE_REVIEW.md` with findings.
   - Flag credentials, private repo names, personal email, tokens, and sealed holdout paths.
   - For holdout/evaluator content, include path and hash metadata only unless the user explicitly authorizes sharing the sealed material.
   - Treat `gitleaks detect --no-git` on the sanitized bundle as the required pass/fail gate.

6. For git-native handoff, produce two LFS artifacts.
   - Sanitized archive: redacted, gitleaks-clean, suitable for normal repo access.
   - Exact raw archive: encrypted `.gpg` file, suitable for Git LFS transport only; passphrase stays out of git and is shared out of band.
   - Never commit the raw plaintext archive or the passphrase file.

## Commands

For the July 6-7, 2026 Claude/fable vs Codex plan-miss incident, the committed artifact is:

```text
artifacts/repro-developer/claude-fable-adversarial-review-codex-plan-miss/
```

It contains a sanitized LFS archive and an encrypted exact raw LFS archive. Use the artifact README first for replay.

Create a bundle:

```bash
python3 ~/.claude/skills/repro-developer/scripts/collect_repro.py \
  --repo /home/jleechan/projects/dark-factory \
  --incident claude-adversarial-review-missed-plan-flaws \
  --out /tmp \
  --claude-session-dir /home/jleechan/.claude/projects/-home-jleechan-projects-dark-factory/61098aae-66af-474b-a488-1a47f9e8b66d \
  --codex-session /path/to/codex-parent.jsonl \
  --codex-session /path/to/codex-subagent.jsonl \
  --repo-file docs/factory-goal-gap-review-2026-07-06.md \
  --repo-file docs/adversarial-review-miss-retrospective-2026-07-06.md
```

Create git/LFS-ready artifacts:

```bash
python3 ~/.claude/skills/repro-developer/scripts/collect_repro.py \
  --repo /home/jleechan/projects/dark-factory \
  --incident claude-adversarial-review-missed-plan-flaws \
  --out /tmp \
  --sanitize \
  --require-gitleaks-clean \
  --encrypt-raw \
  --publish-dir artifacts/repro-developer/claude-adversarial-review-missed-plan-flaws \
  ...

git lfs track "artifacts/repro-developer/**"
git add .gitattributes artifacts/repro-developer/claude-adversarial-review-missed-plan-flaws
```

Exact command used for the committed incident:

```bash
python3 .claude/skills/repro-developer/scripts/collect_repro.py \
  --repo /home/jleechan/projects/dark-factory \
  --incident claude-fable-adversarial-review-codex-plan-miss \
  --out /tmp \
  --claim "Claude fable ran a 53-agent adversarial review that confirmed current-state findings but missed plan-level hazards; a later Codex review with three subagents caught ordering, watchdog-metric, canary-overclaim, and self-reference issues already latent in the prior context." \
  --claude-session /home/jleechan/.claude/projects/-home-jleechan-projects-dark-factory/61098aae-66af-474b-a488-1a47f9e8b66d.jsonl \
  --claude-session-dir /home/jleechan/.claude/projects/-home-jleechan-projects-dark-factory/61098aae-66af-474b-a488-1a47f9e8b66d \
  --codex-session /home/jleechan/.codex/sessions/2026/07/06/rollout-2026-07-06T20-38-21-019f3aa7-c615-74a0-8d41-d643dd48a804.jsonl \
  --codex-session /home/jleechan/.codex/sessions/2026/07/06/rollout-2026-07-06T20-58-08-019f3ab9-e056-7540-ba77-72d4712ad4ba.jsonl \
  --codex-session /home/jleechan/.codex/sessions/2026/07/06/rollout-2026-07-06T20-58-14-019f3ab9-f9b6-7852-99e0-d2eba90a498d.jsonl \
  --codex-session /home/jleechan/.codex/sessions/2026/07/06/rollout-2026-07-06T20-58-18-019f3aba-09dd-72b2-b064-c55a372397dc.jsonl \
  --repo-file docs/factory-goal-gap-review-2026-07-06.md \
  --repo-file docs/adversarial-review-miss-retrospective-2026-07-06.md \
  --repo-file docs/setup-agent-hooks-review-2026-07-06.md \
  --repo-file roadmap/nextsteps-2026-07-06-gap-review.md \
  --bead jleechan-niq \
  --bead jleechan-ron \
  --bead jleechan-qdw \
  --bead jleechan-1m4 \
  --bead jleechan-gib \
  --sanitize \
  --require-gitleaks-clean \
  --encrypt-raw \
  --publish-dir artifacts/repro-developer/claude-fable-adversarial-review-codex-plan-miss
```

The script writes:

- `manifest.json` with source paths, sizes, hashes, git metadata, and generated files.
- `REPLAY.md` with a developer-oriented reading order.
- `raw/claude/` and `raw/codex/` with transcripts and subagent state.
- `repo/` with selected source documents and command outputs.
- `checksums.sha256`.
- `<incident>.tar.zst` when `zstd` exists, otherwise `<incident>.tar.gz`.
- With `--sanitize`, a sibling sanitized bundle plus `<incident>-sanitized.tar.*`.
- With `--encrypt-raw`, an encrypted raw archive and a local passphrase file that must not be committed.

## Quality Bar

A bundle is complete only if it contains:

- The initial agent workflow that produced the missed plan or claim.
- The later review that caught the issue.
- Raw subagent state, not just summaries.
- The repo artifacts that show the missed facts were already present.
- A manifest with hashes for every copied file.
- A replay guide that can be followed without needing this chat.
- For git handoff: a sanitized archive that passes gitleaks and an encrypted exact archive whose passphrase is not in git.

If any of those are unavailable, mark the bundle `PARTIAL` in `REPLAY.md` and list the missing evidence.
