---
name: kobo-translation
description: "Translation and localization guidelines for KoboToolbox content in French, Spanish, and Arabic. Use when translating KoboToolbox materials including: (1) Academy courses and educational content, (2) User interface text and documentation, (3) Support articles, (4) Marketing materials, (5) Form building terminology, or (6) XLSForm technical terms. Covers tone, pronouns (tú/usted, tu/vous), gender-inclusive language, and official translations for brand terms and UI elements."
---

# KoboToolbox Translation & Localization

## Overview

Translate KoboToolbox content in French, Spanish, and Arabic with consistent terminology, appropriate tone, and cultural adaptation.

**📹 For Video Subtitles/Transcripts:** If you're translating SRT subtitle files, use the **[kobo-translation-srt](../kobo-translation-srt/SKILL.md)** skill extension which includes all base rules plus subtitle-specific guidelines for character limits, spoken language, and chunked translation.

**Translation approach:**

For **NEW FILES** (full translation):
- Translate the complete source document provided
- Use consistent terminology for reliable, repeatable translations
- Follow all guidelines in this skill document

For **UPDATES** (diff-based translation):
- You will receive ONLY the changed content from the source document
- Translate ONLY what is provided between the markers
- Do NOT translate anything outside the markers
- Do NOT add explanations or extra content
- Output ONLY the translated version of the diff content
- The system will automatically merge your translation with the existing translated file

**Why diff-based?** LLMs are non-deterministic, so re-translating an entire document produces slightly different results each time, creating "translation noise" in git diffs. By translating only actual changes, we preserve manual reviewer improvements and reduce unnecessary churn.

## 🚨 CRITICAL: Pre-Translation Checklist

**BEFORE starting translation, read these reference files:**

1. **[brand-terminology.md](references/brand-terminology.md)** - For server names, Question Library, Formbuilder, and ALL brand terms
2. **[ui-terminology.md](references/ui-terminology.md)** - For button names, tabs, and capitalization rules

**Common mistakes to avoid:**
- ❌ Translating server names incorrectly (missing articles or adding extra words)
- ❌ Not including English term on first reference for Formbuilder
- ❌ Missing capital article for "Question Library" / "La bibliothèque de questions" / "La biblioteca de preguntas"
- ❌ Not capitalizing UI terms like "Brouillon" / "Borrador"
- ❌ Using "de" article when it shouldn't be there in French data management terms

## Quick Reference

**Translation types:**
- **OFFICIAL** - Must use EXACT translation character-for-character (brand terms, UI elements, XLSForm terms)
- **Preferred** - Can adapt for context (general terminology, course content)

**Key principles:**
- **ALWAYS check brand-terminology.md FIRST** before translating any brand-related terms
- Prioritize localization over literal translation
- Use gender-inclusive language
- Maintain consistency with KoboToolbox UI
- Apply appropriate formality level (vous/tu, usted/tú)

## Common Translation Pitfalls

### ⚠️ Brand Terms - Most Frequent Errors

| ❌ WRONG | ✅ CORRECT | Notes |
|---------|-----------|-------|
| **Spanish:** Servidor Global de KoboToolbox | **Servidor Global** | Do NOT add "de KoboToolbox" |
| **Spanish:** Servidor de la Unión Europea | **Servidor con sede en la Unión Europea** | Use full official name |
| **French:** serveur KoboToolbox mondial | **Le serveur KoboToolbox mondial** | Must include definite article "Le" (capitalized) |
| **French:** serveur Union européenne | **Le serveur KoboToolbox Union européenne** | Include article AND "KoboToolbox" |
| **Spanish:** la biblioteca de preguntas | **La biblioteca de preguntas** | Capital "L" for brand feature |
| **French:** la bibliothèque de questions | **La bibliothèque de questions** | Capital "L" for brand feature |

### ⚠️ First Reference Rule - Frequently Missed

**Formbuilder MUST include English on first reference:**

| Language | First Reference | Subsequent Uses |
|----------|----------------|-----------------|
| Spanish | editor de formularios de KoboToolbox (Formbuilder) | editor de formularios |
| French | l'interface de création de formulaires KoboToolbox (KoboToolbox Formbuilder) | interface de création de formulaires |

### ⚠️ UI Capitalization - Often Forgotten

