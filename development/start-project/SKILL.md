---
name: start-project
description: Start a new project from an idea or create, audit, or update its self-contained agent harness. Use when the user wants to shape or initialize a software, content, research, operations, personal, or other project, decide when it needs a repository, or install or revise a project harness. Ordinary work inside an already-harnessed project does not invoke this skill; a repository with substantial existing code and conventions but no harness yet is better served by `integrate-project`'s deeper audit.
---

# Start Project

Own the path from an unshaped idea to a portable project. A repository, stack, tracker, and harness
are outputs of project design, not prerequisites. Keep each phase read-only until the owner confirms
its proposed durable artifact.

Resolve this skill's real path and verify that the public `agent-harness` root two levels above it
contains `skills/REGISTRY.md` and `harness/bin/harness.py`. Its vendored workflows are a library: use
the registry to locate and read only the exact `SKILL.md` needed for the current phase. This
resolution is complete only when both files exist; otherwise report that the public package is
incomplete instead of guessing another installation.

## Shape

1. Establish whether the user has an idea, a seed directory, or an existing repository. Inspect
   existing files before asking questions. A repository with substantial existing code and
   conventions but no harness yet is `integrate-project`'s dedicated audit, not this generic path —
   hand off to it rather than deriving facts thinly here.
2. Classify the project's primary work as software, content, research/knowledge, operations,
   personal, or another explicit domain. Classification selects workflows; it does not constrain
   what the project may become.
3. Resolve the decisions that change the next artifact. For an unshaped idea, read and follow
   `skills/vendor/mattpocock/productivity/grilling/SKILL.md`. Use `research`, `to-questionnaire`,
   `prototype`, or `domain-modeling` only when its registry description matches the current branch.
   Tracker-dependent workflows such as `to-spec` and `wayfinder` begin after a repository and its
   tracker contract exist.
4. Keep disposable thinking in the session. Once purpose, intended outcome, recurring work, and
   the next useful artifact are known, recommend exactly one of: continue the conversation, write a
   brief, create a seed repository, or assemble a harness.

Shape is complete only when the owner confirms that recommendation or explicitly keeps the work in
the conversation. Confirmation authorizes that one artifact, not later scaffolding.

## Seed

After the owner confirms a seed, create or reuse the named Git repository and write only the
confirmed brief and decision notes. Preserve an existing repository's layout and instructions.
Record unresolved stack, tracker, and harness decisions as unresolved rather than choosing them to
make the seed look complete.

Seed is complete when the repository path is verified, durable files contain only confirmed facts,
`git status` has been inspected, and the owner can see which decisions remain open. Application
code, tracker setup, and a harness require their own confirmed next artifact.

## Assemble

Build a harness only after the project has stable work to support, or immediately when the user
explicitly requests one.

1. Derive purpose, project type, stage, base branch, tracker, recurring activities, commands,
   boundaries, delivery policy, and Definition of Done from the repository and conversation. Mark
   inapplicable commands and tracker as `N/A`.
2. Select the smallest coherent public capability:
   - `project-foundation` for general project thinking, research, handoff, domain language, and
     agent-facing instructions;
   - `mattpocock-suite` for recurring software engineering work;
   - no additional package merely because it is available.
3. When the owner asks `start-project` to select recurring workflows, allow a matching installed
   personal or organization catalog-entry skill to return catalog metadata. Pass only the project
   facts and recurring activities, and follow that entry skill's access boundary. Catalog selection
   does not authorize unrelated personal knowledge, tasks, notes, or secrets.
4. Present one harness manifest containing the project facts, public capability, overlay packages,
   project-only packages, integrations, boundaries, and files that will change. Resolve same-name,
   provenance, and licensing conflicts, then obtain owner confirmation for this manifest.
