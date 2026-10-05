---
name: hyper-research
description: "ГИПЕР-РЕСЁРЧ: один вопрос уходит в максимум НЕЗАВИСИМЫХ LLM разом (рельса = вендор#аккаунт: Claude x3 бака, ChatGPT x2, Gemini, Grok, GLM, Mistral), каждая в самом сильном режиме думания с ДОКАЗАТЕЛЬСТВОМ режима. Пол 3, кворум 4 — синтез сразу, опоздавших добирает суточный доборщик. Транспорт делегируется /dr-fanout. Триггеры: /hyper, гипер-ресёрч, прогони вопрос по максимуму LLM."
version: 1.0.0
---

# /hyper — одно исследование, максимум независимых голов

> Приказ Антона 14.09.2026: «каждый deep research запускать сразу в максимальном количестве LLM,
> минимум в 3; цель — как можно больше НЕЗАВИСИМЫХ исследований».

⛔ **Это НЕ второй транспорт.** Разнос промпта, сбор, синтез, кворум живут в `/dr-fanout` и
`dr_queue.py` — там же и остаются. `/hyper` добавляет ровно три вещи, которых там не было, и
делегирует всё остальное вниз (та же схема, что `/rr` → `/retro`).

| Что нового | Прибор | Красный тест |
|---|---|---|
| рельса = **вендор#аккаунт** (9 живых ног вместо 6) + лок профиля по полному id | `~/.claude/dr_rails.json` + `dr_rails_registry.py` | `_test_dr_rails_registry.py` |
| **доказанный** максимальный режим думания у каждой ноги | поле `max_reasoning.proof` в реестре | там же, кейс 5 |
| **добор опоздавших** после закрытия кворумом | `dr_latecomer_sweep.py` | долг виден на живых данных |
| **цель без двери заказать нельзя** (одна схема имён на заказ и на сбор) | `dr_doors.py` + гейт в `dr_queue new` | `_test_dr_door_gate.py`, красный показан мутацией 14.09 |

Тизер после синтеза собирает `dr_post_draft.py` — **единственный** источник этой работы
(мой близнец `dr_flash_teaser.py` убит в `_scratch` 14.09, чтобы не было двух писателей).

## Шаг 0. RECALL и дедуп (§8.4)
```bash
python "$IMPORTS_ROOT/brain_ask.py" "<тема>"
```
Уже исследовали → поднимаем старый отчёт, второй раз не заказываем.

## Шаг 1. Набрать веер
```bash
python ~/.claude/scripts/dr_rails_registry.py pick --n 6
python ~/.claude/scripts/dr_rails_registry.py doors
```
⭐ CLI-ноги Claude (`claudecli#a2`, `claudecli#bb`) — полноценные ДР-рельсы, а не суррогат: замер 14.09.2026 на обоих баках вернул живые URL с материалом, датированным ТЕМ ЖЕ ДНЁМ, то есть веб-поиск работает и ссылки настоящие. Двери у них CLI (`dr_headless_dispatch.py --rails claude-a2`).

`pick` берёт СНАЧАЛА по одной ноге на вендора и лишь потом вторые/третьи ноги того же вендора:
шесть вкладок одного вендора — не шесть мнений. `doors` печатает ноги без доказанной двери —
это **долг, а не приговор** (`perplexity#web`: 0 кук во всех Firefox-профилях этого узла,
следы в бэкапе кук Chrome есть ⇒ дверь возможна через Chrome-MCP, но НЕ проверена; честная
формулировка — «я не нашёл двери», а не «её нет», §5.4).

Пол — 3 ноги. Заказали 3 → кворум станет 3, а не 4 (`quorum()` = `min(4, len)`), заказ не
повиснет в ожидании несуществующей четвёртой.

## Шаг 2. Заказать и разнести — делегирование в /dr-fanout
```bash
python ~/.claude/scripts/dr_start.py "<тема>" --for "<потребитель>" --for-why "<зачем>"
# без --targets дефолт = ВСЕ ноги реестра, у которых есть дверь (сейчас 8);
# нужен свой список — можно писать и id реестра: --targets "claudecli#a2,glm#web"
```
⭐ **ИМЯ ЦЕЛИ НЕ ПЕРЕВОДИТСЯ РУКАМИ — БОЛЬШЕ НИКОГДА** (корень класса `dr-quorum-unreachable-doorless-rail`, починен 14.09.2026). Здесь раньше стояла таблица «переводи руками `claudecli#a2` → `claude-a2`» — и это и был корень: ручной перевод не с чем сверить, он не падает, он молчит, а заказ на несуществующую цель уходил в вечный долг (замер: DR26-09-14-ZB-10-2009 заказан на 8 целей, две без двери, уехал в delivered на 4/8).
Теперь имя берётся готовой строкой, а `dr_start` понимает и форму `вендор#аккаунт`:
```bash
python ~/.claude/scripts/dr_rails_registry.py targets   # готовая строка для --targets
python ~/.claude/scripts/dr_doors.py list               # у каких целей ЕСТЬ дверь
```
⛔ Заказать цель без двери теперь НЕЛЬЗЯ: `dr_queue new` падает до создания манифеста (тест `_test_dr_door_gate.py`, показан красным мутацией). Нужна цель, двери у которой ещё нет, — сперва строй дверь (`dr_ff_rail.RAILS` / `dr_headless_dispatch.RAILS`), либо заказывай осознанно впрок через `DR_ALLOW_DOORLESS=1` и в тот же заход строй дверь.
Дальше — механика `/dr-fanout` (она решает: живой Chrome-MCP или headless Firefox; Grok
**никогда** в безлюдный демон — xAI AUP). К телу промпта идёт add-on максимального режима:

