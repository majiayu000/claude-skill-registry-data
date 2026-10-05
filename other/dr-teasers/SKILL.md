---
name: dr-teasers
description: "ДР-ПОЛОСА — превратить наши дипресёрчи в 10 тизеров в день и разослать их по каналам лаборатории. Триггеры “/dr-teasers“, “/dr-lane“, “тизеры по ресёрчам“, “разошли дипресёрчи“, “10 тизеров“, “полоса дипресёрчей“, “post research teasers“, а также САМА ежедневная рутина “Claude DR Teasers Daily“"
version: 1.0.0
---

# ДР-полоса: 10 тизеров в день из корпуса дипресёрчей

**Зачем.** Антон сделал 400+ дипресёрчей, они лежали в волте и наружу не выходили.
21.08.2026 он поставил полосу: каждый день 10 тизеров, каждый со ссылкой в публичный
корпус. Корпус тогда же и появился — до этого на гитхабе ДР не было вообще, ссылку
давать было некуда.

**Машинная истина**
- корпус: `https://github.com/tonydzi/deep-research` (клон `[путь владельца]`)
- движки: `$IMPORTS_ROOT/content-factory/dr_lane.py`, `dr_teaser_gate.py`
- журнал публикаций: `$IMPORTS_ROOT/content-factory/_dr_lane/published.jsonl`
- что НЕ публикуем: `$IMPORTS_ROOT/content-factory/dr_lane_denylist.txt`
- длина тира: `episode_adapter.TIER_LEN["dr-teaser"] = (240, 500)`, HARD обе границы

## Шаг 0. Пополнить корпус (если появились новые ДР)

```bash
python "$IMPORTS_ROOT/content-factory/dr_lane.py" build
```

Печатает три числа: сколько ушло в корпус, сколько снял denylist, сколько отсёк leak-gate.
**Появились новые имена в списке — прочитай их глазами.** leak_scan ловит машинные утечки
(номера, хостнеймы, боты), но не умеет судить «это личное» или «это досье на живого
человека». Эту границу держишь ты, и держишь через `dr_lane_denylist.txt` с причиной в
строке. 21.08 первый прогон вынес наружу детские велосипеды семьи и OSINT-досье с
обвинениями в мошенничестве — оба гейта их пропустили, поймали глаза.

Изменился корпус → закоммить и запушь, иначе ссылки в тизерах будут вести в 404:

```bash
cd [путь владельца] && git add -A && git commit -m "..." && git push
```

## Шаг 1. Взять десятку на сегодня

```bash
python "$IMPORTS_ROOT/content-factory/dr_lane.py" pick --n 10
```

Отдаёт карточки: `dr_id`, `title`, `summary`, `findings`, `url`, и сколько осталось в
очереди. Выборка равномерная по всему корпусу, а не «10 свежих» — ресёрчи идут пачками
по одной теме, и подряд взятая десятка даёт десять постов про одно и то же.

## Шаг 2. Написать тизеры

Модель — **Fable** (авторский текст, §6.2). Формат каждого:

1. **зачем гнали** — какой вопрос нас интересовал, своими словами;
2. **что получили** — конкретный результат, с цифрой или именем;
3. 240-500 знаков **тела**. Ссылка и раскрытие авторства в лимит не входят.

Пиши RU и EN версии + короткую версию `x` (тело+ссылка ≤ 280).

Правила голоса: строчными, живо, без длинных тире, без канцелярита. Раскрытие авторства
обязательно первой строкой (§3.3), формулировка «Майкрофт, синтетический кофаундер
Антона. Из корпуса наших дипресёрчей:». **Ничего не выдумывай:** если в карточке нет
результата, бери другой ресёрч, а не додумывай вывод за отчёт.

Сложи в `$IMPORTS_ROOT/content-factory/_dr_lane/teasers-<дата>.json`:

```json
{"date": "...", "teasers": [{"dr_id": "...", "url": "...", "ru": "...", "en": "...", "x": "..."}]}
```

`url` бери **программно из `[путь владельца]`**, не с клавиатуры:
21.08 три ссылки из десяти, набранные руками, дали 404.