5. For a confirmed new harness run the resolved package command, replacing the example values with
   the confirmed manifest:

   ```bash
   python3 "<resolved-agent-harness-root>/harness/bin/harness.py" init "<repo>" \
     --project-type <type> \
     --capability <selected-capability> \
     --base-branch <branch>
   ```

   On Windows/PowerShell there is no `python3` (use `python`), and line
   continuation is `` ` ``, not `\`.

   Fill every unresolved `{{...}}` in `AGENTS.md`. Add project-only packages under
   `.harness/skills`; run `harness lock-project-skills` for their versioned hash lock, then
   `harness registry` after composing all packages. Use relative discovery links, never links back
   to a machine-local catalog.
6. For an existing harness run `harness diff` before `harness update`. Use `harness adopt
   --replace-conflicts` only for an explicit migration after reviewing same-name conflicts.
7. Keep MCP servers, plugins, hooks, and runtime settings in their native project files. When such
   files exist, inventory their relative paths, hashes, runtimes, verification action, and secret
   environment-variable names in `.harness/integrations.json`; never copy credentials into Git.

Assemble is complete when the confirmed manifest is represented by committed project files, every
package has source and hash provenance, and no unconfirmed integration or workflow was added.

## Finish

Prove each layer separately:

1. **Stored** — selected packages and locks exist under `.harness/`.
2. **Wired** — `.agents/skills` and `.claude/skills` resolve to the same project snapshot.
3. **Healthy** — `harness health` passes: template markers, names, registry, public/overlay hashes,
   discovery links, and integration inventory agree.
4. **Advertised** — a fresh runtime session lists an installed project skill. If the runtime has no
   native project skill root, it can route through `.harness/skills/REGISTRY.md` from `AGENTS.md`.
5. **Invoked** — that session opens the selected skill through its native mechanism.

If the current session cannot rescan discovery, report steps 4 and 5 as the exact remaining fresh-
session check. Finish by naming the project type, installed capabilities, excluded surfaces,
verification evidence, and next useful action.


<!--
Краткое описание (Summary): Навык `start-project` помогает пользователю пройти путь от неоформленной идеи до переносимого проекта, включая создание репозитория, сборку агентной обвязки (agent harness) и проверку установленных зависимостей.

Перевод:
---
name: start-project
description: Начать новый проект с идеи или создать, провести аудит или обновить его автономную агентную обвязку (agent harness). Используйте, когда пользователь хочет сформировать или инициализировать программный, контентный, исследовательский, операционный, личный или иной проект, решить, когда ему нужен репозиторий, или установить, либо пересмотреть проектную обвязку. Обычная работа внутри проекта, уже имеющего обвязку, не вызывает этот навык; для репозитория со значительным существующим кодом и соглашениями, но пока без обвязки, лучше подойдет более глубокий аудит от `integrate-project`.
---

# Начать проект

Владейте путем от неоформленной идеи до переносимого проекта. Репозиторий, стек, трекер и обвязка (harness)
являются результатами проектирования проекта, а не предварительными условиями. Держите каждую фазу в режиме только для чтения, пока владелец не подтвердит
её предложенный долговечный артефакт.

Определите реальный путь этого навыка и убедитесь, что публичный корень `agent-harness` на два уровня выше него
содержит `skills/REGISTRY.md` и `harness/bin/harness.py`. Его встроенные рабочие процессы — это библиотека: используйте
реестр, чтобы найти и прочитать только тот точный `SKILL.md`, который нужен для текущей фазы. Это
определение считается завершенным только тогда, когда существуют оба файла; в противном случае сообщите, что публичный пакет
неполный, вместо того чтобы угадывать другую установку.

## Формирование (Shape)

1. Установите, есть ли у пользователя идея, начальный каталог или существующий репозиторий. Изучите
   существующие файлы, прежде чем задавать вопросы. Репозиторий со значительным существующим кодом и
   соглашениями, но пока без обвязки — это специализированный аудит от `integrate-project`, а не этот общий путь —
   передайте работу ему, вместо того чтобы поверхностно выводить факты здесь.
2. Классифицируйте основную работу проекта как программное обеспечение, контент, исследования/знания, операции,
   личное или другую явную область. Классификация выбирает рабочие процессы; она не ограничивает
   то, чем проект может стать.
3. Примите решения, которые изменят следующий артефакт. Для неоформленной идеи прочитайте и следуйте
   `skills/vendor/mattpocock/productivity/grilling/SKILL.md`. Используйте `research`, `to-questionnaire`,
   `prototype` или `domain-modeling` только тогда, когда их описание в реестре соответствует текущей ветке.
   Рабочие процессы, зависящие от трекера, такие как `to-spec` и `wayfinder`, начинаются после того, как появятся репозиторий и его
   контракт с трекером.
4. Оставляйте одноразовые размышления в сессии. Как только цель, ожидаемый результат, повторяющаяся работа и
   следующий полезный артефакт будут известны, порекомендуйте ровно одно из следующего: продолжить разговор, написать
   бриф (brief), создать начальный репозиторий или собрать обвязку.

Формирование завершено только тогда, когда владелец подтверждает эту рекомендацию или явно оставляет работу в
разговоре. Подтверждение авторизует этот один артефакт, а не последующие строительные леса (scaffolding).

## Начало (Seed)

После того, как владелец подтвердит начало (seed), создайте или переиспользуйте названный Git-репозиторий и запишите только
подтвержденный бриф и заметки о решениях. Сохраняйте структуру и инструкции существующего репозитория.
Записывайте нерешенные решения по стеку, трекеру и обвязке как нерешенные, а не выбирайте их, чтобы
сделать начальную версию (seed) выглядящей завершенной.

Начало (Seed) завершено, когда путь к репозиторию проверен, долговечные файлы содержат только подтвержденные факты,
`git status` был проверен, и владелец может видеть, какие решения остаются открытыми. Код
приложения, настройка трекера и обвязка требуют своего собственного подтвержденного следующего артефакта.

## Сборка (Assemble)

Создавайте обвязку только после того, как у проекта появится стабильная работа для поддержки, или немедленно, когда пользователь
явно её запрашивает.

1. Выведите цель, тип проекта, этап, базовую ветку, трекер, повторяющиеся действия, команды,
   границы, политику доставки и Определение готовности (Definition of Done) из репозитория и разговора. Пометьте
   неприменимые команды и трекер как `N/A`.
2. Выберите наименьшую целостную публичную возможность (capability):
   - `project-foundation` для общего проектного мышления, исследований, передачи дел (handoff), языка предметной области и
     инструкций, ориентированных на агентов;
   - `mattpocock-suite` для повторяющейся работы в области программной инженерии;
   - никаких дополнительных пакетов только потому, что они доступны.
3. Когда владелец просит `start-project` выбрать повторяющиеся рабочие процессы, позвольте соответствующему установленному
   навыку входа в личный каталог или каталог организации (catalog-entry skill) вернуть метаданные каталога. Передайте только факты
   о проекте и повторяющиеся действия, и следуйте границам доступа этого навыка входа. Выбор из каталога
   не дает прав на не относящиеся к делу личные знания, задачи, заметки или секреты.
4. Представьте один манифест обвязки, содержащий факты о проекте, публичную возможность, пакеты-наложения (overlay),
   пакеты только для проекта (project-only), интеграции, границы и файлы, которые будут изменены. Разрешите конфликты одинаковых имен,
   происхождения и лицензирования, затем получите подтверждение владельца для этого манифеста.
5. Для подтвержденной новой обвязки выполните команду разрешенного пакета, заменив примеры значений на
   подтвержденный манифест:

   ```bash
   python3 "<resolved-agent-harness-root>/harness/bin/harness.py" init "<repo>" \
     --project-type <type> \
     --capability <selected-capability> \
     --base-branch <branch>
   ```

   В Windows/PowerShell нет `python3` (используйте `python`), и перенос
   строки — это `` ` ``, а не `\`.

   Заполните каждое неразрешенное `{{...}}` в `AGENTS.md`. Добавьте пакеты только для проекта в
   `.harness/skills`; запустите `harness lock-project-skills` для блокировки их версионированного хэша, затем
   `harness registry` после компоновки всех пакетов. Используйте относительные ссылки для обнаружения (discovery links), никогда не делайте ссылки обратно
   на локальный каталог машины.
6. Для существующей обвязки выполните `harness diff` перед `harness update`. Используйте `harness adopt
   --replace-conflicts` только для явной миграции после проверки конфликтов одинаковых имен.
7. Храните MCP-серверы, плагины, хуки и настройки среды выполнения в их родных файлах проекта. Когда такие
   файлы существуют, внесите их относительные пути, хэши, среды выполнения, действия по проверке и имена секретных
   переменных среды в инвентарь `.harness/integrations.json`; никогда не копируйте учетные данные в Git.

Сборка завершена, когда подтвержденный манифест представлен закоммиченными файлами проекта, каждый
пакет имеет подтвержденное происхождение источника и хэша, и не была добавлена ни одна неподтвержденная интеграция или рабочий процесс.

## Завершение (Finish)

Докажите каждый слой по отдельности:

1. **Сохранено (Stored)** — выбранные пакеты и блокировки существуют в каталоге `.harness/`.
2. **Подключено (Wired)** — `.agents/skills` и `.claude/skills` указывают на один и тот же снимок проекта.
3. **Здорово (Healthy)** — `harness health` проходит успешно: маркеры шаблонов, имена, реестр, хэши публичных/наложенных пакетов,
   ссылки для обнаружения и инвентарь интеграций совпадают.
4. **Объявлено (Advertised)** — новая сессия среды выполнения (runtime) отображает установленный навык проекта. Если среда выполнения не имеет
   родного корня навыков проекта, она может маршрутизировать через `.harness/skills/REGISTRY.md` из `AGENTS.md`.
5. **Вызвано (Invoked)** — эта сессия открывает выбранный навык через его родной механизм.

Если текущая сессия не может повторно просканировать обнаружение (discovery), сообщите шаги 4 и 5 как точную оставшуюся проверку новой
сессии. Завершите, назвав тип проекта, установленные возможности, исключенные поверхности,
доказательства проверки и следующее полезное действие.
-->