| Term | ❌ Wrong | ✅ Correct |
|------|---------|-----------|
| Draft (FR) | formulaire brouillon | formulaire Brouillon |
| Draft (ES) | borrador | Borrador (when in UI context) |

### ⚠️ French Article Usage

| Concept | ❌ Wrong | ✅ Correct | Rule |
|---------|---------|-----------|------|
| Data management | gestion de données | gestion de données | NO article for general concept |
| Managing your data | gérer vos données | gérer vos données | ✓ Correct |
| Projects and data section title | Gestion de projets et de données | Gestion de projets et données | NO "de" before "données" in compound titles |

## Translation Workflow

### Step 0: MANDATORY First Step

**🔴 STOP! Before translating anything:**

1. Identify all brand terms in the source text (KoboToolbox, servers, Question Library, Formbuilder, etc.)
2. Open **brand-terminology.md** and verify EXACT translations
3. Check **ui-terminology.md** for any UI elements (buttons, tabs, page names)
4. Note any terms requiring "English + translation" on first reference

### Step 1: Identify Content Type

**Formal communications** (server announcements, formal emails):
- French: Use "vous", addressee "Cher utilisateur, Chère utilisatrice"
- Spanish: Use "usted", addressee "Estimado usuario/a"

**User Interface**:
- French: Use formal "vous" and "votre"
- Spanish: Use informal "tú"

**Courses and educational content** (INCLUDES SUPPORT ARTICLES):
- French: Use formal "vous" (even for individuals)
- Spanish: Use informal "tú", "ustedes" for plural
- Examples:
  - FR: "Les utilisatrices et utilisateurs débutant(e)s"
  - ES: "Se te dirigirá" (neutral, not "serás dirigido/a")

**Support articles**:
- French: Use formal "vous"
- Spanish: Use informal "tú"
- Apply gender-inclusive language throughout

**Informal communications** (social media, blogs):
- Context-dependent
- Generally use "vous"/"usted" for semi-formal
- May use "tu"/"tú" for very informal contexts

**Video subtitles/transcripts (SRT files):**
- **Use the [kobo-translation-srt](../kobo-translation-srt/SKILL.md) skill extension**
- All base rules apply PLUS subtitle-specific adaptations
- Key differences:
  - XLSForm terms: English only (no translations due to character limits)
  - Character limits: 35-42 characters per line ideal, 50 max
  - Natural spoken language (more conversational than written)
  - Chunked translation approach to preserve context
- Same formality levels as educational content (vous/tú)

### Step 2: Check Terminology Category

**🚨 Brand and product terms** → See [brand-terminology.md](references/brand-terminology.md)
- **OFFICIAL translations must be used EXACTLY** (KoboToolbox, Academy, User Plans, servers, Question Library, etc.)
- **Pay special attention to:**
  - Server names (require articles in French, specific wording in both languages)
  - Question Library (requires capital article in both languages)
  - Formbuilder (requires English + translation on first reference)
  - KoboCollect app name format

**Form building and XLSForm** → See [form-building-terms.md](references/form-building-terms.md)
- Many terms must include English + translation in parentheses
- Video subtitles: English only (character limits)
- Examples: list_name (nom de la liste), cascading select (Sélection en cascade)

**Question types and appearances** → See [question-types.md](references/question-types.md)
- Question appearances in written content: English + translation
- Example: "vertical, picker (sélecteur), rating (notation)"

**UI terminology** → See [ui-terminology.md](references/ui-terminology.md)
- **OFFICIAL translations, capitalize per UI**
- Common UI terms: FORMULAIRE/FORMULARIO, DONNÉES/DATOS, Brouillon/Borrador
- Flag any needed corrections in tracker

**Data collection terms** → See [data-collection-terms.md](references/data-collection-terms.md)
- Preferred translations, adapt for context
- Special rules for management, submissions, data collection

**Documentation website terms** → See [documentation-terminology.md](references/documentation-terminology.md)
- Preferred translations for Help Center content
- Support articles, Getting started patterns, UI element descriptions

**Course and learning platform** → See [course-terminology.md](references/course-terminology.md)
- Preferred translations
- Context-specific adaptations allowed

### Step 3: Apply Gender-Inclusive Language

**French:**
- Use parenthetical markers: "utilisateur(rice)s", "débutant(e)s"
- Use double forms: "Les utilisatrices et utilisateurs"
- Course subtitles: "Vous serez redirigé(e)"

