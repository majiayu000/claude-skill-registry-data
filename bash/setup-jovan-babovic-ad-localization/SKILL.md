---
name: setup
description: Interview the user about their company, buyers, ad platforms, target markets, tone per language, names never to translate and claims that need care, then write config/company.md, config/markets.json and config/glossary.md for the ad-localization job. Use when the user types /setup or wants to change their markets, languages, tone or glossary.
disable-model-invocation: true
allowed-tools: Edit(./config/**) Bash(python3 scripts/job.py *) Bash(python3 scripts/reset_image_text.py *) Bash(which *) Bash(python3 --version) Bash(python3 -m venv .venv) Bash(.venv/bin/pip install -r requirements.txt) Bash(.venv/bin/python -c "import PIL, numpy") WebFetch
---

# /setup: get to know the company, then write config/

You are setting up the ad-localization job for a marketer. Plain words, no jargon. **Ask one question at a time.**
When a question has clear options, use the AskUserQuestion tool, put your recommended option first and mark it
"(Recommended)" with a short reason. Look facts up yourself (their website) and only ask what is genuinely their call.
Never ask for an API key.

## 0. Check the computer

Run `which python3 ffmpeg ffprobe claude swift` and `python3 --version`. If `.venv/` exists, also run
`.venv/bin/python -c "import PIL, numpy"`.
Tell the person, in one or two lines:
- Python must be 3.9 or newer; the `python3` that comes with macOS works (https://www.python.org/downloads/).
- Image ads and text on screen in videos need a Mac (text detection uses Apple's built-in OCR through `swift`) and
  Pillow plus NumPy in this folder's own Python environment. If `.venv/` is missing, offer to make it (free, about a
  minute): `python3 -m venv .venv`, then `.venv/bin/pip install -r requirements.txt`. The scripts use `.venv`
  by themselves once it exists; every command stays `python3 scripts/...`.
- FFmpeg is only needed for video ads (https://ffmpeg.org/download.html; on a Mac with Homebrew: `brew install ffmpeg`).
Missing tools do not stop the setup; just say what will not work until they are installed. These four are all the
kit needs. Anything else you notice on this computer (Chrome, a speech-to-text model, extra fonts) is a bonus:
never make a step depend on it.

## 1. Start

If `config/markets.json` already exists, run `python3 scripts/job.py config`, show the summary and ask what they
want to change. Change only that, then go to step 4.

Otherwise ask: **"Set up your own company now, or first watch it work on a sample?"**
- "Set up my company (Recommended): about 10 questions, 5 minutes"
- "Try the sample first: type /localize example, then come back to /setup"

## 2. The interview (one question per message)

1. **Company and website.** Then read their homepage with WebFetch (and a localized version if the site has one,
   such as /fr or /es). Tell them in two or three lines what you found: what they sell, product names, any
   languages the site already has.
2. **Who buys (ICP).** Propose one or two sentences from the site; ask them to confirm or correct.
3. **Which ads and where they run.** Ask which platforms they advertise on (multi-select): LinkedIn, Google search,
   Meta (Facebook and Instagram), other. The platform sets the character limits (saved in `scripts/limits.json`
   with their official sources). Also ask which formats they want to localize: text, image, video.
   If they have image or video ads, find the brand font: look for `font-family` in the site's CSS, or the font
   service it loads (Google Fonts, Adobe Fonts / `use.typekit.net`). Ask whether that font is installed on this
   computer. If yes, write its file path (one per line, for example `~/Library/Fonts/Brand-Regular.otf`) to
   `config/fonts.txt`; the image and screen tools try those first, then the fonts that ship with macOS. If it is
   not installed, offer the closest font that is: once a sample ad is in `input/`, run
   `python3 scripts/reset_image_text.py detect input/AD.png output/fonts.boxes.json` and
   `python3 scripts/reset_image_text.py fonts input/AD.png output/fonts.boxes.json output/fonts.png`, show the
   sheet (the ad's text next to the same words in its closest fonts) and let them pick. Fonts stay on their
   computer; never copy a font file into this folder. Note which text uses which font (headlines, body, buttons,
   highlighted words) in `company.md` under "Ads and channels": the review pins those fonts, because the automatic
   match can confuse two similar typefaces or weights.
4. **Target markets.** Which languages first (multi-select, offer the languages their site already has first).
   Then, per language, the market variant when it matters: Spanish for Spain or Latin America, Portuguese for
   Brazil or Portugal, French for France or Canada, English for UK or US, Chinese simplified or traditional.
   Norwegian Bokmål gets the code `no` (not `nb`): ElevenLabs lists Norwegian as `no`, so the voice step finds it.
5. **Address and tone, per language.** For example French "vous" (formal) or "tu"; Spanish "tú" or "usted";
   Brazilian Portuguese "você"; German "Sie" or "du"; Japanese polite form. If their own site already uses one,
   recommend that and say so. Otherwise recommend the usual choice for B2B ads in that market and explain it in
   one line. Ask for any tone notes (playful, plain, technical).
6. **Names never to translate.** Propose a list from the site (company, products, features, plan names); ask them
   to add or remove. Generic descriptions ("AI assistant") are translated, names are not. A product name that is
   also an ordinary word (Connect, Insights, Mail) goes under "Names in context" instead: the check counts names
   exactly, so "Connect" under "Never translate" would flag every "Connect your team" that is rightly translated.
7. **Set translations (optional).** Any term they always translate a certain way, or a term to avoid? Offer
   "None for now (Recommended)".
8. **Claims that need care.** Numbers, guarantees, "free" offers and their conditions, awards, compliance
   wording, anything legal has asked them to word carefully. Propose what you saw on the site. For mainland
   Chinese markets, add a standing note: China's Advertising Law (Article 9, item 3) bans "national-level",
   "highest-level", "best" and similar wording, so avoid 最 (most), 第一 (number one), 国家级 and 最佳 unless legal
   has cleared them. Say plainly that this is a reminder, not legal review.
9. **Video ads.** Only if they run video: explain that the job dubs with a ready-made ElevenLabs stock voice
   (never a clone of the speaker), which needs a paid ElevenLabs plan for commercial use
   (https://elevenlabs.io/pricing). Then tell them how to save their key, word for word:

   > Open a new terminal window in this folder and run `python3 scripts/save_key.py`. Paste your ElevenLabs key
   > when it asks (it stays hidden). Please don't paste the key here in the chat.

   If they paste a key into the chat anyway, tell them to delete that key in ElevenLabs and make a new one.

## 3. Write the files

`config/company.md`:

```markdown
# <Company>

## Company and site
## Who buys (ICP)
## Ads and channels
## Voice
## Claims that need care
## Notes for translators

Source: answers given in /setup on <YYYY-MM-DD>; pages read: <urls>.
```

`config/markets.json` (language codes like `fr`, `es`, `pt-BR`, `de`, `ja`, `zh-Hant`; platforms from
`scripts/limits.json`: `linkedin`, `google`, `meta`; any other platform is allowed and is marked "limit not known"
unless you add a limit under `limits`, for example `"tiktok.primary_text": {"recommended": 100}`):

```json
{
  "source_language": "English",
  "platforms": ["linkedin", "google"],
  "markets": [
    {"language": "French", "code": "fr", "market": "France", "address": "vous",
     "tone": "Professional and direct.", "voice_id": null}
  ],
  "limits": {}
}
```

`config/glossary.md` (the job reads the bullet list under "Never translate" exactly):

```markdown
# Glossary

## Never translate
- <Company>
- <Product>

## Names in context
- <Product name that is also an ordinary word, if any>

## Preferred wording
| English | French (fr) | Note |
|---|---|---|
```

## 4. Check and finish

Run `python3 scripts/job.py config`. Fix anything it reports and run it again until it says `"ok": true`.
Then finish with a five-line summary (company, markets with address, platforms, names kept, claims to watch)
and the next step: "Drop your ads into `input/` (a CSV of text ads, images, videos), then type `/localize`."
See `input/README.md` for the CSV columns.
