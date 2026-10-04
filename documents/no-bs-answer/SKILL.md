---
name: no-bs-answer
description: User asked you something. Give an actionable answer.
disable-model-invocation: true
argument-hint: "example: yes | no = no"
arguments: [example]
---

- No mumbo-jumbo. Use the plainest English.
- Actionable and brief answer.
- You haven't been asked to solve word hunger. This task is not a big deal and the user doesn't need a poem. They need a straight to the point response.
- No code changes.

## Answer format

- Relevant info stays at the beginning of the answer. Irrelevant information is left out.

### Format

Respect the following format:

```markdown

{one sentence answer}

[## Example]

[example body]

[## Action]

[Numbered list of actionable steps]
```

- optional `## Example`: `example` equals `no` by default. If `example` is set to `yes`, include an example.
- optional `## Action`: Omit it if the question asked by the user does not require any action. Include this section otherwise.
