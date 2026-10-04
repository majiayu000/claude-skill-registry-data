---
name: agent-portability-matrix
description: Use when a complete research workflow — its instructions, skills, data boundaries, and tool connections — must be assessed for portability across AI agents or environments, so each component is explicitly mapped before migration rather than assumed to transfer.
---

# Agent Portability Matrix

## When to use

Use this skill when a research workflow built in one AI environment — Claude Code, Codex, or any other agent — needs to move to, or be validated against, a second environment: before migration, when evaluating whether an existing skill set will work in a new tool, or when a release checkpoint requires a cross-tool audit of instructions, data boundaries, and permission models. It is not for simply copying a CLAUDE.md file into a new tool and assuming compatibility, and it is not for substituting a portability check for a scientific reproducibility review — those are separate concerns. After a portability audit, hand the verified workflow to cross-agent-second-opinion if a substantive output from the new environment needs independent verification, to mcp-research-stack-triage if MCP server configuration is the migration blocker, to research-lifecycle-pipeline for lifecycle orientation, and to agentic-session-debugger if the destination tooling itself misbehaves during the transition.

## Inputs

- The current project structure: instruction files, persistent directives, and CLAUDE.md or equivalent.
- The installed skill list and any MCP or tool connections active in the source environment.
- Repository layout and data folder boundaries, including which folders are off-limits to AI tools.
- Disclosure templates naming the source environment and contribution level.
- The target agent environment and any known differences in its permission or memory model.
- Sensitive-data boundaries that must be re-verified rather than assumed to transfer.

## Workflow

1. Extract every component of the current workflow: persistent instructions, archived sessions, data folders, installed skills, tool connections, and disclosure statements.
2. For each component, determine whether the destination environment has a direct equivalent, an approximate one requiring adaptation, or no equivalent at all.
3. Re-scope sensitive data folders explicitly for the target tool — do not inherit the source tool's access rules without a fresh check.
4. Audit each installed skill for format compatibility with the destination environment and flag any that require rewriting.
5. List the health tests the target environment must pass before work begins: file read, file write, diff, command execution, and permission scope.
6. Update disclosure statements to reflect the new tool name, model, and contribution level.
7. Deliver a portability decision for each component: portable as-is, requires adaptation, or must not transfer, with a brief reason for each.

## Output

Return:

- A portability matrix table with one row per workflow component and columns for source status, destination equivalent, and decision.
- A list of instructions that transfer directly.
- A list of instructions that require rewriting, with the rewrite scope noted.
- Sensitive data areas that must not transfer and the reason.
- A per-tool capability and skill-support comparison: for each installed skill or tool connection in the source environment, whether the destination environment supports it natively, requires a substitute, or has no equivalent.
- A health-test checklist for the destination environment before substantive work begins.
- A disclosure update note listing the tool names and contribution levels to replace.
- What to record at session end: the output file path, any components whose portability decision is still pending human review, and the handoff to cross-agent-second-opinion if the migrated environment's first outputs need verification.

## Verification

- Every workflow component appears in the matrix with an explicit decision — none are silently skipped.
- Sensitive data boundaries were re-checked against the destination tool's permission model, not assumed to carry over.
- Health tests for the target environment are listed before any substantive work is delegated to it.
- Disclosure statements name the destination tool correctly.
- Before closing: the human researcher has confirmed the portability decisions for every component marked "requires adaptation" or "must not transfer," and no sensitive data has been sent to the new environment before its boundaries were re-established.

## Safety

Changing tools does not reset working discipline — every discipline element must be verified in the new environment before it is trusted. The destination agent is not a copy of the source agent; equivalent functions must be tested separately. Two environments agreeing on a portability decision is not evidence the destination environment is correctly configured. Sensitive data, raw interview transcripts, and student-identifying material pass through sensitive-data-anonymization-gate before any AI tool sees them, including the destination agent. Keep AI contribution visible: record the migration stage, the source and destination models, the contribution level, and the human review step.

## Example prompt

"Bu Claude Code projesini başka bir ajan ortamına taşımak istiyorum. Talimat, skill, veri sınırı, izin modeli, MCP bağlantıları, repo yapısı ve beyan açısından taşınabilirlik matrisi hazırla."

Expected smoke output:

- A portability matrix with one row per workflow component and a portable / adapt / do-not-transfer decision for each.
- A health-test checklist for the destination environment covering file read, write, diff, and permission scope.
- A disclosure update note listing the tool names and contribution levels to replace in existing disclosure statements.

## Türkçe kullanım notu

Bu beceri, bir yapay zekâ ortamında kurulmuş çalışma düzenini başka bir araç ya da ajana taşımadan önce her bileşeni tek tek denetler. Kalıcı talimatlar, veri klasörleri, skill listesi, araç bağlantıları ve beyan şablonları kaynak ortamdaki haliyle değil, hedef ortamda gerçekten çalışıp çalışmadığı sorusuyla ele alınır. Araç değişimi disiplini sıfırlamaz ama her disiplin öğesinin yeni ortamda yeniden doğrulanması gerekir. Hassas veriler, ham mülakat dökümleri ve kimlik içeren materyaller hedef araca girmeden önce sensitive-data-anonymization-gate kapısından geçirilerek anonimleştirme sürecinden geçirilir. İki ortamın taşınabilirlik kararında mutabık kalması, hedef ortamın doğru yapılandırıldığının kanıtı değildir — ortak hata her zaman mümkündür. Taşınabilirlik kararı insan araştırmacıya aittir — beceri karar taslağı üretir, uyumu garanti etmez. Büyük uyuşmazlıklar ya da yeni ortamın ilk çıktılarına güvensizlik durumunda cross-agent-second-opinion'a devredin, araç yapılandırması sorun yaratıyorsa mcp-research-stack-triage'a başvurun.
