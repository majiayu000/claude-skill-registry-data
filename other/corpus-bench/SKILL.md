---
name: corpus-bench
description: "Станок верификации чужого кода на НАШИХ живых корпусах (GIT-25). Триггеры - “/corpus-bench“, “прогони по корпусу“, “проверь их фикс на наших транскриптах“, “corpus bench“, “верифицируй на корпусе“, а также САМ внутри заходов GIT-S5/S8/S9, когда чужой PR/фикс трогает чтение транскриптов, сессий, памяти агентов"
version: 1.0.0
---

# /corpus-bench — верификация чужого кода на наших корпусах

> Родился 14.08.2026 из ручных прогонов GIT-S5/S9 (casdk#1202: 3 дерева x 12 227
> файлов руками ~час; станком — 5 минут). Приказ Антона: «Делай станок и скилл и рутину».

**Движок (единственный источник логики, дока = его docstring):**
`python "$USERPROFILE/.claude/scripts/git25-tools/corpus_bench.py"`

## Когда применять
Чужой PR/фикс/релиз читает или пишет **транскрипты Claude Code, сессии, память агентов,
JSONL-логи** — всё, для чего у нас есть живой корпус, которого нет у автора.
Наше несправедливое преимущество: 12k+ живых транскриптов на узел, 5 узлов, 3 ОС.

## Ритуал (4 шага)
1. **Цель.** Папка `corpus_bench_targets/<name>/` рядом с движком: `target.json`
   (repo · pinned_ref · install · metric · direction · fetch_refs для PR-голов) +
   `plugin.py` с одной функцией `evaluate(tree_path, files) -> dict`
   (сам добавляет tree в sys.path; возвращает СЧЁТЧИКИ, никогда содержимое файлов).
   Образец: `corpus_bench_targets/casdk-session-reader/`.
2. **Прогон.** `... run <name> --refs main_sha,pr_sha [--limit 200]` — сначала с
   `--limit` (быстрая проверка плагина), потом полный. Таблица: metric · ratio ·
   delta improved/same/WORSE. Exit 3 = есть регрессия.
3. **Мутант-дисциплина (руками, до отправки коммента):** (а) red-before — метрика
   обязана двигаться между деревьями не вакуумно; (б) зонд загрузки — правка
   реально в пути исполнения (класс «невыполнившийся мутант» из журнала 12.08);
   (в) в коммент — только счётчики и оффсеты, leak-scan обязателен.
4. **Пин.** Верификация закончена → `watch: true` в target.json: недельная рутина
   дальше сама следит, что фикс не растерялся в main.

## Watch-рутина
- Задача Task Scheduler `corpus-bench-weekly` (этот узел; ночное окно §4.6).
- Отчёт: `$USERPROFILE/.claude/scripts/_logs/corpus_bench_last_<host>.txt` —
  **потребитель = вахта следующего захода GIT-S5** (мастер-файл GIT-25, приказ 14.08).
- ALARM (exit 3) = watch_ref ухудшился >5пп с прошлого прогона → это сырьё для
  issue с репро, не для паники: сначала найти коммит-виновник.
- Счётчик использования: `_logs/corpus_bench_<host>.jsonl` (читается на /retro).

## Границы
- Клоны/venv в `%LOCALAPPDATA%/corpus_bench` — узло-локально, в синк не едет.
- Пер-хостовые state/report/counter (single-writer shard) лежат в `_logs`. ⚠️ ПРОВЕРЕНО 25.08.2026:
  синкается ТОЛЬКО `.txt`-отчёт; `*.jsonl`/`*.json` заперты чёрным списком `.stignore.shared`
  (стр. 90), поэтому счётчик и state — **узло-локальные**. Это осознанно: кросс-узловых
  читателей у счётчика нет (проверено грепом 25.08), а общий append-леджер с шестью
  писателями — тот самый класс гонок, что уже сжёг pub_ledger/approval_ledger/voice-registry.
- Плагин НЕ печатает содержимое транскриптов — только счётчики (приватность).
- Selftest: `... selftest` (7 оффлайн-кейсов). Crash-guard: exit 4 = станок упал сам.


<!--kit-footer-->

---

**Like this skill?** It is one of 100 in [second-brain-starter-kit](https://github.com/tonydzi/second-brain-starter-kit): the second brain we built for ourselves and run every day at Palo Alto AI Research Lab. Install the whole set with `npx skills add tonydzi/second-brain-starter-kit`. Everything is open source and free, so take what you need.

Flagships worth a look on their own: [secondop-panel](https://github.com/tonydzi/secondop-panel) (a second opinion from a panel of external models), [claude-memory-tidy](https://github.com/tonydzi/claude-memory-tidy) (stop your agent's memory from rotting), [telegram-mcp-kit](https://github.com/tonydzi/telegram-mcp-kit) (your own Telegram over MCP in about 15 minutes).

Author: **Anton Dziatkovskii**, Palo Alto AI Research Lab. Telegram [@tonydzi](https://t.me/tonydzi) - WhatsApp [+1 341 222 9178](https://wa.me/13412229178) - X [@Tony_Stef_](https://x.com/Tony_Stef_)

**Engineers: want to test-drive this setup?** Message me. I hand out free starter seeds to engineers who test and report back, and custom skill requests are welcome.
