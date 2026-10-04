---
name: code-wiki-ru
description: "Builds and validates Russian Obsidian repository wikis, architecture docs, and code/docs/ADR drift reports."
---

# Code Wiki RU

Use this skill to create, refresh, validate, and safely apply Russian Obsidian-compatible code wikis under `docs/wiki` or a user-specified wiki path.

For a read-only question about an existing wiki or ADR, use `wiki-query` without
running the indexing, planning, or drafting workflow below.

Default variables used below:

```bash
SKILL_DIR="${SKILL_DIR:-$HOME/.codex/skills/code-wiki-ru}"
REPO_ROOT="${REPO_ROOT:-$(pwd)}"
WIKI_PATH="${WIKI_PATH:-docs/wiki}"
META_PATH="${META_PATH:-docs/wiki/_meta}"
```

## Safety

- Do not read, print, summarize, store, or commit secrets.
- Treat `.env`, `.env.*`, private keys, certificates, credential stores, tokens, cookies, auth files, production dumps, and credential-bearing logs as redacted paths.
- Keep code identifiers, paths, commands, package names, API names, config keys, schema names, and ADR titles exactly as written.
- Prefer deterministic scripts before model analysis.
- DeepSeek output is draft material only. Do not apply it until it is reviewed and validated by the host agent.
- Do not ask DeepSeek or OpenCode to modify files, stage files, commit files, run deployment commands, or execute destructive commands.
- Preserve user changes. Do not revert unrelated work in the repository.

## Repository Inspection

1. Identify `REPO_ROOT` from the user request or current working directory.
2. Read repository-local instructions before generating wiki content, especially `AGENTS.md`, `README.md`, ADR indexes, docs indexes, and architecture notes when present.
3. Inspect dependency/configuration files relevant to the repository type before writing architecture claims.
4. Identify existing wiki location. Use `docs/wiki` by default unless the user or repository config clearly points elsewhere.
5. Identify source documents and ADRs, but treat code as authoritative for runtime behavior.

## Init/Index

Run the indexer before planning or drafting. It initializes wiki metadata and records bounded, non-secret source inventory.

```bash
python3 "$SKILL_DIR/scripts/build_repo_index.py" --repo "$REPO_ROOT" --wiki-path "${WIKI_PATH:-docs/wiki}" --meta-path "${META_PATH:-docs/wiki/_meta}"
```

Expected output is metadata under `${META_PATH:-docs/wiki/_meta}`. If the command fails, fix the invocation or report the failure before proceeding.

## Plan

Run the planner after the index exists. It creates update chunks for bounded analysis.

```bash
python3 "$SKILL_DIR/scripts/plan_wiki_update.py" --repo "$REPO_ROOT" --wiki-path "${WIKI_PATH:-docs/wiki}" --meta-path "${META_PATH:-docs/wiki/_meta}"
```

Use the generated plan to choose the smallest chunk set that satisfies the request. Keep unrelated chunks out of scope.

## Analyze

- Read `references/wiki-taxonomy.md` before designing page structure.
- Read `references/drift-policy.md` before classifying mismatches.
- Prefer verified source references over broad summaries.
- Use Russian prose for wiki pages.
- Use Obsidian `[[wiki-links]]` for internal links and relative Markdown links for source docs and ADRs.
- Use Mermaid only when the available source context supports the diagram.
- Keep pages focused: one subsystem, component, flow, API surface, data concept, integration, operation, decision, or glossary topic per page.

## Draft

For each selected `CHUNK_ID`, render a context pack:

```bash
python3 "$SKILL_DIR/scripts/render_context_pack.py" --repo "$REPO_ROOT" --wiki-path "${WIKI_PATH:-docs/wiki}" --meta-path "${META_PATH:-docs/wiki/_meta}" --chunk-id "$CHUNK_ID" --output "$CONTEXT_PACK"
```

Before invoking OpenCode, read:

- `references/opencode-deepseek.md`
- `references/prompt-contracts.md`

Dispatch only through the verified local `tests-docs` worker route described in
the reference. Send the explicit export-authorized context through bounded
stdin or a supported private file, never a large prompt argument. Keep the
worker outside the repository with no source editing, shell, inherited MCP or
parent auth access. Select provider/model from private runtime configuration;
report BLOCKED when that exact route has not been verified. Preserve requested
and observed metadata, checks, and artifacts using `subagent-result-merge`.

Do not ask DeepSeek to apply patches. The parent reviews model-authored drafts
before staging them under `${META_PATH:-docs/wiki/_meta}/drafts/`, validates
them, and owns application to the wiki.

## Drift

Classify drift using `references/drift-policy.md`:

- `code-docs`: docs disagree with verified runtime code.
- `code-adr`: code no longer follows accepted ADR intent.
- `docs-adr`: docs disagree with ADR intent.

Every drift candidate must include:

- drift class
- severity
- source file references
- short evidence summary
- recommended action

If evidence is insufficient, do not invent drift. State that the available context does not confirm a mismatch.

## Validate

Run validation before applying staged pages or reporting completion:

```bash
python3 "$SKILL_DIR/scripts/validate_wiki.py" --repo "$REPO_ROOT" --wiki-path "${WIKI_PATH:-docs/wiki}" --meta-path "${META_PATH:-docs/wiki/_meta}"
```

Validation should check structure, links, required metadata, and staged output consistency. Report exact command output or the failure reason.

## Apply

Apply drafted wiki changes only after the user explicitly asks for application or the current task clearly requires it.

Before applying:

- Review staged drafts in `${META_PATH:-docs/wiki/_meta}/drafts/`.
- Confirm proposed page paths match `references/wiki-taxonomy.md`.
- Confirm drift findings include source references and recommended actions.
- Confirm no secret-bearing content is present.
- Re-run validation after applying.

Do not stage or commit repository changes unless the user explicitly requests it.

## Resume

When resuming an interrupted wiki update:

1. Re-read repository-local instructions.
2. Re-run the index command to refresh metadata.
3. Re-run the plan command and compare the current chunks with any existing drafts.
4. Continue from the smallest unfinished chunk.
5. Validate before applying or reporting completion.

Discard stale drafts only when they are proven obsolete or the user authorizes cleanup.

## References

- `references/wiki-taxonomy.md`: wiki hierarchy, page naming, links, diagrams, and page focus rules.
- `references/drift-policy.md`: source-of-truth order, drift classes, severity levels, and required finding fields.
- `references/opencode-deepseek.md`: safe OpenCode invocation and DeepSeek handling rules.
- `references/prompt-contracts.md`: required Markdown sections and staged-output contract for model drafts.
