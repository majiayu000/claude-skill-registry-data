---
name: integrate-project
description: Audit an existing, already-substantial codebase and fold this harness into it without disrupting what's already there. Use when a repository already has meaningful code, conventions, CI, or other AI-tool configuration and needs the harness (skills, AGENTS.md, discovery links) integrated for the first time. For a brand-new idea, an empty or near-empty repository, or revising an already-harnessed project, use `start-project` instead.
---

# Integrate Project

Fold a portable harness onto a codebase that already exists, without guessing what the project already
knows about itself. Read real files before asking; treat the repository, not the conversation, as the
primary source of truth.

Resolve this skill's real path and verify that the public `agent-harness` root two levels above it
contains `skills/REGISTRY.md` and `harness/bin/harness.py`. This resolution is complete only when both
files exist; otherwise report that the public package is incomplete instead of guessing another
installation.

## Audit

1. **Stack and commands.** Read manifests directly — `package.json` (and its `scripts`), lockfiles,
   `pyproject.toml`/`requirements.txt`, `go.mod`, `Cargo.toml`, `Gemfile`, or equivalent. Derive the
   stack and the real install/run/test/lint/build commands from what is actually configured, not from
   a README claim or the user's memory.
2. **Conventions the manifest doesn't state.** Read CI workflow files (`.github/workflows/*`,
   `.gitlab-ci.yml`, etc.) for the commands CI actually runs — ground truth over documentation, which
   drifts. Read recent branch names (`git branch -a`, `git log --all --oneline -20`) and the remote's
   default branch for `branch_pattern` and `base_branch`. Read the existing test/docs directory layout
   rather than assuming a convention.
3. **Existing AI-tool configuration.** Look for `AGENTS.md`, `CLAUDE.md`, `.cursor/rules`,
   `.github/copilot-instructions.md`, and a `.claude/` directory not managed by this harness (no
   `.harness/harness.lock` yet). Read what is there. An existing instruction that conflicts with this
   harness's conventions is a finding to reconcile with the owner, not a file to overwrite silently.
4. **Domain.** Classify the project's primary work — software, content, research/knowledge,
   operations, personal, or another explicit domain — from what the repository actually contains.
5. **What files can't answer.** Definition of Done, delivery/merge policy, and forbidden actions
   rarely live in the repository. Note these as open questions instead of guessing them from stack
   conventions.
6. **Decision-history signal.** Check whether the repository already has an ADR or decision-record
   convention (`docs/adr/`, or another location an existing doc points to) and get a rough sense of
   its merge/session history (`gh pr list --state merged` / `glab mr list --merged`, `git log --all
   --oneline | wc -l`). This is signal for the optional Reconstruct decision history phase below, not
   the investigation itself — keep it to a glance.

Audit is read-only. Do not write, install, or select a capability during this phase.

## Present and confirm

Summarise findings compactly: stack, real commands, branch/CI convention, detected domain, any
existing AI-tool configuration and where it conflicts with this harness, and the recommended
capability. Ask only what Audit left genuinely open — do not re-ask what a file already answered.
Do not proceed until the owner confirms this manifest.

When step 6 found meaningful history and no existing decision-record convention, separately offer
the optional Reconstruct decision history phase below — name it as a slow investigation independent
of installing the harness, so the owner can decline lightly. A yes there does not change this
manifest; a no does not block Install.

## Install

