---
name: windowless
description: "Убрать мелькающие ЧЁРНЫЕ КОНСОЛЬНЫЕ ОКНА (cmd/powershell/Windows Terminal) на любом Windows-узле флота: найти все три источника уликами, погасить обратимо, доказать цифрой «до → после». Триггеры: “/windowless“, “/окошки“, “чёрные окна“, “чёрные окошки“, “мигают окна“, “лезут окна“, “мелькает консоль“, “окна воруют фокус“, “black windows“, “console windows popping“"
version: 1.0.0
---

# /windowless — чёрные окошки: найти, погасить, доказать

## 0. Зачем это существует

Антон работает глазами (§2.4). Окно, ворующее фокус раз в минуту, ломает работу сильнее,
чем медленный скрипт. Проблема **рецидивирующая**: каждая новая задача планировщика
рождается в режиме `Interactive` и становится новым мигателем. Поэтому лечение — не
разовый подвиг, а прогон этого скилла.

Замер на хабе 06.08.2026: было **~84 вспышки/час**, после прогона — **0**.

## 1. Три источника (и чем лечится каждый)

| № | Источник | Улика | Лечение |
|---|---|---|---|
| №1 | **Сам Claude Code** — окно на КАЖДУЮ shell-команду | в простое окон нет, при работе — есть | официального выключателя НЕТ → только скрыватель |
| №2 | **Задачи планировщика в режиме Interactive** | `LogonType=Interactive` + частый повтор | флип в `S4U` — окно физически не может появиться |
| №3 | **Сторожа MCP**, респавнящие мёртвые демоны через `cmd` | лог сторожа «порт мёртв → перезапуск» каждые N минут | флип сторожа в S4U + починить сам демон |
| №4 | **Дочерний консольный exe из скрипта** — python зовёт `subprocess.run` без `CREATE_NO_WINDOW` | заголовок окна = ИМЯ EXE (не cmd/терминал), цепочка родителей ведёт к скрипту | `creationflags=CREATE_NO_WINDOW` в вызывающем коде |

⭐ Иерархия: **S4U — настоящий фикс** (окна нет), **скрыватель — подпорка** (гасит уже
показанное, возможен под-кадровый блик). Скрыватель не заменяет флип.

⭐ №4 — отдельный класс (замер [машина флота] 10.08.2026: **120 окон/мин**, каждое —
`ssh-keygen.exe`, цепочка: задача Regress Grid Nightly → `regress_run.py` → `fleet_sign.py` →
ssh-keygen). Отличие от №2 по улике: заголовок окна называет полезный exe, а не терминал.
Флип родительской задачи в S4U эти окна тоже гасит, но НЕ лечит класс — тот же скрипт из
живой сессии (источник №1) снова мигает. Корень чинится в коде:
`creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0` на каждый
`subprocess.run` консольного exe. Починено в `fleet_sign.py` 10.08 (ZBOOKG8), selftest PASS;
файл разъезжается синком, но проверяй на узле фактом (§7.3-бис).

## 2. Порядок работы

### Шаг 1 — ДИАГНОЗ (0 токенов, ничего не меняет)

```
powershell -NoProfile -ExecutionPolicy Bypass -File "%USERPROFILE%\.claude\scripts\windowless_audit.ps1"
```

Даёт: сколько активных Interactive, сколько ЧАСТЫХ (тикают чаще раза в час — именно они
дают ощущение «постоянно»), оценку **вспышек/час**, жив ли скрыватель, состояние портов
MCP 8765-8768 и какие сторожа мигают. Последняя строка `ИТОГ ...` — машинная, для сводки.

⛔ Не выноси вердикт «виноват X» без строки из аудита или лога (§5.4 причина = такой же
claim, как вывод).

### Шаг 2 — СКРЫВАТЕЛЬ (обратимо, без UAC, делаю САМ)

Если аудит говорит `hider_alive=False` или `hider_autostart=False`:

1. Проверить `~/.claude/scripts/console_hider.ps1` на диске.
2. Положить в автозапуск `console-hider.vbs` (запуск через `wscript`, `WindowStyle 0`).
3. Запустить сразу, не ждать перезагрузки.
4. **Доказать**: `_console_hider_log.txt` должен получить строки `hide#N [hook] <класс>`.
   Журнала нет = скрыватель не доказан, вердикт максимум ⚠️.

⚠️ Он прячет ВСЕ окна Windows Terminal. Если оператор узла пользуется терминалом руками —
скрыватель ему не ставить (Антон CLI не пользуется, §2.4).

### Шаг 3 — ФЛИП В S4U (нужен ОДИН клик UAC оператора)

```
%USERPROFILE%\.claude\scripts\fix_windowless.cmd
```

Скрипт сам себя элевирует, сам находит кандидатов, **сам себя проверяет** (сначала одна
пробная задача — если она под S4U упала, всё откатывается и батч не идёт), пишет список
изменённого в `_windowless_flipped.txt`. Откат: `revert_windowless.cmd`.

