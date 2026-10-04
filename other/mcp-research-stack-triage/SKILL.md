---
name: mcp-research-stack-triage
description: Use when choosing or configuring MCP servers for research work, when a literature, reference manager, or scholarly search server needs a trust check before installation, or when an existing research tool stack needs a data flow and permission audit.
---

# MCP Research Stack Triage

## When to use

Use this skill when Model Context Protocol servers are entering a research workflow and the question is which ones to trust, with what permissions, and with what data. It applies before installation, and again whenever a server updates or a new category of data, such as participant material, enters the workflow. It is not for switching the agent runtime itself or comparing agent environments across projects; for that use agent-portability-matrix, and when a second opinion on a server trust decision is needed, cross-agent-second-opinion provides an independent review lane.

## Inputs

- The research tasks that lack tooling, stated as tasks rather than product names.
- Candidate servers, with their publisher and source.
- The data constraints that bind the work: consent scope, KVKK and GDPR posture, institutional policy.
- The existing MCP configuration, when one exists.

## Workflow

1. Start from the task list. A server earns a place by covering a lifecycle gap, and a server without a task is surface area without a purpose.
2. For each candidate, answer four questions in writing: who publishes it, what data leaves the machine, where that data goes, and what authentication it requires.
3. Prefer a layered route for literature access. Open lanes such as public metadata APIs come first, and authenticated lanes engage only when the open lane fails. Credentials stay in environment stores on the user's side.
4. Configure minimal permissions: only the tools the named tasks need, nothing granted because it might be useful later.
5. Probe each server with a known-answer query before trusting it, such as a DOI whose metadata the user already knows. A server that fails its probe is not in the stack.
6. Record the stack: server, version, scope, the four data flow answers, and the probe result.
7. Re-triage on change. A server update, a new data category, or a new institutional rule reopens the file.

## Output

Return:

- The task-to-server map with the gap each server covers.
- The four data flow answers per server.
- The minimal permission configuration.
- Probe queries and their results.
- The stack record, ready for the project's documentation.
- What to record at session end: the final stack record with probe results, any server excluded and the reason, and the open permission questions awaiting institutional confirmation.

## Verification

- Every server in the final stack has written answers to all four data flow questions.
- Every server passed a known-answer probe in the current session, and the probe is recorded.
- Permissions match the named tasks, with no speculative grants.
- Participant or otherwise sensitive data is routed only to servers explicitly cleared for it, and that clearance is written down.
- Before closing: the stack record is saved to the project documentation folder, and any server whose clearance remains uncertain is flagged for human decision before the next data-touching session.

## Safety

Credentials never appear in configuration files, prompts, or logs, and environment stores hold them on the user's side. Treat server outputs as claims that still need verification through apa-doi-verifier and the source passport, since a search server's confidence is not evidence. When in doubt about a server's data handling, the sensitive data stays out.

## Example prompt

"Literatür taraması için iki MCP sunucusu kurmayı düşünüyorum, hangisine ne izin vereceğime ve neye güveneceğime birlikte karar verelim."

Expected smoke output:

- A task-to-server map with the gap each candidate covers.
- The four data flow questions answered per candidate.
- A probe plan with a known-answer query and a minimal permission proposal.

## Türkçe kullanım notu

Bu beceri, araştırma iş akışına girecek MCP sunucularını güven süzgecinden geçirir. Her aday için dört soru yazılı yanıtlanır, yayıncısı kim, makineden hangi veri çıkıyor, nereye gidiyor, hangi kimlik doğrulamayı istiyor. Açık erişim katmanı önce denenir, kimlikli katman ancak açık katman yetmezse devreye girer ve kimlik bilgileri her zaman sizde kalır. Kurulumdan önce bilinen cevaplı bir sorgu ile sunucu sınanır, sınavı geçemeyen sunucu yığına girmez. Bir sunucunun izinleri ya da veri akışı değiştiğinde yığın kaydı yeniden gözden geçirilir — ilk triage onayı kalıcı değildir.