## Шаг 3. Гейты (оба обязательны)

```bash
python "$IMPORTS_ROOT/content-factory/dr_teaser_gate.py" check _dr_lane/teasers-<дата>.json
```

Судит длину, живость ссылки (реальный HTTP 200), дедуп по журналу, лимит X, конкретику.
Ненулевой код = не публикуем. **Не заворачивай вывод в пайп** — `| tail` съедает код возврата.

```bash
python "$IMPORTS_ROOT/content-factory/slop_gate.py" --file <тизер.md> --tier dr-teaser
```

Коды slop_gate: `0` OK, `1` WARN (не блокирует), `2` FAIL (блокирует). Считать любой
ненулевой код провалом — ошибка, на ней 21.08 сгорели 20 честных тизеров.

## Шаг 4. Разослать

Каналы (`dr_teaser_gate.py channels`):

| ключ | язык | куда | как |
|---|---|---|---|
| `tg_en` | en | [аккаунт] `-[id]` | MCP telegram, аккаунт `[рабочий аккаунт]` |
| `tg_ru` | ru | [аккаунт] `-[id]` | MCP telegram, аккаунт `[рабочий аккаунт]` |
| `x` | en | [аккаунт] | ⚠️ API 403 (приложение не в Project), рабочий путь = браузер |
| `fb` | ru | стена AntonyDzi | ⚠️ нужен Claude-in-Chrome, IP-гейт §7.2 (только хаб) |

Десять постов подряд в один канал — это флуд. Первый шли сразу, остальные девять ставь
через `mcp__telegram__send_scheduled_message` с шагом ~70 минут на день вперёд. Время в
расписании — **UTC**; Лиссабон = UTC+1 летом.

Рельса лежит → пиши об этом вслух и постишь в живые каналы, а не молчишь про всю полосу.

## Шаг 5. Записать факт

```bash
python "$IMPORTS_ROOT/content-factory/dr_teaser_gate.py" mark <dr_id> --channels tg_en,tg_ru
```

Без этого завтрашний `pick` выдаст тот же ресёрч заново.

## Границы

- Стоп-кран `[шина]/STOP-POSTING.flag`: файл есть → полоса молчит и говорит почему.
  Снимают [коллега] или Антон явным словом, не таймер и не машина.
- Личное, досье на живых людей, серые методы и наша продающая кухня наружу не идут —
  это `denylist`, и решение туда вносит человек, а не эвристика.
- Цифры в тизере = цифры из отчёта. Округлять можно, придумывать нельзя.

## Канон

Правило и разбор граблей: память `dr-teaser-lane` (слаг для гейтов: dr-teaser-lane).
Приказ Антона 21.08.2026, дверь = этот скилл + рутина `auto-hub-260821-dr-teasers-daily`.

## Тест

```bash
python "$IMPORTS_ROOT/content-factory/_test_dr_teaser_gate.py"
```

11 ловушек: каждая — заведомо плохой тизер, тест падает, если гейт его пропустил.


<!--kit-footer-->

---

**Like this skill?** It is one of 100 in [second-brain-starter-kit](https://github.com/tonydzi/second-brain-starter-kit): the second brain we built for ourselves and run every day at Palo Alto AI Research Lab. Install the whole set with `npx skills add tonydzi/second-brain-starter-kit`. Everything is open source and free, so take what you need.

Flagships worth a look on their own: [secondop-panel](https://github.com/tonydzi/secondop-panel) (a second opinion from a panel of external models), [claude-memory-tidy](https://github.com/tonydzi/claude-memory-tidy) (stop your agent's memory from rotting), [telegram-mcp-kit](https://github.com/tonydzi/telegram-mcp-kit) (your own Telegram over MCP in about 15 minutes).

Author: **Anton Dziatkovskii**, Palo Alto AI Research Lab. Telegram [@tonydzi](https://t.me/tonydzi) - WhatsApp [+1 341 222 9178](https://wa.me/13412229178) - X [@Tony_Stef_](https://x.com/Tony_Stef_)

**Engineers: want to test-drive this setup?** Message me. I hand out free starter seeds to engineers who test and report back, and custom skill requests are welcome.
