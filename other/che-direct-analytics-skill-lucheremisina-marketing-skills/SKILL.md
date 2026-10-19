---
name: che-direct-analytics-skill
description: "Собирает и рассчитывает данные Директа и Метрики раздельно, сверяет периоды, KPI и аномалии. Применяется для диагностики кампаний, ключей, CPA/ROAS/CTR и атрибуции; не распределяет неизвестную выручку по расходам."
license: MIT
metadata:
  version: 3.0.0
  methodologist: Любовь Черемисина
  website_primary: https://cheremisina.ru
  website_secondary: https://cheremisina.online
  repository: https://github.com/LuCheremisina/marketing-skills
  display_name: CHE_direct-analytics-skill
  author: Любовь Черемисина
---

# CHE_direct-analytics-skill — che-direct-analytics-skill

## Границы и принцип работы

Навык только читает API и локальный SQLite-кэш. Он никогда не меняет кампании,
ставки, бюджеты или цели. Любое предложенное действие — черновик для проверки
аналитиком.

Директ и Метрика — параллельные источники. `CrossSourceROAS` рассчитывается
только по явно сопоставленным строкам: выручка Метрики ÷ расход Директа.
Подписывай оба источника, период и правило сопоставления; это межисточниковая оценка.
Неатрибутированная выручка остаётся отдельной строкой и никогда не
распределяется по расходу.

## Настройка проекта

Проверь `~/.direct_analytics/{project}/config.json`. Для нового проекта:

```bash
python scripts/setup.py --new
```

Помимо OAuth-токенов, зафиксируй data contract:

- `REPORT_TIMEZONE` — IANA timezone отчёта;
- `UTM_SOURCE` и `UTM_MEDIUM` — фильтр трафика Директа, обычно `yandex` и `cpc`;
- `UTM_CAMPAIGN_MAPPING` — `campaign_id` или `campaign_name`;
- `ATTRIBUTION_MODE` — только `parallel` в первой версии;
- `GUARDRAILS` — проектные цели и `min_abs_delta` для алертов;
- `MONITOR_METRICS` и `COHORT_RULES` — список контролируемых KPI и regex-правила внутренних когорт.

Не добавляй универсальные пороги CPA/ROAS: они должны быть заданы в конкретном
проекте и иметь бизнес-смысл.

## Сбор фактов

```bash
python scripts/collect.py --project NAME --date_from 2026-08-01 --date_to 2026-08-07
python scripts/collect.py --project NAME --scope keyword --scope ad --date_from D --date_to D
```

- По умолчанию собирается `core`: `campaign`, `device`, `region`, `placement`, `adnetwork`.
- `keyword` и `ad` собираются только отдельными Direct Reports и только по явному `--scope`.
- Все данные сохраняются по завершённым дням. Пустой день — валидный факт;
  ошибка API — `complete=false` и будет повторно запрошена при следующем запуске.
- `--refresh` инвалидирует и пересобирает весь выбранный диапазон.
- Collector печатает contract, покрытие дат, свежесть и ошибки. Успешный выход
  не является доказательством production-эффекта — только успешного чтения API.

## Аналитика и reconciliation

```bash
python scripts/analyze.py --project NAME --period 7d --dim campaign --compare prev_period --format json
python scripts/analyze.py --project NAME --dim keyword --date_from D --date_to D
python scripts/analyze.py --project NAME --dim campaign --anomaly
```

Доступные разрезы: `campaign`, `device`, `region`, `keyword`, `placement`,
`ad`, `day`, `adnetwork`.

`campaign` и `day` читают reconciliation; поэтому могут показать Direct KPI,
Метрика KPI и подписанные cross-source показатели. Остальные разрезы показывают
только нативные Direct KPI, пока для них не настроено совместимое зерно Метрики.
Если нужный scope отсутствует, `analyze.py` подскажет точную команду сбора.

