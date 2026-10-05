---
name: relay-context
description: Turn the latest relevant topic segment into a copyable, self-contained prompt for another agent or conversation. Use when the user invokes `$relay-context`, asks to turn the current discussion into a prompt, explicitly asks to package the current issue as a prompt for another agent to implement or review, or wants to move a focused task across conversations without creating a full-session handoff document. Do not use for ordinary delegation requests that ask Codex to start or message another agent directly.
---

# Relay Context

Act as a lightweight context-to-prompt relay. Convert the latest relevant topic segment into one prompt the recipient can use directly. Use only conversation context already available to you. Do not summarize the entire conversation by default, read transcripts, inspect files or repositories, perform the underlying task, call tools, operate the clipboard, or create a handoff file.

## Determine the recipient and purpose

1. Honor any recipient explicitly named by the user. Interpret `main` as the Codex main conversation and `side` as the Codex sidebar conversation.
2. For a bare invocation in Codex, relay to the main conversation when the current conversation is clearly a sidebar, and to the sidebar when the current conversation is clearly the main conversation.
3. Otherwise infer the recipient and whether the prompt is for implementation, analysis, or review from the user's latest wording and discussion goal.
4. Only when the recipient remains genuinely ambiguous, output only this clarification question as plain text: `Which conversation or agent should receive this prompt?` Wait for the answer before generating the prompt.

Do not require arguments for routine use.

## Select the topic segment

Use semantic relevance rather than a fixed number of turns:

1. Use the topic or range explicitly specified by the user, when present.
2. Otherwise identify the newest coherent unresolved topic segment.
3. Scan backward through the available conversation and collect only details needed to understand or act on that topic.
4. Stop at unrelated topics, resolved or superseded older tasks, repetitive process discussion, and details the recipient can reconstruct independently.
5. Include earlier information when the current topic depends on it, even if it is not in the immediately preceding turn.

Assume the recipient cannot see the source conversation. Carry conversational intent, decisions, constraints, evidence, and other context that affects the next step and cannot be reconstructed independently. When a workspace or artifact is explicitly known to be available to the recipient, reference the known item instead of reproducing content the recipient can recover from it.

## Preserve signal

- State the target outcome and why the handoff is needed.
- Preserve user-confirmed decisions, necessary rationale, constraints, unresolved questions, and known evidence.
- Distinguish confirmed decisions from unconfirmed assistant suggestions.
- Include only known project, file, artifact, or validation details.
- Remove repetition, abandoned exploration, tool-call history, and unrelated background.
- Preserve a failed approach and its reason only when omitting it could cause the recipient to repeat a significant mistake.
- Redact secrets, credentials, tokens, and unnecessary personal information. Refer to sensitive values generically when their existence matters.
- Do not invent paths, repository state, approvals, evidence, capabilities, or decisions.

## Shape the recipient prompt

For implementation, include only supported details needed to execute and verify the change, such as the outcome, problem, confirmed decisions, requirements, constraints, deliverables, relevant artifacts, and validation criteria.

For analysis or review, include only supported details needed to examine the issue independently, such as the core question, background, current conclusion or dispute, scope, evidence, uncertainties, and desired response format. Require read-only analysis, candid treatment of counterexamples and invalid assumptions, and conclusions without modifications to files, Git, permissions, or external state.

Do not force a fixed template or add empty sections. Make the result concise but sufficient for the recipient to proceed without the source conversation.

## Output constraints

- Apply these constraints after determining the recipient; the clarification question above is the sole exception.
- Output exactly one copyable fenced code block.
- Use a fence longer than any consecutive run of backticks contained in the prompt so embedded code, logs, or Markdown cannot close the outer block.
- Put only the recipient prompt inside the code block.
- Add nothing before or after the code block. Put every detail the recipient needs inside the prompt itself.
