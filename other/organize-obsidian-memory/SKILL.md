---
name: organize-obsidian-memory
description: "Turn Markdown notes, chat exports, research fragments, and ideas in an Obsidian vault inbox into source-linked candidate memory notes for human review. Use when Codex needs to organize an Obsidian inbox, deduplicate candidate memories, create candidate notes, or build and validate a candidate-only memory index. Never use to silently import private data, alter raw sources, or promote a candidate to active memory."
---

# Organize Obsidian Memory

Convert named inbox material into a small set of source-linked candidate notes.
Preserve evidence, uncertainty, and the existing vault structure.

## Resolve the vault contract

1. Use only the vault path named by the user. Do not assume a personal default
   path.
2. Before writing, read the vault's own rules and templates when present:
   80-系统/AI自动整理规则.md, 80-系统/记忆库规范.md,
   80-系统/记忆库去重与审核规则.md, and
   90-模板/AI候选记忆模板.md.
3. Treat 00-收集箱/AI待整理/ as raw input and
   00-收集箱/待确认/AI整理/ as generated output.
4. When these policies are absent, read
   references/vault-contract.md and either use its conservative contract or
   ask the user before creating an incompatible structure.

## Organize a batch

1. List unprocessed source files in the named raw-input directory. Ignore
   README files and unrelated folders.
2. Search existing candidate and active notes for the same claim, project,
   person, decision, or source link before creating a note.
3. Extract only information likely to affect a future decision or action.
   Exclude ordinary conversation filler.
4. Create one Markdown candidate per core memory using the vault template.
   Keep status as candidate and confidence as needs_review unless the user
   explicitly authorizes another state.
5. Link every claim to one or more source files. Separate direct evidence from
   inference, and state uncertainty plainly.
6. Add new source evidence to an existing candidate when the claim matches.
   Do not rewrite active notes during inbox organization.

## Protect user state

- Do not move, rename, delete, or rewrite raw source files.
- Do not read outside the named inbox or vault policy files without user
  direction.
- Do not store credentials, identity documents, payment data, private keys,
  cookies, or unnecessary private-chat text.
- Do not promote candidate memories to active, even if a summary sounds
  convincing.
- Keep conflicting evidence visible instead of choosing one version silently.

## Verify and report

1. Run the vault's index builder and validator when they exist. Report their
   exact result.
2. If the scripts are absent or fail, say so. Do not claim the vault was
   validated.
3. Report created candidates, evidence added to existing candidates, duplicates
   flagged, unresolved uncertainty, and files left unchanged.

For a fully synthetic reference vault, see
../../examples/obsidian-evidence-memory-demo/.