Кого он НЕ трогает и почему:
- задачи, лезущие на **подключённые диски** ([путь владельца] гугл-драйв) — в session 0 этих дисков нет;
- **desktop-needers** по регексу: chrome/firefox/selenium/playwright/computer-use/скриншоты/
  буфер обмена/**git-daemon** (у git-демона в session 0 ломаются LISTEN-сокеты, проверено 03-04.07);
- **системные задачи Microsoft** — под `\Microsoft\` скрипт не ходит.

⚠️ Смена `LogonType` **требует администратора** — это единственное место, где нужны руки
оператора (§4.1: истинный блок, не рутина). Регистрация НОВОЙ задачи сразу с S4U из
неэлевированного шелла тоже упадёт (`0x[id]`) → ставь новую задачу Interactive, потом
флипай пачкой ([[s4u-needs-uac-preregister-interactive]]).

### Шаг 4 — ПЕРЕПРОГОН И ДОКАЗАТЕЛЬСТВО

Повторить Шаг 1. Годный результат: `frequent=0`, `flashes_per_hour=0`, `hider_alive=True`.
В отчёт Антону — цифра **до → после**, а не «починил».

### Шаг 5 — ОСТАТКИ

Оставшиеся Interactive — назвать поимённо и сказать, почему они там законны (редкие /
нужен десктоп). Молча оставлять нельзя. Если среди них есть частый — это баг отбора,
разбирайся, а не списывай.

## 3. Грабли (замерены, не выдуманы)

1. **Самосовпадение grep.** `Get-CimInstance Win32_Process | ? CommandLine -match 'console_hider'`
   поймает ТВОЙ ЖЕ процесс — паттерн лежит в твоей командной строке. Собирай строку из
   кусков (`'console' + '_hider'`) и исключай `$PID`, иначе получишь ложное «скрыватель жив».
2. **UTF-8 без BOM.** PowerShell 5.1 читает такой файл как ANSI → кириллица превращается в
   мусор и скрипт не парсится. Сохранять `.ps1` с кириллицей **с BOM**
   (`[Text.UTF8Encoding]::new($true)`).
3. **Хардкод пути пользователя.** В `console_hider.ps1` был зашит журнал `[путь владельца]` —
   на другом узле он молча не писался, и «работает ли» доказать было нечем. Все пути —
   от `%USERPROFILE%` (§10.3).
4. **Отключённые задачи в счёте.** `Get-ScheduledTask` без фильтра `State -ne 'Disabled'`
   даёт завышенную цифру (на хабе 107 против реальных 45). Interactive + Disabled окон не даёт.
5. **`conhost --headless` не работает** — ошибка 4320, полезная нагрузка не стартует. Не использовать.
6. **Скрыватель гасит ПОСЛЕ показа** — возможен блик в один кадр. Полный ноль даёт только
   S4U (или WSL, отклонён Антоном).

## 4. Флот

Прогонять на КАЖДОМ Windows-узле (хаб, [машина флота], машины коллег). Mac/Linux не касается.
Движки лежат в `~/.claude/scripts` и разъезжаются синком, но **флип требует локального клика
UAC на каждой машине** — доставка ≠ применение (§7.3-бис). Готово = аудит на узле показал
`flashes_per_hour=0`, а не «отправил посылку».

## 5. Связанное

Память: [[black-windows-root-claude-code]] (корень и три слоя), [[hub-tasks-s4u-windowless]]
(история флипа, mapped-drive карв-аут), [[s4u-needs-uac-preregister-interactive]] (почему
UAC), [[deterministic-script-gotchas]] (BOM, хардкоды).
Канон: §5.5 сторож не живёт в том, что сторожит · §7.3-бис раскатка на весь флот · §2.4 глазами.


<!--kit-footer-->

---

**Like this skill?** It is one of 100 in [second-brain-starter-kit](https://github.com/tonydzi/second-brain-starter-kit): the second brain we built for ourselves and run every day at Palo Alto AI Research Lab. Install the whole set with `npx skills add tonydzi/second-brain-starter-kit`. Everything is open source and free, so take what you need.

Flagships worth a look on their own: [secondop-panel](https://github.com/tonydzi/secondop-panel) (a second opinion from a panel of external models), [claude-memory-tidy](https://github.com/tonydzi/claude-memory-tidy) (stop your agent's memory from rotting), [telegram-mcp-kit](https://github.com/tonydzi/telegram-mcp-kit) (your own Telegram over MCP in about 15 minutes).

Author: **Anton Dziatkovskii**, Palo Alto AI Research Lab. Telegram [@tonydzi](https://t.me/tonydzi) - WhatsApp [+1 341 222 9178](https://wa.me/13412229178) - X [@Tony_Stef_](https://x.com/Tony_Stef_)

**Engineers: want to test-drive this setup?** Message me. I hand out free starter seeds to engineers who test and report back, and custom skill requests are welcome.
