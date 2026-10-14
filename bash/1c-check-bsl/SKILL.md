---
name: 1c-check-bsl
description: "Проверяет синтаксис изменённых BSL-модулей одной командой: статический разбор BSL Analyzer и компиляция платформой 1С в целевой ИБ. Используйте для модулей основной конфигурации, расширений и внешних обработок/отчётов."
metadata:
  short-description: "Статическая и платформенная проверка BSL."
---

# Проверка BSL

Repo script: `./scripts/qa/check-bsl.sh`
Windows launcher: `./scripts/qa/check-bsl.ps1`

Команда проверяет выбранные модули одного корня исходников и печатает две независимые оценки:

- `static` — `bsl-analyzer-app analyze` только по выбранным модулям, диагностика `ParseError`; быстрый ответ, не финальная проверка;
- `platform` — компиляция платформой 1С в ИБ runtime profile, на её версии платформы и в режиме совместимости её конфигурации.

## Запуск

```bash
./scripts/qa/check-bsl.sh src/cf/CommonModules/Имя/Ext/Module.bsl
./scripts/qa/check-bsl.sh --mode fast src/cfe/<Расширение>/CommonModules/Имя/Ext/Module.bsl
./scripts/qa/check-bsl.sh --mode platform --profile env/local.json src/cf/Documents/Имя/Ext/ObjectModule.bsl
./scripts/qa/check-bsl.sh --profile env/local.json --dry-run src/cf/CommonModules/Имя/Ext/Module.bsl
```

Режимы:

- `full` (по умолчанию) — сначала `static`, затем `platform`;
- `fast` — только `static`; итог `static-only`, платформа в результате помечена `not-run`;
- `platform` — только `platform`.

Явный выбор режима пользователем имеет приоритет. Не выдавайте `fast` за полную проверку.

## Как команда выбирает цель

- Корень определяется по ближайшему каталогу с `Configuration.xml`: это основная конфигурация или, если в нём есть `ConfigurationExtensionPurpose`, расширение. Модули выгрузки EPF/ERF (`<Имя>.xml` рядом с каталогом `<Имя>/`) образуют внешний артефакт.
- Модули из разных корней команда отклоняет с кодом 2. Проверяйте один корень за запуск; успех соседней конфигурации не доказывает правильность целевой.
- Для расширения и EPF/ERF статическому разбору нужна основная конфигурация целевой ИБ: `--configuration-root <каталог>`, `BSL_CONFIGURATION_ROOT` или `src/cf`. Без неё `static` получает `not-run`.

## Платформенная проверка

- Основная конфигурация: `./scripts/platform/check-cf-modules.sh`. Выбранные модули сначала частично загружаются (`/LoadConfigFromFiles -listFile ... -partial`) в конфигурацию ИБ профиля без обновления конфигурации базы данных, затем `/CheckModules` компилирует всю конфигурацию в режимах запуска из `Configuration.xml`. Режимы можно задать через `--execution-mode`.
- Расширение: `./scripts/platform/check-cfe-config.sh` с именем расширения.
- EPF/ERF: платформенной проверки модулей нет. Сборка внешнего артефакта не является проверкой синтаксиса; итог основан на `static`.
- Без профиля целевой ИБ платформенная проверка не выполняется (`not-run`). Не подставляйте профиль другой базы.
- Уже существующие замечания базы можно передать в `check-cf-modules.sh --baseline-diagnostics <json>`: блокируют только новые.
- `source_identity.loaded_match=not-verified` означает, что проверена установленная в ИБ конфигурация, а не локальные исходники.

Прямые вызовы Designer, `ibcmd` и клиента 1С запрещены. Платформенный запуск наблюдается по навыку `1c-observe-run`. Проверка всей конфигурации может долго не печатать вывод; повторный запуск из-за паузы в выводе не делайте, смотрите `<run-root>/observation.jsonl`.

## Внешние артефакты пакетом

Для набора EPF/ERF без платформы используйте `./scripts/qa/analyze-bsl-external.sh` (`--all-managed`, имена или каталоги выгрузок, `--extension`, `--declare-extension`, `--configuration-root`). Выгрузки из `ordinary/` этой командой не проверяются.

## Итог

Команда печатает и пишет в `<run-root>/summary.json`:

```text
target: configuration|extension|external <имя> (<корень>)
mode: full|fast|platform
static: passed|failed|not-run — <причина или доказательство>
platform: passed|failed|blocked|not-run — <причина>; platform <версия>, compatibility <режим>, modes <режимы>
overall: passed|failed|blocked|static-only
синтаксис: проверен|ошибки|не проверен
```

Коды выхода: 0 — `passed` или `static-only`; 1 — `failed`; 2 — неверный выбор модулей; 3 — проверка не выполнена или заблокирована.

Если ни анализатор, ни платформа недоступны, результат — `синтаксис: не проверен`. Сообщайте его пользователю как есть; не заменяйте проверку чтением кода.

Структурные проверки `cf-validate`, `cfe-validate`, `epf-validate` и XML не заменяют платформенную оценку.
