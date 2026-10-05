---
name: fb-likes
description: "Ежедневная лайк-активность в Facebook двумя лейнами. Триггеры «/fb-likes», «/fb-like», «лайк-хвост», «пролайкай комменты», «обход лидов», «полайкай лидов», «дневная активность в фб», «fb likes», «like round»"
version: 1.0.0
---

# /fb-likes — лайки как ежедневная механика, а не разовое действие

> ⛔ **ЛИЧНОСТЬ БРАУЗЕРА (канон 30.08.2026).** Chrome профиля Default на хабе = личность Антона (claude.ai там под **[рабочий аккаунт]**, всегда).
> Робот здесь **ЧИТАЕТ и действует, но НЕ ТРОГАЕТ ЛОГИНЫ**: ни logout, ни смены аккаунта, ни «самолечения входа», ни инжекта кук.
> Увидел «не тот аккаунт» → доложи и работай из робо-профиля (`_chrome_profile_a2`, Firefox-профили). Канон: `reglament-hab-brauzernye-lichnosti-bb-i-roboty`.

**Зачем.** Голосовая Антона 04.08.2026: «все наши посты и комментарии должны получать лайки — это ничего не стоит, а людям приятно», плюс отдельная задача — каждый день заходить к 5–10 случайным лидам с реальным контактом и лайкать их. Ключевое слово — **КАЖДЫЙ ДЕНЬ**: важна не разовая пробежка, а то, что активность в аккаунте есть постоянно.

**До этого было покрыто ровно одно:** шаг 7 в `/fb-post` — селф-лайк своего поста. Комменты под нашими постами, наши собственные ответы и обход лидов не покрывал никто.

---

## ⛔ ШАГ 0 — где можно исполнять (проверяй ВСЕГДА, до браузера)

```bash
python -c "import os;print(os.environ.get('COMPUTERNAME'))"
```

- Хаб `[машина флота]` → работаем.
- Любая другая машина → **боевые лайки отсюда НЕ ставим** (CLAUDE.md §7.2, `reglament-ip-sensitive-deystviya-tolko-s-haba`: FB-действия идут с постоянного IP хаба). С не-хаба можно всё, кроме браузера: чинить ростер, смотреть счётчик, готовить список. Работу текстом на хаб через шину.

---

## ЛЕЙН 1 — хвост публикации (запускается САМ после каждого нашего поста/ответа)

Это не отдельная команда для Антона, а **штатный хвост** `/fb-post` и `/fb-reply`. Отдельно спрашивать не нужно: лайк своего контента обратим, наружу ничего не пишет, не Tier-2.

Порядок под КАЖДЫМ нашим постом:

1. Гейт темпа перед серией:
   ```bash
   python "$USERPROFILE/.claude/scripts/fb_guard.py" check like_own
   ```
   `BLOCKED` (exit 3) → СТОП, доложить, не обходить.
2. **Свой пост** — Like (если ещё не стоит после шага 7 `/fb-post`).
3. **Все комментарии под постом** — Like каждому. Минимум топовые, цель — все. Свои ответы в тредах тоже (Антон назвал это явно).
4. **Наши собственные комментарии** (футер-коммент, ответы) — Like им же.
5. После КАЖДОГО поставленного лайка:
   ```bash
   python "$USERPROFILE/.claude/scripts/fb_guard.py" record like_own
   ```
6. Один раз на пост — запись в счётчик механики:
   ```bash
   python "$USERPROFILE/.claude/scripts/fb_like_roster.py" record --person "<permalink поста>" \
       --kind own --outcome ok --note "пост + N комментов"
   ```

**Грабли браузера.** Кнопка `Like` в строке `Like · Reply · Hide` — кликать ПО КООРДИНАТЕ из свежего скриншота, не по `find`-ref (та же грабля, что описана в `/fb-reply` §4: ref уводит фокус на Close модалки). Перед кликом убедиться, что лайк ещё не стоит (уже лайкнутая кнопка синяя/жирная) — повторный клик СНИМАЕТ лайк.

**Что НЕ лайкаем в лейне 1:** ничего за пределами нашего поста. Лента, чужие посты, рекламные комменты и тролли — не сюда.

---

## ЛЕЙН 2 — ежедневный обход лидов (5–10 человек)

### 2.1 Кого берём
Только тех, кто есть в **ростере** — людей с ДОКАЗАННЫМ реальным контактом (звонок или осмысленная переписка). «Лайкать всех подряд» Антон запретил прямым текстом.

```bash
python "$USERPROFILE/.claude/scripts/fb_like_roster.py" pick --n 7
```

Движок сам: берёт случайных (случайно для людей, но стабильно в пределах суток — повторный запуск в тот же день не даёт второй круг), исключает тех, кого лайкали за последние 14 дней, показывает, кто уже отработан сегодня.

- Вернул `⚠️ меньше 5 человек` → это **не повод импровизировать и добирать людей из ленты**. Отработать сколько есть и сказать Антону, что ростер надо пополнять.
- `exit 4` (ростер пуст) → лейн сегодня не идёт, доложить.