`--anomaly` применяет только `GUARDRAILS` проекта. Он не содержит скрытых
глобальных правил и не рекомендует автоматическое отключение площадок.

## Диагностика и feedback

```bash
python scripts/diagnose.py --project NAME --metric MetrikaRevenue \
  --date_from 2026-08-01 --date_to 2026-08-07 --compare prev_period --format json

python scripts/diagnose.py feedback --project NAME --run-id RUN_ID \
  --verdict confirmed --actual-cause "Campaign was paused" \
  --action-outcome "No change was applied"
```

`diagnose.py` возвращает `diagnosis_record`:

- data-status, coverage, timezone и правила атрибуции;
- trigger и сравниваемые периоды;
- воронку `показы → клики → визиты/цели → транзакции/выручка`;
- `confirmed_causes` только с прямым системным доказательством;
- `likely_drivers` как численный вклад, не как причинное утверждение;
- `hypotheses` и следующий read-only тест;
- draft-действие с явным требованием approval для любого изменения кабинета.

Human feedback хранит `confirmed`, `partial` или `refuted`, фактическую причину
и результат действия. Он предназначен для измерения калибровки, не для
неявного обучения модели.

## Monitor, бенчмарки и dashboards

```bash
python scripts/monitor.py --project NAME --date 2026-08-10 --format json
python scripts/benchmark.py --project NAME --period 30d --format html
python scripts/dashboard.py --project NAME --spec report-spec.json --format html
```

Monitor использует четыре предыдущих сопоставимых дня недели за 28 дней,
median и MAD. High alert требует одновременно статистической аномалии,
проектной материальности и полного data-quality gate. При недостаточной истории
возвращается `baseline_insufficient`. Доставка ограничена CLI + JSON/HTML:
n8n, Telegram и scheduler не входят в навык.

`benchmark.py` строит только внутренние когорты и показывает `n`, p25, median,
p75. Внешний market benchmark не создаётся.

LLM может превратить естественный запрос в `ReportSpec`, но `dashboard.py`
принимает лишь JSON со списком зарегистрированных `metrics`, `dimension`,
`period` либо `date_from/date_to` и `chart` из `table|line|bar`. Ответ всегда
содержит исходный query-spec и data-status.

Пример:

```json
{
  "dimension": "campaign",
  "metrics": ["Cost", "MetrikaRevenue", "CrossSourceROAS"],
  "period": "30d",
  "chart": "bar",
  "top": 10
}
```

## Quality gate

Перед результатом применить `evals/shared.csv`, `evals/skill-specific.csv` и
`evals/judge_prompt.md`. Арифметику, зерно данных, coverage, filters,
reconciliation, нулевые знаменатели и baseline проверяет код; LLM оценивает
только трассируемость и интерпретацию. Не вычислять общий балл.

Запуск локального test gate:

```bash
PYTHONPYCACHEPREFIX=/tmp/directanalytics-pycache \
python3 -m unittest discover -s tests -v
```

### Shadow-mode до запуска мониторинга

Для десяти исторических отклонений аналитик сохраняет `confirmed`, `partial`
или `refuted` через `diagnose.py feedback`. В каждом `run_id` обязательны
complete data-status и evidence trail. Локальный gate не обучает модель и не
запускает мониторинг:

```bash
python scripts/shadow_gate.py --project NAME --minimum-cases 10 --format json
```

Он считает долю подтверждённых диагнозов, false-certainty для явных
`confirmed_cause`, precision high-priority кейсов (если они промаркированы) и
медианное время до human verdict. Пока gate не `passed`, реальный запуск
монитора запрещён процессом; CLI сам не создаёт расписание или доставку.

## Навигация по ресурсам

- [references/api_notes.md](references/api_notes.md) — читать при соответствующем этапе workflow.

## Зависимости

Python-зависимости: [requirements.txt](requirements.txt). Использовать разрешённое
изолированное окружение; при отсутствии зависимостей раскрыть ограничение.

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