Continue with `global-skills/start-project/SKILL.md`'s Assemble section from step 2 onward, using
this audit in place of its step 1 (which this skill's Audit phase already covers, in more depth), and
its Finish section unchanged. A repository reaching this skill has no existing harness by definition,
so Assemble step 5 (`harness init`) applies, not step 6 (`harness update`/`adopt`) — unless Audit
found a `.harness/harness.lock` already present, in which case stop and defer to `start-project`
entirely: that is routine harness maintenance, not a first integration.

## Reconstruct decision history (optional)

Only when the owner opted in above. A separate, read-only investigation, independent of Install in
both directions — it neither blocks Install nor requires the harness having been installed first.
Read [RECONSTRUCT-HISTORY.md](./RECONSTRUCT-HISTORY.md) for sourcing, evidentiary discipline, the ADR
template, and the closing report shape. It writes no file — ADRs included — until the owner has seen
that report and separately authorized which ones to write.


<!--
Краткое описание (Summary): Этот навык предназначен для аудита существующей кодовой базы и безопасной интеграции ИИ-каркаса (agent-harness) без нарушения текущих процессов. Он включает в себя чтение конфигураций, анализ CI/CD, выявление конфликтов с существующими ИИ-инструментами и опциональную реконструкцию истории архитектурных решений, прежде чем переходить к установке.

Перевод:
---
name: integrate-project
description: Аудит существующей, уже значительной кодовой базы и интеграция этого каркаса (harness) в неё без нарушения того, что уже есть. Используйте, когда в репозитории уже есть значимый код, соглашения, CI или другая конфигурация ИИ-инструментов, и требуется впервые интегрировать каркас (навыки, AGENTS.md, ссылки на обнаружение). Для совершенно новой идеи, пустого или почти пустого репозитория, или для пересмотра проекта, в котором уже используется каркас, вместо этого используйте `start-project`.
---

# Интеграция проекта

Интегрируйте переносимый каркас (harness) в кодовую базу, которая уже существует, не пытаясь угадать, что проект уже знает о самом себе. Читайте реальные файлы, прежде чем спрашивать; относитесь к репозиторию, а не к разговору, как к первичному источнику истины.

Определите реальный путь этого навыка и убедитесь, что публичный корень `agent-harness` двумя уровнями выше содержит `skills/REGISTRY.md` и `harness/bin/harness.py`. Это разрешение завершено только тогда, когда существуют оба файла; в противном случае сообщите, что публичный пакет неполон, вместо того чтобы предполагать другую установку.

## Аудит

1. **Стек и команды.** Читайте манифесты напрямую — `package.json` (и его `scripts`), файлы блокировок (lockfiles), `pyproject.toml`/`requirements.txt`, `go.mod`, `Cargo.toml`, `Gemfile` или их эквиваленты. Выводите стек и реальные команды для установки/запуска/тестирования/линтера/сборки из того, что фактически настроено, а не из утверждений в README или памяти пользователя.
2. **Соглашения, которые не указаны в манифесте.** Читайте файлы рабочих процессов CI (`.github/workflows/*`, `.gitlab-ci.yml` и т.д.) для команд, которые фактически запускает CI — реальное положение дел важнее документации, которая может устаревать. Читайте недавние имена веток (`git branch -a`, `git log --all --oneline -20`) и ветку по умолчанию удаленного репозитория для `branch_pattern` и `base_branch`. Изучайте существующую структуру каталогов тестов/документации вместо того, чтобы предполагать какое-то соглашение.
3. **Существующая конфигурация ИИ-инструментов.** Ищите `AGENTS.md`, `CLAUDE.md`, `.cursor/rules`, `.github/copilot-instructions.md` и каталог `.claude/`, который не управляется этим каркасом (где еще нет `.harness/harness.lock`). Читайте то, что там есть. Существующая инструкция, которая конфликтует с соглашениями этого каркаса, является находкой для согласования с владельцем, а не файлом для молчаливой перезаписи.
4. **Домен.** Классифицируйте основную работу проекта — программное обеспечение, контент, исследования/знания, операции, личное или другой явный домен — на основе того, что фактически содержит репозиторий.
5. **На что файлы не могут ответить.** Критерии готовности (Definition of Done), политика доставки/слияния и запрещенные действия редко находятся в репозитории. Отметьте их как открытые вопросы вместо того, чтобы угадывать их из соглашений стека.
6. **Сигнал истории решений.** Проверьте, есть ли уже в репозитории соглашение об ADR (журнал архитектурных решений) или записях решений (`docs/adr/`, или другое место, на которое указывает существующий документ), и получите примерное представление об истории его слияний/сессий (`gh pr list --state merged` / `glab mr list --merged`, `git log --all --oneline | wc -l`). Это сигнал для опционального этапа "Реконструкция истории решений" (Reconstruct decision history) ниже, а не само расследование — просто бегло просмотрите это.

Аудит работает только в режиме чтения. Не пишите, не устанавливайте и не выбирайте возможности (capability) на этом этапе.

## Представление и подтверждение

Кратко резюмируйте результаты: стек, реальные команды, соглашение о ветках/CI, обнаруженный домен, любую существующую конфигурацию ИИ-инструментов и то, где она конфликтует с этим каркасом, а также рекомендуемую возможность (capability). Спрашивайте только о том, что Аудит оставил действительно открытым — не переспрашивайте то, на что файл уже ответил.
Не продолжайте, пока владелец не подтвердит этот манифест.

Если на шаге 6 была найдена значимая история и нет существующего соглашения о записях решений, отдельно предложите опциональный этап "Реконструкция истории решений" ниже — назовите его медленным расследованием, независимым от установки каркаса, чтобы владелец мог легко от него отказаться. Согласие здесь не меняет этот манифест; отказ не блокирует Установку (Install).

## Установка

Продолжите с раздела "Сборка" (Assemble) из `global-skills/start-project/SKILL.md`, начиная с шага 2 и далее, используя этот аудит вместо его шага 1 (который уже более глубоко покрыт этапом Аудита этого навыка), а также его раздел "Завершение" (Finish) без изменений. Репозиторий, дошедший до этого навыка, по определению не имеет существующего каркаса, поэтому применяется шаг 5 Сборки (`harness init`), а не шаг 6 (`harness update`/`adopt`) — если только Аудит не обнаружил уже присутствующий файл `.harness/harness.lock`, в этом случае остановитесь и полностью перейдите к `start-project`: это рутинное обслуживание каркаса, а не первичная интеграция.

## Реконструкция истории решений (необязательно)

Только когда владелец согласился выше. Отдельное расследование только для чтения, независимое от Установки в обоих направлениях — оно не блокирует Установку и не требует, чтобы каркас был установлен первым.
Прочитайте [RECONSTRUCT-HISTORY.md](./RECONSTRUCT-HISTORY.md) для получения информации об источниках, доказательной дисциплине, шаблоне ADR и форме итогового отчета. На этом этапе не записывается ни один файл — включая ADR — до тех пор, пока владелец не увидит этот отчет и отдельно не авторизует, какие именно из них записать.
-->

