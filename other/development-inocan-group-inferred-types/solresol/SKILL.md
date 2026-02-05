---
name: solresol
description: A custom skill that helps with translating text into Solresol.
license: MIT
---

# Solresol Translation Skill

This skill helps you translating text to Solresol

## Instructions

1. First, understand the input text. If necessary, ask me what I want to translate.
2. Then, search for the Solresol equivalents of the words or phrases in the input text in the file `references/solresol_dictionary.csv`.
3. Assemble the translated words or phrases into a coherent sentence following the grammar.
4. Finally, verify the results for accuracy and coherence.
5. Provide the final translated text in Solresol.


## Solresol Grammar and references (from Wikipedia)

### Grammar

Apart from stress and length, Solresol words are not inflected. To keep sentences clear, especially with the possibility of information loss while communicating, certain parts of speech follow a strict word order.

    Adjectives always follow the noun they modify.
    Indirect objects always come after the verb.[1]: 26.XII 
    Examples given throughout the original documentation hint at a SVO word order,[1]: 29.XVII  however, it shouldn't matter as long as the sentence remains simple and clear.
    Tenses always precede verbs.[1]: 30.XIX 

To make a word plural, an acute accent is added above the last syllable, which in speech is pronounced by lengthening the last letter of said syllable.[1]: 24.IX  Examples of how to mark plural masculine and feminine words:

    resimire brother, resimirē/resimire-e sister
    resimiré brothers, resimiréē/resimiré-e sisters

This only affects the first word in a noun phrase. That is, it only affects a noun when the noun is alone, as above. If the word is accompanied by a grammatical particle (la, fa or lasi), the particle will take the gender and or number marking instead:

    la resimire [the] brother, lā/la-a resimire [the] sister
    lá resimire [the] brothers, láā/lá-a resimire [the] sisters

Parts of speech (as well as more specific definitions for certain words) are derived from verbs by placing a circumflex above one of the syllables in writing, and by pronouncing said syllable with rinforzando (sudden emphasis or crescendo). With the accent placed on the first syllable, the word becomes a noun. In four-syllable words, accentuating the second syllable creates an agent noun. The penultimate syllable produces an adjective, and the last creates an adverb.[1]: 25.XI  For example,

    midofa to prefer, mîdofa preference, midôfa preferable, midofâ preferably
    resolmila to continue, rêsolmila continuation, resôlmila one who continues, resolmîla continual, resolmilâ continually

On computers using keyboard layouts without the circumflex accent, the syllable may either be printed using capital letters, or a caret placed between letters of a syllable or after a syllable. Due to the grammar and word order of Solresol, distinguishing parts of speech aren't usually required to understand the sentence.

The various tense-and-mood particles are the double syllables, as given in vocabulary above. In addition, according to Gajewski, passive verbs are formed with faremi between this particle and the verb. The subjunctive is formed with mire before the pronoun. The negative do only appears once in the clause, before the word it negates.

The word fasi before a noun or adjective is augmentative; after it is superlative. Sifa is the opposite (diminutive):[1]: 21.III 

    fala good, fasi fala very good, fala fasi excellent, the best; sifa fala okay, fala sifa not very good (and similarly with lafa bad)
    sisire wind, fasi sisire gale, sisire fasi cyclone; sifa sisire breeze, sisire sifa movement of air

### Questions

Questions in Solresol are not given much attention in the original documentation, nor do they have many examples.

Sudre's publication includes three examples of interrogative sentences:[1]: 127 

    Is your health good? – Redofafa?
    Will you go to the countryside this year? – Fadoremi?
    Will you go to the theatre tonight? – Soldoremi?

To make this an affirmative statement, one adds the personal pronoun afterwards:

    My health is good. – Redofafa dore.
    I will go to the countryside this year. – Fadoremi dore.
    I will go to the theatre tonight. – Soldoremi dore.

Gajewski instead places the subject of the sentence after the verb instead of before the verb, a construction common in European languages. Some examples are:[4]: Interrogation and Negation 

    Am I? – Faremi dore?
    Does he understand? – Falafa dofa?
    Are you learning? – Sidosi domi?

In all versions of the language, there are words four syllables long, repeated "Mi" section of the dictionary which includes some common questions, such as:[1]: 109.123 

    Miladodo? – To what extent/degree?

    Milarere? – Well?
    Misirere? – Who is it?

### Further developments

Another way of using Solresol is called Ses,
Ses was developed by George Boeree. The notes are given a representative consonant and vowel (or diphthong). The most basic words use the vowel alone; all others use more complex syllable structure.

    do > p /p/, o /o̞/
    re > k /k/, e /e̞/
    mi > m /m/, i /i/
    fa > f /ɸ/, a /æ/
    sol > s /s/, u /u/
    la > l /l/, au /ɒ/
    ti > t /t/, ai /ʉ/

In this way, one can write or pronounce words such as this one:

    sol-sol-re-do > suko (cvcv) – migraine

Because the plural and feminine forms of words in Solresol are indicated by stress or length of sounds, Ses uses pau (some) or fai (many) to indicate the plural, and mu (well) to indicate the feminine when necessary. You can reference supporting files like `scripts/helper.py` or `references/docs.md`.