### 2.2 Как лайкаем
На каждого человека из списка:

1. Гейт: `python "$USERPROFILE/.claude/scripts/fb_guard.py" check like_lead` → `BLOCKED` = стоп на сегодня.
2. Открыть его профиль по `fb_url` из выдачи `pick`.
3. Лайкнуть **1–2 свежих поста** (не больше). Старую ленту не листать, годовалые посты не трогать — это выглядит как бот-обход.
4. `python "$USERPROFILE/.claude/scripts/fb_guard.py" record like_lead` после каждого лайка.
5. Записать факт:
   ```bash
   python "$USERPROFILE/.claude/scripts/fb_like_roster.py" record --person <slug> --kind lead \
       --outcome ok --target "<ссылка на пост>"
   ```
   Профиль закрыт / нечего лайкать / свежих постов нет → `--outcome fail --note "<причина>"`. Это НЕ ошибка, это факт для счётчика; человек останется в пуле.

### 2.3 Пополнение ростера

**Источник №1 — те, кто лайкает НАС** (приказ Антона 05.08: «лайк поста чужого человека — из тех,
кто нас часто лайкает»). Это самый объёмный и самый честный источник: человек уже проголосовал
вниманием. Собирается скиллом `/fb-audience`, оттуда в ростер одной командой:
```bash
python "$USERPROFILE/.claude/scripts/fb_audience.py" promote --min-likes 3
```

**Источник №2 — треды FB Messenger**: там человек уже = FB-профиль, склеивать ничего не нужно.

```bash
python "$USERPROFILE/.claude/scripts/fb_like_roster.py" add --slug ivan-petrov --name "Иван [человек]" \
    --fb-url "https://www.facebook.com/ivan.petrov" --proof "звонок 2026-07-12" --source messenger
```

`--proof` обязателен — это и есть барьер «только лиды с реальным контактом».

Автосбор из карточек волта (идемпотентный, ничего не затирает):
```bash
python "$USERPROFILE/.claude/scripts/fb_like_roster.py" seed
```

---

## Счётчик и «была ли активность сегодня»

```bash
python "$USERPROFILE/.claude/scripts/fb_like_roster.py" status --days 30
```
Показывает размер ростера, лайки по лейнам, **сколько дней из 30 была активность** и предупреждает, если тишина ≥2 дней (Антон просил каждый день).

---

## Стоп-краны

- Любое предупреждение FB (checkpoint, «вы делаете это слишком часто», запрос подтверждения личности) → **немедленно СТОП**, доложить, не ретраить.
- Кап `like_lead` (20/день) — потолок из голосовой (5–10 человек × ≤2 лайка). Хочется выше → **не поднимать самому**, спросить Антона: `python ~/.claude/scripts/approval.py ask`.
- Не лайкать людей вне ростера. Не лайкать чужие комментарии под чужими постами. Не лайкать в группах.
- Снятый лайк (двойной клик) — считать сбоем, поправить и записать `--outcome fail`.

## Связанное

- 🗺 **Общая карта FB-рельсы (читать первой):** `~/.claude/scripts/docs/fb-rails.md` — где лежат данные, все капы, IP-гейт, общие грабли браузера + замер «склейки TG→FB нет».
- `/fb-post` §7 — хвост лейна 1 после публикации; `/fb-reply` §3-бис — хвост после нашего ответа.
- `/fb-messenger` — источник людей для ростера.
- Движки: `fb_like_roster.py` (ростер/отбор/счётчик), `fb_guard.py` (темп/объём).
- Паспорт: `~/.claude/scripts/docs/fb_like_roster.md`.
- Канон: голосовая hub:5087 04.08.2026, CLAUDE.md §7.2, память `fb-skill-set`, `comment-to-call-funnel`.


<!--kit-footer-->

---

**Like this skill?** It is one of 100 in [second-brain-starter-kit](https://github.com/tonydzi/second-brain-starter-kit): the second brain we built for ourselves and run every day at Palo Alto AI Research Lab. Install the whole set with `npx skills add tonydzi/second-brain-starter-kit`. Everything is open source and free, so take what you need.

Flagships worth a look on their own: [secondop-panel](https://github.com/tonydzi/secondop-panel) (a second opinion from a panel of external models), [claude-memory-tidy](https://github.com/tonydzi/claude-memory-tidy) (stop your agent's memory from rotting), [telegram-mcp-kit](https://github.com/tonydzi/telegram-mcp-kit) (your own Telegram over MCP in about 15 minutes).

Author: **Anton Dziatkovskii**, Palo Alto AI Research Lab. Telegram [@tonydzi](https://t.me/tonydzi) - WhatsApp [+1 341 222 9178](https://wa.me/13412229178) - X [@Tony_Stef_](https://x.com/Tony_Stef_)

**Engineers: want to test-drive this setup?** Message me. I hand out free starter seeds to engineers who test and report back, and custom skill requests are welcome.
