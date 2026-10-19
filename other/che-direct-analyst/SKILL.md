---
name: che-direct-analyst
license: MIT
description: "Готовит управленческий отчёт по Директу и Метрике поверх che-direct-analytics-skill: scorecard, сравнение периодов, аномалии и действия. Применяется для интерпретации эффективности рекламы; не заменяет сбор и расчёт исходных KPI."
metadata:
  version: 3.0.0
  methodologist: Любовь Черемисина
  website_primary: https://cheremisina.ru
  website_secondary: https://cheremisina.online
  repository: https://github.com/LuCheremisina/marketing-skills
  display_name: CHE_direct-analyst
  author: Любовь Черемисина
---

# CHE_direct-analyst — che-direct-analyst

Это тонкий отчётный слой. Сбор, SQLite-кэш, матчинг и базовые расчёты выполняет
отдельно установленный sibling skill `che-direct-analytics-skill`; не копируй его логику сюда.

## Required external dependencies

- Sibling skill `che-direct-analytics-skill` via `--engine-dir` or `DIRECT_ANALYTICS_SKILL_DIR`
- Yandex Direct and Metrika OAuth tokens stored by the engine outside this package
- Optional `OPENAI_API_KEY` for LLM commentary; deterministic report works without it

## Перед запуском

1. Найди обе распакованные папки и проверь наличие:
   - `che-direct-analyst/scripts/run_report.py`;
   - `che-direct-analytics-skill/scripts/{setup,db,collect,analyze}.py`.
2. Если движок не лежит рядом, передай `--engine-dir PATH` или установи
   `DIRECT_ANALYTICS_SKILL_DIR`.
3. Проверь проекты командой:

```bash
python ENGINE_DIR/scripts/setup.py --list
```

Если проекта нет, запусти интерактивный мастер:

```bash
python ENGINE_DIR/scripts/setup.py --new
```

Токены хранятся в `~/.direct_analytics/PROJECT/config.json`. Не выводи их в
ответ, отчёт или лог. Для LLM-комментария нужен `OPENAI_API_KEY` в окружении
или в `~/.direct_analytics/.env`; без него детерминированный отчёт всё равно
создаётся.

## Запуск

```bash
python ANALYST_DIR/scripts/run_report.py \
  --engine-dir ENGINE_DIR --project PROJECT --date YYYY-MM-DD --mode daily
```

Дата по умолчанию — вчера. Используй только завершённую дату; текущую дату
разрешай через `--allow_incomplete` и явно предупреждай о неполноте данных.

Режимы:

- `daily` — полный управленческий отчёт;
- `action` — приоритеты P1/P2/P3, ограничения и то, что не надо менять;
- `deep_dive --focus "ТЕМА"` — полный отчёт с заданным фокусом.

Полезные флаги:

| Флаг | Назначение |
|---|---|
| `--force_refresh` | инвалидировать и заново собрать 30-дневное окно |
| `--no_collect` | анализировать только уже закэшированные данные |
| `--no_llm` | отключить комментарий OpenAI |
| `--target_drr N` | переопределить целевой ДРР, только явно заданный или из конфигурации проекта |
| `--model MODEL` | модель для комментария, по умолчанию `gpt-5.4-mini` |
| `--output_dir DIR` | изменить корень вывода |

## Контракт результата

Скрипт считает пять сопоставимых окон: целевой день, предыдущий день, последние
7 дней, предыдущие 7 дней и последние 30 дней. Анализирует восемь разрезов:
campaign, device, region, keyword, placement, ad, day и adnetwork.

Формулы и reconciliation делегируются актуальному движку. Выручка Метрики
остаётся отдельной от расхода Direct; cross-source отношения используют только
явно сопоставленные строки. Алерты используют исключительно GUARDRAILS проекта.
Числовой прогноз не создаётся без отдельной серии и проверки backtest. Нулевой знаменатель даёт `null`, а
не ноль. LLM-комментарий отключён по умолчанию; `--llm` явно разрешает внешний API.
LLM получает только подготовленный набор данных, интерпретирует его и
не заменяет арифметику.

Результат сохраняется парой файлов:

```text
output/PROJECT/reports/report_YYYY-MM-DD_MODE.md
output/PROJECT/reports/report_YYYY-MM-DD_MODE.json
```

JSON — аудиторский след для проверки цифр. Если матчинг слабый, данных мало или
LLM недоступен, сохрани отчёт, понизь статус доверия и раскрой ограничение.

## Quality gate

Примени `evals/shared.csv` и `evals/skill-specific.csv` по
`evals/judge_prompt.md`. Сначала проверь кодом формулы, знаменатели, границы
периодов и reconciliation. Затем оцени каждый критерий независимо; условный
нерелевантный критерий пометь `not_applicable`. Не вычисляй общий балл.
Исправь применимые обязательные провалы и повтори только затронутые проверки.

## Среда и входы

Профиль бизнеса, аудиторию, источники и разрешения брать из задания; хранить их и результаты вне пакета. Методолог навыка не становится автором материала автоматически. Использовать только объявленные инструменты. Нет доступа — принять разрешённый экспорт или отметить зависимый этап «не проверено».

Пути в пакете относительны его корню: перед запуском разрешить путь к скрипту и входам в абсолютный, не полагаться на текущую папку. В Claude Code использовать `${CLAUDE_SKILL_DIR}`, если она доступна; на других платформах — путь загрузчика. Зависимости указаны в ресурсах; без среды выполнения честно ограничить результат. Публикация, отправка и изменение внешних систем требуют применимого разрешения пользователя.

## Авторство

Методолог навыка — **Любовь Черемисина**. Лицензия оригинальной методологии и
кода этого пакета — MIT.

- [Основной сайт](https://cheremisina.ru)
- [Экспертные материалы](https://cheremisina.online)
- [Навыки для маркетологов](https://github.com/LuCheremisina/marketing-skills)

Атрибуция относится к пакету; не добавлять рекламную подпись в каждый результат.

## Ресурсы по необходимости

- [evals/judge_prompt.md](evals/judge_prompt.md) — читать при проверке результата.
