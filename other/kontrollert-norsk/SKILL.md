---
name: Kontrollert norsk
description:
  Kontrollert norsk - teknisk norsk etter klarspråksprinsippene i NS-ISO 24495-1
  og skriveregler fra ASD-STE100. Use when the user asks for documentation in
  Norwegian, mentions "klarspråk", "kontrollert norsk", or one of the standards,
  or wants Norwegian text rewritten to plain technical language.
version: 0.1.0
---

# Kontrollert norsk

Kontrollert norsk er teknisk norsk med et fast begrepsapparat og faste
skriveregler. Skriv bokmål, med mindre brukeren ber om nynorsk.

## Bruk

- **Ny tekst:** skriv teksten etter reglene nedenfor fra første utkast.
- **Eksisterende tekst eller fil:** les hele teksten først. Rett deretter hver
  setning som bryter en regel. Bruk Edit-verktøyet på filer. Skriv revidert
  løpende tekst direkte uten forklaring eller merkelapper.

Teksten er ferdig når hver setning følger alle reglene.

## Regler

### Terminologi

- Bruk ett fast begrep for hvert konsept. Ikke varier med synonymer.
- Bruk konkrete, vanlige og korte ord når de er presise nok.
- Forklar nødvendige fagbegreper første gang de brukes.

### Setninger

- Bruk aktiv form, ikke passiv. Angi hvem eller hva som utfører handlingen.
- Hvis du kan stryke et ord uten å endre meningen, stryk det.
- Ikke skjul handlinger i substantiver. Skriv «systemet validerer
  konfigurasjonen», ikke «validering av konfigurasjonen utføres».
- Unngå vage ord som `enkelt`, `sømløst`, `robust`, `typisk`, `vanligvis`,
  `på en effektiv måte` og `etter behov`, med mindre teksten definerer hva de
  betyr.
- Bruk korte avsnitt, men ikke fjern nødvendig årsak, virkning eller kontekst.

### Prosedyrer

- Skriv én handling per instruksjonstrinn.
- Bruk imperativ: «Åpne filen», ikke «Filen åpnes».
- Plasser vilkåret før handlingen: «Hvis testen feiler, stopp utrullingen.»

### Tone og innhold

- Unngå metaforer, retoriske formuleringer og salgsaktige adjektiver.
- Unngå innledninger som bare beskriver at temaet er viktig.
- Ikke finn på forutsetninger, funksjoner eller begrunnelser.

### Modalitet

Skill tydelig mellom krav, anbefalinger, muligheter og eksempler:

- **skal** - krav
- **bør** - anbefaling
- **kan** - mulighet
