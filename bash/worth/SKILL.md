---
name: worth
description: "Score how much attention a person deserves: classify them (investor, engineer, student, partner, community, noise, personal), estimate the value they can bring in the next 90 days, their temperature, and the next move. Triggers: /worth, how valuable is <who>, who is <who>, should I reply to <who>, score this person, score this lead."
license: MIT
permissions: [filesystem, shell]
risk_level: local
processes_untrusted_data: true
related: triage, cynical-privateer-help-only-useful, engineer-acquisition-enrichment-not-scraping
version: 1.0.0
---

# /worth — сколько человек стоит нашего внимания

## ⚖️ ШАГ 0 — Библия по лидам

```bash
python ~/.claude/scripts/bible_leads.py --grep <тема>
```

## Одна команда

```bash
python ~/.claude/scripts/people_value.py score --handle [аккаунт]
python ~/.claude/scripts/people_value.py score --name "Ben @ [человек]" --text "его сообщение"
python ~/.claude/scripts/people_value.py score --tg-id [id] --json
```

**Текст его сообщения — самая сильная улика.** Роль в базе часто устарела или её нет
вовсе; то, что человек сам про себя написал сегодня, весит больше. Всегда передавай
`--text`, если сообщение есть.

## Что означает ответ

**Класс** — кто он для наших целей:

| класс | вклад | что с ним делаем |
|---|---|---|
| `investor` | 35 | инвест-ветка, разговор про деньги ведёт Антон (Tier-2) |
| `engineer` | 30 | миссия №2: репо, issue, звезда, приглашение сломать |
| `partner` | 22 | эдвайзер / экосистемный: даёт дистрибуцию |
| `student` | 18 | адепт в своём городе и универе |
| `community` | 12 | уже в нашей группе |
| `other` / `unknown` | 5 | лёгкий CTA, дверь открыта |
| `personal` | 0 | личная жизнь Антона, воронка ни при чём |
| `noise` | 0 | спам, не отвечаем |

**Ценность 0..100** — класс плюс улики: живой код на GitHub (до +20), его собственные
ответы нам (до +15, это ЧЕСТНАЯ теплота, а не наши исходящие), живые звонки (до +10),
температура CRM (до +12), членство в нашей группе, карточка в волте. Минус 10 тому,
кто просит наш капитал, ничего не предлагая взамен (§1.6 циничный капер).

**Тир** решает цену разговора: `A` → Fable 5, `B` → Sonnet, `C` → шаблон 0 токенов,
`P` → отдать Антону, `X` → тишина.

## ⚠️ Как читать честно

1. **Слепые рельсы.** В конце вывода бывает блок «СЛЕПЫЕ РЕЛЬСЫ». Он значит: сюда мы не
   заглянули, и пустота там ничего не доказывает. Вердикт по человеку, у которого рельса
   GitHub закрыта, — это гипотеза, а не факт.
2. **`unknown` ≠ «никто».** Это «в наших базах его нет». Незнакомец с сильным первым
   сообщением может быть ценнее знакомого из CRM.
3. **`confidence: low`** — не спорь с человеком на основании такого вердикта, посмотри
   тред глазами.
4. **Это сильный ПРИОР, а не приговор.** Перед реальным аутричем всё равно читаем живой
   тред (память `lead-base-read-thread-warn-not-block`).

## Пакетом

```bash
python ~/.claude/scripts/people_value.py batch --in очередь.json --out оценено.json
```

Вход — список `{handle, name, tg_id, text}`. Так работает `/triage`.

## Откуда берутся улики

`leads.db` (`leads`, `contacts`, `people`, `person_groups`) · дашборды
`_Dashboards/Engineer-*.html` (доказательство стройки с GitHub) · `07-People/person-*.md`.

⚠️ **Известный долг (замер 06.08.2026):** JSON-кэшей слоя enrichment
(`_imports/eng-enrich/warm_eng.json`) на хабе НЕТ, хотя память их описывает. Уцелели
только дашборды, движок читает их. Вернутся JSON — он переключится сам.

## Тест

```bash
python ~/.claude/scripts/people_value.py selftest
```



<!--kit-footer-->

---

**Like this skill?** It is one of 100 in [second-brain-starter-kit](https://github.com/tonydzi/second-brain-starter-kit): the second brain we built for ourselves and run every day at Palo Alto AI Research Lab. Install the whole set with `npx skills add tonydzi/second-brain-starter-kit`. Everything is open source and free, so take what you need.

Flagships worth a look on their own: [secondop-panel](https://github.com/tonydzi/secondop-panel) (a second opinion from a panel of external models), [claude-memory-tidy](https://github.com/tonydzi/claude-memory-tidy) (stop your agent's memory from rotting), [telegram-mcp-kit](https://github.com/tonydzi/telegram-mcp-kit) (your own Telegram over MCP in about 15 minutes).

Author: **Anton Dziatkovskii**, Palo Alto AI Research Lab. Telegram [@tonydzi](https://t.me/tonydzi) - WhatsApp [+1 341 222 9178](https://wa.me/13412229178) - X [@Tony_Stef_](https://x.com/Tony_Stef_)

**Engineers: want to test-drive this setup?** Message me. I hand out free starter seeds to engineers who test and report back, and custom skill requests are welcome.
