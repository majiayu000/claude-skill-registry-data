---
name: ask
description: Ask a legal question grounded in the user's GC AI knowledge base, optionally against specific documents. Use for legal research, summarization, or Q&A over the user's own files, playbooks, and skills rather than the model's general knowledge.
---

# Ask GC AI a grounded question

Answer a legal question using the user's GC AI knowledge base so the response is grounded in their own material, not general model knowledge.

## Steps

1. **Bring in any referenced documents first.** If the question is about a specific file the user attached, upload it (`upload_file`, or `start_file_upload` plus `finish_file_upload` for a sandbox file) and poll `get_files({ id })` until `ready`. If the question is about material already in GC AI, locate it with `get_files`, `get_projects`, or `get_playbooks` as needed.

2. **Ask.** Call `ask_gcai` with the question, scoping it to the relevant files or project when there is one. It is a long-running job: poll `ask_gcai_status` until `status` is `succeeded`, `failed`, or `canceled`.

3. **Present the answer.** Return the grounded answer with its citations to the underlying documents. Do not add legal conclusions the source material does not support.

4. **Offer to keep it.** If the user wants a record of the exchange in their GC AI history, call `ask_gcai_save_chat`. Only save when the user asks; it writes to their account.

## Notes

- Prefer grounding over recall. If the knowledge base has nothing relevant, say so plainly instead of answering from general knowledge.
- Complete the whole chain in one turn. Poll jobs yourself; never ask the user to wait.
