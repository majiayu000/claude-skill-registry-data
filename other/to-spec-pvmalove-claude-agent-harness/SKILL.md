---
name: to-spec
description: Turn the current conversation into a spec and publish it to the project issue tracker. No interview, just synthesis of what you've already discussed.
disable-model-invocation: true
---

**Objective:** Synthesize the current conversation context and codebase understanding into a final specification.
**Strict Rule:** Do NOT interview the user or start a new grilling round. If information feels missing, it means the previous grilling was incomplete; synthesize the spec using only the known facts and explicit assumptions.

The issue tracker and triage label vocabulary should have been provided to you. If not, tell the user to run `/setup-matt-pocock-skills`.

## Execution in Two Phases

You must execute this skill in two distinct phases to ensure the user agrees with the testing strategy before you write the final document.

### Phase 1: Exploration & Seam Proposal
1. **Explore the Codebase:** Use the project's domain glossary (`CONTEXT.md`) and respect any ADRs in the touched area.
2. **Define Seams:** Sketch out the seams at which the feature will be tested.
    - Prefer existing seams over new ones.
    - Use the highest seam possible.
    - Ideal state: exactly *one* seam for the whole feature.
3. **STOP AND ASK:** Present your proposed seams and one integration branch name in the form
   `integration/<service-or-team>`. Derive the slug from explicit project/domain language; never
   guess it. Ask the user to approve both. **Do not proceed to Phase 2 until the user confirms.**

### Phase 2: Drafting & Publishing (After User Approval)
1. **Draft the File:** Write the spec using the `<spec-template>` below, at the root of its own folder under `docs/tasks/` — that folder also reserves `tickets/` (one file per child ticket, filled in later by `/to-tickets`) and `artifacts/` (the `/grilling` Live Artifact).
    - *Naming convention:* If the issue ID is known, use it. If not, use a descriptive slug (e.g., `docs/tasks/add-user-auth/add-user-auth.md`) and rename both the folder and file later once the ID is generated — see `docs/agents/artifacts.md` for the full convention, including the epic-folder grouping and the `tickets/`/`artifacts/` subfolders.
    - Take the final Discovery Context file list from that same folder's `artifacts/discovery-context.md` (written by `/grilling`'s Persisted List step); if that file doesn't exist because artifact tracking never ran, take the approved-paths list from the final Trunk summary instead. Append it in the template's final `## Relevant Files (Discovery Context)` section. Preserve every path and any supplied context; do not rediscover or replace that list while drafting.
2. **Publish to Tracker:** Publish the issue using the CLI: `gh issue create --body-file <path>`.
    - **CRITICAL:** Do NOT use an inline `--body` heredoc. Spec bodies contain characters (nested quotes, backticks, etc.) that break heredoc quoting. Always use `--body-file`.
3. **Apply Labels:** This published issue acts as the feature's **epic**. Apply the following labels (see `docs/agents/triage-labels.md` for the full taxonomy):
    - `type::bug` OR `type::feature`
    - `status::specs` (Do NOT use `status::ready` as it requires decomposition first).
    - `task-report::required` (unless told to skip).
    - *Note:* Do NOT create ad-hoc `epic::<slug>` labels. `/to-tickets` will handle linking sub-tasks natively later, as GitHub sub-issues — see `docs/agents/issue-tracker.md#wayfinding-operations` for the mechanism.
4. **Ensure the selected integration branch exists after the epic issue succeeds:**
    - Read `base_branch` from `.harness/project.json` (default `main`). This is the release/base
      branch from which the epic integration branch starts.
    - Fetch the base ref. Create `integration/<service-or-team>` from `origin/<base_branch>` when
      a remote exists, otherwise from the local base branch. Do not switch the current worktree;
      it may contain unrelated changes.
    - If the integration branch already exists locally or remotely, reuse it without resetting,
      force-updating, or deleting it. If publication succeeds but branch creation fails, report
      the partial state and the exact recovery action; do not recreate the epic issue.
    - Push a newly created remote branch with `git push -u origin integration/<service-or-team>`.
      For a local tracker or a repository without a remote, create the local branch and report
      that it was not pushed.

---

<spec-template>

## Problem Statement
The problem that the user is facing, from the user's perspective.

## Solution
The solution to the problem, from the user's perspective.

## User Stories
A LONG, numbered list of user stories covering all aspects of the feature.
Format: `1. As an <actor>, I want a <feature>, so that <benefit>`
*(Example: As a bank customer, I want to see my balance, so that I can make informed spending decisions).*

## Implementation Decisions
A list of modules to build/modify, interface changes, technical clarifications, architectural decisions, schema changes, API contracts, and specific interactions.
- **DO NOT** include specific file paths or generic code snippets (they outdate quickly).
- **Exception:** If a prototype produced a snippet that encodes a decision perfectly (state machine, schema, type shape), inline it and note it came from a prototype. Trim it to the decision-rich parts only.

## Testing Decisions
- Description of what makes a good test here (test external behavior, not implementation details).
- Which modules will be tested.
- Prior art (similar existing tests in the codebase).

## Out of Scope
A strict list of things that will NOT be done. This is your insurance policy against over-engineering. Be explicit about boundaries so future agents do not build more than requested.

## Integration Branch

- Branch: `integration/<service-or-team>`
- Created from: `base_branch` in `.harness/project.json`
- Child issue branches start from this integration branch and open PRs back to it.

## Further Notes
Any remaining context or constraints.

## Relevant Files (Discovery Context)
The final Discovery Context file list captured in the session's `Live Artifact`, or in the final Trunk summary when artifact publishing is unavailable, including each path and any supplied context.

</spec-template>
<!--
## Problem Statement (Постановка проблемы)
Проблема, с которой сталкивается пользователь, с точки зрения пользователя.

## Solution (Решение)
Решение проблемы с точки зрения пользователя.

## User Stories (Пользовательские истории)
ДЛИННЫЙ, пронумерованный список пользовательских историй, охватывающий все аспекты фичи.
Формат: `1. Как <actor>, я хочу <feature>, чтобы <benefit>` (1. Как <субъект>, я хочу <функцию>, чтобы <выгода>)
*(Пример: Как клиент банка, я хочу видеть свой баланс, чтобы принимать обоснованные решения о расходах).*

## Implementation Decisions (Решения по реализации)
Список модулей для создания/изменения, изменения интерфейсов, технические уточнения, архитектурные решения, изменения схемы, контракты API и конкретные взаимодействия.
- **НЕ** включайте конкретные пути к файлам или общие фрагменты кода (они быстро устаревают).
- **Исключение:** Если прототип создал фрагмент, который идеально кодирует решение (конечный автомат, схема, форма типа), встройте его и отметьте, что он взят из прототипа. Обрежьте его только до частей, богатых решениями.

## Testing Decisions (Решения по тестированию)
- Описание того, что делает тест хорошим здесь (тестирование внешнего поведения, а не деталей реализации).
- Какие модули будут тестироваться.
- Предшествующий уровень техники / Prior art (похожие существующие тесты в кодовой базе).

## Out of Scope (Вне рамок)
Строгий список вещей, которые НЕ будут сделаны. Это ваш страховой полис от переусложнения (over-engineering). Четко определите границы, чтобы будущие агенты не создавали больше, чем запрашивалось.

## Integration Branch (Интеграционная ветка)

- Ветка: `integration/<service-or-team>`
- Создана из: `base_branch` в `.harness/project.json`
- Дочерние ветки задач начинаются из этой интеграционной ветки и открывают PR к ней.

## Further Notes (Дополнительные заметки)
Любой оставшийся контекст или ограничения.

</spec-template>
-->