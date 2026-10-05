---
name: ceo-document-review
description: Use for requests to inspect, summarize, compare, comment on, or approve DingTalk or Lark documents, files, images, and tables. Use ceo-mail-review for the enclosing mail thread and ceo-meeting-work for meeting records. Load the operation Skill matching the actual material type before reading or editing it.
metadata:
  managed_by: ceo-agent-service
  version: 1
---

# CEO Document Review

Identify the material type, read the current version, and keep review output tied to evidence in that material.

Load the operation Skill that matches the actual material type before reading, commenting, or delivering a review. Use only the capability and command shape documented by that Skill.

## Material Reads

| Material | Operation Skill | Required read |
| --- | --- | --- |
| DingTalk document | `dingtalk-doc` | read current content |
| DingTalk AI table | `dingtalk-aitable` | never use document read |
| ordinary file | `matching drive Skill` | use the supplied exact command |
| image | none for attached input | inspect the image before conclusions |
| Lark document | `lark-doc` | read current content |
| Lark table | `lark-base` | read current table data |
| Lark file | `lark-drive` | use the supplied exact command |

For DingTalk stored files, the matching drive Skill is `dingtalk-drive`. Load `dingtalk-chat` before delivering a DingTalk chat response. For another supported source, load its corresponding document, table, drive, and source-conversation Skills rather than substituting a DingTalk operation.

## Review Workflow

1. Determine the material's real type from its reference and metadata, then load the matching operation Skill. Do not treat a table as a document or choose a read merely because two references look similar.
2. The agent chooses and performs every content read. The service exposes references and exact read commands but does not interpret business content. For an ordinary file, use the supplied exact download/read command and inspect the downloaded content.
3. For an attached image, inspect the image content already present in the current Agent input before drawing conclusions. If the input instead exposes an exact supplied local material reference or operation, use that exact reference or operation to inspect the image. Do not load image-generation and do not guess an image-reading Skill. A filename, caption, attachment card, or prior description is not image evidence.
4. Reread the current material when the sender says it changed, was supplemented, or received new comments. Do not reuse a conclusion from an older version.
5. Review readable material directly. Do not ask the sender to paste content that the agent can read. Tie conclusions, requested changes, risks, and next steps to the content actually inspected.
6. If decisive material cannot be read because the dependency, authentication, permission, command, or content is unavailable, return an explicit dependency failure. Do not infer or invent the missing content.
7. Deliver comments in the material when the loaded operation Skill supports comments; otherwise deliver the review in the source conversation after loading that conversation's operation Skill.

Consumer A performs only reads and proposes any comment or response. Audit B independently loads the same business and operation Skills, validates the exact path and SHA receipts, rereads current material when required, and alone executes approved effects. The service validates and records operations but never decides what the material means.