**Spanish:**
- **Strongly prefer neutral constructions:** "Se te dirigirá" instead of "serás dirigido/a"
- **Use double forms for nouns:** "los/as usuarios/as", "las/os participantes"
- When no neutral option exists, use masculine: "los usuarios"
- **Apply throughout:** Every mention of users/people should be inclusive

**Arabic:**
[To be specified based on project needs]

### Step 4: Handle Technical Terms

**XLSForm and form building terms that must stay in English:**
- Written content: English followed by translation in parentheses on first use
- Video subtitles: English only
- Examples:
  - list_name (nom de la liste)
  - XML values (valeurs XML)
  - data column name (nom du champ)

**Cascading select components:**
Always include English + translation approach:
```
"Pour chaque liste d'options, remplissez la colonne list_name (nom de la liste)."
```

## Core Translation Principles

**Localization over literal translation:**
- Adapt idioms and expressions naturally
- Maintain technical accuracy
- Ensure clarity for new users

**Consistency:**
- Use same term for same concept throughout
- Align with KoboToolbox UI terminology
- Flag UI terminology corrections in tracker

**Formatting:**
- Maintain spacing, paragraphs, structure when possible
- Use concise sentences
- Follow target language punctuation conventions
- Avoid slang: "gonna" → "going to"
- **Convert HTML heading tags to markdown format:** `<h2>` → `##`, `<h3>` → `###`, etc.
- Preserve all other HTML tags and attributes (iframe, section, etc.)
- Keep markdown link syntax intact
- Don't translate image paths or URLs

**Acronyms:**
- First use: Full translation followed by acronym in parentheses
- If no common translated acronym exists, use English acronym
- Example FR: "l'Agence des Nations Unies pour les réfugiés (HCNUR)"
- Example ES: "Agencia de las Naciones Unidas para los refugiados (ACNUR)"

**Plain language:**
- Technical content must be beginner-friendly
- Avoid unnecessary jargon
- Prioritize clarity

**Natural language flow:**
- Don't force English sentence structure
- Adapt word order to target language conventions
- Use natural expressions, not literal translations

## Common Translation Patterns

### HTML and Markdown Elements

**Preserve HTML structure:**
- Keep all HTML tags intact EXCEPT heading tags: `<iframe>`, `<section>`, etc.
- **IMPORTANT: Convert HTML heading tags to markdown headings:**
  - `<h1>` → `#` (markdown h1)
  - `<h2>` → `##` (markdown h2)
  - `<h3>` → `###` (markdown h3)
  - `<h4>` → `####` (markdown h4)
  - Example: `<h2>Why KoboToolbox is unique</h2>` → `## Por qué KoboToolbox es único`
- Maintain non-heading attributes: `dir="rtl"`, `id`, `class`, `style`, etc.
- Do NOT translate HTML attributes or parameters

**Metadata and front matter:**
- Preserve "Last updated" lines with dates and GitHub links
- Format: `**Last updated:** <a href="[github-url]" class="reference">[date]</a>`
- Keep the GitHub URL and class unchanged
- Do NOT translate "Last updated" text - keep in English

**Links and cross-references:**
- Preserve markdown link syntax: `[Text](url.md)`
- **Internal documentation links (same language):** Keep relative links as-is - they automatically resolve to the correct language folder
  - Example: In `docs/es/article_a.md`, a link `[other article](article_b.md)` correctly points to `docs/es/article_b.md`
- **Cross-language reference links:** Update the path to point to the correct language directory
  - From Spanish (`docs/es/`), link to:
    - English: `../en/filename.md` → Example: `[Read in English](../en/about_kobotoolbox.md)`
    - French: `../fr/filename.md` → Example: `[Lire en français](../fr/about_kobotoolbox.md)`
    - Arabic: `../ar/filename.md` → Example: `[اقرأ باللغة العربية](../ar/about_kobotoolbox.md)`
  - From French (`docs/fr/`), link to:
    - English: `../en/filename.md`
    - Spanish: `../es/filename.md`
    - Arabic: `../ar/filename.md`
  - From Arabic (`docs/ar/`), link to:
    - English: `../en/filename.md`
    - Spanish: `../es/filename.md`
    - French: `../fr/filename.md`
- Cross-language link text:
  - English: "Read in English"
  - French: "Lire en français"
  - Spanish: "Leer en español"
  - Arabic: "اقرأ باللغة العربية"
