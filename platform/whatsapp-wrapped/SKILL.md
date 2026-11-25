---
name: whatsapp-wrapped
description: Spotify-Wrapped-style recap of WhatsApp, made on this device with nothing uploaded. Two editions. One chat, from a WhatsApp "Export chat" file (.txt or .zip, iOS or Android, any date locale). Or "my WhatsApp wrapped" across ALL your chats, from the WhatsApp Desktop database on a Mac or a folder of exports, with your top people, top groups, busiest day, streak, voice notes, reply speed, languages and an archetype. Outputs a self-contained HTML page and 9:16 PNG story cards, plus a share-safe version that hides friends' names. Use when someone asks for a WhatsApp Wrapped, a WhatsApp year in review, stats of a chat or of all their chats, who they text most, chat awards, or story cards from WhatsApp.
license: Apache-2.0
metadata:
  version: "1.1.0"
---

# WhatsApp Wrapped

A Spotify-Wrapped-style recap of WhatsApp, made on this device.

## Always use the bundled renderer (read first)

The designed cards (cream cover with the sky image, blue bar charts, emoji card, awards, "made with Edge" footer)
come ONLY from `scripts/wrapped.py`. Never write your own parser, HTML page, chart or card, and never "improve" the
output by hand. If the script fails, fix the input or the flags, or report the error; do not fall back to
freestyling. Run one of the exact commands below, then do Step 4.

## Privacy rules

- Use only the source the user agrees to: an export they point you to, a folder of exports, or the WhatsApp Desktop
  database on this Mac after they say yes. Never search the disk for other chat files, and never pull messages
  through any other tool, connector, API or server (no WhatsApp bridges, no inbox tools, no remote machines).
- Everything stays on this device: the scripts use the Python standard library only, the page and cards contain
  no external URLs, and the PNG renderer blocks every network request.
- Never read, open into your own context or quote the chat text, the database, `stats.json`, the page or the
  cards that show names. Report the paths and the numbers the script prints. If you must check a layout, look
  only at a `--share-cards` card.
- The normal cards show names. Before the user shares them, point them to the share-safe version.

## Step 1: which edition, and the first reply

- "Wrap this chat / our group": the **chat edition** from one export.
- "My WhatsApp wrapped", "my year on WhatsApp", "all my chats": the **personal edition**.

If the user has not given you a source yet, your first reply is short and complete, so they can act on it at once:
1. One line on what they get (story cards plus a page, made on this device, nothing uploaded).
2. Personal edition on a Mac: ask "Can I read your WhatsApp Desktop database on this Mac? I copy it to a temp
   folder, read it locally and delete the copy. Nothing is uploaded." Without a Mac or WhatsApp Desktop: the
   two export steps below. Chat edition: the export steps.
3. Unless the request already says which, ask "One chat, or all your chats?" in the same message.
Never reply with only "I need some details".

## Step 2: the source

- **All chats, Mac with WhatsApp Desktop (best: the full history the Mac has synced):** after the user says yes,
  pass `--personal mac`. The script finds the database itself and reads a temporary copy. If it prints that macOS
  blocked access, tell the user to give the terminal Full Disk Access and run again.
- **All chats, no Mac:** 1. on the phone, open each chat you care about > Export chat > Without media; 2. put the
  files in one folder and send the folder path.
- **One chat:** iPhone: open the chat > tap the name > Export Chat > Without Media (a `.zip`). Android: chat > three
  dots > More > Export chat > Without media (a `.txt` or `.zip`).

## Step 3: run it (exactly this)

Personal edition: the full version for you, then the share cards (PNG only, names as initials, no message
text, no word chips) to post:

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/wrapped.py --personal mac --owner "<first name>" --out ~/whatsapp-wrapped/me --open
python3 ${CLAUDE_SKILL_DIR}/scripts/wrapped.py --personal mac --owner "<first name>" --out ~/whatsapp-wrapped/me-share-cards --share-cards
```

(Replace `mac` with the folder of exports when there is no Mac database.)

Chat edition:

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/wrapped.py "<export .zip or .txt>" --out ~/whatsapp-wrapped/<chat> --open
python3 ${CLAUDE_SKILL_DIR}/scripts/wrapped.py "<export .zip or .txt>" --out ~/whatsapp-wrapped/<chat>-share-cards --share-cards
```

Options:
- `--share-cards`: writes ONLY share-safe PNG cards into `--out`: every person "Person #1 · A.L.", every group
  "Group #1", no page, no stats file, and no word chips. Add `--words` to include word chips minus anything that
  looks like a name, place, number or email (words mostly written with a capital letter are dropped).