> Думай максимально глубоко и долго, включи самый сильный доступный в этом аккаунте режим
> рассуждения. Ответ нужен максимально качественный, подробный и продуманный: с источниками,
> датами, оценкой уверенности и явным указанием, где данных не хватает.

**Перед Send доказать режим.** У каждой ноги в реестре есть `proof` — что обязано быть ВИДНО:
чип `Deep research` у ChatGPT, пилюля у Gemini, оба тумблера у GLM (`glm_probe.js`), непустой
thinking-блок у Claude CLI. Не увидел → нога `no-deepthink`: в кворум **сбора** идёт, в кворум
**подтверждения** — нет. Причина: тариф второго аккаунта ≠ тариф первого, нога молча
скатывается на базовую модель и приносит красивый пустой текст.

⚠️ Параллельные ноги ОДНОГО вендора обязаны брать лок по полному id, иначе три Claude-ноги
затирают куки друг друга:
```bash
python ~/.claude/scripts/dr_rails_registry.py lock --rail claudecli#a2   # BUSY = ногу ведёт сосед
```

## Шаг 3. Кворум и синтез
4 из 6 → синтез **немедленно**, оставшихся не ждём. В синтезе назвать вслух: сколько ног дошло,
кто молчит, у кого не доказан deep-think.

## Шаг 4. Тизер в том же заходе
```bash
python ~/.claude/scripts/dr_post_draft.py --id <DR-ID> --topic "<вопрос>" --audience "<кому полезно>" \
  --verdict "<главный вывод>" --collected <сколько дошло> --ordered <сколько заказано> \
  --why "<что искали>" --link <ссылка на корпус/синтез>
```
Тело 240-300 HARD, ссылок в теле нет; атрибуция (заказал Tony Dzi (Anton Dziatkovskii) ·
Palo Alto AI Research Lab · available for hire · Calendly · Linktree · WhatsApp) — в первом
комментарии. Иначе не влезает: тело + футер = 600-700 знаков. Формулировки берутся из
`_STYLE-footer.md`, не сочиняются. Число LLM в теле = реально дошедшие ноги.

## Шаг 5. Финиш заказа (§9.1)
`applied` с «что поменяли» либо `parked` с «почему не берём». `synthesized` навсегда = потраченная квота.

## Шаг 6. Добор опоздавших (суточно, безлюдно)
```bash
python ~/.claude/scripts/dr_latecomer_sweep.py            # показать долг
python ~/.claude/scripts/dr_latecomer_sweep.py --apply    # добрать
```
Закрытие кворумом больше не теряет хвост: замер 14.09 — 4 заказа, 10 ног висели недобранными и
их не искал никто. Синтез после добора **не перезапускается сам** — добор может сдвинуть вывод,
это решение человека.

## Потребители (§9.3-тер)
Человек: **Антон** (печатает `/hyper`). Робот: суточный прогон Шага 6. Соседи и граница:
`/dr-fanout` = транспорт (вызывается отсюда), `/dr-teasers` = равномерная полоса по СТАРОМУ
корпусу, `/hyper` = ОДИН свежий ресёрч от заказа до тизера.

**Нужен Claude**: Шаг 2 в живом режиме опирается на Chrome-MCP. Ноги `cli` и `ff` работают у
любого агента (§9.3-тер, пишем для любого агента).


<!--kit-footer-->

---

**Like this skill?** It is one of 100 in [second-brain-starter-kit](https://github.com/tonydzi/second-brain-starter-kit): the second brain we built for ourselves and run every day at Palo Alto AI Research Lab. Install the whole set with `npx skills add tonydzi/second-brain-starter-kit`. Everything is open source and free, so take what you need.

Flagships worth a look on their own: [secondop-panel](https://github.com/tonydzi/secondop-panel) (a second opinion from a panel of external models), [claude-memory-tidy](https://github.com/tonydzi/claude-memory-tidy) (stop your agent's memory from rotting), [telegram-mcp-kit](https://github.com/tonydzi/telegram-mcp-kit) (your own Telegram over MCP in about 15 minutes).

Author: **Anton Dziatkovskii**, Palo Alto AI Research Lab. Telegram [@tonydzi](https://t.me/tonydzi) - WhatsApp [+1 341 222 9178](https://wa.me/13412229178) - X [@Tony_Stef_](https://x.com/Tony_Stef_)

**Engineers: want to test-drive this setup?** Message me. I hand out free starter seeds to engineers who test and report back, and custom skill requests are welcome.
