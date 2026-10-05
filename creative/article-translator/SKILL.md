---
name: article-translator
description: "Translates a news or feature article from one language to another, preserving journalistic register, factual precision, and the editorial voice of the original."
status: stable
category: translation
subcategory: text
version: 1.0
eval_score: 4.44
tags: [translation, article, journalism, languages, precision, register]
---
# Article Translator

## What This Skill Does
Translates a news or feature article from one language to another, preserving journalistic register, factual precision, and the editorial voice of the original.

## When To Use This Skill
- You have a published or near-final article in one language and need a faithful version in another for an international edition or partner outlet
- A foreign-language source article is central to your reporting and you need a working translation before writing your own piece
- You need to produce a same-day translation of a breaking news story for a multilingual newsroom
- You are localizing a feature article for a different market and need a clean baseline translation before cultural adaptation

## What You Need To Provide
**Required:** The full article text in the source language; the target language (e.g., "French," "Brazilian Portuguese," "Simplified Chinese"); the article type (hard news, feature, opinion, interview, analysis).

**Optional:** The target publication's tone or register (broadsheet formal, tabloid accessible, digital conversational); any proper nouns, technical terms, or organization names that must remain untranslated or use a specific approved translation; whether quotes should be translated or left in the original language with a bracketed translation; word count target if the translated version must fit a specific layout.

## How the Assistant Approaches This
1. **Reads the full piece before translating a single word.** Identifies the article's structure (lede, nut graf, body, kicker), tone, register, and any rhetorical devices — puns, wordplay, cultural references — that will need creative adaptation rather than literal translation.

2. **Translates paragraph by paragraph in document order,** maintaining the original's sentence rhythm and paragraph breaks. Prioritizes meaning fidelity over word-for-word correspondence. Where a phrase has no natural equivalent, selects the closest idiom in the target language that preserves the intent and energy of the original.

3. **Preserves journalistic conventions for the target language.** Adjusts dateline formatting, number conventions (commas vs. periods in large figures), title conventions, and attribution phrasing to match standard journalistic practice in the target language. Does not impose source-language conventions on the output.

4. **Handles quotes with care.** By default, translates quoted speech into the target language. If the user requests original-language quotes, retains them with a bracketed translation immediately following. Speaker attributions follow the target language's standard journalism conventions (e.g., "said" placement varies by language).

5. **Flags translation decisions.** After the translated text, provides a brief translator's note listing any significant choices: cultural references adapted, idioms replaced, ambiguous passages where two readings were possible, or terms where the user should confirm the preferred translation.

## Output Format
Full translated article, matching the original's length within 10%. Same paragraph structure and formatting as the source. Headline and sub-headline translated. After the article, a "Translator's Notes" section (3–8 bullet points) flagging significant decisions. Tone matches the register specified by the user or, if unspecified, mirrors the register of the original. No commentary within the article body — all notes are appended.

## Quality Criteria
- [ ] Every factual claim in the original appears in the translation — nothing omitted, nothing added
- [ ] Register and tone match the original (formal stays formal, conversational stays conversational)
- [ ] Proper nouns are handled consistently — either translated according to convention or retained, not mixed randomly
- [ ] Quotes are attributed using the target language's standard journalistic conventions
- [ ] Numbers, dates, and measurements follow target-language formatting norms
- [ ] Cultural references are adapted where necessary, not translated literally into nonsense
- [ ] Translator's notes flag every significant decision so the editor can review them
- [ ] The translation reads as though it was originally written in the target language — no "translationese"

## Example

### Input
**Source language:** English
**Target language:** French
**Article type:** Feature
**Register:** Broadsheet formal

**Article text:**

**Headline:** The Architects Rebuilding Cities Without Cars

**Sub-headline:** A new generation of urban planners is designing neighborhoods where the automobile is an afterthought — and residents are lining up to move in.

The first thing you notice about Elm Quarter is the silence. No idling engines. No horns. No SUVs backing into spaces too small for them. Instead: birdsong, a fountain, and the rhythmic click of a bicycle freewheel.

