---
name: sflow-upload
description: Attach, inspect, list, or governably detach files, folders, images, PDFs, Figma exports, notes, and HTTPS references for an Epic or Story.
disable-model-invocation: true
argument-hint: "attach <PATH...> [--epic EPIC-ID] | list [OWNER-ID] | view <ID|NAME> [--work-id WORK-ID] | detach <ID|NAME> --reason TEXT [--epic EPIC-ID]"

---

# Upload governed evidence

<!-- sflow-output-contract: canonical-delegation -->
**Output contract:** Run the canonical skill once and preserve its result and handoff; do not repeat its preflight, authoring, or publication.
<!-- sflow-execution-boundary -->
**Boundary:** machine-local; no repository or Story required. Use explicit arguments or SFlow-returned paths; never search `$HOME` or infer a repository.

REV feedback: use `/sf-revision-attachments`; ordinary upload cannot bypass its importer.

Delegate once to `/sf-documents`, mapping `attach` to `upload` and preserving paths, names, owner selectors, and the requested list/view/detach action. That canonical skill owns context resolution, choices, preview, confirmation, mutation, and reporting. Stop when it returns; preserve its result and next action. Do not repeat a preview, ask again for a choice already accepted by the canonical skill, or run a second upload/detach command.
