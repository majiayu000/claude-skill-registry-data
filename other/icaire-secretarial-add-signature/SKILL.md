---
name: icaire-secretarial-add-signature
description: Insert an approved ICAIRE signature asset into Word or PowerPoint documents. Use when the user asks to add a signature block or selected signer image to a document or deck.
---

# ICAIRE Secretarial Add Signature

Insert an approved signature image into a user-supplied Word or PowerPoint
file while keeping authorization, asset storage, and government-machine
constraints explicit.

## Contract

- Confirm the document type, signer, signature asset location, target
  placement, and whether the file may be edited on this machine.
- Supported signer choices for the first version are Abdulaziz, Dr. Majid, and
  ICAIRE only when the user supplies or identifies an approved local asset.
- Do not store signature images, credentials, or approval-sensitive assets in
  the ICAIRE brain by default.
- Do not guess that a signature is authorized. Treat the user's signer choice
  and supplied asset as the only authorization signal available to the agent.
- If the source document must stay on a government machine where Codex cannot
  run, prepare exact insertion instructions or a placeholder version for manual
  completion by the requesting teammate.
- Return an edited copy when file editing is allowed, and state where the
  signature was inserted.

## Workflow

1. Confirm the request.
   - Identify the signer, file type, file path, target page or slide, and
     desired placement.
   - Ask for the signature asset path if it is not already supplied.
   - Confirm whether the document may be edited locally.
2. Inspect the file.
   - For Word documents, inspect relevant sections, paragraphs, tables, and
     signature blocks.
   - For PowerPoint files, inspect target slides and placeholders.
   - Preserve existing content, formatting intent, page order, slide order, and
     metadata where practical.
3. Insert or prepare.
   - Insert the approved image into the specified location when the file can be
     edited locally.
   - Use a clear placeholder and manual instructions when the final operation
     must happen on a government machine.
4. Verify the result.
   - Re-open or render the edited file when possible.
   - Check that the signature is visible, not stretched, not covering text, and
     placed near the intended signature block.
   - Save the output as a new file rather than silently overwriting the source
     unless the user explicitly asks for in-place editing.

## Output

Default to this structure:

- `Signer`: selected signer and asset source.
- `Document`: input file and output file.
- `Placement`: page, slide, section, or signature block used.
- `Result`: edited file or manual insertion instructions.
- `Verification`: what was checked visually or structurally.
- `Constraints`: any government-machine, authorization, or asset-storage limits.

## Guardrails

- Do not create, modify, or store a signature asset unless explicitly asked.
- Do not upload signature assets into ICAIRE brain pages or raw files.
- Do not imply that the agent approved the signature or the document.
- Do not sign a document without a user-supplied approved asset.
- Do not alter contract, policy, financial, or approval language while inserting
  a signature.
- Do not claim completion if the final step must happen on a government machine;
  report the remaining human step clearly.
