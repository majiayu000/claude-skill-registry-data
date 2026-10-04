---
name: clarify-first
description: Resolve unclear instructions before acting. Ask focused clarification questions until every ambiguity that could change scope, behavior, safety, compatibility, data sources, API contracts, or acceptance criteria is settled. Use whenever a request starts with `cf:` or `cf :`, or when the user explicitly requests clarify-first, such as `$clarify-first` in Codex or `/clarify-first` in Claude Code.
---

# Clarify First

Treat the text after `cf:` or `cf :` as the requested task. Do not interpret `cf` as part of the task.

## Workflow

1. Inspect available context and use safe read-only discovery when it can answer a question directly.
2. Identify every unresolved choice that could materially change the result.
3. Ask one to three focused questions. Explain the consequence of each choice when it is not obvious.
4. After every answer, reassess the complete task for remaining or newly introduced ambiguity.
5. Repeat the questions until the task has one clear, internally consistent interpretation.
6. Once clear, briefly state the resolved contract and perform the task without requesting redundant confirmation.

Do not write files, mutate external state, or begin implementation while material ambiguity remains. Read-only inspection is allowed when it stays within the requested scope.

## What To Clarify

Clarify choices involving:

- included and excluded scope;
- source of truth and data boundaries;
- expected behavior, output, and success criteria;
- destructive actions, external side effects, and rollback expectations;
- compatibility, API contracts, migrations, and deployment targets;
- conflicts between the request and existing constraints.

Do not ask about details already established by the conversation, discoverable from the scoped workspace, or safely governed by existing project conventions. Do not turn trivial implementation choices into questions.

If the user explicitly delegates a choice with phrases such as "알아서 해" or "use your judgment," treat that choice as resolved. If the user declines to answer, proceed only when a safe reversible assumption exists; state that assumption before acting. Otherwise, explain why the task remains blocked.

## Question Style

- Ask concrete questions, not "Can you clarify?"
- Prefer one decisive question at a time when later questions depend on its answer.
- Group independent questions only when answering them together saves a round trip.
- Offer mutually exclusive options when the real choices are known.
- Keep asking while a material ambiguity remains, even if an earlier answer resolved only part of it.

Example invocation:

```text
cf: 사용자 데이터를 정리하는 배치를 만들어줘
```

Example response direction:

```text
삭제 대상은 원본 DB row인가요, 파생 검색 문서인가요? 이 선택에 따라 복구 가능성과 실행 위치가 달라집니다.
```