- **External links** (https://...) translate the visible text but keep the URL unchanged
  - Example: `[our mission](https://www.kobotoolbox.org/about-us/our-mission/)` → FR: `[notre mission](https://www.kobotoolbox.org/about-us/our-mission/)`

**Images:**
- Keep image paths unchanged: `![image](images/about_kobotoolbox/usermap.png)`
- Do NOT translate image file names or paths

**YouTube embeds:**
- Update language parameters for target language:
  - `cc_lang_pref=fr` for French
  - `cc_lang_pref=es` for Spanish
  - `cc_lang_pref=ar` for Arabic
  - `hl=fr` / `hl=es` / `hl=ar`
- Keep all other iframe attributes unchanged

### Language-Specific Formatting

**Title and heading conventions:**
- English: Title case for main headings ("About KoboToolbox: Accessible Data Collection")
- French: Capitalize first word and proper nouns only ("À propos de KoboToolbox : Collecte de données accessible à toutes et tous")
- Spanish: Capitalize first word and proper nouns only ("Acerca de KoboToolbox: Recolección de datos accesible para todas las personas")
- **CRITICAL: Always use markdown heading syntax (`##`, `###`) NOT HTML tags (`<h2>`, `<h3>`)**
- Note: Some titles may use h1 (`#`), others h2 (`##`) - follow the source document's pattern

**Inclusive language in titles:**
- French: "à toutes et tous" (to all, everyone - feminine and masculine)
- Spanish: "para todas las personas" (for all people)

**Section headers:**
- Use `<h2>` or `<h3>` tags for HTML format, or `##` / `###` for markdown
- French examples: "Pourquoi KoboToolbox est unique", "Soutenir l'impact à échelle mondiale"
- Spanish examples: "Por qué KoboToolbox es único", "Apoyamos el impacto global"
- Note natural language variations: ES "Apoyamos" (we support) vs EN "Supporting" (present participle)

**Arabic (RTL):**
- Wrap Arabic content in `<section dir="rtl">` tags
- Keep heading IDs: `<h1 id="ar">`
- Cross-reference links stay OUTSIDE the RTL section
- Arabic titles are placed inside RTL section with proper heading markup

**Heading levels:**
- Maintain heading hierarchy (h1, h2, h3)
- In Arabic translations, the h1 is inside the RTL section
- Title may be rendered as h2 (##) in some contexts, h1 in others - follow source

### French-Specific Rules

**"Data collection":**
- Default: "collecte de données" (general concept)
- Specific project data: "collecte des données"
- Not: "collecte de données d'enquête"

**"Submission/Record/Response":**
Context-dependent, see [data-collection-terms.md](references/data-collection-terms.md) for full guide:
- Use "soumission" for data management contexts, UI, Data table
- Use "réponse" or "formulaire" when less technical, avoid confusion

**"Upload":**
- Primary: "importer"
- Context: "envoyer" (e.g., send a form)
- Not: "télécharger"

**"View" (UI):**
- "mode" (mode Tableau, mode Carte)
- Not: "affichage" or "aperçu" for UI elements

**Website terms:**
- "site web" not "site Internet"
- "web" lowercase: "formulaire web Enketo"

**Verbs with object pronouns:**
- French naturally places pronouns before verbs: "les rend" (makes them)
- Don't force English word order

**"Getting started with…" translation pattern:**
- DO NOT translate as "Débuter avec" (awkward in French)
- Instead, adapt for context: "Découvrir…", "Introduction à…", "Pour commencer avec…"
- Example: "Getting started with KoboToolbox" → "Introduction à KoboToolbox" OR "Découvrir KoboToolbox"

**"Press" (button):**
- Use "appuyer sur" (not "presser")
- Example: "appuyer sur le bouton Soumettre"

**"Let's go ahead and…" simplification:**
- Simplify and omit "Let's go ahead"
- Example: "Let's go ahead and add the question" → "ajoutons la question"
- NOT: "allons-y et ajoutons la question"

### Spanish-Specific Rules

**"Management":**
- Data/case management: "manejo" (manejo de datos, manejo de casos)
- Teams/projects: "gestión" (gestión de equipos, gestión de proyectos)

**"Collect" (data):**
- Use "recolectar" not "recopilar"

**Gender-neutral when possible:**
- Prefer "Se te dirigirá" over "serás dirigido/a"
- Use masculine when no neutral option: "los usuarios"

**Natural word order:**
- Spanish sentence structure may differ from English
- Example: "makes data accessible" → "permite que los datos sean accesibles" (not literal translation)

### Cross-Language Rules

**"Disaggregate":**
- FR: "désagréger" (not "ventiler")
- ES: "desagregar"

**"Case sensitive":**
- FR: "sensibles à l'utilisation de majuscules et de minuscules" (not "sensible à la casse")
- ES: "distingue entre mayúsculas y minúsculas"

**Organization and context-specific terms:**
- "Social impact" → FR: "impact social" / ES: "impacto social"
- "Practitioners" → FR: "praticiens" (context: data collection practitioners = "mختصين في جمع البيانات" in Arabic)
- "Challenging settings" → FR: "environnements difficiles" / ES: "entornos desafiantes"

**Adapting metaphors and expressions:**
- Don't translate idioms literally
- Example: "accessible to/for" may require restructuring in target language
- French: "rendre accessible" (make accessible) rather than "être accessible à"

## Terminology References

For detailed term-by-term translations, consult these reference files:

- **[brand-terminology.md](references/brand-terminology.md)** - Brand terms, product names, user plans (OFFICIAL) - **READ THIS FIRST**
- **[form-building-terms.md](references/form-building-terms.md)** - Form building, XLSForm, cascading selects (OFFICIAL)
- **[question-types.md](references/question-types.md)** - Question types and appearances (PREFERRED for types, special rules for appearances)
- **[ui-terminology.md](references/ui-terminology.md)** - Formbuilder and KoboCollect UI (OFFICIAL) - **READ THIS SECOND**
- **[data-collection-terms.md](references/data-collection-terms.md)** - Data collection concepts (PREFERRED)
- **[documentation-terminology.md](references/documentation-terminology.md)** - Documentation website and Help Center terms (PREFERRED)
- **[course-terminology.md](references/course-terminology.md)** - Learning platform and course content (PREFERRED)

## Translation Decision Tree

```
START: Do I see ANY of these terms in the source text?
├─ Server names (Global Server, EU Server)?
│  └─ 🚨 STOP → Open brand-terminology.md → Use EXACT translation with articles
│
├─ "Question Library"?
│  └─ 🚨 STOP → Must be "La bibliothèque de questions" / "La biblioteca de preguntas" (capital L)
│
├─ "Formbuilder"?
│  └─ 🚨 STOP → First reference must include English in parentheses
│     ES: "editor de formularios de KoboToolbox (Formbuilder)"
│     FR: "l'interface de création de formulaires KoboToolbox (KoboToolbox Formbuilder)"
│
├─ UI element (button, tab, menu - like DEPLOY, NEW, FORM, DATA)?
│  └─ Check ui-terminology.md → Use OFFICIAL translation → Match UI capitalization
│
├─ Draft / Brouillon / Borrador?
│  └─ Capitalize in UI contexts: "Brouillon" / "Borrador"
│
├─ XLSForm technical term (list_name, cascading select)?
│  └─ Written: English + translation in parentheses
│     Subtitles: English only
│     See form-building-terms.md
│
├─ Question appearance (minimal, picker, rating)?
│  └─ Written: English + translation in parentheses
│     Subtitles: English only
│     See question-types.md
│
├─ Form building or data collection term?
│  └─ Check if OFFICIAL or PREFERRED
│     Apply OFFICIAL exactly; adapt PREFERRED for context
│     See relevant reference file
│
├─ Course or educational content?
│  └─ Use PREFERRED translations
│     Apply appropriate pronoun formality
│     See course-terminology.md
│
└─ Unsure about gender inclusivity?
   └─ Use gender-neutral language
      FR: vous + parenthetical markers (e)
      ES: neutral constructions or tú with "se te"
```

## Enhanced Quality Checklist

Before finalizing translation:

** CRITICAL - Brand & UI Terms:**
- [ ] All server names use EXACT translations from brand-terminology.md (with articles!)
- [ ] "Question Library" has capital article: "La bibliothèque" / "La biblioteca"
- [ ] Formbuilder includes English on first reference
- [ ] All UI elements (buttons, tabs) match ui-terminology.md exactly
- [ ] UI terms capitalized correctly (Brouillon, Borrador, etc.)

**Structure & Formatting:**
- [ ] HTML heading tags converted to markdown (## for h2, ### for h3, etc.)
- [ ] All other HTML tags preserved and unchanged (iframe, section, etc.)
- [ ] Internal documentation links kept as relative paths (they auto-resolve correctly)
- [ ] Cross-language reference links updated to use directory paths (../en/, ../es/, ../fr/, ../ar/)
- [ ] External links: translated text, unchanged URLs
- [ ] Image paths unchanged
- [ ] YouTube embed language parameters updated (cc_lang_pref, hl)
- [ ] Arabic content wrapped in `<section dir="rtl">` tags
- [ ] Heading hierarchy maintained

**Language & Style:**
- [ ] Correct formality level (vous/tu, usted/tú) for content type
- [ ] Gender-inclusive language throughout (especially Spanish double forms)
- [ ] XLSForm/technical terms follow English + translation pattern
- [ ] Consistent terminology (same term for same concept)
- [ ] Plain language, beginner-friendly
- [ ] Proper acronym handling (full term + acronym first use)
- [ ] Target language punctuation conventions
- [ ] No slang or colloquialisms
- [ ] Natural word order (not forced English structure)

**French-Specific:**
- [ ] "collecte de données" (not "collecte des données" unless specific data)
- [ ] "importer" for upload (not "télécharger")
- [ ] Gender-inclusive forms used: "utilisatrices et utilisateurs"
- [ ] Natural pronoun placement: "les rend" not forced English order

**Spanish-Specific:**
- [ ] "recolectar" for collect (not "recopilar")
- [ ] "manejo" for data/case management, "gestión" for teams/projects
- [ ] Gender-inclusive: "los/as usuarios/as" throughout
- [ ] Neutral constructions preferred: "Se te dirigirá"
- [ ] Natural sentence structure adapted from English

## Translation Error Examples

### Real-World Translation Patterns

**Example from actual translations:**

**Source English:**
"KoboToolbox makes high quality data accessible to social impact organizations worldwide."

**✅ CORRECT French (adapted structure):**
"KoboToolbox rend les données de haute qualité accessibles aux organisations à impact social dans le monde entier."

**✅ CORRECT Spanish (adapted structure):**
"KoboToolbox permite que los datos de alta calidad sean accesibles para organizaciones de impacto social a nivel mundial."

**Key observations:**
- French naturally restructures: "makes data accessible" → "rend les données accessibles" (makes the data accessible)
- Spanish restructures differently: "permite que los datos sean accesibles" (permits that the data be accessible)
- Both translations adapt to natural target language expressions rather than forcing English structure

**Source English:**
"Designed by data collection practitioners specifically for challenging settings"

**✅ CORRECT French:**
"Conçu par des praticiens de la collecte de données spécifiquement pour des environnements difficiles"

**✅ CORRECT Spanish:**
"Fue diseñado por personas profesionales de la recolección de datos específicamente para entornos desafiantes"

**✅ CORRECT Arabic:**
"مُصممة من قبل مختصين في جمع البيانات للتعامل مع الظروف الصعبة بشكل خاص"

**Key observations:**
- Spanish uses gender-inclusive "personas profesionales" instead of literal "practitioners"
- Spanish adds "Fue" (was) for natural past tense flow
- Arabic restructures significantly: "designed... for dealing with difficult circumstances especially"
- All prioritize natural expression over literal translation

### Example 1: Server Names
**Source:** "Most users sign up for an account on our Global KoboToolbox Server."

**❌ WRONG Spanish:**
"La mayoría de los usuarios se registran en nuestro Servidor Global de KoboToolbox."

**✅ CORRECT Spanish:**
"La mayoría de los/as usuarios/as se registran en nuestro Servidor Global."

**Errors fixed:**
1. Removed "de KoboToolbox" (not in official name)
2. Added gender inclusivity: "los/as usuarios/as"

**❌ WRONG French:**
"La plupart des utilisateurs s'inscrivent sur notre serveur KoboToolbox mondial."

**✅ CORRECT French:**
"La plupart des utilisatrices et utilisateurs s'inscrivent sur notre Le serveur KoboToolbox mondial."

**Errors fixed:**
1. Added definite article "Le" (capitalized)
2. Added gender inclusivity: "utilisatrices et utilisateurs"

### Example 2: Question Library
**Source:** "Build a form using a template from the question library."

**❌ WRONG Spanish:**
"Elabora un formulario usando una plantilla de la biblioteca de preguntas."

**✅ CORRECT Spanish:**
"Elabora un formulario usando una plantilla de La biblioteca de preguntas."

**Error fixed:** Capitalized "L" in "La" (brand feature name)

### Example 3: Formbuilder First Reference
**Source:** "Create a new form using the KoboToolbox Formbuilder."

**❌ WRONG French:**
"Créez un nouveau formulaire en utilisant l'interface de création de formulaires KoboToolbox."

**✅ CORRECT French:**
"Créez un nouveau formulaire en utilisant l'interface de création de formulaires KoboToolbox (KoboToolbox Formbuilder)."

**Error fixed:** Added English term in parentheses on first reference

### Example 4: HTML Headings to Markdown

**Source (English with HTML tags):**
```markdown
<h3>Why KoboToolbox is unique</h3>

KoboToolbox is hosted and maintained by the international nonprofit organization...

<h3>Supporting global impact</h3>

KoboToolbox is the most widely used data collection tool...
```

**✅ CORRECT Spanish (converted to markdown):**
```markdown
## Por qué KoboToolbox es único

KoboToolbox es una organización internacional sin fines de lucro...

## Apoyamos el impacto global

KoboToolbox es la herramienta de recolección de datos más utilizada...
```

**❌ WRONG Spanish (keeping HTML tags):**
```markdown
<h3>Por qué KoboToolbox es único</h3>

KoboToolbox es una organización internacional sin fines de lucro...
```

**Error fixed:** Converted HTML `<h3>` tags to markdown `##` (since h3 corresponds to ##)

**Key observations:**
- Always convert HTML heading tags to markdown format
- Maintain the heading level: h1→#, h2→##, h3→###, h4→####
- Keep all other HTML tags (iframe, section, etc.) intact

### Example 5: Internal and Cross-Language Links

**Source (English file in `docs/en/p_codes.md`):**
```markdown
# Including P-Codes in the Output Data

[Lire en français](../fr/p_codes.md) | [Leer en español](../es/p_codes.md)

If using cascading lists, please [follow the instructions](cascading_select.md)
for cascading selects.
```

**✅ CORRECT Spanish translation (file in `docs/es/p_codes.md`):**
```markdown
# Incluir P-Codes en los datos de salida

[Read in English](../en/p_codes.md) | [Lire en français](../fr/p_codes.md)

Si utilizas listas en cascada, por favor [sigue las instrucciones](cascading_select.md)
para selecciones en cascada.
```

**Key observations:**
- Internal doc link `cascading_select.md` stays as-is (relative path auto-resolves to `docs/es/cascading_select.md`)
- Cross-language links updated to use directory structure (`../en/`, `../fr/`)
- Link text translated appropriately for each language

**❌ WRONG Spanish translation:**
```markdown
[Read in English](p_codes.md) | [Lire en français](p_codes_fr.md)

Si utilizas listas en cascada, por favor [sigue las instrucciones](cascading_select_es.md)
```

**Errors:**
- Cross-language links don't specify the language directory
- Internal link incorrectly uses `_es` suffix instead of relying on relative path

### Example 6: Natural Language Flow

**Source:** "To support our nonprofit users, we provide our tools for free under the Community Plan."

**✅ CORRECT French (natural structure):**
"Pour soutenir nos utilisateurs sans but lucratif, nous fournissons nos outils gratuitement dans le cadre du plan Community."

**✅ CORRECT Spanish (natural structure):**
"Para apoyar a nuestros usuarios sin fines de lucro, proporcionamos nuestras herramientas de forma gratuita bajo el plan Community."

**Key observations:**
- French: "for free" → "gratuitement" (as adverb, not "pour gratuit")
- French: "under the plan" → "dans le cadre du plan" (in the framework of)
- Spanish: "for free" → "de forma gratuita" (in free form)
- Spanish: "nonprofit users" → "usuarios sin fines de lucro" (different word order)

## Notes

**Reporting issues:**
If UI terminology needs correction, flag in comment and record in appropriate tracker or communications channel.

**Working document:**
This is a living guideline. Feedback welcome. More languages and terms will be added.

**Reference documents:**
- KoboToolbox Academy Course Style Guide
- Essentials Translation Glossary (Master)
- Transifex UI translations
- UN Women Gender Inclusive Language (Spanish)
- Clear Global terminology documents