- `--share-safe`: the full page and cards with names replaced (word chips stay; use `--share-cards` to post).
- `--theme green|edge`: card colours. `green` (default) uses Edge's meadow greens on cream; `edge` is Edge blue.
  The only WhatsApp brand element is the small unaltered glyph on the cover.
- `--open`: opens the finished page in the browser.
- `--owner "Sam"`: personal; the name on the cover ("Sam's WhatsApp, wrapped"). Also kept out of the top words.
- `--since 2026-01-01` / `--until`: personal; the date range. Default: this year so far. `--all-time` for everything.
- `--me "Sam Reed"`: personal from a folder of exports; your name as it appears there. Without it, the sender who
  is in every chat is taken as you.
- `--tz auto|Europe/Berlin`: personal from the database; hours and days. `auto` (default) estimates your local
  time week by week from your quiet hours, so travel does not turn a 2pm peak into 3am.
- `--title "Sunday League"`: chat edition; the chat name to show (needed when the file is called `_chat.txt`).
- `--no-words`, `--date-order dmy|mdy|ymd`, `--no-png`, `--json` (writes `stats.json`, which contains names).

## Step 4: check and hand over

The script prints the range, the totals, what it left out, `page:` and `cards (...):` paths and a `share:` line.
- If there is no `cards (...)` line, no headless browser was found: say so and suggest
  `pip install playwright && playwright install chromium`, then run again. Never replace the cards with your own.
- Give the user the page path (already open with `--open`), the cards folder, and the share-cards summary card as
  the one to post. Mention the "left out" line so the numbers make sense.

What comes out:

- `<folder>/wrapped.html`: one self-contained page with every card and a table. Opens offline, works on a phone.
- `<folder>/cards/NN-*.png`: 1080x1920 story cards, each with the "made with Edge" footer.
  - Chat edition: cover, who talked the most, when the chat comes alive, longest streak, emojis and words, fastest
    replies and who starts, voice notes and media, awards (one per person), summary.
  - Personal edition: cover, volume (sent vs received, chats), top 5 people, top groups, when I text (peak hour,
    busiest day), longest daily streak, voice notes sent vs received, my emojis and words, who replies fastest and
    who I reply to fastest, who I text first, new people this year, languages, archetype, summary.
- The summary card is the one to post if they post only one.

PNG rendering needs a headless Chromium: Playwright for Python if installed, otherwise a local Chrome, Chromium, Edge or
Brave. Without either, the HTML page still has every card; suggest `pip install playwright && playwright install chromium`.

## What it measures

- Messages per person and share, words, words per message; peak hour, weekday split, busiest day; longest streak.
- Top emojis (skin tones, flags and joined emojis count as one).
- Top words: the words a chat keeps coming back to, not the most common ones. Stopwords and chat filler in
  EN, DE, IT and ES (plus short PT and FR lists) are removed, words need 4 or more letters, names of people
  never count, a long message pasted again and again counts once, and the rest are ranked by TF-IDF with each
  conversation as a document.
- Typical reply time: the median time to answer someone else, counting gaps up to 6 hours. In the personal edition
  only one-to-one chats with 150+ messages and 20+ replies rank, and a median under 10 seconds (an auto-reply or a
  bot) is left out.
- A conversation starts after 4 hours of silence.
- Personal edition: broadcast lists, status, channels and your notes-to-self chat are left out, and so are groups
  you barely write in (under 5 messages, or under 2% of a group with 50+ members). One-to-one chats with the same
  saved name are merged (WhatsApp moved many chats to new ids). "New people" = first message inside the range and
  20+ messages, shown only when the source has real history before the range. Languages (EN, DE, IT, ES) are
  counted from function words that belong to one language only. Unsaved numbers are never printed.
- Awards (chat edition): one distinct award per person, each with the number behind it. Archetype (personal
  edition): one headline title and two runner-ups, each scored against a typical-user baseline.

## Formats handled

iOS and Android exports, `.txt` or `.zip`; `[date, time] Name:` and `date, time - Name:`; day-first, month-first and
year-first dates with `/`, `.` or `-`; 24h and 12h clocks (AM/PM, a. m./p. m., vorm./nachm. and others); invisible
direction marks and narrow spaces; multi-line messages; system notices are skipped; edited messages count once.
WhatsApp Desktop for Mac: `ChatStorage.sqlite` (with its `-wal` and `-shm` files when present).

## Testing

```bash
cd ${CLAUDE_SKILL_DIR} && python3 -m unittest discover -s tests -v
python3 tests/make_synthetic.py /tmp/wa-synthetic   # fake chats in 5 export formats, no real data
```

Tests use synthetic chats and a synthetic database only.