Elm Quarter, a 12-hectare development on the eastern edge of a mid-sized European city, is one of a growing number of neighborhoods designed from scratch to make car ownership unnecessary. There are no parking garages. No drive-throughs. The widest road in the district is five meters across — just enough for an emergency vehicle.

"We didn't ban cars," says lead architect Sofia Ekman. "We simply designed a place where you don't need one. That's a very different proposition."

The development houses 3,200 residents in mid-rise buildings arranged around courtyards. A tram stop at the northern edge connects to the city centre in 14 minutes. Grocery stores, a primary school, and a medical clinic sit within a five-minute walk of every front door.

### Output

**Titre :** Les architectes qui reconstruisent des villes sans voitures

**Sous-titre :** Une nouvelle generation d'urbanistes concoit des quartiers ou l'automobile est reléguée au second plan — et les habitants se bousculent pour y emménager.

La premiere chose que l'on remarque a Elm Quarter, c'est le silence. Pas de moteurs au ralenti. Pas de klaxons. Pas de SUV manoeuvrant dans des places trop étroites. A la place : des chants d'oiseaux, une fontaine et le cliquetis régulier d'une roue libre de vélo.

Elm Quarter, un aménagement de 12 hectares situé en bordure est d'une ville européenne de taille moyenne, fait partie d'un nombre croissant de quartiers concus de toute piece pour rendre la voiture individuelle superflue. Pas de parkings souterrains. Pas de service au volant. La voie la plus large du quartier mesure cinq metres — juste assez pour un véhicule de secours.

« Nous n'avons pas interdit la voiture, explique l'architecte en chef Sofia Ekman. Nous avons simplement concu un endroit ou l'on n'en a pas besoin. C'est une proposition tres différente. »

Le quartier abrite 3 200 résidents dans des immeubles de hauteur moyenne organisés autour de cours intérieures. Un arret de tramway a l'extrémité nord relie le centre-ville en 14 minutes. Des commerces alimentaires, une école primaire et un cabinet médical se trouvent a moins de cinq minutes a pied de chaque porte d'entrée.

---

**Notes du traducteur**

- « Drive-throughs » traduit par « service au volant », terme courant dans la presse francophone pour désigner les points de restauration rapide accessibles en voiture.
- Les guillemets anglais (" ") remplacés par des guillemets francais (« ») conformément aux conventions typographiques de la presse francophone.
- « Elm Quarter » conservé en anglais : il s'agit d'un nom propre de quartier. Si la publication préfere une traduction (« Quartier de l'Orme »), merci de le préciser.
- « Mid-rise buildings » traduit par « immeubles de hauteur moyenne » plutot que « immeubles R+4 a R+8 » — la formulation technique est disponible si la publication la préfere.
- L'expression « lining up to move in » (sous-titre) adaptée en « se bousculent pour y emménager » — traduction idiomatique plutot que littérale pour conserver l'énergie de la phrase.

## Known Limitations
- The assistant cannot guarantee the accuracy of specialized terminology in highly technical fields (legal, medical, financial). For articles heavy in domain jargon, have a subject-matter expert review the translation before publication.
- Translation quality is strongest for widely spoken languages with large training corpora (English, French, Spanish, German, Portuguese, Chinese, Japanese). For less-resourced languages, expect more literal phrasing and fewer idiomatic adaptations.
- The skill translates text faithfully but does not perform cultural localization — it will not restructure an article to suit a different market's editorial conventions. For that, use Regional Variant Adapter after translation.

## Related Skills
- [quote-translator](../quote-translator/SKILL.md) — translate individual quotes with full attribution context
- [press-release-translator](../../institutional/press-release-translator/SKILL.md) — translate institutional press releases with corporate terminology
- [regional-variant-adapter](../../localization/regional-variant-adapter/SKILL.md) — adapt a translated text for a specific regional market
- [translation-reviewer](../../quality/translation-reviewer/SKILL.md) — quality-check a completed translation
